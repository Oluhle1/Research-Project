# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—This study analysed reported Older Person’s Grant (OPG) non-receipt among adults aged 60 or older in KwaZulu-Natal (KZN), using the Living Conditions Survey (LCS) 2014/2015. The study used administrative-burden theory to choose predictors and observable research rules to identify apparently eligible adults. Screening did not establish legal entitlement. Among 1,013 adults who passed with resolved receipt, 67 reported non-receipt: 6.6% unweighted and 7.5% person-weighted. Alternative screening rules gave weighted rates of 7.1%–9.1%. Logistic regression used five predictor groups and household-held-out validation. AUC (area under the receiver operating characteristic curve) was 0.752; average precision (AP) was 0.203. The Brier score was 0.0578, compared with 0.0618 for an intercept-only reference using training-group prevalence. Checks supported reproducibility. The application displays rules, decisions, scores and reports. No participant study tested ease of use. These results do not establish entitlement, explain non-receipt, or demonstrate performance elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [1], including during crises [2]. Prior studies examine rural pension receipt [3] and household grant receipt [4]. This study examines reported non-receipt among older adults who pass a research eligibility screen.

Screening, reported receipt and legal entitlement remain distinct. Passing observable research conditions does not establish a South African Social Security Agency decision [5]. Missing spouse resources and unresolved responses change the denominator, whose construction must precede estimation.

This study develops and evaluates an interpretable research artefact using the Living Conditions Survey (LCS) 2014/2015 in KwaZulu-Natal. It documents cohort construction, estimates weighted non-receipt, tests predictions in held-out households and verifies computational correctness, reproducibility and inspectability.

RQ1 asks how common reported non-receipt is among screen-PASS adults with resolved receipt and how screening alternatives change that proportion. RQ2 evaluates logistic discrimination and probability accuracy in held-out households. RQ3 asks whether the artefact reproduces the analysis and clearly presents screening decisions and model outputs; participant usability remains untested.

## II. Related Work and Predictor Selection

### A. Review Approach, Programme Context and Research Gap

The narrative review drew on Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst. Searches covered social assistance, eligibility, take-up, non-receipt, exclusion and prediction. Studies differed in programme, population, unit and outcome, preventing pooled estimates.

Review records report 511 items: 136 duplicates removed, 375 titles/abstracts screened, 222 exclusions, 153 full-text assessments, 98 further exclusions and 55 retained sources across grants and populations. Queries, search dates/filters, exports, item-level decisions and the full extraction register are unavailable. These aggregate counts cannot establish reproducible selection or exhaustive coverage.

Table I distinguishes individual receipt [3] from household proportions [4], and this study’s provincial resource screen from both. Other-grant studies separate enquiry, application, receipt and uninterrupted payment [6], [7], [8].

TABLE: Table I. Evidence scope informing the study
| Study | Grant / people studied / measure | Contribution and transfer limit |
| --- | --- | --- |
| Ralston et al. [3] | Pension; rural older person; receipt | Selection by age in rural Agincourt differs from this study’s resource screen. |
| Godfrey et al. [4] | Grants; Msunduzi household; receipt proportions | Local household findings cannot directly explain individual receipt. |
| Case et al. [6]; Zembe-Mkabile et al. [7] | Child Support Grant (CSG); enquiry/application and infant receipt | Separates access steps; cannot estimate OPG non-receipt. |
| Heinrich and Brill [8]; Gibbs et al. [9]; Majola and Maharaj [10] | CSG; interruption and application experiences | Receipt can still require costly effort. |
| Gazeaud [11] | Targeting assistance using survey measures; resources | Supports checking income assumptions; cannot set South African legal limits. |

Gazeaud motivates income sensitivity [11]; Mabala studies a different grant and age group [12]. Neither establishes OPG eligibility.

Cited studies do not directly show how resource, partnership and grant-compatibility assumptions shape provincial person-level non-receipt estimates. This study connects explicit screening, sensitivity analysis, weighted description and household-held-out prediction through shared rules and inspectable software. Its contribution concerns measurement and reproducibility, rather than statutory entitlement or access mechanisms.

### B. Grant Access and Administrative Burden

Administrative-burden theory distinguishes learning, compliance and psychological costs [13]. Grant studies describe paperwork, repeated visits, interrupted payments and difficult encounters [8], [9], [10], [14]. Child Support Grant research suggests barriers [6], [7], without establishing their effects among older OPG applicants. Digital access can create difficulties [15]. Low non-receipt therefore does not demonstrate easy access.

The screen operationalises observable age, resources, partnership and grant-compatibility rules while retaining unresolved information. Screening status and reported receipt remain separate. Only screen-PASS adults with resolved receipt enter descriptive and predictive analyses; unclear or contradictory receipt responses remain unresolved.

### C. Predictor Selection and Software Design

Table II separates demographic context from circumstances relevant to learning and compliance costs. These predictors do not directly measure administrative burden or establish why a person reports non-receipt.

TABLE: Table II. Administrative-burden theory and predictor selection
| Predictor | Theoretical role | LCS coding and limit |
| --- | --- | --- |
| Age | Demographic context: receipt differs by age [3] | Per decade above 60; health and application history unmeasured. |
| Sex | Demographic context: receipt differs by sex [3], [4] | Female versus male; social roles and discrimination unmeasured. |
| Schooling | Learning costs: schooling may help people find and understand grant information [10], [13] | Below Grade 7 versus Grade 7 or above; awareness and literacy unmeasured. |
| Settlement | Compliance costs: place may shape service access [6], [14], [15] | Urban informal and traditional/rural formal, each versus urban formal; office capacity unmeasured. |
| Office distance | Compliance costs: distance may add travel effort [10], [14] | At least 5 km/unavailable versus nearer than 5 km; visits and travel costs unmeasured. |

NOTE: Psychological costs are unmeasured. Settlement contributes two contrasts, giving five predictor groups and six slopes.

Rare outcomes require precision–recall assessment alongside discrimination and calibration [16], [17]. Sample size limits precision [18]; household grouping constrains validation [19]. TRIPOD informed prediction reporting [20]. Software verification and participant usability require different evidence.

### D. Conceptual Framework

Reported non-receipt motivates an administrative-burden perspective. Figure 1 links theory to LCS proxies, with age and sex as demographic context. Observable screening is necessary because age alone cannot define eligibility and LCS omits legal conditions. Resource, partnership and grant-compatibility rules define the population; reported receipt defines the outcome. Person weights describe non-receipt; unweighted household-held-out validation assesses prediction. The artefact implements this design through shared rules, frozen scoring and inspectable reports. Application scores remain separate from held-out evaluation and never change screening or receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual framework. Theory informs predictor selection; observable screening defines the population for separate descriptive and predictive analyses. The dashed boundary identifies the artefact’s implementation scope. Arrows show conceptual rationale or analytical dependencies, not causal effects.

## III. Methods

### A. Data and study population

The analysis linked LCS 2014/2015 person, household and person-income files using survey identifiers, checking duplicates, unmatched records and row counts. Questionnaire, metadata and COICOP (Classification of Individual Consumption According to Purpose) codes guided interpretation [21], [22], [23]. The study included sampled KwaZulu-Natal residents aged 60+; the household survey excludes institutional residents. Screening used interview-month rules. Statistics South Africa had hot-deck-imputed age and sex before release, without record-level flags. Model preprocessing addressed missing predictors separately. Aggregating income before linkage preserved person-level records (Table III).

TABLE: Table III. How each data field enters the analysis
| Data concept | LCS measurement | Use and restriction |
| --- | --- | --- |
| Person/household identifiers | Household and person codes | Link files, identify spouses and keep households together for model checks; excluded from model inputs and public reports. |
| Age/province | Completed years; province code | Select KZN adults aged 60+; model also uses age. |
| Partnership | Marital/resident-partner answers; spouse identifier | Select resource rule and link spouses; excluded from primary model. |
| Resources | Yearly income items and source schedule | Screen using estimated private resources; no allocation of household income. |
| OPG receipt | General grant/OPG answers and skipped questions | Define outcome after PASS; exclude receipt and derived labels from predictors. |
| Other/prior grants | Own grants; preceding-year OPG income | Check incompatible grants and reporting periods; excluded from predictors. |
| Schooling/sex/place | Education, sex, settlement, office distance | Primary predictors; fill missing values using training data only. |
| Weight/design | Person weight; derived survey group | Describe population and test alternatives; excluded from primary predictors. |

NOTE: Released documentation supports these field uses [21], [22], [23]. Filling missing model predictors never changes screening fields or receipt answers.

### B. Screening rules and receipt outcome

The screen summed already annualised, nominal person-income amounts, excluding social-assistance income. It did not allocate household income. A missing applicant or linked-spouse amount remained unresolved unless the no-income response and absent schedule supported zero. Assets, deemed income and permitted deductions were outside this research proxy.

GN 211 set the standard monthly maximum at R1,350 from 1 April 2014 [24]; GN 277 raised it to R1,410 from 1 April 2015 [25]. The 2014 amendment, Schedule paragraph 2, substituted D = 1.6A − 0.4B from 1 April 2014 [26]. With annual standard maximum A and minimum D = R1,200 (Annexure A(5)) [27], B = (1.6A − 1,200)/0.4. This yields annual single/couple research ceilings of R61,800/R123,600 for October 2014–March 2015 and R64,680/R129,360 for April–October 2015. Half-joint income doubles couple limits; equality passed. The screen applied these boundaries to its private-income proxy. Both notices add R20 for age 75+; the primary screen retained the standard maximum across ages, while S1c tested the supplement. S1 also tested period and payment-boundary alternatives.

The 2008 regulations define spouses (regulation 1), include spouse income regardless of property regime (18(2)) and use half-joint annual income (19(1)). They allow Agency-approved exclusion after continuous desertion for at least three months and unwillingness to support (18(3)) [27]. The July 2015 amendment left these OPG means provisions unchanged [28]. Survey responses established neither legal spouse status nor desertion conditions. Never-married, widowed and divorced adults used single ceilings. For married adults, research rules required resolved applicant/spouse incomes and reciprocal pointers linking a resident spouse; sums applied regardless of spouse age. Nonresident spouse income was unavailable; separated respondents lacked spouse details [23]. Cohabitation, unspecified status and missing/inconsistent links remained unresolved, without assumed single status or zero partner income. S2 tested alternatives.

An adult's reported disability or war-veterans grant caused FAIL. Caregiver child grants and grant-in-aid neither excluded the adult nor defined OPG receipt. A known failure took priority over unresolved information; the screen retained all reasons.

For adults who passed, the software interpreted general-grant and OPG answers together, including structural skips (questions omitted because earlier answers make them inapplicable). A consistent “no grant” answer can establish non-receipt when the OPG follow-up does not apply. Contradictory or unexplained answers remain unresolved and exclude the person from modelling. The analysis flagged disagreements between current receipt and preceding-year OPG income without changing the outcome because the periods differ. Rule version opg-kzn-primary-v1 records these decisions. The denominator contains adults who pass and have a clear receipt answer.

### C. Survey-weighted description and uncertainty

RQ1 reported unweighted and person-weighted non-receipt, p = Σ(wᵢYᵢ)/Σwᵢ, where Yᵢ = 1 denotes non-receipt and wᵢ is the person weight. Group comparisons were descriptive. For the weighted proportion, a with-replacement linearisation approximation clustered by derived primary sampling unit (PSU; first 11 household-ID digits) supplied the standard error (SE); 95% intervals used p ± 1.96SE. Unreleased strata prevented full survey-design variance estimation. Adults with unresolved screening remained outside the denominator. Receipt bounds assigned all unresolved PASS outcomes first to receipt, then to non-receipt.

### D. Model specification and validation

An unweighted, unpenalised logistic regression estimated reported non-receipt using five predictor groups, six slopes and an intercept (Table II). There was no class rebalancing, automated variable selection or cutoff optimisation. Income, receipt, derived outcome labels and marital status were excluded from primary predictors.

The attempted seven-slope model contained one rural-formal non-recipient; holding out that adult left no training event in that category. Decision D-052 combined rural formal with traditional settlement to support estimation, without treating the settings as equivalent. This outcome-informed choice was not nested within validation; performance remains conditional on the retained specification.

The 1,013 adults formed 827 households, including 182 with multiple included adults and six with both outcomes. Five folds stratified sorted households by any member’s non-receipt, keeping household members together (seed 201415). Each iteration trained on four folds and predicted the fifth. Held-out folds contained 199–207 adults and 12–14 events; age, sex and settlement were complete, with predictor missingness reported in Table V. Training sets supplied the age median and categorical modes used to impute training and held-out predictors before constructing fixed contrasts; ties selected the smallest code sorted as text. Fixed coding handled structural skips. Eligibility, receipt and weights were not imputed. Each adult received one out-of-fold (OOF) probability; the reference used the corresponding training-set event rate.

Pooled OOF predictions supplied unweighted average precision, AUC, Brier score and calibration measures. Calibration-in-the-large estimated an intercept correction with slope fixed at 1; ideal intercept and slope values were zero and 1. In 1,000 bootstrap draws, 827 households were sampled with replacement, retaining all included members and repeated selections. Outcomes and fixed OOF/reference probabilities stayed paired. Metrics, including calibration regressions, were recalculated; 2.5th/97.5th percentiles formed 95% intervals, with 1,000 valid draws per reported metric. Predictive models, imputers, folds and the settlement revision were not repeated. These conditional intervals omit variability from repeating model development or fold assignment, leave dependence from shared training data unaddressed, and do not reproduce the survey design or establish external performance.

### E. Alternative assumptions

S1–S6 varied thresholds, partnership, other-grant rules, income definition, receipt period and unresolved-receipt bounds. Each recorded cohort size, events, unweighted/person-weighted rates and internal predictive performance; unchanged cohorts retained primary OOF results. S7 used complete cases; S8 replaced welfare access with a married indicator. S9 fitted frequency-weighted regression while retaining unweighted imputation and evaluation; it was not a survey-design regression. S10 weighted primary OOF metrics without refitting; S11 grouped folds by derived PSU. These analyses remained separate from primary results.

## IV. Software and Evaluation

The command-line interface (CLI), python analysis/run_study.py, reproduces linkage, screening, description and held-out evaluation. Run records store versions, settings, seed, folds and checksums. The app loads JSON coefficients and imputation statistics from opg-kzn-six-slope-v1, fitted to the full cohort. Uploads never retrain it.

The Streamlit app accepts opg-screen-v1 CSVs, including members needed for spouse linkage. It rejects schema/context errors, duplicate identifiers and invalid values. Uploads are limited to 20 MiB/50,000 rows and remain in session memory. Views and exports omit submitted identifiers, raw income and household links. Filters preserve the full resolved-PASS summary denominator.

FIGURE: figures/architecture.png | Fig. 2. Research and app workflows share screening rules. Household-held-out predictions remain separate from app scores calculated using the model trained on all included adults.

Only supported PASS adults with resolved receipt receive scores; partially missing predictors use frozen statistics, while records missing every categorical predictor remain unscored. Integrity checks bind model/evaluation files to code. Historical OOF results remain distinct from uploaded scores; uploaded records may overlap training data. CSV, JSON and ZIP exports include classifications, reasons, probabilities, versions and audit manifests. The synthetic MVP excludes survey records, historical respondent outputs and Git history.

Technical checks covered expected decisions, excluded predictors, linkage, repeatability, exports, saved-score parity and invalid/stale interface states. The owner’s Windows walkthrough confirmed synthetic execution and report generation, without independent participant evidence.

An unused protocol proposes synthetic tasks for three to five consenting participants, measuring completion, time, errors, ease and assistance. No participant usability or acceptance results exist; automated checks establish program behaviour.

## V. Results

### A. Study group and reported non-receipt

The survey included 15,388 people in 3,686 KwaZulu-Natal households (Table IV). Adults aged 60+ partition into failed, unresolved and passed groups; receipt partitions PASS. Household counts can overlap across rows. Of 117 failures, 93 exceeded the income ceiling and 25 reported disability grants; one met both conditions. None reported war-veterans grants. Of 187 unresolved adults, 105 were married, mostly with non-resident spouses, and 63 reported living together. Unresolved adults outnumbered non-recipients.

TABLE: Table IV. KwaZulu-Natal study group at each screening step
| Step | People | Households |
| --- | --- | --- |
| KwaZulu-Natal respondents | 15,388 | 3,686 |
| Aged 60 or older | 1,317 | 1,068 |
| Failed observable rule | 117 | 98 |
| Eligibility unresolved | 187 | 168 |
| PASS and resolved receipt | 1,013 | 827 |
| Reported receipt | 946 | 773 |
| Reported non-receipt | 67 | 60 |

NOTE: Person counts partition as 117 + 187 + 1,013 among adults aged 60+, then 946 + 67 within PASS. Adding all rows double-counts adults. Household counts are distinct within rows and do not form the same partition.

FIGURE: figures/cohort_flow.png | Fig. 3. FAIL, UNRESOLVED and PASS groups do not overlap. All 1,013 PASS adults resolve receipt and enter the final denominator.

Among 1,013 resolved passes, 67 reported non-receipt: 6.61% unweighted and 7.49% person-weighted. A PSU-clustered normal approximation across 345 PSUs gave SE 1.3 percentage points and a 95% interval of 4.9%–10.0%. Missing strata prevent full survey-design inference; this approximation does not supply intervals for Tables V–VIII. Current receipt matched preceding-year OPG income throughout. Table V describes pre-imputation composition within receipt groups, rather than non-receipt rates or predictions, and reports no standard errors.

TABLE: Table V. Characteristics by receipt, before filling missing values
| Characteristic | Recipients | Non-recipients |
| --- | --- | --- |
| Age, average years | 70.4; 69.8 | 67.3; 68.4 |
| Female | 686 (72.5%); 70.4% | 33 (49.3%); 53.4% |
| Grade 7 or above | 290 (30.7%); 33.0% | 49 (73.1%); 80.8% |
| Urban formal settlement | 284 (30.0%); 36.2% | 38 (56.7%); 66.2% |
| Office ≥5 km or unavailable | 717 (75.8%); 72.0% | 34 (50.7%); 40.3% |

NOTE: Recipients: 946; non-recipients: 67. Entries give unweighted then person-weighted means, or unweighted counts/within-group percentages then weighted percentages. Denominators retain three recipients missing schooling and 14 recipients/four non-recipients missing office-distance values. These describe group composition, without uncertainty intervals.

Unweighted non-recipients were younger, more often men, more educated and more often urban-formal residents. Weighting reduced the age difference. No between-group tests were performed.

### B. Screening sensitivity

Table VI reports scenario denominators, events, unweighted/person-weighted prevalence and unweighted OOF performance. Weighted prevalence ranged from 7.12% to 9.06%; AUC ranged from 0.736 to 0.763. Sensitivity performance entries are point estimates without intervals; similar AUC neither equates screened populations nor validates a screening rule.

TABLE: Table VI. Screening changes, non-receipt rates and held-out point estimates
| ID | N/events | Unw. | Wtd. | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- | --- |
| S0 | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S1b,d | 1,015/69 | 6.80 | 7.68 | .763 | .0584 | .875 |
| S2a | 1,072/71 | 6.62 | 7.42 | .749 | .0588 | .779 |
| S2b | 1,073/69 | 6.43 | 7.17 | .756 | .0564 | .841 |
| S2c | 1,021/67 | 6.56 | 7.43 | .753 | .0571 | .839 |
| S2d | 1,081/69 | 6.38 | 7.12 | .751 | .0565 | .808 |
| S3 | 1,032/82 | 7.95 | 9.06 | .736 | .0682 | .864 |
| S4b | 1,007/67 | 6.65 | 7.55 | .755 | .0576 | .854 |
| Same* | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |

NOTE: Events are reported non-recipients. Unw./Wtd. denote unweighted/person-weighted percentages. AUC, Brier and calibration slope are unweighted OOF point estimates without intervals. Same* repeats S0 for unchanged scenarios.

S1b applies the 2015 ceiling throughout; S1d uses the zero-payment boundary. These distinct settings produced identical results. S2a/S2b treat living-together adults as couples/single; S2c treats separated adults as single; S2d treats both as single. S3 retains disability/war-veterans recipients, adding no veterans. S4b includes social-assistance income.

*Unchanged scenarios: S1a applies the 2014 ceiling throughout; S1c adds the age-75 supplement; S4a adjusts income for prices with unchanged ceilings; S4c excludes UIF and similar transfers; S5 uses preceding-year receipt. S6a/S6b assign unresolved PASS receipt to receipt/non-receipt; no such cases occurred. Each retains the S0 denominator, events and measures.

### C. Predictive performance and associations

Predictive performance uses OOF probabilities; associations use the full-cohort fit. Neither establishes causal mechanisms, temporal ordering or intervention effects.

All five folds converged. Figure 4 uses five similarly sized bins. The highest bin had average prediction 0.188 and 35/203 non-recipients (17.2%); the lowest had average 0.0107 and 3/206 non-recipients (1.5%).

TABLE: Table VII. Primary held-out performance and resampling intervals
| Metric | Logistic model | Intercept-only |
| --- | --- | --- |
| AUC | .752 [.687–.814] | — |
| Average precision | .203 [.139–.292] | — |
| Brier score | .0578 [.0448–.0706] | .0618 [.0467–.0758] |
| Calibration-in-the-large | .020 [−.316–.273] | .0001 |
| Calibration slope | .836 [.591–1.133] | — |

NOTE: Brackets give conditional 95% percentile intervals from 1,000 household resamples of fixed OOF predictions (1,013 people/67 events); each interval had 1,000 valid, zero invalid draws. Predictive models and imputers were not refitted. These differ from the PSU approximation in V.A and full-fit Wald intervals below. The reference uses training-fold prevalence; its .0001 calibration-in-the-large has no saved interval. Dashes indicate unavailable measures. Ideal calibration intercept/slope values are 0/1.

FIGURE: figures/calibration.png | Fig. 4. Saved group summaries show unweighted OOF calibration. Labels give events/people; the diagonal shows exact agreement between average predictions and observed rates. Plot range: 0–0.22.


Full-cohort adjusted odds ratios were 0.39 for women versus men (Wald interval 0.23–0.66) and 0.24 for schooling below Grade 7 versus Grade 7 or above (0.13–0.43). Age, settlement and office-distance intervals included 1. These exploratory model-based intervals omit household clustering, survey design and specification-selection uncertainty. They describe odds associations, rather than probability changes, held-out performance or causal effects.

TABLE: Table VIII. Model and validation sensitivities, as point estimates
| Scenario | N/events | Unw. | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- |
| S0 primary | 1,013/67 | 6.61 | .752 | .0578 | .836 |
| S7 complete | 992/63 | 6.35 | .758 | .0556 | .819 |
| S8 married | 1,013/67 | 6.61 | .755 | .0578 | .846 |
| S9 wtd. fit | 1,013/67 | 6.61 | .750 | .0583 | .718 |
| S10 wtd. measures | 1,013/67 | 6.61 | .763 | .0641 | .935 |
| S11 PSU folds | 1,013/67 | 6.61 | .758 | .0575 | .860 |

NOTE: Unw. is the unweighted non-receipt percentage; performance entries have no intervals. S8–S11 retain weighted non-receipt of 7.49%. S7 removes 21 adults/four events lacking usable schooling or distance. S8 substitutes marriage for office distance, retaining six slopes. S9 uses frequency-weighted fitting with unweighted imputation/evaluation, not full survey-design regression. S10 weights primary OOF predictions without refitting; S11 changes fold grouping to derived PSU.

Table VIII changes sample, predictors or evaluation, rather than estimating effects. Its point estimates do not establish a preferred specification.

### D. Software verification

Table IX summarises 26 original checks: 22 synthetic screening cases, two income-schedule checks, one forbidden-predictor check and one run trace. Two research runs produced 14 byte-identical files and preserved the cohort checksum.

TABLE: Table IX. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Check rules, schedules, excluded predictors and run tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Check software, app state and exports; includes 18 Streamlit interface tests. |
| App–command agreement | 15,388/15,388 agree; 1,013 scored | Both paths select the same people and give the same decisions, receipt, reasons and outcome. |
| Reloaded model scores | Maximum score difference 5.55 × 10⁻¹⁷ | Reloading preserves saved-model scores; this does not assess OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Check synthetic local use and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The owner’s Windows walkthrough exercised six synthetic classifications. Six extracted reports passed 50 checks of outputs, summaries, checksums and versions. The ZIP container itself was not inspected. This supports local technical functionality, without independent execution or participant-usability evidence.

## VI. Discussion

### A. Scope of measured non-receipt

RQ1 measures non-receipt among historical KwaZulu-Natal adults who pass the screen and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. This does not measure unlawful denial or non-receipt among everyone legally entitled. The 187 unresolved adults outnumbered the 67 events. Excluding them changes the population described, regardless of sampling uncertainty. Stable estimates cannot reveal their receipt.

S2d added 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly changed the denominator. S3 retained adults with incompatible grants, added 19 people/15 events and raised non-receipt to 9.06%, the largest tested change. Table VI gives AUC, Brier and slope as point estimates on those changed denominators, without intervals. Similar AUC cannot justify screening rules or establish equivalent populations. Ralston studies rural age-eligible people [3]; Godfrey studies households' grants [4]. Different units, programmes, screens and places prevent direct comparison of their percentages. This study adds a provincial estimate with an explicit resource screen. High receipt can involve access costs [13], [14]; it cannot prove low burden.

### B. Predictive performance and interpretation

AUC 0.752 indicates ranking discrimination, rather than cutoff accuracy. AP 0.203 summarises precision–recall across thresholds, rather than precision at one cutoff [16]. Brier fell from 0.0618 to 0.0578, a modest 0.0040 reduction. No paired interval was calculated for that reduction; it remains a descriptive comparison. Calibration-in-the-large 0.020 estimates an intercept correction with slope fixed at 1; an interval spanning the ideal zero does not prove calibration. Slope 0.836 suggests overly extreme predictions, but its 0.591–1.133 interval includes 1 [17]. Only 67 events informed evaluation [18], and most adults in the highest-risk bin reported receipt.

Household resampling, the PSU survey approximation and full-fit Wald intervals address different uncertainties. None converts predictive discrimination or fitted associations into effects of sex, schooling, settlement or office distance.

Table VIII separates sample, predictor and evaluation changes. S7’s lower Brier concerns a different sample (992/63), not evidence that imputation harms prediction. S8 substitutes marriage for office distance. S9 weights fitting only; S10 weights the same OOF predictions, raising Brier to 0.0641. S11 changes grouping to derived PSU. S8–S11 retain 1,013 adults/67 events. These internal checks do not establish specification superiority or performance elsewhere [19], [20].

### C. Technical verification, separate from usability

RQ3 concerns reproducibility and inspectable explanations. Table IX supports technical correctness within tested conditions: synthetic cases check rules, repeated files check repeatability, interface–command agreement checks screening/receipt outputs, and model reload checks serialization. The owner’s walkthrough confirms local synthetic execution. Versioned sources and validation records support scrutiny; these checks do not establish independent user comprehension.

Historical OOF evaluation remains separate from uploaded full-data scores, whose records may overlap training data. Reload agreement verifies stored predictions, rather than new predictive accuracy or user understanding.

Participant usability remains untested. The unused protocol proposes independent participants, with task completion, time, errors, ease and assistance measures. Automated Streamlit checks and the developer’s walkthrough cannot establish usability or field acceptance.

### D. Transfer to other settings

This study covers screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in services, policy and reporting; administrative application, award and payment records measure other outcomes. No independent province, period or administrative sample validated the model. Transfer requires comparable populations, period-specific screening and independent discrimination/calibration checks [19], [20].

### E. Synthesis of the Conceptual Framework

Returning to Figure 1, screening sensitivity shows why the denominator requires explicit assumptions. Sex differences describe demographic associations without establishing burden mechanisms [3], [4]. Lower schooling accompanied receipt, contrary to the expectation that fewer information resources increase non-receipt [13]. Selection or other resources could explain this finding; neither explanation was tested. Office-distance and settlement intervals included 1, leaving compliance-cost expectations unresolved. LCS did not measure psychological costs. The artefact implements these bounded measurements through separate, traceable rules, outcomes and predictions. It supports inspection of the framework without establishing causes, statutory entitlement or participant usability.

## VII. Limitations and Ethics

The research proxy omits assets, deemed income and deductions and cannot establish statutory eligibility. Income/receipt misreporting, cross-sectional ordering, few events, unresolved screening and missing strata limit interpretation. Fixed-prediction resampling omits repeated model-development uncertainty; coefficient intervals condition on the selected specification. Household sampling excludes institutionalised older adults. Participant usability and external predictive performance remain untested.

This DUT honours study uses existing LCS 2014/2015 microdata without contacting respondents. Access and disclosure conditions still apply. Public demonstrations use synthetic records; controlled reference-parity tests also used the research data. The downloadable package excludes survey records, and app displays/exports omit submitted identifiers and raw income. These controls do not establish disclosure review or release permission for historical repository files.

The project record contains no DUT-IREC clearance number, faculty or departmental determination, or gatekeeper letter. The study therefore claims no approval, exemption or consent determination. Confirmation of the applicable institutional ethics route and secondary-data governance remains outstanding. These requirements are separate from the technical controls above. The application supports research analysis and does not determine grant entitlement.

## VIII. Conclusion

Screened historical non-receipt was 6.6% unweighted and 7.5% person-weighted; alternatives gave 7.1%–9.1%. Grant-compatibility and partnership assumptions changed the population described. Five predictor groups/six slopes gave AUC 0.752, AP 0.203 and Brier 0.0578, supporting moderate internal ranking and a small descriptive probability-error reduction.

The contribution integrates transparent screening, interpretable prediction and reproducible software for the same adults. Separate rules, unresolved cases, outcomes and scores make the path from survey measurement to displayed result inspectable. This provides a historical benchmark and an implementable analytical design, without establishing legal entitlement, causal barriers, participant usability or external validity.


## References

[1] T. Raniga and B. Simpson, “Poverty, HIV/AIDS and the old age pension in Bhambayi, KwaZulu-Natal, South Africa,” Develop. Southern Afr., vol. 28, no. 1, pp. 75–85, Mar. 2011, doi: 10.1080/0376835X.2011.545171.

[2] M. Alloush, J. R. Bloem, and J. G. Malacarne, “Social protection amid a crisis: New evidence from South Africa’s Older Person’s Grant,” World Bank Econ. Rev., vol. 38, no. 2, pp. 371–393, Apr. 2024, doi: 10.1093/wber/lhad037.

[3] M. Ralston, E. Schatz, J. Menken, F. X. Gómez-Olivé, and S. Tollman, “Who benefits—or does not—from South Africa’s old age pension? Evidence from characteristics of rural pensioners and non-pensioners,” Int. J. Environ. Res. Public Health, vol. 13, no. 1, Jan. 2016, Art. no. 85, doi: 10.3390/ijerph13010085.

[4] E. B. Godfrey et al., “Which eligible households get grants? Demographic correlates of receipt in South Africa,” Develop. Southern Afr., vol. 33, no. 6, pp. 774–789, Nov. 2016, doi: 10.1080/0376835X.2016.1231059.

[5] Republic of South Africa, Social Assistance Act 13 of 2004, Government Gazette 26446, Jun. 10, 2004.

[6] A. Case, V. Hosegood, and F. Lund, “The reach and impact of Child Support Grants: Evidence from KwaZulu-Natal,” Develop. Southern Afr., vol. 22, no. 4, pp. 467–482, Oct. 2005, doi: 10.1080/03768350500322925.

[7] W. Zembe-Mkabile, T. Doherty, D. Sanders, and D. Jackson, “Child Support Grant access and receipt among 12-week-old infants in an urban township setting in South Africa,” Global Health Action, vol. 7, no. 1, Aug. 2014, Art. no. 25310, doi: 10.3402/gha.v7.25310.

[8] C. J. Heinrich and R. Brill, “Stopped in the name of the law: Administrative burden and its implications for cash transfer program effectiveness,” World Develop., vol. 72, pp. 277–295, Aug. 2015, doi: 10.1016/j.worlddev.2015.03.015.

[9] A. Gibbs, L. Washington, N. Jama Shai, Y. Sikweyiya, and S. Willan, “Systematically excluded: Young women’s experiences of accessing child support grants in South Africa,” Global Public Health, vol. 13, no. 12, pp. 1820–1830, Mar. 2018, doi: 10.1080/17441692.2018.1449231.

[10] T. N. Majola and P. Maharaj, “The challenges associated with the Child Support Grant application process: A case of young mothers in a South African township,” J. Social Service Res., vol. 51, nos. 5–6, pp. 1140–1150, May 2025, doi: 10.1080/01488376.2025.2502004.

[11] J. Gazeaud, “Proxy means testing vulnerability to measurement errors?,” J. Develop. Stud., vol. 56, no. 11, pp. 2113–2133, Jan. 2020, doi: 10.1080/00220388.2020.1715942.

[12] M. T. Mabala, “Factors associated with social grant uptake in South Africa: A closer look at the Special COVID-19 Social Relief of Distress Grant among the youth aged 18–35 years,” M.A. research report, School Social Sci., Univ. Witwatersrand, Johannesburg, South Africa, Aug. 2023. [Online]. Available: https://hdl.handle.net/10539/40003

[13] D. P. Moynihan, P. Herd, and H. Harvey, “Administrative burden: Learning, psychological, and compliance costs in citizen-state interactions,” J. Public Admin. Res. Theory, vol. 25, no. 1, pp. 43–69, Jan. 2015, doi: 10.1093/jopart/muu009.

[14] S. Granlund, “They are not leaving without their money: Exploring encounters with the state through cash transfers in the rural Eastern Cape, South Africa,” Southern Afr. J. Social Work Social Develop., vol. 34, no. 1, Apr. 2022, Art. no. 9052, doi: 10.25159/2708-9355/9052.

[15] A. N. Vujovic, G. M. Jonathan, and S. Hacks, “Digitalisation and its impact on social protection programmes effectiveness: A case from South Africa,” Procedia Comput. Sci., vol. 237, pp. 882–890, 2024, doi: 10.1016/j.procs.2024.05.177.

[16] T. Saito and M. Rehmsmeier, “The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,” PLOS ONE, vol. 10, no. 3, Mar. 2015, Art. no. e0118432, doi: 10.1371/journal.pone.0118432.

[17] B. Van Calster et al., “Calibration: The Achilles heel of predictive analytics,” BMC Med., vol. 17, no. 1, Dec. 2019, Art. no. 230, doi: 10.1186/s12916-019-1466-7.

[18] R. D. Riley et al., “Minimum sample size for developing a multivariable prediction model: Part II—binary and time-to-event outcomes,” Statist. Med., vol. 38, no. 7, pp. 1276–1296, Mar. 2019, doi: 10.1002/sim.7992.

[19] D. R. Roberts et al., “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” Ecography, vol. 40, no. 8, pp. 913–929, Mar. 2017, doi: 10.1111/ecog.02881.

[20] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, “Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement,” Ann. Internal Med., vol. 162, no. 1, pp. 55–63, Jan. 2015, doi: 10.7326/M14-0697.

[21] Statistics South Africa, “Living Conditions Survey 2014/2015: Metadata,” Pretoria, South Africa, Statistical Release P0310, 2017.

[22] Statistics South Africa, “COICOP codes,” Pretoria, South Africa, Living Conditions Survey 2014/2015 code list. (n.d.).

[23] Statistics South Africa, “Living Conditions Survey 2014/2015: Household questionnaire,” Pretoria, South Africa. (n.d.).

[24] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 211, Government Gazette 37474, p. 3, Mar. 28, 2014.

[25] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 277, Government Gazette 38647, p. 3, Mar. 30, 2015.

[26] Dept. of Social Development, “Amendment: Social Assistance Regulations,” Government Notice R211, Government Gazette 37474, pp. 4–5, Mar. 28, 2014.

[27] Dept. of Social Development, “Social Assistance Act: Regulations,” Government Notice R898, Government Gazette 31356, Aug. 22, 2008.

[28] Dept. of Social Development, “Amendment: Social Assistance Regulations,” Government Notice R621, Government Gazette 39007, Jul. 21, 2015.
