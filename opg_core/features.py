"""Outcome-independent adapter to the retained research predictor coding."""

from __future__ import annotations

import sys
from pathlib import Path
from collections.abc import Mapping

import numpy as np
import pandas as pd

from opg_core.schema import MODEL_FIELDS

_ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
if str(_ANALYSIS) not in sys.path:
    sys.path.insert(0, str(_ANALYSIS))
import phase4_rq1 as description  # noqa: E402
import phase5_model as historical_model  # noqa: E402

FEATURE_ORDER = (
    "age_per_10", "sex_female", "school_below", "settle_urban_informal",
    "settle_traditional_or_rural", "welfare_far",
)
PREPARED_FIELDS = (
    "age_per_10", "sex_code", "school_code", "settlement_code", "welfare_code",
)
CATEGORICAL_FIELDS = PREPARED_FIELDS[1:]
TRAINING_STAT_FIELDS = (
    "age_per_10_median", "sex_code", "school_code", "settlement_code", "welfare_code",
)
STAT_CODES = {
    "sex_code": {"1", "2"}, "school_code": {"0", "1"},
    "settlement_code": {"1", "2", "4", "5"}, "welfare_code": {"0", "1"},
}


def _code(value) -> str | None:
    """Normalize integer source codes; missing/unsupported values stay missing."""
    if value is None or pd.isna(value) or isinstance(value, (bool, np.bool_)):
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.isascii() and text.isdigit() and len(text) <= 3:
        return str(int(text))
    if isinstance(value, (int, float, np.integer, np.floating)):
        number = float(value)
        if np.isfinite(number) and number.is_integer() and 0 <= number <= 999:
            return str(int(number))
    return None


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Prepare the five predictor sources without reading any outcome fields.

    Extra screening/output columns are ignored. Missing or unsupported category
    codes remain missing for the frozen training imputer; nothing is fitted here.
    Ages must be whole historical survey ages from 0 through 105 when supplied.
    """
    if not isinstance(frame, pd.DataFrame):
        raise ValueError("Predictor input must be a table.")
    if frame.columns.duplicated().any():
        raise ValueError("Predictor input contains duplicate columns.")
    if not set(MODEL_FIELDS).issubset(frame.columns):
        raise ValueError("Predictor input must include all five source columns.")
    for name in MODEL_FIELDS:
        if frame[name].map(lambda value: isinstance(value, (list, dict, tuple, set))).any():
            raise ValueError("Predictor values must be scalar.")
    ages = frame["age"]
    missing_age = ages.isna() | ages.map(lambda value: isinstance(value, str) and not value.strip())
    numeric = pd.to_numeric(ages.where(~missing_age), errors="coerce")
    age_values = numeric.to_numpy(dtype=float, na_value=np.nan)
    supplied = ~missing_age.to_numpy()
    invalid = supplied & (
        ~np.isfinite(age_values) | (age_values < 0) | (age_values > 105)
        | (age_values != np.floor(age_values))
    )
    if ages.map(lambda value: isinstance(value, (bool, np.bool_))).any() or invalid.any():
        raise ValueError("Age predictors must be finite whole values from 0 to 105.")

    sex = frame["sex"].map(_code)
    school = frame["schooling_raw"].map(_code)
    settlement = frame["settlement"].map(_code)
    welfare = frame["welfare_distance"].map(_code)
    school_labels = school.map(lambda code: description.schooling_class(code) if code is not None else "Not assigned")
    welfare_labels = welfare.map(lambda code: description.welfare_class(code) if code is not None else "Missing")
    return pd.DataFrame({
        "age_per_10": (numeric - 60) / 10,
        "sex_code": sex.where(sex.isin(["1", "2"])),
        "school_code": school_labels.map({"Grade 7 or above": "0", "Below Grade 7": "1"}),
        "settlement_code": settlement.where(settlement.isin(["1", "2", "4", "5"])),
        "welfare_code": welfare_labels.map({"Nearer than 5 km": "0", "At least 5 km or unavailable": "1"}),
    }, index=frame.index).loc[:, PREPARED_FIELDS]


def build_matrix(prepared: pd.DataFrame, training_stats: Mapping) -> pd.DataFrame:
    """Apply already learned statistics and use the original six-slope matrix."""
    if not isinstance(prepared, pd.DataFrame) or tuple(prepared.columns) != PREPARED_FIELDS:
        raise ValueError("Prepared predictor columns or their order are invalid.")
    if set(training_stats) != set(TRAINING_STAT_FIELDS):
        raise ValueError("Frozen imputer fields are invalid.")
    for name, codes in STAT_CODES.items():
        if training_stats[name] not in codes:
            raise ValueError("Frozen categorical imputer contains an unsupported code.")
    median = training_stats["age_per_10_median"]
    if isinstance(median, (bool, np.bool_)) or not isinstance(median, (int, float)) or not np.isfinite(median):
        raise ValueError("Frozen age imputer is invalid.")
    filled = historical_model.apply_stats(prepared, dict(training_stats))
    matrix = historical_model.model_matrix(filled)
    if tuple(matrix.columns) != FEATURE_ORDER or not np.isfinite(matrix.to_numpy(dtype=float)).all():
        raise ValueError("Frozen predictor matrix is invalid.")
    return matrix
