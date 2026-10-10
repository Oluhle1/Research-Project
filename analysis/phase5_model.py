"""Phase 5: logistic model and household-grouped validation.

Uses the frozen final cohort only. Does not edit that file, does not
balance classes, and does not choose a classification threshold.

The primary model is the Table I specification with one logged revision:
traditional area and rural formal settlement are one contrast, because
rural formal has a single non-recipient and the separate contrast did not
converge in every training fold. The unrevised attempt is kept in
output/phase5/table_i_attempt/.

Primary performance is the pooled out-of-fold predictions. A full-sample
fit is saved only as an apparent association.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase4_rq1 as description  # noqa: E402

OUT = ROOT / "output" / "phase5"
FROZEN = ROOT / "output" / "phase3" / "cohort_person.csv"
FROZEN_HASH = "50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2"
SEED = 201415
N_BOOT = 1000
PROB_CLIP = 1e-6
N_BINS = 5
# Rural formal is merged with traditional area. Table I's separate rural-formal
# contrast was not estimable in every training fold: that category has one
# non-recipient. See decision D-050.
SLOPE_NAMES = [
    "age_per_10",
    "sex_female",
    "school_below",
    "settle_urban_informal",
    "settle_traditional_or_rural",
    "welfare_far",
]
FORBIDDEN = {
    "y",
    "y_n",
    "opg_income_annual",
    "applicant_private_income",
    "spouse_private_income",
    "combined_private_income",
    "reason_codes",
    "eligibility_status",
    "outcome_status",
    "person_weight",
    "in_final_cohort",
}


def modal_code(codes: pd.Series) -> str:
    """Most frequent code. Ties use the smallest code when sorted as text."""
    counts = codes.astype(str).value_counts()
    top = counts.max()
    tied = sorted(counts[counts == top].index, key=str)
    return tied[0]


def prepare(frame: pd.DataFrame) -> pd.DataFrame:
    work = frame.copy()
    work["age_n"] = pd.to_numeric(work["age"])
    work["y_n"] = pd.to_numeric(work["y"]).astype(int)
    work["age_per_10"] = (work["age_n"] - 60) / 10
    work["sex_code"] = work["sex"].where(work["sex"].isin(["1", "2"]))
    school = work["schooling_raw"].map(description.schooling_class)
    work["school_code"] = school.map({"Grade 7 or above": "0", "Below Grade 7": "1"})
    work["settlement_code"] = work["settlement"].where(work["settlement"].isin(["1", "2", "4", "5"]))
    welfare = work["welfare_distance"].map(description.welfare_class)
    work["welfare_code"] = welfare.map({"Nearer than 5 km": "0", "At least 5 km or unavailable": "1"})
    return work


def assign_folds(work: pd.DataFrame) -> pd.DataFrame:
    households = (
        work.groupby("uqno", as_index=False)
        .agg(any_event=("y_n", "max"), size=("y_n", "size"), distinct_y=("y_n", "nunique"))
        .sort_values("uqno")
        .reset_index(drop=True)
    )
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    fold_of = {}
    for fold, (_, test_index) in enumerate(splitter.split(households, households["any_event"]), start=1):
        for household_id in households.loc[test_index, "uqno"]:
            fold_of[household_id] = fold
    work = work.copy()
    work["fold"] = work["uqno"].map(fold_of)
    if work["fold"].isna().any() or work.groupby("uqno")["fold"].nunique().max() != 1:
        raise SystemExit("Household fold assignment failed")
    return work, households


def fold_support(work: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for fold, subset in work.groupby("fold"):
        rows.append({
            "fold": int(fold),
            "people": int(len(subset)),
            "households": int(subset["uqno"].nunique()),
            "events": int(subset["y_n"].sum()),
            "non_events": int((subset["y_n"] == 0).sum()),
        })
    return pd.DataFrame(rows)


def learning_stats(train: pd.DataFrame) -> dict:
    return {
        "age_per_10_median": float(train["age_per_10"].median()),
        "sex_code": modal_code(train["sex_code"].dropna()),
        "school_code": modal_code(train["school_code"].dropna()),
        "settlement_code": modal_code(train["settlement_code"].dropna()),
        "welfare_code": modal_code(train["welfare_code"].dropna()),
    }


def apply_stats(subset: pd.DataFrame, stats: dict) -> pd.DataFrame:
    filled = subset.copy()
    filled["age_per_10"] = filled["age_per_10"].fillna(stats["age_per_10_median"])
    for column in ("sex_code", "school_code", "settlement_code", "welfare_code"):
        filled[column] = filled[column].fillna(stats[column])
    return filled


def model_matrix(filled: pd.DataFrame) -> pd.DataFrame:
    """Seven slope columns. Reference levels are fixed in the run record."""
    columns = {
        "age_per_10": filled["age_per_10"].astype(float),
        "sex_female": (filled["sex_code"] == "2").astype(float),
        "school_below": (filled["school_code"] == "1").astype(float),
        "settle_urban_informal": (filled["settlement_code"] == "2").astype(float),
        "settle_traditional_or_rural": filled["settlement_code"].isin(["4", "5"]).astype(float),
        "welfare_far": (filled["welfare_code"] == "1").astype(float),
    }
    matrix = pd.DataFrame(columns, index=filled.index)
    if list(matrix.columns) != SLOPE_NAMES or set(matrix.columns) & FORBIDDEN:
        raise SystemExit("Model matrix contains a forbidden or unexpected column")
    return matrix


def fit_logit(y: np.ndarray, matrix: pd.DataFrame):
    design = sm.add_constant(matrix.to_numpy(dtype=float), has_constant="add")
    result = sm.Logit(y, design).fit(disp=False, maxiter=200)
    names = ["intercept", *SLOPE_NAMES]
    converged = bool(result.mle_retvals.get("converged", False))
    return result, names, converged


def predict(result, matrix: pd.DataFrame) -> np.ndarray:
    design = sm.add_constant(matrix.to_numpy(dtype=float), has_constant="add")
    return np.asarray(result.predict(design), dtype=float)


def clipped(probability: np.ndarray) -> np.ndarray:
    return np.clip(probability, PROB_CLIP, 1 - PROB_CLIP)


def citl_and_slope(y: np.ndarray, probability: np.ndarray, weight: np.ndarray | None = None) -> tuple[float, float]:
    logit = np.log(clipped(probability) / (1 - clipped(probability)))
    frequent = {} if weight is None else {"freq_weights": weight}
    citl_fit = sm.GLM(
        y, np.ones((len(y), 1)), family=sm.families.Binomial(), offset=logit, **frequent
    ).fit(maxiter=100)
    if np.unique(np.round(logit, 8)).size < 2:
        return float(citl_fit.params[0]), float("nan")
    slope_fit = sm.GLM(
        y, sm.add_constant(logit), family=sm.families.Binomial(), **frequent
    ).fit(maxiter=100)
    return float(citl_fit.params[0]), float(slope_fit.params[1])


def metric_row(name: str, y: np.ndarray, probability: np.ndarray, weight: np.ndarray | None = None) -> dict:
    kwargs = {} if weight is None else {"sample_weight": weight}
    citl, slope = citl_and_slope(y, probability, weight)
    return {
        "model": name,
        "prevalence": float(np.average(y, weights=weight)),
        "average_precision": float(average_precision_score(y, probability, **kwargs)),
        "roc_auc": float(roc_auc_score(y, probability, **kwargs)),
        "brier": float(brier_score_loss(y, probability, sample_weight=weight)),
        "calibration_in_the_large": citl,
        "calibration_slope": slope,
    }


def riley_note(n: int, events: int, parameters: int) -> dict:
    """Riley et al. 2019 shrinkage calculation for a stated anticipated R-squared.

    This informs the feasibility note. It does not select predictors.
    """
    prevalence = events / n
    entropy = prevalence * np.log(prevalence) + (1 - prevalence) * np.log(1 - prevalence)
    r2_max = float(1 - np.exp(2 * entropy))
    shrinkage = 0.9
    anticipated = 0.05
    denominator = (shrinkage - 1) * np.log(1 - anticipated / shrinkage)
    n_shrinkage = float(parameters / denominator)
    n_overall = float((1.96 / 0.05) ** 2 * prevalence * (1 - prevalence))
    return {
        "events_per_slope": events / parameters,
        "cox_snell_r2_maximum": r2_max,
        "anticipated_cox_snell_r2_for_the_calculation": anticipated,
        "target_shrinkage": shrinkage,
        "n_for_that_shrinkage": n_shrinkage,
        "n_to_estimate_outcome_risk_within_0.05": n_overall,
        "analysis_n": n,
    }


def vif_table(matrix: pd.DataFrame) -> pd.DataFrame:
    design = sm.add_constant(matrix.to_numpy(dtype=float), has_constant="add")
    rows = []
    for index, name in enumerate(["intercept", *SLOPE_NAMES]):
        if name == "intercept":
            continue
        rows.append({"term": name, "vif": float(variance_inflation_factor(design, index))})
    return pd.DataFrame(rows)


def calibration_bins(y: np.ndarray, probability: np.ndarray) -> pd.DataFrame:
    bins = pd.qcut(probability, N_BINS, duplicates="drop")
    frame = pd.DataFrame({"y": y, "p": probability, "bin": bins})
    grouped = frame.groupby("bin", observed=True)
    out = grouped.agg(people=("y", "size"), events=("y", "sum"), mean_predicted=("p", "mean"), mean_observed=("y", "mean"))
    return out.reset_index(drop=True)


def plot_calibration(bins: pd.DataFrame, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(5.2, 5.2))
    axis.plot([0, 1], [0, 1], color="0.6", linewidth=1)
    axis.scatter(bins["mean_predicted"], bins["mean_observed"], s=40 + bins["people"] / 5)
    axis.set_xlabel("Mean predicted probability")
    axis.set_ylabel("Observed non-receipt")
    axis.set_xlim(0, max(0.2, float(bins["mean_predicted"].max()) + 0.05))
    axis.set_ylim(0, max(0.2, float(bins["mean_observed"].max()) + 0.05))
    axis.set_title("Out-of-fold calibration, five quantile bins")
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def bootstrap(work: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    households = work["uqno"].drop_duplicates().to_numpy()
    positions = work.groupby("uqno").indices
    y = work["y_n"].to_numpy()
    probability = work["p_model"].to_numpy()
    reference = work["p_intercept"].to_numpy()
    records = []
    invalid = {"auc": 0, "calibration": 0}
    for _draw in range(N_BOOT):
        drawn = rng.choice(households, size=len(households), replace=True)
        index = np.concatenate([positions[household] for household in drawn])
        y_b = y[index]
        p_b = probability[index]
        if len(np.unique(y_b)) < 2:
            invalid["auc"] += 1
            invalid["calibration"] += 1
            records.append({"brier": np.nan, "average_precision": np.nan, "roc_auc": np.nan, "citl": np.nan, "slope": np.nan, "brier_intercept": np.nan})
            continue
        row = {
            "brier": float(brier_score_loss(y_b, p_b)),
            "average_precision": float(average_precision_score(y_b, p_b)),
            "roc_auc": float(roc_auc_score(y_b, p_b)),
            "brier_intercept": float(brier_score_loss(y_b, reference[index])),
        }
        try:
            citl, slope = citl_and_slope(y_b, p_b)
            row["citl"] = citl
            row["slope"] = slope
        except Exception:
            invalid["calibration"] += 1
            row["citl"] = np.nan
            row["slope"] = np.nan
        records.append(row)
    summary = []
    for metric in ("roc_auc", "average_precision", "brier", "brier_intercept", "citl", "slope"):
        values = pd.Series([record[metric] for record in records], dtype=float).dropna()
        summary.append({
            "metric": metric,
            "valid_resamples": int(values.shape[0]),
            "invalid_resamples": int(N_BOOT - values.shape[0]),
            "percentile_2.5": float(np.percentile(values, 2.5)) if len(values) else np.nan,
            "percentile_97.5": float(np.percentile(values, 97.5)) if len(values) else np.nan,
        })
    return pd.DataFrame(summary), invalid


def check_rules() -> None:
    if modal_code(pd.Series(["1", "2", "2", "1"])) not in {"1", "2"}:
        raise SystemExit("Mode tie break failed")
    if modal_code(pd.Series(["1", "2", "1", "2"])) != "1":
        raise SystemExit("Smallest-code tie break failed")
    train_codes = pd.Series(["0", "0", "1"])
    untouched = modal_code(train_codes)
    contaminated = pd.concat([train_codes, pd.Series(["1", "1", "1"])])
    if modal_code(train_codes) != untouched or modal_code(contaminated) == untouched:
        raise SystemExit("Imputation isolation check failed")
    toy = pd.DataFrame({
        "age_per_10": [0.0],
        "sex_code": ["2"],
        "school_code": ["1"],
        "settlement_code": ["4"],
        "welfare_code": ["1"],
    })
    built = model_matrix(toy)
    if list(built.columns) != SLOPE_NAMES:
        raise SystemExit("Slope list drifted")
    if float(built.iloc[0].sum()) != 4:
        raise SystemExit("Contrast coding failed")


def main() -> None:
    check_rules()
    digest = hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    if digest != FROZEN_HASH:
        raise SystemExit("Frozen cohort hash does not match Phase 3")
    raw = pd.read_csv(FROZEN, dtype=str)
    work = prepare(raw[raw["in_final_cohort"] == "1"])
    households = (
        work.groupby("uqno")
        .agg(size=("y_n", "size"), events=("y_n", "sum"), distinct=("y_n", "nunique"))
    )
    mixed = int((households["distinct"] > 1).sum())
    work, household_frame = assign_folds(work)
    support = fold_support(work)
    if (support["events"] == 0).any() or (support["non_events"] == 0).any():
        support.to_csv(OUT / "fold_support.csv", index=False)
        raise SystemExit("A validation fold lacks an outcome class. The validation plan needs review.")

    OUT.mkdir(parents=True, exist_ok=True)
    feasibility = {
        "people": int(len(work)),
        "events": int(work["y_n"].sum()),
        "households": int(work["uqno"].nunique()),
        "households_with_more_than_one_cohort_member": int((households["size"] > 1).sum()),
        "mixed_outcome_households": mixed,
        "households_with_any_nonrecipient": int((households["events"] > 0).sum()),
        "riley": riley_note(len(work), int(work["y_n"].sum()), len(SLOPE_NAMES)),
        "missing_schooling": int(work["school_code"].isna().sum()),
        "missing_welfare": int(work["welfare_code"].isna().sum()),
        "missing_age": int(work["age_per_10"].isna().sum()),
        "missing_sex": int(work["sex_code"].isna().sum()),
        "missing_settlement": int(work["settlement_code"].isna().sum()),
    }
    support.to_csv(OUT / "fold_support.csv", index=False)

    predictions = work[["uqno", "personno", "fold", "y_n", "person_weight"]].copy()
    predictions["p_model"] = np.nan
    predictions["p_intercept"] = np.nan
    coefficient_rows = []
    imputer_rows = []
    for fold in range(1, 6):
        train = work[work["fold"] != fold]
        test = work[work["fold"] == fold]
        stats = learning_stats(train)
        imputer_rows.append({"fold": fold, **stats})
        train_m = model_matrix(apply_stats(train, stats))
        test_m = model_matrix(apply_stats(test, stats))
        result, names, converged = fit_logit(train["y_n"].to_numpy(), train_m)
        coefficient_rows.append({
            "fold": fold,
            "converged": converged,
            **dict(zip(names, [float(value) for value in result.params])),
        })
        predictions.loc[test.index, "p_model"] = predict(result, test_m)
        predictions.loc[test.index, "p_intercept"] = float(train["y_n"].mean())

    if predictions["p_model"].isna().any():
        raise SystemExit("A person did not receive an out-of-fold prediction")

    y = predictions["y_n"].to_numpy()
    p_model = predictions["p_model"].to_numpy()
    p_intercept = predictions["p_intercept"].to_numpy()
    weight = pd.to_numeric(predictions["person_weight"]).to_numpy()
    metrics = pd.DataFrame([
        metric_row("logistic_out_of_fold", y, p_model),
        {
            "model": "intercept_only_out_of_fold",
            "prevalence": float(y.mean()),
            "average_precision": "",
            "roc_auc": "",
            "brier": float(brier_score_loss(y, p_intercept)),
            "calibration_in_the_large": citl_and_slope(y, p_intercept)[0],
            "calibration_slope": "",
        },
        metric_row("logistic_out_of_fold_weighted_metrics", y, p_model, weight),
    ])
    bins = calibration_bins(y, p_model)
    plot_calibration(bins, OUT / "calibration_plot.png")
    intervals, invalid = bootstrap(predictions)

    complete = work.dropna(subset=["age_per_10", "sex_code", "school_code", "settlement_code", "welfare_code"])
    collinearity = vif_table(model_matrix(complete))
    full_result, full_names, full_converged = fit_logit(work["y_n"].to_numpy(), model_matrix(apply_stats(work, learning_stats(work))))
    apparent = pd.DataFrame({
        "term": full_names,
        "coefficient": [float(value) for value in full_result.params],
        "std_error": [float(value) for value in full_result.bse],
        "converged": full_converged,
    })

    predictions.to_csv(OUT / "oof_predictions.csv", index=False)
    metrics.to_csv(OUT / "metrics.csv", index=False)
    bins.to_csv(OUT / "calibration_bins.csv", index=False)
    intervals.to_csv(OUT / "bootstrap_intervals.csv", index=False)
    pd.DataFrame(coefficient_rows).to_csv(OUT / "fold_coefficients.csv", index=False)
    pd.DataFrame(imputer_rows).to_csv(OUT / "fold_imputers.csv", index=False)
    collinearity.to_csv(OUT / "vif.csv", index=False)
    apparent.to_csv(OUT / "apparent_coefficients.csv", index=False)
    record = {
        "frozen_sha256": digest,
        "seed": SEED,
        "bootstrap_draws": N_BOOT,
        "interval": "95 percent percentile of household resamples of the fixed out-of-fold predictions",
        "probability_clip_for_logit": PROB_CLIP,
        "calibration_bins": "five quantile bins of predicted probability; tied boundaries are merged",
        "reference_levels": {
            "sex": "male (code 1)",
            "schooling": "Grade 7 or above",
            "settlement": "urban formal (code 1); traditional area and rural formal are one contrast",
            "welfare": "nearer than 5 km",
        },
        "stratification": "household labelled positive if any member has Y=1; mixed households observed before the split",
        "mixed_outcome_households": mixed,
        "bootstrap_invalid": invalid,
        "feasibility": feasibility,
        "sklearn": __import__("sklearn").__version__,
        "statsmodels": sm.__version__,
    }
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    (OUT / "feasibility.json").write_text(json.dumps(feasibility, indent=2), encoding="utf-8")
    print(metrics.to_string(index=False))
    print(intervals.to_string(index=False))
    print(apparent.to_string(index=False))
    print("mixed", mixed, "folds")
    print(support.to_string(index=False))
    print("vif")
    print(collinearity.to_string(index=False))


if __name__ == "__main__":
    main()
