# Methodology checklist

**Source:** Submission 1 (`21634436_Oluhle_Jawe_Submission_1.pdf`), Sections II–VII and Figures 1–2 and Table I.  
**Process constraints** from `Agent.md` are included only where they restate that design or require a record of it.  
**Created:** 2026-09-25; current evidence update: 2026-10-15 (Africa/Johannesburg).

**Rule:** status changes only when the named evidence exists. Phase 1 originally set every row to Proposed; this table records current implementation evidence.

Statuses: **Proposed** / **Implemented** / **Verified**.

## A. Study definition

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| A1 | Aim | Interpretable artefact for reported OPG non-receipt among apparently eligible adults aged 60+ in KwaZulu-Natal, LCS 2014/2015 | Implemented | Aim retained in the existing paper and current manuscript sources; `README.md` |
| A2 | RQ1 | Proportion reporting non-receipt, and change under alternative eligibility assumptions | Implemented | `output/phase4/rq1_estimate.csv` and `rq1_sensitivity.csv`; `paper/results.md` |
| A3 | RQ2 | Discrimination and probability estimates from a small logistic model in held-out households | Implemented | `output/runs/primary/metrics.csv` and calibration display; `docs/model_decision_record.md` |
| A4 | RQ3 | Artefact reproduces the analysis and explains screening decisions and model outputs | Implemented | `docs/validation_summary.json`, `docs/windows_validation.json`, reason-coded app/report outputs; no participant clarity claim |
| A5 | Objectives | Person-level population; weighted description; internally validated parsimonious model; artefact correctness, reproducibility, clarity | Implemented | Phases 3, 4, 5, and 8 outputs and `docs/evidence_log.md`; participant usability remains untested |
| A6 | Apparently eligible | Passes observable screening rules. Not confirmed legal eligibility. Not an official grant decision | Implemented | `docs/rulebook.md`, app notice and exported responsible-use note; no legal-eligibility flag |
| A7 | Unit of analysis | Person. Household is context, linkage, and grouping, not the outcome | Implemented | Frozen `cohort_person.csv`; `output/phase2/join_audit.csv` shows no duplicated person key |
| A8 | Study population | Adults aged 60+ in sampled KwaZulu-Natal households. Institutionalised older adults are outside coverage | Implemented | `output/phase3/cohort_flow.csv`; coverage limitation retained in paper |

## B. Data linkage

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| B1 | Files | Person, household, and person-income files, plus metadata, questionnaire, and COICOP codes | Implemented | `specification/variable_mapping.md` |
| B2 | Identifiers | Link on documented household and person identifiers | Implemented | `output/phase2/join_audit.csv`: 0 duplicate person keys, 0 unmatched households |
| B3 | Income aggregation | COICOP classification; aggregate to the person; use released annualised values once | Implemented | `analysis/phase3_build_cohort.py`, `specification/variable_mapping.md` and frozen cohort proxies |
| B4 | Join audit | Duplicate person keys, unmatched records, unexpected row-count changes | Implemented | `specification/phase2_data_audit.md` |
| B5 | No silent substitution | A concept that cannot be built is reported. Replacement needs a decision-log entry | Implemented | Mapping Section 9; decision log D-029 and D-030 |
| B6 | Assets | Asset acquisitions are not treated as a full assessable asset stock | Implemented | Decisions D-030 and D-040; no asset-stock exclusion in the primary rule engine |
| B7 | Household totals | Not allocated to individual applicants | Implemented | Decision D-030; `analysis/phase3_build_cohort.py` uses person-attributable income |

## C. Eligibility and outcome

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| C1 | Screen frozen first | Thresholds, boundary, and partnership treatment finalised and versioned before any predictive metric is examined | Implemented | Decisions D-033 to D-039; rule version `opg-kzn-primary-v1` |
| C2 | Age frame | 60 and older. Missing age and age under 60 stay out of the frame and are counted | Implemented | `output/phase3/cohort_flow.csv` |
| C3 | Married spouse link | Spouse identifier within household; linked person exists; relationship consistent | Implemented | Rule checks in `analysis/phase3_build_cohort.py`; spouse reasons in `reason_frequencies.csv` |
| C4 | Missing or non-resident spouse | Unresolved income screen. Single-person threshold not applied | Implemented | Rule check; 81 `UNRES_SPOUSE_NONRESIDENT` in the age-60 frame |
| C5 | Ambiguous partnership | Conservative primary treatment (unresolved). Alternatives only in named sensitivities | Implemented | Primary rule D-037; S2a–S2d already run in `output/phase4/rq1_sensitivity.csv` |
| C6 | Resource proxy | Annual nominal income of applicant and, where applicable, spouse; social-assistance income excluded | Implemented | Proxy columns on `cohort_person.csv`. Leakage test remains G-a7 |
| C7 | Absent income | Not treated as zero unless the logged release convention supports zero | Implemented | Rule checks; 28 supported zeros and 7 unresolved absences in the age-60 frame |
| C8 | Incompatible grants | Own disability grant and own war-veterans grant excluded on the primary screen and flagged separately | Implemented | 25 disability exclusions; war-veterans exclusion coded and excludes nobody |
| C9 | Grants that do not exclude | Caregiver-linked child grants and grant-in-aid | Implemented | Rule checks; flag counts in `reason_frequencies.csv` |
| C10 | Status and reasons | Every person has PASS, FAIL, or UNRESOLVED, plus reason codes. Known FAIL takes precedence over unresolved items. All reasons retained | Implemented | Cohort file and the rule check that keeps both a fail and an unresolved reason |
| C11 | Outcome | Y = 1 non-receipt, Y = 0 receipt, among PASS with a resolved response | Implemented | 946 recipients and 67 non-recipients reconcile to 1,013 passes |
| C12 | Skip-aware grant items | General social-grant question and OPG item read together. Consistent report of no grant can be Y = 1 | Implemented | Rule check for Q4.1a = No with the OPG item not applicable |
| C13 | Contradictions and unexplained missing | Outcome unresolved; not coded as non-receipt; not in the primary model | Implemented | Rule check; 0 unresolved outcomes in this release’s pass group |
| C14 | Caregiver CSG | Does not determine the OPG label | Implemented | Rule check: caregiver flag with Y = 1 |
| C15 | Receipt-period flag | Current receipt compared with preceding-year OPG income. Disagreement does not change the primary label | Implemented | Flag coded, with 0 disagreements among 1,013 resolved passes; S5 already run in `output/phase4/rq1_sensitivity.csv` |
| C16 | Final cohort | PASS and resolved outcome only | Implemented | `output/phase3/cohort_flow.csv` |
| C17 | Cohort frozen | Primary person file written once and hashed before modelling | Implemented | `output/phase3/cohort_freeze.json`, sha256 `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2` |

## D. RQ1 description

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| D1 | Unweighted proportion | Non-recipients / resolved outcomes in the screened population | Implemented | `output/phase4/rq1_estimate.csv`: 67/1,013 |
| D2 | Weighted proportion | Σ(wᵢ Yᵢ) / Σ wᵢ with released person weights | Implemented | Same file; weight is `Persns_wgt` |
| D3 | Characteristics | Recipients and non-recipients on the Table I variables; unweighted counts and weighted summaries | Implemented | `output/phase4/rq1_characteristics.csv` |
| D4 | Design variance | Use strata and PSU if present. If absent, weighted figures stay point estimates and any approximation is named | Implemented | Strata absent. Named PSU-cluster approximation in the estimate file |
| D5 | Outcome bounds | Assign unresolved PASS outcomes to receipt, then to non-receipt | Implemented | Bounds in `rq1_estimate.csv`. Unresolved PASS outcomes: 0 |
| D6 | Non-causal reading | Descriptive differences are not effects | Implemented | `specification/phase4_rq1.md` states the description is not an effect |

## E. RQ2 model

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| E1 | Table I age | Linear, per 10 years above 60 | Implemented | `analysis/phase5_model.py` column `age_per_10` |
| E2 | Table I sex | Male and female, 1 df | Implemented | Female indicator, male reference, D-049 |
| E3 | Table I schooling | Below Grade 7 versus Grade 7 or above, 1 df | Implemented | `school_below`, Grade 7 or above as reference |
| E4 | Table I settlement | Four documented categories, 3 df | Implemented | Four categories exist. Rural formal is merged with traditional area in the retained model, D-052 |
| E5 | Table I welfare access | At least 5 km or unavailable, versus nearer, 1 df | Implemented | Missing distance is imputed; code 8 stays in the far-or-unavailable class |
| E6 | Intercept + 7 slopes | No additional primary coefficient. Marital status is not a primary predictor | Implemented | Seven-slope attempt archived. Retained model has six slopes and no marital coefficient |
| E7 | No stepwise selection | Specification fixed, or simplified only by a logged feasibility revision | Implemented | D-052 |
| E8 | Feasibility gate | Cohort size, events, households, category frequencies, fold support, separation, convergence | Implemented | `output/phase5/feasibility.json` and `fold_support.csv` |
| E9 | Simplification rule | If unsupported, a smaller model is logged. The original proposal remains recorded | Implemented | D-052 and `output/phase5/table_i_attempt/` |
| E10 | Imputation | Training-fold median (continuous) and mode (categorical). Structural skips interpreted first. Eligibility and outcome not imputed | Implemented | `fold_imputers.csv`; isolation check in the script |
| E11 | Complete cases | Sensitivity only | Implemented | `output/phase6/model_sensitivity.csv`, S7: 992 people, 63 events |
| E12 | Estimator | Unweighted logistic regression. No class balancing or oversampling | Implemented | `run_record.json` |
| E13 | Weighted fitting | Sensitivity only | Implemented | `output/phase6/model_sensitivity.csv`, S9; frequency-weighted fit documented in D-054 |
| E14 | CV | Five-fold, stratified, grouped by household. Same household never split. Approximate outcome balance | Implemented | `fold_support.csv`; script stops if a household is split |
| E15 | Mixed-household label | Proposed default: household is positive if any member has Y = 1. Adopt or revise before fitting | Implemented | D-050. Six mixed households |
| E16 | Empty class in a fold | Review the validation plan; do not drop the fold silently | Implemented | Every retained fold has 12 to 14 events |
| E17 | Held-out predictions | One prediction per final-cohort person from a model that did not train on their household | Implemented | `oof_predictions.csv`, 1,013 rows |
| E18 | PSU grouping | Sensitivity if PSU exists | Implemented | `output/phase6/model_sensitivity.csv`, S11; 345 derived sampling units |
| E19 | Average precision | Reported beside prevalence | Implemented | 0.203 beside prevalence 0.066 |
| E20 | ROC AUC | Complementary discrimination metric | Implemented | 0.752 |
| E21 | Brier score | Probability error | Implemented | 0.058 |
| E22 | Calibration-in-the-large | Slope fixed at 1 | Implemented | 0.020 |
| E23 | Calibration slope | Intercept free | Implemented | 0.836 |
| E24 | Calibration plot | Predeclared binning or smoothing | Implemented | `calibration_plot.png`; five quantile bins |
| E25 | Intercept-only reference | Training-fold prevalence, same folds, compared on probability error | Implemented | Brier 0.062 against the model’s 0.058 |
| E26 | Primary metrics unweighted | Weighted metrics reported separately | Implemented | Third row of `metrics.csv`, labelled as weighted metrics |
| E27 | Household resampling | Uncertainty for the fixed prediction set. No refit inside the resample | Implemented | `bootstrap_intervals.csv`, 1,000 draws, 0 invalid |
| E28 | No decision threshold | Probabilities only. No operating-point selection for grant decisions | Implemented | No threshold in the metrics or the report |

## F. Sensitivity programme

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| F1 | S1 thresholds | Alternative income thresholds, each identified as an assumption when simplified | Implemented | `output/phase4/rq1_sensitivity.csv` rows S1a–S1d |
| F2 | S2 partner resources | Alternative partnership treatment | Implemented | Same file, rows S2a–S2d |
| F3 | S3 grant compatibility | Retain own disability and war-veterans records | Implemented | Same file, row S3 |
| F4 | S4 income definition | Documented alternative income definition | Implemented | Same file, rows S4a–S4c |
| F5 | S5 receipt period | Current receipt versus preceding-year OPG income | Implemented | Same file, row S5. Disagreements in the pass group: 0 |
| F6 | S6 outcome bounds | Covered also as D5 | Implemented | Same file, rows S6a–S6b |
| F7 | S7 complete cases | Predictor missingness | Implemented | `output/phase6/model_sensitivity.csv` row S7: 992 people, 63 events |
| F8 | S8 partnered status | Replaces welfare access; slope count unchanged | Implemented | Row S8. Married indicator, six slopes, D-053 |
| F9 | S9 weighted model | Separate from the primary fit | Implemented | Row S9, labelled as a weighted fit |
| F10 | S10 weighted metrics | On the primary predictions | Implemented | Row S10 and the Phase 5 weighted metrics row |
| F11 | S11 PSU CV | Only if PSU exists | Implemented | Row S11. Derived PSU, 345 units |
| F12 | Separate storage | Sensitivity results are not written over primary results | Implemented | `output/phase6/` is separate from `output/phase5/` |
| F13 | Random forest | Secondary. After logistic validation, sensitivities, and artefact evaluation. Same rows, predictors, and outer folds. Tuning only inside training. Skip is allowed | Proposed | Either a secondary report or a logged decision not to run |

## G. Artefact and RQ3

| ID | Component | Approved content | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| G-a1 | Pipeline order | Raw files → validation and linkage → rule engine → cohort → description → prediction → outputs | Implemented | `python analysis/run_study.py` |
| G-a2 | Rule version on every output | Scenario, survey period, rule version, model specification | Implemented | `output/runs/primary/run_record.json` |
| G-a3 | Reproducibility record | Checksums, variable mapping, software versions, seed, fold ids | Implemented | Same run record; fold ids are in `oof_predictions.csv` |
| G-a4 | CLI is the MVP path | Streamlit is secondary and waits until the core artefact works | Implemented | Original CLI preserved; Streamlit added after baseline reproduction, documented in `docs/evidence_log.md` |
| G-a5 | Synthetic correctness | Income boundaries, missing partner resources, unresolved receipt, caregiver-linked grants, incompatible own grants, contradictory responses | Implemented | `output/phase8/evaluation_log.csv`: 22 screening cases + 2 schedule checks + 1 leakage check + 1 run trace, all 26 passed; extended app tests in `docs/validation_summary.json` |
| G-a6 | Data integrity | Joins preserve the person-level unit; counts trace to the flow | Implemented | The command runs `validate` and matches the frozen cohort hash |
| G-a7 | Leakage prevention | Receipt and derived labels cannot enter predictor preparation | Implemented | Evaluation case `forbidden_predictor_is_rejected` |
| G-a8 | Repeatability | Two runs, same configuration: identical membership, reasons, folds, and numeric outputs within tolerance | Implemented | Two runs; all 14 files byte-identical. Recorded in `specification/phase7_artefact.md` |
| G-a9 | Transparency | Status, reasons, rule version, and predictions can be inspected | Implemented | Run record; app result/reason grids and audit downloads; `examples/synthetic_report/` |
| G-a10 | Streamlit | Secondary review interface | Implemented | `app/Home.py`; previously recorded 220 automated tests, all 15,388 reference records match CLI, and 50 Windows synthetic export checks. These functional checks were not rerun for manuscript expansion |
| G-a11 | Interface user test | Locate a reason, name the scenario, read a calibration display | Proposed | Protocol in `docs/usability_protocol.md`; participant study not conducted and excluded from the current revision by user instruction. Screenshots/export checks are functional evidence, not user acceptance |
| G-a12 | Synthetic public demo | Any example that leaves controlled storage is synthetic | Implemented | Built-in/downloadable synthetic template and `examples/synthetic_report/`; controlled local package excludes raw data/history. No public site deployed |

## H. Submission 2 process records

These are working rules from the Submission 2 brief. They do not change the estimator.

| ID | Component | Requirement | Status | Evidence required to move status |
| --- | --- | --- | --- | --- |
| H1 | Sequential phases | No Results prose before the producing analysis is verified | Implemented | Dated study close-outs and October implementation evidence; revised paper uses frozen outputs |
| H2 | Phase close-out | Completed, Evidence, Problems, Decisions, Next step | Implemented | Historical close-outs and October plan Phase 6 revision record in `specification/decision_log.md` |
| H3 | Decision log | Every deviation and every resolution of an open parameter | Implemented | `specification/decision_log.md`, 74 unique D-001–D-074 rows |
| H4 | Traceability matrix | RQ → method → evidence → result → discussion → conclusion | Implemented | Section 13 of `specification/implementation_specification.md`, updated for current RQ3 evidence |
| H5 | Paper | IEEE, at most 8 pages, written from verified outputs, future tense removed only for work that was done | Implemented | Current D-074: 5,469 manuscript words, 141-word abstract, 408-word III.B; eight Letter pages, nine tables, four figures, 28 active first-use references, 18 DOI references and APRE402. Fresh verifier: 209 numerical/100 supporting comparisons passed, zero failures, 314 rows/four limits; root review passed all eight final pages. Fonts/builder unchanged. Original 2014 formula/rate, 2015 rate and R621 amendment read; four standard-rate ceilings verified. `paper/historical_thresholds_verified_audit.md`/`.json` records the chain and research limits. Standard age-60–74 maximum across ages is a research choice; S1c unchanged. Point 3 addressed within research scope, pending user review; points 4–10 pending. D-073's 5442/141/374 counts, 28 references and completed checks are historical at 7d54c18. No code, rule, result, refit or checklist status change. |

## Current summary

| Status | Count |
| --- | --- |
| Proposed | 2 |
| Implemented | 94 |
| Verified | 0 |

Counted rows: A1–A8 (8), B1–B7 (7), C1–C17 (17), D1–D6 (6), E1–E28 (28), F1–F13 (13), G-a1–G-a12 (12), H1–H5 (5).

The two Proposed rows are the deferred random forest (F13) and unperformed
participant interface evaluation (G-a11). Implemented records the evidenced
minimum status; functional verification is described in the evidence cells and
`docs/evidence_log.md`, without implying participant usability or external
predictive validation. D-074 closes the specific historical threshold-source
gap within the research scope: four standard-rate ceilings and the operative
formula/minimum/couple provisions are verified from original texts. Point 3
is addressed within that scope and awaits user review; points 4–10 remain
pending. The new audit is `paper/historical_thresholds_verified_audit.md`/`.json`;
`paper/manuscript_validation.json` records current build evidence. The paper
has not been externally submitted. Broader publisher/source checks, ethics,
access/disclosure, portal requirements and participant usability remain open.
All build accounts below through D-073 are historical. In particular D-073's
5,442 words, 141-word abstract, 374-word III.B, 28 references, hashes and
completed checks are archived at `7d54c18`; they do not verify the D-074 build.

## Historical revision stages, through D-073

The following dated accounts preserve the evidence available at each stage.
Their source gaps and pending actions are superseded by the D-074 update
above and the current closure below where applicable.

The targeted revision preserves the scientific model and nine-table/four-figure
evidence while strengthening RQ interpretation and theory/sensitivity synthesis.
P1–P4 are addressed in text. P5 is partially addressed through the reproducible
claim register and three locally read primary Stats SA documents; thirteen
external source requests failed with proxy CONNECT 403. Source verification,
participant usability, ethics/access/disclosure and portal requirements must not
be inferred from software or formatting checks.

The 13 October D-066 revision follows the user's instruction to write for
specialist readers without defining every technical term. It removes elementary
glosses while keeping normal terminology, acronym expansions, study-specific
assumptions and metric interpretation. Concrete active subjects and appropriate
tense remain. The literature opening presents one paper's context and retains
the qualified 511-to-55 mixed-grant review flow and unavailable original
search/screening records. Language and scientific-consistency reviews are
editing evidence, not participant comprehension or usability results. No app
suite, refit, province analysis or primary-source query ran. D-062–D-065 counts,
hashes and the earlier 90-term reviews remain historical records.

The 14 October D-067 revision addressed only supervisor point 1 in Section
II.A. The user reviewed it positively, then authorised D-068's three framework
refinements: Section II.D, Figure 1 and the Section VI.E synthesis. The user
accepted those refinements before authorising D-069's point 2 revision. At the
D-068 stage, Table II formatting and supervisor points 3–10 remained pending.
No table-cell, methods, numerical-result, limitation, conclusion, reference,
app, model or data change follows. The 94 Implemented / two Proposed /
zero Verified summary remains unchanged. Figure 1, its conceptual generator,
related prose, working mirrors and reporting/audit records implement D-068.

The 14 October D-069 revision addresses Table II's conceptual relationships
and formatting. Age/sex provide demographic context, schooling concerns
learning costs, and settlement/distance concern compliance costs; coding and
measurement limits remain explicit. Psychological costs are unmeasured, and
two settlement contrasts explain the six slopes across five predictor groups.
Only Table II receives top/left-aligned 9 pt cells, black horizontal rules,
no vertical grid, unsplit rows, repeating header and caption keep. Other tables,
sections, figures, references, analyses and software remain unchanged from
`0dd3d0e`. The user subsequently approved point 2 and requested point 3;
D-070 records that follow-up. No checklist status changed.

The historical 14 October D-070 revision addresses III.B's screening description and
verification boundary. Annual ceilings, conditional formula/payment/couple
assumptions, inclusive equality and reciprocal resident spouse/resource checks
are explicit. Marital responses do not prove legal spouse status. Arithmetic,
code and local survey checks pass, but twelve official requests failed with
HTTP 403 before original text retrieval. Original notices, operative formula,
R100 minimum and legal spouse definition remain unverified; point 3 is
partially addressed and awaits user review. Points 4–10 remain pending.
Scientific outputs and substantive rules are unchanged. No checklist status
changed; implemented code does not establish legal verification. Its
5,430-word draft and original hashes/reviews are retained at `beec7d77`.

The historical 15 October D-071 revision records the user's four legal follow-ups to
original supervisor point 3. Scoped audit wording distinguishes verified
arithmetic, coded ceilings and LCS partnership items from unauthenticated
legal provisions. Research rationale explains combined resources regardless
of spouse age, residence/reciprocity checks, unavailable nonresident income,
the questionnaire's omission of separated-spouse details and unresolved
cohabitation/ambiguous cases without single-status or zero-income assumptions.
Follow-ups 2 and 3 are addressed within that scope. Five expanded public
requests on 14 October and two exact user-provided URL requests on 15 October
failed HTTP/proxy CONNECT 403. The user's narrative, favicon links and URL
candidates did not supply primary clause text or amendment history. Critical
follow-ups 1 and 4 therefore remain blocked; no historical in-force chain or
legal reference was authenticated. The seven follow-up attempts are
separate from D-070's twelve and the older P5 thirteen; those audits are
historical and unchanged.

Root and independent reviews passed all eight current retained page images
on 15 October (Africa/Johannesburg); their 14 October UTC render timestamps
remain tied to the current source. Independent actual-diff and questionnaire
pages 5–6 review passed. Original supervisor point 3 remains partially
addressed and awaits user review; supervisor points 4–10 remain pending. The
fourth legal follow-up is not supervisor feedback point 4. No checklist status
changed: 96 rows remain 94 Implemented, two Proposed and zero Verified. D-062–
D-070 counts/hashes and earlier reviews remain explicitly historical. D-071's
5,451-word/377-word III.B draft, hashes and completed checks are retained at
`214647e42adad9a20a30461d4026e1f93732ae7a`; D-072 below records the historical
uploaded-source review; D-073 records the current correct-2008-base review.

The historical 15 October D-072 revision reads uploaded original 2011 and 2022 legal
texts. GN R286/GG 34169 Schedule 2 uses 1.4A − 0.4B, effective 1 April 2011
under Schedule 4. GN R2119/GG 46459 Annexure A(2)/(5) uses 1.6A − 0.4B and
R100 monthly minimum, commencing 31 May 2022 under regulation 41. The later
formula does not establish historical 2014–2015 applicability. `415.pdf`/
GG 31342 concerns banking/customs and is excluded; the correct 2008 base
GN R898/GG 31356 is identified but full text unread. The intervening formula
chain and original 2014/2015 rate notices remain missing.

III.B and Section VII's first paragraph now make that historical limitation
explicit; references [26]/[27] and source copies support the read originals.
Reference after-spacing reduces from 2.5 to 1 pt; 10/9/8 pt fonts remain.
The D-072 draft has 5,457 words, a 141-word abstract, 389-word III.B and
eight Letter pages with nine tables, four figures and 27 references. D-072
source-bound audits pass 209 numerical and 100 supporting comparisons, with
zero failures, 314 register rows and four limits. Root and independent visual
reviews passed all eight final page images. Independent
uploaded-source/scientific reviews passed. D-071's completed audits/reviews
remain historical. Follow-ups 2/3 are addressed within accuracy/research scope,
criteria 1/4 remain historically
incomplete, original supervisor point 3 remains partial and awaits user review,
and supervisor points 4–10 remain pending. No checklist status changes:
96 rows remain 94 Implemented, two Proposed and zero Verified; the decision
table contains 72 unique rows. D-062–D-071 counts, hashes and earlier reviews
remain historical.

The historical 15 October D-073 revision at `7d54c18` reads the correct 81-page base GN R898,
GG 31356, 22 August 2008. Regulation 1 supplies the spouse definition;
18(2)/(3) joint-income/desertion rules; 19(1) half-joint annual income;
20 deductions; 39 commencement. Annexure A(2) uses 1.3A − 0.5B and A(5)
the R100 monthly minimum. Source SHA-256:
`c54ce6e72a31430ddd4fe1c3a8177b113b8f56194856719e8652eb24c66b59c6`.
The original 2008 income scope includes dependent-child/ex-gratia items
absent from 2022; no identity of definitions, lists or operative versions is
assumed. Verified formulas differ across 2008, 2011 and 2022, while the
operative 2014–2015 amendment/rate chain remains missing.

Only III.B's threshold/partnership paragraphs, source (stable ID28/published 26) and a
source PDF are in scope; frozen science, other sections, all nine tables/four
figures and fonts remain unchanged. Final counts, pages, current-source audits, visual reviews and artifact hashes passed as recorded below. The D-072
5,457/141/389 manuscript, 27 references and completed checks are historical
at `132e96cee7d7b3b6f5d5b91a214590359a25d210`; its original source audit
and appended supplements remain intact. Legal criteria 1/4 remain partial,
2 accuracy and 3 research justification improve, original supervisor point 3
remains partial and awaits user review, and supervisor points 4–10 remain
pending. No checklist status changes: 96 rows remain 94 Implemented, two
Proposed and zero Verified; the decision table contains 73 unique rows.
D-062–D-072 counts, hashes and earlier checks remain historical.

The final D073 manuscript has **5,442 whitespace tokens**, a **141-word abstract**
and **374-word III.B**, with **eight Letter pages, nine tables, four figures and
28 first-use references**. All 209 numerical and 100 supporting comparisons passed
with zero failures, 314 register rows and four documented limits. Primary and
independent reviews passed all eight final page images. Manuscript SHA-256:
`980b21d321cfd9c22ac5c2546e35363ef03cc5c8bb520cffc9de60b4db260138`.
PDF SHA-256:
`b8e29a730d96284d7d08aeed1a0057635aac4cac0663c70d2bc36a8076cbb527`.
Word SHA-256:
`3f82e2937c853dc9a82b620ba36c6d48b3cdadb1f014dca0284c3bc9657104b0`.
The builder's only new change gives its final invisible balancing paragraph an
exact 1-point line to prevent a blank ninth page. Visible fonts remain 10/9/8 points;
reference spacing, all nine table XML records, figures and scientific files match
`132e96c`. The new stable source ID28 is published reference 26, with 2011/2022
renumbered 27/28. These checks do not authenticate the missing survey-period chain.

## D-074 current source closure — 15 October 2026

GG 37474, 28 March 2014, page 3 (GN 211) verifies R1,350 monthly from
1 April 2014. On pages 4–5, Schedule paragraph 2 substitutes Annexure A(2) with
`D = 1.6A − 0.4B`; printed commencement paragraph 1 applies from 1 April
2014. GN 277/GG 38647, 30 March 2015, page 3 verifies R1,410 from
1 April 2015. R898/2008 Annexure A(5) gives the R100 monthly minimum,
19(1) half-joint income, 18(2)/(3) joint income/desertion with Agency
approval, and regulation 1 the spouse definition. R621/GG 39007,
21 July 2015, leaves the OPG formula, means and spouse provisions unchanged.
These establish R61,800/R123,600 and R64,680/R129,360 standard-rate ceilings.

Both rate notices include an extra R20 from age 75. Using the standard
age-60–74 maximum across ages is an explicit primary research choice;
S1c is unchanged. The proxy still omits assets, deemed asset income and
deductions. Resident reciprocal spouse links are research consistency
requirements; ambiguous or nonresident cases are unresolved, not ineligible.
Point 3 is addressed within research scope, pending user review; points 4–10
remain pending. The 96 rows remain 94 Implemented, two Proposed and zero
Verified; the decision table now contains 74 unique rows. Current manuscript:
5,469 words, 141-word abstract, 408-word III.B, eight Letter pages,
nine tables, four figures and 28 active first-use references. The fresh
source-bound verifier passed
**209 numerical and 100 supporting comparisons**, with **zero failures,
314 register rows and four documented limits**. Root visual review passed
all eight final pages. Fonts and builder are unchanged; 18 DOI references
are retained. No science, code, rules or results change follows from source closure.
