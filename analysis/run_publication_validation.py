"""Run the separate retrospective publication validation extension.

Original data, submitted documents and production model are read-only inputs.
Public outputs are aggregate records; optional respondent-level QA arrays must
be written outside the repository. AI assistance is recorded in the protocol.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import time

from joblib import Parallel, delayed, parallel_config
import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss
from threadpoolctl import threadpool_limits

import publication_model as model

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "paper/publication/validation_config.json"
DEFAULT_OUTPUT = ROOT / "output/publication_validation"
METRICS = ["roc_auc", "average_precision", "brier", "log_loss",
           "calibration_in_the_large", "calibration_slope",
           "reference_brier", "paired_brier_improvement"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(json_safe(value), indent=2, allow_nan=False) + "\n")


def load_frozen_cohort(config: dict) -> tuple[pd.DataFrame, dict]:
    path = ROOT / config["cohort_path"]
    original = path.read_bytes()
    raw_hash = hashlib.sha256(original).hexdigest()
    windows_hash = hashlib.sha256(original.replace(b"\r\n", b"\n")
                                  .replace(b"\n", b"\r\n")).hexdigest()
    if (raw_hash not in {config["cohort_sha256_raw_expected"],
                         config["cohort_sha256_crlf_expected"]}
            or windows_hash != config["cohort_sha256_crlf_expected"]):
        raise ValueError("Frozen cohort checksum mismatch")
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    if raw.duplicated(["uqno", "personno"]).any():
        raise ValueError("Frozen household/person keys are not unique")
    selected = raw.loc[raw["in_final_cohort"].eq("1")].copy()
    if not selected["eligibility_status"].eq("PASS").all():
        raise ValueError("Frozen final cohort contains a non-PASS row")
    work = model.prepare_frame(selected)
    actual = (len(work), int(work["y_n"].sum()), work["uqno"].nunique(), work["psu"].nunique())
    if actual != (1013, 67, 827, 345):
        raise ValueError("Frozen final cohort counts changed")
    return work, {"path": config["cohort_path"], "raw_sha256": raw_hash,
                  "CRLF_sha256": windows_hash, "source_rows": len(raw),
                  "people": actual[0], "events": actual[1],
                  "households": actual[2], "derived_PSUs": actual[3]}


def tagged(records: list[dict], **metadata) -> list[dict]:
    return [{**metadata, **row} for row in records]


def empty_result(row: dict) -> dict:
    return {"row": row, "folds": [], "inner": [], "grid": [], "coefficients": []}


def failure_audit(result: dict, error: model.UnsupportedSampleError, **metadata) -> None:
    result["inner"].extend(tagged(error.inner_records, **metadata))
    result["grid"].extend(tagged(error.grid_records, **metadata))
    result["folds"].append({**metadata, "valid": False,
                            "final_attempted": error.final_attempted,
                            "final_converged": error.final_converged,
                            "error": str(error)})


def nested_repetition(work: pd.DataFrame, group_col: str, seed: int, config: dict) -> dict:
    """Each person is tested exactly once; all tuning is inside outer training."""
    with threadpool_limits(limits=1):
        result = empty_result({"grouping": group_col, "seed": seed, "valid": False})
        probability = np.full(len(work), np.nan)
        reference = np.full(len(work), np.nan)
        coverage = np.zeros(len(work), dtype=int)
        try:
            folds = model.group_folds(work, group_col, seed, config["outer_folds"])
            for fold in range(config["outer_folds"]):
                train, test = work.iloc[folds != fold], work.iloc[folds == fold]
                if (not set(train[group_col]).isdisjoint(test[group_col])
                        or not set(train["uqno"]).isdisjoint(test["uqno"])):
                    raise AssertionError("Original household or group crossed an outer boundary")
                meta = {"phase": "nested", "grouping": group_col,
                        "seed": seed, "outer_fold": fold + 1}
                try:
                    fitted = model.tune_and_fit(train, group_col, seed + fold + 1,
                                                config["c_grid"], config["inner_folds"])
                except model.UnsupportedSampleError as error:
                    failure_audit(result, error, **meta)
                    raise
                probability[folds == fold] = fitted.predict(test)
                reference[folds == fold] = float(train["y_n"].mean())
                coverage[folds == fold] += 1
                result["inner"].extend(tagged(fitted.inner_records, **meta))
                result["grid"].extend(tagged(fitted.grid_records, **meta))
                result["coefficients"].append({**meta, "C": fitted.selected_c,
                                                **fitted.coefficients_original_scale()})
                result["folds"].append({**meta, "valid": True,
                    "train_people": len(train), "test_people": len(test),
                    "train_households": train["uqno"].nunique(),
                    "test_households": test["uqno"].nunique(),
                    "train_groups": train[group_col].nunique(), "test_groups": test[group_col].nunique(),
                    "train_events": int(train["y_n"].sum()), "test_events": int(test["y_n"].sum()),
                    "reference_probability": float(train["y_n"].mean()),
                    "C": fitted.selected_c, "final_attempted": True,
                    "final_converged": fitted.final_converged, "iterations": fitted.final_iterations})
            if not (coverage == 1).all() or not np.isfinite(probability).all():
                raise AssertionError("Incomplete or duplicated outer-held-out predictions")
            y = work["y_n"].to_numpy()
            measured = model.metrics(y, probability)
            reference_brier = float(brier_score_loss(y, reference))
            result["row"].update({"valid": True, "people": len(work), "events": int(y.sum()),
                **measured, "reference_brier": reference_brier,
                "reference_log_loss": float(log_loss(y, reference, labels=[0, 1])),
                "paired_brier_improvement": reference_brier - measured["brier"],
                "complete_OOF_coverage": True})
            result["qa"] = {"row_position": np.arange(len(work)), "y": y,
                            "p_model": probability, "p_reference": reference,
                            "outer_fold": folds + 1, "coverage": coverage}
        except model.UnsupportedSampleError as error:
            result["row"].update({"error": str(error),
                                   "people_with_predictions": int(np.isfinite(probability).sum())})
        return result


def sample_households(work: pd.DataFrame, seed: int, n_households: int | None = None):
    """Keep multiplicity but group every copy by its original household ID."""
    positions = work.groupby("uqno", sort=True).indices
    keys = np.array(list(positions), dtype=object)
    draw = np.random.default_rng(seed).choice(keys, len(keys) if n_households is None else n_households,
                                             replace=True)
    index = np.concatenate([positions[key] for key in draw])
    bootstrap = work.iloc[index].reset_index(drop=True)
    oob = work.loc[~work["uqno"].isin(draw)].reset_index(drop=True)
    support = {"draws": len(draw), "people": len(bootstrap),
               "unique_households": bootstrap["uqno"].nunique(),
               "events": int(bootstrap["y_n"].sum()),
               "event_households": int(bootstrap.groupby("uqno")["y_n"].max().sum()),
               "oob_people": len(oob), "oob_households": oob["uqno"].nunique(),
               "oob_events": int(oob["y_n"].sum())}
    return bootstrap, oob, support


def bootstrap_replicate(work: pd.DataFrame, seed: int, replicate: int, config: dict) -> dict:
    with threadpool_limits(limits=1):
        result = empty_result({"replicate": replicate, "seed": seed, "valid": False})
        meta = {"phase": "bootstrap", "grouping": "uqno", "seed": seed,
                "replicate": replicate, "outer_fold": 0}
        bootstrap, oob, support = sample_households(work, seed)
        result["row"].update(support)
        try:
            fitted = model.tune_and_fit(bootstrap, "uqno", seed,
                                        config["c_grid"], config["inner_folds"])
            result["inner"].extend(tagged(fitted.inner_records, **meta))
            result["grid"].extend(tagged(fitted.grid_records, **meta))
            result["folds"].append({**meta, "valid": True, "C": fitted.selected_c,
                "final_attempted": True, "final_converged": fitted.final_converged,
                "iterations": fitted.final_iterations})
            result["coefficients"].append({"replicate": replicate, "seed": seed,
                                            "C": fitted.selected_c, **fitted.coefficients_original_scale()})
            measured_boot = model.metrics(bootstrap["y_n"].to_numpy(), fitted.predict(bootstrap))
            measured_original = model.metrics(work["y_n"].to_numpy(), fitted.predict(work))
            prevalence = float(bootstrap["y_n"].mean())
            base_boot = float(np.mean((bootstrap["y_n"].to_numpy() - prevalence) ** 2))
            base_original = float(np.mean((work["y_n"].to_numpy() - prevalence) ** 2))
            result["row"].update({"valid": True, "C": fitted.selected_c,
                **{f"bootstrap_{k}": v for k, v in measured_boot.items()},
                **{f"original_{k}": v for k, v in measured_original.items()},
                "bootstrap_reference_brier": base_boot, "original_reference_brier": base_original,
                "delta_brier": measured_original["brier"] - measured_boot["brier"],
                "delta_roc_auc": measured_original["roc_auc"] - measured_boot["roc_auc"],
                "delta_reference_brier": base_original - base_boot,
                "delta_paired_brier_improvement": (base_original - measured_original["brier"])
                    - (base_boot - measured_boot["brier"]), "oob_valid": False})
            if len(oob) and oob["y_n"].nunique() == 2:
                try:
                    oob_metrics = model.metrics(oob["y_n"].to_numpy(), fitted.predict(oob))
                    oob_baseline = float(np.mean((oob["y_n"].to_numpy() - prevalence) ** 2))
                    result["row"].update({"oob_valid": True,
                        **{f"oob_{k}": v for k, v in oob_metrics.items()},
                        "oob_reference_brier": oob_baseline,
                        "oob_paired_brier_improvement": oob_baseline - oob_metrics["brier"]})
                except model.UnsupportedSampleError as error:
                    result["row"]["oob_error"] = str(error)
            else:
                result["row"]["oob_error"] = "empty_or_single_class"
        except model.UnsupportedSampleError as error:
            # No replacement draw: preserve the originally specified seed and support.
            if not result["inner"]:
                failure_audit(result, error, **meta)
            result["row"].update({"error": str(error)})
        return result


def optimism_summary(apparent: dict, bootstrap: pd.DataFrame) -> list[dict]:
    """Finite-bootstrap Monte Carlo error is not a predictive sampling CI."""
    rows = []
    for metric in ["brier", "roc_auc", "reference_brier", "paired_brier_improvement"]:
        column = f"delta_{metric}"
        series = (bootstrap.loc[bootstrap["valid"], column] if column in bootstrap
                  else pd.Series(dtype=float))
        values = pd.to_numeric(series, errors="coerce").dropna()
        n = len(values)
        mean = float(values.mean()) if n else float("nan")
        rows.append({"metric": metric, "apparent_original": apparent[metric],
                     "valid_replicates": n, "mean_correction": mean,
                     "optimism_corrected_estimate": apparent[metric] + mean,
                     "correction_MCSE": float(values.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan"),
                     "MCSE_interpretation": "finite_simulation_error_not_sampling_SE_or_CI"})
    return rows


def distribution(values: pd.Series) -> dict:
    values = pd.to_numeric(values, errors="coerce").dropna()
    return {"valid_values": len(values), "median": values.median(),
            "q1": values.quantile(.25), "q3": values.quantile(.75),
            "minimum": values.min(), "maximum": values.max()}


def save_csv(out: Path, name: str, records: list[dict], sort_by: list[str]) -> pd.DataFrame:
    frame = pd.DataFrame(records)
    order = [key for key in sort_by if key in frame.columns]
    if order and not frame.empty:
        frame = frame.sort_values(order, kind="stable").reset_index(drop=True)
    frame.to_csv(out / name, index=False)
    return frame


def validate_destinations(output: Path, qa_dir: Path | None, pilot: bool) -> None:
    if output == ROOT or ROOT in output.parents:
        if pilot or not (output == DEFAULT_OUTPUT or DEFAULT_OUTPUT in output.parents):
            raise ValueError("In-repository outputs are restricted to output/publication_validation; pilots must be outside Git")
    if qa_dir is not None and (qa_dir == ROOT or ROOT in qa_dir.parents):
        raise ValueError("Respondent-level QA arrays must be outside the repository")


def validate_config(config: dict, households: int) -> None:
    """Reject configuration drift instead of silently running another procedure."""
    expected = {"candidate": "original_four_settlement_categories_ridge_logistic",
        "slopes": len(model.SLOPE_NAMES), "c_grid": model.C_GRID,
        "solver": "lbfgs", "max_iter": model.MAX_ITER, "tolerance": model.TOL,
        "outer_folds": 5, "inner_folds": 5, "outer_seed_start": 201415,
        "outer_repetitions": 20, "inner_seed_rule": "outer_seed + outer_fold_number_1_based",
        "primary_group": "uqno", "sensitivity_group": "psu",
        "inner_scoring": "pooled_unweighted_person_brier",
        "primary_comparison": "reference_brier_minus_ridge_brier",
        "bootstrap_draws": 1000, "bootstrap_seed_start": 730001,
        "bootstrap_group": "original_household", "bootstrap_inner_seed_rule": "bootstrap_seed",
        "bootstrap_resample_size_households": households,
        "optimism_corrected_metrics": ["brier", "roc_auc", "reference_brier", "paired_brier_improvement"],
        "confidence_intervals_claimed": False, "external_validation_claimed": False,
        "selection_by_outer_scores": False}
    differing = [name for name, value in expected.items() if config.get(name) != value]
    if differing:
        raise ValueError(f"Configuration differs from the recorded procedure: {', '.join(differing)}")


def run(config_path: Path, output: Path, qa_dir: Path | None = None,
        jobs: int = 4, pilot: bool = False) -> dict:
    start = time.monotonic()
    output = output.resolve()
    qa_dir = None if qa_dir is None else qa_dir.resolve()
    validate_destinations(output, qa_dir, pilot)
    config = json.loads(config_path.read_text())
    if jobs < 1:
        raise ValueError("At least one worker is required")
    work, cohort = load_frozen_cohort(config)
    validate_config(config, int(work["uqno"].nunique()))
    seeds = list(range(config["outer_seed_start"], config["outer_seed_start"]
                       + (2 if pilot else config["outer_repetitions"])))
    boot_seeds = list(range(config["bootstrap_seed_start"], config["bootstrap_seed_start"]
                            + (5 if pilot else config["bootstrap_draws"])))
    output.mkdir(parents=True, exist_ok=True)
    if qa_dir is not None:
        qa_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        qa_dir.chmod(0o700)
    inner, grid, fold_audit = [], [], []
    with threadpool_limits(limits=1):
        fitted = model.tune_and_fit(work, "uqno", seeds[0], config["c_grid"], config["inner_folds"])
        apparent = model.metrics(work["y_n"].to_numpy(), fitted.predict(work))
    apparent["reference_brier"] = float(np.mean((work["y_n"] - work["y_n"].mean()) ** 2))
    apparent["paired_brier_improvement"] = apparent["reference_brier"] - apparent["brier"]
    meta = {"phase": "full_candidate", "grouping": "uqno", "seed": seeds[0], "outer_fold": 0}
    inner.extend(tagged(fitted.inner_records, **meta)); grid.extend(tagged(fitted.grid_records, **meta))
    fold_audit.append({**meta, "valid": True, "final_attempted": True,
                       "final_converged": fitted.final_converged, "C": fitted.selected_c,
                       "iterations": fitted.final_iterations})
    write_json(output / "full_candidate.json", {
        "candidate": config["candidate"], "purpose": "retrospective_research_candidate_not_production_model",
        "C": fitted.selected_c, "slopes": model.SLOPE_NAMES,
        "coefficients_original_encoded_units": fitted.coefficients_original_scale(),
        "preprocessing": asdict(fitted.state), "apparent_metrics": apparent,
        "apparent_metrics_are_held_out": False})
    print(f"Full-data development complete; running {2 * len(seeds)} nested repetitions", flush=True)
    nested_rows, outer_coefficients = [], []
    with parallel_config(backend="loky", inner_max_num_threads=1):
        tasks = ((group, seed) for group in ["uqno", "psu"] for seed in seeds)
        results = Parallel(n_jobs=jobs, return_as="generator")(
            delayed(nested_repetition)(work, group, seed, config) for group, seed in tasks)
        for index, result in enumerate(results, 1):
            row = result["row"]; nested_rows.append(row)
            inner.extend(result["inner"]); grid.extend(result["grid"])
            fold_audit.extend(result["folds"]); outer_coefficients.extend(result["coefficients"])
            if qa_dir is not None and row["valid"] and row["seed"] == seeds[0]:
                path = qa_dir / f"nested_{row['grouping']}_{row['seed']}.npz"
                np.savez_compressed(path, **result["qa"]); path.chmod(0o600)
            if index % 5 == 0 or index == 2 * len(seeds):
                print(f"Nested validation: {index}/{2 * len(seeds)} repetitions", flush=True)
        nested = save_csv(output, "nested_metrics.csv", nested_rows, ["grouping", "seed"])
        save_csv(output, "outer_coefficients.csv", outer_coefficients, ["grouping", "seed", "outer_fold"])
        summaries = [{"grouping": group, "metric": metric,
                      **distribution(subset.loc[subset["valid"], metric]),
                      "interpretation": "partition_refit_sensitivity_not_CI"}
                     for group, subset in nested.groupby("grouping") for metric in METRICS if metric in subset]
        save_csv(output, "nested_summary.csv", summaries, ["grouping", "metric"])
        print(f"Running {len(boot_seeds)} full-development household bootstrap draws", flush=True)
        bootstrap_rows, bootstrap_coefficients = [], []
        results = Parallel(n_jobs=jobs, return_as="generator")(
            delayed(bootstrap_replicate)(work, seed, index + 1, config)
            for index, seed in enumerate(boot_seeds))
        for index, result in enumerate(results, 1):
            bootstrap_rows.append(result["row"]); inner.extend(result["inner"])
            grid.extend(result["grid"]); fold_audit.extend(result["folds"])
            bootstrap_coefficients.extend(result["coefficients"])
            if index % 25 == 0 or index == len(boot_seeds):
                print(f"Development bootstrap: {index}/{len(boot_seeds)} draws", flush=True)
    bootstrap = save_csv(output, "bootstrap_replicates.csv", bootstrap_rows, ["replicate"])
    coefficients = save_csv(output, "bootstrap_coefficients.csv", bootstrap_coefficients, ["replicate"])
    save_csv(output, "optimism_correction.csv", optimism_summary(apparent, bootstrap), ["metric"])
    coefficient_summaries = [{"term": term, **distribution(coefficients[term]),
        "negative": int(coefficients[term].lt(0).sum()), "positive": int(coefficients[term].gt(0).sum()),
        "zero": int(coefficients[term].eq(0).sum()), "interpretation": "penalised_stability_not_Wald_or_causal"}
        for term in ["intercept", *model.SLOPE_NAMES] if term in coefficients]
    save_csv(output, "coefficient_stability.csv", coefficient_summaries, ["term"])
    inner_frame = save_csv(output, "inner_fits.csv", inner,
                           ["phase", "grouping", "seed", "outer_fold", "C", "inner_fold"])
    save_csv(output, "tuning_scores.csv", grid, ["phase", "grouping", "seed", "outer_fold", "C"])
    final_frame = save_csv(output, "final_fits.csv", fold_audit, ["phase", "grouping", "seed", "outer_fold"])
    if sha(ROOT / config["cohort_path"]) != cohort["raw_sha256"]:
        raise AssertionError("Frozen cohort changed during execution")
    record = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(), "pilot_only": pilot,
        "analysis_status": "retrospective_internal_validation", "external_validation": False,
        "config": config, "cohort": cohort, "outer_seeds": seeds, "bootstrap_seeds": boot_seeds,
        "nested_repetitions_attempted": len(nested), "nested_repetitions_valid": int(nested["valid"].sum()),
        "bootstrap_attempted": len(bootstrap), "bootstrap_valid": int(bootstrap["valid"].sum()),
        "bootstrap_invalid": int((~bootstrap["valid"]).sum()), "redraws": 0,
        "inner_fits_attempted": len(inner_frame), "inner_fits_converged": int(inner_frame["converged"].sum()),
        "final_fits_attempted": int(final_frame["final_attempted"].sum()),
        "final_fits_converged": int(final_frame["final_converged"].sum()),
        "elapsed_seconds": time.monotonic() - start,
        "runtime_versions": {p: importlib.metadata.version(p) for p in
            ["numpy", "pandas", "scipy", "scikit-learn", "joblib", "threadpoolctl"]},
        "python": platform.python_version(), "jobs": jobs,
        "source_commit_at_run": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "sha256": {str(p.relative_to(ROOT)): sha(p) for p in
            [Path(__file__), Path(model.__file__), config_path,
             ROOT / "paper/publication/methodology_protocol.md"]},
        "controlled_QA_arrays_outside_repository": qa_dir is not None,
        "public_outputs": "aggregate_only_no_respondent_identifiers_or_row_predictions",
        "interpretation_limits": ["Repeated-split summaries are not confidence intervals",
            "Optimism-bootstrap MCSE measures simulation error, not sampling uncertainty",
            "Original-cohort bootstrap evaluation deliberately overlaps development",
            "OOB diagnostics vary in prevalence and training support",
            "No causal, external-validation or participant-usability claim",
            "Original outcome-informed D-052 history is not erased"]}
    record["output_sha256"] = {p.name: sha(p) for p in sorted(output.glob("*.csv"))}
    record["output_sha256"]["full_candidate.json"] = sha(output / "full_candidate.json")
    write_json(output / "run_record.json", record)
    print(f"Complete: {record['bootstrap_valid']}/{len(bootstrap)} bootstrap draws valid; "
          f"{record['nested_repetitions_valid']}/{len(nested)} nested repetitions valid", flush=True)
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--qa-dir", type=Path)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--pilot", action="store_true", help="Two repetitions/five draws, outside Git only")
    args = parser.parse_args()
    run(args.config.resolve(), args.output_dir, args.qa_dir, args.jobs, args.pilot)


if __name__ == "__main__":
    main()
