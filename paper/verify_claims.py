#!/usr/bin/env python3
"""Recheck the paper against retained evidence without fitting any model.

Run from any directory: python /path/to/repository/paper/verify_claims.py --write
Only Python's standard library is required. The default is a read-only check;
--write replaces the three paper audit/register files owned by this verifier.
This is an audit of saved evidence, not a new application test execution,
publisher verification, ethics determination, or proof of human usability.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE = "opg-kzn-primary-v1"
MODEL = "opg-kzn-six-slope-v1"
VERSION = f"{RULE}; {MODEL}"
REGISTER_FIELDS = [
    "Paper section", "Claim/number", "Underlying output file and row/field",
    "Rule/model version", "Rechecked?", "Notes",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def participant_usability_unproven(text: str) -> bool:
    """Require a stated testing limit and reject common affirmative claims.

    The phrase check accepts retained, first-person and professional active
    explanations. An affirmative-claim scan matters because adding a truthful
    limit elsewhere must not make a contradictory participant claim pass.
    This text check does not replace a human review of the manuscript.
    """
    stated_limit = re.search(
        r"(?:participant usability (?:has not|remains untested)|"
        r"usability[^\n.]{0,80}not conducted|human interpretation remains untested|"
        r"I have not tested (?:how easily participants use it|participant usability)|"
        r"I have not established human usability|"
        r"no participant study tested ease of use)", text, re.I)
    participant_row = re.search(
        r"^\|\s*Participant usability\s*\|\s*([^|]+)", text, re.I | re.M)
    if participant_row and participant_row.group(1).strip().lower() != "not conducted":
        return False
    active_actor = r"(?:I|we|(?:the|this)\s+(?:study|project|research|evaluation|team|researcher|author))"
    affirmative_patterns = [
        rf"\b{active_actor}\s+(?:have\s+|has\s+)?(?:successfully\s+)?"
        r"(?:tested|evaluated|established|proved|demonstrated|confirmed)\s+"
        r"(?:the\s+)?(?:participant|human|user)\s+usability\b",
        rf"\b{active_actor}\s+(?:have\s+|has\s+)?(?:conducted|completed|performed|ran)\s+"
        r"(?:a\s+)?(?:participant|human|user)\s+(?:study|test(?:ing)?|evaluation)\b",
        r"\b(?:participant|human|user)\s+usability\s+"
        r"(?:(?:has|had)\s+been|was|is)\s+(?:successfully\s+)?"
        r"(?:tested|evaluated|established|proved|demonstrated|confirmed)\b",
        r"\b(?:participant|human|user)\s+(?:study|testing|evaluation)\s+"
        r"(?:has\s+been|was|is)\s+(?:conducted|completed|performed)\b",
        r"\b(?:\d+|three|four|five)\s+(?:consenting\s+)?(?:participants|users)\s+"
        r"(?:completed|tested|evaluated|tried|used|rated)\b",
    ]
    for pattern in affirmative_patterns:
        for match in re.finditer(pattern, text, re.I):
            # "No participant study has been conducted" states a limit, even
            # though its noun/verb sequence also resembles a positive claim.
            prefix = text[max(0, match.start() - 60):match.start()]
            negative_subject = re.search(
                r"\b(?:no|not|without)\s+(?:\w+\s+){0,2}$", prefix, re.I)
            if not negative_subject:
                return False
    return bool(stated_limit)


def audit(manuscript: Path) -> tuple[dict, dict, list[dict]]:
    raw = manuscript.read_bytes()
    text = raw.decode("utf-8")
    manuscript_hash = hashlib.sha256(raw).hexdigest()
    rows, comparisons, support, sources, limits = [], [], [], {}, []

    def source(path: str) -> Path:
        p = ROOT / path
        sources[path] = digest(p)
        return p

    def csv_rows(path: str) -> list[dict]:
        with source(path).open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))

    def read_json(path: str) -> dict:
        return json.loads(source(path).read_text(encoding="utf-8"))

    def register(section, claim, origin, status, notes="", version=VERSION):
        rows.append(dict(zip(REGISTER_FIELDS, [section, claim, origin, version, status, notes])))

    def check(section, claim, origin, condition, notes="", recorded=False):
        passed = bool(condition)
        support.append({"claim": claim, "passed": passed, "source": origin,
                        "basis": "previously saved evidence" if recorded else "recomputed/read from frozen output"})
        register(section, claim, origin, "Yes: saved record" if passed and recorded else
                 "Yes" if passed else "FAILED", notes)

    def limit(section, claim, origin, notes, version="Not independently established"):
        limits.append({"claim": claim, "source": origin, "limitation": notes})
        register(section, claim, origin, "LIMIT: not independently verified", notes, version)

    def numbers(cell: str) -> list[str]:
        return re.findall(r"[-−]?(?:\d+\.\d+|\.\d+|\d+)", cell.replace(",", ""))

    def table(label: str) -> list[list[str]]:
        m = re.search(rf"^TABLE: Table {label}\. [^\n]+\n((?:\|[^\n]+\n)+)", text, re.M)
        if not m:
            raise ValueError(f"Missing or malformed table {label}")
        return [[c.strip() for c in line.strip().strip("|").split("|")]
                for line in m.group(1).splitlines()[2:]]

    def numeric(label, claim, actual, expected, origin):
        # Match the precision actually printed, rather than rounding all values
        # to a fixed arbitrary tolerance. Integer counts must match exactly.
        token = actual.replace("−", "-")
        precision = len(token.partition(".")[2]) if "." in token else 0
        expected_display = f"{float(expected):.{precision}f}"
        passed = float(token) == float(expected_display)
        comparisons.append({"table": label, "claim": claim, "displayed": actual,
                            "expected_rounded": expected_display, "passed": passed, "source": origin})
        register(f"Table {label}", f"{claim} = {actual}", origin,
                 "Yes" if passed else "FAILED",
                 "Compared at the precision printed in the manuscript; no model refit.")

    def prose(section, claim, passage, pattern, expected, origin):
        match = re.search(pattern, passage)
        actual = match.group(1) if match else None
        if actual is None:
            passed = False
        else:
            token = actual.replace(",", "").replace("−", "-")
            precision = len(token.partition(".")[2]) if "." in token else 0
            passed = float(token) == float(f"{float(expected):.{precision}f}")
        check(section, f"{claim}: {actual if actual is not None else 'MISSING'}", origin,
              passed, "Paper prose compared with frozen evidence at its printed precision.")

    def cell(label, claim, actual, expected, origin):
        tokens = numbers(actual)
        if len(tokens) != len(expected):
            raise ValueError(f"Table {label}, {claim}: expected {len(expected)} numeric entries, found {tokens}")
        for index, (token, value) in enumerate(zip(tokens, expected), 1):
            numeric(label, f"{claim} [{index}]" if len(tokens) > 1 else claim,
                    token, value, origin)

    flow_path = "output/runs/primary/cohort_flow.csv"
    flow = {r["step"]: r for r in csv_rows(flow_path)}
    cohort_steps = ["KZN sample", "Age 60+", "Eligibility FAIL", "Eligibility UNRESOLVED",
                    "Final analysis cohort", "Recipients", "Non-recipients"]
    for printed, step in zip(table("IV"), cohort_steps):
        for index, field in [(1, "people"), (2, "households")]:
            cell("IV", f"{step}: {field}", printed[index], [flow[step][field]],
                 f"{flow_path}; step={step}; {field}")
    if len(table("IV")) != 7:
        raise ValueError("Table IV must contain the seven audited cohort rows")

    char_path = "output/runs/primary/rq1_characteristics.csv"
    characteristics = {(r["variable"], r["level"], r["group"]): r for r in csv_rows(char_path)}
    char_labels = [("Age in completed years", "Mean"), ("Sex", "Female"),
                   ("Schooling", "Grade 7 or above"), ("Settlement", "Urban formal"),
                   ("Welfare-office access", "At least 5 km or unavailable")]
    if len(table("V")) != 5:
        raise ValueError("Table V must contain the five audited predictor domains")
    for printed, (variable, level) in zip(table("V"), char_labels):
        for index, group in [(1, "Recipients"), (2, "Non-recipients")]:
            r = characteristics[(variable, level, group)]
            values = [r["unweighted_mean"], r["weighted_mean"]] if level == "Mean" else [
                r["people"], 100 * float(r["unweighted_share"]), 100 * float(r["weighted_share"])]
            cell("V", f"{variable}/{level}: {group}", printed[index], values,
                 f"{char_path}; variable={variable}; level={level}; group={group}; " +
                 ("unweighted_mean, weighted_mean" if level == "Mean" else "people, unweighted_share*100, weighted_share*100"))

    screen_path = "output/phase4/rq1_sensitivity.csv"
    model_path = "output/phase6/model_sensitivity.csv"
    screens = {r["scenario"]: r for r in csv_rows(screen_path)}
    models = {r["scenario"]: r for r in csv_rows(model_path)}
    scenarios = [["S0"], ["S1b", "S1d"], ["S2a"], ["S2b"], ["S2c"], ["S2d"],
                 ["S3"], ["S4b"], ["S1a", "S1c", "S4a", "S4c", "S5", "S6a", "S6b"]]
    if len(table("VI")) != 9:
        raise ValueError("Table VI must contain nine displayed rows covering 16 scenarios")
    for printed, group in zip(table("VI"), scenarios):
        for scenario in group:
            s, m = screens[scenario], models[scenario]
            values = [[s["cohort_size"], s["nonrecipients"]],
                      [100 * float(s["unweighted_nonreceipt"])], [100 * float(s["weighted_nonreceipt"])],
                      [m["auc"]], [m["brier"]], [m["slope"]]]
            for index, (field, expected) in enumerate(zip(
                    ["N/events", "unweighted prevalence", "person-weighted prevalence", "AUC", "Brier", "slope"], values), 1):
                cell("VI", f"{scenario}: {field}", printed[index], expected,
                     f"{screen_path}; {model_path}; scenario={scenario}; {field}")
            check("III.E / Tables VI,VIII", f"{scenario} definition and converged folds", model_path + f"; scenario={scenario}",
                  bool(s["rule_changed"]) and bool(m["rule_changed"]) and m["status"] == "ok" and int(m["folds_converged"]) == 5,
                  f"Screen: {s['rule_changed']} Model/evaluation: {m['rule_changed']}")

    metrics_path = "output/runs/primary/metrics.csv"
    intervals_path = "output/runs/primary/bootstrap_intervals.csv"
    metrics = {r["model"]: r for r in csv_rows(metrics_path)}
    intervals = {r["metric"]: r for r in csv_rows(intervals_path)}
    primary, intercept = metrics["logistic_out_of_fold"], metrics["intercept_only_out_of_fold"]
    metric_fields = [("roc_auc", "roc_auc"), ("average_precision", "average_precision"),
                     ("brier", "brier"), ("calibration_in_the_large", "citl"), ("calibration_slope", "slope")]
    if len(table("VII")) != 5:
        raise ValueError("Table VII must contain five metric rows")
    for printed, (field, interval_key) in zip(table("VII"), metric_fields):
        b = intervals[interval_key]
        cell("VII", field, printed[1], [primary[field], b["percentile_2.5"], b["percentile_97.5"]],
             f"{metrics_path}; model=logistic_out_of_fold; {field}; {intervals_path}; metric={interval_key}")
        if field == "brier":
            b = intervals["brier_intercept"]
            cell("VII", "intercept Brier", printed[2], [intercept[field], b["percentile_2.5"], b["percentile_97.5"]],
                 f"{metrics_path}; model=intercept_only_out_of_fold; brier; {intervals_path}; metric=brier_intercept")
        elif field == "calibration_in_the_large":
            cell("VII", "intercept CITL", printed[2], [intercept[field]],
                 f"{metrics_path}; model=intercept_only_out_of_fold; {field}")
        else:
            check("Table VII", f"Intercept {field} is unavailable, not zero", metrics_path,
                  intercept[field] == "" and printed[2] == "—")

    if len(table("VIII")) != 6:
        raise ValueError("Table VIII must contain six model/validation scenarios")
    for printed, scenario in zip(table("VIII"), ["S0", "S7", "S8", "S9", "S10", "S11"]):
        m = models[scenario]
        for index, (field, values) in enumerate([
                ("N/events", [m["people"], m["events"]]),
                ("unweighted prevalence", [100 * int(m["events"]) / int(m["people"])]),
                ("AUC", [m["auc"]]), ("Brier", [m["brier"]]), ("slope", [m["slope"]])], 1):
            cell("VIII", f"{scenario}: {field}", printed[index], values,
                 f"{model_path}; scenario={scenario}; {field}")
        check("III.E / Table VIII", f"{scenario} saved specification", model_path + f"; scenario={scenario}; rule_changed",
              m["status"] == "ok" and int(m["folds_converged"]) == 5, m["rule_changed"])

    # Independent aggregate recalculation from retained OOF predictions. These
    # files contain identifiers, but only aggregate findings enter the register.
    oof_path = "output/runs/primary/oof_predictions.csv"
    predictions = csv_rows(oof_path)
    n, events = len(predictions), sum(int(r["y_n"]) for r in predictions)
    weight_sum = math.fsum(float(r["person_weight"]) for r in predictions)
    weighted_rate = math.fsum(float(r["person_weight"]) * int(r["y_n"]) for r in predictions) / weight_sum
    check("Abstract / III.D / V.A,C", "1,013 people; 67 events; prevalence 0.06614017769", oof_path,
          n == 1013 and events == 67 and math.isclose(events / n, float(primary["prevalence"]), abs_tol=1e-14),
          "Recomputed from retained OOF rows; no identifiers copied to this register.")
    check("V.A / VI.A", "Person-weighted prevalence 7.487682626%", oof_path + "; person_weight, y_n",
          math.isclose(weighted_rate, float(screens["S0"]["weighted_nonreceipt"]), abs_tol=1e-14),
          "Independent weighted-ratio sum; displayed as 7.49%.")
    hh_folds = defaultdict(set)
    for r in predictions:
        hh_folds[r["uqno"]].add(r["fold"])
    check("III.D", "827 households; five folds; no household split across folds", oof_path + "; uqno, fold",
          len(hh_folds) == 827 and all(len(s) == 1 for s in hh_folds.values()) and
          {r["fold"] for r in predictions} == {"1", "2", "3", "4", "5"})
    grouped_scores = defaultdict(lambda: [0, 0])
    for r in predictions:
        grouped_scores[float(r["p_model"])][int(r["y_n"])] += 1
    lower_negative, concordance = 0, 0.0
    for probability in sorted(grouped_scores):
        negatives, positives = grouped_scores[probability]
        concordance += positives * (lower_negative + negatives / 2)
        lower_negative += negatives
    auc = concordance / (events * (n - events))
    true_positive, cumulative, ap = 0, 0, 0.0
    for probability in sorted(grouped_scores, reverse=True):
        negatives, positives = grouped_scores[probability]
        true_positive += positives
        cumulative += negatives + positives
        ap += (positives / events) * (true_positive / cumulative)
    brier = math.fsum((float(r["p_model"]) - int(r["y_n"])) ** 2 for r in predictions) / n
    baseline_brier = math.fsum((float(r["p_intercept"]) - int(r["y_n"])) ** 2 for r in predictions) / n
    for label, computed, expected in [("AUC", auc, primary["roc_auc"]), ("AP", ap, primary["average_precision"]),
                                     ("Brier", brier, primary["brier"]), ("intercept Brier", baseline_brier, intercept["brier"])]:
        check("V.C / VI.B", f"OOF {label} recomputed = {computed:.12g}", oof_path + f"; y_n, p_model/p_intercept; {metrics_path}",
              math.isclose(computed, float(expected), rel_tol=0, abs_tol=1e-12),
              "Rank-tie-aware AUC/AP or squared-error sum, computed without estimator fitting.")
    improvement = baseline_brier - brier
    check("VI.B", f"Absolute Brier reduction = {improvement:.12g} (approximately 0.0040)", metrics_path,
          round(improvement, 4) == 0.004)

    abstract = next(line for line in text.splitlines() if line.startswith("Abstract—"))
    conclusion = text.split("## VIII. Conclusion", 1)[1]
    discussion = text.split("## VI. Discussion", 1)[1].split("## VII.", 1)[0]
    # Definitions can sit between a metric's name and its value. The number
    # still has to follow that name; this does not accept an unrelated number
    # elsewhere in the section as a substitute for a missing prose claim.
    definition_and_link = r"(?:\s*\([^()\n]*\))?\s*(?:(?:is|was|of|=)\s*)?"
    for section, passage in [("Abstract", abstract), ("VI.B", discussion), ("VIII", conclusion)]:
        for claim, pattern, value in [
                ("primary AUC", rf"AUC{definition_and_link}(\d+\.\d+)", auc),
                ("primary AP", rf"(?:average precision|AP){definition_and_link}(\d+\.\d+)", ap),
                ("primary Brier", rf"Brier(?: score)?{definition_and_link}(\d+\.\d+)", brier)]:
            if section == "VI.B" and claim == "primary Brier":
                pattern = r"Brier (?:improvement|falls|fell) from \d+\.\d+ to (\d+\.\d+)"
            prose(section, claim, passage, pattern, value, metrics_path + "; model=logistic_out_of_fold")
    prose("Abstract", "intercept-only Brier", abstract,
          r"(?:compared with|Predicting only[^.\n]+gives) (\d+\.\d+)", baseline_brier,
          metrics_path + "; model=intercept_only_out_of_fold")
    prose("VI.B", "absolute Brier reduction", discussion,
          r"(?:reduction of approximately |a modest )(\d+\.\d+)(?: reduction)?", improvement, metrics_path)
    for section, passage in [("Abstract", abstract), ("VI.A", discussion), ("VIII", conclusion)]:
        prose(section, "unweighted prevalence", passage, r"(\d+\.\d+)% unweighted", 100 * events / n, metrics_path)
        prose(section, "person-weighted prevalence", passage, r"(\d+\.\d+)% person-weighted", 100 * weighted_rate, screen_path + "; scenario=S0")
        if section != "VI.A":
            prose(section, "lowest screening sensitivity", passage,
                  r"(?:ranged from|alternatives yield|weighted rates of|alternatives give|alternatives gave) (\d+\.\d+)%",
                  100 * min(float(r["weighted_nonreceipt"]) for r in screens.values()), screen_path)
            prose(section, "highest screening sensitivity", passage,
                  r"(?:ranged from|alternatives yield|weighted rates of|alternatives give|alternatives gave) "
                  r"\d+\.\d+%\s*(?:to|[–−-])\s*(\d+\.\d+)%",
                  100 * max(float(r["weighted_nonreceipt"]) for r in screens.values()), screen_path)

    cohort_path = "output/runs/primary/cohort_person.csv"
    cohort = csv_rows(cohort_path)
    final = [r for r in cohort if r["in_final_cohort"] == "1"]
    psu_scores = defaultdict(float)
    for r in final:
        psu_scores[r["psu"]] += float(r["person_weight"]) * (int(r["y"]) - weighted_rate)
    psus = len(psu_scores)
    se = math.sqrt(psus / (psus - 1) * math.fsum(v * v for v in psu_scores.values())) / weight_sum
    estimate_path = "output/runs/primary/rq1_estimate.csv"
    estimate = next(r for r in csv_rows(estimate_path) if r["estimate"] == "PSU-clustered approximation")
    check("V.A", "345 derived PSUs; SE 1.294833441 pp; approximate 95% interval 4.9498–10.0256%", cohort_path + f"; psu, y, person_weight; {estimate_path}",
          psus == 345 and math.isclose(se, float(estimate["se"]), abs_tol=1e-13) and
          math.isclose(weighted_rate - 1.96 * se, float(estimate["ci_low"]), abs_tol=1e-13) and
          math.isclose(weighted_rate + 1.96 * se, float(estimate["ci_high"]), abs_tol=1e-13),
          "With-replacement linearisation independently recalculated; no released strata, not a full design-based interval.")
    check("V.A / Fig. 3", "15,388 KZN rows; 1,317 aged 60+; FAIL 117; unresolved 187; resolved PASS 1,013", cohort_path,
          len(cohort) == 15388 and sum(int(r["age"]) >= 60 for r in cohort) == 1317 and
          sum(r["eligibility_status"] == "FAIL" for r in cohort) == 117 and
          sum(r["eligibility_status"] == "UNRESOLVED" for r in cohort) == 187 and len(final) == 1013,
          "Recounted retained screen output; this does not rerun the screening engine.")

    bins_path = "output/runs/primary/calibration_bins.csv"
    bins = csv_rows(bins_path)
    check("Fig. 4 / V.C", "Five calibration bins sum to 1,013 people and 67 events", bins_path,
          len(bins) == 5 and sum(int(r["people"]) for r in bins) == 1013 and sum(int(r["events"]) for r in bins) == 67)
    for index, r in enumerate(bins, 1):
        check("Fig. 4 / V.C", f"Bin {index}: {r['events']}/{r['people']}; mean prediction {float(r['mean_predicted']):.12g}", bins_path + f"; row={index}; all fields",
              math.isclose(int(r["events"]) / int(r["people"]), float(r["mean_observed"]), abs_tol=1e-14),
              "Observed proportion independently recomputed; mean prediction read from frozen aggregate.")

    coefficients_path = "output/phase5/apparent_coefficients.csv"
    coefficients = {r["term"]: r for r in csv_rows(coefficients_path)}
    for term, display in [("sex_female", (0.39, 0.23, 0.66)), ("school_below", (0.24, 0.13, 0.43))]:
        r = coefficients[term]
        beta, error = float(r["coefficient"]), float(r["std_error"])
        values = [math.exp(beta), math.exp(beta - 1.96 * error), math.exp(beta + 1.96 * error)]
        check("V.C / VI.B", f"{term} full-fit OR and Wald interval = {display}", coefficients_path + f"; term={term}; coefficient, std_error",
              tuple(round(v, 2) for v in values) == display,
              "Exponentiated retained full-cohort coefficients; not OOF effects, causal effects or direct burden measures.")
    check("V.C", "Age/place/office-distance full-fit Wald intervals include 1", coefficients_path,
          all(abs(float(coefficients[t]["coefficient"])) <= 1.96 * float(coefficients[t]["std_error"])
              for t in ["age_per_10", "settle_urban_informal", "settle_traditional_or_rural", "welfare_far"]))

    record_path = "output/runs/primary/run_record.json"
    record = read_json(record_path)
    check("III.D", "Five household-grouped folds; seed 201415; 1,000 fixed-prediction bootstrap draws", record_path + "; model_specification",
          record["model_specification"]["seed"] == 201415 and record["model_specification"]["bootstrap_draws"] == 1000 and
          "household" in record["model_specification"]["validation"],
          "Saved run settings checked; historical random fold assignment not regenerated.")
    check("Table VII", "Every retained metric interval has 1,000 valid and zero invalid resamples", intervals_path,
          all(int(r["valid_resamples"]) == 1000 and int(r["invalid_resamples"]) == 0 for r in intervals.values()))
    for name, historical_hash in record["output_sha256"].items():
        path = source("output/runs/primary/" + name)
        data = path.read_bytes()
        raw_hash = hashlib.sha256(data).hexdigest()
        normalized = hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()
        check("IV / reproducibility provenance", f"Historical run checksum: {name}", record_path + f"; output_sha256.{name}",
              historical_hash in {raw_hash, normalized},
              "Raw checksum matches." if raw_hash == historical_hash else
              "Historical hash uses CRLF; current tracked CSV uses LF. Both representations checked; current raw hash recorded separately.")

    manifest = read_json("models/manifest.json")
    evaluation = read_json("models/evaluation.json")
    check("III.B / IV", f"Rule {RULE}; model {MODEL}; six feature slopes", "models/manifest.json; rule_version, model_version, feature_order",
          manifest["rule_version"] == RULE and manifest["model_version"] == MODEL and len(manifest["feature_order"]) == 6)
    check("IV / V.D", "Model and held-out evaluation checksums match manifest", "models/manifest.json; artifact_sha256, evaluation_sha256",
          digest(source("models/logistic_model.json")) == manifest["artifact_sha256"] and
          digest(source("models/evaluation.json")) == manifest["evaluation_sha256"])
    check("IV / VI.C", "Frozen full-data scoring and pooled household-held-out evaluation have distinct contexts", "models/manifest.json; models/evaluation.json; score_context",
          "full-data" in manifest["score_context"] and "held-out" in evaluation["score_context"],
          "App scores are full-data fitted; this register does not relabel them as held-out/external performance.")
    for item in evaluation["provenance"]["sources"]:
        check("IV / provenance", f"Current evaluation source hash: {item['path']}", "models/evaluation.json; provenance.sources",
              digest(source(item["path"])) == item["sha256"])
    verification = manifest["verification"]
    check("V.D / Table IX", "Recorded JSON reload maximum difference 5.551115123125783e-17 over 1,013 rows", "models/manifest.json; verification",
          verification["verified_rows"] == 1013 and math.isclose(verification["prediction_reload_max_abs_difference"], 5.551115123125783e-17, rel_tol=1e-14),
          "Prior serialization evidence read; no estimator refitted or new inference parity run performed.", recorded=True)

    original_path = "output/phase8/evaluation_log.csv"
    original = csv_rows(original_path)
    extras = {"no_to_all_is_a_supported_zero", "source_reported_without_a_row_is_unresolved",
              "forbidden_predictor_is_rejected", "run_folder_person_and_flow_trace"}
    check("V.D / Table IX", "26 recorded passing checks = 22 synthetic screen + 2 schedule + 1 predictor + 1 trace", original_path,
          len(original) == 26 and all(r["passed"] == "True" for r in original) and
          len([r for r in original if r["case"] not in extras]) == 22 and extras.issubset({r["case"] for r in original}),
          "Recounted saved check log; original cases not rerun.", recorded=True)
    old_validation = read_json("docs/validation_summary.json")
    package = read_json("docs/local_package_validation.json")
    check("V.D / Table IX", "Prior full suite: 220 pass, zero fail/skip, 37.07 s", "docs/local_package_validation.json; tests, passed, failed, skipped, duration_seconds",
          package["tests"] == package["passed"] == 220 and package["failed"] == package["skipped"] == 0 and
          math.isclose(package["duration_seconds"], 37.07, rel_tol=0, abs_tol=1e-9),
          "Saved portability run, not freshly executed. Earlier 218-test run overlaps it; do not sum to 438.", recorded=True)
    parity = old_validation["reference_parity"]
    check("V.D / Table IX", "Prior native-UI/CLI parity: 15,388 matched, zero mismatches; 1,013 scores; 18 native tests", "docs/validation_summary.json; reference_parity, native_streamlit_tests",
          parity["rows"] == parity["matched"] == 15388 and parity["mismatched"] == 0 and parity["scored"] == 1013 and old_validation["native_streamlit_tests"] == 18,
          "Recorded application-path parity; retained output recount alone is not a fresh UI execution.", recorded=True)
    windows = read_json("docs/windows_validation.json")
    check("V.D / Table IX", "Prior owner Windows report audit: 50/50 checks on six files", "docs/windows_validation.json; files_checked, checks, passed, failed",
          windows["files_checked"] == 6 and windows["checks"] == windows["passed"] == 50 and windows["failed"] == 0 and
          len(windows["check_results"]) == 50 and all(windows["check_results"].values()),
          "Saved extracted-report audit; actual ZIP container and independent remote execution not verified.", recorded=True)
    supplied = read_json("examples/synthetic_report/audit_manifest.json")
    for filename, expected in supplied["output_sha256"].items():
        check("V.D / export provenance", f"Retained synthetic export checksum: {filename}", "examples/synthetic_report/audit_manifest.json; output_sha256",
              digest(source("examples/synthetic_report/" + filename)) == expected,
              "Fresh hash check of retained synthetic export, not regeneration or a new Windows run.")
    check("V.D / VI.C / VII", "Participant usability remains untested", "docs/validation_summary.json; human_usability_tested; manuscript",
          old_validation["human_usability_tested"] is False and participant_usability_unproven(text),
          "A stated limitation is required and common affirmative participant-testing claims are rejected. "
          "No recruited participants, task-time/error/ease observations or acceptance evidence; "
          "the phrase scan does not replace human review.")

    register("IV / V.D", "Two historical research runs: all 14 files byte-identical", "specification/phase7_artefact.md; Second run", "Yes: saved narrative record",
             "The earlier second-run record reports byte identity. Both historical run folders are not retained; no repeat run or fit was performed here.")
    source("specification/phase7_artefact.md")
    proposal = "21634436_Oluhle_Jawe_Submission_1.pdf"
    check("II.A / review provenance", "Submission 1 source PDF identity", proposal,
          digest(source(proposal)) == "6d6cac29f9a6d7cd07968f5ddb2ad2a38a69c82d19f208ae33f6c0cf2611fa32",
          "Identity with the supplied approved proposal is checked; this is not reproduction of review screening decisions.")
    limit("II.A", "Reported review flow: 511 −136 =375 −222 =153 −98 =55", proposal + "; II Literature Review / review selection narrative",
          "Counts are reported in Submission 1 and arithmetically consistent. Database exports, screening log and 55-source extraction log are not archived; not independently reproduced and not 55 OPG-only studies.", "Approved proposal; no new search")
    limit("VII", "DUT ethics approval/exemption status", "No institutional ethics determination in project record",
          "No approval, exemption or consent determination is documented; supervisor/official confirmation remains required.")
    limit("III.B / VII", "Historical legal provisions and current release/disclosure permission", "specification/phase3_cohort.md; paper/references.json; original government notices / licence conditions",
          "Research rule values are reproducible; this verifier does not independently authenticate the notices, establish statutory entitlement, or clear historical repository disclosure.")
    primary_sources = read_json("paper/primary_source_audit.json")
    limit("References / II / III.B", "Article claims and operative legal-notice provisions remain incompletely verified", "paper/primary_source_audit.json; overall_status, source_audits; paper/primary_source_audit.md",
          f"The retained primary-source audit dated {primary_sources['audit_date']} reports "
          f"{primary_sources['external_attempts']} external attempts and "
          f"{primary_sources['external_primary_texts_accessed']} remote primary texts accessed (HTTPS proxy 403). "
          f"{primary_sources['local_authentic_stats_sa_documents_read']} authentic local Stats SA documents were read. "
          "Its then-current 25-reference first-use check and 18 DOI-string matches establish "
          "citation/bibliographic consistency only; they do not authenticate article findings or "
          "the operative Annexure/R100/couple-threshold chain. This run reads that historical record "
          "and does not repeat publisher or legal-source access.",
          "Retained primary-source evidence audit; no fresh external verification")
    title_line = next((line for line in text.splitlines() if "ICT Honours" in line), "Title metadata not found")
    check("Title block", "Author-confirmed APRE402 module appears with student number 21634436", "Author confirmation in revision conversation; paper/manuscript.md; author/module line",
          "APRE402" in title_line and "21634436" in title_line,
          "The author confirmed APRE402 for this revision. This is not independent access to the university portal or its final-assignment instructions.", recorded=True)

    if digest(manuscript) != manuscript_hash:
        raise ValueError("Manuscript changed during verification; repeat after editing completes")
    failures = [c for c in comparisons + support if not c["passed"]]
    counts = {label: sum(c["table"] == label for c in comparisons) for label in ["IV", "V", "VI", "VII", "VIII"]}
    if counts != {"IV": 14, "V": 28, "VI": 112, "VII": 19, "VIII": 36}:
        raise ValueError(f"Unexpected table-comparison totals: {counts}")
    manuscript_name = str(manuscript.relative_to(ROOT)) if manuscript.is_relative_to(ROOT) else str(manuscript)
    common = {
        "status": "failed" if failures else "passed",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "manuscript_path": manuscript_name, "manuscript_sha256": manuscript_hash,
        "numeric_comparisons": len(comparisons), "passed": sum(c["passed"] for c in comparisons),
        "failed": sum(not c["passed"] for c in comparisons),
        "tables": {label: {"displayed_rows": len(table(label)), "numeric_comparisons": count} for label, count in counts.items()},
        "source_sha256": sources,
        "model_refitted": False, "application_tests_rerun": False,
        "manuscript_edited": False,
        "scope": "Read-only comparison and aggregate recalculation from retained evidence. Historical software runs are labelled as saved records; primary literature, legal, ethics, portal and review-log confirmation are not supplied by this audit.",
    }
    empirical = dict(common, supporting_checks={
        "independent_oof_auc_ap_brier_and_weighted_ratio": "passed" if not failures else "see failures",
        "independent_psu_approximation": "passed" if not failures else "see failures",
        "all_grouped_screen_scenarios_checked_separately": "passed" if not failures else "see failures",
        "unavailable_intercept_metrics_not_fabricated": "passed" if not failures else "see failures",
        "no_participant_usability_claim": "passed" if not failures else "see failures",
    }, substantive_issues=failures)
    full = dict(common, verifier="paper/verify_claims.py", verifier_sha256=digest(Path(__file__).resolve()),
                register="paper/claim_source_register.csv", register_rows=len(rows),
                supporting_comparisons=len(support), supporting_passed=sum(c["passed"] for c in support),
                supporting_failed=sum(not c["passed"] for c in support),
                limitations=limits, failures=failures, support_checks=support,
                numeric_checks=comparisons)
    return full, empirical, rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Save register and validation JSONs under paper/")
    parser.add_argument("--manuscript", type=Path, default=ROOT / "paper/manuscript.md")
    parser.add_argument("--expect-sha", help="Require this manuscript SHA-256 before verification")
    args = parser.parse_args()
    manuscript = args.manuscript.resolve()
    if args.expect_sha and digest(manuscript) != args.expect_sha:
        raise SystemExit("Manuscript SHA-256 does not match --expect-sha")
    full, empirical, rows = audit(manuscript)
    if args.write:
        for filename, result in [("claim_source_validation.json", full), ("empirical_expansion_validation.json", empirical)]:
            (ROOT / "paper" / filename).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=REGISTER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        (ROOT / "paper/claim_source_register.csv").write_text(stream.getvalue(), encoding="utf-8")
    print(json.dumps({"status": full["status"], "numeric_comparisons": full["numeric_comparisons"],
                      "numeric_failed": full["failed"], "supporting_comparisons": full["supporting_comparisons"],
                      "supporting_failed": full["supporting_failed"], "register_rows": len(rows),
                      "documented_limits": len(full["limitations"]), "model_refitted": False,
                      "application_tests_rerun": False, "manuscript_sha256": full["manuscript_sha256"]}, indent=2))
    return 0 if full["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
