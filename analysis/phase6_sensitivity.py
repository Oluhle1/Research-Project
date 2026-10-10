"""Phase 6: model sensitivities kept apart from the primary result.

Reuses the Phase 5 coding and the Phase 4 screens. Does not edit the
frozen cohort or the primary out-of-fold file. Does not fit a random forest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase3_build_cohort as cohort  # noqa: E402
import phase4_rq1 as phase4  # noqa: E402
import phase5_model as model  # noqa: E402

OUT = ROOT / "output" / "phase6"
PRIMARY_AUC = 0.752248
PRIMARY_BRIER = 0.057780


def assign_groups(work: pd.DataFrame, group_col: str) -> pd.DataFrame:
    groups = (
        work.groupby(group_col, as_index=False)
        .agg(any_event=("y_n", "max"))
        .sort_values(group_col)
        .reset_index(drop=True)
    )
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=model.SEED)
    fold_of = {}
    for fold, (_, test_index) in enumerate(splitter.split(groups, groups["any_event"]), start=1):
        for group_id in groups.loc[test_index, group_col]:
            fold_of[group_id] = fold
    out = work.copy()
    out["fold"] = out[group_col].map(fold_of)
    if out["fold"].isna().any() or out.groupby(group_col)["fold"].nunique().max() != 1:
        raise SystemExit(f"Fold assignment failed for {group_col}")
    return out


def fit_weighted(y: np.ndarray, matrix: pd.DataFrame, weight: np.ndarray):
    design = sm.add_constant(matrix.to_numpy(dtype=float), has_constant="add")
    result = sm.GLM(y, design, family=sm.families.Binomial(), freq_weights=weight).fit(maxiter=200)
    return result, bool(getattr(result, "converged", False))


def matrix_partnered(filled: pd.DataFrame) -> pd.DataFrame:
    """Welfare access is replaced by a married indicator. Slope count stays six."""
    return pd.DataFrame({
        "age_per_10": filled["age_per_10"].astype(float),
        "sex_female": (filled["sex_code"] == "2").astype(float),
        "school_below": (filled["school_code"] == "1").astype(float),
        "settle_urban_informal": (filled["settlement_code"] == "2").astype(float),
        "settle_traditional_or_rural": filled["settlement_code"].isin(["4", "5"]).astype(float),
        "partnered_married": (filled["marital"] == "1").astype(float),
    }, index=filled.index)


def cross_validate(work: pd.DataFrame, matrix_fn, weighted: bool, group_col: str) -> dict:
    folded = assign_groups(work, group_col)
    support = []
    for fold, subset in folded.groupby("fold"):
        support.append((int(fold), int(subset["y_n"].sum()), int((subset["y_n"] == 0).sum())))
    if any(events == 0 or non_events == 0 for _, events, non_events in support):
        return {"status": "fold_without_both_classes", "fold_events": support}
    probability = pd.Series(np.nan, index=folded.index)
    converged_flags = []
    for fold in range(1, 6):
        train = folded[folded["fold"] != fold]
        test = folded[folded["fold"] == fold]
        stats = model.learning_stats(train)
        train_m = matrix_fn(model.apply_stats(train, stats))
        test_m = matrix_fn(model.apply_stats(test, stats))
        y_train = train["y_n"].to_numpy()
        if weighted:
            result, converged = fit_weighted(y_train, train_m, pd.to_numeric(train["person_weight"]).to_numpy())
            design = sm.add_constant(test_m.to_numpy(dtype=float), has_constant="add")
            probability.loc[test.index] = np.asarray(result.predict(design), dtype=float)
        else:
            result, _names, converged = model.fit_logit(y_train, train_m)
            probability.loc[test.index] = model.predict(result, test_m)
        converged_flags.append(bool(converged))
    y = folded["y_n"].to_numpy()
    predicted = probability.to_numpy()
    metrics = model.metric_row("sensitivity", y, predicted)
    return {
        "status": "ok",
        "people": int(len(folded)),
        "events": int(y.sum()),
        "households": int(folded["uqno"].nunique()),
        "groups": int(folded[group_col].nunique()),
        "folds_converged": int(sum(converged_flags)),
        "auc": metrics["roc_auc"],
        "average_precision": metrics["average_precision"],
        "brier": metrics["brier"],
        "citl": metrics["calibration_in_the_large"],
        "slope": metrics["calibration_slope"],
        "fold_events": support,
    }


def analysis_frame(raw: pd.DataFrame, keys: pd.DataFrame | None = None) -> pd.DataFrame:
    work = raw.copy()
    if keys is not None:
        keep = keys.loc[keys["in_final"] == 1, ["uqno", "personno", "y"]].copy()
        keep["personno"] = keep["personno"].map(cohort.norm_person)
        work["personno"] = work["personno"].map(cohort.norm_person)
        merged = keep.merge(work.drop(columns=["y"]), on=["uqno", "personno"], how="left", indicator=True)
        if (merged["_merge"] != "both").any() or merged["age"].isna().any():
            raise SystemExit("A screened person is missing from the cohort file")
        merged["y"] = keep["y"].to_numpy()
        work = merged.drop(columns=["_merge"])
    else:
        work = work[work["in_final_cohort"] == "1"].copy()
    prepared = model.prepare(work)
    prepared["psu"] = prepared["uqno"].str.slice(0, 11)
    return prepared


def row_from_result(scenario: str, rule: str, result: dict, primary: dict, same_cohort: bool) -> dict:
    if result.get("status") != "ok":
        return {
            "scenario": scenario,
            "rule_changed": rule,
            "same_cohort_as_primary": same_cohort,
            "status": result.get("status"),
            "people": "",
            "events": "",
            "households": "",
            "auc": "",
            "average_precision": "",
            "brier": "",
            "citl": "",
            "slope": "",
            "auc_minus_primary": "",
            "brier_minus_primary": "",
            "folds_converged": "",
        }
    return {
        "scenario": scenario,
        "rule_changed": rule,
        "same_cohort_as_primary": same_cohort,
        "status": "ok",
        "people": result["people"],
        "events": result["events"],
        "households": result["households"],
        "auc": result["auc"],
        "average_precision": result["average_precision"],
        "brier": result["brier"],
        "citl": result["citl"],
        "slope": result["slope"],
        "auc_minus_primary": result["auc"] - primary["auc"],
        "brier_minus_primary": result["brier"] - primary["brier"],
        "folds_converged": result["folds_converged"],
    }


def load_people_and_raw():
    raw = pd.read_csv(model.FROZEN, dtype=str)
    digest = __import__("hashlib").sha256(model.FROZEN.read_bytes()).hexdigest()
    if digest != model.FROZEN_HASH:
        raise SystemExit("Frozen cohort hash changed")
    persons, _household, _income = cohort.load_inputs()
    income = pd.read_csv(
        cohort.DATA / "LCS2015PERSONINCOME.csv",
        dtype=str,
        usecols=["UQNO", "PERSONNO", "Coicop", "Valueannualized", "Valueannualized_adj"],
    )
    people = cohort.build_people(persons, income)
    return raw, people, income


def main() -> None:
    raw, people, income = load_people_and_raw()
    primary_frame = analysis_frame(raw)
    primary = cross_validate(primary_frame, model.model_matrix, weighted=False, group_col="uqno")
    if abs(primary["auc"] - PRIMARY_AUC) > 1e-4:
        raise SystemExit(f"Primary AUC {primary['auc']} does not match Phase 5 {PRIMARY_AUC}")

    nominal = phase4.regroup(income, "Valueannualized")
    adjusted = phase4.regroup(income, "Valueannualized_adj")
    populations = {
        "primary": people,
        "adjusted": phase4.with_income(people, adjusted, cohort.SOCIAL_ASSISTANCE),
        "with_grants": phase4.with_income(people, nominal, set()),
        "without_other_funds": phase4.with_income(people, nominal, cohort.SOCIAL_ASSISTANCE | {phase4.OTHER_FUNDS}),
    }
    scenario_specs = [
        ("S1a", "2014 ceiling for every interview", "primary", {"ceiling_mode": "all_2014"}),
        ("S1b", "2015 ceiling for every interview", "primary", {"ceiling_mode": "all_2015"}),
        ("S1c", "Age-75 supplement added to the ceiling", "primary", {"ceiling_mode": "age75"}),
        ("S1d", "Ceiling where the formula pays nothing", "primary", {"ceiling_mode": "zero_grant"}),
        ("S2a", "Living together screened as a couple", "primary", {"also_married": ("2",)}),
        ("S2b", "Living together screened as single", "primary", {"also_single": ("2",)}),
        ("S2c", "Separated screened as single", "primary", {"also_single": ("5",)}),
        ("S2d", "Living together and separated screened as single", "primary", {"also_single": ("2", "5")}),
        ("S3", "Disability and war-veterans recipients retained", "primary", {"exclude_incompatible_grants": False}),
        ("S4a", "CPI-adjusted income, nominal ceilings", "adjusted", {}),
        ("S4b", "Social-assistance income kept in the proxy", "with_grants", {}),
        ("S4c", "UIF and similar funds also excluded", "without_other_funds", {}),
    ]
    rows = [row_from_result("S0", "Primary six-slope model, household folds", primary, primary, True)]
    screened_cache = {}
    for scenario, rule, population_name, rules in scenario_specs:
        screened = phase4.screen_age60(populations[population_name], rules)
        screened_cache[scenario] = screened
        final_keys = set(zip(
            screened.loc[screened["in_final"] == 1, "uqno"],
            screened.loc[screened["in_final"] == 1, "personno"].map(cohort.norm_person),
        ))
        primary_keys = set(zip(primary_frame["uqno"], primary_frame["personno"].map(cohort.norm_person)))
        same = final_keys == primary_keys
        if same:
            result = primary
        else:
            result = cross_validate(analysis_frame(raw, screened), model.model_matrix, False, "uqno")
        rows.append(row_from_result(scenario, rule, result, primary, same))

    for label, rule in (
        ("S5", "Receipt-period relabel. No disagreements in the primary pass group."),
        ("S6a", "Unresolved outcomes assigned to receipt. None in the pass group."),
        ("S6b", "Unresolved outcomes assigned to non-receipt. None in the pass group."),
    ):
        rows.append(row_from_result(label, rule, primary, primary, True))
    weighted_metrics = pd.read_csv(ROOT / "output" / "phase5" / "metrics.csv")
    weighted_metrics = weighted_metrics.loc[
        weighted_metrics["model"] == "logistic_out_of_fold_weighted_metrics"
    ].iloc[0]
    weighted_result = {
        "status": "ok",
        "people": primary["people"],
        "events": primary["events"],
        "households": primary["households"],
        "folds_converged": 5,
        "auc": float(weighted_metrics["roc_auc"]),
        "average_precision": float(weighted_metrics["average_precision"]),
        "brier": float(weighted_metrics["brier"]),
        "citl": float(weighted_metrics["calibration_in_the_large"]),
        "slope": float(weighted_metrics["calibration_slope"]),
    }
    rows.append(row_from_result(
        "S10",
        "Person-weighted metrics on the primary unweighted out-of-fold predictions. Not a new fit.",
        weighted_result,
        primary,
        True,
    ))

    complete = primary_frame.dropna(subset=["school_code", "welfare_code"])
    rows.append(row_from_result(
        "S7",
        "Complete cases on schooling and welfare distance",
        cross_validate(complete, model.model_matrix, False, "uqno"),
        primary,
        False,
    ))
    rows.append(row_from_result(
        "S8",
        "Married indicator replaces welfare access. Reference is not married. Living-together adults are outside this cohort.",
        cross_validate(primary_frame, matrix_partnered, False, "uqno"),
        primary,
        True,
    ))
    rows.append(row_from_result(
        "S9",
        "Survey-weighted fit with Persns_wgt as frequency weights. Imputation stays unweighted. Metrics below are unweighted on the held-out people.",
        cross_validate(primary_frame, model.model_matrix, True, "uqno"),
        primary,
        True,
    ))
    rows.append(row_from_result(
        "S11",
        "Five-fold validation grouped by derived primary sampling unit instead of household",
        cross_validate(primary_frame, model.model_matrix, False, "psu"),
        primary,
        True,
    ))

    OUT.mkdir(parents=True, exist_ok=True)
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "model_sensitivity.csv", index=False)
    record = {
        "primary_auc_reproduced": primary["auc"],
        "primary_brier_reproduced": primary["brier"],
        "partnered_definition": "marital code 1 within the primary final cohort",
        "weighted_fit": "GLM binomial frequency weights; prediction metrics on held-out people are unweighted in row S9",
        "random_forest": "not run; specification places it after artefact evaluation",
        "s1d_same_people_as_s1b": set(zip(
            screened_cache["S1d"].loc[screened_cache["S1d"]["in_final"] == 1, "uqno"],
            screened_cache["S1d"].loc[screened_cache["S1d"]["in_final"] == 1, "personno"],
        )) == set(zip(
            screened_cache["S1b"].loc[screened_cache["S1b"]["in_final"] == 1, "uqno"],
            screened_cache["S1b"].loc[screened_cache["S1b"]["in_final"] == 1, "personno"],
        )),
    }
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    show = table[["scenario", "same_cohort_as_primary", "people", "events", "auc", "brier", "slope", "folds_converged"]]
    print(show.to_string(index=False))
    print(record)


if __name__ == "__main__":
    main()
