# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—This study analysed reported Older Person’s Grant (OPG) non-receipt among adults aged 60 or older in KwaZulu-Natal (KZN), using the Living Conditions Survey (LCS) 2014/2015. The study used administrative-burden theory to choose predictors and observable research rules to identify apparently eligible adults. Screening did not establish legal entitlement. Among 1,013 adults who passed with resolved receipt, 67 reported non-receipt: 6.6% unweighted and 7.5% person-weighted. Alternative screening rules gave weighted rates of 7.1%–9.1%. Logistic regression used five predictor groups and household-held-out validation. AUC (area under the receiver operating characteristic curve) was 0.752; average precision (AP) was 0.203. The Brier score was 0.0578, compared with 0.0618 for an intercept-only reference using training-group prevalence. Checks supported reproducibility. The application displays rules, decisions, scores and reports. No participant study tested ease of use. These results do not establish entitlement, explain non-receipt, or demonstrate performance elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [7], including during crises [8]. Other work examines receipt and access barriers [2], [6]. This study examines adults who appear eligible but report receiving no OPG.

Screening, reported receipt and legal entitlement remain distinct. Passing the research screen does not establish a South African Social Security Agency decision [1]. Missing spouse resources and unresolved answers can change the screened denominator and its non-receipt proportion.

This study develops and evaluates an interpretable research tool using LCS 2014/2015 in KwaZulu-Natal. It documents cohort construction, describes person-weighted non-receipt, validates predictions in held-out households and assesses correctness, reproducibility and clarity.

RQ1 asks how common reported non-receipt is among screened adults and how alternative rules change it. RQ2 assesses prediction in held-out households. RQ3 assesses whether the tool reproduces the analysis and clearly presents screening and model outputs; participant usability remains untested.

## II. Related Work and Predictor Selection

### A. Review Approach, Programme Context and Research Gap

The structured narrative review examined grant access, eligibility measurement and prediction using Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst. Search concepts included social assistance, eligibility, take-up, non-receipt, exclusion and prediction. Selection considered relevance to the research question, population, outcome and methodological contribution.

The searches identified 511 records. Removing 136 duplicates left 375 records for title and abstract screening; 222 were excluded. Full-text assessment of the remaining 153 records excluded 98 and retained 55 sources across grants and populations. Table S5 lists the eight recorded search strings, search date and source-specific counts. The synthesis compared programme, setting, unit of analysis, outcome definition, findings and limitations; these differences prevented a pooled estimate.

RECORD: Table S5. Recorded literature searches (17 August 2026)
| Search | Source | Hits | Kept | Query |
| --- | --- | --- | --- | --- |
| S1 | Scopus | 43 | 9 | TITLE-ABS-KEY(("social grant*" OR "social assistance" OR "cash transfer*" OR "social protection") AND (exclusion OR "non-take-up" OR "take-up" OR "coverage gap*" OR "targeting error*" OR "access barrier*") AND ("South Africa*" OR "KwaZulu-Natal")) |
| S1b | Scopus, widened | 149 | 10 | TITLE-ABS-KEY(("social grant*" OR "social assistance" OR "cash transfer*" OR "social protection" OR "social security" OR SASSA OR "child support grant" OR "social relief of distress" OR SRD) AND (exclusion OR exclud* OR "non-take-up" OR "take-up" OR uptake OR "coverage gap*" OR "targeting error*" OR "access barrier*" OR "non-receipt" OR eligib*) AND ("South Africa*" OR "KwaZulu-Natal")) |
| S2 | Scopus, method | 100 | 11 | TITLE-ABS-KEY(("machine learning" OR "random forest" OR XGBoost OR "gradient boosting" OR "proxy means test*" OR "predictive model*") AND (poverty OR "social protection" OR "social assistance" OR "cash transfer*" OR "food insecur*") AND ("household survey" OR "survey data" OR "household data")) AND NOT TITLE-ABS-KEY(cancer OR tumour OR HIV OR malaria OR clinical OR patient*) |
| S3 | Dimensions | 36 | 5 | ("social grant" OR "social assistance" OR "cash transfer" OR "social protection") AND (exclusion OR "take-up" OR "non-receipt" OR "access barriers") AND ("South Africa" OR "KwaZulu-Natal") |
| S4 | IEEE Xplore | 47 | 0 | ("machine learning" OR "classification") AND ("poverty" OR "social welfare" OR "socioeconomic") AND ("survey data") |
| S5 | SABINET/AJOL | 100 | 9 | social grant AND exclusion AND (KwaZulu-Natal OR "South Africa") |
| S6 | Google Scholar | 35 | 11 | "social grant" exclusion "South Africa" -site:pinterest.com |
| S7 | DataFirst/Stats SA | 1 | 0 | Living Conditions Survey 2014/2015 metadata KwaZulu-Natal |

NOTE: Counts refer to the recorded searches. Repeated retained sources are assigned to their first search; search and scenario IDs differ.

Table I distinguishes individual receipt [2] from household proportions [6], and this study’s provincial resource screen from both. Other-grant studies separate enquiry, application, receipt and uninterrupted payment [9], [10], [13].

TABLE: Table I. Evidence scope informing the study
| Study | Grant / people studied / measure | Contribution and transfer limit |
| --- | --- | --- |
| Ralston et al. [2] | Pension; rural older person; receipt | Selection by age in rural Agincourt differs from this study’s resource screen. |
| Godfrey et al. [6] | Grants; Msunduzi household; receipt proportions | Local household findings cannot directly explain individual receipt. |
| Case et al. [9]; Zembe-Mkabile et al. [10] | Child Support Grant (CSG); enquiry/application and infant receipt | Separates access steps; cannot estimate OPG non-receipt. |
| Heinrich and Brill [13]; Gibbs et al. [14]; Majola and Maharaj [15] | CSG; interruption and application experiences | Receipt can still require costly effort. |
| Gazeaud [11] | Targeting assistance using survey measures; resources | Supports checking income assumptions; cannot set South African legal limits. |

Gazeaud supports checking income assumptions [11], without quantifying LCS errors or defining South African eligibility. Mabala models another grant for younger applicants [18]; its findings cannot directly predict OPG receipt.

Existing studies leave unclear how resource, partnership and grant-compatibility assumptions shape provincial person-level non-receipt estimates. Ralston studies rural age-eligible people [2]; Godfrey measures household receipt proportions [6]. This study connects explicit screening, sensitivity analysis, person-weighted description and household-held-out prediction through shared rules and inspectable software. It contributes a reproducible measurement workflow without establishing statutory entitlement, causal barriers, participant usability or performance elsewhere.

### B. Grant Access and Administrative Burden

Administrative-burden theory distinguishes learning, compliance and psychological costs [12]. Studies describe paperwork, repeated visits, interrupted payments and difficult encounters [13]–[16]. Other-grant [9], [10] and digital-access findings [17] suggest possible barriers, without establishing effects among older OPG applicants. High receipt can coexist with burden.

The screen assigns PASS for satisfied observable conditions, FAIL for a known failed rule and UNRESOLVED for insufficient information. Receipt is assessed separately. Only PASS adults with resolved receipt enter description and prediction; contradictory answers remain unresolved.

### C. Predictor Selection and Software Design

Table II separates demographic context from circumstances relevant to learning and compliance costs. These predictors do not directly measure administrative burden or establish why a person reports non-receipt.

TABLE: Table II. Administrative-burden theory and predictor selection
| Predictor | Theoretical role | LCS coding and limit |
| --- | --- | --- |
| Age | Demographic context: receipt differs by age [2] | Per decade above 60; health and application history unmeasured. |
| Sex | Demographic context: receipt differs by sex [2], [6] | Female versus male; social roles and discrimination unmeasured. |
| Schooling | Learning costs: schooling may help people find and understand grant information [12], [15] | Below Grade 7 versus Grade 7 or above; awareness and literacy unmeasured. |
| Settlement | Compliance costs: place may shape service access [9], [16], [17] | Urban informal and traditional/rural formal, each versus urban formal; office capacity unmeasured. |
| Office distance | Compliance costs: distance may add travel effort [15], [16] | At least 5 km/unavailable versus nearer than 5 km; visits and travel costs unmeasured. |

NOTE: Psychological costs are unmeasured. Settlement contributes two contrasts, giving five predictor groups and six slopes.

Rare outcomes require precision–recall assessment, discrimination and calibration [20], [19]. Sample size and household dependence limit validation [21], [22]. TRIPOD informed reporting [23]. Software verification and participant usability require different evidence.

### D. Conceptual Framework

Reported OPG non-receipt among apparently eligible older adults motivates an administrative-burden perspective [12], [16]. Learning, compliance and psychological costs may obstruct access; high receipt does not establish low burden.

Figure 1 links theory to LCS proxies: schooling reflects possible information resources; office distance and settlement reflect potential compliance effort. Age and sex provide demographic context. These proxies do not directly measure burden. Screening defines the denominator because age alone is insufficient and LCS omits legal conditions. Resources, partnership and grant compatibility define the population; reported receipt defines the outcome.

Person weights describe non-receipt; household-held-out validation assesses prediction. Neither establishes causes. The artefact implements shared screening rules, separate receipt classifications, frozen-model scoring and inspectable reports. Application scores never change screening or receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual framework. Theory informs predictor selection; observable screening defines the population for separate descriptive and predictive analyses. The dashed boundary identifies the artefact’s implementation scope. Arrows show conceptual rationale or analytical dependencies, not causal effects.

## III. Methods

### A. Data and study population

The analysis linked LCS person, household and person-income files through survey identifiers, checking duplicates, unmatched records and row counts. Questionnaire, metadata and COICOP (Classification of Individual Consumption According to Purpose) codes guided interpretation [3]–[5]. The study included sampled KZN residents aged 60+; the household survey excludes institutional residents. Screening used interview-month rules. Stats SA had hot-deck-imputed age and sex before release without record-level flags; model preprocessing addressed missing predictors separately.

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

NOTE: Released documentation supports these field uses [3]–[5]. Filling missing model predictors never changes screening fields or receipt answers.

### B. Screening rules and receipt outcome

The screen summed released annualised nominal person income (metadata, p. 182) [3], excluding social assistance without allocating household totals. Zero required Q1.17(14)'s no-income response [5] and an absent schedule; missing applicant/spouse amounts otherwise remained unresolved. The proxy omits assets, deemed income and deductions.

GN 211 set the standard maximum at R1,350 monthly from 1 April 2014 [24]; GN 277 raised it to R1,410 from 1 April 2015 [25]. GN R211 amended Annexure A(2) to D = 1.6A − 0.4B from 1 April 2014 [29]. With annual maximum A and minimum D = R1,200 (R100 monthly; Annexure A(5)) [28], B = (1.6A − 1,200)/0.4 gives annual single/couple research ceilings of R61,800/R123,600 for October 2014–March 2015 and R64,680/R129,360 for April–October 2015. Half-joint income doubles couple boundaries; equality passed. Standard rates applied at all ages; S1c tested both notices' R20 age-75+ supplement, and S1 tested period/payment boundaries.

Regulation 1 defines recognised spouses; regulations 18(2) and 19(1) require spouse income regardless of property regime and use half-joint annual income. Regulation 18(3) allows Agency-approved exclusion after at least three continuous months of desertion and unwillingness to support [28]. The July 2015 amendment left these provisions unchanged [30]. Survey responses established neither legal spouse status nor desertion approval. Never-married, widowed and divorced adults used single ceilings. Conservative research rules required resolved applicant/spouse incomes and resident, reciprocal spouse pointers for married adults, summing both incomes regardless of spouse age. Nonresident income was unavailable; separated respondents skipped spouse details [5]. Cohabitation, unspecified status and missing/inconsistent links remained unresolved without assumed single status or zero partner income. S2 tested alternatives.

Own disability/war-veterans receipt caused FAIL (regulation 2(c)); regulation 5 permits grant-in-aid [28]. Grant-in-aid and caregiver child grants neither excluded adults nor defined OPG receipt (Q4.1b) [5]. A known failure overrode unresolved information; all reasons were retained.

Among PASS adults, general-grant and OPG answers were interpreted with structural skips [5]. Consistent “no grant” with an inapplicable OPG follow-up established non-receipt; contradictory/unexplained answers remained unresolved and outside modelling. Current-receipt/prior-year OPG-income disagreements were flagged without overriding outcomes because periods differ. Rule opg-kzn-primary-v1 records these decisions; the denominator requires PASS and resolved receipt.

### C. Survey-weighted description and uncertainty

RQ1 used count and person-weighted proportions: p = Σ(wᵢYᵢ)/Σwᵢ, where wᵢ is the person weight and Yᵢ is 1 for non-receipt and 0 for receipt. Group comparisons are descriptive.

Released files lack strata. Derived primary sampling units (PSUs), allowing repeated sampling of a group, supported approximate sampling uncertainty but cannot reproduce the full survey design. Eligibility-unresolved adults remain outside the proportion. Receipt bounds assign every unresolved PASS receipt answer to receipt or to non-receipt.

### D. Model specification and validation

The unweighted logistic model estimated probability of reported non-receipt. The analysis did not rebalance recipients and non-recipients, automatically select variables or choose a cutoff. The model describes associations after accounting for other predictors. Age enters per decade above 60. Comparison categories are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five predictor groups require six slopes and an intercept, because settlement requires two comparisons.

Rural formal settlement had 31 adults and one non-recipient. One seven-slope training fold contained 30 rural-formal adults and no event; its coefficient was about −21.88 and did not converge. Four of five folds converged. D-052 then merged rural formal with traditional settlement after observing this pattern, outside the training folds. The primary ordinary merged model remains exploratory; its coefficients and performance are conditional on D-052 and may be optimistic. Household hold-out does not validate the complete selection process. Confirmatory work should prespecify coding or select it within each outer training set. Supplementary Table S2 retains the failed attempt and compares ridge codings on the same household folds. Five inner household folds selected C by mean Brier score with training-only imputation and scaling; all ten outer fits converged with C = 0.1. AUC was 0.756 for merged and 0.750 for separate coding. These comparisons cannot remove outcome-informed selection or establish equivalence or superiority. Income, receipt, derived labels and marital status do not enter the primary model.

Validation used five household-grouped folds. Sorted households were labelled by whether any member reported non-receipt, then stratified so every adult from a household stayed in one fold. Seed 201415 fixes this division. The 1,013 adults come from 827 households: 182 contain more than one modelled adult, and 6 contain both receipt and non-receipt. Each adult received one out-of-fold (OOF) probability from a model trained without that household. The intercept-only reference uses the training group's non-receipt rate. These internal estimates do not establish performance in independent populations or survey periods.

After interpreting skipped questions, each training fold supplied the fill-in for its held-out adults. Schooling contrasted below Grade 7 with Grade 7 or above, and office distance contrasted at least 5 km or unavailable with nearer than 5 km. Other codes stayed missing. The training fold filled missing age, in decades above 60, with its median, and a missing category with its most frequent code, or the smaller code in a tie. Eligibility, receipt and weights were not filled or modelled. Three recipients lacked usable schooling; 14 recipients and four non-recipients lacked usable office distance. Age, sex and settlement were already complete.

Pooled OOF probabilities supplied average precision, AUC, Brier score, calibration slope and calibration-in-the-large. Calibration-in-the-large is an intercept correction with its slope fixed at 1; the ideal values are 0 and 1. The reported 95% bootstrap intervals are the 2.5 and 97.5 percentiles from 1,000 with-replacement household samples of fixed predictions, using seed 201415. Every selected household's adults were retained, and all samples contained both outcome classes. These intervals condition on the original split, preprocessing, fits and Decision D-052. They do not repeat model development or represent survey-design uncertainty. A separate sensitivity analysis used 20 household-grouped repetitions (seeds 201415–201434), relearning training-only imputation and refitting while keeping D-052 fixed. Each repetition pooled one held-out prediction per adult (Supplementary Table S3). Its medians, interquartile ranges and ranges describe variation across splits and refits, not 95% confidence intervals. The repetitions reuse participants and do not independently validate the coding decision.

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
| Characteristic | Recipients, unweighted (N = 946) | Recipients, weighted | Non-recipients, unweighted (N = 67) | Non-recipients, weighted |
| --- | --- | --- | --- | --- |
| Age, mean years | 70.4 | 69.8 | 67.3 | 68.4 |
| Female | 686 (72.5%) | 70.4% | 33 (49.3%) | 53.4% |
| Grade 7 or above | 290 (30.7%) | 33.0% | 49 (73.1%) | 80.8% |
| Schooling missing | 3 (0.3%) | 0.4% | 0 (0.0%) | 0.0% |
| Urban formal settlement | 284 (30.0%) | 36.2% | 38 (56.7%) | 66.2% |
| Office ≥5 km or unavailable | 717 (75.8%) | 72.0% | 34 (50.7%) | 40.3% |
| Office distance missing | 14 (1.5%) | 1.8% | 4 (6.0%) | 7.2% |

NOTE: Unweighted cells show n (%) and weighted cells person-weighted percentages; age cells show means in completed years. N = 946 and N = 67 are sample sizes. Missing predictors remain in denominators. Values precede imputation; no uncertainty intervals were calculated. Supplementary Table S4 repeats these values.

### B. Screening sensitivity

Table VI identifies each screening scenario separately. Changed cohorts were refitted; unchanged cohorts reused the primary predictions. Supplementary Table S1 defines every rule.

TABLE: Table VI. Screening scenarios and OOF performance
| ID | N/events | Unw.% | Wtd.% | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- | --- |
| S0 | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S1a | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S1b | 1,015/69 | 6.80 | 7.68 | .763 | .0584 | .875 |
| S1c | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S1d | 1,015/69 | 6.80 | 7.68 | .763 | .0584 | .875 |
| S2a | 1,072/71 | 6.62 | 7.42 | .749 | .0588 | .779 |
| S2b | 1,073/69 | 6.43 | 7.17 | .756 | .0564 | .841 |
| S2c | 1,021/67 | 6.56 | 7.43 | .753 | .0571 | .839 |
| S2d | 1,081/69 | 6.38 | 7.12 | .751 | .0565 | .808 |
| S3 | 1,032/82 | 7.95 | 9.06 | .736 | .0682 | .864 |
| S4a | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S4b | 1,007/67 | 6.65 | 7.55 | .755 | .0576 | .854 |
| S4c | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S5 | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S6a | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |
| S6b | 1,013/67 | 6.61 | 7.49 | .752 | .0578 | .836 |

NOTE: Events are non-recipients; performance is unweighted. S1 changes thresholds; S2 partnership; S3 incompatible grants; S4 income; S5 receipt period; S6 unresolved receipt. Supplementary Table S1 defines each rule. S1b and S1d admitted the same two adults under different rules. S1a, S1c, S4a, S4c, S5, S6a and S6b retained the S0 cohort and reused its predictions. Matching results do not imply equivalent rules or independent fits. No PASS receipt was unresolved, so S6a/S6b changed no records.

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

The odds ratio for women versus men was 0.39 (Wald interval 0.23–0.66). Schooling below Grade 7 versus Grade 7 or above gave 0.24 (0.13–0.43). These are exploratory full-sample associations, not held-out performance or causal effects. Only 67 events supported six slopes; sparse data can destabilise coefficients and Wald intervals. The intervals also omit uncertainty from choosing the settlement coding. Across 100 overlapping training fits, the female and below-Grade-7 coefficients stayed negative, while the urban-informal coefficient changed sign. Sign consistency across these fits is not independent confirmation. Age, settlement and welfare-distance intervals included 1, indicating limited precision rather than evidence of no association. The 20 repeated splits gave 100 converged fits. AUC ranged from 0.733 to 0.773 (median 0.753) and the calibration slope from 0.738 to 0.943 (median 0.837). Supplementary Table S3 gives the median, interquartile range and range for each performance measure, and coefficient ranges. These describe sensitivity under the fixed coding, not confidence intervals.

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

S2d added 68 people/two events, reducing weighted non-receipt to 7.12%. S3 added 19 people/15 events, raising it to 9.06%, the largest change. Similar AUC cannot justify screening rules. Different units and populations [2], [6] prevent direct comparisons. The provincial resource screen here is explicit; high receipt can coexist with access costs [12], [16].

### B. Predictive performance and interpretation

AUC 0.752 measures ranking, not classification accuracy. AP 0.203 summarises precision–recall ranking against 6.61% prevalence, not precision at one cutoff [20]. Brier improved by 0.0040, from 0.0618 to 0.0578: a modest probability-error reduction. Calibration-in-the-large 0.020, with an interval spanning zero, does not establish perfect agreement. Slope 0.836 suggests predictions may be too extreme, but its 0.591–1.133 interval includes 1 [19]. Only 67 events informed these checks [21]; most adults in the highest-score bin reported receipt.

Table VIII changes samples, predictors, fitting or evaluation. Complete-case Brier concerns different adults; S10 reweights unchanged predictions. These internal checks cannot establish model superiority or external reliability [22], [23].

### C. Reproducibility and usability

RQ3 separates synthetic rule checks, repeatability, UI–CLI agreement, model reloading, the owner's walkthrough and participant usability. Table IX supports the first five within tested conditions; it does not establish independent user ease, acceptance or field success. Supplementary Tables S1–S5 and the aggregate evidence files document rule settings, validation procedures and recorded searches.

Application scores may overlap training data and remain separate from historical OOF results. Reload agreement checks score persistence, not new predictive accuracy. Participant clarity remains untested; the task sheet supports future evaluation.

### D. Transfer to other settings

Provinces and periods differ in services, policy and reporting. Administrative application/payment records differ from reported receipt and may contain linkage errors. Independent transfer testing requires comparable populations/outcomes, period-specific rules and discrimination/calibration checks [22], [23].

### E. Synthesis of the Conceptual Framework

Returning to Figure 1, sensitivity results support explicit denominator construction; sex differences support demographic comparison, not burden mechanisms [2], [6]. Lower schooling accompanied receipt, contrary to a simple learning-cost expectation [12]. Screening selection or other resources could explain this, but neither was tested. Settlement and office-distance intervals included 1, leaving compliance-cost expectations unresolved. Psychological costs were unmeasured. The artefact implements these bounded choices reproducibly; proxy associations establish neither the theory’s causal mechanisms nor statutory entitlement.

## VII. Limitations and Ethics

The resource proxy omits assets, deemed income and deductions. Misreporting, cross-sectional ordering, few events, unresolved screening, missing strata and fixed-prediction resampling limit inference. Household sampling excludes institutionalised adults. Participant usability and external predictive performance remain untested.

The study analysed anonymised LCS 2014/2015 secondary data from Stats SA via DataFirst [31]. The catalogue describes version 1.1 (18 September 2017) as edited, anonymised data for public distribution with public access. The supervisor advised that formal ethical clearance was not required: this study involved no direct human participation or primary data collection. Stats SA produced the data; analyses are the author's own. Data-use and confidentiality conditions apply. Public access does not clear every historical repository file. Demonstrations use synthetic records; downloadable packages exclude survey microdata. Reports omit submitted identifiers and raw income. The app does not decide grants or rank named applicants.

## VIII. Conclusion

Screened non-receipt was 6.6% unweighted and 7.5% person-weighted; alternatives gave 7.1%–9.1%. Five predictor groups/six slopes gave AUC 0.752, AP 0.203 and Brier 0.0578. The principal contribution is a reproducible, interpretable workflow linking observable screening, person-weighted description and exploratory prediction. Future work should independently validate the frozen model before updating it and test intended users’ task success, errors, time and perceived ease. Legal entitlement, causal explanations, human usability and external predictive validity remain unestablished.
