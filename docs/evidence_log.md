# Implementation evidence log

## Phase 0 — 10 October 2026

Completed: inventory, phase 3/4/5 reproduction, primary CLI and phase 8 execution,
row-level cohort parity, floating-point result comparison, and model reconciliation.

Evidence: `tools/audit_baseline.py`, `docs/current_state_audit.md`,
`docs/model_decision_record.md`, `docs/baseline_reference.json`; private validation
artifacts in `.local/baseline/`. Five entry points exited 0; 15,388/15,388 rows
matched; all 29 numerical/text CSV comparisons passed; 26/26 existing checks passed.

Problems: CRLF-specific freeze; alternate bootstrap row order; archived
complete-case folds differ; no inference model or upload validator. Existing
documentation calls 26 mixed evaluation checks 26 synthetic decisions and has
minor stale model comments. These are recorded rather than silently rewritten.

Decision: freeze the current six-slope CLI/Phase 5 outputs as one result set.
Preserve the historical rule version and substantive methodology.

Next: Phase 1 reusable screening adapter, validated schema and tests.

## Phase 1 — 10 October 2026

Completed: strict normalized CSV contract, pure validation, thin screening
adapter, rulebook and data dictionary. The screen calls the original rule engine
and spouse-link resolver. Uploads do not change the research methodology.

Evidence: 85 schema/screen/parity tests passed; adding four reporting tests gives
89 passed in 14.47 seconds. All 15,388 reference rows match screen status,
receipt status, ordered reasons and outcome. The synthetic template exercises
all five required classifications plus age below the study frame.

Problems: a derived cohort export lacks raw grant inputs. The complete normalized
schema therefore requires source-derived person/grant fields and household
members for spouse context. Missing income is retained, not zero-filled. Truly
blank screening responses normalize to the existing unspecified code; predictor
missingness is handled separately.

Decision: use `opg-screen-v1`, restrict historical context/dates, reject duplicate
normalized keys before lookup, bound uploads at 20 MiB/50,000 rows, and keep
the below-60 category explicit. Reports omit original identifiers and income.

Next: freeze six-slope coefficients and fitted preprocessing, then verify
outcome-independent inference and reload parity before UI integration.

## Phase 2 — 10 October 2026

Completed: outcome-independent feature adapter, JSON coefficients with fitted
full-cohort preprocessing, model manifest, verified aggregate held-out evidence
and explicit offline build command. There is no executable pickle or upload-time fit.

Evidence: 99 prediction tests passed in 5.04 seconds. Across all 1,013 records,
reloaded scores matched the same in-memory full-data fitted model, maximum
absolute difference `5.551115123125783e-17`. Reference coefficients match within
`1e-10`. Artifact SHA-256:
`b39f36e2ea08b59c76243665b6eae571f2861a5a75d44cd657f170d62d6921b1`.
Repeating `tools/freeze_model.py` returned `reused` without fitting again.

Additional application-backend checks passed for invalid-input stopping,
synthetic upload repeatability/exports, and all 15,388 reference rows through
the actual CSV upload-to-report processing path, with 1,013 valid scores.

Problems: individual missing predictor codes need frozen imputation; rows with
all categorical predictors absent cannot support useful model scores and remain
unscored. Scoring never changes screening or observed receipt fields.

Decision: model `opg-kzn-six-slope-v1`; app scores are full-data fitted scores with
unknown training overlap, never held-out performance. Aggregate evaluation is
bound to the model manifest by checksum/version and remains a separate display.
New uncommitted training code is identified by file hashes alongside the baseline
commit, not falsely represented as already included in that commit.

Next: Streamlit upload, screening, prediction, filtering and audited downloads.

## Phases 3–4 — 10 October 2026

Completed: five-section Streamlit MVP, strict upload feedback, explicit analysis,
classification/reason summaries, fixed-model scores, filters, safe previews,
CSV/JSON/ZIP downloads and machine-readable audit manifests. Actual widget
download bytes match report contents and their hashes.

Evidence: final complete suite **218 passed, 0 failed, 0 skipped** in 34.11
seconds. This includes 18 native Streamlit AppTests, 107 model/inference tests,
86 schema/screen/reference tests, four report tests and three workflow tests.
Native full-reference upload compares all 15,388 records with CLI membership,
screen status, receipt, ordered reasons and outcome: **zero mismatches**.
The app scores the same 1,013 resolved passes and reports 67 non-recipients.
Synthetic reanalysis produces identical result/summary bytes. Invalid replacement,
removed uploads and repeated uploads clear old results, filters and exports.

The server was started, stopped and restarted using `tools/run_app.sh`.
After restart, loopback port 8501 returned HTTP 200 / `ok` at
`/_stcore/health` and HTTP 200 / Streamlit HTML at `/`. Startup requests alone
are not functional proof; the native upload-to-download tests provide that proof.

Final review found and closed a preprocessing provenance gap. Loading, cached
model scoring and evaluation reject changed/unreadable scientific or feature/
schema/screening code before feature preparation. Added eight targeted tests.
Runtime metadata records the integrity-guard change; estimator coefficients,
evaluation and original training/scientific hashes are unchanged. The offline
freeze command still returns `reused`, without fitting.

CSV extension is validated by the app before schema processing. The upload
transport is unrestricted because Streamlit's server deserializer can throw on
a wrong extension before the callback can clear prior state. Controlled rejection
now clears stale analysis and disables Run. This does not enable non-CSV analysis.

The complete saved environment install script ran successfully and passed
`pip check` plus frozen model/evaluation loading. `install_script` and
`start_skill` are saved as an environment draft; review/save and publication
remain user actions. Draft saving does not publish or prove restoration in a
new task.

Existing scientific source, requirements and research outputs are unchanged;
only `.gitignore` changed among pre-existing tracked files. New respondent-level
validation outputs are ignored; new fixtures/metadata contain no
survey respondent rows. See `docs/validation_summary.json` for aggregate evidence.

## Windows local package — 10 October 2026

Added `tools/run_app.py` as a cross-platform launcher and documented Windows
PowerShell installation without environment activation or execution-policy
changes. Added `tools/package_mvp.py` with an explicit allowlist: app/core,
three unchanged scientific modules, frozen JSON model/evaluation, requirements,
configuration, launchers and selected instructions. Raw datasets, historical
outputs, Git history and local caches are excluded. Archive contents preserve
the original bytes and carry SHA-256 checksums.

Fixed report generation when Git is not installed. Git metadata now remains
unknown (`null`) if the executable or repository is unavailable; application
source hashes remain available. Two end-to-end regression cases exercise
analysis, scoring and ZIP report checks without Git provenance. The complete
suite passed **220 tests, 0 failures, 0 skips** in 37.07 seconds.

The ZIP was extracted outside the repository and installed into a fresh Python
3.12 virtual environment using only its included requirements. Dependency
checks passed. Native Streamlit synthetic analysis, two frozen scores, all
result/model/export sections and report generation passed in the extracted
folder without Git history or survey data. The included Python launcher returned
HTTP 200 / `ok` and was stopped after verification. These automated package
checks ran on Linux; native Windows execution has not been observed here.
The earlier sandbox demonstration process was also stopped.

## User Windows verification — 11 October 2026

The user ran the downloaded MVP on Windows and supplied screenshots showing
successful validation, historical screening, model scoring and export controls.
They then supplied the six extracted report files for the built-in synthetic
example. The complete local workflow produced six classifications, two resolved
passes, one reported recipient, one reported non-recipient and two probabilities
of `0.18525299518191343`. Both synthetic summary proportions are 50%.

All **50 report verification checks passed**. All five output hashes match the
audit manifest; all five output files also match regenerated synthetic outputs
byte-for-byte. The dataset checksum agrees with the built-in synthetic input.
The eight recorded application source hashes, after normalizing Windows path
separators, agree with the packaged MVP, as do model checksum and version labels.
Summary CSV and JSON agree, and no active filter reduced the six-row report.

The verified originals are retained under `examples/synthetic_report/`, with
machine-readable aggregate evidence in `docs/windows_validation.json`.
The audit manifest remains unchanged: its Git fields record the original
research revision and a modified working tree at the time of the run. The user
supplied extracted files rather than the ZIP container. These checks establish
consistency with the known synthetic workflow, not remote execution attestation,
usability acceptance or external predictive validation.

For repository checkout portability, `.gitattributes` now retains LF Python,
shell and model JSON files and preserves the example reports without newline
conversion. This prevents Windows `core.autocrlf` settings from invalidating
frozen model/source checksums or altering the archived report hashes.

## Later phases — status before manuscript revision

Local controlled deployment is documented in `docs/deployment.md`. No public
site has been published. Optional raw-three-table upload remains outside this MVP.
No nontechnical participants have been tested: automated functional evidence
does not establish usability or user acceptance. The next research step is the
consented task protocol in `docs/usability_protocol.md`, followed by Submission 2
paper integration using these actual software/evaluation results. The paper has
not been rewritten or submitted by this implementation task.

## October plan Phase 6 — completed Submission 2 review draft, 11 October 2026

The user directed us to return to the plan and improve Submission 2 while
leaving participant usability testing out of the present revision. This is
Phase 6 (paper integration) of the October plan, distinct from September's
study Phase 6 (model sensitivities). The previous dated implementation entries
remain historical records.

Reporting changes strengthen the administrative-burden/access conceptual
mapping to measured predictors in `paper/conceptual_framework.md` and update
`paper/results.md` and `paper/discussion.md`. The revised manuscript was
assembled through `paper/manuscript.md` and `paper/build_ieee.js`. The
specification, current checklist and RQ3 traceability now identify the local
Streamlit implementation and its verified functional evidence.

The primary historical screening code, cohort, six-slope research result set,
OOF predictions, model artefact and sensitivity outputs are unchanged. No
scientific model is refit for this writing task. The research test claim is
corrected to **26 mixed checks: 22 synthetic screening cases, two schedule
checks, one structural leakage check and one run trace**. The application
evidence is separately **220 automated tests passed**, **15,388 reference
records matched with zero mismatches**, and **50 checks of the user's six
Windows synthetic report files passed**. Those counts are supported by the
preceding dated entries and machine-readable evidence; manuscript editing does
not itself constitute another test run.

No participant study, unaided task timings, ease ratings or acceptance results
are available. The prepared `docs/usability_protocol.md` remains a future
protocol. The revised paper must limit its usability statement accordingly;
the user's Windows walkthrough is local functional evidence. Public deployment
also remains optional and unperformed.

Decision D-061 records these reporting choices. The final revised
`paper/Jawe_OPG_nonreceipt_KZN.pdf` is **six Letter pages**, below the eight-page
limit, with two columns, 10 pt body text and 8 pt tables/references. It contains
**five tables, two figures and 23 references numbered by first use**. The
portable build ran after `npm ci` from the pinned lockfile. Final layout fixes
corrected cropped-figure paragraph spacing, kept tables together and balanced
the final columns. The read-only scientific audit passed **162 numerical table
checks**, preserving the frozen scientific outputs. See
`paper/manuscript_validation.json` for the recorded mechanical and numerical
build evidence. These checks do not constitute a fresh 220-test app-suite run.

Phase 6 manuscript integration is complete as a review draft. Independent
bibliographic/reference and official-notice verification remains outstanding;
mechanical citation numbering does not establish source validity. Ethics
approval is not documented in the project record. No participant usability
result or external submission is claimed. The previous four-page draft count
is retained only in its historical close-out.
