# Implementation specification

**Project:** Interpretable prediction of reported Older Person’s Grant non-receipt among apparently eligible adults in KwaZulu-Natal  
**Student:** Oluhle Jawe (21634436), ICT Honours; Submission 1 PRIC401, Submission 2 APRE402 (confirmed by the user)
**Source of truth:** `21634436_Oluhle_Jawe_Submission_1.pdf` (Submission 1, 6 pages)  
**This document:** Specification created in study Phase 1, with current implementation and traceability updates for Submission 2. The approved scientific design is preserved.

**Specification status:** Original study phases 1–11 and October Streamlit local implementation/functional verification remain complete. P1–P4 interpretation improvements and the reproducible claim register remain complete. After positively reviewing supervisor point 1, the user requested the D-068 framework follow-up: Section II.D, a refined Figure 1 and a Section VI.E synthesis. The current draft retains eight pages, APRE402, specialist-audience language and frozen results. This follow-up awaits user review; Table II formatting under point 2 and supervisor points 3–10 remain pending. See Section 23 and current manuscript validation. P5 remains limited by unavailable original journal/legal texts and unconfirmed ethics/access/disclosure/portal records. Participant usability has not been evaluated.

**Created:** 2026-09-25; updated 2026-10-14 (Africa/Johannesburg).

**Rule version:** `opg-kzn-primary-v1`. Retained research model: six slopes under D-052; packaged inference version `opg-kzn-six-slope-v1`.

Submission 2 (`Agent.md`) asks for a completed empirical study written up as an IEEE conference paper of at most 8 pages. The original empirical outputs exist; the October revision adds conceptual framing and actual computational-artefact evaluation evidence. The user subsequently authorized integrating Submission 1's approved title, aim, objectives, literature/review approach and proposal context into an exactly eight-page Submission 2. Original proposal counts are attributed as historical context, rather than presented as empirical cohort results. The integration does not alter the frozen research results or refit the scientific model.

---

## 1. How to read statuses

| Status | Meaning |
| --- | --- |
| Proposed | Required by Submission 1, or required by the Submission 2 brief as a restatement of that design. Not yet built. |
| Implemented | Code or an analysis artefact exists and has been run on the project data or on the specified tests. |
| Verified | An independent check supports the implementation: a synthetic test, a count reconciliation, or a repeated run. |

A step moves status only when the evidence named in `specification/checklist.md` exists. Adding a method because it is common in machine-learning work is out of scope.

## 2. Aim, questions, and objectives

**Aim.** Develop and evaluate an interpretable computational artefact for analysing reported Older Person’s Grant (OPG) non-receipt among apparently eligible older adults in KwaZulu-Natal, using the Living Conditions Survey (LCS) 2014/2015.

**Research questions.**

- **RQ1.** What proportion of the study population reports OPG non-receipt, and how does this estimate change under alternative eligibility assumptions?
- **RQ2.** How well does a small logistic regression model distinguish recipients from non-recipients and estimate non-receipt probabilities in held-out households?
- **RQ3.** Can the proposed artefact reproduce the analysis and clearly explain the screening decisions and model outputs?

**Objectives.**

1. Construct a documented person-level study population.
2. Describe receipt and non-receipt with the released person weights.
3. Develop and internally validate a parsimonious logistic model.
4. Evaluate the artefact’s correctness, reproducibility, and clarity.

RQ1 is the substantive estimate. RQ2 is the predictive assessment. RQ3 evaluates the artefact. The artefact estimates reported non-receipt in a historical survey population. It does not predict future grant decisions, determine official legal eligibility, or rank applicants.

## 3. Study design

Quantitative, cross-sectional secondary analysis of Statistics South Africa’s LCS 2014/2015.

| Element | Approved definition |
| --- | --- |
| Target survey population | Adults aged 60 years and older living in sampled KwaZulu-Natal households |
| Unit of analysis | Person |
| Household role | Spouse linkage; geographic context; grouping unit for cross-validation and for uncertainty resampling; a count in the cohort flow. The household is not the outcome unit |
| Apparently eligible | An adult who passes the study’s observable screening rules. This is not confirmed legal eligibility |
| Final analysis cohort | A person who passes the primary screen and has a resolved OPG receipt response |
| What the survey cannot represent | Institutionalised older adults; present-day access; a complete legal means test; application history; an administrative payment record |

Submission 1 cites a realised national sample of 27,527 households and an 89.6% KwaZulu-Natal response rate from the LCS metadata. Those figures are context. They are not the analysis cohort. Phase 2 confirms them against the metadata. The screened KwaZulu-Natal 60+ size and the non-receipt event count are established only after the cohort is built.

**Released files named as inputs** (present in `Dataset/`; contents not audited in this phase):

- `Dataset/LCS2015/LCS2015PERSONSFINAL.csv`
- `Dataset/LCS2015/LCS2015HOUSEHOLD.csv`
- `Dataset/LCS2015/LCS2015PERSONINCOME.csv`
- `Dataset/LCS2015/LCS2015HOUSEHOLDASSETS.csv`
- `Dataset/LCS2015/LCS2015TOTALLCS.csv`
- `Dataset/metadata/Living Conditions Survey Metadata.pdf`
- `Dataset/metadata/Living Conditions Survey Questionnaire.pdf`
- `Dataset/metadata/Living Conditions Survey Coicopcodes.pdf`

`LCS2015TOTALLCS.csv` and `LCS2015HOUSEHOLDASSETS.csv` are not given a role by Submission 1. Phase 2 records what they contain. They are not used unless a logged decision shows that a required concept cannot be built from the person, household, and person-income files.

## 4. Linkage and audit before any screen

Person records are linked to household information and to person-attributable income on the documented household and person identifiers.

Income records are classified with the survey COICOP codes and aggregated to the person before linkage. Annualised values released by the survey are used as annual values. They are not annualised again.

Before screening, the pipeline reports:

- duplicate person keys;
- duplicate household keys, if a household file is joined;
- person rows with no matching household;
- household rows with no matching person, counted separately and not dropped into the person file;
- income rows that do not match a person;
- persons with no income rows;
- row counts before and after every join and aggregation;
- any Submission 1 concept that cannot be constructed (Section 12).

No variable is substituted silently. A concept that cannot be built is reported, and any replacement requires an entry in `specification/decision_log.md` before it is used.

## 5. Cohort construction

Figure 1 of Submission 1 is the process. Counts are filled only after implementation.

```text
KZN adults aged 60 and older
  (linked person and household records)
        |
        v
Apply observable eligibility rules
  age (already applied at entry), partner resources,
  income screen, grant compatibility
        |
        +-- FAIL -------- record every reason
        |
        +-- UNRESOLVED -- record every reason; keep out of the model
        |
        +-- PASS -------- assess OPG receipt
                              |
                              +-- unresolved receipt --> not in the primary model
                              |
                              +-- resolved receipt
                                    Y = 0 recipient
                                    Y = 1 non-recipient
                                          |
                                          v
                              Final analysis cohort
                              (description and internal validation)
```

### 5.1 Status precedence

Each person receives one status and every applicable reason code.

| Status | Rule |
| --- | --- |
| Out of frame | Not a KwaZulu-Natal respondent, or age is missing, or age is under 60. These people are counted in the audit. They are not eligibility failures inside the study population |
| FAIL | At least one deterministic exclusion is met |
| UNRESOLVED | No deterministic exclusion is met, and at least one required screen cannot be resolved |
| PASS | Every required screen is resolved and none excludes the person |

A known exclusion takes precedence over an unresolved item. Example: a reported own disability grant excludes the person even if income is missing. The missing-income reason is still stored. This keeps “known rule failure” and “status cannot be resolved” distinct, which is the distinction in Figure 1.

### 5.2 Primary screen, in order

The screen is applied to KwaZulu-Natal respondents aged 60 and older.

1. **Incompatible own grants.** Reported receipt of an own disability grant or an own war-veterans grant is a FAIL in the conservative primary screen. The two grants are flagged separately. Caregiver-linked child grants, including the Child Support Grant received as a caregiver, and grant-in-aid are not incompatible pensions in the primary screen.
2. **Partnership class.** Classify the person from the questionnaire’s marital or partnership items.
   - Unambiguously unpartnered: apply the single-person income screen.
   - Married, with a resident spouse: link the spouse and apply the couple income screen.
   - Ambiguous partnership: UNRESOLVED on the primary screen. Sensitivity scenarios examine stated alternatives.
3. **Spouse link, for married people only.** Link the resident spouse with the questionnaire’s spouse identifier within the household. The linked person must exist, must belong to the same household, and the relationship must be consistent. A missing spouse identifier, a spouse who is not in the household, a non-resident spouse, or a spouse whose resources are unavailable produces an UNRESOLVED income screen. The single-person threshold is not applied in those cases.
4. **Income screen.** Compare the resource proxy with the period-appropriate annual threshold for that partnership class. Resources above the threshold, once both the resources and the boundary are resolved, are a FAIL. Resources within the threshold are a pass on this rule. An income screen that cannot be resolved is UNRESOLVED.

Age has already defined the frame: 60 and older. Marital circumstances are used here and are not a coefficient in the primary model.

### 5.3 Resource proxy

The proxy is annual nominal income attributable to the applicant and, where the couple screen applies, the spouse.

| Rule | Requirement |
| --- | --- |
| Amount | Survey annualised values. Do not annualise them a second time |
| Social assistance | Exclude recorded social-assistance income from the proxy, and keep it identifiable so OPG income can be compared with current receipt later |
| Other income | Retain non-social-assistance sources in the proxy |
| Household totals | Do not split a household total across people |
| Assets | Do not treat asset acquisitions as a stock of legally assessable assets. Assets are a reason the result is called apparently eligible. They are not a primary exclusion rule |
| Absent income rows | Do not treat absence as zero. Zero is allowed only when the release convention or a complete schedule supports zero. Otherwise the resource status is UNRESOLVED |
| Partial couple resources | If the spouse is required and the spouse’s income is unresolved, the couple screen is UNRESOLVED. The applicant’s income is not compared alone with either threshold |

The proxy is a research construct. It does not reproduce every legal deduction, income definition, or assessable asset. That limitation stays in the write-up.

### 5.4 Outcome

Inside the PASS group only:

| Label | Definition |
| --- | --- |
| Y = 1 | Reported OPG non-receipt |
| Y = 0 | Reported OPG receipt |
| Unresolved outcome | Contradictory responses, or unexplained missing values. These adults passed the screen and stay visible. They do not enter the primary model |

Interpretation rules:

- Read the general social-grant question and the OPG-specific response together, following the questionnaire skip pattern.
- An explicit and consistent report of no social grant supports Y = 1.
- Receiving a Child Support Grant as a caregiver does not set the OPG label.
- Compare current reported receipt with preceding-year OPG income. Disagreement is stored as a flag. The primary label follows current reported receipt. Disagreement is not “corrected” toward either measure. It is a sensitivity analysis.

### 5.5 Cohort-flow table

The frozen cohort file must be able to produce this flow, in people and in distinct households.

| Step | What is counted |
| --- | --- |
| KZN sample | Person respondents in KwaZulu-Natal, plus distinct households |
| Age missing | Reported separately; not in the 60+ frame |
| Age under 60 | Reported separately; not in the 60+ frame |
| Age 60+ | Study-population entry |
| Eligibility FAIL | Known rule failures, with reason frequencies |
| Eligibility UNRESOLVED | Unresolved screens, with reason frequencies |
| Eligibility PASS | Apparently eligible on the primary rules |
| Outcome unresolved | PASS and unresolved OPG response |
| Recipients | PASS and Y = 0 |
| Non-recipients | PASS and Y = 1 |
| Final analysis cohort | Recipients + non-recipients |

Household counts are the distinct household identifiers among the people in that row. They are not a partition: one household can contain people with different statuses, so household counts need not sum to the KZN household total. Person counts are the primary denominator.

The cohort file, the rule version, and the reason-code list are frozen before any model is fit. Later sensitivity scenarios re-screen the same linked records under a named rule version. They do not edit the frozen primary cohort in place.

### 5.6 Reason codes

These codes implement the reasons Submission 1 requires. Names may change before the first implementation commit. Meanings may not be merged.

| Code | Status contribution | Meaning |
| --- | --- | --- |
| `OUT_NOT_KZN` | Out of frame | Person is not in the KwaZulu-Natal sample |
| `OUT_AGE_MISSING` | Out of frame | Age missing; 60+ cannot be confirmed |
| `OUT_AGE_BELOW_60` | Out of frame | Age under 60 |
| `FAIL_DISABILITY_GRANT` | FAIL | Reported receipt of an own disability grant |
| `FAIL_WAR_VETERAN_GRANT` | FAIL | Reported receipt of an own war-veterans grant |
| `FAIL_INCOME_ABOVE_THRESHOLD` | FAIL | Resolved resources above the applicable threshold |
| `UNRES_PARTNERSHIP_AMBIGUOUS` | UNRESOLVED | Partnership category is ambiguous |
| `UNRES_SPOUSE_MISSING` | UNRESOLVED | Married, spouse identifier missing |
| `UNRES_SPOUSE_NOT_IN_HOUSEHOLD` | UNRESOLVED | Spouse link does not resolve to a person in the household |
| `UNRES_SPOUSE_RELATIONSHIP` | UNRESOLVED | Linked person exists but the relationship is inconsistent |
| `UNRES_SPOUSE_NONRESIDENT` | UNRESOLVED | Spouse is non-resident, or resources of a non-resident spouse are unavailable |
| `UNRES_INCOME_ABSENT` | UNRESOLVED | Required income record absent and zero is not supported |
| `UNRES_INCOME_SPOUSE` | UNRESOLVED | Couple screen required and spouse income unresolved |
| `UNRES_GRANT_RESPONSE` | Outcome unresolved | Grant items contradictory or unexplained missing |
| `FLAG_CAREGIVER_CHILD_GRANT` | Flag only | Caregiver-linked child grant. Does not exclude and does not set Y |
| `FLAG_GRANT_IN_AID` | Flag only | Grant-in-aid. Does not exclude |
| `FLAG_RECEIPT_PERIOD_DISAGREE` | Flag only | Current reported receipt disagrees with preceding-year OPG income |
| `PASS_PRIMARY` | PASS | All primary rules resolved and none exclude |

## 6. RQ1 — descriptive analysis

**Denominator.** People with a PASS screen and a resolved outcome. Unresolved outcomes stay in a separate count.

**Unweighted non-receipt proportion.** Number of people with Y = 1, divided by the number of people with resolved outcomes.

**Weighted non-receipt proportion.** Σ(wᵢ Yᵢ) / Σ wᵢ, using the released person weights on the same people.

**Characteristics.** Recipients and non-recipients are described on the Table I variables: age, sex, schooling, settlement, and welfare-office access. Marital or partnership status is described as well because it defines the screen, and it is labelled as a screening variable rather than a primary predictor. Each characteristic is reported as unweighted counts and as weighted summaries. Differences are descriptive. They are not causal effects.

**Survey uncertainty.** If strata and primary sampling unit identifiers are in the release, variance estimation for the KwaZulu-Natal 60+ domain uses that design. If they are absent or incomplete, the weighted figures remain point estimates, and any variance approximation is named as an approximation in the output and in the decision log.

**Outcome-uncertainty bounds.** Among PASS adults with unresolved outcomes, compute the non-receipt proportion twice: once assigning all unresolved outcomes to receipt (Y = 0), and once assigning them to non-receipt (Y = 1). Report both bounds beside the primary estimate. This is a bound, not an imputation into the model.

## 7. RQ2 — primary model

### 7.1 Predictors

Table I of Submission 1 is the primary specification. Seven slope coefficients plus an intercept. No stepwise selection. No extra predictors “to see if they help.”

| Predictor | Coding | df | Role |
| --- | --- | --- | --- |
| Age | Linear, per 10 years above 60: `(age − 60) / 10` | 1 | Individual |
| Sex | Male and female | 1 | Individual |
| Schooling | Below Grade 7 versus Grade 7 or above | 1 | Individual |
| Settlement | Four categories as documented in the LCS | 3 | Geographic context |
| Welfare-office access | At least 5 km, or unavailable, versus nearer access | 1 | Geographic context |
| Intercept | Included | — | — |
| **Slope total** | | **7** | |

Marital circumstances do not add a coefficient to this model.

**Leakage rules.**

- The outcome, the general grant item, the OPG item, disability and war-veteran items, grant-in-aid, caregiver grant items, social-assistance income, preceding-year OPG income, and any label or flag derived from those items stay out of predictor preparation.
- The resource proxy used for the income screen is not a predictor. Screening variables and prediction variables stay separate.
- A check fails the run if any forbidden column is passed into the model matrix.

Reference categories for sex, schooling, settlement, and welfare access are open until Phase 2 names the codes (Section 12). They are fixed before the first fit and written into the model specification. They are not chosen by searching for significance.

### 7.2 Feasibility gate, before fitting

Record cohort size, number of Y = 1 events, number of households, category frequencies, missingness, and the distribution of categories and events across the five folds.

Use that record to judge whether seven slopes are supportable. Riley et al. (Submission 1, reference [21]) informs the judgement and does not by itself guarantee adequacy for a clustered survey sample. If the specification is unsupported, simplify it, write the reason and the new specification in the decision log, and refit only the simplified model as the primary model. Keep the original Table I specification in the log as the proposal that was not supported.

Also check multicollinearity where relevant, separation, convergence, and support for each term. Report estimation failures. Do not oversample and do not balance classes.

### 7.3 Missing predictors

- Interpret structural skips before any imputation. A skip that means “not applicable” is a category or a defined code, not a hole to be filled.
- “Welfare office unavailable” is a substantive category in the Table I coding. Item non-response is not the same thing and is not recoded to “unavailable” unless the questionnaire defines it that way.
- Eligibility fields and the outcome are not imputed.
- Inside each training fold only: median imputation for continuous predictors, modal imputation for categorical predictors.
- The validation fold receives the training fold’s medians and modes.
- Tie in the mode: break ties deterministically and record the rule. The proposed tie break is the category with the smallest code after sorting codes as text. Adopt this when the pipeline is first implemented, and log it.
- Complete-case analysis is a sensitivity analysis, not the primary estimator.

### 7.4 Estimator and validation

- Primary estimator: unweighted logistic regression for P(Y = 1 | predictors).
- Survey-weighted fitting is a sensitivity analysis only.
- Validation: five-fold stratified group cross-validation.
- Group: household. Every member of a household is in the same fold.
- Stratification target: approximate balance of the outcome across folds.
- Mixed outcomes inside one household are likely. The paper does not define the household-level stratification label. **Proposed default, not yet adopted:** stratify on whether the household contains at least one Y = 1 person. Record how many households are mixed. Adopt or revise this default in the decision log before the first fit, using the observed mix.
- Every person receives a prediction from a model whose training data excluded that person’s household.
- If a fold does not contain both outcome classes, stop and review the validation plan. Do not drop the fold silently.
- Imputation and any other fitted preparation are learned on the training fold only.
- A primary-sampling-unit grouping, in place of household grouping, is a sensitivity analysis if PSU identifiers exist.

### 7.5 Metrics

Primary metrics are unweighted, on the pooled held-out predictions. Weighted versions of the same metrics are a sensitivity.

| Metric | Operational definition used for the named Submission 1 metric |
| --- | --- |
| Non-receipt prevalence | Mean of Y on the evaluated rows |
| Average precision | Area under the precision–recall curve with Y = 1 as the event. Interpret it next to prevalence |
| ROC AUC | Area under the ROC curve with Y = 1 as the event |
| Brier score | Mean of (predicted probability − Y)² |
| Calibration-in-the-large | Intercept from a logistic regression of Y on the logit of the predicted probability, with the slope fixed at 1 |
| Calibration slope | Slope from a logistic regression of Y on the logit of the predicted probability, intercept free |
| Calibration plot | Observed against predicted probability, using a predeclared binning or smoothing rule recorded in the run |
| Intercept-only reference | Within each training fold, predict the training-fold prevalence for every validation row. Compare probability error (Brier score, and calibration-in-the-large) on the same held-out rows |

No classification threshold is chosen. The study reports probabilities.

**Uncertainty.** Resample households with replacement from the pooled held-out prediction set and recompute metrics. Do not refit the model inside the resample. State the interval level and the number of resamples in the run record. Submission 1 does not set those two numbers. The proposed settings, to be adopted at implementation and logged, are a 95% percentile interval and 1,000 household resamples. Report invalid resamples and unstable calibration estimates. These intervals describe uncertainty in a fixed prediction set. They do not include variance from refitting.

**Interpretation bound.** Coefficients and performance describe association and predictive value inside the screened sample. They do not explain why a person did not receive the grant.

## 8. Sensitivity analyses

Each scenario keeps a name, a rule version, its own denominator, its own event count, and its own non-receipt rate. A change in predictive performance is read together with the change in population. Sensitivity results are stored separately from the primary results.

| ID | What changes | What stays as in the primary | Required report |
| --- | --- | --- | --- |
| S1 | Income threshold amounts, and any simplified threshold explicitly marked as an assumption | Partnership rules, grant rules, outcome definition | Cohort size, recipients, non-recipients, unweighted rate, weighted rate, change from primary |
| S2 | Partner-resource treatment, including stated alternatives for ambiguous partnership categories | Threshold source, grant rules, outcome definition | Same |
| S3 | Grant compatibility: retain people with an own disability grant or war-veterans grant | Income and partnership rules | Same, plus how many retained records came from each grant |
| S4 | Income definition, including a documented alternative to the social-assistance exclusion | Threshold, partnership, grants | Same |
| S5 | Receipt period: reclassify using preceding-year OPG income where it disagrees with current receipt | Primary eligibility screen | Same, plus the count of disagreements |
| S6 | Outcome bounds: assign unresolved PASS outcomes all to receipt, then all to non-receipt | Primary screen | Both bounds |
| S7 | Complete cases on predictors | Primary cohort eligibility; rows with missing predictors dropped after screening | Cohort size, event rate, and the same predictive metrics |
| S8 | Predictor swap: partnered status replaces welfare-office access. One coefficient either way, so the slope count stays seven | Other Table I predictors; primary cohort | Same predictive metrics, with the new specification named |
| S9 | Survey-weighted logistic fitting | Primary cohort and Table I predictors | Metrics identified as weighted |
| S10 | Weighted metric calculation on the primary unweighted model’s predictions | Primary fit | Metrics identified as weighted |
| S11 | Group cross-validation by primary sampling unit instead of household | Primary cohort and predictors, if PSU exists | If PSU is absent, record “not run” and the reason. Do not invent a PSU |

**Exploratory random forest.** Secondary. It is not part of the primary answer to RQ2. Consider it only after the logistic model, its validation, the sensitivity analyses above, and the artefact evaluation are complete, and only if the event count and the validation design support it. If it is run: same eligible observations, same predictor information, same outer household partitions; any tuning stays inside training data with grouped inner validation. Better performance is not assumed. A decision to skip it is a valid result and is logged.

## 9. Computational artefact

### 9.1 MVP, required for RQ1–RQ3

```text
Released LCS files and definitions
        |
        v
Python preparation
  validate, link, aggregate income, write an audit
        |
        v
Rule engine
  assign status and reason codes under a named rule version
        |
        v
Screened cohort (frozen primary file)
        |
        +---------------------------+
        v                           v
Descriptive analysis          Predictive analysis
  cohort flow                   training-fold preparation
  weighted non-receipt          household-grouped validation
        |                           |
        +-------------+-------------+
                      v
        Command-line workflow
          saved settings, partitions, outputs
```

| MVP piece | Requirement |
| --- | --- |
| Preparation module | Validate and link; write the audit in Section 4 |
| Rule module | Status, all reason codes, rule version |
| Descriptive module | Section 6 |
| Predictive module | Section 7 |
| Command-line workflow | One command reruns a named configuration from documented inputs |
| Run record | Input-file checksums, variable mapping version, software versions, random seed, rule version, model specification, fold membership |
| Inspectability | A researcher can read, for a person, the status and reasons, and can read the active rule version and the held-out predicted probabilities |

### 9.2 October secondary implementation and remaining limits

The original CLI MVP was reproduced before adding the Streamlit interface.
The local interface is now implemented in `app/Home.py`, backed by schema,
screening, feature, inference, reporting and workflow modules in `opg_core/`.
It accepts only the versioned normalized person CSV contract (`opg-screen-v1`),
including required grant fields and spouse context. Uploading arbitrary survey
columns, uploading the three raw tables through the interface, and reconstructing
the screen from a pre-screened cohort alone are outside this MVP.

The five sections show study context, upload validation, primary historical
screening and receipt summaries, frozen model scores and separate aggregate
held-out research evidence, and CSV/JSON/ZIP exports. Interactive filters apply
to displayed/exported rows; summary rates retain the full resolved-pass
denominator. The app does not provide alternative-scenario selection or rerun
the modelling sensitivities. Those remain documented research outputs.

The frozen JSON inference package contains coefficients and fitted full-cohort
preprocessing, with schema, rule/model versions and source checksums. Uploads
never fit a model. Full-data fitted app scores are distinct from the saved
household-held-out evaluation. Reload scores match the same fitted in-memory
model for all 1,013 records within `5.551115123125783e-17`.

Extended functional tests, full-reference UI/CLI comparisons, repeatability
and exported checksums are implemented. The recorded suite passed 220 tests;
all 15,388 reference records match, with zero mismatches. A user Windows
synthetic walkthrough and six supplied export files passed 50 cross-file,
reference and checksum checks. These support correctness and local operation;
they do not measure unaided task completion or establish user acceptance.

Participant interface evaluation remains Proposed. The protocol is
`docs/usability_protocol.md`; the user excluded conducting the study from this
revision. No participant timings, task-error counts, ease ratings or acceptance
claim are reported. The exploratory random forest also remains deferred.

Public examples are synthetic. Displays/exports omit supplied identifiers,
household pointers and raw income; uploads remain in session memory. The
standalone local package excludes raw survey data, historical outputs and Git
history. The repository already contains historical respondent-level data, so
the whole repository must not be described as an approved public demo package.
Local deployment is documented in `docs/deployment.md`; no public site exists.
The interface does not issue eligibility decisions.

### 9.3 RQ3 tests

The program running is not the evaluation. Each test has an expected result written before the observed result is recorded.

| Test | Expectation |
| --- | --- |
| Income just inside the threshold | PASS on the income rule, partnership class held fixed |
| Income just outside the threshold | FAIL, reason `FAIL_INCOME_ABOVE_THRESHOLD` |
| Income exactly on the threshold | Matches the logged comparison boundary. This test is specified when the boundary is logged |
| Married, spouse resources unavailable | UNRESOLVED. Single-person threshold not applied |
| Own disability grant | FAIL, even if income would pass |
| Own war-veterans grant | FAIL on the primary screen |
| Caregiver-linked child grant, otherwise eligible, consistent OPG response | Grant does not exclude and does not set Y |
| Grant-in-aid, otherwise eligible | Does not exclude |
| Contradictory or unexplained grant responses, otherwise eligible | PASS on eligibility, outcome unresolved, excluded from the model |
| Consistent report of no social grant | Y = 1 |
| Consistent OPG receipt | Y = 0 |
| Current receipt disagrees with preceding-year OPG income | Primary label unchanged; disagreement flag set |
| Absent income, zero not supported | UNRESOLVED |
| Absent income, zero supported by the logged release convention | Treated as zero and then screened |
| Join audit | Person count is unchanged by the household join except for documented unmatched keys. No duplicated person key in the analysis file |
| Leakage | Model matrix build fails when a forbidden column is supplied |
| Repeat run | Same configuration produces the same cohort membership, reason codes, fold ids, and numeric outputs within the logged tolerance |

The adopted repeat-run comparison is exact for statuses, reason codes and fold
ids, with `1e-10` absolute tolerance for deterministic probabilities and metric
components. The historical evaluation contains 26 checks: 22 synthetic screening
cases, two threshold-schedule checks, one structural leakage check and one run
trace. These are not 26 synthetic screening cases. The 220-test application
suite and 50 Windows-export checks are additional evidence with separate scopes;
none is a participant usability study.

## 10. What this study will not add

The following are outside the approved design. They are listed so later implementation does not absorb them as defaults.

- Stepwise or other significance-based feature selection.
- Class balancing or outcome oversampling.
- An operational classification threshold.
- Causal claims about why a person did not receive OPG.
- Allocation of household income totals to individuals.
- Treating a missing income record as zero without a logged release convention.
- Treating caregiver child grants or grant-in-aid as incompatible pensions.
- Using receipt, social-assistance income, or the screening income proxy as predictors.
- Silent replacement of a variable that cannot be constructed.
- Writing Results, Discussion, or a revised paper before the corresponding outputs exist.
- Treating the national household count or the KwaZulu-Natal response rate as a study result.

## 11. Limitations and ethics carried into the write-up

These are already accepted in Submission 1. Empirical work does not remove them.

- Observable eligibility is incomplete relative to the legal test.
- Income and receipt can be mismeasured.
- The non-recipient count may be small.
- Cross-sectional associations do not establish causes or time order.
- Design information may be too incomplete for full variance estimation.
- Internal validation does not estimate performance in another province, period, or administrative system.
- The household sample does not represent institutionalised older adults.
- The survey period does not describe present-day access.
- Reporting follows the survey’s disclosure practice. Public examples are synthetic.
- The project follows the survey access conditions and the DUT ethics determination required for this research. Ethics status is an administrative fact to record; it is not a modelling choice.

## 12. Original open parameters and recorded resolution

Submission 1 required these to be finalised against the questionnaire, the
release and official provisions. The table retains the original Phase 1 gap
list; its reasons are historical, not current blockers. Phase 2 closed the data
items G4–G16. Phase 3 closed G1–G3 and G7 and froze the cohort. Phase 5 closed
G17–G22 in D-049–D-051. None of these modelling settings is currently open.
Absent stratum information remains a documented limitation, not an invented
variable. Current implementation status is recorded in the checklist.

| ID | Parameter | Why it is open | Blocks |
| --- | --- | --- | --- |
| G1 | Annual income thresholds for a single person and for a couple, in the prices and definitions relevant to LCS 2014/2015 | Submission 1 requires a check against official provisions and does not state rand amounts | Screening |
| G2 | Comparison boundary at the exact threshold (within versus above) | “Comparison boundaries” are to be checked, not assumed | Screening |
| G3 | Whether more than one statutory threshold applied during fieldwork | The primary threshold must be identified if the legal amount changed during the survey window. Confirm the window from the metadata | Screening |
| G4 | Province code for KwaZulu-Natal | Must come from the data dictionary | Frame |
| G5 | Person identifier, household identifier, spouse identifier | Must come from the questionnaire and files | Linkage |
| G6 | Age variable and confirmation that 60 means completed years | Boundary of the frame | Frame |
| G7 | Partnership codes: unambiguously unpartnered, married, ambiguous | Primary screen treats ambiguous categories conservatively. The code list is in the questionnaire | Screening |
| G8 | Consistency check for the spouse link | “The relationship is consistent” needs the questionnaire’s relationship items | Screening |
| G9 | COICOP codes that are social assistance, and the code that is OPG income | Proxy exclusion and the receipt-period comparison | Screening and S5 |
| G10 | Release convention for zero income versus a missing schedule | Decides `UNRES_INCOME_ABSENT` versus a true zero | Screening |
| G11 | Items and skip pattern for any social grant, OPG, own disability grant, war-veterans grant, caregiver child grant, grant-in-aid | Outcome and compatibility | Screening and outcome |
| G12 | Settlement variable and its four documented categories | Table I df = 3 depends on four categories being present | Predictors |
| G13 | Welfare-office distance item; coding of “unavailable” versus item non-response; 5 km rule | Table I coding | Predictors |
| G14 | Schooling item; where Grade 7 falls; no schooling and “other” | Table I coding | Predictors |
| G15 | Sex item coding | Table I coding | Predictors |
| G16 | Person weight, stratum, PSU variable names, or confirmation that design variables are absent | Weighted estimates and S11 | Description |
| G17 | Reference categories for sex, schooling, settlement, welfare access | Required for a stable model specification | Model |
| G18 | Household stratification label when a household contains both outcomes | Paper requires approximate outcome balance and intact households, and does not define the mixed-household label | Validation |
| G19 | Random seed | Required for reproducibility; no value is given in Submission 1 | Reproducibility |
| G20 | Bootstrap count and interval level | Proposed: 1,000 resamples, 95% percentile interval | Uncertainty |
| G21 | Numeric tolerance for the repeat-run test | Proposed: exact for discrete outputs; 1e-10 absolute for deterministic floats | RQ3 |
| G22 | Mode-imputation tie break | Proposed: smallest code, codes sorted as text | Model |

Official threshold amounts were resolved in Phase 3 from the instruments in
force for the survey period and logged in D-033–D-035.

## 13. Traceability matrix

Result cells were initially filled from study Phase 9, discussion cells from
Phase 10 and conclusion cells from the Phase 11 paper. The RQ3 row now also
includes the October implementation evidence and the explicit untested-usability
limit. The current conceptual-framework eight-page draft and latest mechanical/layout
evidence are recorded in `paper/manuscript_validation.json`; Section 23 records
the current reporting scope. Earlier completed visual reviews remain historical evidence.
Independent publisher and official-notice verification are not claimed complete.

| Question | Method | Evidence / output | Result | Discussion | Conclusion |
| --- | --- | --- | --- | --- | --- |
| RQ1 | Primary screen; unweighted and weighted proportions; S1–S6 | Cohort flow; non-receipt table; sensitivity table | 67 of 1,013 apparently eligible adults (6.6% unweighted, 7.5% weighted) report non-receipt. Eligibility alternatives move the weighted figure to between 7.1% and 9.1%. | Reported receipt is usual under the observable rules. The rate is stable to the rand ceiling and more sensitive to the disability-grant exclusion. The unresolved group is larger than the non-recipient group. | About 7% of the screened adults report non-receipt. The disability-grant rule moves that figure more than the income ceiling, and the unresolved group is larger than the non-recipient group. |
| RQ2 | Retained six-slope logistic model; household-grouped five-fold CV; metrics in Section 7.5; S7–S11 | Feasibility record; held-out predictions; metric table; calibration plot | Out-of-fold ROC area 0.75 (interval 0.69 to 0.81). Average precision 0.20 beside prevalence 0.066. Brier score 0.058 against 0.062 for an intercept-only prediction. | Sex and schooling carry the ranking. Settlement and welfare access are imprecise. A high score is still usually a recipient. The model does not explain non-receipt. | Sex and schooling rank non-receipt moderately. The probabilities improve only slightly on a constant risk, and they do not explain non-receipt. |
| RQ3 | Shared rule engine; CLI reproduction; strict CSV validation; frozen inference; native UI/CLI parity; repeatability and export verification | Historical `evaluation_log.csv`; `docs/validation_summary.json`; `docs/windows_validation.json`; `examples/synthetic_report/`; current Results/Discussion sources | All 26 historical checks passed (22 screening, 2 schedule, 1 leakage, 1 trace); previously recorded 220 automated tests passed, all 15,388 reference rows match CLI with zero mismatches, and 50 checks of the user's Windows synthetic exports passed. These functional checks were not rerun for manuscript expansion. | CLI and local Streamlit make screen status, receipt, reasons, model scores and provenance inspectable. App full-data scores are distinct from held-out research evaluation. Functional tests and one user's local workflow do not establish nontechnical usability or broad acceptance. | The historical research workflow is reproducible and the local interface is functionally verified. Participant usability was not tested; no official eligibility or external predictive-validation claim follows. |

## 14. Original study phase map

This is the original September study sequence. Its Phase 6 means modelling
sensitivities; it is distinct from Phase 6 (paper integration) in the uploaded
October Streamlit implementation plan. Historical close-outs are preserved in
the decision log, with an October update appended separately.

| Phase | Starts when | Does |
| --- | --- | --- |
| 1 | Now, and complete when this file, the checklist, and the decision log exist | Specification only |
| 2 | After Phase 1 is accepted as the working specification | Audit files and metadata. Produce the variable mapping. Resolve G4–G16 as far as the files allow. Do not screen and do not model |
| 3 | After the mapping is verified and blocking gaps are either filled or logged as impossible | Build and freeze the cohort. Resolve G1–G3, G7–G11 against official provisions and the questionnaire |
| 4 | After the primary cohort is frozen | RQ1 description and eligibility sensitivities |
| 5 | After RQ1 outputs exist | Logistic model, validation, metrics |
| 6 | After the primary model has been evaluated | Remaining sensitivities. Random forest only at the end, and only if supported |
| 7 | Can be built alongside Phases 3–6 as the same pipeline, not as a separate notebook | MVP artefact |
| 8 | After the pipeline runs | RQ3 evaluation |
| 9–11 | After Phases 4, 5, and 8 have verified outputs | Results, Discussion, IEEE paper |

Work is sequential. A later phase does not invent a result for an earlier phase.

## 15. Phase 2 resolution

Phase 2 closed the data side of G4–G16. The variable dictionary is `specification/variable_mapping.md`. The join counts are `specification/phase2_data_audit.md`. Decisions D-016 to D-032 record the coding rules.

Phase 3 froze the primary cohort as rule version `opg-kzn-primary-v1`. The threshold, boundary, and partnership decisions are D-033 to D-045. The person file is `output/phase3/cohort_person.csv`.

Phase 4 answered RQ1 from the frozen cohort. The estimate and the eligibility sensitivities are in `specification/phase4_rq1.md`. The primary cohort was not replaced.

Phase 5 fit the logistic model on the frozen cohort. The retained specification has six slopes, documented in D-052. Performance is in `specification/phase5_rq2.md`.

G17–G22 were closed in decisions D-049 to D-051. Phase 6 compared the eligibility screens, complete cases, the married-status swap, the weighted fit, and sampling-unit folds with the primary out-of-fold metrics. The comparison is in `specification/phase6_sensitivity.md`. The random forest is still deferred. Phase 7 added `python analysis/run_study.py`, which rewrites the primary run in `output/runs/primary/` and matches the frozen cohort hash. Phase 8 recorded 26 expected-versus-actual checks in `specification/phase8_evaluation.md`.

Stratum cannot be constructed. That remains a limit on design-based variance.

## 16. October plan Phase 6 — earlier six-page review draft, 11 October 2026

This section records the earlier D-061 stage. Its six-page counts and 162
numerical checks are historical; Sections 17–21 record later historical builds
and Section 23 records the current framework follow-up. The validation JSON is
maintained for the latest build.

The revision strengthens the predictor-to-concept mapping in
`paper/conceptual_framework.md`, updates `paper/results.md` and
`paper/discussion.md`, and assembles a revised manuscript through
`paper/manuscript.md` and `paper/build_ieee.js`. It uses one frozen six-slope
research result set and adds the implemented Streamlit architecture, parity,
invalid-input, repeatability and Windows-export evidence. Decision D-061 records
this reporting update without a scientific refit.

The revised `paper/Jawe_OPG_nonreceipt_KZN.pdf` contains six Letter pages in
two columns, with 10 pt body text and 8 pt tables/references. It contains five
tables, two figures and 23 references numbered by first use. A pinned-lockfile
`npm ci` installation and portable build ran successfully; table paragraphs
remain together, figure spacing is corrected and the final columns are balanced.
The read-only scientific audit passed 162 numerical table checks without
changing research outputs. Build, citation-order and layout evidence is recorded
in `paper/manuscript_validation.json`. The manuscript is below the eight-page
limit; the previous four-page draft count is historical.

No participant usability study was conducted for this revision, by user
instruction. Claims stop at observed functional evidence; the previously recorded
220-test suite has not been described as a fresh run for manuscript editing.
Independent verification of bibliographic sources and the official notices
remains outstanding, and ethics approval is not documented in the project
record. This is a completed review draft, not an external submission.

## 17. Submission 1 integration and eight-page expansion, 11 October 2026

This D-062 section records the historical 4,988-word build; Section 22 describes
the earlier point 1 draft; Section 23 records the current follow-up. Its
scientific decisions remain in force.

The user authorized integrating the uploaded Submission 1 into Submission 2,
restoring its approved title, aim, objectives, review approach and attributed
proposal context while expanding literature comparisons and data
operationalization. The uploaded PDF matches the repository baseline source
byte-for-byte (SHA-256
`6d6cac29f9a6d7cd07968f5ddb2ad2a38a69c82d19f208ae33f6c0cf2611fa32`).
Decision D-062 records this change in manuscript scope; it does not revise the
historical screen, cohort, frozen six-slope model or sensitivity results.

The final rendered `paper/Jawe_OPG_nonreceipt_KZN.pdf` passed the check for
exactly eight Letter pages. The manuscript contains 4,988 words,
with two columns, 10 pt body text, 9 pt tables and 8 pt references. It contains
nine tables, four figures and 25 references numbered by first use. Added
content includes literature comparisons, data operationalization, weighted
descriptive characteristics and performance-uncertainty tables, plus conceptual
framework and cohort-flow diagrams. The independent read-only scientific audit
verified all 209 numerical table values: the previous 162 plus 47 additional
checks.
`paper/manuscript_validation.json` records the current build and audit evidence.
Independent final visual review passed for all eight freshly rendered pages:
all nine tables and four figures are legible and unclipped, captions remain
attached, and there are no blank pages or orphan headings. The final reference
page is naturally partial. The final PDF SHA-256 is
`0101c41c5332bc45def6f449ff5d5fbe88e86093adc88dfdf11e710b18548561`.

The recorded 220-test application suite and 50 Windows-report checks were not
rerun for this writing task; they retain their earlier functional scope and dates.
Participant usability remains unperformed by user direction, the random forest
remains deferred and no new public deployment occurred. Independent publisher
and legal-notice verification and ethics confirmation remain outstanding.
The integrated manuscript is a review draft; no external submission is claimed.

## 18. Targeted interpretation and claim verification, 11 October 2026

This D-063 section records the historical 5,262-word build. Its source and
claim-verification limits remain in force; Section 23 describes the current
framework follow-up.

The user authorised the attached revision plan and confirmed APRE402 as the
final-paper module identifier. The original PRIC401 Submission 1 remains
unchanged. D-063 records the new reporting scope. The revised manuscript is
5,262 words by whitespace splitting and remains eight actual PDF pages,
including references, with the existing nine tables, four figures and 25 cited
sources. Body/table/reference fonts remain 10/9/8 pt.

Discussion now defines the RQ1 estimand, prioritises unresolved cases and S3
versus S2 consequences, compares study scope with earlier literature, and
separates metric meanings and theory/proxy findings. S7–S11 are interpreted as
sample, specification, fitting-weight, evaluation-weight and grouping changes.
RQ3 distinguishes rule cases, repeatability, software-path parity, inference
serialization, owner functionality and untested participant usability.

`paper/verify_claims.py` is a portable standard-library audit of retained
evidence. It writes a 314-row `paper/claim_source_register.csv` when invoked
with `--write`. All 209 table comparisons and 100 supporting checks pass;
`paper/claim_source_validation.json` records the exact manuscript/source hashes.
Independent recalculation checks AUC/AP/Brier, weighted prevalence, the derived-
PSU approximation, fold grouping and coefficient Wald intervals. Historical
software runs are explicitly saved evidence, not fresh application execution.
Run-record CSV hashes distinguish original CRLF from retained LF bytes.

`paper/primary_source_audit.json` and its readable companion record three
authentic local Stats SA PDFs and thirteen blocked remote-source requests.
The absent journal texts and operative legal provisions remain unverified;
the 18 DOI matches to the submitted bibliography are only consistency checks.
Ethics/access/disclosure and final portal requirements require confirmation.
No participant study, refit, new scientific analysis, deployment, predicted
grade or external submission is claimed. `paper/targeted_revision_response.md`
maps all five priorities and fourteen acceptance items to this evidence.

## 19. Plain-language reporting revision, 13 October 2026

This D-064 section records the historical 5,632-word build and its 263-word
abstract. Its source hash remains a record of that version. Section 21 records
the later historical specialist-audience revision; Section 23 records the
current framework follow-up.

The user asked for active verbs, first-use parenthetical explanations and
first-person wording. D-064 records this writing scope. “I” describes the
single author's research actions; “you” guides readers through the tool and
results. Plain words replace dense terms where a technical label is unnecessary.
The revision also simplifies table text, captions and diagram labels. It does
not change the approved title, APRE402, research questions or study methods.

The D-064 manuscript has 5,632 whitespace-delimited words, including a
263-word abstract. Its rebuilt PDF has exactly eight US Letter pages, nine
tables, four figures and 25 first-use references. Body/table/reference fonts
remain 10/9/8 pt. The D-064 source SHA-256 is
`69b44ac75d1f4efb45d36cec4fa534b5cd53c7ffde17fc347e94c833a9cf9c93`;
`paper/manuscript_validation.json` records the latest render and layout evidence.
The earlier 4,988- and 5,262-word records are historical, with their original
hashes retained in the evidence log.

`paper/plain_language_revision.md` and `paper/plain_language_validation.json`
record a reading-order review of 90 essential terms and 16 scientific meanings.
The review covers prose, tables, captions and diagram-label sources. Apparent
screening, reported receipt, predicted non-receipt and legal entitlement remain
separate. Sentence and pronoun diagnostics support editing decisions; they do
not measure reader comprehension, task success or participant usability.

`paper/verify_claims.py` still passes 209 numerical table comparisons and 100
supporting checks. Its 314-row source register retains four limitation rows.
Four temporary negative controls confirm that it rejects an incorrect table
count, wrong abstract AUC, false participant-usability prose and false Table IX
evidence. Source hashes bind these checks to the unchanged scientific outputs.

Scientific, model, application, test, tool and dataset paths are unchanged from
`bfabb350a8062cab7237a31c362afc4cc15196f4`. No model was fitted or application
suite rerun; the earlier 220 tests, 15,388-record agreement and 50 Windows-report
checks remain historical evidence. No participant study or other-province
analysis was performed. The earlier province-extension conversation remains
brainstorming, rather than a result or new method in this paper.

P5 remains partial. This writing revision does not authenticate inaccessible
journal/legal texts, confirm institutional ethics/access or historical-data
disclosure clearance, or verify portal requirements. No new original-source
reads, public deployment, predicted grade or external submission are claimed.

## 20. Professional-language reporting revision, 13 October 2026

This D-065 section records the historical 5,627-word build, its 249-word
abstract and original source hash. Section 23 records the current framework
follow-up.

The user requested a clear, concise and scientifically sound ICT paper for
conference review and marking. D-065 records this writing scope. Concrete
subjects, including the pipeline, screen, model and app, now perform the
actions without first-person or direct-address pronouns. Past tense describes
completed methods and observed results. Present tense describes software
behaviour, rules, tables and interpretation. Conditional language identifies
future work. Parenthetical technical explanations remain at first use. The
revision preserves the approved title, APRE402, research questions and all
scientific distinctions.

The D-065 manuscript has **5,627 whitespace-delimited words**, including a
**249-word abstract**. The regenerated PDF has **exactly eight US Letter
pages**, nine tables, four figures and 25 references numbered by first use.
Body/table/reference fonts remain 10/9/8 pt. Root and independent reviewers
passed visual inspection of all eight fresh pages.
`paper/manuscript_validation.json` records the current build and layout
evidence. D-065 source SHA-256:
`1f0080d9982dbe5a5d6b4f022b542341c343ca597338034fc714fd79a8f25df3`.

`paper/professional_language_revision.md` and
`paper/professional_language_validation.json` record the professional wording,
tense and term review. All 90 term checks and 16 scientific-meaning checks
pass. Apparent eligibility, reported receipt, predicted non-receipt and legal
entitlement remain separate. These reviews support manuscript editing; they
do not measure participant understanding or usability.

The retained-evidence verifier passes **209 numerical table comparisons and
100 supporting checks**. Its **314-row register retains four limitation rows**.
`paper/professional_language_negative_controls.json` records four temporary
false-evidence variants rejected as expected. These checks bind the manuscript
to retained scientific evidence; they do not add new application performance
or participant-evaluation results.

Scientific, model, app, data, reference, diagram and build-layout paths remain
unchanged from `e70b300895c9777067f5825abc25709b4a0e197d`. No app suite ran,
no model was refitted and no other province was analysed. The earlier 220 app
tests, 15,388-record agreement and 50 Windows-report checks remain historical
functional evidence. Participant usability remains unperformed by the user's
scope direction.

P5 remains partial. Original journal and legal verification, institutional
ethics/access, historical-data disclosure and official portal requirements
remain unconfirmed. No new primary-source read, public deployment or external
submission occurred. Sections 17–19 retain the historical D-062, D-063 and
D-064 word counts and source hashes; Section 23 identifies the current framework follow-up.

## 21. Specialist-audience and integrated-literature revision, 13 October 2026

This section records the historical D-066 5,097-word build. Its generated
artifacts and audits remain in Git commit `e83b504`. Section 22 records the
historical supervisor point 1 draft. Section 23 records the current framework follow-up.

The user's latest instruction explicitly replaces the earlier requirement to
define every technical term. D-066 records the new specialist-audience scope.
The revision removes 52 elementary parenthetical glosses and condenses the
abstract, theory and metric-definition paragraphs. Standard technical terms,
acronym expansions, study-specific operational assumptions and metric
interpretation remain. Concrete active subjects, appropriate tense and
scientific qualifications continue. The earlier 90-term definition requirement
belongs to the historical D-064/D-065 builds, not the current acceptance rule.

The literature opening now presents one paper's research context without
speaking about a separate proposal. It retains the recorded 511-to-55 review
flow and states that the literature covers mixed grants rather than 55
OPG-only studies. Original search exports and screening logs remain unavailable
for independent verification. This writing task did not repeat the search or
authenticate additional sources.

The D-066 manuscript contains **5,097 whitespace-delimited words** and a
**141-word abstract**, **530 words fewer** than D-065. Its regenerated PDF has
**exactly eight US Letter pages**, nine tables, four figures and 25 references
numbered by first use. Body/table/reference fonts remain 10/9/8 pt. The
approved title, APRE402, research questions, figure assets and build layout
remain unchanged. Root and independent reviewers passed all eight fresh pages;
`paper/manuscript_validation.json` records the current build and layout review.
D-066 manuscript SHA-256:
`3dac12bcb9fd9ba60c05c64fa683a8e61e065b575c8c70a6e0a18f3fe8cd7ee3`.

`paper/specialist_language_revision.md` and
`paper/specialist_language_validation.json` record the language scope and
**16 passed scientific-distinction checks**. Apparent eligibility, reported
receipt, predicted non-receipt and legal entitlement remain separate. The
retained-evidence audit passes **209 numerical table comparisons and 100
supporting checks**, with **314 register rows and four explicit limitations**.
All four temporary controls pass in
`paper/specialist_language_negative_controls.json`; the verifier itself is
unchanged. These are manuscript-consistency reviews, not measures of reader
comprehension or participant usability.

Scientific, application, data, model, reference, figure and build-layout paths
remain unchanged from `17e1b0536ec4f683d2a04e5caced2bb89635a943`. No app suite,
model refit, other-province analysis, participant study or primary-source query
occurred. Earlier 220-test, 15,388-record agreement and 50 Windows-report results
remain dated functional evidence. Participant usability remains unperformed.

P5 remains partial. Original journal/legal verification, institutional
ethics/access, historical-data disclosure and official portal requirements
remain unconfirmed. No deployment or external submission occurred. Sections
17–21 retain historical D-062–D-066 counts and source hashes. Section 23 and
the current audit files identify the framework follow-up.

## 22. Supervisor feedback point 1, 14 October 2026

This section records the historical D-067 5,308-word draft at `1fe4820`.
The user subsequently reviewed point 1 positively and authorised the three
framework refinements recorded in Section 23. Original counts and hashes
remain historical evidence.

The user requested one supervisor correction at a time, with review and
acceptance before the next. D-067 records a draft revision of Section II.A
only. It strengthens the integration gap and contribution relative to the
reviewed studies and clarifies literature-search reproducibility limits.
Supervisor points 2–10 remain pending. Table II, screening assumptions,
validation methods, software evaluation, statistical results, interpretation,
ethics, conclusion and references have not changed under this point 1 task.

The review description retains documented databases/resources, search concepts,
broad selection criteria and thematic narrative comparison. The recorded
511-to-55 flow covers mixed-grant literature. Exact database queries, search
dates and filters, original exports, item-level screening/exclusion decisions
and the 55-source extraction register remain unavailable; the search and
selection decisions cannot therefore be independently reproduced or exhaustive
coverage established. The study's contribution concerns transparent screening,
person-weighted description, household-held-out prediction and inspectable,
reproducible software within this historical KZN analysis. No new algorithm,
legal entitlement, causal explanation, usability or external performance is
established by this wording change.

The D-067 draft contains **5,308 whitespace-delimited words** and a
**141-word abstract**. The regenerated render retains **eight US Letter pages**,
nine tables, four figures and 25 first-use references with 10/9/8 pt body/table/
reference fonts. Root and independent reviewers passed all eight final pages;
`paper/manuscript_validation.json` records the completed render and layout review.
Manuscript SHA-256:
`bf897e564f37e3d3dc19176a796eae3f8fea04c2392156dccf90163913e4e91a`.
`paper/supervisor_feedback_response.md` and
`paper/supervisor_point1_validation.json` document the response and scope.

All **209 numerical comparisons and 100 supporting checks pass**, with
**314 register rows and four explicit limitations**. Only Section II.A prose
changed from `e83b504fb124d6bf5f384a656f52ed2a7bd45a11`; all other
sections and table cells remain byte-identical. Scientific, app, data, model,
reference, diagram, build and verifier-code paths remain unchanged. No negative
controls, app suite, model refit, province extension, participant study or
primary-source query ran. Earlier controls and 220-test, 15,388-record agreement
and 50 Windows-report checks retain their historical dates and scope.

P5 original-source/legal, institutional ethics/access, historical-data
disclosure and portal limits remain unchanged. Participant usability remains
unperformed. The checklist remains 96 rows: 94 Implemented, two Proposed and
zero Verified. No deployment or external submission occurred. Sections 17–21
retain historical D-062–D-066 counts and hashes. The next step at this stage
was user review of point 1 before point 2. Section 23 records the later
positive review and authorised follow-up.

## 23. Conceptual-framework follow-up, 14 October 2026

D-068 records three refinements explicitly requested after the user's positive
review of point 1. This follow-up adds Section II.D, refines Figure 1 and adds
Section VI.E. It does not apply all remaining supervisor comments. The
framework aspect of point 2 is addressed; Table II formatting and supervisor
points 3–10 remain pending. The follow-up awaits user review.

The **142-word Conceptual Framework** connects reported OPG non-receipt with
administrative-burden theory and explains why observable screening defines the
analysis population. It distinguishes theoretical costs from survey proxies:
schooling concerns potential information resources, distance and settlement
concern possible compliance effort, and age and sex provide demographic
context. Figure 1 distinguishes theory, observed measurements, screening
status, reported receipt, person-weighted description and unweighted
household-held-out prediction. Its dashed enclosure identifies artefact
implementation, not another causal factor. PASS and resolved receipt define
the cohort; the app's frozen full-data upload scores remain separate from
held-out evaluation and never alter screening or receipt.

The **109-word Section VI.E synthesis** explicitly returns to the framework.
Screening sensitivity supports an explicit denominator and sex differences
support demographic comparison without confirming burden mechanisms. Lower
schooling challenges a simple information-barrier expectation. Office-distance
and settlement uncertainty leaves compliance-cost expectations unresolved;
psychological costs remain untested. The artefact contributes reproducible,
traceable implementation of bounded measurement choices despite these limits.

The current source contains **5,423 whitespace-delimited words** and a
**141-word abstract**. The PDF has **eight US Letter pages**, nine tables,
four figures and 25 first-use references. Body/table/reference fonts remain
10/9/8 pt and build layout is unchanged. Root and independent reviewers passed
all eight final pages; `paper/manuscript_validation.json` records the completed
render and review. Science and specialist-audience reviews
pass; all **209 numerical comparisons and 100 supporting checks pass**.
The **314-row register retains four explicit limits**. Current response and
validation records are `paper/conceptual_framework_revision.md`,
`paper/conceptual_framework_validation.json` and
`paper/supervisor_feedback_response.md`. Manuscript SHA-256:
`1fcaa1d081dbdabe3de4ed7e21ebc601a9a73b8adf3a81078a77b75bec654b49`.
PDF SHA-256:
`9a75be43b0f4f18ef9c0cb4b2aa3119cf9b0468e3cfeb69cdacbaef4506e5211`.

Section II.A, all table cells, Methods III, Software and Evaluation IV,
numerical Results V, Limitations VII, Conclusion VIII and references remain
unchanged from `1fe4820088603bf531cd55e9f2fe19cd420a0e99`. Changes concern
II.C/II.D, moved VI.B material and VI.E, Figure 1 and its generator, working
mirrors, reporting records and audits. The cohort flow and other figure assets,
app, model, data and verifier remain unchanged. No app suite, refit,
negative-control rerun, publisher/source query, province analysis, participant
study, ethics/administrative confirmation, deployment or external submission
occurred. Earlier functional checks retain their original scope and dates.

The checklist remains 96 rows: 94 Implemented, two Proposed and zero Verified.
Participant usability remains unperformed and P5 source, ethics/access,
disclosure and portal limits remain open. Sections 17–22 preserve historical
D-062–D-067 counts and hashes; Section 23 identifies the current draft.
