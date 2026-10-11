"""Local private-reference parity; no respondent data are written or committed."""

from pathlib import Path

import pandas as pd
import pytest

from opg_core.schema import from_research_people, validate_frame
from opg_core.screening import historical, screen_frame

ROOT = Path(__file__).resolve().parents[1]


def test_every_kzn_reference_screen_matches_frozen_cli_output():
    paths = [
        historical.DATA / "LCS2015PERSONSFINAL.csv",
        historical.DATA / "LCS2015HOUSEHOLD.csv",
        historical.DATA / "LCS2015PERSONINCOME.csv",
        ROOT / "output" / "phase3" / "cohort_person.csv",
    ]
    if not all(path.exists() for path in paths):
        pytest.skip("Private local reference inputs are unavailable; synthetic public tests remain runnable.")
    persons, household, income = historical.load_inputs()
    people = historical.build_people(persons, income)
    welfare = dict(zip(household.UQNO, household.Q531WELFARE))
    validation = validate_frame(from_research_people(people, welfare))
    assert not validation.errors, "Reference upload schema validation failed."
    actual = screen_frame(validation.frame).set_index("record_id")
    expected = pd.read_csv(paths[-1], dtype=str, keep_default_na=False)
    expected["record_id"] = expected.uqno + ":" + expected.personno
    expected = expected.set_index("record_id")
    assert len(actual) == len(expected) == 15388
    membership_matches = set(actual.index) == set(expected.index)
    assert membership_matches, "Reference membership differs (private identifiers suppressed)."
    actual = actual.loc[expected.index]
    for original, adapted in (
        ("eligibility_status", "screen_status"), ("outcome_status", "receipt_status"),
        ("reason_codes", "reason_codes"), ("y", "y"),
    ):
        mismatch = (actual[adapted].astype(str) != expected[original]).sum()
        assert mismatch == 0, f"{adapted}: {mismatch} reference mismatches (private rows suppressed)."
    assert int(actual.model_eligible_for_scoring.sum()) == 1013
    assert int((actual.receipt_status == "NON_RECIPIENT").sum()) == 67
    assert int((actual.receipt_status == "RECIPIENT").sum()) == 946
    assert int((actual.screen_status == "FAIL").sum()) == 117
    assert int((actual.screen_status == "UNRESOLVED").sum()) == 187
