# Research decision log

Deviations from Submission 1, resolutions of open parameters, and implementation clarifications are recorded here before they are used. A row is an instruction to the next phase. It is not a result.

**Source of truth:** `21634436_Oluhle_Jawe_Submission_1.pdf`.  
**Specification:** `specification/implementation_specification.md`.  
**Checklist:** `specification/checklist.md`.

| ID | Date | Phase | Type | Decision | Why | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D-001 | 2026-09-25 | 1 | Process | Phase 1 produces the specification, checklist, and this log only. No data audit, no cohort, no model, no paper rewrite. | `Agent.md` limits the start of work to Phase 1. | Adopted |
| D-002 | 2026-09-25 | 1 | Process | Every checklist row starts as Proposed. Status changes only when the evidence column is satisfied. | Prevents the manuscript from describing work that has not been run. | Adopted |
| D-003 | 2026-09-25 | 1 | Deferred parameter | Numeric OPG income thresholds and the at-threshold comparison boundary are not stated in Submission 1. They will be taken from the official provision in force for the LCS period and logged before the cohort is frozen. No rand amount is entered in Phase 1. | Submission 1, Section IV.C: thresholds and comparison boundaries are checked against official provisions. Inventing an amount would be an undeclared revision. | Open (G1, G2, G3) |
| D-004 | 2026-09-25 | 1 | Deferred parameter | Variable names, codes, settlement categories, spouse identifier, grant items, weights, strata, and PSU are taken from the released files and the three metadata documents in Phase 2. Nothing is substituted in advance. | Submission 1, Section IV.A. The files were not audited in Phase 1. | Open (G4–G16) |
| D-005 | 2026-09-25 | 1 | Clarification | People with missing age, or age under 60, are outside the study frame. They are counted in the audit and are not eligibility FAIL inside the 60+ population. | Figure 1 starts at “KZN adults aged 60 and older.” The paper does not call younger people screening failures. | Adopted as a reading of Figure 1. Revisit if the questionnaire treats age missing differently. |
| D-006 | 2026-09-25 | 1 | Clarification | If a person meets a deterministic exclusion and also has an unresolved item, status is FAIL. Every reason is still stored. | Figure 1 separates “fails screen” from “unresolved.” A known failure would be hidden if unresolved items always won. | Adopted as a reading of Figure 1. |
| D-007 | 2026-09-25 | 1 | Clarification | Household counts in the flow are distinct household ids among the people in that row. They need not sum across rows, because one household can contain people with different statuses. Person counts are the denominator for proportions. | Submission 1 asks for people and households. It does not define households as a second analysis unit. | Adopted |
| D-008 | 2026-09-25 | 1 | Deferred parameter | Reference categories for sex, schooling, settlement, and welfare access are fixed after the data dictionary exists and before the first fit. They are not chosen by significance search. | Table I specifies coding and degrees of freedom, not the reference level. | Open (G17) |
| D-009 | 2026-09-25 | 1 | Proposed default | Where a household contains both outcome classes, the stratification label is 1 if any member has Y = 1. Confirm or revise after the cohort shows how often households are mixed, and log the choice before fitting. | Five-fold stratified group CV requires a household-level label. Submission 1 does not define the mixed-household case. | Proposed, not yet adopted (G18) |
| D-010 | 2026-09-25 | 1 | Proposed default | Reproducibility settings to adopt at implementation, not before: random seed chosen and stored; 1,000 household resamples; 95% percentile intervals; mode-imputation ties broken by the smallest code (codes sorted as text); repeat-run tolerance exact for discrete outputs and 1e-10 absolute for deterministic floats. | Submission 1 requires seeds, partitions, and a stated numerical tolerance, and does not give the values. | Proposed, not yet adopted (G19–G22) |
| D-011 | 2026-09-25 | 1 | Clarification | Calibration-in-the-large, calibration slope, average precision, Brier score, and the intercept-only reference use the operational definitions in specification Section 7.5. | Submission 1 names the metrics and the citations. It does not write formulas. The definitions follow those named metrics. | Adopted as implementation detail |
| D-012 | 2026-09-25 | 1 | Scope | MVP is the rule engine, weighted description, unweighted logistic model, household-grouped cross-validation, recorded reasons, saved settings, and a command-line rerun. Streamlit, interface user tests, extended automation, and the random forest stay secondary. | Submission 1, Section VI, final paragraph. | Adopted |
| D-013 | 2026-09-25 | 1 | Scope | `LCS2015TOTALLCS.csv` and `LCS2015HOUSEHOLDASSETS.csv` have no assigned role in Submission 1. Phase 2 inventories them. They are unused unless a later logged decision shows a required concept cannot be built without them. Asset acquisitions are not an eligibility stock. | Submission 1, Section IV.B, on assets. Avoids a silent extra data source. | Adopted |
| D-014 | 2026-09-25 | 1 | Scope | Predictor preparation excludes the outcome, grant items, social-assistance income, preceding-year OPG income, labels derived from those fields, and the income proxy used for screening. | Submission 1, Sections III.E, IV, and Figure 2. Table I is the positive list of predictors. | Adopted |
| D-015 | 2026-09-25 | 1 | Scope | No stepwise selection, no class balancing, no oversampling, and no classification threshold. | Submission 1, Sections V.B and V.C. | Adopted |
| D-016 | 2026-09-25 | 2 | Parameter | Household id is `UQNO`. Person id is `UQNO` + `PERSONNO`. Spouse pointer is `Q19SPOUSNO` (`88` not applicable, `99` unspecified). | Metadata person-file and spouse-number entries. Join audit: 0 duplicate person keys and 0 persons without a household. | Adopted (G5) |
| D-017 | 2026-09-25 | 2 | Parameter | KwaZulu-Natal is `province_code` 5. | Metadata province code list. Person and household province agree on every row. | Adopted (G4) |
| D-018 | 2026-09-25 | 2 | Parameter | `Q14AGE` is age in completed years. The age frame is `Q14AGE >= 60`, which includes people recorded as 60. The release has no missing age. | Questionnaire 1.4 and the metadata final code list. | Adopted (G6) |
| D-019 | 2026-09-25 | 2 | Caveat | Age was hot-deck imputed for 0.2% of respondents and sex for 0.4% before release. The public file does not mark those people. They remain in the frame. | Metadata, data-processing note. | Adopted |
| D-020 | 2026-09-25 | 2 | Parameter | Sex is `Q12SEX`: `1` male, `2` female. No other codes. Reference level remains open. | Metadata. Value counts are only 1 and 2. | Adopted (G15). G17 still open |
| D-021 | 2026-09-25 | 2 | Parameter | Settlement has the four documented categories and no code 3: `1` urban formal, `2` urban informal, `4` traditional area, `5` rural formal. Table I’s 3 degrees of freedom can be built. Reference level remains open. | Metadata settlement code list. | Adopted (G12). G17 still open |
| D-022 | 2026-09-25 | 2 | Parameter | Welfare access is `Q531WELFARE`. Nearer than 5 km is codes 1–4. At least 5 km is 5–7. Unavailable is 8. Don’t know (9) and unspecified (99) are predictor missing, not unavailable. `Q532WELFARE` is mode of transport and is not this predictor. | Metadata code list for distance to the nearest welfare office, and questionnaire 5.32. | Adopted (G13) |
| D-023 | 2026-09-25 | 2 | Parameter | Grade 7 in `Q21HIGHLEVEL` is code `08`. Below Grade 7 is `98` and `01`–`07`. Grade 7 or above is `08`–`20` and `23`–`30`. Codes `21`, `22`, `31`, `32`, and `99` stay missing for the binary predictor. | Metadata education code list. Codes 21 and 22 are “less than Grade 12” and do not identify the Grade 7 side. | Adopted (G14) |
| D-024 | 2026-09-25 | 2 | Parameter | Primary income amount is nominal `Valueannualized`, summed to the person. Do not annualise again. CPI-adjusted `Valueannualized_adj` is the income-definition sensitivity, not the primary proxy. | Metadata: annualised questionnaire income, with a separate CPI-adjusted column. Submission 1 asks for annual nominal income. | Adopted |
| D-025 | 2026-09-25 | 2 | Parameter | Social-assistance codes excluded from the proxy are `50331000`, `50332000`, `50332100`, `50333100`, `50333200`, `50333300`, `50333400`, and `50333500`. Preceding-year OPG income is `50331000` only. `50310000` and `50320000` stay in the proxy. `50333600` stays in the primary proxy and may be dropped in the income-definition sensitivity. | COICOP income labels. Questionnaire 4.1 names the social grants. `50333600` is compensation and UIF, not a section 4.1 grant. | Adopted (G9) |
| D-026 | 2026-09-25 | 2 | Parameter | A person with `Q11714NOTOALL = 1` and no income row is a supported zero. A person who reported a source (`Q11714NOTOALL = 8`) and has no income row is an unresolved amount. Code 9, and the 11 national cases with code 1 plus an income row, are unresolved. | Questionnaire 1.17 item 14 and the income-absence table. | Adopted (G10) |
| D-027 | 2026-09-25 | 2 | Clarification | A spouse link is consistent when the pointer finds another person in the household and that person’s pointer returns. A self-pointer, an unmatched pointer, or a pointer that does not return is unresolved. Relationship code `02` is not required, because it means partner of the head only. | Questionnaire 1.6 and 1.9. Spouse-link audit. | Adopted (G8) |
| D-028 | 2026-09-25 | 2 | Deferred parameter | Marital codes are mapped. Code 1 is the couple path. Codes 3, 4, and 6 follow the questionnaire’s unpartnered route. Codes 2 (living together) and 5 (separated) are not assigned to a threshold until Phase 3 checks the official spouse definition. Code 9 is unresolved. | Submission 1 treats ambiguous partnership conservatively and leaves the legal comparison to the official provisions. | Open for codes 2 and 5 (G7) |
| D-029 | 2026-09-25 | 2 | Parameter | Person weight is `Persns_wgt`. PSU is digits 1–11 of `UQNO`, as the metadata tells users to derive it. No stratum variable is released. Weighted point estimates can be calculated. Full design-based variance cannot. S11 can use the derived PSU. | Metadata unique-number note and the column inventory. | Adopted (G16) |
| D-030 | 2026-09-25 | 2 | Scope | `LCS2015HOUSEHOLD.income` and `LCS2015TOTALLCS.csv` are not used as person income. The asset file is not an eligibility stock. | Submission 1 forbids allocating household totals and forbids treating acquisitions as an assessable asset stock. | Adopted. Confirms D-013 |
| D-031 | 2026-09-25 | 2 | Parameter | Fieldwork is 13 October 2014 to 25 October 2015. Rand thresholds and the at-threshold boundary remain unset. | Metadata data-collection note. The LCS files do not contain the statutory amounts. | Window adopted (G3). G1 and G2 still open |
| D-032 | 2026-09-25 | 2 | Clarification | The released analysis file has 23,380 households. The 27,527 households cited in Submission 1 are the realised sample before households lacking Sections 1 and 6 or diary information were removed. The KwaZulu-Natal response rate of 89.6% matches the metadata. None of these figures is the analysis cohort. | Metadata response-details and final-inclusion note. | Adopted |
| D-033 | 2026-09-25 | 3 | Parameter | Single-person private-income ceiling is R61,800 from 1 April 2014 to 31 March 2015, and R64,680 from 1 April 2015. Couple ceiling is exactly twice that: R123,600 then R129,360. | Annexure A formula D = 1.6A − 0.4B, with no grant below R100 a month. A is R1,350 a month under GN 211 in GG 37474 (1 April 2014) and R1,410 under GN 277 in GG 38647 (1 April 2015). The October 2014 notice raised only the child support grant and grant-in-aid. The April 2015 published pair R64,680 / R129,360 matches the formula. | Adopted (G1) |
| D-034 | 2026-09-25 | 3 | Parameter | Private income at the ceiling passes. Income above the ceiling fails. At the ceiling, D is exactly R1,200 a year, which is the R100 minimum that remains payable. | Annexure A paragraphs (2) and (5). | Adopted (G2) |
| D-035 | 2026-09-25 | 3 | Parameter | Each person is screened with the ceiling in force in their interview month, taken from `SURVEYDATE`. October 2014–March 2015 uses the first ceiling. April 2015–October 2015 uses the second. | Fieldwork runs from 13 October 2014 to 25 October 2015, so one national ceiling would mix two legal amounts. | Adopted (G3) |
| D-036 | 2026-09-25 | 3 | Simplification | The primary ceiling uses the 60–74 grant maximum. The extra R20 a month paid from age 75 is not added to A. Adding it would raise the single ceiling by R960. That alternative is identified for a later sensitivity and is not the primary rule. | Published means-test schedules give one older-person income ceiling, not a second ceiling from age 75. Submission 1 requires a simplified threshold to be named as an assumption. | Adopted |
| D-037 | 2026-09-25 | 3 | Parameter | Marital codes 2 (living together) and 5 (separated) are unresolved on the primary screen. They are not put on the single-person ceiling. | The spouse definition in the regulations in force covers marriage under the Marriage Act, customary marriage, a civil union, or the tenets of an Asiatic religion. It does not cover unmarried cohabitation. A separated spouse still counts unless desertion for three months is established, and the survey does not observe that spouse’s income. Submission 1 keeps ambiguous partnership unresolved. | Adopted (G7) |
| D-038 | 2026-09-25 | 3 | Parameter | Codes 3, 4, and 6 use the single ceiling. Code 1 uses the couple ceiling when a resident spouse can be linked. | Questionnaire routing and the spouse definition. | Adopted (G7) |
| D-039 | 2026-09-25 | 3 | Parameter | The couple test compares the sum of the two private-income proxies with twice the single ceiling. Social-assistance COICOP amounts stay out of both proxies. | The operative married threshold is double the single threshold, which is what follows when the applicant’s income in a spousal relationship is half of the joint income. | Adopted |
| D-040 | 2026-09-25 | 3 | Scope | The asset test in Annexure A is not applied. Regulation 20 deductions and deemed income from assets are not in the proxy. | The asset file is an acquisition list, not an assessable stock. Submission 1 already excludes that stock. The result remains “apparently eligible”. | Adopted |
| D-041 | 2026-09-25 | 3 | Clarification | An unspecified own disability or war-veterans item is an unresolved eligibility item. A reported “yes” is a fail and takes precedence. | Unresolved grant responses are not treated as a definite no. | Adopted |
| D-042 | 2026-09-25 | 3 | Clarification | Care-dependency and foster-care grants are flagged separately from the child support grant. None of the three, and not grant-in-aid, excludes a person or sets Y. | Questionnaire 4.1 links those child grants to a caregiver. The flags keep them visible. | Adopted |
| D-043 | 2026-09-25 | 3 | Clarification | A consistent no is Q4.1a = No together with an OPG item of No or not applicable. Any other pattern that is not a clean OPG yes or no leaves the outcome unresolved. | Questionnaire skip from 4.1a, and Submission 1’s rule for contradictory or unexplained responses. | Adopted |
| D-044 | 2026-09-25 | 3 | Finding | The receipt-period flag does not change Y. In the frozen pass group the current OPG answer and preceding-year OPG income agree for all 1,013 people. | Cohort file. Every recipient has a positive `50331000` amount and every non-recipient has none. | Adopted as a cohort fact. S5 still to be run |
| D-045 | 2026-09-25 | 3 | Freeze | Primary cohort file `output/phase3/cohort_person.csv`, rule version `opg-kzn-primary-v1`, sha256 `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`. The same script run again reproduced that hash. | Cohort must be frozen before a model is fit. | Adopted |
| D-046 | 2026-09-25 | 4 | Process | Phase 4 reads the frozen cohort and writes separate output. The primary screen is not replaced by a sensitivity. | Submission 1 keeps sensitivity results separate from the primary estimate. | Adopted |
| D-047 | 2026-09-25 | 4 | Parameter | The weighted non-receipt figure is a point estimate using `Persns_wgt`. Because no stratum variable exists, the reported interval is a with-replacement linearisation clustered on the derived PSU. It is named as an approximation, not as a full design-based interval. | Submission 1: if design information is incomplete, weighted figures stay descriptive and any variance approximation is identified. | Adopted |
| D-048 | 2026-09-25 | 4 | Scope | Eligibility sensitivities S1–S6 are the Phase 4 set. Predictor, weighted-model, and PSU-grouping sensitivities stay for the modelling phases. | Phase 4 is the descriptive question. Those later rows need the fitted model. | Adopted |
| D-049 | 2026-09-25 | 5 | Parameter | Reference levels, fixed from the code list before any coefficient was read: male; Grade 7 or above; urban formal; welfare office nearer than 5 km. | Table I names the contrasts and the settlement codes. The reference is the first listed level, not a searched level. | Adopted (G17) |
| D-050 | 2026-09-25 | 5 | Parameter | Six of 827 households contain both outcomes. Folds keep each household together and stratify on whether the household contains any non-recipient. Seed 201415. | The pre-specified mixed-household rule matches a rare mix. | Adopted (G18, G19) |
| D-051 | 2026-09-25 | 5 | Parameter | Mode ties use the smallest code sorted as text. Uncertainty uses 1,000 household resamples of the fixed predictions and a 95% percentile interval. Calibration uses five quantile bins. Logit calculations clip probabilities at 1e-6. | These were the settings proposed at Phase 1 for the first model run. | Adopted (G20–G22) |
| D-052 | 2026-09-25 | 5 | Revision | The retained model has six slopes. Traditional area and rural formal are one settlement contrast. Table I’s separate rural-formal term is not the primary model. | Rural formal has one non-recipient. The training fold that held that person out did not converge, and the coefficient reached about −22. Outputs of that attempt are in `output/phase5/table_i_attempt/`. The merge is a support revision, not a significance search. | Adopted |
| D-053 | 2026-09-25 | 6 | Parameter | In S8, partnered status is marital code 1. The reference is everyone else in the primary final cohort. Living-together adults are not in that cohort. | The swap has to stay at one coefficient. Code 2 is excluded by the primary screen, so it cannot be part of this contrast. | Adopted |
| D-054 | 2026-09-25 | 6 | Parameter | The survey-weighted fit uses `Persns_wgt` as frequency weights. Training-fold imputation stays unweighted. Held-out metrics for that fit are unweighted. S10 remains the weighted summary of the primary predictions. | Weighted fitting is a sensitivity. The primary estimator stays unweighted. Frequency weights change the fit, not the survey variance of the metrics. | Adopted |
| D-055 | 2026-09-25 | 6 | Deferral | The random forest is not run in this phase. | The specification places it after artefact evaluation and asks for grouped inner tuning. Sixty-seven events is a thin sample for that check. The logistic model stays primary. | Deferred |
| D-056 | 2026-09-25 | 7 | Artefact | The minimum artefact is `python analysis/run_study.py`. It writes `output/runs/primary/`. The review interface and the random forest are outside this command. | Submission 1 makes the command-line workflow the minimum path. The interface waits until this command reproduces the frozen results. | Adopted |
| D-057 | 2026-09-25 | 8 | Evaluation | RQ3 is answered from the expected-versus-actual log and the two identical command runs. A failed check stops the evaluation script. | The specification asks for the decision the program returns beside the decision that was specified. | Adopted |
| D-058 | 2026-09-25 | 9 | Reporting | The Results section uses the frozen cohort, the Phase 4 estimate, the Phase 5 held-out metrics, the Phase 6 sensitivity table, and the Phase 8 test log. Coefficients are labelled as full-sample associations. The rural-formal revision is stated. Discussion is not written in this phase. | Phase 9 asks for evidence rather than a repeat of the methods, and it asks that weak results stay visible. | Adopted |
| D-059 | 2026-09-25 | 10 | Reporting | The Discussion uses only the literature already cited in Submission 1. It treats the schooling association as opposite to a simple information-barrier reading, and it treats settlement and welfare access as imprecise. No new citation was added. | Phase 10 asks for comparison with the existing review and for weak results to stay visible. The submission already supplies the access and calibration sources those points need. | Adopted |
| D-060 | 2026-09-25 | 11 | Reporting | The IEEE paper is `paper/Jawe_OPG_nonreceipt_KZN.docx` (also exported as PDF). It is 4 pages. References [24] and [25] are the 2014 and 2015 grant-increase notices, added because the income ceilings come from those instruments. The DUT ethics determination is not claimed as granted. | Phase 11 asks for a paper of at most 8 pages, built from Submission 1 and the completed analysis. The notices are the legal source of the ceilings. Ethics approval was not observed in the project record, so the paper states the access conditions and the synthetic tests instead. | Adopted |
| D-061 | 2026-10-11 | October plan 6 | Reporting | Revise Submission 2 sources to connect administrative-burden/access concepts to measured predictors and report the implemented local Streamlit architecture and actual functional evidence. Preserve the frozen primary research results and six-slope specification; do not refit for manuscript revision. State 26 historical checks as 22 screening cases + 2 schedule checks + 1 leakage check + 1 run trace; separately report the recorded 220 automated tests, zero mismatches across 15,388 reference records and 50 Windows-report checks. Participant usability is not conducted in this revision by user instruction; no user acceptance claim follows. Final review draft has six Letter pages, five tables, two figures and 23 references numbered by first use; 162 read-only scientific table checks passed. | Uploaded October implementation plan Phase 6, user scope direction, `docs/evidence_log.md`, `docs/validation_summary.json`, `docs/windows_validation.json`, `paper/manuscript_validation.json`, and existing frozen outputs. Functional verification is not participant usability or external predictive validation. | Adopted; six-page review draft built and mechanically checked. Independent reference/official-notice verification and ethics documentation remain outstanding; no external submission |
| D-062 | 2026-10-11 | Submission 1 integration | Reporting | Following user authorization, integrate the reuploaded Submission 1 into Submission 2 and expand to exactly eight pages. Restore the approved original title, aim, objectives and review approach; attribute earlier proposal/sample context, compare the reviewed literature and explain released-data operationalization. Add weighted descriptive characteristics and performance-uncertainty tables, conceptual-framework and cohort-flow diagrams. Keep the frozen scientific screen, cohort, six-slope model and sensitivities unchanged. Final render passed: exactly eight Letter pages; 4,988 manuscript words, nine tables, four figures, 25 references by first use; 10 pt body, 9 pt tables, 8 pt references; all 209 numerical values independently verified (previous 162 plus 47 new). | Reuploaded Submission 1 equals the repository baseline PDF, SHA-256 `6d6cac29f9a6d7cd07968f5ddb2ad2a38a69c82d19f208ae33f6c0cf2611fa32`; current manuscript/build sources and `paper/manuscript_validation.json`. This expansion does not rerun the inherited 220-test suite or 50 Windows-report checks. | Adopted; final render/page-count check and independent visual review of all eight pages passed. Participant usability remains unperformed; independent publisher/legal-notice verification and ethics confirmation outstanding; no external submission |

## Phase close-outs

### Phase 1 — 2026-09-25

**Completed.** Submission 1 was read in full (6 pages, including Figure 1, Figure 2, and Table I). The approved aim, research questions, population, eligibility logic, outcome, predictors, validation, metrics, sensitivities, artefact boundary, and limitations were written into an implementation specification. A 96-row checklist records each component as Proposed. Open parameters that Submission 1 left to the questionnaire and the official threshold provisions are listed as G1–G22 and are not filled with guessed values.

**Evidence.**

- `specification/implementation_specification.md`
- `specification/checklist.md`
- `specification/decision_log.md`
- Source read: `21634436_Oluhle_Jawe_Submission_1.pdf`

**Problems.**

- Submission 1 does not state rand thresholds, the at-threshold boundary, variable names, or category code lists. That is expected. It blocks cohort construction until Phase 2 and Phase 3 close the blocking gaps.
- Table I’s “four documented” settlement categories are not named in the paper. If the release does not contain four settlement categories, the 3 df term cannot be implemented as written and will need a logged revision.
- Strata and PSU may be absent. Weighted point estimates can still be computed from person weights. Design-based intervals and the PSU-grouping sensitivity then cannot be done as proposed.
- The legal income threshold may have changed during LCS fieldwork. The primary amount has to be tied to a dated instrument once the fieldwork window is confirmed from the metadata.

**Decisions.** D-001 through D-015. No deviation from the approved estimator, predictor list, outcome definition, or MVP boundary.

**Next step.** Phase 2 only. Audit the LCS files and the three metadata documents. Produce a variable mapping (research concept → file → variable → coding → transformation → purpose). Verify joins. Report duplicate keys, unmatched records, missingness, row-count changes, and any Submission 1 concept that cannot be constructed. Do not screen the cohort and do not fit a model.

### Phase 2 — 2026-09-25

**Completed.** The five LCS files and the three metadata documents were audited. Every Submission 1 concept was mapped to a file, a variable, a code list, a transformation, and a purpose, or was recorded as impossible to build. Joins were checked. No eligibility screen was applied and no model was fit.

**Evidence.**

- `analysis/phase2_data_audit.py`
- `output/phase2/join_audit.csv`
- `output/phase2/code_frequencies.csv`
- `output/phase2/income_absence_by_q11714.csv`
- `output/phase2/spouse_link_audit.csv`
- `output/phase2/file_inventory.csv`
- `specification/variable_mapping.md`
- `specification/phase2_data_audit.md`

**Problems.**

- No stratum identifier is in the release. Design-based confidence intervals that need stratum cannot be produced. Person weights and a derived PSU are available.
- Age and sex were hot-deck imputed for a small share of respondents before release, and those rows are not flagged.
- Grade 7 is code `08`, not code `07`. Codes `21` and `22` do not identify which side of Grade 7 they fall on.
- 47,399 people have no person-income row. In the KwaZulu-Natal age-60 frame, 28 of those absences are supported zeros and 7 are unresolved amounts.
- Married people with a resident spouse include self-pointers and non-returned pointers (4 and 1 in the KwaZulu-Natal age-60 frame).
- The national file has no reported war-veterans grant. The exclusion rule can still be coded.
- Statutory rand thresholds are not in the LCS files.

**Decisions.** D-016 through D-032. No predictor was added. No silent substitute was used. Living-together and separated marital codes are mapped and not yet assigned to a threshold.

**Next step.** Phase 3. Look up the official OPG income thresholds in force between 13 October 2014 and 25 October 2015, log the amounts and the at-threshold boundary, and decide the primary treatment of marital codes 2 and 5. Then build the person-level cohort with a status and reason code for every KwaZulu-Natal adult aged 60 or older, and freeze that file before any model is fit.

### Phase 3 — 2026-09-25

**Completed.** The official income ceilings for the survey window were derived from Annexure A and the April 2014 and April 2015 grant notices. Marital codes 2 and 5 stay unresolved on the primary screen. Every KwaZulu-Natal person now has an eligibility status and reason codes. The pass group has a resolved OPG outcome. The person file is frozen.

**Evidence.**

- `analysis/phase3_build_cohort.py`
- `output/phase3/cohort_person.csv`
- `output/phase3/cohort_flow.csv`
- `output/phase3/reason_frequencies.csv`
- `output/phase3/threshold_periods.csv`
- `output/phase3/cohort_freeze.json`
- `specification/phase3_cohort.md`

Frozen hash: `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`. A second run produced the same hash. The flow reconciles: 15,388 = 0 + 14,071 + 1,317, and 1,317 = 117 + 187 + 1,013, and 1,013 = 946 + 67.

**Problems.**

- The legal asset test and the regulation 20 deductions cannot be applied. The pass group is apparently eligible on the observable income and grant rules.
- The age-75 supplement is not in the primary ceiling. The alternative differs by R960 a year for a single person.
- 187 people aged 60 or older are unresolved, mostly because a spouse is not in the household (81) or the partnership category is ambiguous (74, of whom 3 also fail the disability rule).
- No pass-group outcome was left unresolved, and current receipt agrees with preceding-year OPG income for every resolved pass. The receipt-period sensitivity will not move this cohort.
- Household counts in the flow are not a partition. A household can appear in more than one row.

**Decisions.** D-033 through D-045. No model was fit. No weighted non-receipt rate was calculated.

**Next step.** Phase 4. Using the frozen cohort only, calculate the unweighted and person-weighted non-receipt proportions, describe recipients and non-recipients on the Table I variables, and run the eligibility sensitivity scenarios. Do not fit the logistic model in that phase.

### Phase 4 — 2026-09-25

**Completed.** RQ1 was answered from the frozen cohort. The unweighted and person-weighted non-receipt proportions were calculated, recipients and non-recipients were described, and the eligibility sensitivities S1–S6 were run without editing the primary file.

**Evidence.**

- `analysis/phase4_rq1.py`
- `output/phase4/rq1_estimate.csv`
- `output/phase4/rq1_characteristics.csv`
- `output/phase4/rq1_sensitivity.csv`
- `output/phase4/rq1_status_by_marital.csv`
- `specification/phase4_rq1.md`

The script refused to run unless the frozen cohort hash matched `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`. A rescreen with the primary rules reproduced 1,013 passes and 67 non-recipients.

**Problems.**

- No stratum identifier, so the interval is a PSU-cluster approximation.
- Non-recipients are 67 people. Several descriptive cells contain one person, and one of those people has a large weight.
- The age-75 ceiling, the CPI-adjusted income series, the UIF-type exclusion, the receipt-period comparison, and the outcome bounds do not move this cohort. That is a result, not a failed check.
- Retaining disability-grant recipients moves the estimate more than the other eligibility changes.

**Decisions.** D-046 through D-048. Differences between recipients and non-recipients are descriptions. No model was fit.

**Next step.** Phase 5. Fit the Table I logistic model on the frozen final cohort, using five-fold household-grouped cross-validation, and report the prespecified discrimination and calibration metrics. Do not use a sensitivity cohort as the primary model.

### Phase 5 — 2026-09-25

**Completed.** The logistic model was fit on the frozen cohort of 1,013 people. Household-grouped cross-validation produced one prediction per person from a model that did not train on that person’s household. Discrimination, probability error, and calibration were calculated on those predictions.

**Evidence.**

- `analysis/phase5_model.py`
- `output/phase5/metrics.csv`
- `output/phase5/oof_predictions.csv`
- `output/phase5/bootstrap_intervals.csv`
- `output/phase5/calibration_plot.png`
- `output/phase5/apparent_coefficients.csv`
- `output/phase5/fold_coefficients.csv`
- `output/phase5/fold_support.csv`
- `output/phase5/table_i_attempt/`
- `specification/phase5_rq2.md`

All five retained folds converged. The earlier seven-slope attempt did not: fold 4 failed when the only rural-formal non-recipient was held out.

**Problems.**

- Rural formal settlement has one non-recipient, so Table I’s three settlement contrasts are not stable across folds.
- There are 11 events per retained slope. The calibration-slope interval includes values well below 1, so the spread of the predicted probabilities is uncertain.
- The bootstrap does not refit the model, so it understates that part of the uncertainty.
- Weighted metrics on these predictions are a separate summary. A survey-weighted fit and a primary-sampling-unit cross-validation have not been run.

**Decisions.** D-049 through D-052. The primary answer uses the six-slope model. Coefficients are reported as associations. No threshold was chosen.

**Next step.** Phase 6. Run the remaining model sensitivities on this specification: complete cases, replacing welfare access with partnered status at the same number of slopes, a survey-weighted fit, and household versus primary-sampling-unit grouping. Keep those results separate from the primary out-of-fold metrics. The exploratory random forest stays last, and only if the event count and the validation design support it.

### Phase 6 — 2026-09-25

**Completed.** The six-slope model was refit under the eligibility screens that change the cohort, under complete cases, with welfare access replaced by a married indicator, with survey weights in the fit, and with folds grouped by sampling unit. Scenarios that keep the same 1,013 people were checked and left on the primary metrics. Person-weighted metrics of the primary predictions were carried forward from Phase 5.

**Evidence.**

- `analysis/phase6_sensitivity.py`
- `output/phase6/model_sensitivity.csv`
- `output/phase6/run_record.json`
- `specification/phase6_sensitivity.md`

The script reproduced the primary ROC area of 0.752 before comparing anything else. Every sensitivity fit converged in all five folds.

**Problems.**

- Several eligibility screens change the number of non-recipients, so a higher or lower Brier score is not only a change in prediction.
- The weighted fit’s calibration slope, 0.72, is weaker than the primary slope, 0.84.
- The random forest was not run. It is still waiting on the artefact evaluation.

**Decisions.** D-053 through D-055. No sensitivity replaces the primary model.

**Next step.** Phase 7. Build the minimum artefact around the frozen screen and the retained model: one command that reruns a named configuration, writes the cohort, the description, the out-of-fold predictions, and a run record with checksums, the rule version, the seed, and the fold ids. The interface and the random forest stay out of that command.

### Phase 7 — 2026-09-25

**Completed.** One command now rebuilds the primary cohort, the descriptive estimates, and the held-out model from the released person, household, and income files. The run record stores the rule version, the six-slope specification, the seed, software versions, and checksums of the inputs and outputs.

**Evidence.**

- `analysis/run_study.py`
- `output/runs/primary/run_record.json`
- `output/runs/primary/cohort_person.csv`
- `output/runs/primary/metrics.csv`
- `specification/phase7_artefact.md`

The cohort hash matches Phase 3. The ROC area matches Phase 5 to the recorded digits, 0.752248272380171. A second run reproduced all 14 files byte for byte.

**Problems.**

- The command covers the primary configuration. The sensitivity scenarios remain in `analysis/phase6_sensitivity.py` and are not part of this one command.
- Synthetic cases with an expected-versus-actual log are still outstanding. The command does run the existing rule checks before it builds the cohort.

**Decisions.** D-056. No interface was added.

**Next step.** Phase 8. Evaluate the rule engine with synthetic cases: income just inside and just outside the ceiling, a missing spouse, contradictory grant answers, an own disability grant, and a caregiver-linked child grant. Record the expected decision and the decision the program returns. The repeat-run check is already done.

### Phase 8 — 2026-09-25

**Completed.** Twenty-six checks compared a pre-stated decision with the program output. All passed. The checks cover the income ceiling, a missing or inconsistent spouse, incompatible grants, caregiver grants, contradictory receipt, the zero-income rule, rejection of the outcome as a predictor, and a trace from the run record back to the cohort and prediction files.

**Evidence.**

- `analysis/phase8_evaluate.py`
- `output/phase8/evaluation_log.csv`
- `specification/phase8_evaluation.md`
- Repeat run recorded in `specification/phase7_artefact.md`

**Problems.**

- The synthetic people are constructed records, not rows drawn from the LCS. They test the rules. They do not re-estimate the survey rates.
- The random forest is still deferred. These checks do not change that.

**Decisions.** D-057. No screening rule was changed because a test failed.

**Next step.** Phase 9. Write the Results section from the verified outputs only: cohort flow, the non-receipt estimate and its eligibility sensitivities, the held-out model metrics and calibration figure, and the artefact checks. Keep the methodology short enough for an eight-page IEEE paper.

### Phase 9 — 2026-09-25

**Completed.** The Results section was written from the verified outputs. It reports the cohort flow, the unweighted and weighted non-receipt estimates, the eligibility range, the held-out discrimination and calibration, the model sensitivities, and the artefact checks. The traceability matrix now has a result sentence for each research question.

**Evidence.**

- `paper/results.md`
- Result column in `specification/implementation_specification.md`
- Source tables: `output/runs/primary/`, `output/phase4/rq1_estimate.csv`, `output/phase5/metrics.csv`, `output/phase6/model_sensitivity.csv`, `output/phase8/evaluation_log.csv`

**Problems.**

- The sampling-unit interval is an approximation, and the Results section says so.
- The rural-formal contrast could not be kept, and the Results section reports the six-slope model that was actually evaluated.
- The highest predicted fifth still has an observed non-receipt rate of 17%, so most adults in that fifth report receipt. That result is included.

**Decisions.** D-058. No new estimate was calculated for this section.

**Next step.** Phase 10. Write the Discussion around the three research questions: how far the non-receipt estimate depends on the observable eligibility rules, what the discrimination and calibration do and do not establish, and whether the command makes the cohort and the predictions inspectable. Compare those points with the literature already used in Submission 1. Keep the weak results visible.

### Phase 10 — 2026-09-25

**Completed.** The Discussion was written around the three research questions. It states that reported receipt is the usual outcome under the observable rules, that the rate depends more on the disability-grant exclusion than on the rand ceiling, that sex and schooling carry the limited ranking information, and that the command makes the pipeline inspectable without a tested review screen.

**Evidence.**

- `paper/discussion.md`
- Discussion column in the traceability matrix in `specification/implementation_specification.md`

**Problems.**

- The access variables suggested by the grant literature remain imprecise, and schooling points away from an information-barrier reading. Those points are discussed as limits.
- The resampling interval around 7.5% runs from about 5% to 10%. The Discussion treats that width as part of the answer.
- No reader trial of the files was done, so the artefact claim stops at reproducible inspection.

**Decisions.** D-059. No new literature was added.

**Next step.** Phase 11. Assemble the eight-page IEEE paper from Submission 1 and from `paper/results.md` and `paper/discussion.md`. Compress the literature review and methods, use completed-study wording only for work that was done, and check that each research question has a result, a discussion point, and a conclusion drawn from the same evidence.

### Phase 11 — 2026-09-25

**Completed.** Submission 1 was turned into a four-page IEEE conference paper. The literature review and methods were compressed. Results, discussion, limitations, and conclusions use only the completed analysis. Each research question has a result, a discussion point, and a conclusion in the traceability matrix. Word counted 4 pages, which is within the eight-page limit.

**Evidence.**

- `paper/Jawe_OPG_nonreceipt_KZN.docx`
- `paper/Jawe_OPG_nonreceipt_KZN.pdf`
- `paper/build_ieee.js`
- Traceability matrix in `specification/implementation_specification.md`

**Problems.**

- The separate rural-formal contrast could not be kept, and the paper says so.
- The calibration slope and the access predictors remain imprecise, and the paper says so.
- No ethics-approval letter is in the project record, so the paper does not claim that a DUT determination was granted.
- A review screen and a random forest were not built. The paper describes the command that was built.

**Decisions.** D-060. References [24] and [25] cite the grant-increase notices used for the ceilings.

**Next step.** The eleven phases in the study plan are complete. Anything further is optional: a reader trial of the files, the deferred random forest, or a review screen. None of those is required to answer the three research questions.

### October plan Phase 6 — earlier six-page Submission 2 review draft, 2026-10-11

This is Phase 6 of the uploaded October Streamlit implementation plan, not
the September study Phase 6 modelling sensitivities above. Historical
close-outs describe their dated state and are retained unchanged.

This D-061 close-out records the earlier six-page stage. D-062 and the expansion
close-out below describe the current eight-page integrated review draft. The
validation JSON is maintained for the current build.

**Completed.** The specification, checklist and traceability records now include
the implemented Streamlit interface and verified local functional evidence.
The manuscript revision connects concepts to measured predictors and updates
the artefact/evaluation discussion from these records. It preserves the
existing screen, cohort, primary six-slope model and sensitivity outputs; no
scientific model is refit for the writing task. The final review draft was built
as six Letter pages in two columns, with 10 pt body text and 8 pt tables/references,
five tables, two figures and 23 references numbered by first use.

**Evidence.**

- `paper/conceptual_framework.md`, `paper/results.md` and `paper/discussion.md`
- Revised assembly sources: `paper/manuscript.md` and `paper/build_ieee.js`
- Built review draft: `paper/Jawe_OPG_nonreceipt_KZN.docx` and matching PDF
- `paper/manuscript_validation.json`: six-page build/layout and citation-order
  evidence; 162 passed read-only scientific numerical checks
- `docs/current_state_audit.md` and `docs/model_decision_record.md`
- `docs/validation_summary.json`: full-reference app/CLI parity
- `docs/evidence_log.md`: 220 automated tests passed, zero reference mismatches
- `docs/windows_validation.json`: 50 checks of six synthetic report exports
- `examples/synthetic_report/`: preserved user-supplied synthetic exports

**Problems and limits.**

- The historical evaluation has 22 synthetic screening cases and four other
  checks, not 26 synthetic screening cases. The revised reporting separates
  these from the 220-test app suite and 50 Windows-report checks.
- Participant task testing has not been conducted. The user excluded it from
  the present revision; the prepared protocol is not an evaluation result.
- One user's Windows screenshots and report contents support local operation
  and export consistency, not broad usability acceptance or remote execution
  attestation. The synthetic 50% rate is not the research prevalence.
- The six-page count, mechanical citation ordering and layout checks are
  complete. Independent checks of bibliographic sources and official legal
  notices remain outstanding; these are not inferred from citation numbering.
- Ethics approval is not documented in the available project record and is
  not presented as granted.
- Public deployment and an exploratory random forest remain outside this
  revision. Existing respondent-level repository data/history must not be
  described as a cleared public demonstration package.

**Decisions.** D-061. Report only implemented capability and observed evidence.
Preserve the untested-usability, incomplete legal-screen and historical
generalisability limitations.

**Next step.** Review the six-page draft, independently verify references and
official notices, and resolve/document the applicable ethics status before any
external submission. Participant evaluation remains unperformed. Submission has
not been performed by this revision record.

### Submission 1 integration — eight-page review draft, 2026-10-11

**Completed.** The user authorized integrating Submission 1 into Submission 2
and expanding the paper to exactly eight pages. The source upload matches the
repository baseline PDF byte-for-byte (SHA-256
`6d6cac29f9a6d7cd07968f5ddb2ad2a38a69c82d19f208ae33f6c0cf2611fa32`).
The manuscript restores the approved original title, aim, objectives, review
approach and attributed proposal context, with fuller literature comparisons
and operationalization of the released survey fields. It adds literature,
data-operationalization, weighted descriptive-characteristics and
performance-uncertainty tables, plus conceptual-framework and cohort-flow
diagrams. The screen, cohort, frozen six-slope model and sensitivity outputs
remain unchanged; no scientific refit was performed.

**Evidence.**

- Integrated `paper/manuscript.md` and numbered manuscript source
- `paper/conceptual_framework.md`, `paper/results.md` and `paper/discussion.md`
- `paper/build_ieee.js` and figure sources
- Current `paper/Jawe_OPG_nonreceipt_KZN.docx` and tracked PDF: final render
  passed the check for exactly eight Letter pages; 4,988 manuscript words,
  two columns, nine tables, four figures, 25 references numbered by first use;
  10 pt body, 9 pt tables and 8 pt references
- `paper/manuscript_validation.json`: new render/page-count evidence and all
  209 independently verified scientific table values, consisting of the
  earlier 162 and 47 additional table-value checks
- Independent final visual review: all eight pages passed; nine tables and
  four figures are legible and unclipped, captions attached, with no blank
  pages or orphan headings. Final reference page is naturally partial
- Final PDF SHA-256:
  `0101c41c5332bc45def6f449ff5d5fbe88e86093adc88dfdf11e710b18548561`
- Original recorded functional evidence remains 220 automated app tests,
  zero mismatches over 15,388 reference records and 50 Windows-export checks;
  the 220-test suite and 50 Windows-report checks were not rerun for manuscript
  expansion

**Problems and limits.**

- The final manuscript word count is 4,988 by whitespace splitting, after
  removing a duplicated Discussion paragraph. The eight-page count, numerical
  audit and independent visual review apply to the final rendered PDF.
- Earlier proposal/sample counts are contextual and attributed to Submission 1;
  they are not replacements for the frozen empirical cohort denominators.
- Independent publisher and official legal-notice verification remains
  outstanding. Citation numbering alone does not establish source validity.
- Ethics confirmation is not documented. Participant usability remains
  unperformed by user instruction; no acceptance or external validation is
  claimed. The random forest remains deferred and no public site was deployed.

**Decisions.** D-062. Expand the manuscript and integrate the original proposal
without changing the substantive scientific result set or upgrading the scope
of the functional evidence.

**Next step.** Resolve independent source/legal-notice verification and ethics
confirmation. The integrated paper remains a review
draft; no external submission has occurred.
