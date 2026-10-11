"""Historical rule edge cases with entirely synthetic upload records."""

from decimal import Decimal
import sys
from pathlib import Path

import pandas as pd
import pytest

from opg_core.schema import synthetic_template, validate_frame
from opg_core.screening import screen_frame

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import phase8_evaluate as existing  # noqa: E402


def screen_one(**changes):
    frame = synthetic_template().iloc[:1].copy()
    for field, value in changes.items():
        frame[field] = value
    return screen_frame(frame).iloc[0]


@pytest.mark.parametrize("case", existing.CASES, ids=lambda case: case["case"])
def test_existing_prespecified_screen_cases(case):
    assert existing.evaluate_case(case)["passed"]


def test_template_demonstrates_all_five_categories_plus_out_of_frame():
    frame = screen_frame(synthetic_template())
    assert set(frame.classification) == {
        "APPARENTLY_ELIGIBLE_REPORTED_RECEIPT",
        "APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT", "FAILED_OBSERVABLE_RULE",
        "ELIGIBILITY_UNRESOLVED", "RECEIPT_UNRESOLVED", "OUT_OF_STUDY_FRAME",
    }
    assert frame.model_eligible_for_scoring.tolist() == [True, True, False, False, False, False]
    assert not {"household_id", "personno", "spouse_no", "uqno", "psu"} & set(frame.columns)


def test_age_60_boundary_is_applied_before_income_screen():
    assert screen_one(age=60).screen_status == "PASS"
    under = screen_one(age=59, disability="1")
    assert under.screen_status == "OUT_OF_FRAME"
    assert under.reason_codes == "OUT_AGE_BELOW_60"
    assert under.receipt_status == "NOT_ASSESSED"


@pytest.mark.parametrize("year,month,ceiling", [(2014, 11, "61800"), (2015, 3, "61800"), (2015, 4, "64680")])
def test_month_specific_income_equality_and_one_cent_above(year, month, ceiling):
    passed = screen_one(survey_year=year, survey_month=month, private_income=ceiling, income_schedule="summed")
    failed = screen_one(survey_year=year, survey_month=month, private_income=str(Decimal(ceiling) + Decimal("0.01")), income_schedule="summed")
    assert passed.screen_status == "PASS"
    assert passed.threshold_single == f"{Decimal(ceiling):.2f}"
    assert failed.screen_status == "FAIL"
    assert "FAIL_INCOME_ABOVE_THRESHOLD" in failed.reason_codes


@pytest.mark.parametrize("marital", ["2", "5", "9"])
def test_cohabiting_separated_and_unknown_partnership_are_unresolved(marital):
    result = screen_one(marital=marital)
    assert result.screen_status == "UNRESOLVED"
    assert "UNRES_PARTNERSHIP_AMBIGUOUS" in result.reason_codes


def couple():
    first = synthetic_template().iloc[:1].copy()
    second = first.copy()
    first["marital"] = "1"
    first["partner_in_hh"] = "1"
    first["spouse_no"] = "2"
    first["private_income"] = "60000"
    first["income_schedule"] = "summed"
    second["record_id"] = "SYN-spouse"
    second["personno"] = "2"
    second["marital"] = "1"
    second["partner_in_hh"] = "1"
    second["spouse_no"] = "1"
    second["private_income"] = "63600"
    second["income_schedule"] = "summed"
    return pd.concat([first, second], ignore_index=True)


def test_resident_spouse_is_actually_linked_and_income_combined():
    result = screen_frame(couple())
    assert result.screen_status.tolist() == ["PASS", "PASS"]
    assert result.link_status.tolist() == ["reciprocal", "reciprocal"]
    assert result.combined_private_income.tolist() == [Decimal("123600"), Decimal("123600")]


@pytest.mark.parametrize("pointer,expected_reason", [
    ("1", "UNRES_SPOUSE_RELATIONSHIP"), ("27", "UNRES_SPOUSE_NOT_IN_HOUSEHOLD"),
    ("99", "UNRES_SPOUSE_MISSING"), ("88", "UNRES_SPOUSE_MISSING"),
])
def test_spouse_pointer_failures_are_resolved_by_original_link_function(pointer, expected_reason):
    result = screen_one(marital="1", partner_in_hh="1", spouse_no=pointer)
    assert result.screen_status == "UNRESOLVED"
    assert expected_reason in result.reason_codes


def test_nonreciprocal_spouse_and_missing_spouse_income():
    frame = couple()
    frame.loc[1, "spouse_no"] = "99"
    assert "UNRES_SPOUSE_RELATIONSHIP" in screen_frame(frame).iloc[0].reason_codes
    frame.loc[1, "spouse_no"] = "1"
    frame.loc[1, "private_income"] = ""
    frame.loc[1, "opg_income"] = ""
    frame.loc[1, "income_schedule"] = "absent"
    assert "UNRES_INCOME_SPOUSE" in screen_frame(frame).iloc[0].reason_codes


def test_nonresident_spouse_does_not_apply_single_ceiling():
    result = screen_one(marital="1", partner_in_hh="2", private_income="200000", income_schedule="summed")
    assert result.screen_status == "UNRESOLVED"
    assert "UNRES_SPOUSE_NONRESIDENT" in result.reason_codes
    assert "FAIL_INCOME_ABOVE_THRESHOLD" not in result.reason_codes


def test_known_failure_takes_precedence_but_preserves_unresolved_reasons():
    result = screen_one(marital="1", partner_in_hh="2", disability="1")
    assert result.screen_status == "FAIL"
    assert result.classification == "FAILED_OBSERVABLE_RULE"
    assert "FAIL_DISABILITY_GRANT" in result.reason_codes
    assert "UNRES_SPOUSE_NONRESIDENT" in result.reason_codes


def test_missing_incompatible_grant_answers_do_not_pass():
    result = screen_one(disability="", warvet="")
    assert result.screen_status == "UNRESOLVED"
    assert "UNRES_INCOMPATIBLE_GRANT_UNSPECIFIED" in result.reason_codes


def test_contradictory_receipt_is_separate_from_rule_screen():
    result = screen_one(any_grant="2", oldage="1")
    assert result.screen_status == "PASS"
    assert result.receipt_status == "UNRESOLVED"
    assert result.classification == "RECEIPT_UNRESOLVED"
    assert result.y == ""
    assert not result.model_eligible_for_scoring


def test_duplicate_keys_block_screening_before_dictionary_build():
    frame = pd.concat([synthetic_template().iloc[:1]] * 2, ignore_index=True)
    assert validate_frame(frame).errors
    with pytest.raises(ValueError, match="Duplicate normalized"):
        screen_frame(frame)

