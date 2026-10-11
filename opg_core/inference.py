"""Load a reviewed JSON model and score eligible rows without fitting."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping

import numpy as np
import pandas as pd

from opg_core.features import (
    CATEGORICAL_FIELDS, FEATURE_ORDER, STAT_CODES, TRAINING_STAT_FIELDS,
    build_matrix, prepare_features,
)
from opg_core.schema import CONTEXT, MODEL_FIELDS, SCHEMA_VERSION
from opg_core.screening import RULE_VERSION

ARTIFACT_SCHEMA_VERSION = "opg-frozen-logit-v1"
MODEL_VERSION = "opg-kzn-six-slope-v1"
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
SCORE_CONTEXT = "Frozen full-data fitted scores; training overlap unknown; not held-out performance"
REFERENCE_LEVELS = {
    "sex": "male (code 1)", "schooling": "Grade 7 or above",
    "settlement": "urban formal; traditional area and rural formal share one contrast",
    "welfare": "nearer than 5 km",
}
EVALUATION_SCHEMA_VERSION = "opg-heldout-evaluation-v1"
_SOURCE_ROOT = Path(__file__).resolve().parents[1]
_GUARDED_SOURCES = {
    "source_script_sha256": (
        "analysis/phase3_build_cohort.py", "analysis/phase4_rq1.py", "analysis/phase5_model.py",
    ),
    "adapter_script_sha256": (
        "opg_core/features.py", "opg_core/schema.py", "opg_core/screening.py",
    ),
}


@dataclass(frozen=True)
class FrozenModel:
    intercept: float
    coefficients: tuple[float, ...]
    training_stats: Mapping
    manifest: dict

    def predict_matrix(self, matrix: pd.DataFrame) -> np.ndarray:
        """Predict in the fixed feature order with a numerically stable logistic."""
        if not isinstance(matrix, pd.DataFrame) or tuple(matrix.columns) != FEATURE_ORDER:
            raise ValueError("Model feature columns or their order are invalid.")
        values = matrix.to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError("Model features must be finite numeric values.")
        linear = self.intercept + values @ np.asarray(self.coefficients)
        probability = np.empty(len(linear), dtype=float)
        positive = linear >= 0
        probability[positive] = 1 / (1 + np.exp(-linear[positive]))
        exponent = np.exp(linear[~positive])
        probability[~positive] = exponent / (1 + exponent)
        if not np.isfinite(probability).all():
            raise ValueError("Model produced a nonfinite probability.")
        return probability


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Model JSON contains duplicate fields.")
        result[key] = value
    return result


def _read_json(path: Path) -> tuple[dict, bytes]:
    try:
        content = path.read_bytes()
        if len(content) > 1024 * 1024:
            raise ValueError("Frozen model metadata exceeds the supported size.")
        parsed = json.loads(content, object_pairs_hook=_pairs)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Frozen model artifact is missing or invalid.") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Frozen model JSON must contain an object.")
    return parsed, content


def _number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and np.isfinite(value)


def _validate_live_code(manifest: dict) -> None:
    """Fail closed when live scientific/preprocessing code differs from the fit.

    Inference's loader and checksum guard are intentionally excluded: adding a
    runtime integrity check does not change the retained predictor transforms.
    """
    signature = manifest.get("source_signature")
    if not isinstance(signature, dict):
        raise ValueError("Frozen model source provenance is missing or invalid.")
    for group, names in _GUARDED_SOURCES.items():
        recorded = signature.get(group)
        if not isinstance(recorded, dict):
            raise ValueError("Frozen model source provenance is missing or invalid.")
        for name in names:
            expected = recorded.get(name)
            if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
                raise ValueError("Frozen model source provenance is missing or invalid.")
            try:
                current = hashlib.sha256((_SOURCE_ROOT / name).read_bytes()).hexdigest()
            except OSError as exc:
                raise ValueError("Current scientific preprocessing source cannot be verified.") from exc
            if current != expected:
                raise ValueError("Frozen model preprocessing provenance does not match current code; review and rebuild offline.")


def load_model(model_dir: Path | str = MODEL_DIR) -> FrozenModel:
    """Read validated coefficients and imputation statistics from local JSON.

    No data are read for fitting, and this function never generates an artifact.
    Missing/stale artifacts require the explicit offline freeze command.
    """
    directory = Path(model_dir)
    artifact, content = _read_json(directory / "logistic_model.json")
    manifest, _ = _read_json(directory / "manifest.json")
    required = {
        "artifact_schema_version", "model_version", "estimator", "feature_order",
        "predictor_sources", "intercept", "coefficients", "training_stats", "reference_levels",
    }
    if set(artifact) != required:
        raise ValueError("Frozen model artifact fields are invalid.")
    if artifact["artifact_schema_version"] != ARTIFACT_SCHEMA_VERSION or artifact["model_version"] != MODEL_VERSION:
        raise ValueError("Frozen model artifact version is unsupported.")
    if artifact["estimator"] != "unweighted logistic regression" or artifact["feature_order"] != list(FEATURE_ORDER):
        raise ValueError("Frozen model feature specification or order is invalid.")
    if artifact["predictor_sources"] != list(MODEL_FIELDS):
        raise ValueError("Frozen model predictor sources are invalid.")
    if not _number(artifact["intercept"]):
        raise ValueError("Frozen model intercept is invalid.")
    coefficients = artifact["coefficients"]
    if not isinstance(coefficients, list) or len(coefficients) != len(FEATURE_ORDER) or not all(_number(value) for value in coefficients):
        raise ValueError("Frozen model coefficients are invalid.")
    stats = artifact["training_stats"]
    if not isinstance(stats, dict) or set(stats) != set(TRAINING_STAT_FIELDS):
        raise ValueError("Frozen imputer fields are invalid.")
    if not _number(stats["age_per_10_median"]) or not 0 <= stats["age_per_10_median"] <= 4.5:
        raise ValueError("Frozen age imputer is invalid.")
    for field, codes in STAT_CODES.items():
        if not isinstance(stats[field], str) or stats[field] not in codes:
            raise ValueError("Frozen categorical imputer contains an unsupported code.")
    if artifact["reference_levels"] != REFERENCE_LEVELS:
        raise ValueError("Frozen model reference metadata is invalid.")
    digest = hashlib.sha256(content).hexdigest()
    expected_manifest = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION, "model_version": MODEL_VERSION,
        "data_schema_version": SCHEMA_VERSION, "study_context": CONTEXT,
        "rule_version": RULE_VERSION, "artifact_sha256": digest,
        "feature_order": list(FEATURE_ORDER), "score_context": SCORE_CONTEXT,
    }
    if any(manifest.get(key) != value for key, value in expected_manifest.items()):
        raise ValueError("Frozen model manifest metadata or artifact checksum does not match.")
    _validate_live_code(manifest)
    _validated_evaluation(directory, manifest)
    return FrozenModel(
        float(artifact["intercept"]), tuple(float(value) for value in coefficients),
        MappingProxyType(dict(stats)), dict(manifest),
    )


def _validated_evaluation(directory: Path, manifest: dict) -> dict:
    evaluation, content = _read_json(directory / "evaluation.json")
    if manifest.get("evaluation_sha256") != hashlib.sha256(content).hexdigest():
        raise ValueError("Frozen model evaluation checksum does not match.")
    if evaluation.get("schema_version") != EVALUATION_SCHEMA_VERSION or evaluation.get("model_version") != MODEL_VERSION:
        raise ValueError("Frozen model aggregate evaluation version is unsupported.")
    if evaluation.get("cohort") != manifest.get("training_cohort"):
        raise ValueError("Frozen model aggregate evaluation population does not match.")
    return evaluation


def load_evaluation(model_dir: Path | str = MODEL_DIR, model: FrozenModel | None = None) -> dict:
    """Load aggregate held-out evidence bound to the reviewed model manifest."""
    frozen = load_model(model_dir) if model is None else model
    if not isinstance(frozen, FrozenModel):
        raise ValueError("Evaluation requires a validated frozen model.")
    _validate_live_code(frozen.manifest)
    return _validated_evaluation(Path(model_dir), frozen.manifest)


def score_frame(screened: pd.DataFrame, model: FrozenModel | None = None) -> pd.DataFrame:
    """Return screening columns unchanged and add research probabilities.

    Only PASS rows with resolved receipt and the screening adapter's eligibility
    flag can receive a score. No outcome value enters feature preparation.
    """
    if not isinstance(screened, pd.DataFrame):
        raise ValueError("Scoring input must be a table.")
    if screened.columns.duplicated().any():
        raise ValueError("Scoring input contains duplicate columns.")
    gate_fields = {"screen_status", "receipt_status", "model_eligible_for_scoring"}
    if not gate_fields.issubset(screened.columns):
        raise ValueError("Scoring requires screening status, receipt status, and the eligibility flag.")
    if not screened["model_eligible_for_scoring"].map(lambda value: isinstance(value, (bool, np.bool_))).all():
        raise ValueError("Model eligibility flags must be boolean.")
    if not screened["screen_status"].isin(["PASS", "FAIL", "UNRESOLVED", "OUT_OF_FRAME"]).all():
        raise ValueError("Screening status is unsupported.")
    if not screened["receipt_status"].isin(["RECIPIENT", "NON_RECIPIENT", "UNRESOLVED", "NOT_ASSESSED"]).all():
        raise ValueError("Receipt status is unsupported.")
    frozen = load_model() if model is None else model
    if not isinstance(frozen, FrozenModel):
        raise ValueError("Scoring requires a validated frozen model.")
    _validate_live_code(frozen.manifest)
    prepared = prepare_features(screened)
    eligible = (
        screened["model_eligible_for_scoring"] & (screened["screen_status"] == "PASS")
        & screened["receipt_status"].isin(["RECIPIENT", "NON_RECIPIENT"])
    )
    missing_categories = prepared.loc[:, CATEGORICAL_FIELDS].isna().all(axis=1)
    valid_age = prepared["age_per_10"].notna() & (prepared["age_per_10"] >= 0)
    can_score = eligible & ~missing_categories & valid_age
    out = screened.copy(deep=True)
    out["predicted_nonreceipt"] = pd.array([pd.NA] * len(out), dtype="Float64")
    out["model_version"] = frozen.manifest["model_version"]
    contexts = np.full(len(out), "Not scored: outside the resolved apparently eligible cohort", dtype=object)
    eligible_positions = eligible.to_numpy(dtype=bool)
    contexts[eligible_positions & ~valid_age.to_numpy()] = "Not scored: age is missing or outside the model population"
    contexts[eligible_positions & missing_categories.to_numpy()] = "Not scored: all categorical predictors are missing or unsupported"
    score_positions = np.flatnonzero(can_score.to_numpy(dtype=bool))
    if len(score_positions):
        matrix = build_matrix(prepared.iloc[score_positions], frozen.training_stats)
        probabilities = frozen.predict_matrix(matrix)
        out.iloc[score_positions, out.columns.get_loc("predicted_nonreceipt")] = probabilities
        contexts[score_positions] = SCORE_CONTEXT
    out["score_context"] = contexts
    return out
