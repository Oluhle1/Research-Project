# Research decision log

Deviations from Submission 1, resolutions of open parameters, and implementation clarifications are recorded here before they are used. A row is an instruction to the next phase. It is not a result.

**Source of truth:** `21634436_Oluhle_Jawe_Submission_1.pdf`.  
**Specification:** `specification/implementation_specification.md`.  
**Checklist:** `specification/checklist.md`.

D-062–D-073 record historical builds with their original counts and hashes;
D-073's 5,442/141/374-word build and 28 references are archived at `7d54c18`.
D-074 records the original 2014–2015 formula/rate-source closure: the four
standard-rate ceilings are verified, with the research proxy and age-rate
choice explicit. Point 3 is addressed within research scope, pending user
review; supervisor points 4–10 remain pending. Broader source/governance and
participant-usability limits remain open. There are 74 unique decision rows;
the checklist remains 96 rows: 94 Implemented, two Proposed and zero Verified.

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
| D-063 | 2026-10-11 | Targeted revision | Reporting | Apply the supplied P1–P5 revision plan by strengthening estimand/literature comparison, theory-to-finding synthesis, metric interpretation and sensitivity arguments. Preserve nine tables, four figures, all frozen scientific outputs and the eight-page limit. Correct the final title to APRE402 after explicit user confirmation. Add a portable claim verifier and 314-row source register: 209 numerical comparisons and 100 supporting checks pass; prior application tests remain historical evidence. | `paper/targeted_revision_plan.md`, `paper/targeted_revision_response.md`, `paper/claim_source_validation.json`, `paper/primary_source_audit.json`, and the final eight-page PDF. Three authentic local Stats SA PDFs were read; thirteen external-source requests failed with proxy CONNECT 403 and supplied no original article/legal text. | Adopted; P1–P4 and available evidence/render checks complete. P5 retains original-source, ethics/access/disclosure and portal-confirmation limits. No grade guarantee, participant study, refit or external submission |
| D-064 | 2026-10-13 | Plain-language revision | Reporting | Rewrite dense noun phrases as actions, use “I” for author choices and “you” for reader guidance, and explain necessary technical terms in parentheses at first use. Simplify headings, table text, captions and figure labels while retaining the approved title, APRE402, research questions, frozen results and legal/usability limits. Historical D-064 build: eight Letter pages, 5,632 manuscript words with a 263-word abstract, nine tables, four figures, 25 first-use references; body/table/reference fonts remain 10/9/8 pt. | User readability request; `paper/plain_language_revision.md` and `paper/plain_language_validation.json` review 90 terms and 16 scientific meanings. Retained-evidence audit passes 209 table and 100 supporting checks; four temporary negative controls reject false manuscript evidence. The 314-row source register retains four limitation rows. | Adopted; reporting/term/evidence checks complete. Scientific, model, application and dataset paths remain unchanged from `bfabb35`; no refit, app-suite rerun, participant study or new province analysis. P5 source/ethics/disclosure/portal limits remain open; no external submission |
| D-065 | 2026-10-13 | Professional-language revision | Reporting | Rewrite the readable paper in clear, concise professional language for conference review and ICT marking. Use concrete active subjects instead of author or direct-address pronouns; use past tense for completed methods and observed results, present tense for software/rules/tables/interpretation, and conditional language for future work. Retain first-use parenthetical definitions and all scientific qualifications. Historical D-065 build: eight Letter pages, 5,627 manuscript words with a 249-word abstract, nine tables, four figures and 25 first-use references; fonts remain 10/9/8 pt. | User request; `paper/professional_language_revision.md`, `paper/professional_language_validation.json` and `paper/manuscript_validation.json`. All 90 term and 16 scientific-meaning checks pass; 209 numerical and 100 supporting checks pass, with 314 register rows and four explicit limits; all four temporary negative controls are rejected. | Adopted; all eight fresh pages pass root and independent visual review. Scientific/model/app/data/reference/diagram/build-layout paths remain unchanged from `e70b300`; no app-suite run, refit, participant study, province extension, new primary-source read or external submission. P5 and source/ethics/disclosure/portal limits remain open |
| D-066 | 2026-10-13 | Specialist-audience revision | Reporting | Follow the user's explicit replacement of the define-every-term requirement: remove 52 elementary parenthetical glosses and condense abstract/theory/metric-definition prose, while retaining normal terminology, acronym expansions, study-specific assumptions and statistical interpretation. Present the literature opening as one paper's context, retaining the recorded 511-to-55 mixed-grant review flow and unavailable original search exports/logs. Historical D-066 build: 5,097 words, 141-word abstract, 530 fewer words than D-065; eight Letter pages, nine tables, four figures, 25 references and 10/9/8 pt fonts. | `paper/specialist_language_revision.md`, `paper/specialist_language_validation.json`, `paper/specialist_language_negative_controls.json` and current `paper/manuscript_validation.json`. All 16 scientific distinctions, 209 numerical comparisons and 100 supporting checks pass; 314 register rows retain four explicit limits; all four temporary negative controls pass without verifier changes. | Adopted; all eight fresh pages pass root and independent visual review. Scientific/app/data/model/reference/figure/build-layout paths remain unchanged from `17e1b053`. No app-suite run, refit, province extension, participant study, primary-source query, ethics/admin confirmation, deployment or external submission. P5 remains partial |
| D-067 | 2026-10-14 | Supervisor feedback point 1 | Reporting | Revise only Section II.A to state the research gap, clarify the literature-search reproducibility limits and explain the contribution relative to previous research. Retain documented databases, concepts and broad relevance criteria, the mixed-grant 511-to-55 flow, and the limits from unavailable queries/dates/filters/exports/item decisions/extraction register. Historical D-067 draft: 5,308 words, 141-word abstract, eight Letter pages, nine tables, four figures, 25 first-use references and unchanged 10/9/8 pt fonts. | User instruction to apply one point at a time; `paper/supervisor_feedback_response.md`, `paper/supervisor_point1_validation.json` and current `paper/manuscript_validation.json`. Retained-evidence audit passes 209 numerical and 100 supporting checks; 314 register rows retain four limits. Only II.A prose changed from `e83b504`; all other sections/table cells and scientific/app/data/model/reference/diagram/build/verifier-code paths remain unchanged. | Draft prepared; pending user review and acceptance before point 2. Root and independent visual review passed all eight final pages. Supervisor points 2–10 remain pending. No new negative controls, app suite, refit, search, source authentication, participant study, deployment or submission. P5/governance/source/usability limits unchanged |
| D-068 | 2026-10-14 | Conceptual-framework follow-up | Reporting | Apply only the user's three refinements: add 142-word Section II.D, distinguish conceptual and analytical layers in Figure 1, and add 109-word Section VI.E returning to supported, challenged and unresolved expectations. A dashed artefact boundary denotes implementation, not a causal factor. Historical D-068 draft: 5,423 words, 141-word abstract, eight Letter pages, nine tables, four figures, 25 references and unchanged 10/9/8 pt fonts/layout. | User's positive review of point 1 and explicit framework requests; `paper/conceptual_framework_revision.md`, `paper/conceptual_framework_validation.json`, `paper/supervisor_feedback_response.md` and current `paper/manuscript_validation.json`. Science/audience review and all 209 numerical plus 100 supporting checks pass; 314 register rows retain four limits. Table cells and scientific/app/model/data/reference/verifier paths remain unchanged from `1fe4820`; other figures remain unchanged. | Draft prepared for user review; root and independent visual reviews passed all eight final pages. Only the framework aspect of point 2 is addressed; Table II formatting and points 3–10 remain pending. No app suite, refit, negative-control rerun, source query, province extension, participant study, administrative confirmation, deployment or submission. P5/usability limits unchanged |
| D-069 | 2026-10-14 | Supervisor feedback point 2 | Reporting | Revise Table II's theoretical relationships and formatting only: demographic context for age/sex, learning-cost relevance for schooling, compliance-cost relevance for settlement/distance; preserve coding and measurement limits. State unmeasured psychological costs and five predictor groups/six slopes. Table II-only builder styling uses top/left-aligned 9 pt cells, black horizontal rules, no vertical grid, unsplit rows, repeating header and caption keep. Historical D-069 draft: 5,416 words, 141-word abstract, eight Letter pages, nine tables, four figures, 25 references and 10/9/8 pt fonts. | User accepted point 1 and framework refinements and authorised the next supervisor item; `paper/supervisor_point2_revision.md`, `paper/supervisor_point2_validation.json`, `paper/supervisor_feedback_response.md` and current `paper/manuscript_validation.json`. Independent scientific review and all 209 numerical plus 100 supporting checks pass; 314 register rows retain four limits. Only II.C/Table II reporting and scoped builder formatting change from `0dd3d0e`; all other tables, figure assets, sections, scientific/app/model/data/reference/verifier paths remain unchanged. | Draft prepared for user review; root and independent visual reviews passed all eight final pages. Supervisor points 3–10 remain pending. No app suite, refit, negative-control rerun, source query, figure regeneration, province extension, participant study, administrative confirmation, deployment or submission. P5/usability limits unchanged |
| D-070 | 2026-10-14 | Supervisor feedback point 3 | Reporting / verification | Clarify III.B's interview-period ceilings, conditional annual formula and R1,200 minimum, half-joint-income couple assumption and equality boundary. Distinguish marital research coding from legal spouse proof; require reciprocal resident different-person links and resolved applicant/spouse incomes, combine regardless of spouse age, preserve unresolved cases and known-FAIL priority, and keep receipt separate. Historical D-070 draft at `beec7d77`: 5,430 words, 141-word abstract, eight Letter pages, nine tables, four figures, 25 references and unchanged 10/9/8 pt fonts. | User approved point 2 and requested threshold/spouse verification; historical `paper/supervisor_point3_revision.md`, `paper/supervisor_point3_validation.json`, `paper/historical_screening_source_audit.md`/`.json`, `paper/supervisor_feedback_response.md` and `paper/manuscript_validation.json` at `beec7d77`. Arithmetic, code, local primary survey and independent scientific checks pass; 12 fresh official legal/rate requests returned HTTP 403 before origin text retrieval. All 209 numerical plus 100 supporting checks pass; 314 register rows retain four limits. Only III.B manuscript prose changes from `c95b786`; all other sections, tables, references, figures, builder, app/model/data/analysis/verifier paths remain unchanged. | Partially addressed; original notices, operative formula, R100 minimum-payment rule and legal spouse definition remain unverified. User review pending; root and independent visual reviews passed all eight final pages. Points 4–10 remain pending. No refit, app suite, new empirical analysis, participant study, administrative confirmation, deployment or submission; P5/usability limits unchanged |
| D-071 | 2026-10-15 | Supervisor point 3 legal follow-ups | Reporting / verification | Address the user's four legal follow-ups to original point 3. State what the audit verified and what it did not authenticate; explain combined spouse resources, survey omissions and conservative partnership handling as research choices. Historical D-071 at `214647e`: III.B 377 words, up from historical 356; 5,451 manuscript words, 141-word abstract, eight Letter pages, nine tables, four figures, 25 first-use references and 10/9/8 pt fonts. | `paper/legal_verification_followup.md`/`.json` and historical `paper/manuscript_validation.json` at `214647e`; five expanded public requests on 14 October and two exact user-provided URL requests on 15 October failed HTTP/proxy CONNECT 403 before primary text retrieval. The user's narrative, favicon links and candidate URLs do not authenticate clauses or amendments. Independent actual-diff/questionnaire-pages-5–6 review and root plus independent visual reviews of all eight D-071 renders pass. D-071 source-bound 209 numerical and 100 supporting checks pass; 314 register rows retain four limits. Only III.B prose changes from `beec7d77`; all nine table XML records, other sections, references, figures, builder, scientific/app/model/data/analysis/verifier paths remain unchanged. | Follow-ups 2 and 3 addressed within audit/research scope; critical 1 and 4 blocked by unavailable original notices/clauses and historical amendment/in-force chain. Original supervisor point 3 remains partial and awaits user review; points 4–10 remain pending. Review dated 15 October Africa/Johannesburg; D-071 retained renders retain 14 October UTC timestamps. No fresh app suite, rule run, refit, new empirical result, participant study, administrative confirmation, deployment or submission. D-062–D-070 and older source-attempt counts/hashes remain historical; P5/usability limits unchanged |
| D-072 | 2026-10-15 | Supervisor point 3 uploaded-source review | Reporting / verification | Read uploaded original legal sources and expose the historical formula conflict. GN R286/GG 34169 Schedule 2 uses 1.4A − 0.4B, effective 1 April 2011 under Schedule 4; GN R2119/GG 46459 Annexure A(2)/(5) uses 1.6A − 0.4B and R100 monthly minimum, commencing 31 May 2022 under regulation 41. Clarify III.B and VII's first paragraph, add direct references [26]/[27] and retain source PDFs; reference spacing after paragraphs changes 2.5 to 1 pt. Historical D-072 at `132e96c`: 5,457 words, 141-word abstract, 389-word III.B; eight Letter pages, nine tables, four figures, 27 references and 10/9/8 pt fonts. | `paper/uploaded_legal_source_audit.md`/`.json` and historical manuscript validation at `132e96c`. Supplied `415.pdf`/GG 31342 concerns banking/customs and is excluded; correct 2008 base GN R898/GG 31356 is identified but full text unread. Intervening formula amendments and original 2014/2015 rate notices remain missing. All nine table XML records, other prose/figures and scientific/app/model/data/analysis/verifier code remain unchanged from `214647e`; 209 numerical/100 supporting checks pass with zero failures, 314 register rows and four limits; root and independent all-eight-page visual reviews passed; independent uploaded-source/scientific reviews passed. | Original supervisor point 3 remains partial and awaits user review. Legal follow-ups 2/3 addressed within available evidence; historical verification criteria 1/4 incomplete. Supervisor points 4–10 pending. No science-code change, rule rerun, refit, app suite, new empirical result, participant study, administrative confirmation, deployment or external submission. D-062–D-071 counts/hashes/checks remain historical; 96 checklist rows remain 94 Implemented, two Proposed, zero Verified |
| D-073 | 2026-10-15 | Supervisor point 3 correct-2008-base review | Reporting / verification | Read correct GN R898/GG 31356, 22 August 2008 (81 pages): regulation 1 spouse definition; 18(2)/(3) joint income/desertion; 19(1) half-joint annual income; 20 deductions; 39 commencement; Annexure A(2) D = 1.3A − 0.5B and A(5) R100 monthly minimum. Distinguish 2008/2011/2022 formula and income-scope versions. Revise only III.B's threshold/partnership paragraphs, add stable source ID28 (published 26) and retain the source PDF; preserve frozen science, other sections, all nine tables/four figures and fonts. | `paper/historical_2008_source_audit.md`/`.json`; correct base SHA-256 `c54ce6e72a31430ddd4fe1c3a8177b113b8f56194856719e8652eb24c66b59c6`. Original PDF pages: spouse 15; joint income/desertion 40; annual half-joint income 41; deductions 45–46; commencement 73; formula 74–75; minimum 75. The 2008 list includes dependent-child/ex-gratia items absent from 2022, so version identity is not assumed. Operative 2014–2015 amendment/rate chain remains missing. Final 5442/141/374 words, eight Letter pages, nine tables, four figures and 28 references. All 209 numerical/100 supporting checks and both all-eight-page reviews pass; current audit binds artifact/source hashes. Final invisible balancing-paragraph height avoids blank page 9; fonts and reference spacing unchanged. | Legal criteria 1/4 remain partial; 2 accuracy and 3 research justification improved. Original supervisor point 3 partial and awaiting user review; supervisor points 4–10 pending. D-072 at `132e96c`, its original history and appended source supplements remain intact; D-062–D-072 counts/hashes/checks are historical. No rule rerun, refit, fresh app suite, new empirical result, participant study, administrative confirmation, deployment or submission claimed. Checklist unchanged: 96 rows, 94 Implemented, two Proposed, zero Verified |
| D-074 | 2026-10-15 | Supervisor point 3 historical-source closure | Reporting / verification | Authenticate original 2014–2015 standard rates and operative formula: GG 37474, 28 March 2014, page 3 GN 211 R1,350 from 1 April 2014; pages 4–5 Schedule paragraph 2 substitutes Annexure A(2), D = 1.6A − 0.4B, printed commencement paragraph 1 from 1 April 2014; GN 277/GG 38647, 30 March 2015, page 3 R1,410 from 1 April 2015. Read R621/GG 39007, 21 July 2015, which leaves OPG formula/means/spouse provisions unchanged. Retain verified R898/2008 A(5) R100 minimum, 19(1) half-joint income, 18(2)/(3) joint income/desertion and Agency approval, and regulation 1 spouse definition. Verify ceilings 61,800/123,600 and 64,680/129,360. Both rate notices include age-75+ R20; standard age-60–74 maximum across ages remains an explicit research choice and S1c unchanged. | `paper/historical_thresholds_verified_audit.md`/`.json`. The income proxy omits assets, deemed income and deductions; resident reciprocal spouse links are research consistency rules, not law; ambiguous/nonresident cases remain unresolved, not ineligible. Current manuscript 5,469/141/408 words, eight Letter pages, nine tables, four figures and 28 active first-use references. The fresh source-bound verifier passed 209 numerical and 100 supporting comparisons with zero failures, 314 register rows and four documented limits; root visual review passed all eight final pages. Fonts and builder are unchanged; 18 DOI references are retained. D-073's 5442/141/374 counts, 28 references and completed checks remain historical at 7d54c18. | Point 3 addressed within research scope, pending user review; points 4–10 pending. No code, rule, result or model change, refit, participant study, deployment or submission. Checklist unchanged: 96 rows, 94 Implemented, two Proposed, zero Verified. Decision table: 74 unique D-001–D-074 rows. |

## Phase close-outs

Close-outs through D-073 preserve their dated evidence and then-open source
gaps. D-074 below records the current closure; historical checks do not
certify the current manuscript build.

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

This D-061 close-out records the earlier six-page stage. D-062–D-066 record
later historical builds; D-067 describes the earlier supervisor point 1
draft. D-070 below identifies the current screening follow-up. The validation JSON is maintained for the latest build.

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

This D-062 close-out and its counts/hashes are historical. Later close-outs
record subsequent reporting revisions.

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
- D-062 `paper/Jawe_OPG_nonreceipt_KZN.docx` and tracked PDF: final render
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

### Targeted Submission 2 revision — 2026-10-11

This D-063 close-out records the historical 5,262-word build. D-064 records
the later historical plain-language build; D-070 records the current screening follow-up.

**Completed.** RQ1 now defines the screened/resolved historical estimand and
explains unresolved exclusion, consequential screen alternatives and qualified
Ralston/Godfrey scope comparisons. RQ2 separates AUC, AP, Brier and calibration,
returns to theory/proxy distinctions and evaluates S7–S11 without conflating
samples, weighted fitting, weighted evaluation or external validation. RQ3
distinguishes six verification layers and limits the completed evidence to its
tested conditions. The conclusion answers the same research questions.

**Evidence.** The paper has 5,262 whitespace-delimited words, nine unchanged
tables, four unchanged figures and 25 first-use references. The revised PDF
remains eight Letter pages, independently inspected without layout blockers.
APRE402 was confirmed by the user. The 314-row claim register and reusable
verifier passed 209 table comparisons plus 100 supporting checks. A deliberately
altered temporary manuscript was rejected. Existing 220-test, parity and Windows
results were checked as saved evidence; no application suite or model was rerun.

**Problems and limits.** Thirteen attempted original journal/index/government
reads failed at the outbound proxy; zero remote primary texts were accessed.
Three local authentic Stats SA documents support measurement definitions. DOI
agreement with Submission 1 is a bibliographic consistency check. The operative
formula/Annexure A, R100 payment boundary and couple-resource chain still require
original legal verification. The earlier review counts match the proposal, but
search exports and screening logs are unavailable. Institutional ethics,
access/disclosure clearance and official portal requirements remain unconfirmed.
Participant usability is unperformed by the user's scope direction.

**Decision.** D-063 changes interpretation and evidence traceability, without
changing the approved empirical design or claiming a predicted grade.

**Next step.** Author review and the recorded source/administrative confirmations
before formal submission. No submission or public deployment was performed.

### Plain-language Submission 2 revision — 2026-10-13

This D-064 close-out records the historical 5,632-word build, its 263-word
abstract and original source hash. D-070 below records the current screening follow-up.

**Completed.** The user requested readable prose rather than dense, abstract
phrases. The paper now uses active author actions, explains essential technical
terms in parentheses and guides readers with “you” where appropriate. Headings,
tables, captions and figure labels use simpler wording. The approved original
title, APRE402 and research questions remain. No frozen scientific result or
original application behaviour changed.

**Evidence.** The D-064 manuscript has 5,632 whitespace-delimited words and
a 263-word abstract. The rebuilt PDF has eight Letter pages, nine tables, four
figures and 25 first-use references, with 10/9/8 pt body/table/reference fonts.
`paper/manuscript_validation.json` records the latest build/layout checks.
`paper/plain_language_validation.json` reviews 90 essential terms and 16
scientific meanings. The retained-evidence verifier passes 209 numerical table
comparisons and 100 supporting checks; its 314-row register includes four
explicit limitation rows. It rejects four temporary negative controls: wrong
table count, wrong abstract AUC, false participant usability and false Table IX
evidence. Manuscript SHA-256:
`69b44ac75d1f4efb45d36cec4fa534b5cd53c7ffde17fc347e94c833a9cf9c93`.

**Problems and limits.** Sentence counts, term reviews and editing judgments
are not participant comprehension or usability measurements. The earlier 220
application tests, 15,388-record agreement and 50 Windows-report checks remain
saved evidence; they were not rerun. No model was refitted, other province
analysed, participant recruited, original publisher/legal source newly read,
public site deployed or paper externally submitted. Original-source
verification, ethics/access/disclosure and official portal confirmation remain
outstanding; P5 is still partial.

**Decision.** D-064 changes reporting clarity. Apparent eligibility, reported
receipt, prediction and legal entitlement remain separate. Discussion of
another province remains brainstorming and does not enter the findings.

**Next step.** Author review and the previously recorded source/administrative
confirmations before formal submission. D-062's 4,988 words and D-063's 5,262
words remain historical counts; current evidence files identify this revision.

### Professional-language Submission 2 revision — 2026-10-13

This D-065 close-out records the historical 5,627-word build, its 249-word
abstract and original source hash. D-070 below records the current screening follow-up.

**Completed.** Concrete subjects now describe the research and software actions
without author or direct-address pronouns. The paper uses past tense for
completed methods and observed findings, present tense for software behaviour,
rules, tables and interpretation, and conditional language for proposed work.
The wording remains clear and concise, with parenthetical technical definitions
at first use. The approved title, APRE402, research questions, results and
scientific qualifications remain unchanged.

**Evidence.** The final source contains 5,627 whitespace-delimited words and
a 249-word abstract. The regenerated PDF has eight US Letter pages, nine
tables, four figures and 25 references numbered by first use; body/table/
reference fonts remain 10/9/8 pt. Root and independent visual reviews pass
all eight fresh pages. `paper/manuscript_validation.json` records the latest
build. `paper/professional_language_validation.json` passes 90 term checks and
16 scientific-meaning checks. The retained-evidence audit passes 209 numerical
comparisons and 100 supporting checks, with 314 register rows and four explicit
limitations. Four temporary negative controls are rejected as expected in
`paper/professional_language_negative_controls.json`. Manuscript SHA-256:
`1f0080d9982dbe5a5d6b4f022b542341c343ca597338034fc714fd79a8f25df3`.

**Problems and limits.** Language review and manuscript consistency checks do
not establish participant comprehension or usability. The earlier 220 app
tests, 15,388-record agreement and 50 Windows-report checks remain historical
functional evidence. No app suite, model refit, province extension, participant
study, primary-source read, deployment or external submission occurred. P5
remains partial; journal/legal verification, ethics/access/disclosure and portal
requirements remain unconfirmed.

**Decision.** D-065 changes presentation for conference and marking review.
Scientific, model, app, data, reference, diagram and build-layout paths remain
unchanged from `e70b300895c9777067f5825abc25709b4a0e197d`.

**Next step.** Author review and the previously recorded source/administrative
confirmations before formal submission. D-062's 4,988 words, D-063's 5,262
words and D-064's 5,632 words and their source hashes remain historical records.

### Specialist-audience and integrated-literature revision — 2026-10-13

This D-066 close-out records the historical 5,097-word build and source hash.
Its generated artifacts and audits remain in Git commit `e83b504`. D-067 below
records the historical supervisor point 1 draft. D-068 below identifies the
historical framework follow-up; D-070 identifies the current screening follow-up.

**Completed.** The user's specialist-audience instruction replaces the earlier
requirement to define every technical term. The revision removes 52 elementary
parenthetical glosses and condenses abstract, theory and metric-definition
prose. Standard terminology, acronym expansions, operational assumptions and
metric interpretation remain. Active subjects and appropriate tense continue.
The literature opening presents the study as one paper; the recorded 511-to-55
flow remains mixed-grant literature, with original search exports and screening
logs unavailable for independent verification.

**Evidence.** The D-066 manuscript contains 5,097 whitespace-delimited words
and a 141-word abstract, 530 words fewer than D-065. The regenerated PDF has
eight US Letter pages, nine tables, four figures and 25 first-use references,
with unchanged 10/9/8 pt body/table/reference fonts and layout. Root and
independent visual reviews pass all eight fresh pages. The current
`paper/manuscript_validation.json` records render and final visual-review
evidence. `paper/specialist_language_validation.json` passes 16 scientific-
distinction checks. The retained-evidence audit passes 209 numerical comparisons
and 100 supporting checks, with 314 register rows and four explicit limitations.
All four temporary controls pass in
`paper/specialist_language_negative_controls.json`; the verifier is unchanged.
D-066 manuscript SHA-256:
`3dac12bcb9fd9ba60c05c64fa683a8e61e065b575c8c70a6e0a18f3fe8cd7ee3`.

**Problems and limits.** Editing and scientific-consistency checks do not test
participant comprehension or usability. The earlier 90-term definition review
belongs to the historical D-064/D-065 builds, not the current acceptance rule.
The recorded review flow is retained evidence, not a newly repeated search.
P5 remains partial; original-source and legal authentication, ethics/access,
historical-data disclosure and portal requirements remain unconfirmed.

**Decision.** D-066 changes reporting for specialist readers and integrates the
literature context. Scientific, application, data, model, reference, figure and
build-layout paths remain unchanged from
`17e1b0536ec4f683d2a04e5caced2bb89635a943`. No app suite, model refit,
other-province analysis, participant study, primary-source query, deployment or
external submission occurred.

**Next step.** Author review and the previously recorded source/administrative
confirmations before formal submission. D-062–D-065 counts and hashes remain
historical; D-066 audit records identify that earlier build. D-067 below
identifies the earlier point 1 draft; D-070 records the current screening follow-up.

### Supervisor feedback point 1 — 2026-10-14

This D-067 close-out records the historical 5,308-word draft at `1fe4820`.
The user later reviewed it positively and requested the follow-up in D-068.
The original counts, scope and hash remain evidence for that stage.

**Draft prepared.** Section II.A now explains the research gap and specific
contribution relative to prior studies. It retains the documented relevance
criteria and thematic narrative synthesis, and details the unavailable search
records that prevent independent reproduction and verification of selection.
The recorded 511-to-55 flow remains mixed-grant evidence. No new search,
exhaustive-coverage claim or universal novelty claim follows.

**Evidence.** The D-067 draft contains 5,308 whitespace-delimited words and a
141-word abstract. The render has eight US Letter pages, nine tables, four
figures and 25 first-use references with unchanged 10/9/8 pt fonts. Root and
independent reviewers passed all eight final pages.
`paper/manuscript_validation.json` records the completed render and layout review.
`paper/supervisor_feedback_response.md` and
`paper/supervisor_point1_validation.json` document point 1's response and scope.
All 209 numerical comparisons and 100 supporting checks pass. The 314-row
source register retains four limitation rows. Manuscript SHA-256:
`bf897e564f37e3d3dc19176a796eae3f8fea04c2392156dccf90163913e4e91a`.

**Problems and limits.** Query strings, search dates and filters, exports,
item-level screening/exclusion decisions and the 55-source extraction register
remain unavailable. P5 original-source/legal, ethics/access/disclosure and
portal limits remain unchanged. Participant usability is still unperformed.
The supervisor's remaining nine corrections have not been applied.

**Decision.** D-067 covers point 1 only. All text outside II.A and all table
cells remain byte-identical to `e83b504fb124d6bf5f384a656f52ed2a7bd45a11`.
Scientific, app, data, model, reference, figure, build and verifier-code paths
remain unchanged. No negative controls, app suite or model refit reran; prior
controls and functional checks remain historical. No province extension,
participant study, primary-source query, deployment or submission occurred.

**Next step.** User review and acceptance of point 1 before point 2. Supervisor
points 2–10 remained pending at this stage. D-062–D-066 retain historical
counts and hashes; the audit files in `1fe4820` identify this point 1 draft.

### Conceptual-framework follow-up — 2026-10-14

This D-068 close-out records the historical 5,423-word draft at `0dd3d0e`.
The user later accepted these refinements and authorised point 2, recorded in
D-069 below. The original counts, scope and hashes remain historical evidence.

**Draft prepared.** The user positively reviewed point 1 and authorised three
specific refinements. Section II.D now connects the social problem, theory,
observable screening, predictor proxies and artefact implementation in 142
words. Figure 1 distinguishes theory from measurements, screen decisions,
reported receipt, weighted description and held-out prediction. The dashed
artefact boundary identifies implementation rather than a causal variable.
Section VI.E returns to this framework in 109 words: screening and demographic
comparison provide analytical support, schooling challenges a simple expectation,
geographical/compliance expectations remain unresolved, and psychological costs
remain untested. Traceable software contributes despite those limits.

**Evidence.** The D-068 source has 5,423 whitespace-delimited words and a
141-word abstract. The PDF has eight US Letter pages, nine tables, four figures
and 25 first-use references; fonts remain 10/9/8 pt and build layout is unchanged.
Root and independent reviewers passed all eight final pages;
`paper/manuscript_validation.json` records the completed render and review.
Scientific and specialist-audience reviews pass, as do all 209 numerical
comparisons and 100 supporting checks. The 314-row register retains four limits.
The current revision and validation records are
`paper/conceptual_framework_revision.md`,
`paper/conceptual_framework_validation.json` and
`paper/supervisor_feedback_response.md`. Manuscript SHA-256:
`1fcaa1d081dbdabe3de4ed7e21ebc601a9a73b8adf3a81078a77b75bec654b49`.
PDF SHA-256:
`9a75be43b0f4f18ef9c0cb4b2aa3119cf9b0468e3cfeb69cdacbaef4506e5211`.

**Problems and limits.** Proxy associations do not directly test administrative
burden. Schooling and demographic findings do not establish mechanisms;
imprecise geographical associations do not rule out compliance costs.
Participant usability, external validation and P5 source/governance questions
remain open. These editing and consistency checks add no human evaluation.

**Decision.** D-068 covers the three authorised framework refinements only.
Section II.A, all table cells, methods, software evaluation, numerical results,
limitations, conclusion and references remain unchanged from `1fe4820`.
Changes concern II.C/II.D, moved VI.B material and VI.E, Figure 1 and its
generator, working mirrors, records and audits. Other figures and app/model/
data/verifier paths remain unchanged. No app suite, refit, negative-control
rerun, new source query, province analysis, participant study, administrative
confirmation, deployment or external submission occurred.

**Next step.** User review of this follow-up before further feedback work.
Point 2's framework aspect is addressed, but Table II formatting remains
pending; supervisor points 3–10 remain pending. The checklist stays at
94 Implemented, two Proposed and zero Verified across 96 rows. D-062–D-067
counts and hashes remain historical.

### Supervisor feedback point 2 — 2026-10-14

This D-069 close-out records the historical 5,416-word draft at `c95b786`.
The user subsequently approved point 2 and requested point 3, recorded in
D-070 below. Original counts, scope and hashes remain historical evidence.

**Draft prepared.** Following the user's acceptance of point 1 and the
framework refinements, D-069 addresses Table II's conceptual relationships
and formatting. Its II.C introduction, caption, headers and five rows now
identify demographic context, learning-cost relevance and compliance-cost
relevance. Operational coding and explicit measurement limits remain. The
note identifies unmeasured psychological costs and five predictor groups
with six slopes.

**Evidence.** The D-069 source has 5,416 whitespace-delimited words and a
141-word abstract. The PDF has eight US Letter pages, nine tables, four
figures and 25 first-use references with 10/9/8 pt fonts. Root and independent
reviewers passed all eight final pages; `paper/manuscript_validation.json`
records the completed render and review. Independent scientific review,
all 209 numerical comparisons and 100 supporting checks pass; the 314-row
register retains four limits.
`paper/supervisor_point2_revision.md`,
`paper/supervisor_point2_validation.json` and
`paper/supervisor_feedback_response.md` identify the current response and scope.
Manuscript SHA-256:
`38e4f3b65619d30593c278dbc9827615a7907dc60fde1e97ff31c57430924c69`.
PDF SHA-256:
`1e71b7185884430d14be0cac5d28a22ae789963ab3badb397693747f59d196ef`.
Word SHA-256:
`9862d9aacefcbfdc09ea0ad95a5dcc8e2f3c4512082a6c0f3298e90101bd0669`.

**Problems and limits.** Theory-related predictor roles do not establish
measured burden or causal mechanisms. Psychological costs remain unmeasured.
Participant usability and P5 source, ethics/access/disclosure and portal
questions remain open; no new human or external validation follows.

**Decision.** Point 2 changes only II.C/Table II reporting, its working mirror
and scoped Word-builder formatting, plus current records and audits. Table II
uses left/top-aligned 9 pt cells, black horizontal rules without a vertical
grid, unsplit rows, a repeating header and caption keep. The other eight tables,
all other sections, II.D, VI.E, Figure 1, other figures, references, scientific
outputs and app/model/data/verifier paths remain unchanged from `0dd3d0e6cba7b31aef469bcaefdea6770a09a817`.
No app suite, refit, negative-control rerun, new source query, figure generation,
province analysis, participant study, administrative confirmation, deployment
or external submission occurred.

**Next step.** User review of point 2 before applying the next supervisor item.
Points 3–10 remain pending. The checklist remains 96 rows: 94 Implemented,
two Proposed and zero Verified. D-062–D-068 counts and hashes remain historical.

### Supervisor feedback point 3 — 2026-10-14

This D-070 entry describes the historical build at
`beec7d77c0e32b24b636f3f337ccc5545d899fd1`. Its 5,430-word count, hashes and
completed reviews remain historical. D-071 below records the historical follow-up;
D-072 records the historical uploaded-source review; D-073 records the current 2008-base review.

**Partially addressed.** After approving point 2, the user requested III.B's
threshold and spouse verification. D-070 clarifies the coded annual ceilings
and interview periods, conditional D = 1.6A − 0.4B derivation, minimum annual
R1,200 payment, half-joint-income couple assumption and inclusive equality
boundary. Marital answers select research rules, not legally verified spouse
status. Both incomes must be resolved; reciprocal resident different-person
household links are required, and spouse income enters regardless of age.
Ambiguous partnerships and deficient links remain unresolved. Known failures
retain priority and reported receipt remains separate after PASS.

**Evidence.** Arithmetic, code, local primary survey-document and independent
scientific checks pass.
Twelve fresh official legal/rate requests failed with HTTP 403 before origin
text retrieval. The D-070 source has 5,430 whitespace-delimited words and a
141-word abstract; the PDF has eight US Letter pages, nine tables, four figures,
25 first-use references and 10/9/8 pt fonts. Root and independent reviewers
passed all eight final pages; the `paper/manuscript_validation.json` at `beec7d77` records the
completed render and review. All 209 numerical comparisons and 100
supporting checks pass; the 314-row register retains four limits. Historical
records are `paper/supervisor_point3_revision.md`,
`paper/supervisor_point3_validation.json`,
`paper/historical_screening_source_audit.md`/`.json` and
`paper/supervisor_feedback_response.md`. Manuscript SHA-256:
`ff5bab12dc7c0dfe85ff3911a87a197c6569819ec91c98239d8a4b4f95836b8e`.
PDF SHA-256:
`ec7f77f3e9f06618ff9b9dc85624aad39e12be7240612948182772b0ae61b5c4`.
Word SHA-256:
`39635c5ed5471ef84c416b0775a5cc3f35e763d033e0a5b6f2bb10e00d2e3af8`.

**Problems and limits.** The original official notices, operative formula,
R100 minimum-payment rule and legal spouse definition remain unverified.
Correct arithmetic and consistent implementation do not authenticate legal
entitlement. No source metadata or legal proof was invented. Participant
usability and P5 source, ethics/access/disclosure and portal limits remain open.

**Decision.** Only III.B manuscript prose changes from `c95b786e075f38843478ec690cb2d296e1172be7`.
Other sections, tables, references, figures, builder, scientific outputs and
app/model/data/analysis/verifier paths remain unchanged. Supporting rulebook
and phase-specification caveat notes may link the audit without changing rules.
No refit, app-suite run, new empirical analysis, figure regeneration, province
extension, participant study, administrative confirmation, deployment or
external submission occurred.

**Next step.** User review of point 3; original legal verification remains open.
Points 4–10 remain pending. Checklist counts remain 96 rows: 94 Implemented,
two Proposed and zero Verified. D-062–D-069 counts and hashes remain historical.

### Supervisor point 3 legal-verification follow-up — 2026-10-15

This D-071 entry records the historical draft at
`214647e42adad9a20a30461d4026e1f93732ae7a`. Its 5,451-word count, 377-word
III.B, hashes and completed checks remain historical. D-072 below records the
historical uploaded-source review; D-073 records the current 2008-base review.

**Partially addressed.** D-071 addresses four legal follow-ups to original
supervisor point 3: authenticate the 2014–2015 thresholds and exact provisions;
state accurately what is verified and uncertain; justify spouse resources and
marital ambiguity while distinguishing legal rules from research assumptions;
and strengthen historical references with their amendment/in-force chain.
The fourth request is not supervisor feedback point 4.

**Evidence.** III.B now says that the audit verified arithmetic, coded
ceilings and LCS partnership items, without authenticating the notices or
applicable formula, minimum-payment and spouse provisions. It explains why
resolved spouse income enters regardless of age, why residence/reciprocity
check research consistency and why unavailable nonresident partner income
remains unresolved. Questionnaire pages 5–6 confirm the partnership items and
omission of spouse details for separated respondents; cohabitation does not
establish the legal classification. Independent review of the actual diff and
questionnaire passed. Root and independent reviewers passed all eight current
retained page images on 15 October (Africa/Johannesburg); retained render
timestamps remain 14 October UTC. III.B is clear on pages 3–4 and the retained
tables, figures, synthesis and references remain intact.

The D-071 source has 5,451 whitespace-delimited words, a 141-word abstract
and 377-word III.B (historical D-070: 5,430/141/356). The PDF remains eight
US Letter pages with nine tables, four figures, 25 first-use references and
10/9/8 pt fonts. All 209 numerical comparisons and 100 supporting checks
pass, bound to the current source; 314 register rows retain four limits.
Historical records at `214647e` are `paper/legal_verification_followup.md`/`.json`
and `paper/manuscript_validation.json`. Manuscript SHA-256:
`ca9c2564b7d2fe0f3173ef5c6a4e0654dc90b015c205be093743c8e5849f3c24`.
PDF SHA-256:
`12c857141c3341bf33da314c7264893c361b652bdd3e499b5d0f29cba5ccef07`.
Word SHA-256:
`cd6e002e74c83bc180bce0b15c25376fb3bf0434e83eddb0849f827049f1a930`.

**Problems and limits.** Five expanded public requests on 14 October (three
government sources, SAFLII index and Acts index) failed HTTP 403. Both exact
user-provided URLs fetched on 15 October also failed proxy CONNECT 403:
`https://www.saflii.org/za/gaz/ZAGovGaz/2008/415.pdf` and
`https://www.acts.co.za/social_assistance_act_2004/r898_19__determination_of_means`.
The user's confirmation narrative and favicon links do not supply clause text
or amendment history; the URLs identify candidate sources whose bodies were
not retrieved. No exact provision or 2014–2015 in-force chain was authenticated.
These seven follow-up attempts are distinct from the retained D-070 twelve
and older P5 thirteen. Participant usability and P5 governance/source limits
remain open.

**Decision.** Follow-ups 2 and 3 are addressed within audit/research scope;
critical follow-ups 1 and 4 remain blocked. Only III.B manuscript prose changes
from `beec7d77c0e32b24b636f3f337ccc5545d899fd1`. All nine table XML records,
other sections, references, figures, builder and scientific/app/model/data/
analysis/verifier paths remain unchanged. No fresh app suite, rule run,
refit, new empirical result, figure regeneration, province extension,
participant study, administrative confirmation, deployment or external
submission occurred. No legal proof or reference metadata was invented.

**Next step.** User review of original supervisor point 3; primary clauses and
the historical amendment/in-force chain are still required for legal
authentication. Supervisor points 4–10 remain pending. Checklist counts
remain 96 rows: 94 Implemented, two Proposed and zero Verified. D-062–D-070
counts, hashes and earlier reviews remain historical; the decision table now
contains 71 unique D-001–D-071 rows.

### Supervisor point 3 uploaded legal-source review — 2026-10-15

This D-072 entry records the historical stage at
`132e96cee7d7b3b6f5d5b91a214590359a25d210`: 5,457 manuscript words,
389-word III.B, 27 references and the original hashes/checks. Its source audit
and appended supplements remain intact; D-073 below records the current
correct-2008-base review.

**Partially addressed.** D-072 records the user's uploaded original legal
documents and the current revision from `214647e42adad9a20a30461d4026e1f93732ae7a`.
GN R286, Gazette 34169, Schedule 2 specifies D = 1.4A − 0.4B; Schedule 4
sets 1 April 2011 as the effective date. GN R2119, Gazette 46459 (2022),
Annexure A(2)/(5) specifies D = 1.6A − 0.4B and the R100 monthly minimum;
regulation 41 commences the regulations on 31 May 2022. Reading these texts
authenticates those provisions and dates, while revealing that the later
coefficient cannot alone validate the 2014–2015 research screen.

**Evidence.** `paper/uploaded_legal_source_audit.md`/`.json` record original
source readings, retained PDF copies and the distinction between primary text,
identified sources and unresolved history. III.B identifies both formula
versions and explicitly conditions estimates on the research ceilings.
Section VII's first paragraph repeats the historical limitation. References
[26] and [27] directly cite the original 2011 and 2022 documents. The D-072
manuscript contains 5,457 whitespace-delimited words, a 141-word abstract and
389-word III.B; the PDF has eight US Letter pages, nine tables, four figures,
27 first-use references and 10/9/8 pt fonts. Reference-paragraph after-spacing
reduces from 2.5 to 1 pt. The D-072 source-bound verifier passes 209 numerical
comparisons and 100 supporting checks, with zero failures, 314 register rows
and four limits. Root and independent visual reviews passed all eight final
page images: III.B's threshold paragraph is on page 3 and spouse paragraph on
page 4; VII and all 27 references fit on page 8 without overlap or clipping.
All nine tables and four figures remain legible. Independent uploaded-source/scientific reviews
passed. D-072 results are retained in `paper/manuscript_validation.json`
and the uploaded-source audit at `132e96c`, while D-071 checks remain historical.
Manuscript SHA-256:
`835aee47d51197b7e4f63b0b33390e4727ab1c3bf6b4e78745b57ebdc2c1b381`.
PDF SHA-256:
`95369d879c84faf5343ca224ff2a003100ff6c0ebbc9fc16527f3ff6ae9b7f8a`.
Word SHA-256:
`b9c72c650d5262234ab56d02eba16ad5b90dca8d32dc4132275cd13c8816d260`.

**Problems and limits.** The uploaded `415.pdf`, Gazette 31342, concerns
banking/customs and is excluded from social-assistance evidence. Correct base
GN R898, Gazette 31356 (2008), is identified but its full text remains unread.
The intervening formula/amendment chain and authenticated original 2014/2015
rate notices remain missing. Three uploaded PDFs were read, two with relevant
primary legal text; no official copy was independently retrieved. The main review used uploaded files;
a parallel government/gazette-mirror search failed with CONNECT 403 before any
original text was obtained. Legal follow-ups 1 and 4 therefore remain
historically incomplete; 2 and 3 are addressed within the accuracy/research
rationale scope. No historical applicability was inferred from the 2022 text.
P5 source/governance and participant-usability limits remain open.

**Decision.** Change only III.B and Section VII's first paragraph, add the
two direct legal references/source copies and reduce reference after-spacing.
All nine table XML records, other sections and figure assets, scientific
outputs and app/model/data/analysis/verifier code remain unchanged. No
scientific code change, rule rerun, refit, app suite, new empirical result,
participant study, administrative confirmation, deployment or external
submission occurred.

**Next step.** User review
of original supervisor point 3; obtain the missing historical originals and
amendments before claiming 2014–2015 legal authentication. Supervisor points
4–10 remain pending; the user's fourth legal criterion is distinct from
supervisor point 4. Checklist counts remain 96 rows: 94 Implemented, two
Proposed and zero Verified. D-062–D-071 counts, hashes and reviews remain
historical; the decision table now contains 72 unique D-001–D-072 rows.

### Supervisor point 3 correct 2008 base review — 2026-10-15

This D-073 close-out is archived at `7d54c18`: 5,442 manuscript words,
141-word abstract, 374-word III.B and 28 references. Its then-missing
survey-period sources and pending next step are superseded by D-074 below.

**Partially addressed.** D-073 records reading the correct GN R898,
Gazette 31356, 22 August 2008 (81-page source), rather than the excluded
banking/customs `415.pdf`/GG 31342. Source SHA-256:
`c54ce6e72a31430ddd4fe1c3a8177b113b8f56194856719e8652eb24c66b59c6`.
`paper/historical_2008_source_audit.md`/`.json` record the read original
provisions. This supplies the base text missing at historical D-072;
it does not complete the amendments effective during the LCS interviews.

**Evidence.** Regulation 1 supplies the original spouse definition (PDF
page 15); 18(2)/(3) joint income/desertion (40); 19(1) half-joint annual
income (41); 20 deductions (45–46). Regulation 39 commences the instrument
on 22 August 2008 (73). Annexure A(2) specifies D = 1.3A − 0.5B (74–75),
and A(5) the R100 monthly minimum (75). The 2008 income scope includes
dependent-child/ex-gratia items absent from the 2022 list. Original content
is checked by version, without treating the later list as the earlier one.
The planned manuscript change is limited to III.B's two threshold/partnership
paragraphs, source (stable ID28/published 26) and the retained source PDF. Frozen science,
other sections, all nine tables/four figures and fonts remain unchanged.
Final manuscript counts, artifact hashes, current-source audits and visual reviews passed as recorded below; D-072's
5,457/141/389 counts and completed checks remain historical at `132e96c`.

**Problems and limits.** The verified printed formulas are 2008
1.3A − 0.5B, 2011 1.4A − 0.4B and 2022 1.6A − 0.4B. The operative
2014–2015 amendment chain, including relevant means/spouse wording, and
authenticated original rate notices remain missing. Original base clauses
strengthen legal-source and research-rationale discussion without proving
their unchanged force during the survey. User legal criteria 1 and 4 remain
partial; criterion 2 receives accurate version wording and 3 improved research
justification. Original supervisor point 3 remains partial; points 4–10 pending.
P5 source/governance and participant-usability limits remain open.

**Decision.** Preserve the coded research ceilings, screening logic and frozen
scientific outputs while making source/version limits explicit. No rule rerun,
model refit, fresh app suite, new empirical result, participant study,
administrative confirmation, deployment or external submission is claimed.
D-072's original history and appended source supplements remain intact.

**Next step.** Review point3 with the user; obtain the missing operative-period amendments and rate originals.
The user's fourth legal criterion remains distinct from supervisor point 4.
Checklist counts remain 96 rows: 94 Implemented, two Proposed and zero
Verified. The decision table contains 73 unique D-001–D-073 rows;
D-062–D-072 manuscript counts, hashes and completed checks remain historical.

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

### Supervisor point 3 source closure — 2026-10-15

**Addressed within research scope, pending user review.** D-074 verifies the
original 2014 formula and rate, 2015 rate, R100 minimum and half-joint-income
basis for all four standard-rate ceilings. R621/2015 leaves the relevant OPG
formula/means/spouse provisions unchanged. Evidence and exact pages are in
`paper/historical_thresholds_verified_audit.md`/`.json` and decision D-074 above.

Both notices include the age-75+ R20 supplement. Using the standard maximum
across ages remains an explicit research choice; S1c and frozen outputs are
unchanged. Assets, deemed income and deductions remain outside the proxy;
resident reciprocal spouse linkage is a research consistency rule. Unresolved
ambiguous/nonresident cases do not establish legal ineligibility.

**Current build.** 5,469 manuscript words, 141-word abstract,
408-word III.B, eight Letter pages, nine tables, four figures and 28 active
first-use references. The fresh source-bound verifier passed **209 numerical
and 100 supporting comparisons**, with **zero failures, 314 register rows
and four documented limits**. Root visual review passed all eight final pages.
Fonts and builder are unchanged; 18 DOI references are retained. The decision table has 74 unique
rows; checklist statuses remain 94 Implemented, two Proposed and zero Verified.
Points 4–10 await their own review. No code, rule, model or result change follows.
