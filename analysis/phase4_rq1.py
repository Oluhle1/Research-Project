"""Phase 4: RQ1 description and eligibility sensitivities.

Reads the frozen primary cohort. Does not edit that file and does not
fit a model. Alternative screens are calculated separately.
"""

from __future__ import annotations

import hashlib
import math
import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase3_build_cohort as cohort  # noqa: E402

OUT = ROOT / "output" / "phase4"
FROZEN = ROOT / "output" / "phase3" / "cohort_person.csv"
FROZEN_HASH = "50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2"
OTHER_FUNDS = "50333600"

SEX = {"1": "Male", "2": "Female"}
SETTLEMENT = {
    "1": "Urban formal",
    "2": "Urban informal",
    "4": "Traditional area",
    "5": "Rural formal",
}
MARITAL = {
    "1": "Married",
    "2": "Living together",
    "3": "Never married",
    "4": "Widowed",
    "5": "Separated",
    "6": "Divorced",
    "9": "Unspecified",
}


def require_frozen_cohort() -> pd.DataFrame:
    digest = hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    if digest != FROZEN_HASH:
        raise SystemExit(f"Frozen cohort hash is {digest}, expected {FROZEN_HASH}")
    frame = pd.read_csv(FROZEN, dtype=str)
    frame["age_n"] = pd.to_numeric(frame["age"])
    frame["weight_n"] = pd.to_numeric(frame["person_weight"])
    frame["y_n"] = pd.to_numeric(frame["y"])
    frame["opg_n"] = pd.to_numeric(frame["opg_income_annual"])
    frame["combined_n"] = pd.to_numeric(frame["combined_private_income"])
    return frame


def weighted_rate(y: pd.Series, weight: pd.Series) -> float:
    return float((weight * y).sum() / weight.sum())


def psu_cluster_se(y: pd.Series, weight: pd.Series, psu: pd.Series) -> tuple[float, float, int]:
    """With-replacement PSU linearisation for a weighted proportion.

    Strata were not released, so this is not a full design-based interval.
    """
    rate = weighted_rate(y, weight)
    score = weight * (y - rate)
    clustered = score.groupby(psu).sum()
    n_psu = int(len(clustered))
    variance = (n_psu / (n_psu - 1)) * float((clustered ** 2).sum())
    se = math.sqrt(variance) / float(weight.sum())
    return rate, se, n_psu


def schooling_class(code: str) -> str:
    if code in {"21", "22", "31", "32", "99"}:
        return "Not assigned"
    if code == "98":
        return "Below Grade 7"
    value = int(code)
    if 1 <= value <= 7:
        return "Below Grade 7"
    if 8 <= value <= 20 or 23 <= value <= 30:
        return "Grade 7 or above"
    return "Not assigned"


def welfare_class(code: str) -> str:
    if code in {"", "9", "99"}:
        return "Missing"
    value = int(code)
    if 1 <= value <= 4:
        return "Nearer than 5 km"
    if 5 <= value <= 8:
        return "At least 5 km or unavailable"
    return "Missing"


def age_band(age: int) -> str:
    if age < 70:
        return "60-69"
    if age < 75:
        return "70-74"
    return "75 or older"


def describe(final: pd.DataFrame) -> pd.DataFrame:
    work = final.copy()
    work["sex_label"] = work["sex"].map(SEX)
    work["schooling_label"] = work["schooling_raw"].map(schooling_class)
    work["settlement_label"] = work["settlement"].map(SETTLEMENT)
    work["welfare_label"] = work["welfare_distance"].map(welfare_class)
    work["marital_label"] = work["marital"].map(MARITAL)
    work["age_band"] = work["age_n"].map(age_band)
    groups = {
        "Recipients": work[work["y"] == "0"],
        "Non-recipients": work[work["y"] == "1"],
        "Final cohort": work,
    }
    rows = []
    for group_name, subset in groups.items():
        rows.append({
            "variable": "Age in completed years",
            "level": "Mean",
            "group": group_name,
            "people": int(len(subset)),
            "unweighted_share": "",
            "weighted_share": "",
            "weighted_mean": float((subset["weight_n"] * subset["age_n"]).sum() / subset["weight_n"].sum()),
            "unweighted_mean": float(subset["age_n"].mean()),
            "role": "Table I predictor",
        })
        specs = [
            ("Age group", "age_band", "Table I predictor"),
            ("Sex", "sex_label", "Table I predictor"),
            ("Schooling", "schooling_label", "Table I predictor"),
            ("Settlement", "settlement_label", "Table I predictor"),
            ("Welfare-office access", "welfare_label", "Table I predictor"),
            ("Marital status", "marital_label", "Screening variable"),
        ]
        for variable, column, role in specs:
            counts = subset.groupby(column).size()
            weights = subset.groupby(column)["weight_n"].sum()
            total_n = int(len(subset))
            total_w = float(subset["weight_n"].sum())
            for level in counts.index:
                rows.append({
                    "variable": variable,
                    "level": level,
                    "group": group_name,
                    "people": int(counts[level]),
                    "unweighted_share": counts[level] / total_n,
                    "weighted_share": float(weights[level] / total_w),
                    "weighted_mean": "",
                    "unweighted_mean": "",
                    "role": role,
                })
    return pd.DataFrame(rows)


def primary_estimates(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    age60 = frame[frame["eligibility_status"] != "OUT_OF_FRAME"]
    passed = age60[age60["eligibility_status"] == "PASS"]
    final = frame[frame["in_final_cohort"] == "1"].copy()
    unresolved_outcome = int((passed["outcome_status"] == "UNRESOLVED").sum())
    nonrecipients = int((final["y"] == "1").sum())
    recipients = int((final["y"] == "0").sum())
    denominator = int(len(final))
    unweighted = nonrecipients / denominator
    weighted, se, n_psu = psu_cluster_se(final["y_n"], final["weight_n"], final["psu"])
    # Outcome bounds. Unresolved PASS outcomes are assigned first to receipt, then to non-receipt.
    bound_n = denominator + unresolved_outcome
    low_unweighted = nonrecipients / bound_n
    high_unweighted = (nonrecipients + unresolved_outcome) / bound_n
    if unresolved_outcome == 0:
        low_weighted = high_weighted = weighted
    else:
        unresolved_rows = passed[passed["outcome_status"] == "UNRESOLVED"]
        y_low = pd.concat([final["y_n"], pd.Series(0, index=unresolved_rows.index)])
        w_low = pd.concat([final["weight_n"], unresolved_rows["weight_n"]])
        y_high = pd.concat([final["y_n"], pd.Series(1, index=unresolved_rows.index)])
        low_weighted = weighted_rate(y_low, w_low)
        high_weighted = weighted_rate(y_high, w_low)
    at_ceiling = int((final["combined_n"] == pd.to_numeric(final["threshold_single"])).sum())
    # Applicable ceiling is the couple ceiling when a spouse amount is present.
    applicable = final["threshold_single"].where(final["spouse_private_income"].eq(""), final["threshold_couple"])
    at_ceiling = int((final["combined_n"] == pd.to_numeric(applicable)).sum())
    rows = [
        {
            "estimate": "Unweighted non-receipt",
            "numerator": nonrecipients,
            "denominator": denominator,
            "value": unweighted,
            "se": "",
            "ci_low": "",
            "ci_high": "",
            "note": "Non-recipients divided by resolved passes",
        },
        {
            "estimate": "Weighted non-receipt",
            "numerator": nonrecipients,
            "denominator": denominator,
            "value": weighted,
            "se": "",
            "ci_low": "",
            "ci_high": "",
            "note": "sum(person weight x Y) / sum(person weight); Persns_wgt",
        },
        {
            "estimate": "PSU-clustered approximation",
            "numerator": nonrecipients,
            "denominator": denominator,
            "value": weighted,
            "se": se,
            "ci_low": weighted - 1.96 * se,
            "ci_high": weighted + 1.96 * se,
            "note": f"With-replacement linearisation on {n_psu} derived PSUs. Strata were not released. Not a full design-based interval.",
        },
        {
            "estimate": "Outcome bound, unresolved assigned to receipt",
            "numerator": nonrecipients,
            "denominator": bound_n,
            "value": low_unweighted,
            "se": "",
            "ci_low": "",
            "ci_high": "",
            "note": f"Unweighted. Unresolved PASS outcomes: {unresolved_outcome}. Weighted value {low_weighted:.10f}",
        },
        {
            "estimate": "Outcome bound, unresolved assigned to non-receipt",
            "numerator": nonrecipients + unresolved_outcome,
            "denominator": bound_n,
            "value": high_unweighted,
            "se": "",
            "ci_low": "",
            "ci_high": "",
            "note": f"Unweighted. Unresolved PASS outcomes: {unresolved_outcome}. Weighted value {high_weighted:.10f}",
        },
    ]
    summary = {
        "recipients": recipients,
        "nonrecipients": nonrecipients,
        "denominator": denominator,
        "unweighted": unweighted,
        "weighted": weighted,
        "se": se,
        "n_psu": n_psu,
        "unresolved_eligibility": int((age60["eligibility_status"] == "UNRESOLVED").sum()),
        "fails": int((age60["eligibility_status"] == "FAIL").sum()),
        "unresolved_outcome": unresolved_outcome,
        "at_ceiling": at_ceiling,
        "low_weighted": low_weighted,
        "high_weighted": high_weighted,
    }
    return pd.DataFrame(rows), summary


def ceilings(person: dict, mode: str) -> dict:
    single, _couple, _period = cohort.threshold_for(person["survey_year"], person["survey_month"])
    fail_at_equal = False
    if mode == "all_2014":
        single = cohort.THRESHOLD_2014_SINGLE
    elif mode == "all_2015":
        single = cohort.THRESHOLD_2015_SINGLE
    elif mode == "age75" and person["age"] >= 75:
        single = single + Decimal(960)
    elif mode == "zero_grant":
        if (person["survey_year"], person["survey_month"]) < (2015, 4):
            single = Decimal(64800)
        else:
            single = Decimal(67680)
        fail_at_equal = True
    return {"single": single, "couple": single * 2, "fail_at_equal": fail_at_equal}


def screen_age60(people: dict, rules: dict | None = None) -> pd.DataFrame:
    rules = rules or {}
    single_codes = set(cohort.UNPARTNERED) | set(rules.get("also_single", ()))
    married_codes = {"1"} | set(rules.get("also_married", ()))
    mode = rules.get("ceiling_mode")
    rows = []
    for person in people.values():
        if person["province_code"] != "5" or person["age"] < 60:
            continue
        link_status, spouse = cohort.resolve_link(person, people, married_codes, single_codes)
        person_rules = {key: value for key, value in rules.items() if key != "ceiling_mode"}
        if mode:
            person_rules.update(ceilings(person, mode))
        result = cohort.screen(person, spouse, link_status, person_rules)
        rows.append({
            "uqno": person["uqno"],
            "personno": person["personno"],
            "psu": person["uqno"][:11],
            "weight": float(person["person_weight"]),
            "eligibility_status": result["eligibility_status"],
            "outcome_status": result["outcome_status"],
            "y": result["y"],
            "in_final": result["in_final_cohort"],
        })
    return pd.DataFrame(rows)


def scenario_row(scenario: str, rule: str, screened: pd.DataFrame, primary: dict) -> dict:
    final = screened[screened["in_final"] == 1]
    denominator = int(len(final))
    recipients = int((final["y"] == "0").sum())
    nonrecipients = int((final["y"] == "1").sum())
    unweighted = nonrecipients / denominator if denominator else math.nan
    weighted = weighted_rate(pd.to_numeric(final["y"]), final["weight"]) if denominator else math.nan
    return {
        "scenario": scenario,
        "rule_changed": rule,
        "cohort_size": denominator,
        "households": int(final["uqno"].nunique()) if denominator else 0,
        "recipients": recipients,
        "nonrecipients": nonrecipients,
        "unweighted_nonreceipt": unweighted,
        "weighted_nonreceipt": weighted,
        "change_in_cohort": denominator - primary["denominator"],
        "change_in_nonrecipients": nonrecipients - primary["nonrecipients"],
        "unweighted_change_pp": (unweighted - primary["unweighted"]) * 100,
        "weighted_change_pp": (weighted - primary["weighted"]) * 100,
        "eligibility_fail": int((screened["eligibility_status"] == "FAIL").sum()),
        "eligibility_unresolved": int((screened["eligibility_status"] == "UNRESOLVED").sum()),
    }


def regroup(income: pd.DataFrame, amount_col: str) -> dict:
    grouped: dict[tuple[str, str], list[tuple[str, Decimal]]] = {}
    for row in income.itertuples(index=False):
        key = (row.UQNO, cohort.norm_person(row.PERSONNO))
        grouped.setdefault(key, []).append((row.Coicop, cohort.money(getattr(row, amount_col))))
    return grouped


def with_income(people: dict, grouped: dict, exclude: set[str]) -> dict:
    updated = {}
    for key, person in people.items():
        cloned = dict(person)
        schedule = cohort.classify_schedule(person["q11714"], grouped.get(key, []), exclude)
        cloned["private"] = schedule["private"]
        cloned["opg"] = schedule["opg"]
        cloned["schedule"] = schedule["schedule"]
        updated[key] = cloned
    return updated


def receipt_period_scenario(frame: pd.DataFrame, primary: dict) -> dict:
    final = frame[frame["in_final_cohort"] == "1"].copy()
    historical_receipt = final["opg_n"] > 0
    current_receipt = final["y"] == "0"
    flips = int((historical_receipt != current_receipt).sum())
    # Keep the current label where the two measures agree. Where they disagree, follow the income record.
    nonreceipt = pd.Series(~current_receipt.to_numpy(), index=final.index)
    use_history = historical_receipt.to_numpy() != current_receipt.to_numpy()
    nonreceipt.loc[use_history] = ~historical_receipt.loc[use_history]
    denominator = int(len(final))
    nonrecipients = int(nonreceipt.sum())
    recipients = denominator - nonrecipients
    unweighted = nonrecipients / denominator
    weighted = weighted_rate(nonreceipt.astype(float), final["weight_n"])
    return {
        "scenario": "S5",
        "rule_changed": "Where current receipt and preceding-year OPG income disagree, use the income record. Primary eligibility screen unchanged.",
        "cohort_size": denominator,
        "households": int(final["uqno"].nunique()),
        "recipients": recipients,
        "nonrecipients": nonrecipients,
        "unweighted_nonreceipt": unweighted,
        "weighted_nonreceipt": weighted,
        "change_in_cohort": 0,
        "change_in_nonrecipients": nonrecipients - primary["nonrecipients"],
        "unweighted_change_pp": (unweighted - primary["unweighted"]) * 100,
        "weighted_change_pp": (weighted - primary["weighted"]) * 100,
        "eligibility_fail": primary["fails"],
        "eligibility_unresolved": primary["unresolved_eligibility"],
        "disagreements": flips,
    }


def main() -> None:
    frame = require_frozen_cohort()
    estimates, primary = primary_estimates(frame)
    characteristics = describe(frame[frame["in_final_cohort"] == "1"])
    age60 = frame[frame["eligibility_status"] != "OUT_OF_FRAME"]
    unresolved_profile = (
        age60.groupby(["eligibility_status", "marital"]).size().reset_index(name="people")
    )
    unresolved_profile["marital_label"] = unresolved_profile["marital"].map(MARITAL)

    persons, _household, _income_nominal = cohort.load_inputs()
    income = pd.read_csv(
        cohort.DATA / "LCS2015PERSONINCOME.csv",
        dtype=str,
        usecols=["UQNO", "PERSONNO", "Coicop", "Valueannualized", "Valueannualized_adj"],
    )
    people = cohort.build_people(persons, income)
    primary_screen = screen_age60(people, {})
    primary_check = scenario_row("check", "primary engine", primary_screen, primary)
    if primary_check["cohort_size"] != primary["denominator"] or primary_check["nonrecipients"] != primary["nonrecipients"]:
        raise SystemExit(f"Rescreen does not reproduce the frozen cohort: {primary_check}")

    nominal = regroup(income, "Valueannualized")
    adjusted = regroup(income, "Valueannualized_adj")
    people_adjusted = with_income(people, adjusted, cohort.SOCIAL_ASSISTANCE)
    people_with_grants = with_income(people, nominal, set())
    people_without_other_funds = with_income(people, nominal, cohort.SOCIAL_ASSISTANCE | {OTHER_FUNDS})

    scenarios = [
        ("S0", "Primary screen", people, {}),
        ("S1a", "Every interview uses the 1 April 2014 ceiling (R61,800 / R123,600).", people, {"ceiling_mode": "all_2014"}),
        ("S1b", "Every interview uses the 1 April 2015 ceiling (R64,680 / R129,360).", people, {"ceiling_mode": "all_2015"}),
        ("S1c", "Age 75 or older uses a ceiling R960 higher, from the R20 monthly supplement. Named simplification.", people, {"ceiling_mode": "age75"}),
        ("S1d", "Ceiling is the income at which the formula pays nothing (4 x annual maximum). Income at that point fails.", people, {"ceiling_mode": "zero_grant"}),
        ("S2a", "Living together (code 2) is screened on the couple ceiling when a resident partner can be linked.", people, {"also_married": ("2",)}),
        ("S2b", "Living together (code 2) is screened on the single-person ceiling.", people, {"also_single": ("2",)}),
        ("S2c", "Separated (code 5) is screened on the single-person ceiling.", people, {"also_single": ("5",)}),
        ("S2d", "Living together and separated are both screened on the single-person ceiling.", people, {"also_single": ("2", "5")}),
        ("S3", "Own disability and war-veterans grant recipients are retained.", people, {"exclude_incompatible_grants": False}),
        ("S4a", "CPI-adjusted income is compared with the nominal statutory ceilings. Price bases differ.", people_adjusted, {}),
        ("S4b", "Social-assistance income is kept in the resource proxy.", people_with_grants, {}),
        ("S4c", "Workmen's compensation, UIF and similar funds (COICOP 50333600) are also excluded.", people_without_other_funds, {}),
    ]
    rows = []
    for scenario, rule, population, rules in scenarios:
        screened = primary_screen if scenario == "S0" else screen_age60(population, rules)
        rows.append(scenario_row(scenario, rule, screened, primary))
    rows.append(receipt_period_scenario(frame, primary))
    for label, assign_nonreceipt in (
        ("S6a", False),
        ("S6b", True),
    ):
        rows.append({
            "scenario": label,
            "rule_changed": "Unresolved PASS outcomes assigned to " + ("non-receipt" if assign_nonreceipt else "receipt"),
            "cohort_size": primary["denominator"] + primary["unresolved_outcome"],
            "households": "",
            "recipients": primary["recipients"] + (0 if assign_nonreceipt else primary["unresolved_outcome"]),
            "nonrecipients": primary["nonrecipients"] + (primary["unresolved_outcome"] if assign_nonreceipt else 0),
            "unweighted_nonreceipt": (
                primary["nonrecipients"] + (primary["unresolved_outcome"] if assign_nonreceipt else 0)
            ) / (primary["denominator"] + primary["unresolved_outcome"]),
            "weighted_nonreceipt": primary["high_weighted"] if assign_nonreceipt else primary["low_weighted"],
            "change_in_cohort": primary["unresolved_outcome"],
            "change_in_nonrecipients": primary["unresolved_outcome"] if assign_nonreceipt else 0,
            "unweighted_change_pp": (
                (
                    primary["nonrecipients"] + (primary["unresolved_outcome"] if assign_nonreceipt else 0)
                ) / (primary["denominator"] + primary["unresolved_outcome"])
                - primary["unweighted"]
            ) * 100,
            "weighted_change_pp": (
                (primary["high_weighted"] if assign_nonreceipt else primary["low_weighted"]) - primary["weighted"]
            ) * 100,
            "eligibility_fail": primary["fails"],
            "eligibility_unresolved": primary["unresolved_eligibility"],
        })

    OUT.mkdir(parents=True, exist_ok=True)
    estimates.to_csv(OUT / "rq1_estimate.csv", index=False)
    characteristics.to_csv(OUT / "rq1_characteristics.csv", index=False)
    pd.DataFrame(rows).to_csv(OUT / "rq1_sensitivity.csv", index=False)
    unresolved_profile.to_csv(OUT / "rq1_status_by_marital.csv", index=False)
    print(estimates.to_string(index=False))
    print(pd.DataFrame(rows)[["scenario", "cohort_size", "nonrecipients", "unweighted_nonreceipt", "weighted_nonreceipt", "unweighted_change_pp"]].to_string(index=False))
    print("at ceiling", primary["at_ceiling"], "psu", primary["n_psu"], "se", primary["se"])


if __name__ == "__main__":
    main()
