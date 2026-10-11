"""Exercise the exact upload-to-export path used by the Streamlit interface."""
import io
import json
from pathlib import Path

import pandas as pd

from opg_core.schema import from_research_people, synthetic_template
from opg_core.screening import historical
from opg_core.workflow import process_upload


def test_fatal_upload_never_returns_scores_or_reports():
    run = process_upload(b"bad,columns\n1,2")
    assert run.validation.errors and run.results is None
    assert not run.model_manifest and not run.reports


def test_synthetic_upload_repeats_with_identical_results_and_safe_exports():
    data = synthetic_template().to_csv(index=False).encode()
    first = process_upload(data); second = process_upload(data)
    assert not first.validation.errors
    assert first.summary["uploaded_rows"] == 6
    assert first.summary["resolved_pass_denominator"] == 2
    assert first.summary["reported_nonrecipients"] == 1
    assert first.summary["scored_rows"] == 2
    assert first.reports["results.csv"] == second.reports["results.csv"]
    assert first.reports["summary.json"] == second.reports["summary.json"]
    exported = pd.read_csv(io.BytesIO(first.reports["results.csv"]))
    assert not set(("record_id", "household_id", "personno", "spouse_no", "private_income")) & set(exported)
    assert b"SYN-" not in first.reports["results.csv"]
    manifest = json.loads(first.reports["audit_manifest.json"])
    assert manifest["accepted_rows"] == 6


def test_all_reference_records_match_cli_through_uploaded_csv_processing():
    import pytest
    root = Path(__file__).resolve().parents[1]
    expected_path = root / "output/phase3/cohort_person.csv"
    if not expected_path.exists() or not (historical.DATA / "LCS2015PERSONSFINAL.csv").exists():
        pytest.skip("Private reference datasets unavailable.")
    persons, household, income = historical.load_inputs()
    people = historical.build_people(persons, income)
    welfare = dict(zip(household.UQNO, household.Q531WELFARE))
    content = from_research_people(people, welfare).to_csv(index=False).encode()
    run = process_upload(content)
    assert not run.validation.errors, "Reference input validation failed; private values suppressed."
    actual = run.results.set_index("record_id")
    expected = pd.read_csv(expected_path, dtype=str, keep_default_na=False)
    expected["record_id"] = expected.uqno + ":" + expected.personno
    expected = expected.set_index("record_id")
    assert len(actual) == 15388 and set(actual.index) == set(expected.index)
    actual = actual.loc[expected.index]
    mismatches = {}
    for current, reference in (("screen_status", "eligibility_status"), ("receipt_status", "outcome_status"),
                               ("reason_codes", "reason_codes"), ("y", "y")):
        mismatches[current] = int(actual[current].astype(str).ne(expected[reference]).sum())
    assert all(value == 0 for value in mismatches.values()), str(mismatches)
    assert run.summary["resolved_pass_denominator"] == 1013
    assert run.summary["reported_nonrecipients"] == 67
    assert run.summary["scored_rows"] == 1013
    exported = pd.read_csv(io.BytesIO(run.reports["results.csv"]))
    assert len(exported) == 15388
    assert b"uqno" not in run.reports["results.csv"]
    assert b"personno" not in run.reports["results.csv"]
    assert b"spouse_no" not in run.reports["results.csv"]
