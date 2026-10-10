"""Minimum artefact: rerun the primary OPG study from the released LCS files.

Usage:
    python analysis/run_study.py

Writes output/runs/primary/. The command builds the cohort, the RQ1
description, and the held-out logistic evaluation. It does not start the
review interface and it does not fit a random forest.

A researcher can open cohort_person.csv for a person's status and reason
codes, and oof_predictions.csv for that person's held-out probability and
validation fold.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import phase3_build_cohort as cohort  # noqa: E402
import phase4_rq1 as description  # noqa: E402
import phase5_model as model  # noqa: E402

RUN = ROOT / "output" / "runs" / "primary"
INPUTS = [
    cohort.DATA / "LCS2015PERSONSFINAL.csv",
    cohort.DATA / "LCS2015HOUSEHOLD.csv",
    cohort.DATA / "LCS2015PERSONINCOME.csv",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def software() -> dict:
    import numpy
    import sklearn
    import statsmodels

    return {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": numpy.__version__,
        "statsmodels": statsmodels.__version__,
        "sklearn": sklearn.__version__,
    }


def build_cohort() -> pd.DataFrame:
    cohort.run_rule_checks()
    model.check_rules()
    persons, household, income = cohort.load_inputs()
    people = cohort.build_people(persons, income)
    welfare = dict(zip(household["UQNO"], household["Q531WELFARE"]))
    frame = cohort.screen_kzn(people, welfare)
    flow = cohort.flow_table(frame)
    cohort.validate(frame, flow)
    return frame


def write_cohort(frame: pd.DataFrame) -> str:
    RUN.mkdir(parents=True, exist_ok=True)
    path = RUN / "cohort_person.csv"
    frame.to_csv(path, index=False)
    digest = sha256(path)
    cohort.flow_table(frame).to_csv(RUN / "cohort_flow.csv", index=False)
    cohort.reason_frequencies(frame).to_csv(RUN / "reason_frequencies.csv", index=False)
    return digest


def write_description(cohort_path: Path) -> dict:
    frame = pd.read_csv(cohort_path, dtype=str)
    frame["age_n"] = pd.to_numeric(frame["age"])
    frame["weight_n"] = pd.to_numeric(frame["person_weight"])
    frame["y_n"] = pd.to_numeric(frame["y"])
    frame["opg_n"] = pd.to_numeric(frame["opg_income_annual"])
    frame["combined_n"] = pd.to_numeric(frame["combined_private_income"])
    estimates, summary = description.primary_estimates(frame)
    characteristics = description.describe(frame[frame["in_final_cohort"] == "1"])
    estimates.to_csv(RUN / "rq1_estimate.csv", index=False)
    characteristics.to_csv(RUN / "rq1_characteristics.csv", index=False)
    return summary


def write_model() -> dict:
    raw = pd.read_csv(RUN / "cohort_person.csv", dtype=str)
    work = model.prepare(raw[raw["in_final_cohort"] == "1"])
    work, _households = model.assign_folds(work)
    support = model.fold_support(work)
    if (support["events"] == 0).any() or (support["non_events"] == 0).any():
        raise SystemExit("A validation fold lacks an outcome class")
    support.to_csv(RUN / "fold_support.csv", index=False)

    predictions = work[["uqno", "personno", "fold", "y_n", "person_weight"]].copy()
    predictions["p_model"] = float("nan")
    predictions["p_intercept"] = float("nan")
    coefficient_rows = []
    imputer_rows = []
    for fold in range(1, 6):
        train = work[work["fold"] != fold]
        test = work[work["fold"] == fold]
        stats = model.learning_stats(train)
        imputer_rows.append({"fold": fold, **stats})
        train_matrix = model.model_matrix(model.apply_stats(train, stats))
        test_matrix = model.model_matrix(model.apply_stats(test, stats))
        result, names, converged = model.fit_logit(train["y_n"].to_numpy(), train_matrix)
        if not converged:
            raise SystemExit(f"Fold {fold} did not converge")
        coefficient_rows.append({
            "fold": fold,
            "converged": converged,
            **dict(zip(names, [float(value) for value in result.params])),
        })
        predictions.loc[test.index, "p_model"] = model.predict(result, test_matrix)
        predictions.loc[test.index, "p_intercept"] = float(train["y_n"].mean())

    y = predictions["y_n"].to_numpy()
    probability = predictions["p_model"].to_numpy()
    reference = predictions["p_intercept"].to_numpy()
    metrics = pd.DataFrame([
        model.metric_row("logistic_out_of_fold", y, probability),
        {
            "model": "intercept_only_out_of_fold",
            "prevalence": float(y.mean()),
            "average_precision": "",
            "roc_auc": "",
            "brier": float(__import__("sklearn.metrics", fromlist=["brier_score_loss"]).brier_score_loss(y, reference)),
            "calibration_in_the_large": model.citl_and_slope(y, reference)[0],
            "calibration_slope": "",
        },
    ])
    bins = model.calibration_bins(y, probability)
    model.plot_calibration(bins, RUN / "calibration_plot.png")
    intervals, invalid = model.bootstrap(predictions.assign(p_model=probability, p_intercept=reference))
    predictions.to_csv(RUN / "oof_predictions.csv", index=False)
    metrics.to_csv(RUN / "metrics.csv", index=False)
    bins.to_csv(RUN / "calibration_bins.csv", index=False)
    intervals.to_csv(RUN / "bootstrap_intervals.csv", index=False)
    pd.DataFrame(coefficient_rows).to_csv(RUN / "fold_coefficients.csv", index=False)
    pd.DataFrame(imputer_rows).to_csv(RUN / "fold_imputers.csv", index=False)
    auc = float(metrics.loc[metrics["model"] == "logistic_out_of_fold", "roc_auc"].iloc[0])
    brier = float(metrics.loc[metrics["model"] == "logistic_out_of_fold", "brier"].iloc[0])
    return {"roc_auc": auc, "brier": brier, "bootstrap_invalid": invalid}


def example_person() -> dict:
    cohort_rows = pd.read_csv(RUN / "cohort_person.csv", dtype=str)
    predictions = pd.read_csv(RUN / "oof_predictions.csv", dtype=str)
    final = cohort_rows[cohort_rows["in_final_cohort"] == "1"].iloc[0]
    prediction = predictions[
        (predictions["uqno"] == final["uqno"]) & (predictions["personno"] == final["personno"])
    ].iloc[0]
    return {
        "uqno": final["uqno"],
        "personno": final["personno"],
        "eligibility_status": final["eligibility_status"],
        "reason_codes": final["reason_codes"],
        "y": final["y"],
        "fold": prediction["fold"],
        "held_out_probability": prediction["p_model"],
        "rule_version": cohort.RULE_VERSION,
    }


def main() -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    print("Building the primary cohort")
    frame = build_cohort()
    cohort_hash = write_cohort(frame)
    if cohort_hash != model.FROZEN_HASH:
        raise SystemExit(f"Cohort hash {cohort_hash} does not match the frozen cohort")
    print("Cohort hash matches the frozen file")
    summary = write_description(RUN / "cohort_person.csv")
    print("Fitting the held-out model")
    performance = write_model()
    if abs(performance["roc_auc"] - 0.752248272380171) > 1e-8:
        raise SystemExit(f"ROC area {performance['roc_auc']} does not match Phase 5")
    outputs = {
        path.name: sha256(path)
        for path in sorted(RUN.iterdir())
        if path.is_file() and path.name != "run_record.json"
    }
    record = {
        "configuration": "primary",
        "rule_version": cohort.RULE_VERSION,
        "model_specification": {
            "estimator": "unweighted logistic regression",
            "slopes": model.SLOPE_NAMES,
            "reference_levels": {
                "sex": "male (code 1)",
                "schooling": "Grade 7 or above",
                "settlement": "urban formal; traditional area and rural formal share one contrast",
                "welfare": "nearer than 5 km",
            },
            "validation": "five household-grouped folds, stratified on any non-recipient in the household",
            "seed": model.SEED,
            "bootstrap_draws": model.N_BOOT,
        },
        "input_sha256": {path.name: sha256(path) for path in INPUTS},
        "cohort_sha256": cohort_hash,
        "output_sha256": outputs,
        "software": software(),
        "results": {
            "final_cohort": summary["denominator"],
            "nonrecipients": summary["nonrecipients"],
            "unweighted_nonreceipt": summary["unweighted"],
            "weighted_nonreceipt": summary["weighted"],
            "roc_auc": performance["roc_auc"],
            "brier": performance["brier"],
        },
        "inspection": example_person(),
    }
    (RUN / "run_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record["results"], indent=2))
    print("Wrote", RUN)


if __name__ == "__main__":
    main()
