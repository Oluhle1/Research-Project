"""Native Streamlit upload-to-export checks using invented data only."""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from streamlit.runtime.memory_media_file_storage import MemoryMediaFileStorage
from streamlit.testing.v1 import AppTest
from streamlit.testing.v1 import app_test as native_app_test

from opg_core import inference
from opg_core.reporting import SAFE_COLUMNS, safe_results
from opg_core.schema import MAX_BYTES, from_research_people, synthetic_template
from opg_core.screening import historical
from opg_core.workflow import process_upload

APP = Path(__file__).resolve().parents[1] / "app" / "Home.py"
HOME = "Home / Study context"
UPLOAD = "Upload & validate"
ELIGIBILITY = "Eligibility & receipt"
PREDICTION = "Prediction & model"
EXPORT = "Export & reproducibility"


def csv_bytes(frame: pd.DataFrame) -> bytes:
    return frame.to_csv(index=False, lineterminator="\n").encode("utf-8")


@pytest.fixture
def app(monkeypatch):
    # Retain the native storage so download URLs can be checked against the
    # bytes actually registered by Streamlit, not a replacement widget.
    stores = []

    def storage(endpoint):
        store = MemoryMediaFileStorage(endpoint)
        stores.append(store)
        return store

    monkeypatch.setattr(native_app_test, "MemoryMediaFileStorage", storage)
    at = AppTest.from_file(APP, default_timeout=20).run()
    assert not at.exception
    return at, stores


def upload(at: AppTest, content: bytes, name: str = "invented.csv") -> AppTest:
    at.file_uploader(key="research_upload").set_value((name, content, "text/csv")).run()
    assert not at.exception
    return at


def navigate(at: AppTest, section: str) -> AppTest:
    at.radio(key="section").set_value(section).run()
    assert not at.exception
    return at


def analyse(at: AppTest) -> AppTest:
    at.button(key="run_analysis").click().run()
    assert not at.exception
    assert "analysis_run" in at.session_state
    return at


def downloaded(at: AppTest, stores, name: str) -> bytes:
    url = at.download_button(key="download_" + name).proto.url
    file_id = url.rsplit("/", 1)[-1].split(".", 1)[0]
    return stores[-1].get_file(file_id).content


def test_native_upload_requires_explicit_run_and_survives_navigation(app, monkeypatch):
    at, _ = app
    assert at.button(key="run_analysis").disabled
    assert "analysis_run" not in at.session_state
    loads = []
    original_load = inference.load_model

    def counted_load(*args, **kwargs):
        loads.append(True)
        return original_load(*args, **kwargs)

    monkeypatch.setattr(inference, "load_model", counted_load)
    content = csv_bytes(synthetic_template())
    upload(at, content)
    navigate(at, UPLOAD)
    assert not at.button(key="run_analysis").disabled
    assert "analysis_run" not in at.session_state
    assert not loads
    assert at.file_uploader[0].value.getvalue() == content
    analyse(at)
    assert len(loads) == 1
    run = at.session_state["analysis_run"]
    assert run.summary["uploaded_rows"] == 6
    assert run.summary["resolved_pass_denominator"] == 2
    assert run.summary["reported_nonrecipients"] == 1
    assert len(run.summary["classification_counts"]) == 6
    assert_frame_equal(at.dataframe[-1].value, safe_results(run.results).head(20))
    navigate(at, ELIGIBILITY)
    assert_frame_equal(at.dataframe[-1].value, safe_results(run.results))
    cards = {item.label: item.value for item in at.metric}
    assert cards["Resolved-pass denominator"] == "2"
    assert cards["Unweighted non-receipt"] == "50.0%"
    assert cards["Person-weighted non-receipt"] == "50.0%"


def test_native_filters_and_registered_download_bytes_match_safe_reports(app):
    at, stores = app
    content = csv_bytes(synthetic_template())
    upload(at, content)
    analyse(at)
    navigate(at, ELIGIBILITY)
    at.multiselect(key="classification_filter").set_value([
        "APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT"]).run()
    assert not at.exception
    safe_filtered = at.session_state["filtered_results"]
    assert safe_filtered["research_id"].tolist() == ["R000001"]
    assert_frame_equal(at.dataframe[-1].value, safe_filtered)
    assert {item.label: item.value for item in at.metric}["Resolved-pass denominator"] == "2"
    navigate(at, EXPORT)
    reports = at.session_state["export_reports"]
    for name in ("results.csv", "filtered_results.csv", "summary.csv", "summary.json",
                 "audit_manifest.json", "report.zip"):
        assert downloaded(at, stores, name) == reports[name]
    full = pd.read_csv(io.BytesIO(downloaded(at, stores, "results.csv")))
    selected = pd.read_csv(io.BytesIO(downloaded(at, stores, "filtered_results.csv")))
    assert len(full) == 6
    assert selected["research_id"].tolist() == ["R000001"]
    assert set(full) <= {"research_id", *SAFE_COLUMNS}
    value = json.loads(downloaded(at, stores, "summary.json"))
    assert value["resolved_pass_denominator"] == 2
    manifest = json.loads(downloaded(at, stores, "audit_manifest.json"))
    assert manifest["filtered_rows"] == 1
    assert manifest["dataset_sha256"] == hashlib.sha256(content).hexdigest()
    for name, digest in manifest["output_sha256"].items():
        assert hashlib.sha256(reports[name]).hexdigest() == digest
    with zipfile.ZipFile(io.BytesIO(downloaded(at, stores, "report.zip"))) as archive:
        assert archive.read("filtered_results.csv") == reports["filtered_results.csv"]
        assert archive.read("audit_manifest.json") == reports["audit_manifest.json"]


def invalid_upload(case: str) -> bytes:
    frame = synthetic_template()
    if case == "wrong_extension":
        return csv_bytes(frame)
    if case == "empty":
        return b""
    if case == "malformed":
        return b'"unterminated'
    if case == "encoding":
        return b"\xff\xfeinvalid"
    if case == "large":
        return b"a" * (MAX_BYTES + 1)
    if case == "missing_column":
        frame = frame.drop(columns="age")
    elif case == "duplicate_id":
        frame.loc[1, "record_id"] = frame.loc[0, "record_id"]
    elif case == "wrong_type":
        frame["age"] = frame["age"].astype(object)
        frame.loc[0, "age"] = "sixty"
    elif case == "unknown_category":
        frame.loc[0, "sex"] = "PRIVATE_UNKNOWN_VALUE"
    elif case == "extra_column":
        frame["PRIVATE_UNKNOWN_HEADER"] = "PRIVATE_UNKNOWN_VALUE"
    else:
        raise AssertionError(case)
    return csv_bytes(frame)


@pytest.mark.parametrize("case", ["wrong_extension", "empty", "malformed", "encoding", "large", "missing_column",
                                   "duplicate_id", "wrong_type", "unknown_category", "extra_column"])
def test_invalid_replacement_clears_old_results_filters_and_exports(app, case):
    at, _ = app
    upload(at, csv_bytes(synthetic_template()))
    analyse(at)
    navigate(at, EXPORT)
    at.multiselect(key="screen_filter").set_value(["PASS"]).run()
    assert "export_reports" in at.session_state
    name = "PRIVATE_FILENAME.txt" if case == "wrong_extension" else "PRIVATE_FILENAME.csv"
    upload(at, invalid_upload(case), name)
    assert "analysis_run" not in at.session_state
    assert "export_reports" not in at.session_state
    assert "filtered_results" not in at.session_state
    assert "screen_filter" not in at.session_state
    assert at.button(key="run_analysis").disabled
    assert len(at.download_button) == 1  # The synthetic template remains.
    navigate(at, UPLOAD)
    assert at.error
    assert not at.dataframe
    text = "\n".join(item.value for kind in (at.error, at.warning, at.markdown, at.caption)
                     for item in kind)
    assert "PRIVATE_FILENAME" not in text
    assert "PRIVATE_UNKNOWN_VALUE" not in text
    assert "PRIVATE_UNKNOWN_HEADER" not in text


def test_removal_and_identical_reupload_clear_previous_analysis(app):
    at, _ = app
    content = csv_bytes(synthetic_template())
    upload(at, content)
    analyse(at)
    navigate(at, ELIGIBILITY)
    at.multiselect(key="reason_filter").set_value(["PASS_PRIMARY"]).run()
    upload(at, content)
    assert "analysis_run" not in at.session_state
    assert "reason_filter" not in at.session_state
    analyse(at)
    at.file_uploader[0].set_value(None).run()
    assert not at.exception
    for key in ("analysis_run", "input_validation", "source_bytes", "filtered_results"):
        assert key not in at.session_state
    assert at.button(key="run_analysis").disabled
    assert not at.multiselect


def test_repeat_analysis_is_deterministic_and_agrees_with_workflow(app):
    at, _ = app
    content = csv_bytes(synthetic_template())
    reference = process_upload(content)
    upload(at, content)
    analyse(at)
    first = at.session_state["analysis_run"]
    assert_frame_equal(first.results, reference.results)
    analyse(at)
    second = at.session_state["analysis_run"]
    assert_frame_equal(first.results, second.results)
    assert first.summary == second.summary
    for name in ("results.csv", "filtered_results.csv", "summary.csv", "summary.json",
                 "responsible_use.txt"):
        assert first.reports[name] == second.reports[name] == reference.reports[name]


def test_all_missing_categorical_predictors_remain_visible_but_unscored(app):
    at, _ = app
    frame = synthetic_template()
    for name in ("sex", "schooling_raw", "settlement", "welfare_distance"):
        frame[name] = ""
    upload(at, csv_bytes(frame))
    navigate(at, UPLOAD)
    counts = at.dataframe[0].value.set_index("field")["missing_rows"]
    assert all(counts[name] == 6 for name in ("sex", "schooling_raw", "settlement", "welfare_distance"))
    assert at.warning
    analyse(at)
    assert at.session_state["analysis_run"].summary["scored_rows"] == 0
    navigate(at, PREDICTION)
    assert {item.label: item.value for item in at.metric}["Scored records in current filter"] == "0"
    assert any("No records" in item.value for item in at.info)
    navigate(at, ELIGIBILITY)
    displayed = at.dataframe[-1].value
    assert len(displayed) == 6
    assert displayed["predicted_nonreceipt"].isna().all()
    assert displayed["score_context"].str.contains("Not scored").all()


def test_model_page_uses_fixed_aggregate_oof_evidence_and_safe_ids(app):
    at, _ = app
    frame = synthetic_template()
    frame["record_id"] = [f"PRIVATE-PERSON-{index}" for index in range(len(frame))]
    frame["household_id"] = [f"PRIVATE-HOUSEHOLD-{index}" for index in range(len(frame))]
    frame.loc[0, "private_income"] = "12345.67"
    frame.loc[0, "income_schedule"] = "summed"
    upload(at, csv_bytes(frame), "PRIVATE_SOURCE_FILENAME.csv")
    analyse(at)
    navigate(at, PREDICTION)
    evidence = inference.load_evaluation()
    expected = pd.DataFrame(evidence["metrics"]).rename(columns={
        "logistic_out_of_fold": "Frozen logistic OOF", "intercept_only_out_of_fold": "Intercept-only OOF"})
    assert_frame_equal(at.dataframe[1].value, expected)
    top = at.dataframe[0].value
    assert len(top) == 2
    assert set(top) <= {"research_id", *SAFE_COLUMNS}
    assert top["research_id"].str.match(r"R\d{6}").all()
    text = "\n".join(item.value for kind in (at.markdown, at.caption, at.info, at.warning)
                     for item in kind)
    assert "PRIVATE" not in text
    assert "12345.67" not in text
    assert "not held-out" in text
    assert "never recomputed" in text
    for table in at.dataframe:
        assert "PRIVATE" not in table.value.to_csv()
        assert "12345.67" not in table.value.to_csv()


def test_builtin_example_and_safe_model_failure(app, monkeypatch):
    at, _ = app
    at.button(key="load_example").click().run()
    assert not at.exception
    assert at.session_state["source_kind"] == "synthetic"
    assert any("invented records" in item.value for item in at.caption)
    assert not at.button(key="run_analysis").disabled
    analyse(at)
    assert at.session_state["analysis_run"].summary["uploaded_rows"] == 6

    def failed_model(*args, **kwargs):
        raise RuntimeError("PRIVATE_DATA_VALUE must never reach the UI")

    monkeypatch.setattr(inference, "load_model", failed_model)
    at.button(key="run_analysis").click().run()
    assert not at.exception
    assert "analysis_run" not in at.session_state
    assert at.error
    assert all("PRIVATE_DATA_VALUE" not in item.value for item in at.error)


def test_native_private_reference_upload_matches_every_frozen_cli_record(app):
    root = APP.parents[1]
    expected_path = root / "output" / "phase3" / "cohort_person.csv"
    required = [expected_path, *(historical.DATA / name for name in
        ("LCS2015PERSONSFINAL.csv", "LCS2015HOUSEHOLD.csv", "LCS2015PERSONINCOME.csv"))]
    if not all(path.exists() for path in required):
        pytest.skip("Private local reference inputs unavailable; synthetic UI checks remain runnable.")
    persons, household, income = historical.load_inputs()
    people = historical.build_people(persons, income)
    welfare = dict(zip(household.UQNO, household.Q531WELFARE))
    content = csv_bytes(from_research_people(people, welfare))
    at, _ = app
    upload(at, content, "local_reference.csv")
    analyse(at)
    run = at.session_state["analysis_run"]
    actual = run.results.set_index("record_id")
    expected = pd.read_csv(expected_path, dtype=str, keep_default_na=False)
    expected["record_id"] = expected.uqno + ":" + expected.personno
    expected = expected.set_index("record_id")
    assert len(actual) == len(expected) == 15388
    assert set(actual.index) == set(expected.index), "Reference membership mismatch; private identifiers suppressed."
    actual = actual.loc[expected.index]
    mismatches = {current: int(actual[current].astype(str).ne(expected[reference]).sum())
        for current, reference in (("screen_status", "eligibility_status"),
            ("receipt_status", "outcome_status"), ("reason_codes", "reason_codes"), ("y", "y"))}
    assert not any(mismatches.values()), str(mismatches)
    assert run.summary["resolved_pass_denominator"] == 1013
    assert run.summary["reported_nonrecipients"] == 67
    assert run.summary["scored_rows"] == 1013
    navigate(at, ELIGIBILITY)
    assert_frame_equal(at.dataframe[-1].value, safe_results(run.results))
