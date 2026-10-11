#!/usr/bin/env python3
"""Explicit offline build of the retained full-cohort research logistic model.

Run with the research virtual environment: python tools/freeze_model.py
Existing compatible artifacts are reused without fitting. A changed/incomplete
artifact requires a deliberate --force; imports and uploaded data never train.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from opg_core.features import FEATURE_ORDER, build_matrix, prepare_features  # noqa: E402
from opg_core.inference import (  # noqa: E402
    ARTIFACT_SCHEMA_VERSION, EVALUATION_SCHEMA_VERSION, MODEL_DIR, MODEL_VERSION,
    REFERENCE_LEVELS, SCORE_CONTEXT, load_model,
)
from opg_core.schema import CONTEXT, MODEL_FIELDS, SCHEMA_VERSION  # noqa: E402
from opg_core.screening import RULE_VERSION  # noqa: E402
import phase5_model as research_model  # noqa: E402

OUTPUT_NAMES = ("logistic_model.json", "manifest.json", "evaluation.json")
EVALUATION_SOURCES = (
    "output/runs/primary/metrics.csv", "output/runs/primary/bootstrap_intervals.csv",
    "output/runs/primary/calibration_bins.csv", "output/runs/primary/run_record.json",
)
SCIENTIFIC_SCRIPTS = (
    "analysis/phase3_build_cohort.py", "analysis/phase4_rq1.py", "analysis/phase5_model.py",
)
ADAPTER_SCRIPTS = ("opg_core/features.py", "opg_core/inference.py", "opg_core/schema.py", "opg_core/screening.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def file_provenance(path: Path) -> dict:
    data = path.read_bytes()
    lf_data = data.replace(b"\r\n", b"\n")
    return {
        "raw_sha256": hashlib.sha256(data).hexdigest(),
        "crlf_sha256": hashlib.sha256(lf_data.replace(b"\n", b"\r\n")).hexdigest(),
    }


def software() -> dict:
    import scipy
    import sklearn
    import statsmodels
    return {
        "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
        "scipy": scipy.__version__, "sklearn": sklearn.__version__, "statsmodels": statsmodels.__version__,
    }


def _git(command: list[str]) -> str:
    return subprocess.check_output(["git", *command], cwd=ROOT, text=True).strip()


def source_signature() -> dict:
    """Only file paths, hashes, and dependency versions; never person records."""
    record = json.loads((ROOT / "output/runs/primary/run_record.json").read_text())
    inputs = {"output/phase3/cohort_person.csv": file_provenance(research_model.FROZEN)}
    for filename in sorted(record["input_sha256"]):
        source = ROOT / "Data" / filename
        # The existing pipeline is the authority for the data directory.
        if not source.exists():
            import phase3_build_cohort as cohort
            source = cohort.DATA / filename
        inputs[str(source.relative_to(ROOT))] = file_provenance(source)
    return {
        "training_input_hashes": inputs,
        "source_script_sha256": {name: sha256(ROOT / name) for name in SCIENTIFIC_SCRIPTS},
        "adapter_script_sha256": {name: sha256(ROOT / name) for name in ADAPTER_SCRIPTS},
        "training_script_sha256": sha256(Path(__file__)),
        "evaluation_source_sha256": {name: sha256(ROOT / name) for name in EVALUATION_SOURCES},
        "reference_coefficients_sha256": sha256(ROOT / "output/phase5/apparent_coefficients.csv"),
        "software": software(),
    }


def aggregate_evaluation() -> dict:
    """Select aggregate held-out evidence without copying the inspection example."""
    run = ROOT / "output/runs/primary"
    raw_metrics = pd.read_csv(run / "metrics.csv")
    metric_fields = (
        "prevalence", "average_precision", "roc_auc", "brier",
        "calibration_in_the_large", "calibration_slope",
    )
    metrics = {}
    for name in ("logistic_out_of_fold", "intercept_only_out_of_fold"):
        selected = raw_metrics.loc[raw_metrics["model"] == name]
        if len(selected) != 1:
            raise ValueError("Primary aggregate metric rows are missing or ambiguous.")
        row = selected.iloc[0]
        metrics[name] = {
            field: None if pd.isna(row[field]) else float(row[field]) for field in metric_fields
        }
    interval_rows = pd.read_csv(run / "bootstrap_intervals.csv").to_dict(orient="records")
    calibration = pd.read_csv(run / "calibration_bins.csv").to_dict(orient="records")
    return {
        "schema_version": EVALUATION_SCHEMA_VERSION, "model_version": MODEL_VERSION,
        "score_context": "Pooled held-out predictions from the retained six-slope household validation",
        "cohort": {"people": 1013, "events": 67, "households": 827},
        "metrics": metrics,
        "bootstrap": {
            "draws": research_model.N_BOOT, "seed": research_model.SEED,
            "method": "95 percent percentile of household resamples of fixed out-of-fold predictions; no model refitting",
            "intervals": interval_rows,
        },
        "calibration_bins": calibration,
        "provenance": {
            "rule_version": RULE_VERSION,
            "frozen_cohort_crlf_sha256": research_model.FROZEN_HASH,
            "sources": [{"path": name, "sha256": sha256(ROOT / name)} for name in EVALUATION_SOURCES],
        },
    }


def freeze_model(directory: Path = MODEL_DIR, force: bool = False) -> dict:
    """Build once, validate an in-memory fit against JSON reload, then save."""
    signature = source_signature()
    digest_info = signature["training_input_hashes"]["output/phase3/cohort_person.csv"]
    if digest_info["crlf_sha256"] != research_model.FROZEN_HASH:
        raise ValueError("Frozen cohort does not match the established checksum, even with CRLF compatibility.")
    directory = Path(directory)
    present = [name for name in OUTPUT_NAMES if (directory / name).exists()]
    if present:
        try:
            existing = load_model(directory)
            stored_evaluation = json.loads((directory / "evaluation.json").read_text())
            current_evaluation = aggregate_evaluation()
            reusable = existing.manifest.get("source_signature") == signature and stored_evaluation == current_evaluation
        except (ValueError, OSError, json.JSONDecodeError):
            reusable = False
        if reusable:
            return {"status": "reused", "model_version": MODEL_VERSION, "artifact_sha256": existing.manifest["artifact_sha256"]}
        if not force:
            raise ValueError("Model artifacts changed or are incomplete. Review the change, then explicitly use --force to rebuild.")

    raw = pd.read_csv(research_model.FROZEN, dtype=str)
    raw = raw.loc[raw["in_final_cohort"] == "1"].copy()
    outcome = pd.to_numeric(raw["y"]).astype(int).to_numpy()
    if len(raw) != 1013 or int(outcome.sum()) != 67 or raw["uqno"].nunique() != 827:
        raise ValueError("Training population differs from the retained primary cohort.")
    prepared = prepare_features(raw)
    training_stats = research_model.learning_stats(prepared)
    matrix = build_matrix(prepared, training_stats)
    result, names, converged = research_model.fit_logit(outcome, matrix)
    if not converged or names != ["intercept", *FEATURE_ORDER]:
        raise ValueError("The retained full-data fit did not converge with the required feature order.")
    reference = pd.read_csv(ROOT / "output/phase5/apparent_coefficients.csv")
    if list(reference["term"]) != names or not np.allclose(result.params, reference["coefficient"].to_numpy(), atol=1e-10, rtol=0):
        raise ValueError("Full-data fitted coefficients differ from the established research reference.")
    artifact = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION, "model_version": MODEL_VERSION,
        "estimator": "unweighted logistic regression", "feature_order": list(FEATURE_ORDER),
        "predictor_sources": list(MODEL_FIELDS), "intercept": float(result.params[0]),
        "coefficients": [float(value) for value in result.params[1:]],
        "training_stats": training_stats,
        "reference_levels": dict(REFERENCE_LEVELS),
    }
    artifact_bytes = json_bytes(artifact)
    evaluation = aggregate_evaluation()
    evaluation_bytes = json_bytes(evaluation)
    manifest = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION, "model_version": MODEL_VERSION,
        "data_schema_version": SCHEMA_VERSION, "study_context": CONTEXT, "rule_version": RULE_VERSION,
        "artifact_sha256": hashlib.sha256(artifact_bytes).hexdigest(),
        "evaluation_sha256": hashlib.sha256(evaluation_bytes).hexdigest(),
        "feature_order": list(FEATURE_ORDER), "score_context": SCORE_CONTEXT,
        "positive_class": "reported OPG non-receipt among the resolved apparently eligible cohort",
        "training_cohort": {"people": 1013, "events": 67, "households": 827},
        "seed": research_model.SEED, "source_signature": signature,
        "baseline_commit": _git(["rev-parse", "HEAD"]),
        "working_tree_dirty": bool(_git(["status", "--porcelain"])),
        "commit_scope": "Baseline repository revision; uncommitted build and adapter code are identified by their file hashes",
        "training_input_hashes": signature["training_input_hashes"],
        "source_script_sha256": signature["source_script_sha256"],
        "training_script_sha256": signature["training_script_sha256"],
        "software": signature["software"],
    }
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".freeze-", dir=directory) as stage_name:
        stage = Path(stage_name)
        (stage / "logistic_model.json").write_bytes(artifact_bytes)
        (stage / "manifest.json").write_bytes(json_bytes(manifest))
        (stage / "evaluation.json").write_bytes(evaluation_bytes)
        reloaded = load_model(stage)
        expected = research_model.predict(result, matrix)
        actual = reloaded.predict_matrix(matrix)
        max_difference = float(np.max(np.abs(expected - actual)))
        if not np.allclose(actual, expected, atol=1e-12, rtol=0):
            raise ValueError("JSON-reloaded probabilities do not match the in-memory fitted model.")
        manifest["verification"] = {
            "coefficient_reference_atol": 1e-10, "prediction_reload_atol": 1e-12,
            "prediction_reload_max_abs_difference": max_difference,
            "training_converged": True, "verified_rows": len(raw),
            "reference": "Original retained full-data in-memory fit and saved apparent coefficients",
        }
        (stage / "manifest.json").write_bytes(json_bytes(manifest))
        for name in OUTPUT_NAMES:
            (stage / name).replace(directory / name)
    return {
        "status": "built", "model_version": MODEL_VERSION, "artifact_sha256": manifest["artifact_sha256"],
        "prediction_reload_max_abs_difference": max_difference, "verified_rows": len(raw),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Deliberately replace changed/incomplete model artifacts.")
    parser.add_argument("--output-dir", type=Path, default=MODEL_DIR, help="Directory for reviewed JSON model artifacts.")
    args = parser.parse_args()
    try:
        result = freeze_model(args.output_dir, args.force)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Model freeze failed: {exc}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
