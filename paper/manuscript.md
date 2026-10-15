# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—This study analysed reported Older Person’s Grant (OPG) non-receipt among adults aged 60 or older in KwaZulu-Natal (KZN), using the Living Conditions Survey (LCS) 2014/2015. The study used administrative-burden theory to choose predictors and observable research rules to identify apparently eligible adults. Screening did not establish legal entitlement. Among 1,013 adults who passed with resolved receipt, 67 reported non-receipt: 6.6% unweighted and 7.5% person-weighted. Alternative screening rules gave weighted rates of 7.1%–9.1%. Logistic regression used five predictor groups and household-held-out validation. AUC (area under the receiver operating characteristic curve) was 0.752; average precision (AP) was 0.203. The Brier score was 0.0578, compared with 0.0618 for an intercept-only reference using training-group prevalence. Checks supported reproducibility. The application displays rules, decisions, scores and reports. No participant study tested ease of use. These results do not establish entitlement, explain non-receipt, or demonstrate performance elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [7], including during crises [8]. Other work examines receipt and access barriers [2], [6]. This study examines adults who appear eligible but report receiving no OPG.

The analysis separates screening, reported receipt and legal entitlement. Passing the research screen does not mean approval by the South African Social Security Agency [1]. Non-receipt can reflect high income, no application, a pending decision or incomplete information. The analysis must define the screened group before calculating its non-receipt percentage; missing spouse income can change that group.

The study aims to develop and evaluate an interpretable research tool for analysing reported OPG non-receipt among apparently eligible older adults in KwaZulu-Natal using the Living Conditions Survey (LCS) 2014/2015. Four objectives guide the work: document the included population, describe non-receipt using survey weights, test predictions on excluded households, and assess correctness, reproducibility and clarity.

Research questions (RQs) guide the study. RQ1 asks what proportion of screened adults reports non-receipt and how that proportion changes under different screening assumptions. RQ2 asks how well logistic regression separates recipients from non-recipients and estimates chances in excluded households. RQ3 asks whether the tool can repeat the analysis and clearly explain screening decisions and model results. The study combines documented rules, weighted percentages, tested predictions and a local interface to address them.

## II. Related Work and Predictor Selection

### A. Review Approach, Programme Context and Research Gap

The literature review used thematic narrative synthesis to examine grant access, eligibility measurement and prediction. Searches covered Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst. Search concepts included social assistance, eligibility, take-up, non-receipt, exclusion and prediction. Sources were considered for relevance to the research question, population, outcome and methodological contribution. Studies were compared by programme, setting, unit of analysis, outcome, findings and limitations. Differences in these features prevent a pooled non-receipt estimate.

The recorded search summary lists 511 records: 136 duplicates removed, 375 titles/abstracts screened, 222 excluded, 153 full texts assessed, 98 further exclusions and 55 retained sources. These sources cover several grants and populations, rather than 55 OPG studies. The available record documents the search concepts, broad selection criteria and aggregate counts. It does not preserve database-specific query strings, search dates and filters, original exports or record-level screening and exclusion decisions. The full 55-source extraction register is also unavailable. These omissions prevent independent reproduction of the search and verification of each selection decision. The synthesis therefore provides contextual evidence without establishing exhaustive literature coverage.

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

The research gap concerns how these separate strands can support a reproducible, person-level analysis of OPG non-receipt in KwaZulu-Natal. Ralston's age-based rural receipt analysis [2] and Godfrey's household receipt proportions [6] do not directly provide non-receipt estimates after the resource screen used here. Evidence on other grants informs possible access barriers, but does not establish their effects among older OPG applicants. The study addresses this integration gap by documenting the screening denominator, testing how alternative rules change non-receipt estimates, and evaluating an interpretable model on excluded households. Shared rules connect the research command and application so that decisions, probabilities and reports remain inspectable. The specific contribution is a historical workflow that connects transparent screening, person-weighted description, household-held-out prediction and reproducible software. This supports scrutiny of assumptions and results without establishing legal entitlement, causal barriers, participant usability or performance elsewhere.

### B. Grant Access and Administrative Burden

Administrative-burden theory distinguishes learning, compliance and psychological costs [12]. Grant studies describe paperwork, repeated visits, interrupted payments and difficult encounters [13]–[16]. Child Support Grant research suggests barriers [9], [10], without establishing their effects among older OPG applicants. Digital access can create difficulties [17]. Low non-receipt therefore does not demonstrate easy access.

LCS does not record every legal condition or application experience. The screen checks age, resources, partnership and other-grant rules. It assigns PASS (the person meets the research conditions), FAIL (a known condition is not met) or UNRESOLVED (available information cannot resolve the decision). The analysis then checks receipt separately. Only adults who pass with clear receipt answers enter the prediction study. Unclear or contradictory answers remain unresolved.

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

Few events motivate assessment of precision, calibration and ranking [20], [19]. Sample size and internal validation limit generalisation [21], [22]. Reporting follows TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) [23]. Software checks assess correctness and repeatability; usability requires participant evidence.

### D. Conceptual Framework

Reported OPG non-receipt among apparently eligible older adults motivates an administrative-burden perspective [12], [16]. Learning, compliance and psychological costs may obstruct access; high receipt does not establish low burden.

Figure 1 separates theoretical constructs from LCS measurements. Schooling may reflect information resources; office distance and settlement relate to potential compliance effort. Age and sex provide demographic context. These proxies do not directly measure burden. Screening defines the denominator because age alone is insufficient and LCS cannot establish legal entitlement. Resource, partnership and other-grant rules define the population; incomplete information remains unresolved. Reported receipt defines a separate outcome.

Person-weighted estimates describe non-receipt. Logistic regression describes associations; household-held-out validation tests predictions. Neither establishes causal mechanisms. The artefact implements the design through shared rules, separate receipt classifications, saved-model scoring and inspectable reports. Upload scores remain separate from held-out evaluation and never change screening or receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual framework. Theory informs predictor selection; observable screening defines the population for separate descriptive and predictive analyses. The dashed boundary identifies the artefact’s implementation scope. Arrows show conceptual rationale or analytical dependencies, not causal effects.

## III. Methods

### A. Data and study population

The analysis linked the LCS 2014/2015 person, household and person-income files through survey identifiers. Checks covered duplicates, unmatched records and row counts. The questionnaire, metadata and COICOP (Classification of Individual Consumption According to Purpose) codes guided interpretation [3]–[5]. The study covered sampled KwaZulu-Natal residents aged 60 or older in completed years. The survey excludes older adults living in institutions. Screening used the rules for each interview month. Before releasing the data, Statistics South Africa used hot-deck imputation for age and sex. The released files do not identify these records. The model handled missing predictors separately.

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

The screen summed already annualised, nominal person-income amounts, excluding social-assistance income. It did not allocate household income. A missing applicant or linked-spouse amount remained unresolved unless the no-income response and absent schedule supported zero. Assets, deemed income and permitted deductions were outside this research proxy.

GN 211 set the standard monthly maximum at R1,350 from 1 April 2014 [24]; GN 277 raised it to R1,410 from 1 April 2015 [25]. The 2014 amendment, Schedule paragraph 2, substituted D = 1.6A − 0.4B from 1 April 2014 [29]. With annual standard maximum A and minimum D = R1,200 (Annexure A(5)) [28], B = (1.6A − 1,200)/0.4. This yields annual single/couple research ceilings of R61,800/R123,600 for October 2014–March 2015 and R64,680/R129,360 for April–October 2015. Half-joint income doubles couple limits; equality passed. The screen applied these boundaries to its private-income proxy. Both notices add R20 for age 75+; the primary screen retained the standard maximum across ages, while S1c tested the supplement. S1 also tested period and payment-boundary alternatives.

The 2008 regulations define spouses (regulation 1), include spouse income regardless of property regime (18(2)) and use half-joint annual income (19(1)). They allow Agency-approved exclusion after continuous desertion for at least three months and unwillingness to support (18(3)) [28]. The July 2015 amendment left these OPG means provisions unchanged [30]. Survey responses established neither legal spouse status nor desertion conditions. Never-married, widowed and divorced adults used single ceilings. For married adults, research rules required resolved applicant/spouse incomes and reciprocal pointers linking a resident spouse; sums applied regardless of spouse age. Nonresident spouse income was unavailable; separated respondents lacked spouse details [5]. Cohabitation, unspecified status and missing/inconsistent links remained unresolved, without assumed single status or zero partner income. S2 tested alternatives.

An adult's reported disability or war-veterans grant caused FAIL. Caregiver child grants and grant-in-aid neither excluded the adult nor defined OPG receipt. A known failure took priority over unresolved information; the screen retained all reasons.

For adults who passed, the software interpreted general-grant and OPG answers together, including structural skips (questions omitted because earlier answers make them inapplicable). A consistent “no grant” answer can establish non-receipt when the OPG follow-up does not apply. Contradictory or unexplained answers remain unresolved and exclude the person from modelling. The analysis flagged disagreements between current receipt and preceding-year OPG income without changing the outcome because the periods differ. Rule version opg-kzn-primary-v1 records these decisions. The denominator contains adults who pass and have a clear receipt answer.

### C. Survey-weighted description and uncertainty

RQ1 used both the ordinary count proportion and the person-weighted proportion: p = Σ(wᵢYᵢ)/Σwᵢ. Here, wᵢ is a person's weight and Yᵢ equals 1 for non-receipt and 0 for receipt. Group comparisons describe differences; they do not establish causes.

The released files lack strata. Derived primary sampling units (PSUs) supported an estimate of sampling uncertainty. The calculation allows a group to be sampled more than once. It cannot reproduce the complete survey design. Adults with unresolved screening information remain outside the proportion. Receipt bounds (the lowest and highest rates if all unclear PASS receipt answers mean receipt or all mean non-receipt) tested the effect of unclear receipt answers.

### D. Model specification and validation

The unweighted logistic model estimated probability of reported non-receipt. The analysis did not rebalance recipients and non-recipients, automatically select variables or choose a cutoff. The model describes associations after accounting for other predictors. Age enters per decade above 60. Comparison categories are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five predictor groups require six slopes and an intercept, because settlement requires two comparisons.

Only one rural-formal adult reported non-receipt in the attempted seven-slope model. Excluding that person for testing left the training group with no such case in that category. Decision D-052 combined rural formal with traditional settlement to support estimation, without claiming that these settings are equivalent. Marital status affects screening; income, receipt, derived labels and marital status do not enter the primary model.

Validation used five household-grouped folds. Sorted households were labelled by whether any member reported non-receipt, then stratified so every adult from a household stayed in one fold. Seed 201415 fixes this division. The 1,013 adults come from 827 households: 182 contain more than one modelled adult, and 6 contain both receipt and non-receipt. Each adult received one out-of-fold (OOF) probability from a model trained without that household. Held-out folds had 199 to 207 adults and 12 to 14 non-recipients. The intercept-only reference uses the training group's non-receipt rate.

After interpreting skipped questions, each training fold supplied the fill-in for its held-out adults. Schooling contrasted below Grade 7 with Grade 7 or above, and office distance contrasted at least 5 km or unavailable with nearer than 5 km. Other codes stayed missing. The training fold filled missing age, in decades above 60, with its median, and a missing category with its most frequent code, or the smaller code in a tie. Eligibility, receipt and weights were not filled or modelled. Three recipients lacked usable schooling; 14 recipients and four non-recipients lacked usable office distance. Age, sex and settlement were already complete.

Pooled OOF probabilities supplied average precision, AUC, Brier score, calibration slope and calibration-in-the-large. Calibration-in-the-large is an intercept correction with its slope fixed at 1; the ideal values are 0 and 1. The 95% intervals are 2.5 and 97.5 percentiles from 1,000 with-replacement household samples of those fixed predictions, using the same seed. Every selected household's adults were retained. All 1,000 samples contained both outcome classes, but preprocessing, refitting and Decision D-052 were not repeated. The intervals omit a new split, fill-in and fit, and they omit primary sampling units, unreleased strata and person weights. They are not design-based confidence intervals.

### E. Alternative assumptions

S1 changes thresholds, S2 partnership assumptions, S3 rules about other grants, S4 income definition, S5 receipt period and S6 unresolved-receipt bounds. Each records the denominator, non-recipients, ordinary/person-weighted rates and internally validated model performance. S7 uses complete cases. S8 replaces welfare access with a married indicator. S9 uses frequency weights (treating person weights as repeated-record contributions), keeping unweighted missing-value treatment and evaluation. This is not a full survey-design regression. S10 weights primary OOF measures without refitting. S11 groups validation folds by derived PSU. These results remain separate from the primary analysis.

## IV. Software and Evaluation

The command python analysis/run_study.py links survey files, screens adults and calculates results. Run records retain settings, versions, seed, folds and checksums. The saved model stores coefficients and missing-value settings in JSON, without executable program code. Version opg-kzn-six-slope-v1 uses the model trained on all included adults. Uploads do not retrain it.

The local Streamlit app has five sections: study context, upload/validation, eligibility/receipt, prediction/model and export/reproducibility. It accepts historical opg-screen-v1 CSV files, including household members needed to check spouse resources. Validation rejects incorrect schema, study context, duplicate identifiers, categories and numeric values. Limits are 20 MiB and 50,000 rows. Uploads stay in memory during the current session. Reports use generated row labels and omit submitted identifiers, raw income and household links. The interface provides filters for views and exports, and summary rates retain all uploaded adults who pass with resolved receipt. Filters, labels and reports are functions of the program. They are not measurements of user experience.

FIGURE: figures/architecture.png | Fig. 2. Research and app workflows share screening rules. Household-held-out predictions remain separate from app scores calculated using the model trained on all included adults.

The app reuses the screening rules and saved model settings. It scores only supported adults who pass with resolved receipt. Saved training statistics fill partly missing predictors; records missing every categorical predictor remain unscored. Integrity checks link model and evaluation files to the analysis and predictor code. The interface labels historical OOF results separately from uploaded scores; uploaded records may overlap training data. CSV, JSON and ZIP reports contain classifications, reasons, supported probabilities, versions and an audit manifest (settings and file checksums). The downloadable minimum viable product, or MVP, uses invented data and excludes raw survey files, historical respondent outputs and Git version history.

Technical verification compares the program with specified expectations. The checks compared screening decisions with expected results and tested excluded predictors, links, repeated runs, reports and saved predictions. Further checks compared the command-line interface with the Streamlit interface, including invalid inputs and outdated results. These tests ask whether the software follows the stated rules and returns the same outputs. They do not ask whether a person finds the screen understandable.

The owner's Windows walkthrough belongs to that technical record. The author ran the synthetic workflow on the local installation, and the exported files were compared with expected contents. The result shows that this installation produced the specified reports. The author is not an independent participant, and the walkthrough does not measure ease, errors or acceptance by someone else.

Usability evaluation is a separate study. It would ask people other than the developer to attempt set tasks and would record completion, time taken, errors, ease and any assistance given. A protocol for three to five consenting users, restricted to synthetic records, has been written and has not been used. No participant has been recruited. No task time, error count, ease rating or acceptance result exists. Participant usability remains untested. Automated interface checks and the owner walkthrough do not fill that gap. An automated Streamlit test checks program state. It is not a session with a nontechnical participant.

## V. Results

### A. Study group and reported non-receipt

The survey included 15,388 people in 3,686 KwaZulu-Natal households. Table IV shows the selection steps. People aged 60 or older equal the failed, unresolved and passed rows. Reported receipt and non-receipt divide the passed row. Households are counted inside each row, and one household can contribute to more than one row. Among 117 failures, 93 exceeded the income ceiling and 25 reported a disability grant; one met both conditions. None reported a war-veterans grant. Among 187 unresolved adults, 105 were married, mostly with a non-resident spouse, and 63 reported living together. Unresolved adults outnumbered non-recipients.

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

NOTE: People aged 60 or older equal 117 + 187 + 1,013. The passed row equals 946 + 67. Adding every people cell would count the same adults more than once. Each household cell counts distinct households in that row. Those cells do not follow the people partition.

FIGURE: figures/cohort_flow.png | Fig. 3. FAIL, UNRESOLVED and PASS groups do not overlap. All 1,013 PASS adults resolve receipt and enter the final denominator.

Of these 1,013 adults, 67 reported non-receipt: 6.61% without weights and 7.49% with person weights. The calculation used 345 derived PSUs and gave a standard error of 1.3 percentage points. A bell-shaped sampling approximation gave a 95% confidence interval of 4.9%–10.0%. Missing strata limit this approximation. It is not a design-based confidence interval, and it does not apply to Tables V–VIII. All 1,013 PASS answers agreed with preceding-year OPG income, so those checks changed nothing. Table V compares five predictors before filling missing values. Average age and percentages describe each receipt group. The percentages describe receipt-group composition, not non-receipt rates or predictions. Table V reports no standard errors.

TABLE: Table V. Characteristics by receipt, before filling missing values
| Characteristic | Recipients | Non-recipients |
| --- | --- | --- |
| Age, average years | 70.4; 69.8 | 67.3; 68.4 |
| Female | 686 (72.5%); 70.4% | 33 (49.3%); 53.4% |
| Grade 7 or above | 290 (30.7%); 33.0% | 49 (73.1%); 80.8% |
| Urban formal settlement | 284 (30.0%); 36.2% | 38 (56.7%); 66.2% |
| Office ≥5 km or unavailable | 717 (75.8%); 72.0% | 34 (50.7%); 40.3% |

NOTE: Recipients: 946 people. Non-recipients: 67 people. Each cell gives the unweighted figure, then the person-weighted figure. A category cell gives an unweighted count and percentage inside that receipt group, then the weighted percentage. These percentages describe the composition of each group. They are not non-receipt rates and they are not predictions. Three recipients lack schooling. Fourteen recipients and four non-recipients lack an office-distance value. Those adults remain in the group denominators. This table has no uncertainty intervals.

In the unweighted figures, non-recipients had a lower average age and were more often men, educated to Grade 7 or above, and living in urban formal settlements. Weighting brought the average ages closer. These are descriptions of the two groups. Table V does not test the differences.

### B. Screening sensitivity

Table VI reports each scenario's denominator and non-receipt events. Unw. and Wtd. abbreviate unweighted and person-weighted non-receipt. Slope means calibration slope in Tables VI and VIII. Compared with S0, S1b/S1d added two people/two events. S2a, S2b, S2c and S2d added 59/4, 60/2, 8/0 and 68/2 people/events. S3 added 19 people/15 events; S4b removed six people but no events. Weighted non-receipt ranged from 7.12% to 9.06%. Held-out AUC in this table runs from 0.736 to 0.763. Brier and calibration slope also change. AUC, Brier and slope are point estimates, and the table gives them no intervals. A close AUC does not make the screened groups the same population, and it does not show which rule predicts better.

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

NOTE: Events are reported non-recipients. Unw. and Wtd. are the unweighted and person-weighted non-receipt rates. AUC, Brier and slope are unweighted out-of-fold point estimates, with no intervals in this table. Performance uses no weights. Same* is not a new result. It repeats the S0 row for the scenarios that left the sample and the measures unchanged.

S1b applies the 2015 ceiling to every interview. S1d uses the ceiling at which the formula pays nothing. The two settings are different, and the saved counts and measures match, so one row displays both. S2a screens living-together adults as couples. S2b screens them as single. S2c screens separated adults as single. S2d screens both living-together and separated adults as single. S3 retains adults who report a disability or war-veterans grant. It adds no veterans. S4b keeps social-assistance income in the resource proxy.

*S1a uses the 2014 ceiling throughout. S1c adds the age-75 supplement. S4a adjusts income for price changes and leaves the ceiling unchanged. S4c also excludes UIF (the Unemployment Insurance Fund) and similar transfers. S5 uses preceding-year receipt. S6a and S6b assign unresolved receipt to receipt or to non-receipt. No passed adult has unresolved receipt to bound, so those bounds change nothing. Each starred scenario keeps the S0 denominator, events and measures.

### C. Held-out prediction

All five folds converged. Figure 4 uses five similarly sized bins. The highest bin had average prediction 0.188 and 35/203 non-recipients (17.2%); the lowest had average 0.0107 and 3/206 non-recipients (1.5%).

TABLE: Table VII. Primary held-out performance and resampling intervals
| Metric | Logistic model | Intercept-only |
| --- | --- | --- |
| AUC | .752 [.687–.814] | — |
| Average precision | .203 [.139–.292] | — |
| Brier score | .0578 [.0448–.0706] | .0618 [.0467–.0758] |
| Calibration-in-the-large | .020 [−.316–.273] | .0001 |
| Calibration slope | .836 [.591–1.133] | — |

NOTE: Each logistic cell is the estimate and its 95% interval. Estimates pool unweighted out-of-fold predictions from 1,013 people and 67 events. An interval is the 2.5 and 97.5 percentiles of 1,000 household resamples of those fixed predictions. Every reported interval had 1,000 valid resamples and no invalid resample. Resampling did not refit the model or the missing-value fill. These intervals are not design-based confidence intervals. They are not the survey approximation in Section V.A, and they are not the Wald intervals beside the odds ratios below. The intercept-only reference uses the training group's non-receipt rate. Its calibration-in-the-large is .0001, and no resampling interval was saved for that value. A dash means the intercept-only model does not supply that measure. A dash is not zero and is not chance performance. The ideal calibration-in-the-large is 0. The ideal slope is 1.

FIGURE: figures/calibration.png | Fig. 4. Saved group summaries show unweighted OOF calibration. Labels give events/people; the diagonal shows exact agreement between average predictions and observed rates. Plot range: 0–0.22.

The odds ratio for women versus men was 0.39. Its Wald interval was 0.23–0.66. Schooling below Grade 7 versus Grade 7 or above gave 0.24 (0.13–0.43). The model trained on all included adults produced these estimates. The intervals exponentiate that model's coefficients and standard errors. They are not the Table VII resampling intervals, and they do not measure held-out performance. Age, settlement and welfare-distance intervals included 1. These associations describe odds, not probability reductions, held-out performance or causes.

TABLE: Table VIII. Model and validation sensitivities, as point estimates
| Scenario | N/events | Unw. | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- |
| S0 primary | 1,013/67 | 6.61 | .752 | .0578 | .836 |
| S7 complete | 992/63 | 6.35 | .758 | .0556 | .819 |
| S8 married | 1,013/67 | 6.61 | .755 | .0578 | .846 |
| S9 wtd. fit | 1,013/67 | 6.61 | .750 | .0583 | .718 |
| S10 wtd. measures | 1,013/67 | 6.61 | .763 | .0641 | .935 |
| S11 PSU folds | 1,013/67 | 6.61 | .758 | .0575 | .860 |

NOTE: Unw. is the unweighted non-receipt percentage. AUC, Brier and slope are point estimates. This table does not report intervals for them. S8–S11 keep the person-weighted non-receipt rate at 7.49%. S7 keeps adults with usable schooling and office distance. It removes 21 people and four events, so its Brier describes a smaller sample. S8 replaces office distance with a married indicator and keeps six slopes. S9 fits with person weights as frequency weights. It still fills missing values without weights and checks predictions without weights. That fit is not a full survey-design regression. S10 applies person weights to the primary out-of-fold predictions and does not refit. S11 groups the five folds by derived primary sampling unit and keeps the same adults.

In Table VIII, AUC runs from 0.750 to 0.763. The lowest Brier is the complete-case row. The highest Brier is the weighted-score row, which reuses the primary predictions. These differences have no intervals. They do not rank the specifications.

### D. Software verification

The 26 checks in Table IX included 22 synthetic screening cases (invented records with specified expected decisions), two income-schedule checks, one forbidden-predictor check and one run trace. Boundary, spouse, grant and receipt decisions matched their specifications. Two research runs produced 14 files with exactly matching contents and retained the study-group checksum.

TABLE: Table IX. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Check rules, schedules, excluded predictors and run tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Check software, app state and exports; includes 18 Streamlit interface tests. |
| App–command agreement | 15,388/15,388 agree; 1,013 scored | Both paths select the same people and give the same decisions, receipt, reasons and outcome. |
| Reloaded model scores | Maximum score difference 5.55 × 10⁻¹⁷ | Reloading preserves saved-model scores; this does not assess OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Check synthetic local use and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The owner's Windows walkthrough produced six synthetic classifications: two resolved passes, one recipient and one non-recipient. Matching predictors gave both scores of 0.1853. The invented 50% rate is not the survey non-receipt rate. Screenshots and six extracted reports documented the walkthrough. The checks did not inspect the ZIP container. Regenerated outputs, checksums, summaries and model/source versions passed 50 checks. This verifies functions and exports, not independent execution or representative task times, errors or ease.

## VI. Discussion

### A. Scope of measured non-receipt

RQ1 measures non-receipt among historical KwaZulu-Natal adults who pass the screen and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. This does not measure unlawful denial or non-receipt among everyone legally entitled. The 187 unresolved adults outnumbered the 67 events. Excluding them changes the population described, regardless of sampling uncertainty. Stable estimates cannot reveal their receipt.

S2d added 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly changed the denominator. S3 retained adults with incompatible grants, added 19 people/15 events and raised non-receipt to 9.06%, the largest tested change. Table VI gives AUC, Brier and slope as point estimates on those changed denominators, without intervals. Similar AUC cannot justify screening rules or establish equivalent populations. Ralston studies rural age-eligible people [2]; Godfrey studies households' grants [6]. Different units, programmes, screens and places prevent direct comparison of their percentages. This study adds a provincial estimate with an explicit resource screen. High receipt can involve access costs [12], [16]; it cannot prove low burden.

### B. Predictive performance and interpretation

RQ2 assesses four properties. AUC 0.752 describes ranking held-out non-recipients above recipients, not classification accuracy. Its Table VII interval, 0.687–0.814, lies above 0.5 for these fixed predictions. The interval still describes ranking, not accuracy at a cutoff. AP 0.203 summarises precision–recall ranking across cutoffs against a 6.61% event rate, not precision at one cutoff [20]. Its interval, 0.139–0.292, lies above that event rate. Brier fell from 0.0618 to 0.0578: a modest 0.0040 reduction in squared probability error. The two Brier intervals overlap, and no interval was calculated for the difference. An intercept correction, with calibration slope fixed at 1, checks average bias. The ideal correction is zero. The estimate 0.020 and interval spanning zero do not prove perfect agreement. Slope 0.836 suggests predictions may be too extreme, but its 0.591–1.133 interval includes the ideal 1 [19]. Only 67 events informed these checks [21]. Most adults in even the highest-risk bin reported receipt.

The Table VII intervals resample fixed out-of-fold predictions by household. They are not the survey approximation in Section V.A. They are not the Wald intervals around the full-sample odds ratios.

Table VIII separates sample, predictor and evaluation changes. It reports point estimates only. S7 removed 21 people/four events (992/63). Its lower Brier concerns a different sample and cannot establish whether filling missing values is better. S8 substituted marriage for welfare access and performed similarly. S9 weighted fitting but not evaluation; it does not model the full survey design. S10 reweighted the same primary OOF predictions without retraining, raising Brier to 0.0641. S11 grouped folds by derived PSU and also performed similarly. S8–S11 retained 1,013 people/67 events. These checks expose internal assumptions; they do not establish model superiority or reliability elsewhere [22], [23].

### C. Technical verification, separate from usability

RQ3 asks whether the tool can repeat the analysis and clearly explain screening decisions and model results. The completed evidence concerns repetition and the presence of those explanations in the program. It does not show that an independent person finds the explanations clear.

Table IX keeps the technical checks separate from the usability row. Synthetic cases compare rule decisions with specified outcomes. Matching file contents check that a repeated run produces the same outputs. Agreement between the interface and the command checks that both paths select the same people and return the same decisions, receipt, reasons and scores. Reloading the saved model checks that stored predictions are preserved. That reload is not a new estimate of predictive accuracy. The owner walkthrough checks that the author could run the synthetic workflow locally and that the exported files matched the programmed comparisons. Saved sources and validation reports document versions, checksums and test conditions. Together, these layers support technical correctness and repeatability inside the tests that were run.

The application keeps historical out-of-fold results separate from scores for an uploaded file. An upload may overlap the training data. A matching reloaded score confirms the stored model. It does not show how the model would perform for new people, and it does not show that a user understands the distinction.

None of these checks is a usability evaluation. A usability study would recruit people other than the developer, give them the prepared tasks, and record completion, time, errors, ease and assistance. That protocol has not been used. Participant usability remains untested. The paper therefore makes no claim about user experience, ease of use, acceptance or success in ordinary work. An automated Streamlit test checks the program. The owner's own run cannot substitute for an independent participant.

### D. Transfer to other settings

This study analysed screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in settlement, services, policy and reporting. Application, award and payment records measure different events from reported receipt and can contain linking errors. The study did not test the model on an independent province, period or administrative sample. Transfer requires comparable populations/outcomes, justified period-specific rules and independent ranking/calibration checks [22], [23]. Making the app available cannot establish suitability for today's applicants.

### E. Synthesis of the Conceptual Framework

Returning to Figure 1, screening sensitivity supported an explicit denominator, and sex differences supported demographic comparison without confirming burden mechanisms [2], [6]. Lower schooling accompanied receipt, contrary to a simple expectation that fewer information resources increase non-receipt [12]. Screening selection or other resources could account for this; neither explanation was tested. Office-distance and settlement intervals included 1, leaving compliance-cost expectations unresolved. Psychological costs remained untested because LCS did not measure them. Proxy associations do not directly test the theory. The artefact contributes a reproducible implementation of these bounded measurement choices. Separate, traceable rules, outcomes and predictions support inspection despite measurement limits, without establishing causes, legal entitlement or participant usability.

## VII. Limitations and Ethics

The survey cannot establish legal eligibility: its resource proxy omits assets, deemed income and deductions. Respondents may misreport income and receipt. Cross-sectional data cannot establish the order of events. Few events, unresolved screening, missing strata and resampling fixed predictions without refitting limit inference. Household sampling excludes institutionalised older adults. Participant usability and performance elsewhere remain untested.

Survey access conditions and disclosure requirements apply. Interface demonstrations and tests use synthetic records. The downloadable package excludes survey records. Displays and reports omit submitted identifiers and raw income. These controls do not establish disclosure review of every historical repository file. The project records contain no DUT (Durban University of Technology) ethics determination. The paper therefore claims no approval. The app explains measurement choices; it neither decides grants nor ranks named applicants.

## VIII. Conclusion

Historical screened non-receipt was 6.6% unweighted and 7.5% person-weighted; alternatives gave 7.1%–9.1%. Rules about other grants changed results more than the ceiling, and unresolved cases made the denominator central. Five predictor groups/six slopes gave AUC 0.752, AP 0.203 and Brier 0.0578: moderate internal ranking with slightly less probability error. The software reproduces screening, receipt categories and scores for inspection under tested conditions. The study provides a historical benchmark. It does not establish human usability, causes, legal entitlement or performance elsewhere.
