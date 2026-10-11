# Phase 0 — current state audit

Audit date: 10 October 2026 (Africa/Johannesburg). Source commit:
`110d84161ffb4ca1821c2c76318a6a13b27e2643`.

The uploaded Streamlit implementation plan is the roadmap for this task.
The existing Submission 1 PDF and research scripts define the substantive
screen and modelling method. No scientific method or existing result was changed.

## Inventory

At the start of this task Git was clean. The repository contained eight analysis
scripts, 68 output files, 13 archived completed-model files, 11 specification
documents, eight dataset/metadata files, and five paper files. It had no
Streamlit app, upload validator, independently packaged test suite, serialized
estimator, or complete inference manifest.

The three required primary survey CSVs are present. The optional
`LCS2015TOTALLCS.csv` is a Git LFS pointer, not the materialized data. It is not
required by phases 3–5 or the MVP. No extra credentials or services are needed.
Python 3.12.14 runs the pinned scientific dependencies, including pandas 3.0.6,
NumPy 2.5.3, statsmodels 0.15.0 and scikit-learn 1.9.1.

## Reproduction

Command: `/workspace/research-venv/bin/python tools/audit_baseline.py`.
This invokes the unchanged phase 3, 4 and 5 entry points, the primary CLI, and
phase 8. All five completed with exit code 0. Generated person-level outputs
stay in ignored `.local/baseline/`; the committed `output/` files are preserved.

The original Windows freeze hashes CRLF CSV serialization. The audit uses
`os.linesep = "\r\n"` before writing new CSVs, without replacing the expected
checksum. This exactly reproduces the frozen SHA-256
`50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`.
The LF checkout contains identical parsed values.

- All 15,388 KZN cohort rows match the reference, including reasons and outcomes.
- Older-adult frame: 1,317; known failures: 117; eligibility unresolved: 187.
- Final resolved cohort: 1,013 people, 827 households, 946 recipients and
  67 non-recipients.
- Non-receipt: 0.06614017769002961 unweighted and
  0.07487682625805854 person-weighted.
- All 29 CSV comparisons passed, using exact values for text and `1e-10`
  absolute/relative tolerance for floating-point values. Maximum observed
  absolute numerical difference was `5.551115123125783e-16`.
- All five retained-model validation folds converged.
- The existing evaluation ran 26 checks successfully: 22 synthetic screening
  cases, two schedule checks, one structural leakage check and one run trace.
  These are not 26 separate synthetic screening cases and do not test uploads.

Evidence: `.local/baseline/baseline_reference.json`,
`.local/baseline/numeric_parity.json`, and the aggregate reference in
`docs/baseline_reference.json`. Model reconciliation is in
`docs/model_decision_record.md`.

## Gaps and decisions

The normalized cohort export omits raw grant responses, so it cannot reconstruct
the screen on its own. The MVP will accept a documented, complete normalized
person schema with household/spouse context. It will distinguish a partial
uploaded dataset from reconstruction of the original study population.

Inference must not call training preparation requiring an outcome. The selected
six-slope model needs a fitted preprocessing record and frozen coefficients,
with reload parity evidence; uploads must never retrain it.

The existing repository already tracks respondent-level data and identifiers.
Ignoring new local outputs does not remove that history. This task provides a
controlled local app, synthetic examples and explicit safe export columns.
Public deployment or publishing this repository as a demo requires separate
data/licence and packaging review.

Phase 0 gate: **passed**. Next: strict schema validation, adapters that call the
existing rule engine, extended edge tests, and full baseline row parity.
