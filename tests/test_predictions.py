"""Frozen inference safeguards using synthetic rows and local reference parity.

No model is fitted, and no respondent-level fixture or output is written.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from opg_core.features import build_matrix, prepare_features
from opg_core.inference import load_evaluation, load_model, score_frame
from opg_core.schema import synthetic_template
from opg_core.screening import screen_frame

ROOT = Path(__file__).resolve().parents[1]
FEATURE_ORDER = [
    "age_per_10", "sex_female", "school_below", "settle_urban_informal",
    "settle_traditional_or_rural", "welfare_far",
]


def scoring_rows(count=1):
    """Invented, already-screened rows; receipt/outcome are never predictors."""
    return pd.DataFrame({
        "record_id": [f"SYN-{index:03d}" for index in range(count)],
        "age": [70] * count, "sex": ["2"] * count,
        "schooling_raw": ["8"] * count, "settlement": ["1"] * count,
        "welfare_distance": ["3"] * count, "screen_status": ["PASS"] * count,
        "receipt_status": ["NON_RECIPIENT"] * count,
        "model_eligible_for_scoring": [True] * count,
        "y": ["1"] * count, "reason_codes": ["PASS_OBSERVABLE_RULES"] * count,
    })


def test_synthetic_workflow_scores_only_the_two_eligible_screen_outcomes():
    screened = screen_frame(synthetic_template())
    before = screened.copy(deep=True)
    first = score_frame(screened)
    second = score_frame(screened)
    pd.testing.assert_frame_equal(screened, before)
    pd.testing.assert_frame_equal(first, second)
    pd.testing.assert_frame_equal(first[before.columns], before)
    assert first.predicted_nonreceipt.notna().tolist() == [True, True, False, False, False, False]
    probability = first.predicted_nonreceipt.dropna().to_numpy(dtype=float)
    assert np.isfinite(probability).all()
    assert ((probability > 0) & (probability < 1)).all()
    assert str(first.predicted_nonreceipt.dtype) == "Float64"
    assert first.model_version.nunique() == 1
    assert first.model_version.iloc[0] == load_model().manifest["model_version"]
    assert first.score_context.dropna().ne("").all()


@pytest.mark.parametrize("field,value", [
    ("screen_status", "FAIL"), ("screen_status", "UNRESOLVED"),
    ("screen_status", "OUT_OF_FRAME"), ("receipt_status", "UNRESOLVED"),
    ("receipt_status", "NOT_ASSESSED"), ("model_eligible_for_scoring", False),
])
def test_every_scoring_gate_is_required_even_if_other_fields_look_eligible(field, value):
    frame = scoring_rows()
    frame[field] = value
    assert score_frame(frame).predicted_nonreceipt.isna().all()


def test_known_receipt_and_nonreceipt_are_both_scored_without_using_outcome():
    frame = scoring_rows(2)
    frame.loc[1, ["receipt_status", "y", "reason_codes"]] = ["RECIPIENT", "0", "SYN_OTHER_REASON"]
    prediction = score_frame(frame).predicted_nonreceipt
    assert prediction.notna().all()
    assert prediction.iloc[0] == prediction.iloc[1]
    changed = frame.copy()
    changed["y"] = ["not-an-outcome", None]
    changed["reason_codes"] = ["SYN-CHANGED", ""]
    changed["combined_private_income"] = [0, 10**12]
    changed["person_weight"] = [0.1, 999999]
    pd.testing.assert_series_equal(score_frame(changed).predicted_nonreceipt, prediction)
    without_outcome = changed.drop(columns=["y", "reason_codes"])
    pd.testing.assert_series_equal(score_frame(without_outcome).predicted_nonreceipt, prediction)


def test_feature_preparation_uses_only_the_five_allowed_source_columns():
    frame = scoring_rows(2)
    prepared = prepare_features(frame)
    assert list(prepared.columns) == [
        "age_per_10", "sex_code", "school_code", "settlement_code", "welfare_code",
    ]
    pd.testing.assert_frame_equal(
        prepare_features(frame[["age", "sex", "schooling_raw", "settlement", "welfare_distance"]]),
        prepared,
    )
    changed = frame.copy()
    changed["y"] = ["0", "INVALID"]
    changed["receipt_status"] = ["RECIPIENT", "UNRESOLVED"]
    changed["screen_status"] = ["FAIL", "UNRESOLVED"]
    changed["private_income"] = [100000, 200000]
    pd.testing.assert_frame_equal(prepare_features(changed), prepared)


@pytest.mark.parametrize("age", [None, "", pd.NA, np.nan])
def test_missing_age_is_not_imputed_into_a_score(age):
    frame = scoring_rows()
    frame["age"] = age
    assert score_frame(frame).predicted_nonreceipt.isna().all()


@pytest.mark.parametrize("codes", [
    ["", "", "", ""], [None, None, None, None],
    ["99", "99", "99", "99"], ["unsupported"] * 4,
    ["", "21", "", "9"],
])
def test_all_four_categorical_predictors_unavailable_do_not_receive_a_score(codes):
    frame = scoring_rows()
    for field, code in zip(("sex", "schooling_raw", "settlement", "welfare_distance"), codes):
        frame[field] = code
    assert score_frame(frame).predicted_nonreceipt.isna().all()


def test_row_and_column_order_and_nonstandard_index_do_not_change_predictions():
    frame = scoring_rows(4)
    frame["age"] = [60, 70, 80, 90]
    frame.index = pd.Index([17, 41, 5, 93], name="synthetic_index")
    expected = score_frame(frame)
    shuffled = frame.iloc[[2, 0, 3, 1], ::-1]
    actual = score_frame(shuffled)
    pd.testing.assert_series_equal(
        actual.predicted_nonreceipt.reindex(frame.index), expected.predicted_nonreceipt,
    )
    assert actual.index.equals(shuffled.index)


@pytest.mark.parametrize("flag", ["True", "False", "1", 1, 0, None])
def test_truthy_strings_and_numeric_scoring_flags_cannot_bypass_boolean_gate(flag):
    frame = scoring_rows()
    frame["model_eligible_for_scoring"] = flag
    with pytest.raises(ValueError):
        score_frame(frame)


@pytest.mark.parametrize("field,value", [
    ("screen_status", "eligible"), ("receipt_status", "unknown"),
])
def test_unrecognized_screening_states_are_rejected(field, value):
    frame = scoring_rows()
    frame[field] = value
    with pytest.raises(ValueError):
        score_frame(frame)


@pytest.mark.parametrize("frame", [None, [], {"age": 70}])
def test_non_table_input_is_rejected(frame):
    with pytest.raises(ValueError):
        score_frame(frame)


@pytest.mark.parametrize("field", [
    "age", "sex", "schooling_raw", "settlement", "welfare_distance",
    "screen_status", "receipt_status", "model_eligible_for_scoring",
])
def test_missing_required_input_column_is_rejected(field):
    with pytest.raises(ValueError):
        score_frame(scoring_rows().drop(columns=field))


def test_duplicate_column_names_are_rejected_before_feature_selection():
    frame = scoring_rows()
    frame = pd.concat([frame, frame[["sex"]]], axis=1)
    with pytest.raises(ValueError):
        score_frame(frame)


@pytest.mark.parametrize("age", ["not-age", -1, 106, 70.5, True, np.inf, -np.inf, "NaN"])
def test_invalid_age_is_rejected_instead_of_silently_imputed(age):
    frame = scoring_rows()
    frame["age"] = age
    with pytest.raises(ValueError):
        score_frame(frame)


def test_loaded_predictions_match_original_statsmodels_formula_on_synthetic_boundaries():
    """Independent design plus saved original coefficients; no fitting occurs."""
    import statsmodels.api as sm

    coefficients_path = ROOT / "output" / "phase5" / "apparent_coefficients.csv"
    if not coefficients_path.exists():
        pytest.skip("Local saved scientific reference coefficients are unavailable.")
    cases = list(itertools.product(
        [60, 70, 105], ["1", "2"], ["1", "7", "8", "20", "23", "30", "98"],
        ["1", "2", "4", "5"], ["1", "4", "5", "8"],
    ))
    frame = scoring_rows(len(cases))
    frame[["age", "sex", "schooling_raw", "settlement", "welfare_distance"]] = cases
    design = np.array([
        [1, (age - 60) / 10, sex == "2", school in {"1", "7", "98"},
         settlement == "2", settlement in {"4", "5"}, welfare in {"5", "8"}]
        for age, sex, school, settlement, welfare in cases
    ], dtype=float)
    saved = pd.read_csv(coefficients_path).set_index("term")
    parameters = saved.loc[["intercept", *FEATURE_ORDER], "coefficient"].to_numpy()
    reference = sm.Logit(np.arange(len(design)) % 2, design).predict(parameters, design)
    first = score_frame(frame, load_model()).predicted_nonreceipt.to_numpy(dtype=float)
    reloaded = score_frame(frame, load_model()).predicted_nonreceipt.to_numpy(dtype=float)
    assert np.isfinite(first).all()
    np.testing.assert_allclose(first, reference, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(first, reloaded)


@pytest.mark.parametrize("source,prepared,missing,raw_modes", [
    ("sex", "sex_code", "", {"1": "1", "2": "2"}),
    ("schooling_raw", "school_code", "99", {"0": "8", "1": "1"}),
    ("settlement", "settlement_code", "", {code: code for code in ["1", "2", "4", "5"]}),
    ("welfare_distance", "welfare_code", "9", {"0": "1", "1": "5"}),
])
def test_partial_missingness_uses_frozen_training_mode_not_upload_mode(source, prepared, missing, raw_modes):
    model = load_model()
    mode = model.training_stats[prepared]
    other = next(code for code in raw_modes if code != mode)
    frame = scoring_rows(5)
    frame[source] = raw_modes[other]
    frame.loc[0, source] = missing
    frame.loc[1, source] = raw_modes[mode]
    expected = score_frame(frame, model).predicted_nonreceipt
    assert expected.notna().all()
    assert expected.iloc[0] == expected.iloc[1]
    assert expected.iloc[0] != expected.iloc[2]
    singleton = score_frame(frame.iloc[[0]], model).predicted_nonreceipt
    assert singleton.iloc[0] == expected.iloc[0]


def test_three_missing_categories_are_imputed_when_one_is_usable():
    model = load_model()
    frame = scoring_rows(2)
    frame.loc[0, ["sex", "schooling_raw", "settlement"]] = ["", "99", ""]
    stats = model.training_stats
    frame.loc[1, ["sex", "schooling_raw", "settlement"]] = [
        stats["sex_code"], "8" if stats["school_code"] == "0" else "1",
        stats["settlement_code"],
    ]
    prediction = score_frame(frame, model).predicted_nonreceipt
    assert prediction.notna().all()
    assert prediction.iloc[0] == prediction.iloc[1]


def test_frozen_matrix_and_predictor_order_are_enforced():
    model = load_model()
    prepared = prepare_features(scoring_rows())
    with pytest.raises(ValueError):
        build_matrix(prepared.iloc[:, ::-1], model.training_stats)
    matrix = build_matrix(prepared, model.training_stats)
    with pytest.raises(ValueError):
        model.predict_matrix(matrix.iloc[:, ::-1])
    matrix["age_per_10"] = np.inf
    with pytest.raises(ValueError):
        model.predict_matrix(matrix)


@pytest.fixture
def artifact_copy(tmp_path):
    """Copy only aggregate JSON metadata, never private training rows."""
    for name in ("logistic_model.json", "manifest.json", "evaluation.json"):
        (tmp_path / name).write_bytes((ROOT / "models" / name).read_bytes())
    return tmp_path


def rewrite_artifact(directory, mutate):
    path = directory / "logistic_model.json"
    artifact = json.loads(path.read_text())
    mutate(artifact)
    content = json.dumps(artifact, sort_keys=True).encode()
    path.write_bytes(content)
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["artifact_sha256"] = hashlib.sha256(content).hexdigest()
    manifest_path.write_text(json.dumps(manifest))


@pytest.mark.parametrize("mutate", [
    lambda item: item.update(artifact_schema_version="unknown"),
    lambda item: item.update(model_version="unknown"),
    lambda item: item.update(estimator="weighted logistic regression"),
    lambda item: item.update(feature_order=item["feature_order"][::-1]),
    lambda item: item.update(predictor_sources=["y", *item["predictor_sources"][1:]]),
    lambda item: item.update(intercept=float("nan")),
    lambda item: item.update(intercept=True),
    lambda item: item.update(coefficients=item["coefficients"][:-1]),
    lambda item: item.update(coefficients=[float("inf"), *item["coefficients"][1:]]),
    lambda item: item.update(coefficients=["0", *item["coefficients"][1:]]),
    lambda item: item["training_stats"].update(age_per_10_median=float("inf")),
    lambda item: item["training_stats"].update(age_per_10_median=-1),
    lambda item: item["training_stats"].update(sex_code="9"),
    lambda item: item["training_stats"].update(school_code="98"),
    lambda item: item["training_stats"].pop("welfare_code"),
    lambda item: item["training_stats"].update(unexpected="1"),
    lambda item: item.update(reference_levels={}),
    lambda item: item["reference_levels"].update(sex="unsupported reference"),
    lambda item: item.update(unexpected_field="SYN"),
], ids=[
    "schema-version", "model-version", "estimator", "feature-order", "forbidden-source",
    "nan-intercept", "boolean-intercept", "coefficient-length", "nonfinite-coefficient",
    "nonnumeric-coefficient", "nonfinite-median", "invalid-median", "invalid-sex-mode",
    "invalid-school-mode", "missing-mode", "unexpected-mode", "reference-fields", "reference-values", "extra-artifact-field",
])
def test_invalid_artifact_rejected_even_with_a_matching_checksum(artifact_copy, mutate):
    rewrite_artifact(artifact_copy, mutate)
    with pytest.raises(ValueError):
        load_model(artifact_copy)


@pytest.mark.parametrize("field,value", [
    ("artifact_sha256", "0" * 64), ("evaluation_sha256", "0" * 64), ("model_version", "unknown"),
    ("artifact_schema_version", "unknown"), ("data_schema_version", "unknown"),
    ("study_context", "unknown"), ("rule_version", "unknown"),
    ("feature_order", FEATURE_ORDER[::-1]), ("score_context", "held-out predictions"),
])
def test_manifest_contract_and_checksum_must_match(artifact_copy, field, value):
    path = artifact_copy / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest[field] = value
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        load_model(artifact_copy)


@pytest.mark.parametrize("field,value", [
    ("schema_version", "unknown"), ("model_version", "unknown"),
    ("cohort", {"people": 1013, "events": 68, "households": 827}),
])
def test_invalid_evaluation_rejected_even_with_a_matching_checksum(artifact_copy, field, value):
    path = artifact_copy / "evaluation.json"
    evaluation = json.loads(path.read_text())
    evaluation[field] = value
    content = json.dumps(evaluation).encode()
    path.write_bytes(content)
    manifest_path = artifact_copy / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["evaluation_sha256"] = hashlib.sha256(content).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        load_model(artifact_copy)
    with pytest.raises(ValueError):
        load_evaluation(artifact_copy)


def test_evaluation_tampering_is_detected_by_both_model_and_evaluation_loaders(artifact_copy):
    model = load_model(artifact_copy)
    path = artifact_copy / "evaluation.json"
    evaluation = json.loads(path.read_text())
    evaluation["metrics"]["logistic_out_of_fold"]["roc_auc"] = 1.0
    path.write_text(json.dumps(evaluation))
    with pytest.raises(ValueError):
        load_model(artifact_copy)
    with pytest.raises(ValueError):
        load_evaluation(artifact_copy, model)


@pytest.mark.parametrize("name", ["logistic_model.json", "manifest.json", "evaluation.json"])
def test_missing_artifacts_are_not_generated_during_loading(artifact_copy, name):
    path = artifact_copy / name
    path.unlink()
    with pytest.raises(ValueError):
        load_model(artifact_copy)
    assert not path.exists()


@pytest.mark.parametrize("content", [b"{", b"[]", b"{\"x\":1,\"x\":2}", b"\xff"])
def test_malformed_nonobject_and_duplicate_key_json_is_rejected(artifact_copy, content):
    (artifact_copy / "logistic_model.json").write_bytes(content)
    with pytest.raises(ValueError):
        load_model(artifact_copy)


def test_import_loading_and_scoring_never_fit_a_model():
    """Fresh interpreter catches training at import time as well as inference."""
    code = """
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

def forbidden_fit(*args, **kwargs):
    raise AssertionError('Inference attempted to train a model.')

sm.Logit.fit = forbidden_fit
sm.GLM.fit = forbidden_fit
LogisticRegression.fit = forbidden_fit

from opg_core.features import historical_model
historical_model.fit_logit = forbidden_fit
historical_model.learning_stats = forbidden_fit
from opg_core.inference import load_model, score_frame
from opg_core.schema import synthetic_template
from opg_core.screening import screen_frame

result = score_frame(screen_frame(synthetic_template()), load_model())
assert result.predicted_nonreceipt.notna().sum() == 2
"""
    completed = subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr


def test_local_full_cohort_reload_matches_original_formula_without_refitting():
    """Optional private-reference check; identifiers never enter failure output."""
    import statsmodels.api as sm
    from opg_core.features import historical_model

    cohort = ROOT / "output" / "phase3" / "cohort_person.csv"
    coefficients = ROOT / "output" / "phase5" / "apparent_coefficients.csv"
    if not cohort.exists() or not coefficients.exists():
        pytest.skip("Private local scientific reference inputs are unavailable.")
    frame = pd.read_csv(cohort, dtype=str)
    frame = frame.loc[frame.in_final_cohort == "1"].copy()
    original = historical_model.prepare(frame)
    stats = historical_model.learning_stats(original)
    original_design = historical_model.model_matrix(historical_model.apply_stats(original, stats))
    design = sm.add_constant(original_design.to_numpy(dtype=float), has_constant="add")
    saved = pd.read_csv(coefficients).set_index("term")
    parameters = saved.loc[["intercept", *FEATURE_ORDER], "coefficient"].to_numpy()
    reference = sm.Logit(original.y_n.to_numpy(), design).predict(parameters, design)
    frame["screen_status"] = "PASS"
    frame["receipt_status"] = frame["outcome_status"]
    frame["model_eligible_for_scoring"] = True
    model = load_model()
    assert dict(model.training_stats) == stats
    actual = score_frame(frame, model).predicted_nonreceipt.to_numpy(dtype=float)
    assert len(actual) == 1013
    assert np.isfinite(actual).all()
    maximum_difference = float(np.max(np.abs(actual - reference)))
    assert maximum_difference <= 1e-12, f"Reference prediction error {maximum_difference:g}; private rows suppressed."


def test_public_evaluation_matches_saved_heldout_metrics_intervals_and_calibration():
    evaluation = load_evaluation()
    assert evaluation["schema_version"] == "opg-heldout-evaluation-v1"
    assert evaluation["model_version"] == load_model().manifest["model_version"]
    assert evaluation["cohort"] == {"people": 1013, "events": 67, "households": 827}
    primary = ROOT / "output" / "runs" / "primary"
    if not all((primary / name).exists() for name in ["metrics.csv", "bootstrap_intervals.csv", "calibration_bins.csv"]):
        pytest.skip("Local held-out aggregate reference outputs are unavailable.")
    metrics = pd.read_csv(primary / "metrics.csv").set_index("model")
    assert set(evaluation["metrics"]) == set(metrics.index)
    for model_name, row in metrics.iterrows():
        actual = evaluation["metrics"][model_name]
        assert set(actual) == set(row.index)
        for metric, expected in row.items():
            if pd.isna(expected):
                assert actual[metric] is None
            else:
                assert actual[metric] == pytest.approx(expected, abs=1e-12, rel=0)
    intervals = pd.read_csv(primary / "bootstrap_intervals.csv")
    actual_intervals = pd.DataFrame(evaluation["bootstrap"]["intervals"], columns=intervals.columns)
    pd.testing.assert_frame_equal(actual_intervals, intervals, check_dtype=False, atol=1e-12, rtol=0)
    assert evaluation["bootstrap"]["draws"] == 1000
    assert evaluation["bootstrap"]["seed"] == 201415
    method = evaluation["bootstrap"]["method"].lower()
    assert "household" in method and "fixed" in method
    expected_bins = pd.read_csv(primary / "calibration_bins.csv")
    actual_bins = pd.DataFrame(evaluation["calibration_bins"], columns=expected_bins.columns)
    pd.testing.assert_frame_equal(actual_bins, expected_bins, check_dtype=False, atol=1e-12, rtol=0)
    for source in evaluation["provenance"]["sources"]:
        relative = Path(source["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        assert source["sha256"] == hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def test_public_model_artifacts_contain_no_person_or_household_records():
    forbidden = {
        "record_id", "household_id", "personno", "spouse_no", "uqno", "psu",
        "inspection", "y", "person_weight", "private_income", "combined_private_income",
    }

    def check_keys(item):
        if isinstance(item, dict):
            assert not forbidden & set(item), "Public metadata contains respondent-level fields."
            for value in item.values():
                check_keys(value)
        elif isinstance(item, list):
            for value in item:
                check_keys(value)

    content = []
    for name in ("logistic_model.json", "manifest.json", "evaluation.json"):
        data = (ROOT / "models" / name).read_text()
        check_keys(json.loads(data))
        content.append(data)
    cohort = ROOT / "output" / "phase3" / "cohort_person.csv"
    if cohort.exists():
        household_ids = pd.read_csv(cohort, usecols=["uqno"], dtype=str).uqno.dropna().unique()
        rendered = "\n".join(content)
        assert not any(identifier in rendered for identifier in household_ids), "Private household identifiers appeared in public metadata."


def test_explicit_freeze_reuses_compatible_artifacts_and_refuses_changed_signature_before_fitting(artifact_copy, monkeypatch):
    from tools import freeze_model as builder

    def forbidden_fit(*args, **kwargs):
        raise AssertionError("Artifact reuse or stale-artifact refusal attempted to fit.")

    monkeypatch.setattr(builder.research_model, "fit_logit", forbidden_fit)
    before = {name: (artifact_copy / name).read_bytes() for name in builder.OUTPUT_NAMES}
    reused = builder.freeze_model(artifact_copy)
    assert reused["status"] == "reused"
    assert before == {name: (artifact_copy / name).read_bytes() for name in builder.OUTPUT_NAMES}

    manifest_path = artifact_copy / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["source_signature"]["training_script_sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest))
    changed = {name: (artifact_copy / name).read_bytes() for name in builder.OUTPUT_NAMES}
    with pytest.raises(ValueError, match="explicitly use --force"):
        builder.freeze_model(artifact_copy, force=False)
    assert changed == {name: (artifact_copy / name).read_bytes() for name in builder.OUTPUT_NAMES}
    assert set(path.name for path in artifact_copy.iterdir()) == set(builder.OUTPUT_NAMES)


def test_manifest_distinguishes_baseline_revision_from_current_build_source_provenance():
    from tools import freeze_model as builder

    manifest = load_model().manifest
    assert manifest["working_tree_dirty"] is True
    baseline = manifest["baseline_commit"]
    assert len(baseline) == 40 and all(character in "0123456789abcdef" for character in baseline)
    revision = subprocess.run(
        ["git", "cat-file", "-t", baseline], cwd=ROOT, capture_output=True, text=True,
        check=True, timeout=10,
    )
    assert revision.stdout.strip() == "commit"
    assert "Baseline repository revision" in manifest["commit_scope"]
    signature = manifest["source_signature"]
    assert signature == builder.source_signature()
    training_hash = hashlib.sha256((ROOT / "tools" / "freeze_model.py").read_bytes()).hexdigest()
    assert manifest["training_script_sha256"] == signature["training_script_sha256"] == training_hash
    assert baseline != training_hash
    for field in ("source_script_sha256", "adapter_script_sha256", "evaluation_source_sha256"):
        for relative, expected in signature[field].items():
            assert expected == hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    assert manifest["source_script_sha256"] == signature["source_script_sha256"]
    assert manifest["training_input_hashes"] == signature["training_input_hashes"]
    assert manifest["software"] == signature["software"]
    frozen_input = signature["training_input_hashes"]["output/phase3/cohort_person.csv"]
    assert frozen_input["crlf_sha256"] == builder.research_model.FROZEN_HASH
    evaluation_sources = {source["path"]: source["sha256"] for source in load_evaluation()["provenance"]["sources"]}
    assert evaluation_sources == signature["evaluation_source_sha256"]


@pytest.mark.parametrize("group,path", [
    ("source_script_sha256", "analysis/phase3_build_cohort.py"),
    ("source_script_sha256", "analysis/phase4_rq1.py"),
    ("source_script_sha256", "analysis/phase5_model.py"),
    ("adapter_script_sha256", "opg_core/features.py"),
    ("adapter_script_sha256", "opg_core/schema.py"),
    ("adapter_script_sha256", "opg_core/screening.py"),
])
def test_stale_scientific_or_preprocessing_provenance_rejected_before_scoring(artifact_copy, monkeypatch, group, path):
    import copy
    from dataclasses import replace
    from opg_core import inference

    loaded = load_model()
    stale_manifest = copy.deepcopy(loaded.manifest)
    stale_manifest["source_signature"][group][path] = "0" * 64
    (artifact_copy / "manifest.json").write_text(json.dumps(stale_manifest))
    with pytest.raises(ValueError, match="preprocessing provenance"):
        load_model(artifact_copy)

    def forbidden_preparation(*args, **kwargs):
        raise AssertionError("Stale transforms were used before the provenance guard.")

    monkeypatch.setattr(inference, "prepare_features", forbidden_preparation)
    stale_cached_model = replace(loaded, manifest=stale_manifest)
    with pytest.raises(ValueError, match="preprocessing provenance"):
        score_frame(scoring_rows(), stale_cached_model)
    with pytest.raises(ValueError, match="preprocessing provenance"):
        load_evaluation(artifact_copy, stale_cached_model)


def test_missing_or_unverifiable_live_source_provenance_fails_closed(artifact_copy, monkeypatch, tmp_path):
    from opg_core import inference

    manifest_path = artifact_copy / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["source_signature"]["adapter_script_sha256"].pop("opg_core/features.py")
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="source provenance"):
        load_model(artifact_copy)
    monkeypatch.setattr(inference, "_SOURCE_ROOT", tmp_path / "unavailable-source")
    with pytest.raises(ValueError, match="source cannot be verified"):
        load_model()


def test_runtime_guard_update_retains_fitted_model_and_training_provenance():
    manifest = load_model().manifest
    update = manifest["runtime_provenance_updates"][-1]
    assert update["note"] == "hash guard added, estimator not refitted"
    assert update["estimator_refitted"] is False
    assert update["path"] == "opg_core/inference.py"
    assert update["previous_sha256"] != update["current_sha256"]
    assert update["current_sha256"] == manifest["source_signature"]["adapter_script_sha256"][update["path"]]
    assert manifest["artifact_sha256"] == hashlib.sha256((ROOT / "models/logistic_model.json").read_bytes()).hexdigest()
    assert manifest["training_script_sha256"] == manifest["source_signature"]["training_script_sha256"]
