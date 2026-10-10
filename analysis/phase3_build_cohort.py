"""Build and freeze the primary OPG screening cohort.

Applies the Phase 1 rules and the Phase 3 threshold decisions to
KwaZulu-Natal respondents. It does not fit a model and it does not
estimate a weighted non-receipt rate.

Rule version: opg-kzn-primary-v1
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Dataset" / "LCS2015"
OUT = ROOT / "output" / "phase3"
RULE_VERSION = "opg-kzn-primary-v1"

# Social-assistance COICOP codes excluded from the private-income proxy.
SOCIAL_ASSISTANCE = {
    "50331000",
    "50332000",
    "50332100",
    "50333100",
    "50333200",
    "50333300",
    "50333400",
    "50333500",
}
OPG_INCOME_CODE = "50331000"

# Annexure A: D = 1.6A - 0.4B, and no grant below R100 a month is payable.
# The single-person ceiling is the income at which D is still exactly R1,200 a year.
THRESHOLD_2014_SINGLE = Decimal("61800")  # A = R1,350 x 12, 1 April 2014 to 31 March 2015
THRESHOLD_2015_SINGLE = Decimal("64680")  # A = R1,410 x 12, 1 April 2015 onward
UNPARTNERED = {"3", "4", "6"}
AMBIGUOUS_MARITAL = {"2", "5", "9"}


def single_threshold(monthly_maximum: int) -> Decimal:
    annual = Decimal(monthly_maximum) * Decimal(12)
    return (Decimal("1.6") * annual - Decimal(1200)) / Decimal("0.4")


def parse_survey_month(value: str) -> tuple[int, int]:
    """Return (year, month) from SURVEYDATE.

    The release stores a 7-character month-year token. The last four
    digits are the year. The two digits before that are the month.
    """
    year = int(value[-4:])
    month = int(value[:-4][-2:])
    if month < 1 or month > 12:
        raise ValueError(f"Unreadable survey date: {value}")
    return year, month


def threshold_for(year: int, month: int) -> tuple[Decimal, Decimal, str]:
    if (year, month) < (2015, 4):
        single = THRESHOLD_2014_SINGLE
        period = "2014-04-01_to_2015-03-31"
    else:
        single = THRESHOLD_2015_SINGLE
        period = "2015-04-01_onward"
    return single, single * 2, period


def norm_person(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    if value in {"88", "99"}:
        return value
    try:
        return str(int(value))
    except ValueError:
        return value


def money(value: str) -> Decimal:
    return Decimal(value)


def classify_schedule(
    q11714: str,
    amounts: list[tuple[str, Decimal]],
    exclude: set[str] | None = None,
) -> dict:
    """Turn income rows into a private-income proxy and an OPG amount.

    The default exclusion is the social-assistance set used by the primary screen.
    """
    if exclude is None:
        exclude = SOCIAL_ASSISTANCE
    if q11714 == "9":
        return {"private": None, "opg": None, "schedule": "unspecified"}
    if q11714 == "1" and amounts:
        return {"private": None, "opg": None, "schedule": "contradiction"}
    if not amounts:
        if q11714 == "1":
            return {"private": Decimal(0), "opg": Decimal(0), "schedule": "supported_zero"}
        return {"private": None, "opg": None, "schedule": "absent"}
    opg = sum((amount for code, amount in amounts if code == OPG_INCOME_CODE), Decimal(0))
    private = sum((amount for code, amount in amounts if code not in exclude), Decimal(0))
    return {"private": private, "opg": opg, "schedule": "summed"}


def resolve_link(
    person: dict,
    people: dict,
    married_codes: set[str] | None = None,
    single_codes: set[str] | None = None,
) -> tuple[str, dict | None]:
    marital = person["marital"]
    married_codes = {"1"} if married_codes is None else married_codes
    single_codes = set(UNPARTNERED) if single_codes is None else single_codes
    if marital in single_codes:
        return "not_needed", None
    if marital not in married_codes:
        return "ambiguous", None
    partner = person["partner_in_hh"]
    if partner == "2":
        return "nonresident", None
    if partner == "9":
        return "unspecified", None
    if partner != "1":
        return "missing", None
    pointer = norm_person(person["spouse_no"])
    if pointer in {None, "88", "99"}:
        return "missing", None
    if pointer == norm_person(person["personno"]):
        return "self", None
    spouse = people.get((person["uqno"], pointer))
    if spouse is None:
        return "unmatched", None
    if norm_person(spouse["spouse_no"]) != norm_person(person["personno"]):
        return "not_reciprocal", spouse
    return "reciprocal", spouse


def screen(person: dict, spouse: dict | None, link_status: str, rules: dict | None = None) -> dict:
    """Return eligibility status, outcome, and reason codes for one person.

    `rules` is empty for the primary screen. Sensitivity calls pass an
    explicit alternative. Defaults reproduce opg-kzn-primary-v1.
    """
    rules = rules or {}
    reasons: list[str] = []
    if "single" in rules:
        single = rules["single"]
        couple = rules["couple"]
    else:
        single, couple, _period = threshold_for(person["survey_year"], person["survey_month"])
    fail_at_equal = bool(rules.get("fail_at_equal", False))
    single_codes = set(UNPARTNERED) | set(rules.get("also_single", ()))
    married_codes = {"1"} | set(rules.get("also_married", ()))

    def over_ceiling(amount: Decimal, ceiling: Decimal) -> bool:
        if fail_at_equal:
            return amount >= ceiling
        return amount > ceiling

    if rules.get("exclude_incompatible_grants", True):
        if person["disability"] == "1":
            reasons.append("FAIL_DISABILITY_GRANT")
        if person["warvet"] == "1":
            reasons.append("FAIL_WAR_VETERAN_GRANT")
    if person["disability"] == "9" or person["warvet"] == "9":
        reasons.append("UNRES_INCOMPATIBLE_GRANT_UNSPECIFIED")

    income_comparable = False
    combined = None
    if person["marital"] in single_codes and person["marital"] not in married_codes:
        if person["private"] is None:
            reasons.append("UNRES_INCOME_ABSENT")
        else:
            income_comparable = True
            combined = person["private"]
            if over_ceiling(combined, single):
                reasons.append("FAIL_INCOME_ABOVE_THRESHOLD")
    elif person["marital"] in married_codes:
        link_reason = {
            "nonresident": "UNRES_SPOUSE_NONRESIDENT",
            "unspecified": "UNRES_SPOUSE_MISSING",
            "missing": "UNRES_SPOUSE_MISSING",
            "self": "UNRES_SPOUSE_RELATIONSHIP",
            "unmatched": "UNRES_SPOUSE_NOT_IN_HOUSEHOLD",
            "not_reciprocal": "UNRES_SPOUSE_RELATIONSHIP",
        }.get(link_status)
        if link_reason:
            reasons.append(link_reason)
        elif link_status == "reciprocal" and spouse is not None:
            if person["private"] is None:
                reasons.append("UNRES_INCOME_ABSENT")
            if spouse["private"] is None:
                reasons.append("UNRES_INCOME_SPOUSE")
            if person["private"] is not None and spouse["private"] is not None:
                income_comparable = True
                combined = person["private"] + spouse["private"]
                if over_ceiling(combined, couple):
                    reasons.append("FAIL_INCOME_ABOVE_THRESHOLD")
        else:
            reasons.append("UNRES_SPOUSE_MISSING")
    else:
        reasons.append("UNRES_PARTNERSHIP_AMBIGUOUS")

    if person["child"] == "1":
        reasons.append("FLAG_CAREGIVER_CHILD_GRANT")
    if person["caredep"] == "1":
        reasons.append("FLAG_CAREGIVER_CARE_DEPENDENCY")
    if person["foster"] == "1":
        reasons.append("FLAG_CAREGIVER_FOSTER")
    if person["inaid"] == "1":
        reasons.append("FLAG_GRANT_IN_AID")

    fail = any(code.startswith("FAIL_") for code in reasons)
    unresolved = any(code.startswith("UNRES_") for code in reasons)
    if fail:
        status = "FAIL"
    elif unresolved:
        status = "UNRESOLVED"
    else:
        status = "PASS"
        reasons.append("PASS_PRIMARY")

    outcome_status = "NOT_ASSESSED"
    y_value = ""
    if status == "PASS":
        outcome_status, y_value, outcome_reasons = resolve_outcome(person)
        reasons.extend(outcome_reasons)

    return {
        "eligibility_status": status,
        "outcome_status": outcome_status,
        "y": y_value,
        "reason_codes": "|".join(reasons),
        "threshold_single": single,
        "threshold_couple": couple,
        "combined_private_income": combined if income_comparable else None,
        "in_final_cohort": int(status == "PASS" and outcome_status in {"RECIPIENT", "NON_RECIPIENT"}),
    }


def resolve_outcome(person: dict) -> tuple[str, str, list[str]]:
    any_grant = person["any_grant"]
    oldage = person["oldage"]
    reasons: list[str] = []
    y_value = ""
    if any_grant == "1" and oldage == "1":
        outcome = "RECIPIENT"
        y_value = "0"
    elif any_grant == "1" and oldage == "2":
        outcome = "NON_RECIPIENT"
        y_value = "1"
    elif any_grant == "2" and oldage in {"2", "8"}:
        outcome = "NON_RECIPIENT"
        y_value = "1"
    else:
        outcome = "UNRESOLVED"
        reasons.append("UNRES_GRANT_RESPONSE")

    if outcome in {"RECIPIENT", "NON_RECIPIENT"} and person["opg"] is not None:
        historical = person["opg"] > 0
        current = outcome == "RECIPIENT"
        if historical != current:
            reasons.append("FLAG_RECEIPT_PERIOD_DISAGREE")
    return outcome, y_value, reasons


def run_rule_checks() -> None:
    if single_threshold(1350) != THRESHOLD_2014_SINGLE:
        raise AssertionError("2014 threshold does not match Annexure A")
    if single_threshold(1410) != THRESHOLD_2015_SINGLE:
        raise AssertionError("2015 threshold does not match Annexure A")

    def person(**overrides):
        base = {
            "uqno": "H",
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
        base.update(overrides)
        return base

    def expect(result, status, y="", required=()):
        if result["eligibility_status"] != status or result["y"] != y:
            raise AssertionError((status, y, result))
        for code in required:
            if code not in result["reason_codes"].split("|"):
                raise AssertionError((code, result["reason_codes"]))

    expect(screen(person(private=Decimal(61800)), None, "not_needed"), "PASS", "1")
    expect(
        screen(person(private=Decimal("61800.01")), None, "not_needed"),
        "FAIL",
        required=("FAIL_INCOME_ABOVE_THRESHOLD",),
    )
    expect(
        screen(person(private=Decimal(64680), survey_year=2015, survey_month=4), None, "not_needed"),
        "PASS",
        "1",
    )
    expect(
        screen(person(marital="1", partner_in_hh="2", spouse_no="88", private=Decimal(0)), None, "nonresident"),
        "UNRESOLVED",
        required=("UNRES_SPOUSE_NONRESIDENT",),
    )
    expect(
        screen(
            person(marital="1", partner_in_hh="2", disability="1"),
            None,
            "nonresident",
        ),
        "FAIL",
        required=("FAIL_DISABILITY_GRANT", "UNRES_SPOUSE_NONRESIDENT"),
    )
    expect(screen(person(marital="2", partner_in_hh="1"), None, "ambiguous"), "UNRESOLVED", required=("UNRES_PARTNERSHIP_AMBIGUOUS",))
    expect(screen(person(marital="5"), None, "ambiguous"), "UNRESOLVED", required=("UNRES_PARTNERSHIP_AMBIGUOUS",))
    expect(screen(person(private=None, schedule="unresolved"), None, "not_needed"), "UNRESOLVED", required=("UNRES_INCOME_ABSENT",))
    spouse = person(personno="2", private=Decimal(60000), spouse_no="1")
    applicant = person(marital="1", partner_in_hh="1", spouse_no="2", private=Decimal(60000))
    expect(screen(applicant, spouse, "reciprocal"), "PASS", "1")
    applicant["private"] = Decimal(70000)
    expect(screen(applicant, spouse, "reciprocal"), "FAIL", required=("FAIL_INCOME_ABOVE_THRESHOLD",))
    spouse["private"] = None
    applicant["private"] = Decimal(0)
    expect(screen(applicant, spouse, "reciprocal"), "UNRESOLVED", required=("UNRES_INCOME_SPOUSE",))
    expect(screen(person(disability="1", private=Decimal(0)), None, "not_needed"), "FAIL", required=("FAIL_DISABILITY_GRANT",))
    expect(screen(person(warvet="1"), None, "not_needed"), "FAIL", required=("FAIL_WAR_VETERAN_GRANT",))
    expect(screen(person(disability="9"), None, "not_needed"), "UNRESOLVED", required=("UNRES_INCOMPATIBLE_GRANT_UNSPECIFIED",))
    caregiver = person(any_grant="1", oldage="2", child="1", private=Decimal(0))
    expect(screen(caregiver, None, "not_needed"), "PASS", "1", required=("FLAG_CAREGIVER_CHILD_GRANT",))
    recipient = person(any_grant="1", oldage="1", inaid="1", opg=Decimal(0), private=Decimal(0))
    expect(screen(recipient, None, "not_needed"), "PASS", "0", required=("FLAG_GRANT_IN_AID", "FLAG_RECEIPT_PERIOD_DISAGREE"))
    historical = person(any_grant="2", oldage="8", opg=Decimal(1000), private=Decimal(0))
    expect(screen(historical, None, "not_needed"), "PASS", "1", required=("FLAG_RECEIPT_PERIOD_DISAGREE",))
    unknown = person(any_grant="1", oldage="9", private=Decimal(0))
    expect(screen(unknown, None, "not_needed"), "PASS", "", required=("UNRES_GRANT_RESPONSE",))
    expect(
        screen(person(marital="1", partner_in_hh="1", spouse_no="1"), None, "self"),
        "UNRESOLVED",
        required=("UNRES_SPOUSE_RELATIONSHIP",),
    )
    print("rule checks passed")


def load_inputs():
    persons = pd.read_csv(
        DATA / "LCS2015PERSONSFINAL.csv",
        dtype=str,
        usecols=[
            "UQNO", "PERSONNO", "SURVEYDATE", "Q12SEX", "Q14AGE", "Q16RELATION",
            "Q17MARITAL", "Q18PARTINHH", "Q19SPOUSNO", "Q21HIGHLEVEL", "Q11714NOTOALL",
            "Q41ASOCGRANT", "Q41B1OLDAGE", "Q41B2DISAB", "Q41B3CHILD", "Q41B4CAREDEP",
            "Q41B5FOSTER", "Q41B6WARVET", "Q41B7INAID", "province_code", "SETTLEMENT_TYPE",
            "Persns_wgt",
        ],
    )
    household = pd.read_csv(
        DATA / "LCS2015HOUSEHOLD.csv",
        dtype=str,
        usecols=["UQNO", "Q531WELFARE"],
    )
    income = pd.read_csv(
        DATA / "LCS2015PERSONINCOME.csv",
        dtype=str,
        usecols=["UQNO", "PERSONNO", "Coicop", "Valueannualized"],
    )
    return persons, household, income


def build_people(persons: pd.DataFrame, income: pd.DataFrame) -> dict:
    grouped: dict[tuple[str, str], list[tuple[str, Decimal]]] = {}
    for row in income.itertuples(index=False):
        key = (row.UQNO, norm_person(row.PERSONNO))
        grouped.setdefault(key, []).append((row.Coicop, money(row.Valueannualized)))

    people = {}
    for row in persons.itertuples(index=False):
        personno = norm_person(row.PERSONNO)
        year, month = parse_survey_month(row.SURVEYDATE)
        schedule = classify_schedule(row.Q11714NOTOALL, grouped.get((row.UQNO, personno), []))
        people[(row.UQNO, personno)] = {
            "uqno": row.UQNO,
            "personno": personno,
            "surveydate": row.SURVEYDATE,
            "survey_year": year,
            "survey_month": month,
            "sex": row.Q12SEX,
            "age": int(row.Q14AGE),
            "relation": row.Q16RELATION,
            "marital": row.Q17MARITAL,
            "q11714": row.Q11714NOTOALL,
            "partner_in_hh": row.Q18PARTINHH,
            "spouse_no": row.Q19SPOUSNO,
            "schooling_raw": row.Q21HIGHLEVEL,
            "settlement": row.SETTLEMENT_TYPE,
            "province_code": row.province_code,
            "person_weight": row.Persns_wgt,
            "any_grant": row.Q41ASOCGRANT,
            "oldage": row.Q41B1OLDAGE,
            "disability": row.Q41B2DISAB,
            "child": row.Q41B3CHILD,
            "caredep": row.Q41B4CAREDEP,
            "foster": row.Q41B5FOSTER,
            "warvet": row.Q41B6WARVET,
            "inaid": row.Q41B7INAID,
            "private": schedule["private"],
            "opg": schedule["opg"],
            "schedule": schedule["schedule"],
        }
    return people


def screen_kzn(people: dict, welfare: dict[str, str]) -> pd.DataFrame:
    rows = []
    for person in people.values():
        if person["province_code"] != "5":
            continue
        year, month = person["survey_year"], person["survey_month"]
        single, couple, period = threshold_for(year, month)
        record = {
            "rule_version": RULE_VERSION,
            "uqno": person["uqno"],
            "personno": person["personno"],
            "psu": person["uqno"][:11],
            "survey_year": year,
            "survey_month": month,
            "threshold_period": period,
            "threshold_single": f"{single:.2f}",
            "threshold_couple": f"{couple:.2f}",
            "age": person["age"],
            "sex": person["sex"],
            "relation": person["relation"],
            "marital": person["marital"],
            "partner_in_hh": person["partner_in_hh"],
            "spouse_no": norm_person(person["spouse_no"]) or "",
            "schooling_raw": person["schooling_raw"],
            "settlement": person["settlement"],
            "welfare_distance": welfare.get(person["uqno"], ""),
            "person_weight": person["person_weight"],
            "income_schedule": person["schedule"],
            "applicant_private_income": "" if person["private"] is None else f"{person['private']:.2f}",
            "opg_income_annual": "" if person["opg"] is None else f"{person['opg']:.2f}",
        }
        if person["age"] < 60:
            record.update({
                "eligibility_status": "OUT_OF_FRAME",
                "outcome_status": "NOT_ASSESSED",
                "y": "",
                "reason_codes": "OUT_AGE_BELOW_60",
                "spouse_private_income": "",
                "combined_private_income": "",
                "link_status": "",
                "in_final_cohort": 0,
            })
            rows.append(record)
            continue

        link_status, spouse = resolve_link(person, people)
        result = screen(person, spouse, link_status)
        record.update(result)
        record["threshold_single"] = f"{result['threshold_single']:.2f}"
        record["threshold_couple"] = f"{result['threshold_couple']:.2f}"
        record["link_status"] = link_status
        record["spouse_private_income"] = ""
        if spouse is not None and spouse["private"] is not None and link_status == "reciprocal":
            record["spouse_private_income"] = f"{spouse['private']:.2f}"
        combined = result["combined_private_income"]
        record["combined_private_income"] = "" if combined is None else f"{combined:.2f}"
        rows.append(record)

    frame = pd.DataFrame(rows)
    return frame.sort_values(["uqno", "personno"]).reset_index(drop=True)


def flow_table(frame: pd.DataFrame) -> pd.DataFrame:
    age60 = frame["eligibility_status"] != "OUT_OF_FRAME"
    steps = [
        ("KZN sample", frame.index == frame.index),
        ("Age missing", frame["reason_codes"] == "OUT_AGE_MISSING"),
        ("Age under 60", frame["reason_codes"] == "OUT_AGE_BELOW_60"),
        ("Age 60+", age60),
        ("Eligibility FAIL", frame["eligibility_status"] == "FAIL"),
        ("Eligibility UNRESOLVED", frame["eligibility_status"] == "UNRESOLVED"),
        ("Eligibility PASS", frame["eligibility_status"] == "PASS"),
        ("Outcome unresolved", frame["outcome_status"] == "UNRESOLVED"),
        ("Recipients", frame["outcome_status"] == "RECIPIENT"),
        ("Non-recipients", frame["outcome_status"] == "NON_RECIPIENT"),
        ("Final analysis cohort", frame["in_final_cohort"] == 1),
    ]
    rows = []
    for label, mask in steps:
        subset = frame.loc[mask]
        rows.append({
            "step": label,
            "people": int(len(subset)),
            "households": int(subset["uqno"].nunique()),
        })
    return pd.DataFrame(rows)


def reason_frequencies(frame: pd.DataFrame) -> pd.DataFrame:
    age60 = frame.loc[frame["eligibility_status"] != "OUT_OF_FRAME"]
    counts: dict[str, int] = {}
    for codes in age60["reason_codes"]:
        for code in str(codes).split("|"):
            if code:
                counts[code] = counts.get(code, 0) + 1
    rows = [{"reason_code": code, "people": counts[code]} for code in sorted(counts)]
    return pd.DataFrame(rows)


def validate(frame: pd.DataFrame, flow: pd.DataFrame) -> None:
    counts = {row.step: row.people for row in flow.itertuples(index=False)}
    if counts["KZN sample"] != 15388:
        raise AssertionError(f"KZN sample changed: {counts['KZN sample']}")
    if counts["Age 60+"] != 1317:
        raise AssertionError(f"Age 60+ frame changed: {counts['Age 60+']}")
    age_parts = counts["Age missing"] + counts["Age under 60"] + counts["Age 60+"]
    if age_parts != counts["KZN sample"]:
        raise AssertionError("Age split does not add up to the KZN sample")
    screened = counts["Eligibility FAIL"] + counts["Eligibility UNRESOLVED"] + counts["Eligibility PASS"]
    if screened != counts["Age 60+"]:
        raise AssertionError("Eligibility statuses do not add up to age 60+")
    resolved = counts["Recipients"] + counts["Non-recipients"]
    if resolved + counts["Outcome unresolved"] != counts["Eligibility PASS"]:
        raise AssertionError("Outcomes do not add up to passes")
    if counts["Final analysis cohort"] != resolved:
        raise AssertionError("Final cohort is not the resolved passes")
    if frame.duplicated(["uqno", "personno"]).any():
        raise AssertionError("Duplicate person key in the cohort file")

    age60 = frame.loc[frame["eligibility_status"] != "OUT_OF_FRAME"]
    passed = age60.loc[age60["eligibility_status"] == "PASS"]
    if (passed["marital"].isin(["2", "5", "9"])).any():
        raise AssertionError("Ambiguous partnership reached PASS")
    final = frame.loc[frame["in_final_cohort"] == 1]
    if final["y"].isin(["", None]).any():
        raise AssertionError("Final cohort row without an outcome")
    if ((frame["eligibility_status"] == "FAIL") & ~frame["reason_codes"].str.contains("FAIL_")).any():
        raise AssertionError("FAIL status without a FAIL reason")
    print("cohort reconciliation passed")


def write_outputs(frame: pd.DataFrame) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    cohort_path = OUT / "cohort_person.csv"
    frame.to_csv(cohort_path, index=False)
    digest = hashlib.sha256(cohort_path.read_bytes()).hexdigest()
    flow = flow_table(frame)
    reasons = reason_frequencies(frame)
    flow.to_csv(OUT / "cohort_flow.csv", index=False)
    reasons.to_csv(OUT / "reason_frequencies.csv", index=False)
    period = (
        frame.loc[frame["eligibility_status"] != "OUT_OF_FRAME", "threshold_period"]
        .value_counts()
        .rename_axis("threshold_period")
        .reset_index(name="age_60plus_people")
    )
    period.to_csv(OUT / "threshold_periods.csv", index=False)
    freeze = {
        "rule_version": RULE_VERSION,
        "cohort_sha256": digest,
        "people": int(len(frame)),
        "flow": flow.to_dict(orient="records"),
        "threshold_2014_single": "61800",
        "threshold_2014_couple": "123600",
        "threshold_2015_single": "64680",
        "threshold_2015_couple": "129360",
        "boundary": "private income at or below the threshold passes",
    }
    (OUT / "cohort_freeze.json").write_text(json.dumps(freeze, indent=2), encoding="utf-8")
    print(flow.to_string(index=False))
    print("sha256", digest)
    return digest


def main() -> None:
    run_rule_checks()
    persons, household, income = load_inputs()
    people = build_people(persons, income)
    welfare = dict(zip(household["UQNO"], household["Q531WELFARE"]))
    frame = screen_kzn(people, welfare)
    flow = flow_table(frame)
    validate(frame, flow)
    write_outputs(frame)


if __name__ == "__main__":
    main()
