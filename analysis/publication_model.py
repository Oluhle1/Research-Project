"""Publication validation extension: original-category nested ridge model.

Technical implementation following supervisory feedback, with AI assistance
recorded in paper/publication. The original primary model stays exploratory.
This module has no file-writing or analysis entry point. Its five raw predictor
sources and seven resulting slopes are fixed; outcome and grouping columns are
metadata only. Every learned transformation is fitted on its supplied training
rows. Duplicated bootstrap copies retain their original group identifiers.
"""
from __future__ import annotations

from dataclasses import dataclass
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import brentq, minimize
from scipy.special import expit
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold


C_GRID = [0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
MAX_ITER = 2000
TOL = 1e-8
PROB_CLIP = 1e-6
RAW_PREDICTORS = ("age", "sex", "schooling_raw", "settlement", "welfare_distance")
SLOPE_NAMES = [
    "age_per_10", "sex_female", "school_below", "settle_urban_informal",
    "settle_traditional", "settle_rural_formal", "welfare_far",
]
CATEGORY_COLUMNS = ("sex_code", "school_code", "settlement_code", "welfare_code")


class UnsupportedSampleError(ValueError):
    """A sample cannot support the specified training or validation procedure."""

    def __init__(self, message: str, *, inner_records=None, grid_records=None,
                 final_attempted: bool = False, final_converged: bool = False):
        super().__init__(message)
        self.inner_records = [] if inner_records is None else inner_records
        self.grid_records = [] if grid_records is None else grid_records
        self.final_attempted = bool(final_attempted)
        self.final_converged = bool(final_converged)


def _normalise_code(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except (TypeError, ValueError):
        return None
    return str(int(number)) if np.isfinite(number) and number.is_integer() else None


def _school_code(value) -> str | None:
    code = _normalise_code(value)
    if code is None:
        return None
    value = int(code)
    if value == 98 or 1 <= value <= 7:
        return "1"
    if 8 <= value <= 20 or 23 <= value <= 30:
        return "0"
    return None


def _welfare_code(value) -> str | None:
    code = _normalise_code(value)
    if code is None:
        return None
    value = int(code)
    return "0" if 1 <= value <= 4 else "1" if 5 <= value <= 8 else None


def _require_households_nested_in_psus(frame: pd.DataFrame) -> None:
    """Reject invalid grouping metadata rather than split an original household."""
    if not {"uqno", "psu"}.issubset(frame.columns):
        raise UnsupportedSampleError("Original household and derived PSU identifiers are required")
    for column in ("uqno", "psu"):
        if (frame[column].isna().any()
                or frame[column].astype(str).str.strip().eq("").any()):
            raise UnsupportedSampleError("Household and PSU identifiers must be observed")
    if frame.groupby("uqno")["psu"].nunique(dropna=False).gt(1).any():
        raise UnsupportedSampleError("Each original household must belong to exactly one PSU")


def prepare_frame(raw_final: pd.DataFrame) -> pd.DataFrame:
    """Prepare already-screened rows without learning any sample statistics.

    Only the five named raw predictor sources enter the predictors. The caller
    selects the frozen resolved-PASS cohort; this function never changes a
    screening decision or reconstructs an outcome from predictor information.
    """
    required = {*RAW_PREDICTORS, "uqno", "psu", "person_weight", "y"}
    missing = sorted(required.difference(raw_final.columns))
    if missing:
        raise UnsupportedSampleError(f"Missing required columns: {missing}")
    if raw_final.empty:
        raise UnsupportedSampleError("No analysis rows")
    y = pd.to_numeric(raw_final["y"], errors="coerce")
    if y.isna().any() or not y.isin([0, 1]).all():
        raise UnsupportedSampleError("Outcome must be observed and binary")
    work = pd.DataFrame(index=raw_final.index)
    for name in ("uqno", "psu"):
        if raw_final[name].isna().any():
            raise UnsupportedSampleError(f"Missing {name} grouping values")
        work[name] = raw_final[name].astype(str).str.strip()
        if work[name].eq("").any():
            raise UnsupportedSampleError(f"Empty {name} grouping values")
    _require_households_nested_in_psus(work)
    work["person_weight"] = pd.to_numeric(raw_final["person_weight"], errors="coerce")
    if (not np.isfinite(work["person_weight"]).all()
            or not work["person_weight"].gt(0).all()):
        raise UnsupportedSampleError("Person weights must be finite and positive")
    work["y_n"] = y.astype(int)
    age = pd.to_numeric(raw_final["age"], errors="coerce")
    work["age_per_10"] = ((age - 60) / 10).where(np.isfinite(age))
    sex = raw_final["sex"].map(_normalise_code)
    work["sex_code"] = sex.where(sex.isin(["1", "2"]))
    work["school_code"] = raw_final["schooling_raw"].map(_school_code)
    settlement = raw_final["settlement"].map(_normalise_code)
    work["settlement_code"] = settlement.where(settlement.isin(["1", "2", "4", "5"]))
    work["welfare_code"] = raw_final["welfare_distance"].map(_welfare_code)
    return work.reset_index(drop=True)


def group_folds(frame: pd.DataFrame, group_col: str, seed: int,
                n_splits: int = 5) -> np.ndarray:
    """Stratify unique original groups by any event, then map every copy back.

    Multiplicity affects fitting and loss, but never creates a new grouping key.
    Row positions, rather than dataframe index labels, identify fold membership.
    """
    if group_col not in {"uqno", "psu"}:
        raise ValueError("Grouping must use original household or derived PSU")
    if n_splits < 2:
        raise ValueError("At least two folds are required")
    _require_households_nested_in_psus(frame)
    if frame[group_col].isna().any() or frame["y_n"].isna().any():
        raise UnsupportedSampleError("Grouping and outcomes must be observed")
    grouped = (frame.groupby(group_col, as_index=False)["y_n"].max()
               .sort_values(group_col).reset_index(drop=True))
    support = grouped["y_n"].value_counts()
    if len(support) != 2 or int(support.min()) < n_splits:
        raise UnsupportedSampleError("Too few event or non-event groups for stratified folds")
    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=int(seed))
    fold_map = {}
    for fold, (_, test_idx) in enumerate(splitter.split(grouped, grouped["y_n"])):
        fold_map.update(dict.fromkeys(grouped.iloc[test_idx][group_col], fold))
    folds = frame[group_col].map(fold_map).to_numpy(dtype=int)
    check = pd.DataFrame({"group": frame[group_col].to_numpy(), "fold": folds})
    if check.groupby("group")["fold"].nunique().max() != 1:
        raise AssertionError("Original group leaked across folds")
    return folds


@dataclass(frozen=True)
class PreprocessState:
    age_median: float
    category_modes: tuple[str, ...]
    means: tuple[float, ...]
    scales: tuple[float, ...]


def _mode(series: pd.Series) -> str:
    counts = series.dropna().astype(str).value_counts()
    if counts.empty:
        raise UnsupportedSampleError("A training categorical predictor is entirely missing")
    return min(counts[counts.eq(counts.max())].index)


def _unscaled_matrix(frame: pd.DataFrame, age_median: float,
                     category_modes: tuple[str, ...]) -> np.ndarray:
    age = frame["age_per_10"].fillna(age_median).to_numpy(dtype=float)
    sex, school, settlement, welfare = (
        frame[column].fillna(mode).to_numpy()
        for column, mode in zip(CATEGORY_COLUMNS, category_modes)
    )
    matrix = np.column_stack([
        age, sex == "2", school == "1", settlement == "2",
        settlement == "4", settlement == "5", welfare == "1",
    ]).astype(float)
    if matrix.shape != (len(frame), len(SLOPE_NAMES)) or not np.isfinite(matrix).all():
        raise UnsupportedSampleError("Invalid seven-slope predictor matrix")
    return matrix


def learn_preprocessor(train: pd.DataFrame) -> PreprocessState:
    """Learn imputation and scaling only from the supplied training rows."""
    age = train["age_per_10"].dropna()
    if age.empty or not np.isfinite(age).all():
        raise UnsupportedSampleError("No finite training ages")
    median = float(age.median())
    modes = tuple(_mode(train[column]) for column in CATEGORY_COLUMNS)
    matrix = _unscaled_matrix(train, median, modes)
    means = matrix.mean(axis=0)
    scales = matrix.std(axis=0, ddof=0)
    scales = np.where(scales == 0, 1.0, scales)
    return PreprocessState(median, modes, tuple(means), tuple(scales))


def transform(frame: pd.DataFrame, state: PreprocessState) -> np.ndarray:
    return ((_unscaled_matrix(frame, state.age_median, state.category_modes)
             - np.asarray(state.means)) / np.asarray(state.scales))


def _fit_logistic(matrix: np.ndarray, y: np.ndarray, penalty_c: float):
    if np.unique(y).size != 2:
        raise UnsupportedSampleError("A training sample has only one outcome class")
    model = LogisticRegression(C=float(penalty_c), solver="lbfgs",
                               max_iter=MAX_ITER, tol=TOL)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(matrix, y)
    iterations = int(np.max(model.n_iter_))
    converged = iterations < MAX_ITER and not any(
        isinstance(w.message, ConvergenceWarning) for w in caught)
    return model, converged, iterations


def select_penalty(grid_records: list[dict]) -> float:
    """Choose minimum pooled person loss; an exact tie favours lower C."""
    eligible = [r for r in grid_records
                if r["all_inner_converged"] and np.isfinite(r["pooled_inner_brier"])]
    if not eligible:
        raise UnsupportedSampleError("No penalty candidate converged in every inner fold",
                                     grid_records=grid_records)
    return float(min(eligible, key=lambda r: (r["pooled_inner_brier"], r["C"]))["C"])


@dataclass
class FitBundle:
    estimator: LogisticRegression
    state: PreprocessState
    selected_c: float
    inner_records: list[dict]
    grid_records: list[dict]
    final_converged: bool
    final_iterations: int

    @property
    def fit_count_attempted(self) -> int:
        return len(self.inner_records) + 1

    @property
    def fit_count_converged(self) -> int:
        return sum(int(r["converged"]) for r in self.inner_records) + int(self.final_converged)

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        probability = self.estimator.predict_proba(transform(frame, self.state))[:, 1]
        if not np.isfinite(probability).all():
            raise UnsupportedSampleError("Non-finite fitted probability")
        return probability

    def coefficients_original_scale(self) -> dict[str, float]:
        slopes = self.estimator.coef_[0] / np.asarray(self.state.scales)
        intercept = float(self.estimator.intercept_[0] - np.dot(slopes, self.state.means))
        return {"intercept": intercept,
                **{name: float(value) for name, value in zip(SLOPE_NAMES, slopes)}}


def tune_and_fit(train: pd.DataFrame, group_col: str, seed: int,
                 c_grid=C_GRID, n_splits: int = 5) -> FitBundle:
    grid = sorted(set(float(c) for c in c_grid))
    if not grid or not all(np.isfinite(c) and c > 0 for c in grid):
        raise ValueError("Penalty grid must contain finite positive values")
    folds = group_folds(train, group_col, seed, n_splits)
    prepared = []
    for fold in range(n_splits):
        fit_rows, test_rows = train.iloc[folds != fold], train.iloc[folds == fold]
        if not set(fit_rows[group_col]).isdisjoint(test_rows[group_col]):
            raise AssertionError("Original groups overlap inside tuning")
        if fit_rows["y_n"].nunique() != 2 or test_rows.empty:
            raise UnsupportedSampleError("Unsupported inner training or test sample")
        state = learn_preprocessor(fit_rows)
        prepared.append((fold, fit_rows, test_rows,
                         transform(fit_rows, state), transform(test_rows, state)))
    inner_records, grid_records = [], []
    for penalty_c in grid:
        squared_error_sum, people, fold_losses = 0.0, 0, []
        all_converged = True
        for fold, fit_rows, test_rows, x_fit, x_test in prepared:
            error_type = ""
            try:
                estimator, converged, iterations = _fit_logistic(
                    x_fit, fit_rows["y_n"].to_numpy(), penalty_c)
                probability = estimator.predict_proba(x_test)[:, 1]
                loss = float(np.mean((probability - test_rows["y_n"].to_numpy()) ** 2))
                if not np.isfinite(loss):
                    converged = False
            except (ValueError, RuntimeError, FloatingPointError) as error:
                converged, iterations, loss = False, 0, float("nan")
                error_type = type(error).__name__
            all_converged = all_converged and converged
            squared_error_sum += loss * len(test_rows)
            people += len(test_rows)
            fold_losses.append(loss)
            inner_records.append({
                "inner_seed": int(seed), "inner_fold": fold, "C": penalty_c,
                "grouping": group_col, "train_people": len(fit_rows),
                "test_people": len(test_rows),
                "train_households": int(fit_rows["uqno"].nunique()),
                "test_households": int(test_rows["uqno"].nunique()),
                "train_groups": int(fit_rows[group_col].nunique()),
                "test_groups": int(test_rows[group_col].nunique()),
                "train_events": int(fit_rows["y_n"].sum()),
                "test_events": int(test_rows["y_n"].sum()),
                "brier": loss, "converged": bool(converged),
                "iterations": iterations, "error_type": error_type,
            })
        grid_records.append({
            "C": penalty_c, "pooled_inner_brier": squared_error_sum / people,
            "mean_fold_brier": float(np.mean(fold_losses)),
            "inner_people": people, "inner_folds": n_splits,
            "all_inner_converged": bool(all_converged),
        })
    try:
        selected_c = select_penalty(grid_records)
    except UnsupportedSampleError as error:
        error.inner_records = inner_records
        error.grid_records = grid_records
        raise
    for row in grid_records:
        row["selected"] = row["C"] == selected_c
    state = learn_preprocessor(train)
    try:
        estimator, converged, iterations = _fit_logistic(
            transform(train, state), train["y_n"].to_numpy(), selected_c)
    except (ValueError, RuntimeError, FloatingPointError) as error:
        raise UnsupportedSampleError(
            f"Selected final ridge fit failed: {type(error).__name__}",
            inner_records=inner_records, grid_records=grid_records,
            final_attempted=True, final_converged=False) from error
    if not converged:
        raise UnsupportedSampleError("Selected final ridge fit did not converge",
                                     inner_records=inner_records, grid_records=grid_records,
                                     final_attempted=True, final_converged=False)
    return FitBundle(estimator, state, selected_c, inner_records, grid_records,
                     converged, iterations)


def _calibration(y: np.ndarray, probability: np.ndarray) -> dict:
    clipped = np.clip(probability, PROB_CLIP, 1 - PROB_CLIP)
    z = np.log(clipped / (1 - clipped))
    # Offset model: solve the intercept score with slope fixed at one.
    intercept = float(brentq(lambda a: float(np.sum(expit(a + z) - y)),
                             -50.0, 50.0, xtol=1e-12))
    result = {"calibration_in_the_large": intercept,
              "calibration_slope": float("nan"),
              "calibration_slope_valid": False,
              "calibration_status": "constant_prediction"}
    if np.ptp(z) <= 1e-8:
        return result
    # A separating calibration predictor has no finite unpenalised slope.
    z0, z1 = z[y == 0], z[y == 1]
    if z0.max() <= z1.min() or z1.max() <= z0.min():
        result["calibration_status"] = "complete_or_quasi_separation"
        return result
    center, spread = float(z.mean()), float(z.std(ddof=0))
    design = np.column_stack([np.ones(len(z)), (z - center) / spread])
    def objective(theta):
        eta = design @ theta
        value = float(np.sum(np.logaddexp(0, eta) - y * eta))
        gradient = design.T @ (expit(eta) - y)
        return value, gradient
    fitted = minimize(objective, np.array([0.0, spread]), jac=True,
                      method="L-BFGS-B",
                      options={"maxiter": 1000, "ftol": 1e-14, "gtol": 1e-9})
    if not np.isfinite(fitted.x).all():
        result["calibration_status"] = "calibration_fit_failed"
        return result
    fitted_prob = expit(design @ fitted.x)
    hessian = design.T @ ((fitted_prob * (1 - fitted_prob))[:, None] * design)
    eigenvalues = np.linalg.eigvalsh(hessian)
    _, gradient = objective(fitted.x)
    valid = bool(fitted.success and np.isfinite(fitted.x).all()
                 and np.linalg.norm(gradient, ord=np.inf) < 1e-5
                 and eigenvalues.min() > 1e-10)
    result["calibration_status"] = "ok" if valid else "calibration_fit_failed"
    result["calibration_slope_valid"] = valid
    if valid:
        result["calibration_slope"] = float(fitted.x[1] / spread)
    return result


def metrics(y: np.ndarray, probability: np.ndarray) -> dict:
    """Unweighted person-level probability metrics and unpenalised calibration."""
    y, probability = np.asarray(y), np.asarray(probability, dtype=float)
    if (y.ndim != 1 or probability.shape != y.shape or not len(y)
            or not np.isin(y, [0, 1]).all() or np.unique(y).size != 2):
        raise UnsupportedSampleError("Metrics require both observed outcome classes")
    if not np.isfinite(probability).all() or np.any((probability < 0) | (probability > 1)):
        raise UnsupportedSampleError("Probabilities must be finite and between zero and one")
    return {
        "prevalence": float(y.mean()),
        "roc_auc": float(roc_auc_score(y, probability)),
        "average_precision": float(average_precision_score(y, probability)),
        "brier": float(brier_score_loss(y, probability)),
        "log_loss": float(log_loss(y, probability, labels=[0, 1])),
        **_calibration(y.astype(float), probability),
    }
