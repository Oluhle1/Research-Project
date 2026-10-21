"""Repeated household-grouped refits of the retained six-slope model.

Does not edit the frozen cohort or the primary out-of-fold files.
Decision D-052 stays fixed. Seeds 201415 through 201434 were set before
the repetitions were examined. Seed 201415 is the primary validation seed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase5_model as model  # noqa: E402

OUT = ROOT / "output" / "phase5_refit_repeats"
SEEDS = list(range(201415, 201435))


def assign_folds(work: pd.DataFrame, seed: int) -> pd.DataFrame:
    households = (
        work.groupby("uqno", as_index=False)
        .agg(any_event=("y_n", "max"))
        .sort_values("uqno")
        .reset_index(drop=True)
    )
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    fold_of = {}
    for fold, (_, test_index) in enumerate(splitter.split(households, households["any_event"]), start=1):
        for household_id in households.loc[test_index, "uqno"]:
            fold_of[household_id] = fold
    out = work.copy()
    out["fold"] = out["uqno"].map(fold_of)
    if out["fold"].isna().any() or out.groupby("uqno")["fold"].nunique().max() != 1:
        raise SystemExit(f"Household fold assignment failed for seed {seed}")
    return out


def one_repetition(work: pd.DataFrame, seed: int) -> tuple[dict, list[dict]]:
    assigned = assign_folds(work, seed)
    predictions = assigned[["uqno", "y_n"]].copy()
    predictions["p_model"] = np.nan
    coefficients = []
    converged_folds = 0
    for fold in range(1, 6):
        train = assigned[assigned["fold"] != fold]
        test = assigned[assigned["fold"] == fold]
        stats = model.learning_stats(train)
        train_m = model.model_matrix(model.apply_stats(train, stats))
        test_m = model.model_matrix(model.apply_stats(test, stats))
        result, names, converged = model.fit_logit(train["y_n"].to_numpy(), train_m)
        converged_folds += int(converged)
        coefficients.append({
            "seed": seed,
            "fold": fold,
            "converged": converged,
            **dict(zip(names, [float(value) for value in result.params])),
        })
        predictions.loc[test.index, "p_model"] = model.predict(result, test_m)
    if predictions["p_model"].isna().any():
        raise SystemExit(f"Missing prediction for seed {seed}")
    metrics = model.metric_row(
        "logistic_out_of_fold",
        predictions["y_n"].to_numpy(),
        predictions["p_model"].to_numpy(),
    )
    metrics["seed"] = seed
    metrics["folds_converged"] = converged_folds
    return metrics, coefficients


def summarise(frame: pd.DataFrame, column: str) -> dict:
    values = frame[column].astype(float)
    return {
        "metric": column,
        "repetitions": int(len(values)),
        "median": float(values.median()),
        "q1": float(values.quantile(0.25)),
        "q3": float(values.quantile(0.75)),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
    }


def main() -> None:
    raw = pd.read_csv(model.FROZEN, dtype=str)
    work = model.prepare(raw[raw["in_final_cohort"] == "1"])
    rows = []
    coefficients = []
    for seed in SEEDS:
        metrics, fold_coefficients = one_repetition(work, seed)
        rows.append(metrics)
        coefficients.extend(fold_coefficients)
    repetitions = pd.DataFrame(rows)
    folds = pd.DataFrame(coefficients)
    primary = repetitions.loc[repetitions["seed"] == model.SEED].iloc[0]
    summary = pd.DataFrame([
        summarise(repetitions, column)
        for column in (
            "roc_auc",
            "average_precision",
            "brier",
            "calibration_in_the_large",
            "calibration_slope",
        )
    ])
    coefficient_summary = []
    for term in ("sex_female", "school_below", "age_per_10", "settle_urban_informal", "settle_traditional_or_rural", "welfare_far"):
        values = folds[term].astype(float)
        coefficient_summary.append({
            "term": term,
            "fits": int(len(values)),
            "negative": int((values < 0).sum()),
            "positive": int((values > 0).sum()),
            "median": float(values.median()),
            "minimum": float(values.min()),
            "maximum": float(values.max()),
        })
    OUT.mkdir(parents=True, exist_ok=True)
    repetitions.to_csv(OUT / "repetition_metrics.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    folds.to_csv(OUT / "fold_coefficients.csv", index=False)
    pd.DataFrame(coefficient_summary).to_csv(OUT / "coefficient_summary.csv", index=False)
    record = {
        "seeds": SEEDS,
        "coding": "D-052 six slopes, fixed before these repetitions",
        "primary_seed": model.SEED,
        "primary_seed_auc": float(primary["roc_auc"]),
        "primary_seed_brier": float(primary["brier"]),
        "fits_attempted": int(len(folds)),
        "fits_converged": int(folds["converged"].sum()),
    }
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(summary.to_string(index=False))
    print(pd.DataFrame(coefficient_summary).to_string(index=False))
    print(record)


if __name__ == "__main__":
    main()
