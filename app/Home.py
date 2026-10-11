"""Local research dashboard: validated upload, historical screen and frozen score."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from opg_core.inference import load_evaluation  # noqa: E402
from opg_core.reporting import NOTICE, build_report, safe_results  # noqa: E402
from opg_core.schema import COLUMNS, CONTEXT, SCHEMA_VERSION, ValidationResult, synthetic_template, validate_csv  # noqa: E402
from opg_core.screening import RULE_VERSION  # noqa: E402
from opg_core.workflow import process_upload  # noqa: E402

SECTIONS = ["Home / Study context", "Upload & validate", "Eligibility & receipt",
            "Prediction & model", "Export & reproducibility"]
CLASSIFICATION_LABELS = {
    "APPARENTLY_ELIGIBLE_REPORTED_RECEIPT": "Apparently eligible: reported receipt",
    "APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT": "Apparently eligible: reported non-receipt",
    "FAILED_OBSERVABLE_RULE": "Failed observable rule",
    "ELIGIBILITY_UNRESOLVED": "Eligibility unresolved",
    "RECEIPT_UNRESOLVED": "Receipt unresolved",
    "OUT_OF_STUDY_FRAME": "Outside the age-60+ study frame",
}
FILTER_KEYS = ("classification_filter", "screen_filter", "receipt_filter", "reason_filter")
ANALYSIS_KEYS = ("analysis_run", "run_failure", "export_reports", "export_signature", "filtered_results")


def clear_analysis() -> None:
    for key in (*ANALYSIS_KEYS, *FILTER_KEYS):
        st.session_state.pop(key, None)


def clear_source() -> None:
    clear_analysis()
    for key in ("source_bytes", "source_kind", "source_digest", "input_validation"):
        st.session_state.pop(key, None)


def set_source(content: bytes, kind: str, csv_extension: bool = True) -> None:
    clear_source()
    st.session_state.source_bytes = content
    st.session_state.source_kind = kind
    st.session_state.source_digest = hashlib.sha256(content).hexdigest()
    st.session_state.input_validation = (validate_csv(content) if csv_extension else
        ValidationResult(None, ["Upload must be a CSV file (.csv)."], [], ["file_type"]))


def load_example() -> None:
    content = synthetic_template().to_csv(index=False, lineterminator="\n").encode("utf-8")
    set_source(content, "synthetic")


def missingness(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate counts only; never preview submitted identifiers or amounts."""
    masks = {
        "age": frame["age"].isna(),
        "sex": frame["sex"].eq(""),
        "schooling_raw": frame["schooling_raw"].isin(["", "21", "22", "31", "32", "99"]),
        "settlement": frame["settlement"].eq(""),
        "welfare_distance": frame["welfare_distance"].isin(["", "9", "99"]),
        "private_income": frame["private_income"].isna(),
        "opg_income": frame["opg_income"].isna(),
    }
    return pd.DataFrame([{"field": field, "missing_rows": int(mask.sum())}
                         for field, mask in masks.items()])


def validation_feedback(validation) -> None:
    if validation is None:
        st.info("Choose a supported CSV or the synthetic example, then review its validation.")
        return
    for message in validation.errors:
        st.error(message)
    for message in validation.warnings:
        st.warning(message)
    st.caption("Checks performed: " + ", ".join(validation.checks))
    if not validation.errors:
        st.success(f"Schema validation passed for {len(validation.frame):,} rows. Select Run analysis to screen and score.")
        st.subheader("Missingness before analysis")
        st.dataframe(missingness(validation.frame), hide_index=True, width="stretch")
        st.caption("Counts refer to uploaded rows. Missing income stays missing; model imputation uses frozen training statistics.")


def filter_results(safe: pd.DataFrame) -> pd.DataFrame:
    """Filter an allowlisted table while preserving its original research IDs."""
    filtered = safe.copy()
    st.sidebar.subheader("Result filters")
    for label, column, key in (
        ("Classification", "classification", "classification_filter"),
        ("Observable screen", "screen_status", "screen_filter"),
        ("Reported receipt", "receipt_status", "receipt_filter"),
    ):
        values = sorted(safe[column].unique().tolist())
        formatter = (lambda value: CLASSIFICATION_LABELS.get(value, value)) if column == "classification" else str
        selected = st.sidebar.multiselect(label, values, key=key, format_func=formatter,
                                         help="Leave empty to include all categories.")
        if selected:
            filtered = filtered[filtered[column].isin(selected)]
    reasons = sorted({code for codes in safe["reason_codes"] for code in codes.split("|") if code})
    selected_reasons = st.sidebar.multiselect("Reason code", reasons, key="reason_filter",
                                             help="A record matches if it contains any selected reason.")
    if selected_reasons:
        filtered = filtered[filtered["reason_codes"].map(
            lambda codes: bool(set(codes.split("|")) & set(selected_reasons)))]
    return filtered


def rate(value) -> str:
    return "Unavailable" if value is None else f"{100 * value:.1f}%"


def eligibility_page(run, safe: pd.DataFrame, filtered: pd.DataFrame) -> None:
    value = run.summary
    st.header("Eligibility & reported receipt")
    st.caption(value["scope"])
    cards = st.columns(4)
    cards[0].metric("Uploaded rows", f"{value['uploaded_rows']:,}")
    cards[1].metric("Resolved-pass denominator", f"{value['resolved_pass_denominator']:,}")
    cards[2].metric("Reported recipients", f"{value['reported_recipients']:,}")
    cards[3].metric("Reported non-recipients", f"{value['reported_nonrecipients']:,}")
    rates = st.columns(2)
    rates[0].metric("Unweighted non-receipt", rate(value["unweighted_nonreceipt_rate"]))
    rates[1].metric("Person-weighted non-receipt", rate(value["person_weighted_nonreceipt_rate"]))
    st.caption("Both proportions use all uploaded records that PASS the observable screen and have resolved reported receipt. The weighted rate uses supplied person weights; no new survey uncertainty estimate is calculated. Filters do not change these denominators.")
    st.subheader("Classification breakdown — all uploaded rows")
    counts = safe["classification"].value_counts().rename_axis("classification").reset_index(name="rows")
    counts["classification"] = counts["classification"].map(CLASSIFICATION_LABELS)
    st.dataframe(counts, hide_index=True, width="stretch")
    st.subheader("Reason codes — all uploaded rows")
    reasons = safe["reason_codes"].str.split("|").explode()
    st.dataframe(reasons.value_counts().rename_axis("reason_code").reset_index(name="rows"),
                 hide_index=True, width="stretch")
    st.caption("A record can have several reason codes. FAIL denotes a failed observable research rule; unresolved is retained explicitly.")
    st.subheader("Inspectable results")
    st.caption(f"Showing {len(filtered):,} of {len(safe):,} uploaded rows. Research IDs are generated row labels and do not encode submitted identifiers.")
    st.dataframe(filtered, hide_index=True, width="stretch")


def prediction_page(run, filtered: pd.DataFrame) -> None:
    st.header("Prediction & frozen model")
    st.subheader("Uploaded record scores")
    st.warning("These are frozen full-data fitted scores. Training overlap is unknown, so they are not held-out performance or external validation. Probability estimates reported non-receipt; it never changes screening or observed receipt.")
    st.caption("Only the resolved apparently eligible cohort is supported for scoring. Partially missing predictors use frozen training preprocessing; records with all categorical predictors missing remain unscored.")
    probabilities = filtered["predicted_nonreceipt"].dropna().astype(float)
    st.metric("Scored records in current filter", f"{len(probabilities):,}")
    if len(probabilities):
        counts, edges = np.histogram(probabilities, bins=np.linspace(0, 1, 11))
        histogram = pd.DataFrame({"probability": [f"{edges[i]:.1f}–{edges[i + 1]:.1f}" for i in range(10)], "records": counts})
        st.bar_chart(histogram, x="probability", y="records")
        st.subheader("Highest model probabilities in current filter")
        top = filtered[filtered["predicted_nonreceipt"].notna()].sort_values("predicted_nonreceipt", ascending=False).head(10)
        st.dataframe(top, hide_index=True, width="stretch")
        st.caption("This ranking describes model output for research inspection and does not establish need, legal eligibility or reasons for non-receipt.")
    else:
        st.info("No records in the current filter can be scored. The result table retains each unscored explanation.")
    st.subheader("Frozen held-out research evaluation")
    try:
        evidence = load_evaluation()
    except Exception:
        st.error("The verified aggregate evaluation is unavailable. Check the local frozen model files before using this page.")
        return
    cohort = evidence["cohort"]
    st.caption(f"Saved household-grouped held-out evaluation: {cohort['people']:,} people, {cohort['households']:,} households, {cohort['events']:,} reported non-recipients. This evidence is fixed and is never recomputed from an upload.")
    metrics = pd.DataFrame(evidence["metrics"]).rename(columns={
        "logistic_out_of_fold": "Frozen logistic OOF", "intercept_only_out_of_fold": "Intercept-only OOF"})
    st.dataframe(metrics, width="stretch")
    st.caption("Unavailable comparator metrics remain blank; they are not replaced by uploaded-data estimates.")
    st.subheader("Saved uncertainty intervals")
    st.dataframe(pd.DataFrame(evidence["bootstrap"]["intervals"]), hide_index=True, width="stretch")
    st.caption(evidence["bootstrap"]["method"])
    bins = pd.DataFrame(evidence["calibration_bins"])
    st.subheader("Held-out calibration")
    st.scatter_chart(bins, x="mean_predicted", y="mean_observed")
    st.dataframe(bins, hide_index=True, width="stretch")
    st.caption("Predicted and observed rates are aggregated into the retained research calibration bins.")
    manifest = run.model_manifest
    st.subheader("Model version and predictors")
    st.write("Model: " + manifest["model_version"])
    st.write("Rule: " + manifest["rule_version"])
    st.write("Predictors: age, sex, schooling, settlement and welfare-office distance; six fitted slopes.")
    st.caption("Small event count, historical survey responses and unmeasured eligibility conditions limit interpretation. Associations are not causes of non-receipt.")


def export_page(run, filtered: pd.DataFrame) -> None:
    st.header("Export & reproducibility")
    filtered_ids = tuple(filtered["research_id"])
    signature = (id(run), filtered_ids)
    if st.session_state.get("export_signature") != signature:
        st.session_state.export_reports = build_report(
            run.results, st.session_state.source_bytes, run.validation,
            run.model_manifest, filtered_ids=list(filtered_ids))
        st.session_state.export_signature = signature
    reports = st.session_state.export_reports
    st.caption(f"Full report: {len(run.results):,} uploaded rows. Filtered report: {len(filtered):,} rows. Summary proportions always use the full resolved-pass denominator.")
    st.write("Results contain generated research IDs, screen and receipt categories, reason codes, supported probabilities and rule/model versions. Original IDs, household pointers and raw income are omitted.")
    for name, label, mime in (
        ("results.csv", "Download all results CSV", "text/csv"),
        ("filtered_results.csv", "Download filtered results CSV", "text/csv"),
        ("summary.csv", "Download summary CSV", "text/csv"),
        ("summary.json", "Download summary JSON", "application/json"),
        ("audit_manifest.json", "Download audit manifest", "application/json"),
        ("report.zip", "Download complete report ZIP", "application/zip"),
    ):
        st.download_button(label, reports[name], file_name=name, mime=mime,
                           key="download_" + name, on_click="ignore")
    st.subheader("Reproducibility information")
    st.write(f"Upload schema: {SCHEMA_VERSION}; historical screen: {RULE_VERSION}; model: {run.model_manifest['model_version']}.")
    st.caption("The manifest records input/output hashes, validation checks and warnings, dependency versions, source commit, working-tree status and a timestamp in Africa/Johannesburg. Run timestamps change; scientific result bytes are deterministic for identical inputs and versions.")
    st.info("Uploads and reports stay in this Streamlit session's memory; the app does not persist uploads to disk. Use synthetic records for shared demonstrations. Participant usability testing and public deployment have not been conducted here.")


st.set_page_config(page_title="OPG research prototype", page_icon="🔎", layout="wide")
st.title("OPG screening & non-receipt research")
st.info(NOTICE)
st.sidebar.title("Research workflow")
section = st.sidebar.radio("Section", SECTIONS, key="section")
uploaded = st.sidebar.file_uploader("Supported research CSV",
                                    key="research_upload", on_change=clear_source,
                                    help="UTF-8 normalized LCS KZN 2014/2015 schema; 20 MiB / 50,000 rows maximum.")
if uploaded is not None:
    content = uploaded.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    if st.session_state.get("source_digest") != digest or st.session_state.get("source_kind") != "upload":
        set_source(content, "upload", csv_extension=Path(uploaded.name).suffix.lower() == ".csv")
template = synthetic_template().to_csv(index=False, lineterminator="\n").encode("utf-8")
st.sidebar.download_button("Download synthetic template", template,
                           file_name="opg_synthetic_template.csv", mime="text/csv",
                           key="synthetic_template", on_click="ignore")
st.sidebar.button("Use synthetic example", key="load_example", on_click=load_example,
                  disabled=uploaded is not None, help="Remove any uploaded file before selecting the built-in invented example.")
validation = st.session_state.get("input_validation")
valid_input = validation is not None and not validation.errors
if st.session_state.get("source_kind") == "synthetic":
    st.sidebar.caption("Synthetic example — invented records")
if valid_input:
    st.sidebar.success(f"Validated: {len(validation.frame):,} rows")
elif validation is not None:
    st.sidebar.error("Input rejected. Review Upload & validate.")
if st.sidebar.button("Run analysis", key="run_analysis", type="primary", disabled=not valid_input):
    for key in ANALYSIS_KEYS:
        st.session_state.pop(key, None)
    try:
        with st.spinner("Applying historical rules and the frozen research model…"):
            run = process_upload(st.session_state.source_bytes)
        if run.results is not None:
            st.session_state.analysis_run = run
        else:
            st.session_state.input_validation = run.validation
    except Exception:
        st.session_state.run_failure = "Analysis could not complete. Check the supported CSV format and local frozen model files."
if st.session_state.get("run_failure"):
    st.error(st.session_state.run_failure)
run = st.session_state.get("analysis_run")
safe = safe_results(run.results) if run is not None else None
filtered = filter_results(safe) if safe is not None else None
if filtered is not None:
    st.session_state.filtered_results = filtered

if section == SECTIONS[0]:
    st.header("Study context")
    st.write("This local prototype examines reported Older Person's Grant non-receipt among apparently eligible adults aged 60+ in KwaZulu-Natal using the historical Living Conditions Survey 2014/2015.")
    columns = st.columns(3)
    columns[0].subheader("Observable screening")
    columns[0].write("Historical research rules produce PASS, FAIL or UNRESOLVED with reason codes. Survey data do not observe every statutory condition.")
    columns[1].subheader("Reported receipt")
    columns[1].write("Survey responses identify reported receipt, non-receipt or an unresolved response separately from the screen.")
    columns[2].subheader("Model probability")
    columns[2].write("A frozen logistic model estimates reported non-receipt for the supported resolved cohort. A score does not determine screening or actual receipt.")
    st.subheader("Use the prototype")
    st.write("1. Download and upload the synthetic template, or select Use synthetic example.\n2. Review Upload & validate, then select Run analysis.\n3. Inspect Eligibility & receipt and Prediction & model.\n4. Apply result filters and download the report in Export & reproducibility.")
    st.caption("Schema " + SCHEMA_VERSION + " · context " + CONTEXT + " · rule " + RULE_VERSION)
elif section == SECTIONS[1]:
    st.header("Upload & validate")
    st.write("Use the exact normalized research schema. Include household members needed for resident spouse linkage, even when they are under 60. An upload containing only the final cohort cannot reconstruct the full older-adult frame.")
    with st.expander("Required columns and accepted contract"):
        st.write(", ".join(COLUMNS))
        st.write("The version and context must match the synthetic template. Coding and missing-value rules are documented in docs/data_dictionary.md. Unknown columns/codes, duplicates and inconsistent income schedules block analysis.")
    validation_feedback(validation)
    if safe is not None:
        st.subheader("Safe result preview")
        st.dataframe(safe.head(20), hide_index=True, width="stretch")
elif run is None:
    st.info("Upload a supported CSV, review validation and select Run analysis to inspect or export results.")
elif section == SECTIONS[2]:
    eligibility_page(run, safe, filtered)
elif section == SECTIONS[3]:
    prediction_page(run, filtered)
else:
    export_page(run, filtered)
