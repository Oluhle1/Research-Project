"""Thin, parity-tested adapter to the existing historical screening rules."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from opg_core.schema import validate_frame

# Legacy analysis modules import each other by filename; preserve their code.
_ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
if str(_ANALYSIS) not in sys.path:
    sys.path.insert(0, str(_ANALYSIS))
import phase3_build_cohort as historical  # noqa: E402

RULE_VERSION = historical.RULE_VERSION
CLASSIFICATIONS = {
    ("PASS", "RECIPIENT"): "APPARENTLY_ELIGIBLE_REPORTED_RECEIPT",
    ("PASS", "NON_RECIPIENT"): "APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT",
    ("PASS", "UNRESOLVED"): "RECEIPT_UNRESOLVED",
}


def screen_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Screen supported rows without writing data or fitting a model.

    Revalidation protects direct callers against duplicate-key overwrites. The
    original resolve_link and screen functions remain the scientific authority.
    Household IDs and spouse pointers are used internally and omitted from output.
    """
    validation = validate_frame(frame)
    if validation.errors:
        raise ValueError("Invalid screening input: " + "; ".join(validation.errors))
    work = validation.frame
    people = {}
    for row in work.to_dict(orient="records"):
        person = {
            **row,
            "uqno": row["household_id"], "private": row["private_income"],
            "opg": row["opg_income"], "schedule": row["income_schedule"],
        }
        people[(person["uqno"], person["personno"])] = person
    rows = []
    for person in people.values():
        single, couple, period = historical.threshold_for(person["survey_year"], person["survey_month"])
        common = {
            "record_id": person["record_id"], "rule_version": RULE_VERSION,
            "age": person["age"], "sex": person["sex"],
            "schooling_raw": person["schooling_raw"], "settlement": person["settlement"],
            "welfare_distance": person["welfare_distance"], "person_weight": person["person_weight"],
            "threshold_period": period, "threshold_single": f"{single:.2f}", "threshold_couple": f"{couple:.2f}",
        }
        if person["age"] < 60:
            rows.append({
                **common, "screen_status": "OUT_OF_FRAME", "receipt_status": "NOT_ASSESSED",
                "reason_codes": "OUT_AGE_BELOW_60", "classification": "OUT_OF_STUDY_FRAME",
                "y": "", "model_eligible_for_scoring": False,
                "combined_private_income": None, "link_status": "",
            })
            continue
        link, spouse = historical.resolve_link(person, people)
        result = historical.screen(person, spouse, link)
        status = result["eligibility_status"]
        receipt = result["outcome_status"]
        if status == "FAIL":
            classification = "FAILED_OBSERVABLE_RULE"
        elif status == "UNRESOLVED":
            classification = "ELIGIBILITY_UNRESOLVED"
        else:
            classification = CLASSIFICATIONS[(status, receipt)]
        rows.append({
            **common, "screen_status": status, "receipt_status": receipt,
            "reason_codes": result["reason_codes"], "classification": classification,
            "y": result["y"], "model_eligible_for_scoring": bool(result["in_final_cohort"]),
            "combined_private_income": result["combined_private_income"], "link_status": link,
        })
    return pd.DataFrame(rows)
