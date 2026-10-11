# Methodology checklist

**Source:** Submission 1 (`21634436_Oluhle_Jawe_Submission_1.pdf`), Sections II–VII and Figures 1–2 and Table I.  
**Process constraints** from `Agent.md` are included only where they restate that design or require a record of it.  
**Created:** 2026-09-25; current evidence update: 2026-10-11 (Africa/Johannesburg).

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
| H3 | Decision log | Every deviation and every resolution of an open parameter | Implemented | `specification/decision_log.md`, D-001–D-062 |
| H4 | Traceability matrix | RQ → method → evidence → result → discussion → conclusion | Implemented | Section 13 of `specification/implementation_specification.md`, updated for current RQ3 evidence |
| H5 | Paper | IEEE, at most 8 pages, written from verified outputs, future tense removed only for work that was done | Implemented | Final rendered `paper/Jawe_OPG_nonreceipt_KZN.pdf`: exactly eight Letter pages; 4,988 manuscript words; two-column layout, 10 pt body, 9 pt tables and 8 pt references; nine tables, four figures and 25 references numbered by first use. `paper/manuscript_validation.json` records current render/mechanical checks, 209 independently verified numerical values and passed independent visual review of all eight pages; publisher/legal-notice verification and ethics confirmation remain outstanding |

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
predictive validation. The current integrated review draft passed the final
render check for exactly eight pages and final independent visual review of all
eight pages.
It has not been externally submitted;
independent publisher/legal-notice verification and ethics confirmation remain
outstanding. The earlier six-page draft is a historical stage, not the current
deliverable.
