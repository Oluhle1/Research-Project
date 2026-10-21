"""Ridge comparison of the separate and merged settlement codings.

The penalty grid and the inner-fold scoring rule were fixed before the
results were examined. This does not edit the frozen cohort or the primary
out-of-fold files. Reusing these adults cannot make Decision D-052
outcome-independent. The ordinary six-slope model remains the reference.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
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
    if folds.isna().any() or work.assign(inner_fold=folds).groupby("uqno")["inner_fold"].nunique().max() != 1:
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


def choose_penalty(train: pd.DataFrame, matrix_builder, seed: int) -> tuple[float, bool, list[dict], list[dict]]:
    """Tune on raw outer-training rows; learn preprocessing inside inner folds."""
    folds = household_folds(train, seed)
    scores = []
    inner_ok = True
    prepared_folds = []
    fit_rows = []
    score_rows = []
    for fold in range(1, 6):
        inner_train = train[folds != fold]
        inner_test = train[folds == fold]
        if inner_train["y_n"].nunique() < 2 or len(inner_test) == 0:
            raise SystemExit(f"Unsupported inner fold {fold} for seed {seed}")
        if not set(inner_train["uqno"]).isdisjoint(inner_test["uqno"]):
            raise SystemExit(f"Household overlap in inner fold {fold} for seed {seed}")
        stats = merged.learning_stats(inner_train)
        x_train, x_test = scale(
            matrix_builder(merged.apply_stats(inner_train, stats)),
            matrix_builder(merged.apply_stats(inner_test, stats)),
        )
        prepared_folds.append((fold, inner_train, inner_test, x_train, x_test))
    for penalty_c in C_GRID:
        losses = []
        all_converged = True
        for fold, inner_train, inner_test, x_train, x_test in prepared_folds:
            probability, converged, iterations = fit_ridge(
                x_train, inner_train["y_n"].to_numpy(), x_test, penalty_c
            )
            if not converged:
                inner_ok = False
                all_converged = False
            loss = float(np.mean((probability - inner_test["y_n"].to_numpy()) ** 2))
            losses.append(loss)
            fit_rows.append({
                "inner_seed": seed,
                "inner_fold": fold,
                "C": penalty_c,
                "train_people": len(inner_train),
                "test_people": len(inner_test),
                "train_households": inner_train["uqno"].nunique(),
                "test_households": inner_test["uqno"].nunique(),
                "train_events": int(inner_train["y_n"].sum()),
                "test_events": int(inner_test["y_n"].sum()),
                "brier": loss,
                "converged": converged,
                "iterations": iterations,
            })
        mean_loss = float(np.mean(losses))
        scores.append(mean_loss if all_converged else np.inf)
        score_rows.append({
            "inner_seed": seed,
            "C": penalty_c,
            "mean_inner_brier": mean_loss,
            "inner_folds": len(losses),
            "all_inner_converged": all_converged,
        })
    if not np.isfinite(scores).any():
        raise SystemExit(f"No converged penalty candidate for inner seed {seed}")
    # C_GRID is increasing: an exact tie selects the stronger penalty.
    selected_c = float(C_GRID[int(np.argmin(scores))])
    for row in score_rows:
        row["selected"] = row["C"] == selected_c
    return selected_c, inner_ok, fit_rows, score_rows


def cross_validate(work: pd.DataFrame, matrix_builder, name: str, qa_dir: Path | None = None) -> tuple[dict, list[dict], list[dict], list[dict]]:
    assigned, _households = merged.assign_folds(work)
    predictions = assigned[["fold", "y_n"]].copy()
    predictions["p_model"] = np.nan
    fold_rows = []
    inner_rows = []
    grid_rows = []
    for fold in range(1, 6):
        train = assigned[assigned["fold"] != fold]
        test = assigned[assigned["fold"] == fold]
        if not set(train["uqno"]).isdisjoint(test["uqno"]):
            raise SystemExit(f"Household overlap in outer fold {fold}")
        penalty_c, inner_ok, fits, scores = choose_penalty(train, matrix_builder, merged.SEED + fold)
        inner_rows.extend({"coding": name, "outer_fold": fold, **row} for row in fits)
        grid_rows.extend({"coding": name, "outer_fold": fold, **row} for row in scores)
        stats = merged.learning_stats(train)
        x_train, x_test = scale(
            matrix_builder(merged.apply_stats(train, stats)),
            matrix_builder(merged.apply_stats(test, stats)),
        )
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
    if qa_dir is not None:
        # Controlled QA only: no respondent or household identifiers are exported.
        qa = predictions.reset_index(drop=True)
        qa.index.name = "qa_row"
        qa_path = qa_dir / f"{name}_oof.csv"
        qa.to_csv(qa_path)
        qa_path.chmod(0o600)
    return metrics, fold_rows, inner_rows, grid_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qa-predictions-dir", type=Path,
                        help="Optional controlled OOF exports outside the repository; not part of the public supplement")
    args = parser.parse_args()
    qa_dir = args.qa_predictions_dir.resolve() if args.qa_predictions_dir is not None else None
    if qa_dir is not None:
        if qa_dir == ROOT or ROOT in qa_dir.parents:
            raise SystemExit("Controlled QA predictions must be stored outside the repository")
        qa_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    raw = pd.read_csv(merged.FROZEN, dtype=str)
    work = merged.prepare(raw[raw["in_final_cohort"] == "1"])
    rows = []
    folds = []
    inner_fits = []
    grid_scores = []
    for name, builder in (
        ("merged_six_slope", merged.model_matrix),
        ("separate_seven_slope", separate.model_matrix),
    ):
        metrics, fold_rows, inner_rows, grid_rows = cross_validate(work, builder, name, qa_dir)
        rows.append(metrics)
        folds.extend(fold_rows)
        inner_fits.extend(inner_rows)
        grid_scores.extend(grid_rows)
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "metrics.csv", index=False)
    pd.DataFrame(folds).to_csv(OUT / "fold_penalties.csv", index=False)
    pd.DataFrame(inner_fits).to_csv(OUT / "inner_fold_scores.csv", index=False)
    pd.DataFrame(grid_scores).to_csv(OUT / "inner_grid_scores.csv", index=False)
    cohort_bytes = merged.FROZEN.read_bytes()
    record = {
        "C_grid": C_GRID,
        "tuning": "lowest mean inner-fold Brier score; five household folds inside each outer training set",
        "inner_seeds": [merged.SEED + fold for fold in range(1, 6)],
        "tie_rule": "first C in the increasing grid (stronger penalty) on an exact score tie",
        "outer_folds": "phase5 assign_folds, seed 201415",
        "imputation": "learned independently on each inner training fold during tuning and on each full outer training fold for its final fit",
        "standardisation": "mean and population standard deviation learned from the corresponding inner or outer training matrix; zero spread replaced by 1; ridge fits only",
        "estimator": "sklearn LogisticRegression, L2 penalty, lbfgs, max_iter=1000; intercept not penalised",
        "inner_fits_attempted": len(inner_fits),
        "inner_fits_converged": sum(int(row["converged"]) for row in inner_fits),
        "outer_fits_attempted": len(folds),
        "outer_fits_converged": sum(int(row["converged"]) for row in folds),
        "runtime_versions": {package: importlib.metadata.version(package) for package in
                             ("numpy", "pandas", "scipy", "scikit-learn", "statsmodels")},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cohort_sha256_raw": hashlib.sha256(cohort_bytes).hexdigest(),
        "cohort_sha256_crlf": hashlib.sha256(cohort_bytes.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest(),
        "public_outputs": "aggregate metrics and tuning/convergence records only; optional row-level QA predictions are outside the repository",
        "ordinary_reference": "unchanged six-slope maximum-likelihood model",
        "limit": "D-052 remains outcome-informed; this comparison does not remove that information",
    }
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(pd.DataFrame(rows).to_string(index=False))
    print(pd.DataFrame(folds).to_string(index=False))


if __name__ == "__main__":
    main()
