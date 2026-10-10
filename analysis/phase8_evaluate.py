"""Phase 8: expected-versus-actual checks for the rule engine.

Each case states the decision the screen should return. The log records
that expectation beside the program output. The script exits with an
error if any case disagrees.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase3_build_cohort as cohort  # noqa: E402
import phase5_model as model  # noqa: E402

OUT = ROOT / "output" / "phase8"
RUN = ROOT / "output" / "runs" / "primary"


def base_person(**overrides):
    person = {
        "uqno": "SYNTH",
        "personno": "1",
        "marital": "4",
        "partner_in_hh": "8",
        "spouse_no": "88",
        "survey_year": 2014,
        "survey_month": 11,
        "private": Decimal(0),
        "opg": Decimal(0),
        "schedule": "supported_zero",
        "disability": "2",
        "warvet": "2",
        "any_grant": "2",
        "oldage": "8",
        "child": "2",
        "caredep": "2",
        "foster": "2",
        "inaid": "2",
    }
    person.update(overrides)
    return person


def codes(result: dict) -> set[str]:
    return set(result["reason_codes"].split("|")) if result["reason_codes"] else set()


CASES = [
    {
        "case": "income_equal_to_2014_ceiling",
        "expects": "A widowed adult interviewed in November 2014 with private income of R61,800 passes and is a non-recipient.",
        "person": base_person(private=Decimal(61800)),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD"],
    },
    {
        "case": "income_one_cent_over_2014_ceiling",
        "expects": "Private income of R61,800.01 fails the income rule.",
        "person": base_person(private=Decimal("61800.01")),
        "link": "not_needed",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_INCOME_ABOVE_THRESHOLD"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "income_one_cent_under_2014_ceiling",
        "expects": "Private income of R61,799.99 passes.",
        "person": base_person(private=Decimal("61799.99")),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD"],
    },
    {
        "case": "income_equal_to_2015_ceiling",
        "expects": "The April 2015 ceiling of R64,680 passes for an interview in April 2015.",
        "person": base_person(private=Decimal(64680), survey_year=2015, survey_month=4),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD"],
    },
    {
        "case": "income_one_cent_over_2015_ceiling",
        "expects": "Private income of R64,680.01 fails for an April 2015 interview.",
        "person": base_person(private=Decimal("64680.01"), survey_year=2015, survey_month=4),
        "link": "not_needed",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_INCOME_ABOVE_THRESHOLD"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "couple_income_equal_to_ceiling",
        "expects": "A married couple whose private incomes sum to R123,600 passes. The single ceiling is not used.",
        "person": base_person(marital="1", partner_in_hh="1", spouse_no="2", private=Decimal(60000)),
        "spouse": base_person(personno="2", private=Decimal(63600), spouse_no="1"),
        "link": "reciprocal",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD", "UNRES_SPOUSE_NONRESIDENT"],
    },
    {
        "case": "couple_income_one_cent_over_ceiling",
        "expects": "A couple sum of R123,600.01 fails.",
        "person": base_person(marital="1", partner_in_hh="1", spouse_no="2", private=Decimal("60000.01")),
        "spouse": base_person(personno="2", private=Decimal(63600), spouse_no="1"),
        "link": "reciprocal",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_INCOME_ABOVE_THRESHOLD"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "married_spouse_not_in_household",
        "expects": "A married adult whose spouse is outside the household is unresolved even when the applicant's own income is high.",
        "person": base_person(marital="1", partner_in_hh="2", spouse_no="88", private=Decimal(200000)),
        "link": "nonresident",
        "status": "UNRESOLVED",
        "y": "",
        "present": ["UNRES_SPOUSE_NONRESIDENT"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD", "PASS_PRIMARY"],
    },
    {
        "case": "married_spouse_income_missing",
        "expects": "A linked spouse with no usable income leaves the couple screen unresolved.",
        "person": base_person(marital="1", partner_in_hh="1", spouse_no="2", private=Decimal(0)),
        "spouse": base_person(personno="2", private=None, spouse_no="1"),
        "link": "reciprocal",
        "status": "UNRESOLVED",
        "y": "",
        "present": ["UNRES_INCOME_SPOUSE"],
        "absent": ["PASS_PRIMARY", "FAIL_INCOME_ABOVE_THRESHOLD"],
    },
    {
        "case": "self_spouse_pointer",
        "expects": "A spouse pointer that names the applicant is an unresolved relationship.",
        "person": base_person(marital="1", partner_in_hh="1", spouse_no="1"),
        "link": "self",
        "status": "UNRESOLVED",
        "y": "",
        "present": ["UNRES_SPOUSE_RELATIONSHIP"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "own_disability_grant",
        "expects": "An own disability grant fails the screen even though income would pass.",
        "person": base_person(disability="1", private=Decimal(0)),
        "link": "not_needed",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_DISABILITY_GRANT"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "disability_grant_and_missing_spouse",
        "expects": "A known disability-grant exclusion wins over an unresolved spouse, and both reasons are kept.",
        "person": base_person(marital="1", partner_in_hh="2", disability="1"),
        "link": "nonresident",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_DISABILITY_GRANT", "UNRES_SPOUSE_NONRESIDENT"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "war_veterans_grant",
        "expects": "An own war-veterans grant fails the primary screen.",
        "person": base_person(warvet="1"),
        "link": "not_needed",
        "status": "FAIL",
        "y": "",
        "present": ["FAIL_WAR_VETERAN_GRANT"],
        "absent": ["PASS_PRIMARY"],
    },
    {
        "case": "caregiver_child_grant_does_not_set_receipt",
        "expects": "A caregiver child grant does not exclude the adult and does not count as OPG receipt.",
        "person": base_person(any_grant="1", oldage="2", child="1", private=Decimal(0)),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["FLAG_CAREGIVER_CHILD_GRANT", "PASS_PRIMARY"],
        "absent": ["FAIL_DISABILITY_GRANT"],
    },
    {
        "case": "grant_in_aid_with_opg_receipt",
        "expects": "Grant-in-aid does not exclude. Consistent OPG receipt stays Y=0.",
        "person": base_person(any_grant="1", oldage="1", inaid="1", opg=Decimal(16200), private=Decimal(0)),
        "link": "not_needed",
        "status": "PASS",
        "y": "0",
        "present": ["FLAG_GRANT_IN_AID", "PASS_PRIMARY"],
        "absent": ["FLAG_RECEIPT_PERIOD_DISAGREE"],
    },
    {
        "case": "contradictory_grant_response",
        "expects": "An unspecified OPG item after a yes to any grant leaves eligibility passed and the outcome unresolved.",
        "person": base_person(any_grant="1", oldage="9", private=Decimal(0)),
        "link": "not_needed",
        "status": "PASS",
        "y": "",
        "present": ["PASS_PRIMARY", "UNRES_GRANT_RESPONSE"],
        "absent": ["FAIL_INCOME_ABOVE_THRESHOLD"],
        "final_cohort": 0,
    },
    {
        "case": "consistent_no_social_grant",
        "expects": "No to any social grant, with the OPG item skipped, is reported non-receipt.",
        "person": base_person(any_grant="2", oldage="8"),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["UNRES_GRANT_RESPONSE"],
    },
    {
        "case": "consistent_opg_receipt",
        "expects": "Yes to any grant and yes to OPG is Y=0.",
        "person": base_person(any_grant="1", oldage="1", opg=Decimal(16200)),
        "link": "not_needed",
        "status": "PASS",
        "y": "0",
        "present": ["PASS_PRIMARY"],
        "absent": ["FLAG_RECEIPT_PERIOD_DISAGREE", "UNRES_GRANT_RESPONSE"],
    },
    {
        "case": "receipt_period_disagreement_keeps_current_label",
        "expects": "Current non-receipt stays Y=1 when preceding-year OPG income is positive. The disagreement is only a flag.",
        "person": base_person(any_grant="2", oldage="8", opg=Decimal(1000)),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["FLAG_RECEIPT_PERIOD_DISAGREE", "PASS_PRIMARY"],
        "absent": [],
    },
    {
        "case": "absent_income_not_treated_as_zero",
        "expects": "An income schedule that is missing, and not a supported zero, is unresolved.",
        "person": base_person(private=None, opg=None, schedule="absent"),
        "link": "not_needed",
        "status": "UNRESOLVED",
        "y": "",
        "present": ["UNRES_INCOME_ABSENT"],
        "absent": ["PASS_PRIMARY", "FAIL_INCOME_ABOVE_THRESHOLD"],
    },
    {
        "case": "supported_zero_income",
        "expects": "A completed no-to-all income schedule is a zero and can pass.",
        "person": base_person(private=Decimal(0), opg=Decimal(0), schedule="supported_zero"),
        "link": "not_needed",
        "status": "PASS",
        "y": "1",
        "present": ["PASS_PRIMARY"],
        "absent": ["UNRES_INCOME_ABSENT"],
    },
    {
        "case": "living_together_not_assigned_a_ceiling",
        "expects": "Living together stays unresolved on the primary screen.",
        "person": base_person(marital="2", partner_in_hh="1", private=Decimal(0)),
        "link": "ambiguous",
        "status": "UNRESOLVED",
        "y": "",
        "present": ["UNRES_PARTNERSHIP_AMBIGUOUS"],
        "absent": ["PASS_PRIMARY", "FAIL_INCOME_ABOVE_THRESHOLD"],
    },
]


def evaluate_case(case: dict) -> dict:
    result = cohort.screen(case["person"], case.get("spouse"), case["link"])
    actual_codes = codes(result)
    missing = [code for code in case["present"] if code not in actual_codes]
    unexpected = [code for code in case["absent"] if code in actual_codes]
    status_ok = result["eligibility_status"] == case["status"] and result["y"] == case["y"]
    final_ok = True
    if "final_cohort" in case:
        final_ok = result["in_final_cohort"] == case["final_cohort"]
    passed = status_ok and final_ok and not missing and not unexpected
    return {
        "case": case["case"],
        "expects": case["expects"],
        "expected_status": case["status"],
        "actual_status": result["eligibility_status"],
        "expected_y": case["y"],
        "actual_y": result["y"],
        "expected_reasons": "|".join(case["present"]),
        "actual_reasons": result["reason_codes"],
        "passed": passed,
    }


def leakage_case() -> dict:
    poisoned = set(model.SLOPE_NAMES) | {"y", "opg_income_annual"}
    rejected = bool(poisoned & model.FORBIDDEN)
    legitimate = model.model_matrix(pd.DataFrame({
        "age_per_10": [0.0],
        "sex_code": ["1"],
        "school_code": ["0"],
        "settlement_code": ["1"],
        "welfare_code": ["0"],
    }))
    clean = list(legitimate.columns) == model.SLOPE_NAMES and not (set(legitimate.columns) & model.FORBIDDEN)
    return {
        "case": "forbidden_predictor_is_rejected",
        "expects": "A model matrix that includes the outcome or OPG income is rejected. The real matrix contains only the six slopes.",
        "expected_status": "REJECTED",
        "actual_status": "REJECTED" if rejected and clean else "ACCEPTED",
        "expected_y": "",
        "actual_y": "",
        "expected_reasons": "y|opg_income_annual",
        "actual_reasons": "|".join(legitimate.columns),
        "passed": rejected and clean,
    }


def trace_case() -> dict:
    cohort_rows = pd.read_csv(RUN / "cohort_person.csv", dtype=str)
    predictions = pd.read_csv(RUN / "oof_predictions.csv", dtype=str)
    record = json.loads((RUN / "run_record.json").read_text(encoding="utf-8"))
    example = record["inspection"]
    row = cohort_rows[
        (cohort_rows["uqno"] == example["uqno"]) & (cohort_rows["personno"] == example["personno"])
    ]
    prediction = predictions[
        (predictions["uqno"] == example["uqno"]) & (predictions["personno"] == example["personno"])
    ]
    flow = pd.read_csv(RUN / "cohort_flow.csv")
    counts = dict(zip(flow["step"], flow["people"]))
    traced = (
        len(row) == 1
        and len(prediction) == 1
        and row.iloc[0]["eligibility_status"] == example["eligibility_status"]
        and row.iloc[0]["reason_codes"] == example["reason_codes"]
        and row.iloc[0]["y"] == example["y"]
        and prediction.iloc[0]["fold"] == example["fold"]
        and counts["Final analysis cohort"] == 1013
        and counts["Non-recipients"] == 67
        and not cohort_rows.duplicated(["uqno", "personno"]).any()
    )
    return {
        "case": "run_folder_person_and_flow_trace",
        "expects": "The example person in the run record matches the cohort and prediction files, and the flow counts are 1,013 and 67.",
        "expected_status": "MATCH",
        "actual_status": "MATCH" if traced else "DIFFER",
        "expected_y": example["y"],
        "actual_y": row.iloc[0]["y"] if len(row) else "",
        "expected_reasons": example["reason_codes"],
        "actual_reasons": row.iloc[0]["reason_codes"] if len(row) else "",
        "passed": traced,
    }


def schedule_cases() -> list[dict]:
    zero = cohort.classify_schedule("1", [])
    absent = cohort.classify_schedule("8", [])
    rows = []
    for name, result, expect_private in (
        ("no_to_all_is_a_supported_zero", zero, Decimal(0)),
        ("source_reported_without_a_row_is_unresolved", absent, None),
    ):
        passed = result["private"] == expect_private
        rows.append({
            "case": name,
            "expects": "The income schedule follows the Phase 2 zero rule.",
            "expected_status": "supported_zero" if expect_private == 0 else "absent",
            "actual_status": result["schedule"],
            "expected_y": "",
            "actual_y": "",
            "expected_reasons": "",
            "actual_reasons": "" if result["private"] is None else str(result["private"]),
            "passed": passed,
        })
    return rows


def main() -> None:
    rows = [evaluate_case(case) for case in CASES]
    rows.append(leakage_case())
    rows.extend(schedule_cases())
    rows.append(trace_case())
    log = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    log.to_csv(OUT / "evaluation_log.csv", index=False)
    failed = log.loc[~log["passed"], "case"].tolist()
    print(f"{int(log['passed'].sum())} of {len(log)} checks passed")
    if failed:
        print("failed:", ", ".join(failed))
        raise SystemExit(1)
    print("evaluation log written")


if __name__ == "__main__":
    main()
