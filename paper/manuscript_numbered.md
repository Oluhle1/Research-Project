# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—This study analysed reported Older Person’s Grant (OPG) non-receipt among adults aged 60 or older in KwaZulu-Natal (KZN), using the Living Conditions Survey (LCS) 2014/2015. The study used administrative-burden theory to choose predictors and observable research rules to identify apparently eligible adults. Screening did not establish legal entitlement. Among 1,013 adults who passed with resolved receipt, 67 reported non-receipt: 6.6% unweighted and 7.5% person-weighted. Alternative screening rules gave weighted rates of 7.1%–9.1%. Logistic regression used five predictor groups and household-held-out validation. AUC (area under the receiver operating characteristic curve) was 0.752; average precision (AP) was 0.203. The Brier score was 0.0578, compared with 0.0618 for an intercept-only reference using training-group prevalence. Checks supported reproducibility. The application displays rules, decisions, scores and reports. No participant study tested ease of use. These results do not establish entitlement, explain non-receipt, or demonstrate performance elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [1], including during crises [2]. Other work examines receipt and access barriers [3], [4]. This study examines adults who appear eligible but report receiving no OPG.

Screening, reported receipt and legal entitlement remain distinct. Passing the research screen does not establish a South African Social Security Agency decision [5]. Missing spouse resources and unresolved answers can change the screened denominator and its non-receipt proportion.

This study develops and evaluates an interpretable research tool using LCS 2014/2015 in KwaZulu-Natal. It documents cohort construction, describes person-weighted non-receipt, validates predictions in held-out households and assesses correctness, reproducibility and clarity.

RQ1 asks how common reported non-receipt is among screened adults and how alternative rules change it. RQ2 assesses prediction in held-out households. RQ3 assesses whether the tool reproduces the analysis and clearly presents screening and model outputs; participant usability remains untested.

## II. Related Work and Predictor Selection

### A. Review Approach, Programme Context and Research Gap

The structured narrative review examined grant access, eligibility measurement and prediction using Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst. Search concepts included social assistance, eligibility, take-up, non-receipt, exclusion and prediction. Selection considered relevance to the research question, population, outcome and methodological contribution.

The searches identified 511 records. Removing 136 duplicates left 375 records for title and abstract screening; 222 were excluded. Full-text assessment of the remaining 153 records excluded 98 and retained 55 sources across grants and populations. Supplementary Table S5 provides the eight recorded search strings, search date and source-specific counts. The synthesis compared programme, setting, unit of analysis, outcome definition, findings and limitations; these differences prevented a pooled estimate.

Table I distinguishes individual receipt [3] from household proportions [4], and this study’s provincial resource screen from both. Other-grant studies separate enquiry, application, receipt and uninterrupted payment [6], [7], [8].

TABLE: Table I. Evidence scope informing the study
| Study | Grant / people studied / measure | Contribution and transfer limit |
| --- | --- | --- |
| Ralston et al. [3] | Pension; rural older person; receipt | Selection by age in rural Agincourt differs from this study’s resource screen. |
| Godfrey et al. [4] | Grants; Msunduzi household; receipt proportions | Local household findings cannot directly explain individual receipt. |
| Case et al. [6]; Zembe-Mkabile et al. [7] | Child Support Grant (CSG); enquiry/application and infant receipt | Separates access steps; cannot estimate OPG non-receipt. |
| Heinrich and Brill [8]; Gibbs et al. [9]; Majola and Maharaj [10] | CSG; interruption and application experiences | Receipt can still require costly effort. |
| Gazeaud [11] | Targeting assistance using survey measures; resources | Supports checking income assumptions; cannot set South African legal limits. |

Gazeaud supports checking income assumptions [11], without quantifying LCS errors or defining South African eligibility. Mabala models another grant for younger applicants [12]; its findings cannot directly predict OPG receipt.

Existing studies leave unclear how resource, partnership and grant-compatibility assumptions shape provincial person-level non-receipt estimates. Ralston studies rural age-eligible people [3]; Godfrey measures household receipt proportions [4]. This study connects explicit screening, sensitivity analysis, person-weighted description and household-held-out prediction through shared rules and inspectable software. It contributes a reproducible measurement workflow without establishing statutory entitlement, causal barriers, participant usability or performance elsewhere.

### B. Grant Access and Administrative Burden

Administrative-burden theory distinguishes learning, compliance and psychological costs [13]. Studies describe paperwork, repeated visits, interrupted payments and difficult encounters [8], [9], [10], [14]. Other-grant [6], [7] and digital-access findings [15] suggest possible barriers, without establishing effects among older OPG applicants. High receipt can coexist with burden.

The screen assigns PASS for satisfied observable conditions, FAIL for a known failed rule and UNRESOLVED for insufficient information. Receipt is assessed separately. Only PASS adults with resolved receipt enter description and prediction; contradictory answers remain unresolved.

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

Rare outcomes require precision–recall assessment, discrimination and calibration [16], [17]. Sample size and household dependence limit validation [18], [19]. TRIPOD informed reporting [20]. Software verification and participant usability require different evidence.

### D. Conceptual Framework

Reported OPG non-receipt among apparently eligible older adults motivates an administrative-burden perspective [13], [14]. Learning, compliance and psychological costs may obstruct access; high receipt does not establish low burden.

Figure 1 links theory to LCS proxies: schooling reflects possible information resources; office distance and settlement reflect potential compliance effort. Age and sex provide demographic context. These proxies do not directly measure burden. Screening defines the denominator because age alone is insufficient and LCS omits legal conditions. Resources, partnership and grant compatibility define the population; reported receipt defines the outcome.

Person weights describe non-receipt; household-held-out validation assesses prediction. Neither establishes causes. The artefact implements shared screening rules, separate receipt classifications, frozen-model scoring and inspectable reports. Application scores never change screening or receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual framework. Theory informs predictor selection; observable screening defines the population for separate descriptive and predictive analyses. The dashed boundary identifies the artefact’s implementation scope. Arrows show conceptual rationale or analytical dependencies, not causal effects.

## III. Methods

### A. Data and study population

The analysis linked LCS person, household and person-income files through survey identifiers, checking duplicates, unmatched records and row counts. Questionnaire, metadata and COICOP (Classification of Individual Consumption According to Purpose) codes guided interpretation [21], [22], [23]. The study included sampled KZN residents aged 60+; the household survey excludes institutional residents. Screening used interview-month rules. Stats SA had hot-deck-imputed age and sex before release without record-level flags; model preprocessing addressed missing predictors separately.

Table III shows each field's role. Summing income before linkage avoided duplicate person records.

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

GN 211 set the standard monthly maximum at R1,350 from 1 April 2014 [24]; GN 277 raised it to R1,410 from 1 April 2015 [25]. Government Notice R211, a separate amendment in the same gazette, substituted D = 1.6A − 0.4B from 1 April 2014 in Schedule paragraph 2 [26]. With annual standard maximum A and minimum D = R1,200 (Annexure A(5)) [27], B = (1.6A − 1,200)/0.4. This yields annual single/couple research ceilings of R61,800/R123,600 for October 2014–March 2015 and R64,680/R129,360 for April–October 2015. Half-joint income doubles couple limits; equality passed. The screen applied these boundaries to its private-income proxy. Both notices add R20 for age 75+; the primary screen retained the standard maximum across ages, while S1c tested the supplement. S1 also tested period and payment-boundary alternatives.

The 2008 regulations define spouses (regulation 1), include spouse income regardless of property regime (18(2)) and use half-joint annual income (19(1)). They allow Agency-approved exclusion after continuous desertion for at least three months and unwillingness to support (18(3)) [27]. The July 2015 amendment left these OPG means provisions unchanged [28]. Survey responses established neither legal spouse status nor desertion conditions. Never-married, widowed and divorced adults used single ceilings. For married adults, research rules required resolved applicant/spouse incomes and reciprocal pointers linking a resident spouse; sums applied regardless of spouse age. Nonresident spouse income was unavailable; separated respondents lacked spouse details [23]. Cohabitation, unspecified status and missing/inconsistent links remained unresolved, without assumed single status or zero partner income. S2 tested alternatives.

An adult's reported disability or war-veterans grant caused FAIL. Caregiver child grants and grant-in-aid neither excluded the adult nor defined OPG receipt. A known failure took priority over unresolved information; the screen retained all reasons.

For adults who passed, the software interpreted general-grant and OPG answers together, including structural skips (questions omitted because earlier answers make them inapplicable). A consistent “no grant” answer can establish non-receipt when the OPG follow-up does not apply. Contradictory or unexplained answers remain unresolved and exclude the person from modelling. The analysis flagged disagreements between current receipt and preceding-year OPG income without changing the outcome because the periods differ. Rule version opg-kzn-primary-v1 records these decisions. The denominator contains adults who pass and have a clear receipt answer.

### C. Survey-weighted description and uncertainty

RQ1 used count and person-weighted proportions: p = Σ(wᵢYᵢ)/Σwᵢ, where wᵢ is the person weight and Yᵢ is 1 for non-receipt and 0 for receipt. Group comparisons are descriptive.

Released files lack strata. Derived primary sampling units (PSUs), allowing repeated sampling of a group, supported approximate sampling uncertainty but cannot reproduce the full survey design. Eligibility-unresolved adults remain outside the proportion. Receipt bounds assign every unresolved PASS receipt answer to receipt or to non-receipt.

### D. Model specification and validation

The unweighted logistic model estimated probability of reported non-receipt. The analysis did not rebalance recipients and non-recipients, automatically select variables or choose a cutoff. The model describes associations after accounting for other predictors. Age enters per decade above 60. Comparison categories are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five predictor groups require six slopes and an intercept, because settlement requires two comparisons.

Rural formal settlement had 31 adults and one non-recipient. One seven-slope training fold then contained 30 rural-formal adults and no event; its coefficient was about −21.88 and did not converge. Four of five folds converged. Decision D-052 combined rural formal with traditional settlement after that outcome pattern was known, so the retained cross-validation can be optimistic and does not show that the settings are equivalent. Supplementary Table S2 retains this failed attempt as a diagnostic. Ridge logistic regression was then applied to both codings on the same household folds. Five inner household folds selected C by mean Brier score, with training-only imputation and scaling; all ten outer fits chose C = 0.1 and converged. Held-out AUC was 0.756 for the merged coding and 0.750 for the separate coding (Supplementary Table S2). The ordinary merged model remains the reference. This comparison does not make Decision D-052 outcome-independent. Income, receipt, derived labels and marital status do not enter the primary model.

Validation used five household-grouped folds. Sorted households were labelled by whether any member reported non-receipt, then stratified so every adult from a household stayed in one fold. Seed 201415 fixes this division. The 1,013 adults come from 827 households: 182 contain more than one modelled adult, and 6 contain both receipt and non-receipt. Each adult received one out-of-fold (OOF) probability from a model trained without that household. The intercept-only reference uses the training group's non-receipt rate.

After interpreting skipped questions, each training fold supplied the fill-in for its held-out adults. Schooling contrasted below Grade 7 with Grade 7 or above, and office distance contrasted at least 5 km or unavailable with nearer than 5 km. Other codes stayed missing. The training fold filled missing age, in decades above 60, with its median, and a missing category with its most frequent code, or the smaller code in a tie. Eligibility, receipt and weights were not filled or modelled. Three recipients lacked usable schooling; 14 recipients and four non-recipients lacked usable office distance. Age, sex and settlement were already complete.

Pooled OOF probabilities supplied average precision, AUC, Brier score, calibration slope and calibration-in-the-large. Calibration-in-the-large is an intercept correction with its slope fixed at 1; the ideal values are 0 and 1. The 95% intervals are 2.5 and 97.5 percentiles from 1,000 with-replacement household samples of those fixed predictions, using the same seed. Every selected household's adults were retained. All 1,000 samples contained both outcome classes. These intervals condition on seed 201415, its preprocessing and fits, and Decision D-052. They do not repeat the split, imputation or estimation, and they are not survey-design confidence intervals. Twenty household-grouped repetitions (seeds 201415–201434) repeated training-only imputation and refitting, with D-052 fixed. Metrics pooled one held-out prediction per adult within each repetition (Supplementary Table S3).

### E. Alternative assumptions

S1 changes thresholds, S2 partnership, S3 grant compatibility, S4 income, S5 receipt period and S6 unresolved-receipt bounds. S7 uses complete cases; S8 replaces office access with marriage. S9 fits frequency-weighted models with unweighted preprocessing/evaluation, not full survey-design regression. S10 weights primary OOF measures without refitting; S11 groups folds by derived PSU. These checks remain separate from the primary analysis. Supplementary Tables S1–S5 provide rules, ridge comparisons, repeated refits, descriptive summaries and search records.

## IV. Software and Evaluation

The command python analysis/run_study.py links survey files, screens adults and calculates results. Run records retain settings, versions, folds, seed and checksums. The full-cohort model, opg-kzn-six-slope-v1, stores coefficients and imputation settings in JSON. Uploads do not retrain it.

The Streamlit app covers context, validation, screening/receipt, prediction and exports. It accepts opg-screen-v1 CSVs with required household members for spouse checks. Validation checks schema, study context, duplicates, categories and numeric values; limits are 20 MiB/50,000 rows. Uploads remain in session memory. Displays and exports use generated labels and omit submitted identifiers, raw income and household links. Filters do not change summary denominators.

FIGURE: figures/architecture.png | Fig. 2. Research and app workflows share screening rules. Household-held-out predictions remain separate from app scores calculated using the model trained on all included adults.

The app shares screening rules and frozen-model settings. Supported PASS adults with resolved receipt are scored using training-data imputation; records missing every categorical predictor remain unscored. Integrity checks bind model/evaluation files to code. Uploaded scores remain separate from OOF results. Reports include classifications, reasons, probabilities, versions and an audit manifest. The downloadable package excludes microdata.

Checks covered expected screening decisions, excluded predictors, linkage, repeatability, reports, saved scores and CLI–UI agreement, including invalid inputs and outdated results. The owner demonstrated Windows functionality. A task sheet supports future testing with three to five consenting participants; no participant study occurred.

## V. Results

### A. Study group and reported non-receipt

The survey included 15,388 people in 3,686 KwaZulu-Natal households. Table IV shows the selection steps. Among 117 failures, 93 exceeded the income ceiling and 25 reported a disability grant; one met both conditions. None reported a war-veterans grant. Among 187 unresolved adults, 105 were married, mostly with a non-resident spouse, and 63 reported living together. Unresolved adults outnumbered non-recipients.

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

NOTE: Each row counts distinct households. A household can appear in several rows.

FIGURE: figures/cohort_flow.png | Fig. 3. FAIL, UNRESOLVED and PASS groups do not overlap. All 1,013 PASS adults resolve receipt and enter the final denominator.

Among 1,013 adults, 67 reported non-receipt: 6.61% unweighted and 7.49% person-weighted. Using 345 derived PSUs gave a standard error of 1.3 percentage points and an approximate normal 95% interval of 4.9%–10.0%; missing strata limit it. All PASS answers agreed with preceding-year OPG income. Table V describes receipt-group composition before imputation, not non-receipt rates or predictions.

TABLE: Table V. Characteristics by reported OPG receipt, before imputation
| Characteristic | Recipients, N = 946 | Non-recipients, N = 67 |
| --- | --- | --- |
| Age, mean years | 70.4 unw.; 69.8 wtd | 67.3 unw.; 68.4 wtd |
| Female | 686 (72.5%) unw.; 70.4% wtd | 33 (49.3%) unw.; 53.4% wtd |
| Grade 7 or above | 290 (30.7%) unw.; 33.0% wtd | 49 (73.1%) unw.; 80.8% wtd |
| Schooling missing | 3 (0.3%) unw.; 0.4% wtd | 0 (0.0%) unw.; 0.0% wtd |
| Urban formal settlement | 284 (30.0%) unw.; 36.2% wtd | 38 (56.7%) unw.; 66.2% wtd |
| Office ≥5 km or unavailable | 717 (75.8%) unw.; 72.0% wtd | 34 (50.7%) unw.; 40.3% wtd |
| Office distance missing | 14 (1.5%) unw.; 1.8% wtd | 4 (6.0%) unw.; 7.2% wtd |

NOTE: unw. is the unweighted count and percentage, or the unweighted mean age. wtd is the person-weighted percentage or mean. Missing predictors remain in the denominators. Supplementary Table S4 prints the unweighted and weighted values in separate columns. These summaries have no uncertainty intervals.

### B. Screening sensitivity

Table VI summarises changed-cohort scenarios alongside the baseline and unchanged-scenario reference. Changed cohorts were refitted. Unchanged cohorts reused the primary predictions, so matching performance is not an independent fit. Supplementary Table S1 defines every rule.

TABLE: Table VI. Changed screening rules and OOF performance
| ID | N/events | Unw.% | Wtd.% | AUC | Brier | Slope |
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

NOTE: Events are reported non-recipients. Performance uses no weights. S1b uses the 2015 ceiling at every interview. S1d uses the income level at which the formula pays nothing; it admitted the same two adults as S1b. S2a/S2b screen living-together adults as couples/single. S2c screens separated adults as single; S2d screens both as single. S3 retains disability-grant recipients and adds no war-veterans recipient. S4b keeps social-assistance income in the proxy.

*S1a, S1c, S4a, S4c, S5 and S6a/S6b keep the S0 counts and reuse its predictions. Identical counts do not make the rules equivalent. No PASS adult has unresolved receipt for S6a/S6b to bound. Definitions are in Supplementary Table S1.

### C. Held-out prediction

All five folds converged. Figure 4 uses five similarly sized bins. The highest bin had average prediction 0.188 and 35/203 non-recipients (17.2%); the lowest had average 0.0107 and 3/206 non-recipients (1.5%).

TABLE: Table VII. Primary held-out performance and uncertainty
| Metric | Logistic: estimate [95% interval] | Intercept-only: estimate [95% interval] |
| --- | --- | --- |
| AUC | .752 [.687–.814] | — |
| Average precision | .203 [.139–.292] | — |
| Brier score | .0578 [.0448–.0706] | .0618 [.0467–.0758] |
| Calibration-in-the-large | .020 [−.316–.273] | .0001 [—] |
| Calibration slope | .836 [.591–1.133] | — |

NOTE: Estimates pool unweighted OOF predictions: 1,013 people/67 events. The intervals use percentile bounds from 1,000 household resamples of fixed predictions. All reported intervals have zero invalid resamples. Resampling did not refit models or missing-value settings. The intercept-only reference uses the training group's non-receipt rate. Dashes mean unavailable measures/intervals, rather than zero or chance performance.

FIGURE: figures/calibration.png | Fig. 4. Saved group summaries show unweighted OOF calibration. Labels give events/people; the diagonal shows exact agreement between average predictions and observed rates. Plot range: 0–0.22.

The odds ratio for women versus men was 0.39 (Wald interval 0.23–0.66). Schooling below Grade 7 versus Grade 7 or above gave 0.24 (0.13–0.43). These full-sample associations are not held-out performance or causes. Only 67 events supported six slopes. Across the 100 refitted training folds, the female and below-Grade-7 coefficients stayed negative, while the urban-informal coefficient changed sign. Age, settlement and welfare-distance intervals included 1. That is limited precision, not evidence of no association, and those intervals omit the settlement-coding decision. The 20 repeated splits gave 100 converged fits. AUC ranged from 0.733 to 0.773 (median 0.753) and the calibration slope from 0.738 to 0.943 (median 0.837). Supplementary Table S3 gives the median, interquartile range and range for every performance measure, and the coefficient ranges. That spread is a sensitivity summary for the fixed coding, not a confidence interval.

TABLE: Table VIII. Model/validation sensitivities
| Scenario | N/events | Unw.% | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- |
| S0 primary | 1,013/67 | 6.61 | .752 | .0578 | .836 |
| S7 complete | 992/63 | 6.35 | .758 | .0556 | .819 |
| S8 married | 1,013/67 | 6.61 | .755 | .0578 | .846 |
| S9 wtd. fit | 1,013/67 | 6.61 | .750 | .0583 | .718 |
| S10 wtd. measures | 1,013/67 | 6.61 | .763 | .0641 | .935 |
| S11 PSU folds | 1,013/67 | 6.61 | .758 | .0575 | .860 |

NOTE: The non-receipt-rate column uses no weights; S8–S11 keep the weighted non-receipt rate at 7.49%. S9 uses frequency weights when fitting, but no weights when filling missing values or checking predictions. S10 weights the primary OOF predictions without refitting. S8 replaces welfare access and keeps six slopes. S7 removes 21 people/four events. S11 changes fold grouping but keeps the study group.

### D. Software verification

The 26 checks comprised 22 synthetic screening cases, two income-schedule checks, one forbidden-predictor check and one run trace. Decisions matched specifications. Two research runs produced 14 byte-identical files and retained the cohort checksum.

TABLE: Table IX. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Check rules, schedules, excluded predictors and run tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Check software, app state and exports; includes 18 Streamlit interface tests. |
| App–command agreement | 15,388/15,388 agree; 1,013 scored | Both paths select the same people and give the same decisions, receipt, reasons and outcome. |
| Reloaded model scores | Maximum score difference 5.55 × 10⁻¹⁷ | Reloading preserves saved-model scores; this does not assess OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Check synthetic local use and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The owner walkthrough used synthetic records. It checks exports, not representative task times or ease.

## VI. Discussion

### A. Scope of measured non-receipt

RQ1 describes historical KZN adults who pass screening and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% weighted. It does not measure unlawful denial or all legally entitled adults. The 187 eligibility-unresolved adults outnumbered events; excluding them changes the population, independently of sampling uncertainty.

S2d added 68 people/two events, reducing weighted non-receipt to 7.12%. S3 added 19 people/15 events, raising it to 9.06%, the largest change. Similar AUC cannot justify screening rules. Different units and populations [3], [4] prevent direct comparisons. The provincial resource screen here is explicit; high receipt can coexist with access costs [13], [14].

### B. Predictive performance and interpretation

AUC 0.752 measures ranking, not classification accuracy. AP 0.203 summarises precision–recall ranking against 6.61% prevalence, not precision at one cutoff [16]. Brier improved by 0.0040, from 0.0618 to 0.0578: a modest probability-error reduction. Calibration-in-the-large 0.020, with an interval spanning zero, does not establish perfect agreement. Slope 0.836 suggests predictions may be too extreme, but its 0.591–1.133 interval includes 1 [17]. Only 67 events informed these checks [18]; most adults in the highest-score bin reported receipt.

Table VIII changes samples, predictors, fitting or evaluation. Complete-case Brier concerns different adults; S10 reweights unchanged predictions. These internal checks cannot establish model superiority or external reliability [19], [20].

### C. Reproducibility and usability

RQ3 separates synthetic rule checks, repeatability, UI–CLI agreement, model reloading, the owner's walkthrough and participant usability. Table IX supports the first five within tested conditions; it does not establish independent user ease, acceptance or field success. Supplementary Tables S1–S5 and the aggregate evidence files document rule settings, validation procedures and recorded searches.

Application scores may overlap training data and remain separate from historical OOF results. Reload agreement checks score persistence, not new predictive accuracy. Participant clarity remains untested; the task sheet supports future evaluation.

### D. Transfer to other settings

Provinces and periods differ in services, policy and reporting. Administrative application/payment records differ from reported receipt and may contain linkage errors. Independent transfer testing requires comparable populations/outcomes, period-specific rules and discrimination/calibration checks [19], [20].

### E. Synthesis of the Conceptual Framework

Returning to Figure 1, sensitivity results support explicit denominator construction; sex differences support demographic comparison, not burden mechanisms [3], [4]. Lower schooling accompanied receipt, contrary to a simple learning-cost expectation [13]. Screening selection or other resources could explain this, but neither was tested. Settlement and office-distance intervals included 1, leaving compliance-cost expectations unresolved. Psychological costs were unmeasured. The artefact implements these bounded choices reproducibly; proxy associations establish neither the theory’s causal mechanisms nor statutory entitlement.

## VII. Limitations and Ethics

The resource proxy omits assets, deemed income and deductions. Misreporting, cross-sectional ordering, few events, unresolved screening, missing strata and fixed-prediction resampling limit inference. Household sampling excludes institutionalised adults. Participant usability and external predictive performance remain untested.

Survey access/disclosure conditions apply. Public demonstrations use synthetic records; downloadable packages exclude survey microdata. Reports omit submitted identifiers and raw income. This does not clear every historical repository file for release. No DUT ethics determination is documented. The app does not decide grants or rank named applicants.

## VIII. Conclusion

Screened non-receipt was 6.6% unweighted and 7.5% person-weighted; alternatives gave 7.1%–9.1%. Five predictor groups/six slopes gave AUC 0.752, AP 0.203 and Brier 0.0578. Shared rules make screening, receipt and prediction inspectable. Future work should independently validate the frozen model before updating it and test intended users’ task success, errors, time and perceived ease. Legal entitlement, causal explanations, human usability and external predictive validity remain unestablished.


## References

[1] T. Raniga and B. Simpson, “Poverty, HIV/AIDS and the old age pension in Bhambayi, KwaZulu-Natal, South Africa,” Dev. South. Afr., vol. 28, no. 1, pp. 75–85, 2011, doi: 10.1080/0376835X.2011.545171.

[2] M. Alloush, J. R. Bloem, and J. G. Malacarne, “Social protection amid a crisis: New evidence from South Africa’s Older Person’s Grant,” World Bank Econ. Rev., vol. 38, no. 2, pp. 371–393, 2024, doi: 10.1093/wber/lhad037.

[3] M. Ralston, E. Schatz, J. Menken, F. X. Gómez-Olivé, and S. Tollman, “Who benefits—or does not—from South Africa’s old age pension? Evidence from characteristics of rural pensioners and non-pensioners,” Int. J. Environ. Res. Public Health, vol. 13, no. 1, Art. no. 85, 2016, doi: 10.3390/ijerph13010085.

[4] E. B. Godfrey et al., “Which eligible households get grants? Demographic correlates of receipt in South Africa,” Dev. South. Afr., vol. 33, no. 6, pp. 774–789, 2016, doi: 10.1080/0376835X.2016.1231059.

[5] Republic of South Africa, Social Assistance Act 13 of 2004, Government Gazette 26446, Jun. 10, 2004.

[6] A. Case, V. Hosegood, and F. Lund, “The reach and impact of Child Support Grants: Evidence from KwaZulu-Natal,” Dev. South. Afr., vol. 22, no. 4, pp. 467–482, 2005, doi: 10.1080/03768350500322925.

[7] W. Zembe-Mkabile, T. Doherty, D. Sanders, and D. Jackson, “Child Support Grant access and receipt among 12-week-old infants in an urban township setting in South Africa,” Global Health Action, vol. 7, no. 1, Art. no. 25310, 2014, doi: 10.3402/gha.v7.25310.

[8] C. J. Heinrich and R. Brill, “Stopped in the name of the law: Administrative burden and its implications for cash transfer program effectiveness,” World Dev., vol. 72, pp. 277–295, 2015, doi: 10.1016/j.worlddev.2015.03.015.

[9] A. Gibbs, L. Washington, N. Jama Shai, Y. Sikweyiya, and S. Willan, “Systematically excluded: Young women’s experiences of accessing child support grants in South Africa,” Global Public Health, vol. 13, no. 12, pp. 1820–1830, 2018, doi: 10.1080/17441692.2018.1449231.

[10] T. N. Majola and P. Maharaj, “The challenges associated with the Child Support Grant application process: A case of young mothers in a South African township,” J. Soc. Serv. Res., vol. 51, nos. 5–6, pp. 1140–1150, 2025, doi: 10.1080/01488376.2025.2502004.

[11] J. Gazeaud, “Proxy means testing vulnerability to measurement errors?,” J. Dev. Stud., vol. 56, no. 11, pp. 2113–2133, 2020, doi: 10.1080/00220388.2020.1715942.

[12] M. T. Mabala, “Factors associated with social grant uptake in South Africa: A closer look at the Special COVID-19 Social Relief of Distress Grant among the youth aged 18–35 years,” Master’s research report, University of the Witwatersrand, Johannesburg, South Africa, 2023. Available: https://hdl.handle.net/10539/40003.

[13] D. P. Moynihan, P. Herd, and H. Harvey, “Administrative burden: Learning, psychological, and compliance costs in citizen-state interactions,” J. Public Adm. Res. Theory, vol. 25, no. 1, pp. 43–69, 2015, doi: 10.1093/jopart/muu009.

[14] S. Granlund, “They are not leaving without their money: Exploring encounters with the state through cash transfers in the rural Eastern Cape, South Africa,” South. Afr. J. Soc. Work Soc. Dev., vol. 34, no. 1, Art. no. 9052, 2022, doi: 10.25159/2708-9355/9052.

[15] A. N. Vujovic, G. M. Jonathan, and S. Hacks, “Digitalisation and its impact on social protection programmes effectiveness: A case from South Africa,” Procedia Comput. Sci., vol. 237, pp. 882–890, 2024, doi: 10.1016/j.procs.2024.05.177.

[16] T. Saito and M. Rehmsmeier, “The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,” PLOS ONE, vol. 10, no. 3, Art. no. e0118432, 2015, doi: 10.1371/journal.pone.0118432.

[17] B. Van Calster et al., “Calibration: The Achilles heel of predictive analytics,” BMC Med., vol. 17, Art. no. 230, 2019, doi: 10.1186/s12916-019-1466-7.

[18] R. D. Riley et al., “Minimum sample size for developing a multivariable prediction model: Part II—binary and time-to-event outcomes,” Stat. Med., vol. 38, no. 7, pp. 1276–1296, 2019, doi: 10.1002/sim.7992.

[19] D. R. Roberts et al., “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” Ecography, vol. 40, no. 8, pp. 913–929, 2017, doi: 10.1111/ecog.02881.

[20] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, “Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement,” Ann. Intern. Med., vol. 162, no. 1, pp. 55–63, 2015, doi: 10.7326/M14-0697.

[21] Statistics South Africa, Living Conditions Survey 2014/2015: Metadata, Statistical Release P0310. Pretoria, South Africa, 2017, ISBN 978-0-621-45185-6. Archived project copy, inspected Oct. 21, 2026. [Online]. Available: https://github.com/Oluhle1/Research-Project/blob/110d84161ffb4ca1821c2c76318a6a13b27e2643/Dataset/metadata/Living%20Conditions%20Survey%20Metadata.pdf

[22] Statistics South Africa, “Coicop codes,” supporting documentation for the Living Conditions Survey 2014/2015, n.d. Archived project copy, inspected Oct. 21, 2026. [Online]. Available: https://github.com/Oluhle1/Research-Project/blob/110d84161ffb4ca1821c2c76318a6a13b27e2643/Dataset/metadata/Living%20Conditions%20Survey%20Coicopcodes.pdf

[23] Statistics South Africa, Living Conditions Survey 2014/15: Household Questionnaire, n.d. Archived project copy, inspected Oct. 21, 2026. [Online]. Available: https://github.com/Oluhle1/Research-Project/blob/110d84161ffb4ca1821c2c76318a6a13b27e2643/Dataset/metadata/Living%20Conditions%20Survey%20Questionnaire.pdf

[24] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 211, Government Gazette 37474, Mar. 28, 2014.

[25] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 277, Government Gazette 38647, Mar. 30, 2015.

[26] Dept. of Social Development, “Amendment: Social Assistance Regulations,” Government Notice R211, Government Gazette 37474, pp. 4–5, Mar. 28, 2014.

[27] Dept. of Social Development, “Social Assistance Act: Regulations,” Government Notice R898, Government Gazette 31356, Aug. 22, 2008.

[28] Dept. of Social Development, “Amendment: Social Assistance Regulations,” Government Notice R621, Government Gazette 39007, Jul. 21, 2015.
