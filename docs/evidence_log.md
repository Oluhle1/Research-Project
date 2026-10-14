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

## October plan Phase 6 — earlier six-page Submission 2 review draft, 11 October 2026

This entry records the historical D-061 stage. D-062–D-066 below record later
historical builds; D-067 records the earlier supervisor point 1 draft. D-068
below records the current conceptual-framework follow-up. The
validation JSON is maintained for the latest build.

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

## Submission 1 integration — eight-page expansion, 11 October 2026

This D-062 entry records a historical build, including its word count and hashes.
The subsequent revision entries describe later builds.

The user authorized integrating the reuploaded Submission 1 into Submission 2
and expanding the paper to exactly eight pages with additional tables and
diagrams. The reuploaded source is byte-identical to the repository baseline
PDF, SHA-256
`6d6cac29f9a6d7cd07968f5ddb2ad2a38a69c82d19f208ae33f6c0cf2611fa32`.
The integrated manuscript restores the approved original title, aim, objectives
and review approach; earlier proposal/sample counts are attributed as context.
It expands literature comparisons and data operationalization, without changing
the frozen empirical cohort or substituting historical proposal counts for
observed results.

The final render copied to the tracked `paper/Jawe_OPG_nonreceipt_KZN.pdf`
passed the check for **exactly eight Letter pages**. The manuscript contains
**4,988 words** by whitespace splitting, with two columns, 10 pt body text,
**9 pt tables** and 8 pt
references. It contains
**nine tables, four figures and 25 references numbered by first use**.
The expansion adds literature comparisons, data-operationalization, weighted
descriptive-characteristics and performance-uncertainty tables, plus conceptual
framework and cohort-flow diagrams. The architecture and calibration figures
remain. The independent read-only scientific audit verified **all 209 numerical
table values**, comprising the previous 162 and 47 additional checks. These
numerical and final render/page-count checks are new verification for the
integrated manuscript, recorded in `paper/manuscript_validation.json`.

Decision D-062 records the expanded manuscript scope. The screening code,
frozen cohort, six-slope model, OOF predictions and sensitivity outputs remain
unchanged; no model refit was performed. The recorded **220 automated app
tests** and **50 Windows-report checks** were not rerun for the manuscript
expansion. Those inherited checks and the previous 15,388-record parity retain
their earlier documented functional scope and dates; they are distinct from
the new 209-value numerical audit and final eight-page render check.

Independent final visual review **passed all eight freshly rendered pages**;
the root agent also reviewed all eight. All nine tables and four figures are
legible and unclipped, captions are attached, and there are no blank pages or
orphan headings. The final reference page is naturally partial. A duplicated
Discussion paragraph was removed before this final render; the current
word count is 4,988. Final PDF SHA-256:
`0101c41c5332bc45def6f449ff5d5fbe88e86093adc88dfdf11e710b18548561`.

Participant usability is still unperformed by user instruction; independent
publisher/legal-notice
verification and ethics confirmation remain outstanding. The random forest
remains deferred and no new public deployment occurred. No external submission
is claimed. The prior six-page, five-table, two-figure, 23-reference stage is
preserved above as a historical record.

## Targeted Submission 2 revision — 11 October 2026

This D-063 entry records a historical build. Its 5,262-word count and recorded
hashes remain evidence for that stage, rather than the current manuscript.

Completed: P1–P4 of the supplied improvement plan, with deeper RQ discussion,
theory/proxy/findings synthesis, distinct predictive-metric interpretation and
screen/model sensitivity implications. APRE402 is confirmed by the user and
shown on the new title block. The approved original PDF remains unchanged.

Evidence: the final revised paper is eight Letter pages, 5,262 words, nine
tables, four figures and 25 first-use references. Root and an independent
reviewer inspected all eight fresh pages and found no layout blocker. The
314-row claim register and portable `paper/verify_claims.py` pass 209 numerical
table comparisons and 100 supporting checks. The verifier detects an altered
cohort count and abstract metric in a temporary copy. All scientific,
application/model, test, tool and dataset files remain unchanged from `3e3dacf`.
The previous 220 application tests, 15,388-record parity and 50 Windows checks
were verified as retained records, not re-executed.

Source checks: three authentic local Stats SA documents were read with page-
level evidence; thirteen publisher/index/government requests returned proxy
CONNECT 403 before original content was accessible. Eighteen DOI strings match
Submission 1, which does not authenticate the publications. Original journal
and historical legal verification remains incomplete, including the operative
formula/Annexure A, R100 minimum-payment and couple-resource provisions.

Decision: D-063. Improve interpretation and claim traceability within the frozen
study, while preserving participant-usability and external-validity limits.
`paper/targeted_revision_response.md` records P5 as partial. Ethics/access/
disclosure and official portal confirmation remain outstanding. No grade,
external submission or public deployment is claimed.

Final manuscript SHA-256:
`a0b1f20eb7f55a7a6eef63bbfb547860dd5cad2c1f8f8c8bf7bf6d7f6cafd852`.
Final PDF SHA-256:
`29eb71eb2b00763b1e30582a9b0cd6331d01c2e5732e999ca6f03bcc4b161e7b`.

## Plain-language Submission 2 revision — 13 October 2026

This D-064 entry records the historical 5,632-word build and its 263-word
abstract. D-065 below records the later professional-language revision;
the D-064 word count and source hash remain evidence for that earlier build.

The user asked for active verbs, parenthetical explanations of technical terms
at first use, “I” for the author and “you” when guiding the reader. Decision
D-064 records this reporting change. The rewritten manuscript keeps the
approved title, APRE402, the original research questions and all frozen results.
It simplifies prose, headings, table wording, captions and diagram labels.

The D-064 manuscript contains **5,632 whitespace-delimited words**, including
a **263-word abstract**. The rebuilt PDF has **eight US Letter pages**, with
**nine tables, four figures and 25 references**. The body, table and reference
fonts remain 10, 9 and 8 pt. Current render and layout evidence is recorded in
`paper/manuscript_validation.json`.

The portable retained-evidence audit passed **209 numerical table comparisons
and 100 supporting checks**, with zero failures. The 314-row source register
retains four explicit limitation rows. Temporary altered copies confirmed that
the verifier rejects an incorrect table count, an altered abstract AUC, a false
participant-usability claim and false Table IX evidence. These are manuscript
verification checks, not new application runs.

`paper/plain_language_revision.md` and `paper/plain_language_validation.json`
record the manual review of **90 essential terms and 16 scientific meanings**.
The review keeps apparent eligibility, reported receipt, predicted non-receipt
and legal entitlement separate. Editing diagnostics describe shorter sentences
and author/reader pronouns; they do not establish reader comprehension or human
usability. The D-064 manuscript SHA-256 is
`69b44ac75d1f4efb45d36cec4fa534b5cd53c7ffde17fc347e94c833a9cf9c93`.

Scientific, model, application, test, tool and dataset paths remain unchanged
from `bfabb350a8062cab7237a31c362afc4cc15196f4`. No model was fitted and no
application suite was rerun. The earlier **220 tests**, **15,388-record
agreement** and **50 Windows-report checks** retain their original scope and
dates. No participant study, new province analysis, publisher/legal-source read,
public deployment or external submission occurred. The earlier discussion of
other provinces remains brainstorming, not completed investigation.

P5 remains partial: original journal/legal authentication, ethics/access and
historical-data disclosure decisions, and official portal requirements are
still outstanding. The D-062 and D-063 word counts and SHA-256 values above
remain historical build records; the current audit files bind this revision to
its retained evidence.

## Professional-language Submission 2 revision — 13 October 2026

This D-065 entry records the historical 5,627-word build and its 249-word
abstract. D-066 below records the later historical specialist-audience revision;
the D-065 counts and source hash remain evidence for that earlier build.

The user requested clear, concise and scientifically sound language suitable
for conference review and ICT marking. Decision D-065 records the revision.
Concrete subjects, such as the pipeline, screen, model and app, now perform
the actions. Author and direct-address pronouns no longer appear in the
authored prose. Completed methods and observed results use past tense;
software behaviour, rules, tables and interpretation use present tense.
Proposed future work remains conditional. Technical explanations remain in
parentheses at first use, without returning to dense abstract phrasing.

The D-065 manuscript contains **5,627 whitespace-delimited words**, including
a **249-word abstract**. Its regenerated Word document and PDF retain the
approved title, APRE402 and research questions. The PDF has **eight US Letter
pages**, **nine tables, four figures and 25 references numbered by first use**.
Body, table and reference fonts remain 10, 9 and 8 pt. The root reviewer and
an independent reviewer inspected all eight fresh pages and passed the layout
review. `paper/manuscript_validation.json` records the current build evidence.
D-065 manuscript SHA-256:
`1f0080d9982dbe5a5d6b4f022b542341c343ca597338034fc714fd79a8f25df3`.

`paper/professional_language_revision.md` and
`paper/professional_language_validation.json` record the language review.
All **90 term checks and 16 scientific-meaning checks** passed. The retained-
evidence audit passed **209 numerical table comparisons and 100 supporting
checks**. Its **314-row register retains four explicit limitation rows**.
`paper/professional_language_negative_controls.json` records four rejected
temporary false-evidence variants. These checks establish manuscript
consistency; they do not measure participant comprehension or usability.

Scientific, model, application, dataset, reference, diagram and build-layout
paths remain unchanged from `e70b300895c9777067f5825abc25709b4a0e197d`.
No application suite ran and no model was refitted. Earlier 220-test,
15,388-record agreement and 50 Windows-report results remain dated functional
evidence. No participant study, other-province analysis, new primary-source
read, public deployment or external submission occurred.

P5 remains partial. Original journal and legal verification, institutional
ethics/access, historical-data disclosure and portal requirements remain
unconfirmed. Participant usability remains unperformed. D-062, D-063 and
D-064 retain their historical counts and hashes; the current audit files bind
D-065 to the regenerated paper and unchanged scientific evidence.

## Specialist-audience and integrated-literature revision — 13 October 2026

This D-066 entry records the historical 5,097-word build and its 141-word
abstract. D-067 below records the historical supervisor point 1 draft; the D-066
counts, hashes and completed checks remain evidence for the earlier build.
Its generated artifacts and audits remain in Git commit `e83b504`.

The user requested a more concise paper for specialist ICT and conference
readers, explicitly replacing the earlier requirement to define every technical
term. Decision D-066 records this scope. The revision removes **52 direct
elementary parenthetical glosses** and condenses the abstract, theory and metric-
definition paragraphs. It retains standard technical terminology, acronym
expansions, study-specific operational assumptions and interpretation of the
statistical measures. Concrete active subjects and appropriate tense remain.
The earlier 90-term definition review is historical, not a current acceptance
requirement.

The literature opening now presents one paper's research context rather than
referring to a separate proposal. It retains the recorded **511-to-55 review
flow**, identifies the included literature as covering mixed grants rather
than 55 OPG-only studies, and states that original search exports and screening
logs are unavailable for independent verification. This revision did not run
a new literature search or authenticate additional sources.

The D-066 manuscript has **5,097 whitespace-delimited words** and a
**141-word abstract**, **530 words fewer** than the D-065 build. The regenerated
PDF retains **eight US Letter pages**, **nine tables, four figures and 25
references numbered by first use**, with 10/9/8 pt body/table/reference fonts.
The approved title, APRE402, research questions, scientific results, figure
assets and build layout remain unchanged. Root and independent reviewers
passed all eight fresh pages. `paper/manuscript_validation.json` records the
current render and final layout-review evidence.
D-066 manuscript SHA-256:
`3dac12bcb9fd9ba60c05c64fa683a8e61e065b575c8c70a6e0a18f3fe8cd7ee3`.
D-066 PDF SHA-256:
`b81d1047e4c86e908267591f2ce831080e64c17ee12f7381b073ccf99d34d6d7`.

`paper/specialist_language_revision.md` and
`paper/specialist_language_validation.json` record the new language scope.
All **16 scientific-distinction checks** passed. The retained-evidence verifier
passed **209 numerical table comparisons and 100 supporting checks**, with
**314 register rows and four explicit limitations**. All four temporary
negative controls passed in `paper/specialist_language_negative_controls.json`.
The verifier itself remains unchanged. These manuscript reviews do not measure
reader comprehension or participant usability.

Scientific, application, dataset, model, reference, figure and build-layout
paths remain unchanged from `17e1b0536ec4f683d2a04e5caced2bb89635a943`.
No app suite, model refit, other-province analysis, participant study, new
primary-source query, deployment or external submission occurred. Earlier
220-test, 15,388-record agreement and 50 Windows-report results remain dated
functional evidence. P5 remains partial: original journal/legal verification,
institutional ethics/access, historical-data disclosure and portal requirements
remain unconfirmed. D-062–D-065 retain their historical counts and source hashes.

## Supervisor feedback point 1 — 14 October 2026

This D-067 entry records the historical 5,308-word draft at commit `1fe4820`.
The user subsequently reviewed it positively and requested the three framework
refinements recorded in D-068 below. Its counts and hash remain historical.

The user requested one correction at a time, with review and acceptance before
moving to the next. Decision D-067 records a draft response to point 1 only:
Section II.A now states the research gap and contribution relative to earlier
studies and explains the literature-search reproducibility limits. Points 2–10
remain pending; this entry does not mark the full supervisor feedback complete.

The revised review approach preserves the documented databases, search
concepts, broad relevance criteria and thematic narrative comparison. The
recorded 511-to-55 flow remains mixed-grant evidence. Database-specific queries,
search dates and filters, original exports, item-level screening/exclusion
decisions and the full 55-source extraction register are unavailable. The paper
therefore does not claim independently reproduced selection or exhaustive
literature coverage. No new search or source authentication occurred.

The contribution concerns this historical KZN workflow: transparent screening,
person-weighted description, household-held-out prediction and inspectable,
reproducible software. It does not establish universal novelty, legal
entitlement, causal barriers, participant usability or external performance.

The D-067 draft has **5,308 whitespace-delimited words**, a **141-word
abstract**, **eight US Letter pages**, **nine tables, four figures and 25
first-use references**, with unchanged 10/9/8 pt body/table/reference fonts.
Root and independent reviewers passed all eight final pages.
`paper/manuscript_validation.json` records the completed render and layout review.
Manuscript SHA-256:
`bf897e564f37e3d3dc19176a796eae3f8fea04c2392156dccf90163913e4e91a`.

`paper/supervisor_feedback_response.md` and
`paper/supervisor_point1_validation.json` record point 1's scope and evidence.
The retained-evidence verifier passes **209 numerical comparisons and 100
supporting checks**, with **314 register rows and four explicit limits**. Only
Section II.A prose changed from `e83b504fb124d6bf5f384a656f52ed2a7bd45a11`;
all other sections and table cells remain byte-identical. Scientific, app,
data, model, reference, diagram, build and verifier-code paths remain unchanged.
No new negative controls, application suite or model refit ran. Earlier
negative-control and 220-test, 15,388-record agreement and 50 Windows-report
checks remain historical records. No province extension, participant study,
primary-source query, deployment or external submission occurred.

D-062–D-066 retain their historical counts and hashes. The checklist remains
96 rows: 94 Implemented, two Proposed and zero Verified. P5 source, ethics,
access, disclosure and portal limits remain unchanged. At this stage, the
next step was user review of point 1 before point 2. D-068 records the later
positive review and authorised follow-up.

## Conceptual-framework follow-up — 14 October 2026

After positively reviewing point 1, the user requested three specific
refinements: a Conceptual Framework subsection, a refined conceptual diagram
and a discussion synthesis returning to the framework. D-068 records this
follow-up. It does not authorise applying all remaining supervisor comments.

Section II.D now contains a **142-word Conceptual Framework**. It connects OPG
non-receipt to administrative-burden theory, explains the observable screening
denominator, links survey proxies to theory and describes artefact implementation.
Figure 1 separates theoretical constructs, observable measurements, screen
status, reported receipt, weighted description and held-out prediction. Dashed
rationale arrows do not assert causal effects. A dashed enclosure identifies
the artefact's implementation scope; software is not another causal factor.
The diagram distinguishes frozen full-data upload scores from held-out research
evaluation and identifies receipt assessment for PASS adults.

Section VI.E adds a **109-word synthesis**. Screening sensitivity supports an
explicit denominator, and sex differences support demographic comparison,
without validating burden mechanisms. Schooling challenges a simple
information-barrier expectation; imprecise geographical associations leave
compliance-cost expectations unresolved. Psychological costs remain untested.
Traceable rules, outcomes and predictions support scrutiny despite these limits.

The current source contains **5,423 whitespace-delimited words**, a **141-word
abstract**, nine tables, four figures and 25 first-use references. The PDF has
**eight US Letter pages**, with unchanged 10/9/8 pt body/table/reference fonts
and build layout. Root and independent reviewers passed all eight final pages;
`paper/manuscript_validation.json` records the completed render and review.
Section II.D spans pages 2–3, Figure 1 appears on page 3 and VI.E appears on
page 8. Manuscript SHA-256:
`1fcaa1d081dbdabe3de4ed7e21ebc601a9a73b8adf3a81078a77b75bec654b49`.
PDF SHA-256:
`9a75be43b0f4f18ef9c0cb4b2aa3119cf9b0468e3cfeb69cdacbaef4506e5211`.

`paper/conceptual_framework_revision.md`,
`paper/conceptual_framework_validation.json` and
`paper/supervisor_feedback_response.md` record the response and scope.
Scientific and specialist-audience reviews pass. The retained-evidence audit
passes **209 numerical comparisons and 100 supporting checks**; its **314-row
register retains four explicit limits**. All table cells, Section II.A, methods,
software evaluation, numerical results, limitations, conclusion and references
remain unchanged from `1fe4820088603bf531cd55e9f2fe19cd420a0e99`.
The edits concern II.C/II.D, moved VI.B material and VI.E, Figure 1 and its
generator, working mirrors, reporting records and current audits. The other
three figures, app, model, data and verifier code remain unchanged.

No application suite, model refit, negative-control rerun, new source query,
province analysis, participant study, administrative confirmation, deployment
or external submission occurred. Prior functional checks remain historical;
participant usability and P5 source/governance limits remain open. Checklist
counts remain 96 rows: 94 Implemented, two Proposed and zero Verified.

The next step is user review of this follow-up. The framework aspect of
supervisor point 2 is addressed, but **Table II formatting remains pending**.
Supervisor points 3–10 remain pending. D-062–D-067 retain their original
counts and hashes; D-068 identifies the current manuscript.
