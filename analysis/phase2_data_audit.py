"""Phase 2 data audit for the LCS 2014/2015 files.

Reads the released CSV files and writes join, key, and code-frequency
tables. It does not screen eligibility and does not fit a model.

Outputs go to output/phase2/.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Dataset" / "LCS2015"
OUT = ROOT / "output" / "phase2"
OUT.mkdir(parents=True, exist_ok=True)

# COICOP labels from Living Conditions Survey Coicopcodes.pdf, income section.
COICOP_LABEL = {
    "50110000": "Household salaries and wages",
    "50120000": "Household self-employment and business",
    "50121000": "Income from subsistence farming",
    "50210000": "Income from letting of fixed property",
    "50220000": "Royalties",
    "50230000": "Interest received",
    "50241000": "Dividends of listed companies",
    "50242000": "Dividends of unlisted companies",
    "50243000": "Unit trusts",
    "50243200": "Income from share trading",
    "50310000": "Pension from previous employment",
    "50320000": "Annuities from own investment",
    "50331000": "Old age grant",
    "50332000": "Disability grants",
    "50332100": "Child support grant",
    "50333100": "Care dependency grant",
    "50333200": "Foster care grant",
    "50333300": "Grant-in-aid",
    "50333400": "War veterans grant",
    "50333500": "Other assistance from government (social relief)",
    "50333600": "Other funds (compensation, UIF and similar)",
    "50410000": "Alimony, palimony and other allowances",
    "50420000": "Other income from individuals",
}

# Social-assistance grants named in questionnaire section 4.1, plus social relief.
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


def write_df(name, frame):
    path = OUT / name
    frame.to_csv(path, index=False)
    print(f"wrote {path.name} ({len(frame)} rows)")


def person_columns():
    return [
        "UQNO", "PERSONNO", "SURVEYDATE", "Q12SEX", "Q14AGE", "Q16RELATION",
        "Q17MARITAL", "Q18PARTINHH", "Q19SPOUSNO", "Q21HIGHLEVEL",
        "Q11710GRANTS", "Q11714NOTOALL",
        "Q41ASOCGRANT", "Q41B1OLDAGE", "Q41B2DISAB", "Q41B3CHILD",
        "Q41B4CAREDEP", "Q41B5FOSTER", "Q41B6WARVET", "Q41B7INAID",
        "province_code", "SETTLEMENT_TYPE", "Persns_wgt",
    ]


def load():
    persons = pd.read_csv(DATA / "LCS2015PERSONSFINAL.csv", usecols=person_columns(), dtype=str)
    household = pd.read_csv(
        DATA / "LCS2015HOUSEHOLD.csv",
        usecols=["UQNO", "Q531WELFARE", "Q532WELFARE", "province_code", "SETTLEMENT_TYPE", "income", "hholds_wgt"],
        dtype=str,
    )
    income = pd.read_csv(
        DATA / "LCS2015PERSONINCOME.csv",
        usecols=["UQNO", "PERSONNO", "Coicop", "Valueannualized", "Valueannualized_adj", "Persns_wgt"],
        dtype=str,
    )
    assets = pd.read_csv(DATA / "LCS2015HOUSEHOLDASSETS.csv", usecols=["UQNO"], dtype=str)
    total = pd.read_csv(DATA / "LCS2015TOTALLCS.csv", usecols=["UQNO", "CoicopType"], dtype=str)
    return persons, household, income, assets, total


def inventory(persons, household, income, assets, total):
    rows = []
    for name, frame, key in [
        ("LCS2015PERSONSFINAL.csv", persons, "UQNO+PERSONNO"),
        ("LCS2015HOUSEHOLD.csv", household, "UQNO"),
        ("LCS2015PERSONINCOME.csv", income, "UQNO+PERSONNO+Coicop"),
        ("LCS2015HOUSEHOLDASSETS.csv", assets, "UQNO"),
        ("LCS2015TOTALLCS.csv", total, "UQNO+item row"),
    ]:
        rows.append({"file": name, "rows_read": len(frame), "columns_read": frame.shape[1], "intended_key": key})
    write_df("file_inventory.csv", pd.DataFrame(rows))


def join_audit(persons, household, income, assets, total):
    person_key = ["UQNO", "PERSONNO"]
    findings = []

    def add(check, value):
        findings.append({"check": check, "value": value})

    add("person_rows", len(persons))
    add("person_duplicate_uqno_personno", int(persons.duplicated(person_key).sum()))
    add("person_unique_households", int(persons["UQNO"].nunique()))
    add("uqno_length_not_18", int((persons["UQNO"].str.len() != 18).sum()))
    add("household_rows", len(household))
    add("household_duplicate_uqno", int(household.duplicated(["UQNO"]).sum()))
    add("persons_without_household", int((~persons["UQNO"].isin(household["UQNO"])).sum()))
    add("households_without_person", int((~household["UQNO"].isin(persons["UQNO"])).sum()))

    merged = persons.merge(
        household[["UQNO", "province_code", "SETTLEMENT_TYPE"]],
        on="UQNO",
        how="left",
        suffixes=("_person", "_household"),
    )
    add("joined_person_rows", len(merged))
    add("province_mismatch", int((merged["province_code_person"] != merged["province_code_household"]).sum()))
    add("settlement_mismatch", int((merged["SETTLEMENT_TYPE_person"] != merged["SETTLEMENT_TYPE_household"]).sum()))

    add("income_rows", len(income))
    add("income_duplicate_person_coicop", int(income.duplicated(["UQNO", "PERSONNO", "Coicop"]).sum()))
    add("income_unique_persons", int(income.groupby(person_key).ngroups))
    income_people = income[person_key].drop_duplicates()
    add("income_person_keys_not_in_person_file", int((~income_people.set_index(person_key).index.isin(persons.set_index(person_key).index)).sum()))
    add("persons_with_no_income_row", int(len(persons) - income.groupby(person_key).ngroups))

    weight = persons[person_key + ["Persns_wgt"]].merge(
        income[person_key + ["Persns_wgt"]].drop_duplicates(person_key),
        on=person_key,
        how="inner",
        suffixes=("_person", "_income"),
    )
    add("person_weight_mismatches_on_income_rows", int((weight["Persns_wgt_person"] != weight["Persns_wgt_income"]).sum()))

    person_weight = pd.to_numeric(persons["Persns_wgt"], errors="coerce")
    add("person_weight_missing", int(person_weight.isna().sum()))
    add("person_weight_nonpositive", int((person_weight <= 0).sum()))

    add("asset_rows", len(assets))
    add("asset_duplicate_uqno", int(assets.duplicated(["UQNO"]).sum()))
    add("asset_uqno_not_in_household", int((~assets["UQNO"].isin(household["UQNO"])).sum()))
    add("households_missing_from_assets", int((~household["UQNO"].isin(assets["UQNO"])).sum()))

    add("total_lcs_rows", len(total))
    add("total_lcs_unique_households", int(total["UQNO"].nunique()))
    add("total_lcs_uqno_not_in_household", int((~total["UQNO"].drop_duplicates().isin(household["UQNO"])).sum()))
    add("households_missing_from_total_lcs", int((~household["UQNO"].isin(total["UQNO"])).sum()))

    persons = persons.copy()
    persons["psu"] = persons["UQNO"].str.slice(0, 11)
    add("derived_psu_count", int(persons["psu"].nunique()))
    add("derived_psu_crossing_provinces", int((persons.groupby("psu")["province_code"].nunique() > 1).sum()))
    add("kzn_persons_province_5", int((persons["province_code"] == "5").sum()))
    add("kzn_households_province_5", int(persons.loc[persons["province_code"] == "5", "UQNO"].nunique()))
    add("kzn_derived_psu", int(persons.loc[persons["province_code"] == "5", "psu"].nunique()))
    age = pd.to_numeric(persons["Q14AGE"], errors="coerce")
    add("age_non_numeric", int(age.isna().sum()))
    kzn60 = (persons["province_code"] == "5") & (age >= 60)
    add("kzn_age_60plus_persons", int(kzn60.sum()))
    add("kzn_age_60plus_households", int(persons.loc[kzn60, "UQNO"].nunique()))

    write_df("join_audit.csv", pd.DataFrame(findings))


def code_frequencies(persons, household, income):
    frames = []
    for col in [
        "Q12SEX", "province_code", "SETTLEMENT_TYPE", "Q17MARITAL", "Q18PARTINHH",
        "Q16RELATION", "Q21HIGHLEVEL", "Q11710GRANTS", "Q11714NOTOALL",
        "Q41ASOCGRANT", "Q41B1OLDAGE", "Q41B2DISAB", "Q41B3CHILD",
        "Q41B4CAREDEP", "Q41B5FOSTER", "Q41B6WARVET", "Q41B7INAID",
    ]:
        vc = persons[col].value_counts(dropna=False).rename_axis("code").reset_index(name="n")
        vc.insert(0, "variable", col)
        vc.insert(1, "file", "LCS2015PERSONSFINAL.csv")
        frames.append(vc)
    for col in ["Q531WELFARE", "Q532WELFARE", "province_code", "SETTLEMENT_TYPE"]:
        vc = household[col].value_counts(dropna=False).rename_axis("code").reset_index(name="n")
        vc.insert(0, "variable", col)
        vc.insert(1, "file", "LCS2015HOUSEHOLD.csv")
        frames.append(vc)
    coicop = income["Coicop"].value_counts(dropna=False).rename_axis("code").reset_index(name="n")
    coicop.insert(0, "variable", "Coicop")
    coicop.insert(1, "file", "LCS2015PERSONINCOME.csv")
    coicop["label"] = coicop["code"].map(COICOP_LABEL)
    coicop["social_assistance_grant"] = coicop["code"].isin(SOCIAL_ASSISTANCE)
    frames.append(coicop)
    write_df("code_frequencies.csv", pd.concat(frames, ignore_index=True))


def income_absence(persons, income):
    has = income[["UQNO", "PERSONNO"]].drop_duplicates()
    has["has_income_row"] = 1
    m = persons.merge(has, on=["UQNO", "PERSONNO"], how="left")
    m["has_income_row"] = m["has_income_row"].fillna(0).astype(int)
    m["age"] = pd.to_numeric(m["Q14AGE"], errors="coerce")
    m["frame"] = "national"
    k = m[(m["province_code"] == "5") & (m["age"] >= 60)].copy()
    k["frame"] = "kzn_age_60plus"
    both = pd.concat([m, k], ignore_index=True)
    tab = (
        both.groupby(["frame", "Q11714NOTOALL", "has_income_row"], dropna=False)
        .size()
        .reset_index(name="n")
    )
    write_df("income_absence_by_q11714.csv", tab)


def spouse_audit(persons):
    lookup = persons.set_index(["UQNO", "PERSONNO"])

    def link_status(row):
        if row.Q19SPOUSNO == row.PERSONNO:
            return "self_pointer"
        key = (row.UQNO, row.Q19SPOUSNO)
        if key not in lookup.index:
            return "unmatched"
        spouse = lookup.loc[key]
        if isinstance(spouse, pd.DataFrame) or spouse["Q19SPOUSNO"] != row.PERSONNO:
            return "not_reciprocal"
        pair = {row.Q16RELATION, spouse["Q16RELATION"]}
        if pair == {"1", "2"}:
            return "reciprocal_head_and_partner"
        return "reciprocal_other_relationship"

    scope = persons[(persons["Q17MARITAL"] == "1") & (persons["Q18PARTINHH"] == "1")].copy()
    scope["link_status"] = [link_status(row) for row in scope.itertuples(index=False)]
    scope["age"] = pd.to_numeric(scope["Q14AGE"], errors="coerce")
    scope["frame"] = "national_married_partner_in_household"
    kzn = scope[(scope["province_code"] == "5") & (scope["age"] >= 60)].copy()
    kzn["frame"] = "kzn_age_60plus_married_partner_in_household"
    both = pd.concat([scope, kzn], ignore_index=True)
    tab = both.groupby(["frame", "link_status"], dropna=False).size().reset_index(name="n")
    write_df("spouse_link_audit.csv", tab)


def main():
    persons, household, income, assets, total = load()
    inventory(persons, household, income, assets, total)
    join_audit(persons, household, income, assets, total)
    code_frequencies(persons, household, income)
    income_absence(persons, income)
    spouse_audit(persons)
    print("phase 2 audit complete")


if __name__ == "__main__":
    main()
