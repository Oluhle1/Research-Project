# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—I studied South Africa’s Older Person’s Grant (OPG) and reported non-receipt (respondents say they receive no OPG). I used the Living Conditions Survey (LCS) 2014/2015 for adults aged 60 or older in KwaZulu-Natal (KZN). I used administrative-burden theory (learning about services, meeting requirements and dealing with officials can make access difficult) to choose predictors (survey characteristics used to estimate non-receipt). I used screening (checking survey answers against research rules) to identify apparently eligible adults (people who pass those checks). This cannot establish legal entitlement (a right to the grant under all its legal conditions). Among 1,013 adults who pass and give clear receipt answers, 67 report non-receipt: 6.6% unweighted (counting each person equally) and 7.5% person-weighted (allowing for how many people each respondent represents). Alternative screening rules give weighted rates of 7.1%–9.1%. Logistic regression (a model for two outcomes) uses five characteristics. I tested it on households I did not use to build it. AUC (area under the receiver operating characteristic curve; how well the model ranks non-recipients above recipients) is 0.752; average precision (AP; the share of true non-recipients in ranked selections, averaged as more are found) is 0.203. I obtained a Brier score (the average squared gap between predicted chances and recorded outcomes) of 0.0578. Predicting only the non-receipt rate of the group used to build the model gives 0.0618. Checks support reproducibility (repeated runs give the same results). App screens show rules, decisions, scores and reports. I have not tested how easily participants use it. These results do not establish entitlement, explain non-receipt, or show that the model works elsewhere.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant (OPG) supports households [7], including during crises [8]. Other work examines receipt and access barriers [2], [6]. I ask who appears eligible but reports receiving no OPG.

I separate screening, reported receipt (a respondent’s grant answer) and legal entitlement. Passing my screen does not mean approval by the South African Social Security Agency [1]. Non-receipt can reflect high income, no application, a pending decision or incomplete information. I must define who passes before calculating a percentage; missing spouse income can change that group.

My aim is to develop and evaluate an interpretable research tool (software whose rules and results you can inspect) for analysing reported OPG non-receipt among apparently eligible older adults in KwaZulu-Natal using the Living Conditions Survey (LCS) 2014/2015. I set four objectives: document the people included, describe non-receipt using survey weights (how many people each respondent represents), test predictions on excluded households, and check correctness, reproducibility (whether repeated runs produce the same results) and clarity.

Research questions (RQs) guide the study. RQ1 asks what proportion of screened adults reports non-receipt and how that proportion changes under different screening assumptions. RQ2 asks how well logistic regression separates recipients from non-recipients and estimates chances in excluded households. RQ3 asks whether the tool can repeat the analysis and clearly explain screening decisions and model results. I combine documented rules, weighted percentages, tested predictions and a local interface to answer them.

## II. Related Work and How I Chose Predictors

### A. Review approach, programme context and research gap

My proposal reported a structured literature review (a search using specified sources and selection steps). It searched Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst for grant, access, non-receipt and prediction research. It reported 511 records: 136 duplicates removed, 375 titles/abstracts screened, 222 excluded, 153 full texts assessed, 98 further exclusions and 55 retained sources. These are earlier reported counts, not a new search or 55 OPG studies. I compare grants, places, people/households and measured outcomes; they cannot supply one combined percentage.

Table I distinguishes individual receipt [2] from household proportions [6], and my provincial resource screen from both. Other-grant studies separate enquiry, application, receipt and uninterrupted payment [9], [10], [13].

TABLE: Table I. Evidence scope informing the study
| Study | Grant / people studied / measure | Contribution and transfer limit |
| --- | --- | --- |
| Ralston et al. [2] | Pension; rural older person; receipt | Selection by age in rural Agincourt differs from my resource screen. |
| Godfrey et al. [6] | Grants; Msunduzi household; receipt proportions | Local household findings cannot directly explain individual receipt. |
| Case et al. [9]; Zembe-Mkabile et al. [10] | Child Support Grant (CSG); enquiry/application and infant receipt | Separates access steps; cannot estimate OPG non-receipt. |
| Heinrich and Brill [13]; Gibbs et al. [14]; Majola and Maharaj [15] | CSG; interruption and application experiences | Receipt can still require costly effort. |
| Gazeaud [11] | Targeting assistance using survey measures; resources | Supports checking income assumptions; cannot set South African legal limits. |

Gazeaud supports checking income assumptions [11], without quantifying LCS errors or defining South African eligibility. Mabala models another grant for younger applicants [18]; its findings cannot directly predict OPG receipt. My contribution combines an explicit screen, weighted description, testing on excluded households and inspectable software for this historical KwaZulu-Natal group.

### B. Grant access and administrative burden

Administrative-burden theory (an account of the effort and stress involved in accessing services) identifies learning costs (effort to find and understand information), compliance costs (effort to meet requirements) and psychological costs (stress, stigma or loss of dignity) [12]. Grant studies describe paperwork, repeated visits, interrupted payments and difficult encounters [13]–[16]. Child Support Grant research suggests barriers [9], [10], without establishing their effects among older OPG applicants. Digital access can create difficulties [17]. Low non-receipt therefore does not show that access is easy.

LCS does not record every legal condition or application experience. My screen checks age, resources, partnership and other-grant rules. I record PASS (the person meets the research conditions), FAIL (a known condition is not met) or UNRESOLVED (I lack enough information to decide). I then check receipt separately. Only adults who pass with clear receipt answers enter the prediction study. Unclear or contradictory answers stay unresolved.

### C. Connecting access concepts to predictors and the tool

Table II links five predictors to possible barriers. They are proxies (indirect indicators), not direct measures of grant awareness, journeys or discrimination. LCS does not record application paperwork, travel spending, waiting, stigma or stress. Theory guides my choices; the model cannot prove that barriers caused non-receipt.

FIGURE: figures/conceptual_framework.png | Fig. 1. How theory guides the choice of survey measures. Arrows show measurement choices and research steps; they do not show proven causes. The survey does not record every condition of legal entitlement.

TABLE: Table II. Predictors suggested by the literature and their limits
| Predictor | Conceptual connection | Observable coding and limit |
| --- | --- | --- |
| Age | Receipt differs across age groups [2] | Each decade above 60; does not record health or application history. |
| Sex | Receipt differs by sex [2], [6] | Female compared with male; does not measure social roles or discrimination. |
| Schooling | May help people find and understand information [12], [15] | Below Grade 7 compared with Grade 7 or above; does not measure awareness or literacy. |
| Settlement | Where people live may affect service access [9], [16], [17] | Two settlement comparisons with formal urban areas; does not measure office capacity. |
| Office distance | Reaching an office may require effort [15], [16] | At least 5 km/unavailable compared with nearer; does not record visits or travel costs. |

Figure 1 separates screening, receipt and prediction; you can inspect each in the tool. Weighted percentages describe the screened population. Testing on excluded households checks prediction within this survey. The app scores uploads using saved model settings. These scores are separate from test results and never change screening or receipt.

With few non-recipients, I assess precision (the share of selected likely non-recipients who report non-receipt) and calibration (whether predicted chances match observed rates), alongside ranking [20], [19]. The number of people studied and testing on excluded households limit conclusions [21], [22]. I use TRIPOD (guidance for reporting prediction models) to explain my methods and results [23]. Software checks support correctness and repeatability; participant usability (how easily people understand and complete tasks) needs people to try the app.

## III. Methods

### A. Data and study population

I linked the LCS 2014/2015 person, household and person-income files by survey identifiers, checking duplicates, unmatched records and row counts. I used the questionnaire, metadata (information describing the data) and COICOP (Classification of Individual Consumption According to Purpose, grouping items by purpose) codes [3]–[5]. I studied sampled KwaZulu-Natal residents aged 60 or older in completed years. The survey excludes older adults living in institutions. I applied rules for the interview month. Before releasing the data, Statistics South Africa used hot-deck imputation (filling a missing answer with another respondent's answer) for age and sex without marking the affected records. I cannot identify those records. I handle missing model predictors separately.

Table III shows each field's use. I summed income before linking files to avoid duplicating people.

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

NOTE: I use the released documentation [3]–[5]. Filling missing model predictors never changes screening fields or receipt answers.

### B. Final screening rules and receipt outcome

I estimated private resources by summing yearly income amounts at their reported values. I excluded social-assistance income (payments from government support grants) so receiving a grant would not cause a failure. I did not divide household totals among individuals. A missing income record means zero only when the source indicator confirms no reported income; otherwise, I leave it unresolved. Asset purchases do not show total asset holdings. The data cannot establish the full legal asset test, income assigned under legal rules, or permitted deductions.

I set the income ceiling (the largest yearly private-resource amount that passes the research rule) where the grant formula still pays R100 monthly. From April 2014, the ceilings are R61,800 for a single person and R123,600 for a couple; from April 2015, they are R64,680 and R129,360 [24], [25]. I included amounts exactly at the interview-month ceiling. These research limits do not establish legal eligibility. I tested alternative thresholds and income definitions.

For married adults, I combined applicant and spouse resources only when I could link a resident spouse and confirm the relationship. Never-married, widowed and divorced adults use the single ceiling. Living-together, separated, absent-spouse and failed-link cases remain unresolved in the primary analysis. I did not assume that unknown partner resources equal zero or that an ambiguous partnership means single. Alternative analyses relax these choices. An adult's own disability or war-veterans grant causes a failure. Caregiver child grants and grant-in-aid (an extra grant for people who need full-time care) do not exclude the adult or define OPG receipt. A known failure takes priority over missing information; the software retains all reasons.

For adults who pass, I read general-grant and OPG answers together, including structural skips (questions omitted because earlier answers make them inapplicable). A consistent “no grant” answer can establish non-receipt when the OPG follow-up does not apply. Contradictory or unexplained answers remain unresolved, excluding the person from modelling. I compared current receipt with preceding-year OPG income, flagging disagreements without changing the outcome because the periods differ. Rule version opg-kzn-primary-v1 records these decisions. The final denominator (the group used to calculate the proportion) contains adults who pass and have a clear receipt answer.

### C. Survey-weighted description and uncertainty

For RQ1, I calculated both the ordinary count proportion and the person-weighted proportion: p = Σ(wᵢYᵢ)/Σwᵢ. Here, wᵢ is a person's weight, Yᵢ equals 1 for non-receipt and 0 for receipt, and Σ means add across people. Group comparisons describe differences; they do not establish causes.

The released files lack strata (groups defined before sampling). I used derived primary sampling units, or PSUs (estimated groups selected before households in the survey sample), to estimate sampling uncertainty (variation between possible samples). The calculation allows a group to be sampled more than once. This cannot reproduce the complete survey design. Adults with unresolved screening information stay outside the proportion. I also tested receipt bounds (the lowest and highest rates if all unclear PASS receipt answers mean receipt or all mean non-receipt).

### D. How I checked predictions

I used the unweighted logistic model to estimate probability (a chance from zero to one) of reported non-receipt. I did not rebalance recipients and non-recipients, automatically select variables, or choose a cutoff (a probability used to classify records). The model describes associations (differences that occur together in the data) after accounting for its other predictors. Age enters per decade above 60. Comparison categories are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five predictors need six slopes (numbers setting each input's contribution) and an intercept (the model's baseline), because settlement needs two comparisons.

Only one rural-formal adult reported non-receipt in the attempted seven-slope model. The training group (records used to learn the model settings) had no such case in that category when I excluded that person for testing. Decision D-052 combined rural formal with traditional settlement to support estimation, without claiming that these settings are equivalent. Marital status affects screening; income, receipt, derived labels and marital status do not enter the primary model.

I made five folds (groups I took turns excluding when training). I kept households together and balanced the five folds by whether any member reported non-receipt. Seed 201415 (a setting that makes random splits repeatable) fixes this division. After interpreting skipped questions, I filled missing predictors using training-group statistics only. I never filled missing eligibility or outcome information. Each adult receives one out-of-fold, or OOF, probability (a prediction from a model trained without that adult's household).

Precision (non-recipients among selected records) and recall (selected non-recipients among all non-recipients) vary across ranking cutoffs. I assessed average precision (precision averaged across increases in recall), AUC (how often the model ranks a non-recipient above a recipient), and Brier score (average squared probability error). I also checked calibration slope (whether predicted chances vary too much or too little; 1 is ideal) and calibration-in-the-large (the overall correction needed when I fix that slope at 1; zero is ideal). The intercept-only reference model (one without predictors) uses the training group's non-receipt rate. Bootstrap intervals (ranges from drawing repeated samples of the existing records) use 1,000 household samples and fixed OOF predictions. Without refitting, these intervals omit uncertainty from repeating model development.

### E. Testing alternative assumptions

S1 changes thresholds, S2 partnership assumptions, S3 rules about other grants, S4 income definition, S5 receipt period and S6 unresolved-receipt bounds. Each records the denominator, non-recipients, ordinary/person-weighted rates and internally validated model performance. S7 uses complete cases (people with all required predictors present). S8 replaces welfare access with a married indicator. S9 uses frequency weights (treating person weights as repeated-record contributions), keeping unweighted missing-value treatment and evaluation. This is not a full survey-design regression. S10 weights primary OOF measures without refitting. S11 groups validation folds by derived PSU. I keep these results separate from the primary analysis.

## IV. Software and Evaluation

The command python analysis/run_study.py links files, screens adults and calculates results. Run records retain settings, versions, seed, folds and checksums (file fingerprints used to detect changes). I saved coefficients (the model's numerical settings) from a model trained on all included adults in JSON (a text format for named data). Version opg-kzn-six-slope-v1 stores those and missing-value settings, without program code. Uploads never retrain it.

The local Streamlit app (software for building browser-based applications) has five sections: study context, upload/validation, eligibility/receipt, prediction/model and export/reproducibility. It accepts the historical opg-screen-v1 CSV (comma-separated table), including household members needed to check spouse resources. It rejects incorrect schema (required columns and allowed values), study context, duplicate identifiers, categories and numeric values. Limits are 20 MiB (mebibytes, each 1,048,576 bytes) and 50,000 rows. Uploads stay in memory during the current session (your interaction with the running app). Reports show generated row labels and omit submitted identifiers, raw income and household links. You can filter views and exports; summaries still include all uploaded adults who pass with resolved receipt.

FIGURE: figures/architecture.png | Fig. 2. Research and app workflows. Both use the same screening rules. Predictions for held-out households (households excluded from training) remain separate from app scores calculated using the model trained on all included adults.

The app reuses screening rules, coefficients and missing-value settings; uploads never retrain it. It scores only supported adults who pass with resolved receipt. Saved training statistics fill partly missing predictors; records missing every categorical predictor (an input with named groups) remain unscored. Integrity checks link model/evaluation files to the scientific and predictor code. The app separately labels historical OOF evaluation and uploaded scores from the model trained on all included adults; uploaded records may overlap its training data. CSV, JSON and ZIP (compressed file bundle) reports include classifications, reasons, supported probabilities, versions and an audit manifest (a record of settings and file checksums). The downloadable minimum viable product, or MVP (the working prototype), uses invented data and excludes raw survey files, historical respondent outputs and Git version history.

I checked expected screening decisions, excluded predictors, links, repeated runs, reports and saved predictions. I compared the CLI (command-line interface, where you type commands) with the UI (user interface, the app screens), including invalid inputs and outdated results. My Windows walkthrough shows local functionality. A task sheet for three to five consenting people exists, but no participant study has taken place.

## V. Results

### A. Who passed and reported non-receipt?

The survey records 15,388 people in 3,686 KwaZulu-Natal households. Table IV shows my selection. Among 117 failures, 93 exceed the income ceiling and 25 report a disability grant; one meets both conditions. None reports a war-veterans grant. Among 187 unresolved adults, 105 are married, mostly with a non-resident spouse, and 63 report living together. Unresolved adults outnumber non-recipients.

TABLE: Table IV. How I selected the KwaZulu-Natal study group
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

Of these 1,013 adults, 67 report non-receipt: 6.61% without weights and 7.49% with person weights. Using 345 derived PSUs gives a standard error (the estimated sampling variation of the percentage) of 1.3 percentage points. A bell-shaped sampling approximation gives a 95% confidence interval (a range that aims to cover the population percentage in 95% of repeated samples) of 4.9%–10.0%. The missing strata limit this approximation. All 1,013 PASS answers agree with preceding-year OPG income, so those checks change nothing. Table V compares five predictors before filling missing values. Average age and percentages describe each receipt group. Its percentages describe receipt-group composition, not non-receipt rates or predictions.

TABLE: Table V. Characteristics by receipt (U = unweighted; W = person-weighted)
| Characteristic | Recipients: U; W | Non-recipients: U; W |
| --- | --- | --- |
| Age, average years | 70.4; 69.8 | 67.3; 68.4 |
| Female | 686 (72.5%); 70.4% | 33 (49.3%); 53.4% |
| Grade 7 or above | 290 (30.7%); 33.0% | 49 (73.1%); 80.8% |
| Urban formal settlement | 284 (30.0%); 36.2% | 38 (56.7%); 66.2% |
| Welfare office ≥5 km/unavailable | 717 (75.8%); 72.0% | 34 (50.7%); 40.3% |

NOTE: Recipients: 946 people; non-recipients: 67 people. U gives unweighted averages, or counts and percentages within each group. W gives person-weighted averages/percentages. Denominators retain missing predictors: three recipients lack schooling; 14 recipients/four non-recipients lack welfare-access values. These summaries have no uncertainty intervals.

Non-recipients are younger before weighting, more often men, more educated and more often urban formal residents. Weights bring average ages closer.

### B. What changes when I alter screening rules?

Table VI shows sensitivity analyses (repeating the analysis after changing assumptions). Events (adults reporting non-receipt) and N (people included) identify each group. Unw. and Wtd. abbreviate unweighted and person-weighted. Slope means calibration slope in Tables VI and VIII. Compared with S0, S1b/S1d add two people/two events. S2a, S2b, S2c and S2d add 59/4, 60/2, 8/0 and 68/2 people/events. S3 adds 19 people/15 events; S4b removes six people but no events. Weighted non-receipt ranges from 7.12% to 9.06%.

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

### C. How well do held-out predictions work?

All five folds converge (reach a stable fit). Figure 4 uses five similarly sized bins (groups). The highest bin has average prediction 0.188 and 35/203 non-recipients (17.2%); the lowest has average 0.0107 and 3/206 non-recipients (1.5%).

TABLE: Table VII. Primary held-out performance and uncertainty
| Metric | Logistic: estimate [95% interval] | Intercept-only: estimate [95% interval] |
| --- | --- | --- |
| AUC | .752 [.687–.814] | — |
| Average precision | .203 [.139–.292] | — |
| Brier score | .0578 [.0448–.0706] | .0618 [.0467–.0758] |
| Calibration-in-the-large | .020 [−.316–.273] | .0001 [—] |
| Calibration slope | .836 [.591–1.133] | — |

NOTE: I pool unweighted OOF predictions: 1,013 people/67 events. The intervals use percentile bounds (the middle 95% of resampled estimates) from 1,000 household resamples of fixed predictions. All reported intervals have zero invalid resamples. I do not refit models or missing-value settings. The intercept-only reference uses the training group's non-receipt rate. Dashes mean unavailable measures/intervals, rather than zero or chance performance.

FIGURE: figures/calibration.png | Fig. 4. Saved group summaries show unweighted OOF calibration. Labels give events/people; the diagonal shows exact agreement between average predictions and observed rates. Plot range: 0–0.22.

Odds (the chance of non-receipt divided by the chance of receipt) let me compare groups. The odds ratio (one group's odds divided by the other's) for women versus men is 0.39. Its Wald interval (a range calculated from a model term and its standard error) is 0.23–0.66. Schooling below Grade 7 versus Grade 7 or above gives 0.24 (0.13–0.43). I calculated these from the model trained on all included adults. Age, settlement and welfare-distance intervals include 1. These associations do not describe held-out effects or causes.

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

Across alternatives, AUC ranges from 0.736 to 0.763; Brier and calibration slopes also change.

### D. How did I check the app?

The 26 checks in Table IX include 22 synthetic screening cases (invented records with specified expected decisions), two income-schedule checks, one forbidden-predictor check and one run trace. Boundary, spouse, grant and receipt decisions match their specifications. Two research runs produced 14 files with exactly matching contents and kept the study-group checksum.

TABLE: Table IX. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Check rules, schedules, excluded predictors and run tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Check software, app state and exports; includes 18 Streamlit interface tests. |
| App–command agreement | 15,388/15,388 agree; 1,013 scored | Both paths select the same people and give the same decisions, receipt, reasons and outcome. |
| Reloaded model scores | Maximum score difference 5.55 × 10⁻¹⁷ | Reloading preserves saved-model scores; this does not assess OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Check synthetic local use and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The Windows walkthrough gives six synthetic classifications: two resolved passes, one recipient and one non-recipient. Matching predictors give both scores of 0.1853. The invented 50% rate is not the survey non-receipt rate. I provided screenshots and six extracted reports. The checks did not inspect the ZIP container. Regenerated outputs, checksums, summaries and model/source versions pass 50 checks. This checks functions/exports, not independent execution or representative task times, errors or ease.

## VI. Discussion

### A. Whose non-receipt does the study measure?

RQ1 measures non-receipt among historical KwaZulu-Natal adults who pass the screen and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. This does not measure unlawful denial or non-receipt among everyone legally entitled. The 187 unresolved adults outnumber the 67 events. Excluding them changes the population I describe, regardless of sampling uncertainty. Stable estimates cannot reveal their receipt.

S2d adds 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly change the denominator. S3 retains adults with incompatible grants, adds 19 people/15 events and raises non-receipt to 9.06%, the largest tested change. Similar AUC cannot justify rules or establish equivalent populations. Ralston studies rural age-eligible people [2]; Godfrey studies households' grants [6]. Different units, programmes, screens and places prevent direct comparison of their percentages. I add a provincial estimate with an explicit resource screen. High receipt can involve access costs [12], [16]; it cannot prove low burden.

### B. What do the predictions tell you?

RQ2 assesses four properties. AUC 0.752 describes ranking held-out non-recipients above recipients, not classification accuracy. AP 0.203 summarises precision–recall ranking across cutoffs against a 6.61% event rate, not precision at one cutoff [20]. Brier falls from 0.0618 to 0.0578: a modest 0.0040 reduction in squared probability error. To check average bias, I estimate an intercept correction while fixing the calibration slope at 1. The ideal is zero. The estimate 0.020 and interval spanning zero do not prove perfect agreement. Slope 0.836 suggests that predictions may be too extreme, but its 0.591–1.133 interval includes the ideal 1 [19]. 67 events inform these checks [21]. Most adults in even the highest-risk bin report receipt.

Table II separates concepts from measured predictors. Schooling suggests learning costs; distance/settlement suggest compliance costs [12], [16]. These odds ratios describe the screened group, not OOF effects or burden. Lower schooling accompanies receipt, against a simple information-barrier expectation. Fewer other resources or screening selection could explain this; I test neither explanation. Uncertain office/settlement associations neither confirm nor rule out compliance costs. I do not measure psychological costs. Without awareness, visits, document demands or administrative decisions, I cannot explain non-receipt.

Table VIII separates sample, predictor and evaluation changes. S7 removes 21 people/four events (992/63). Its lower Brier concerns a different sample and cannot establish whether filling missing values is better. S8 substitutes marriage for welfare access and performs similarly. S9 weights fitting but not evaluation; it does not model the full survey design. S10 reweights the same primary OOF predictions without retraining, raising Brier to 0.0641. S11 groups folds by derived PSU and also performs similarly. S8–S11 keep 1,013 people/67 events. These checks expose internal assumptions, rather than establish model superiority or reliability elsewhere [22], [23].

### C. What does RQ3 establish?

RQ3 has six evidence layers. Synthetic cases check rule decisions; matching file contents check repeatability; UI–CLI agreement checks software paths; JSON reload checks saved-model predictions. The owner walkthrough checks a synthetic workflow; participant testing would assess human usability. Table IX supports the first five within tested conditions. Automated agreement cannot establish independent user ease, acceptance or field success. Saved sources and run/validation reports expose versions, checksums and test conditions.

I separate historical OOF results from uploaded scores; uploads may overlap training data. Matching saved scores checks reloading, not new predictive accuracy. You can inspect the computations, but representative user clarity remains untested. The task sheet supports future testing.

### D. Could this work elsewhere?

I study screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in settlement, services, policy and reporting. Application, award and payment records measure different events from reported receipt and can contain linking errors. I have tested no independent province, period or administrative sample. Transfer needs comparable populations/outcomes, justified period-specific rules and independent ranking/calibration checks [22], [23]. Making the app available cannot establish suitability for today's applicants.

## VII. Limitations and Ethics

I cannot fully observe legal eligibility: the survey-based resource measure omits assets, deemed income (income the law assigns rather than the survey observes) and deductions. Income and receipt reports may contain errors. Cross-sectional data (answers from one survey period rather than repeated follow-up of the same people) cannot establish the order of events. Few events, unresolved eligibility, missing strata and resampling fixed predictions without refitting limit inference. Household sampling excludes institutionalised older adults. I have not tested participant usability or another population.

Survey access conditions and disclosure requirements (rules that limit sharing respondent information) apply. I demonstrate and test interfaces with synthetic records. The downloadable package excludes survey records. Displays and reports omit submitted identifiers and raw income. These controls do not show disclosure review of every historical repository file. The project records contain no DUT (Durban University of Technology) ethics determination (an institutional decision on the ethics requirements for this study). I therefore claim no approval. The app explains measurement choices; it neither decides grants nor ranks named applicants.

## VIII. Conclusion

I estimate historical screened non-receipt at 6.6% unweighted and 7.5% person-weighted; alternatives give 7.1%–9.1%. Rules about other grants change results more than the ceiling, and unresolved cases make the denominator central. Five predictor groups/six slopes give AUC 0.752, AP 0.203 and Brier 0.0578: moderate internal ranking with slightly less probability error. You can inspect the software's reproduced screen, receipt categories and scores under tested conditions. I provide a historical benchmark (a documented result that later studies can compare with). I have not established human usability, causes, legal entitlement or performance elsewhere.
