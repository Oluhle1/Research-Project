# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—This study analysed reported Older Person’s Grant (OPG) non-receipt among adults aged 60 or older in KwaZulu-Natal (KZN), using the Living Conditions Survey (LCS) 2014/2015. The study used administrative-burden theory to choose predictors and observable research rules to identify apparently eligible adults. Screening did not establish legal entitlement. Among 1,013 adults who passed with resolved receipt, 67 reported non-receipt: 6.6% unweighted and 7.5% person-weighted. Alternative screening rules gave weighted rates of 7.1%–9.1%. Logistic regression used five predictor groups and household-held-out validation. AUC (area under the receiver operating characteristic curve) was 0.752; average precision (AP) was 0.203. The Brier score was 0.0578, compared with 0.0618 for an intercept-only reference using training-group prevalence. Checks supported reproducibility. The application displays rules, decisions, scores and reports. No participant study tested ease of use. These results do not establish entitlement, explain non-receipt, or demonstrate performance elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [1], including during crises [2]. Other work examines receipt and access barriers [3], [4]. This study examines adults who appear eligible but report receiving no OPG.

The analysis separates screening, reported receipt and legal entitlement. Passing the research screen does not mean approval by the South African Social Security Agency [5]. Non-receipt can reflect high income, no application, a pending decision or incomplete information. The analysis must define the screened group before calculating its non-receipt percentage; missing spouse income can change that group.

The study aims to develop and evaluate an interpretable research tool for analysing reported OPG non-receipt among apparently eligible older adults in KwaZulu-Natal using the Living Conditions Survey (LCS) 2014/2015. Four objectives guide the work: document the included population, describe non-receipt using survey weights, test predictions on excluded households, and assess correctness, reproducibility and clarity.

Research questions (RQs) guide the study. RQ1 asks what proportion of screened adults reports non-receipt and how that proportion changes under different screening assumptions. RQ2 asks how well logistic regression separates recipients from non-recipients and estimates chances in excluded households. RQ3 asks whether the tool can repeat the analysis and clearly explain screening decisions and model results. The study combines documented rules, weighted percentages, tested predictions and a local interface to address them.

## II. Related Work and Predictor Selection

### A. Review Approach, Programme Context and Research Gap

The literature review used thematic narrative synthesis to examine grant access, eligibility measurement and prediction. Searches covered Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst. Search concepts included social assistance, eligibility, take-up, non-receipt, exclusion and prediction. Sources were considered for relevance to the research question, population, outcome and methodological contribution. Studies were compared by programme, setting, unit of analysis, outcome, findings and limitations. Differences in these features prevent a pooled non-receipt estimate.

The recorded search summary lists 511 records: 136 duplicates removed, 375 titles/abstracts screened, 222 excluded, 153 full texts assessed, 98 further exclusions and 55 retained sources. These sources cover several grants and populations, rather than 55 OPG studies. The available record documents the search concepts, broad selection criteria and aggregate counts. It does not preserve database-specific query strings, search dates and filters, original exports or record-level screening and exclusion decisions. The full 55-source extraction register is also unavailable. These omissions prevent independent reproduction of the search and verification of each selection decision. The synthesis therefore provides contextual evidence without establishing exhaustive literature coverage.

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

The research gap concerns how these separate strands can support a reproducible, person-level analysis of OPG non-receipt in KwaZulu-Natal. Ralston's age-based rural receipt analysis [3] and Godfrey's household receipt proportions [4] do not directly provide non-receipt estimates after the resource screen used here. Evidence on other grants informs possible access barriers, but does not establish their effects among older OPG applicants. The study addresses this integration gap by documenting the screening denominator, testing how alternative rules change non-receipt estimates, and evaluating an interpretable model on excluded households. Shared rules connect the research command and application so that decisions, probabilities and reports remain inspectable. The specific contribution is a historical workflow that connects transparent screening, person-weighted description, household-held-out prediction and reproducible software. This supports scrutiny of assumptions and results without establishing legal entitlement, causal barriers, participant usability or performance elsewhere.

### B. Grant Access and Administrative Burden

Administrative-burden theory distinguishes learning, compliance and psychological costs [13]. Grant studies describe paperwork, repeated visits, interrupted payments and difficult encounters [8], [9], [10], [14]. Child Support Grant research suggests barriers [6], [7], without establishing their effects among older OPG applicants. Digital access can create difficulties [15]. Low non-receipt therefore does not demonstrate easy access.

LCS does not record every legal condition or application experience. The screen checks age, resources, partnership and other-grant rules. It assigns PASS (the person meets the research conditions), FAIL (a known condition is not met) or UNRESOLVED (available information cannot resolve the decision). The analysis then checks receipt separately. Only adults who pass with clear receipt answers enter the prediction study. Unclear or contradictory answers remain unresolved.

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

Few events motivate assessment of precision, calibration and ranking [16], [17]. Sample size and internal validation limit generalisation [18], [19]. Reporting follows TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) [20]. Software checks assess correctness and repeatability; usability requires participant evidence.

### D. Conceptual Framework

Reported OPG non-receipt among apparently eligible older adults motivates an administrative-burden perspective [13], [14]. Learning, compliance and psychological costs may obstruct access; high receipt does not establish low burden.

Figure 1 separates theoretical constructs from LCS measurements. Schooling may reflect information resources; office distance and settlement relate to potential compliance effort. Age and sex provide demographic context. These proxies do not directly measure burden. Screening defines the denominator because age alone is insufficient and LCS cannot establish legal entitlement. Resource, partnership and other-grant rules define the population; incomplete information remains unresolved. Reported receipt defines a separate outcome.

Person-weighted estimates describe non-receipt. Logistic regression describes associations; household-held-out validation tests predictions. Neither establishes causal mechanisms. The artefact implements the design through shared rules, separate receipt classifications, saved-model scoring and inspectable reports. Upload scores remain separate from held-out evaluation and never change screening or receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual framework. Theory informs predictor selection; observable screening defines the population for separate descriptive and predictive analyses. The dashed boundary identifies the artefact’s implementation scope. Arrows show conceptual rationale or analytical dependencies, not causal effects.

## III. Methods

### A. Data and study population

The analysis linked the LCS 2014/2015 person, household and person-income files through survey identifiers. Checks covered duplicates, unmatched records and row counts. The questionnaire, metadata and COICOP (Classification of Individual Consumption According to Purpose) codes guided interpretation [21], [22], [23]. The study covered sampled KwaZulu-Natal residents aged 60 or older in completed years. The survey excludes older adults living in institutions. Screening used the rules for each interview month. Before releasing the data, Statistics South Africa used hot-deck imputation for age and sex. The released files do not identify these records. The model handled missing predictors separately.

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

The screen summed reported yearly income to estimate private resources. It excluded social-assistance income so receiving a grant would not cause a failure. It did not divide household totals among individuals. A missing income record counts as zero only when the source indicator confirms no reported income; otherwise, the screen leaves it unresolved. Asset purchases do not measure total asset holdings. The data cannot establish the full legal asset test, income assigned under legal rules or permitted deductions.

The income ceiling corresponds to a formula payment of R100 monthly. From April 2014, the ceilings are R61,800 for a single person and R123,600 for a couple; from April 2015, they are R64,680 and R129,360 [24], [25]. The screen included amounts exactly at the interview-month ceiling. These research limits do not establish legal eligibility. The legal formula and couple-threshold interpretation remain unverified. Alternative analyses tested thresholds and income definitions.

For married adults, the screen combined applicant and spouse resources only after linking a resident spouse and confirming the relationship. Never-married, widowed and divorced adults use the single ceiling. Living-together, separated, absent-spouse and failed-link cases remain unresolved in the primary analysis. The screen does not treat unknown partner resources as zero or classify ambiguous partnerships as single. Alternative analyses relaxed these choices. An adult's own disability or war-veterans grant causes a failure. Caregiver child grants and grant-in-aid (an extra grant for people who need full-time care) do not exclude the adult or define OPG receipt. A known failure takes priority over missing information; the software retains all reasons.

For adults who passed, the software interpreted general-grant and OPG answers together, including structural skips (questions omitted because earlier answers make them inapplicable). A consistent “no grant” answer can establish non-receipt when the OPG follow-up does not apply. Contradictory or unexplained answers remain unresolved and exclude the person from modelling. The analysis flagged disagreements between current receipt and preceding-year OPG income without changing the outcome because the periods differ. Rule version opg-kzn-primary-v1 records these decisions. The denominator contains adults who pass and have a clear receipt answer.

### C. Survey-weighted description and uncertainty

RQ1 used both the ordinary count proportion and the person-weighted proportion: p = Σ(wᵢYᵢ)/Σwᵢ. Here, wᵢ is a person's weight and Yᵢ equals 1 for non-receipt and 0 for receipt. Group comparisons describe differences; they do not establish causes.

The released files lack strata. Derived primary sampling units (PSUs) supported an estimate of sampling uncertainty. The calculation allows a group to be sampled more than once. It cannot reproduce the complete survey design. Adults with unresolved screening information remain outside the proportion. Receipt bounds (the lowest and highest rates if all unclear PASS receipt answers mean receipt or all mean non-receipt) tested the effect of unclear receipt answers.

### D. Model specification and validation

The unweighted logistic model estimated probability of reported non-receipt. The analysis did not rebalance recipients and non-recipients, automatically select variables or choose a cutoff. The model describes associations after accounting for other predictors. Age enters per decade above 60. Comparison categories are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five predictor groups require six slopes and an intercept, because settlement requires two comparisons.

Only one rural-formal adult reported non-receipt in the attempted seven-slope model. Excluding that person for testing left the training group with no such case in that category. Decision D-052 combined rural formal with traditional settlement to support estimation, without claiming that these settings are equivalent. Marital status affects screening; income, receipt, derived labels and marital status do not enter the primary model.

Validation used five folds. The split kept households together and balanced the folds by whether any member reported non-receipt. Seed 201415 fixes this division. After interpreting skipped questions, the software filled missing predictors using training-group statistics only. It never filled missing eligibility or outcome information. Each adult received one out-of-fold (OOF) probability from a model trained without that adult's household.

Evaluation measured average precision, AUC, Brier score, calibration slope and calibration-in-the-large. Ideal values are 1 for calibration slope and zero for calibration-in-the-large, which estimates an intercept correction with the slope fixed at 1. The intercept-only reference model uses the training group's non-receipt rate. Bootstrap intervals used 1,000 household samples and fixed OOF predictions. Without model refitting, these intervals omit uncertainty from repeating model development.

### E. Alternative assumptions

S1 changes thresholds, S2 partnership assumptions, S3 rules about other grants, S4 income definition, S5 receipt period and S6 unresolved-receipt bounds. Each records the denominator, non-recipients, ordinary/person-weighted rates and internally validated model performance. S7 uses complete cases. S8 replaces welfare access with a married indicator. S9 uses frequency weights (treating person weights as repeated-record contributions), keeping unweighted missing-value treatment and evaluation. This is not a full survey-design regression. S10 weights primary OOF measures without refitting. S11 groups validation folds by derived PSU. These results remain separate from the primary analysis.

## IV. Software and Evaluation

The command python analysis/run_study.py links survey files, screens adults and calculates results. Run records retain settings, versions, seed, folds and checksums. The saved model stores coefficients and missing-value settings in JSON, without executable program code. Version opg-kzn-six-slope-v1 uses the model trained on all included adults. Uploads do not retrain it.

The local Streamlit app has five sections: study context, upload/validation, eligibility/receipt, prediction/model and export/reproducibility. It accepts historical opg-screen-v1 CSV files, including household members needed to check spouse resources. Validation rejects incorrect schema, study context, duplicate identifiers, categories and numeric values. Limits are 20 MiB and 50,000 rows. Uploads stay in memory during the current session. Reports use generated row labels and omit submitted identifiers, raw income and household links. Users can filter views and exports; summary rates retain all uploaded adults who pass with resolved receipt.

FIGURE: figures/architecture.png | Fig. 2. Research and app workflows share screening rules. Household-held-out predictions remain separate from app scores calculated using the model trained on all included adults.

The app reuses the screening rules and saved model settings. It scores only supported adults who pass with resolved receipt. Saved training statistics fill partly missing predictors; records missing every categorical predictor remain unscored. Integrity checks link model and evaluation files to the analysis and predictor code. The interface labels historical OOF results separately from uploaded scores; uploaded records may overlap training data. CSV, JSON and ZIP reports contain classifications, reasons, supported probabilities, versions and an audit manifest (settings and file checksums). The downloadable minimum viable product, or MVP, uses invented data and excludes raw survey files, historical respondent outputs and Git version history.

Software checks compared screening decisions with expected results and tested excluded predictors, links, repeated runs, reports and saved predictions. Further checks compared the CLI (command-line interface) with the UI (user interface), including invalid inputs and outdated results. The owner's Windows walkthrough demonstrated local functionality. A task sheet supports future testing with three to five consenting participants; no participant study has taken place.

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

Of these 1,013 adults, 67 reported non-receipt: 6.61% without weights and 7.49% with person weights. The calculation used 345 derived PSUs and gave a standard error of 1.3 percentage points. A bell-shaped sampling approximation gave a 95% confidence interval of 4.9%–10.0%. Missing strata limit this approximation. All 1,013 PASS answers agreed with preceding-year OPG income, so those checks changed nothing. Table V compares five predictors before filling missing values. Average age and percentages describe each receipt group. The percentages describe receipt-group composition, not non-receipt rates or predictions.

TABLE: Table V. Characteristics by receipt (U = unweighted; W = person-weighted)
| Characteristic | Recipients: U; W | Non-recipients: U; W |
| --- | --- | --- |
| Age, average years | 70.4; 69.8 | 67.3; 68.4 |
| Female | 686 (72.5%); 70.4% | 33 (49.3%); 53.4% |
| Grade 7 or above | 290 (30.7%); 33.0% | 49 (73.1%); 80.8% |
| Urban formal settlement | 284 (30.0%); 36.2% | 38 (56.7%); 66.2% |
| Welfare office ≥5 km/unavailable | 717 (75.8%); 72.0% | 34 (50.7%); 40.3% |

NOTE: Recipients: 946 people; non-recipients: 67 people. U gives unweighted averages, or counts and percentages within each group. W gives person-weighted averages/percentages. Denominators retain missing predictors: three recipients lack schooling; 14 recipients/four non-recipients lack welfare-access values. These summaries have no uncertainty intervals.

Non-recipients were younger before weighting, more often men, more educated and more often urban formal residents. Weights brought average ages closer.

### B. Screening sensitivity

Table VI reports each scenario’s denominator and non-receipt events. Unw. and Wtd. abbreviate unweighted and person-weighted. Slope means calibration slope in Tables VI and VIII. Compared with S0, S1b/S1d added two people/two events. S2a, S2b, S2c and S2d added 59/4, 60/2, 8/0 and 68/2 people/events. S3 added 19 people/15 events; S4b removed six people but no events. Weighted non-receipt ranged from 7.12% to 9.06%.

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

NOTE: Events are reported non-recipients. Unw./Wtd. give unweighted/person-weighted non-receipt rates; performance uses no weights. S1b applies the 2015 ceiling throughout; S1d uses the zero-payout ceiling (the resource level where the grant formula pays zero). S2a/S2b treat living-together adults as couples/single. S2c treats separated adults as single; S2d treats both as single. S3 retains disability/war-veterans grant recipients (it adds no veterans). S4b retains social-assistance income.

*S1a (2014 ceiling throughout), S1c (age-75 supplement), S4a (income adjusted for price changes, with the ceiling unchanged), S4c (excluding UIF, the Unemployment Insurance Fund, and similar transfers), S5 (preceding-year receipt) and S6a/S6b (receipt bounds) change nothing. Each keeps the denominator, events and measures. No PASS adult has unresolved receipt to bound.

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

The odds ratio for women versus men was 0.39. Its Wald interval was 0.23–0.66. Schooling below Grade 7 versus Grade 7 or above gave 0.24 (0.13–0.43). The model trained on all included adults produced these estimates. Age, settlement and welfare-distance intervals included 1. These associations describe odds, not probability reductions, held-out performance or causes.

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

Across alternatives, AUC ranged from 0.736 to 0.763; Brier and calibration slopes also changed.

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

S2d added 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly changed the denominator. S3 retained adults with incompatible grants, added 19 people/15 events and raised non-receipt to 9.06%, the largest tested change. Similar AUC cannot justify screening rules or establish equivalent populations. Ralston studies rural age-eligible people [3]; Godfrey studies households' grants [4]. Different units, programmes, screens and places prevent direct comparison of their percentages. This study adds a provincial estimate with an explicit resource screen. High receipt can involve access costs [13], [14]; it cannot prove low burden.

### B. Predictive performance and interpretation

RQ2 assesses four properties. AUC 0.752 describes ranking held-out non-recipients above recipients, not classification accuracy. AP 0.203 summarises precision–recall ranking across cutoffs against a 6.61% event rate, not precision at one cutoff [16]. Brier fell from 0.0618 to 0.0578: a modest 0.0040 reduction in squared probability error. An intercept correction, with calibration slope fixed at 1, checks average bias. The ideal correction is zero. The estimate 0.020 and interval spanning zero do not prove perfect agreement. Slope 0.836 suggests predictions may be too extreme, but its 0.591–1.133 interval includes the ideal 1 [17]. Only 67 events informed these checks [18]. Most adults in even the highest-risk bin reported receipt.

Table VIII separates sample, predictor and evaluation changes. S7 removed 21 people/four events (992/63). Its lower Brier concerns a different sample and cannot establish whether filling missing values is better. S8 substituted marriage for welfare access and performed similarly. S9 weighted fitting but not evaluation; it does not model the full survey design. S10 reweighted the same primary OOF predictions without retraining, raising Brier to 0.0641. S11 grouped folds by derived PSU and also performed similarly. S8–S11 retained 1,013 people/67 events. These checks expose internal assumptions; they do not establish model superiority or reliability elsewhere [19], [20].

### C. Reproducibility and usability

RQ3 has six evidence layers. Synthetic cases check rule decisions; matching file contents check repeatability; UI–CLI agreement checks software paths; JSON reload checks saved-model predictions. The owner walkthrough checks a synthetic workflow; participant testing would assess human usability. Table IX supports the first five within tested conditions. Automated agreement cannot establish independent user ease, acceptance or field success. Saved sources and run/validation reports document versions, checksums and test conditions.

The app separates historical OOF results from uploaded scores; uploads may overlap training data. Matching saved scores checks reloading, not new predictive accuracy. The software exposes its computations, but representative user clarity remains untested. The task sheet supports future testing.

### D. Transfer to other settings

This study analysed screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in settlement, services, policy and reporting. Application, award and payment records measure different events from reported receipt and can contain linking errors. The study did not test the model on an independent province, period or administrative sample. Transfer requires comparable populations/outcomes, justified period-specific rules and independent ranking/calibration checks [19], [20]. Making the app available cannot establish suitability for today's applicants.

### E. Synthesis of the Conceptual Framework

Returning to Figure 1, screening sensitivity supported an explicit denominator, and sex differences supported demographic comparison without confirming burden mechanisms [3], [4]. Lower schooling accompanied receipt, contrary to a simple expectation that fewer information resources increase non-receipt [13]. Screening selection or other resources could account for this; neither explanation was tested. Office-distance and settlement intervals included 1, leaving compliance-cost expectations unresolved. Psychological costs remained untested because LCS did not measure them. Proxy associations do not directly test the theory. The artefact contributes a reproducible implementation of these bounded measurement choices. Separate, traceable rules, outcomes and predictions support inspection despite measurement limits, without establishing causes, legal entitlement or participant usability.

## VII. Limitations and Ethics

The survey cannot fully establish legal eligibility: its resource measure omits assets, deemed income (income the law assigns rather than the survey observes) and deductions. Income and receipt reports may contain errors. Cross-sectional data cannot establish the order of events. Few events, unresolved eligibility, missing strata and resampling fixed predictions without refitting limit inference. Household sampling excludes institutionalised older adults. Participant usability and performance in another population remain untested.

Survey access conditions and disclosure requirements apply. Interface demonstrations and tests use synthetic records. The downloadable package excludes survey records. Displays and reports omit submitted identifiers and raw income. These controls do not establish disclosure review of every historical repository file. The project records contain no DUT (Durban University of Technology) ethics determination. The paper therefore claims no approval. The app explains measurement choices; it neither decides grants nor ranks named applicants.

## VIII. Conclusion

Historical screened non-receipt was 6.6% unweighted and 7.5% person-weighted; alternatives gave 7.1%–9.1%. Rules about other grants changed results more than the ceiling, and unresolved cases made the denominator central. Five predictor groups/six slopes gave AUC 0.752, AP 0.203 and Brier 0.0578: moderate internal ranking with slightly less probability error. The software reproduces screening, receipt categories and scores for inspection under tested conditions. The study provides a historical benchmark. It does not establish human usability, causes, legal entitlement or performance elsewhere.


## References

[1] T. Raniga and B. Simpson, “Poverty, HIV/AIDS and the old age pension in Bhambayi, KwaZulu-Natal, South Africa,” Dev. South. Afr., vol. 28, no. 1, pp. 75–85, 2011, doi: 10.1080/0376835X.2011.545171.

[2] M. Alloush, J. R. Bloem, and J. G. Malacarne, “Social protection amid a crisis: New evidence from South Africa’s Older Person’s Grant,” World Bank Econ. Rev., vol. 38, no. 2, pp. 371–393, 2024, doi: 10.1093/wber/lhad037.

[3] M. Ralston, E. Schatz, J. Menken, F. X. Gómez-Olivé, and S. Tollman, “Who benefits—or does not—from South Africa’s old age pension? Evidence from characteristics of rural pensioners and non-pensioners,” Int. J. Environ. Res. Public Health, vol. 13, no. 1, Art. 85, 2016, doi: 10.3390/ijerph13010085.

[4] E. B. Godfrey et al., “Which eligible households get grants? Demographic correlates of receipt in South Africa,” Dev. South. Afr., vol. 33, no. 6, pp. 774–789, 2016, doi: 10.1080/0376835X.2016.1231059.

[5] Republic of South Africa, Social Assistance Act 13 of 2004, Government Gazette 26446, Jun. 10, 2004.

[6] A. Case, V. Hosegood, and F. Lund, “The reach and impact of Child Support Grants: Evidence from KwaZulu-Natal,” Dev. South. Afr., vol. 22, no. 4, pp. 467–482, 2005, doi: 10.1080/03768350500322925.

[7] W. Zembe-Mkabile, T. Doherty, D. Sanders, and D. Jackson, “Child Support Grant access and receipt among 12-week-old infants in an urban township setting in South Africa,” Global Health Action, vol. 7, no. 1, Art. 25310, 2014, doi: 10.3402/gha.v7.25310.

[8] C. J. Heinrich and R. Brill, “Stopped in the name of the law: Administrative burden and its implications for cash transfer program effectiveness,” World Dev., vol. 72, pp. 277–295, 2015, doi: 10.1016/j.worlddev.2015.03.015.

[9] A. Gibbs, L. Washington, N. Jama Shai, Y. Sikweyiya, and S. Willan, “Systematically excluded: Young women’s experiences of accessing child support grants in South Africa,” Global Public Health, vol. 13, no. 12, pp. 1820–1830, 2018, doi: 10.1080/17441692.2018.1449231.

[10] T. N. Majola and P. Maharaj, “The challenges associated with the Child Support Grant application process: A case of young mothers in a South African township,” J. Soc. Serv. Res., vol. 51, nos. 5–6, pp. 1140–1150, 2025, doi: 10.1080/01488376.2025.2502004.

[11] J. Gazeaud, “Proxy means testing vulnerability to measurement errors?,” J. Dev. Stud., vol. 56, no. 11, pp. 2113–2133, 2020, doi: 10.1080/00220388.2020.1715942.

[12] M. T. Mabala, “Factors associated with social grant uptake in South Africa: A closer look at the Special COVID-19 Social Relief of Distress Grant among the youth aged 18–35 years,” Master’s research report, University of the Witwatersrand, Johannesburg, South Africa, 2023. Available: https://hdl.handle.net/10539/40003.

[13] D. P. Moynihan, P. Herd, and H. Harvey, “Administrative burden: Learning, psychological, and compliance costs in citizen-state interactions,” J. Public Adm. Res. Theory, vol. 25, no. 1, pp. 43–69, 2015, doi: 10.1093/jopart/muu009.

[14] S. Granlund, “They are not leaving without their money: Exploring encounters with the state through cash transfers in the rural Eastern Cape, South Africa,” South. Afr. J. Soc. Work Soc. Dev., vol. 34, no. 1, Art. 9052, 2022, doi: 10.25159/2708-9355/9052.

[15] A. N. Vujovic, G. M. Jonathan, and S. Hacks, “Digitalisation and its impact on social protection programmes effectiveness: A case from South Africa,” Procedia Comput. Sci., vol. 237, pp. 882–890, 2024, doi: 10.1016/j.procs.2024.05.177.

[16] T. Saito and M. Rehmsmeier, “The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,” PLOS ONE, vol. 10, no. 3, Art. e0118432, 2015, doi: 10.1371/journal.pone.0118432.

[17] B. Van Calster et al., “Calibration: The Achilles heel of predictive analytics,” BMC Med., vol. 17, Art. 230, 2019, doi: 10.1186/s12916-019-1466-7.

[18] R. D. Riley et al., “Minimum sample size for developing a multivariable prediction model: Part II—binary and time-to-event outcomes,” Stat. Med., vol. 38, no. 7, pp. 1276–1296, 2019, doi: 10.1002/sim.7992.

[19] D. R. Roberts et al., “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” Ecography, vol. 40, no. 8, pp. 913–929, 2017, doi: 10.1111/ecog.02881.

[20] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, “Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement,” Ann. Intern. Med., vol. 162, no. 1, pp. 55–63, 2015, doi: 10.7326/M14-0697.

[21] Statistics South Africa, Living Conditions Survey 2014/2015: Metadata, Statistical Release P0310. Pretoria, South Africa, 2017.

[22] Statistics South Africa, Living Conditions Survey: COICOP Codes. LCS 2014/2015 code list.

[23] Statistics South Africa, Living Conditions Survey 2014/2015: Household Questionnaire.

[24] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 211, Government Gazette 37474, Mar. 28, 2014.

[25] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 277, Government Gazette 38647, Mar. 30, 2015.
