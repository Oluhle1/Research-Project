"""Ridge comparison of the separate and merged settlement codings.

The penalty grid and the inner-fold scoring rule were fixed before the
results were examined. This does not edit the frozen cohort or the primary
out-of-fold files. Reusing these adults cannot make Decision D-052
outcome-independent. The ordinary six-slope model remains the reference.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase5_model as merged  # noqa: E402
import phase5_model_original_7slope as separate  # noqa: E402

OUT = ROOT / "output" / "phase5_ridge_settlement"
# Inverse penalty strengths. Smaller C is a stronger penalty.
C_GRID = [0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
MAX_ITER = 1000


def household_folds(work: pd.DataFrame, seed: int) -> pd.Series:
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
    folds = work["uqno"].map(fold_of)
    if folds.isna().any():
        raise SystemExit(f"Inner fold assignment failed for seed {seed}")
    return folds


def scale(train: pd.DataFrame, test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    center = train.mean()
    spread = train.std(ddof=0).replace(0, 1.0)
    return ((train - center) / spread).to_numpy(dtype=float), ((test - center) / spread).to_numpy(dtype=float)


def fit_ridge(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, penalty_c: float):
    model = LogisticRegression(C=penalty_c, solver="lbfgs", max_iter=MAX_ITER)
    model.fit(x_train, y_train)
    iterations = int(np.max(model.n_iter_))
    return model.predict_proba(x_test)[:, 1], iterations < MAX_ITER, iterations


def choose_penalty(train: pd.DataFrame, matrix_builder, seed: int) -> tuple[float, bool]:
    folds = household_folds(train, seed)
    scores = []
    inner_ok = True
    for penalty_c in C_GRID:
        losses = []
        for fold in range(1, 6):
            inner_train = train[folds != fold]
            inner_test = train[folds == fold]
            if inner_train["y_n"].nunique() < 2 or len(inner_test) == 0:
                inner_ok = False
                continue
            x_train, x_test = scale(matrix_builder(inner_train), matrix_builder(inner_test))
            probability, converged, _iterations = fit_ridge(
                x_train, inner_train["y_n"].to_numpy(), x_test, penalty_c
            )
            if not converged:
                inner_ok = False
            losses.append(float(np.mean((probability - inner_test["y_n"].to_numpy()) ** 2)))
        scores.append(float(np.mean(losses)) if losses else np.inf)
    return float(C_GRID[int(np.argmin(scores))]), inner_ok


def cross_validate(work: pd.DataFrame, matrix_builder, name: str) -> tuple[dict, list[dict]]:
    assigned, _households = merged.assign_folds(work)
    predictions = assigned[["y_n"]].copy()
    predictions["p_model"] = np.nan
    fold_rows = []
    for fold in range(1, 6):
        train = assigned[assigned["fold"] != fold]
        test = assigned[assigned["fold"] == fold]
        stats = merged.learning_stats(train)
        train = merged.apply_stats(train, stats)
        test = merged.apply_stats(test, stats)
        penalty_c, inner_ok = choose_penalty(train, matrix_builder, merged.SEED + fold)
        x_train, x_test = scale(matrix_builder(train), matrix_builder(test))
        probability, converged, iterations = fit_ridge(
            x_train, train["y_n"].to_numpy(), x_test, penalty_c
        )
        predictions.loc[test.index, "p_model"] = probability
        fold_rows.append({
            "coding": name,
            "fold": fold,
            "selected_C": penalty_c,
            "converged": converged,
            "iterations": iterations,
            "inner_folds_complete": inner_ok,
        })
    if predictions["p_model"].isna().any():
        raise SystemExit(f"Missing ridge prediction for {name}")
    metrics = merged.metric_row("ridge_out_of_fold", predictions["y_n"].to_numpy(), predictions["p_model"].to_numpy())
    metrics["coding"] = name
    metrics["folds_converged"] = int(sum(row["converged"] for row in fold_rows))
    return metrics, fold_rows


def main() -> None:
    raw = pd.read_csv(merged.FROZEN, dtype=str)
    work = merged.prepare(raw[raw["in_final_cohort"] == "1"])
    rows = []
    folds = []
    for name, builder in (
        ("merged_six_slope", merged.model_matrix),
        ("separate_seven_slope", separate.model_matrix),
    ):
        metrics, fold_rows = cross_validate(work, builder, name)
        rows.append(metrics)
        folds.extend(fold_rows)
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "metrics.csv", index=False)
    pd.DataFrame(folds).to_csv(OUT / "fold_penalties.csv", index=False)
    record = {
        "C_grid": C_GRID,
        "tuning": "lowest mean inner-fold Brier score; five household folds inside each outer training set",
        "outer_folds": "phase5 assign_folds, seed 201415",
        "standardisation": "training-fold mean and standard deviation, applied to ridge fits only",
        "ordinary_reference": "unchanged six-slope maximum-likelihood model",
        "limit": "D-052 remains outcome-informed; this comparison does not remove that information",
    }
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(pd.DataFrame(rows).to_string(index=False))
    print(pd.DataFrame(folds).to_string(index=False))


if __name__ == "__main__":
    main()
