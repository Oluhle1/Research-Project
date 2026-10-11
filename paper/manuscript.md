# Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), APRE402
Durban University of Technology, Durban, South Africa

Abstract—Reported non-receipt of South Africa’s Older Person’s Grant (OPG) was examined among adults aged 60 or older in KwaZulu-Natal using the Living Conditions Survey 2014/2015. Administrative-burden theory motivates candidate predictors while distinguishing observable screening, reported receipt and prediction from legal entitlement. A documented screen identified 1,013 adults with resolved receipt, including 67 non-recipients: 6.6% unweighted and 7.5% person-weighted. Across screening alternatives the weighted rate ranged from 7.1% to 9.1%. A logistic model with five predictor domains and six slopes achieved household-held-out AUC 0.752, average precision 0.203 and Brier score 0.0578, compared with 0.0618 for an intercept-only reference. Correctness and reproducibility evidence includes 22 original synthetic screening cases, 220 automated tests, agreement on all 15,388 reference records, and 50 checks of synthetic report files from a Windows walkthrough. A local Streamlit interface exposes rules, reason codes, frozen scores and audited exports. Participant usability has not been evaluated. Neither the historical screen nor the model establishes statutory eligibility, causes of non-receipt or external validity.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant supports older adults and their households in South Africa. Research in KwaZulu-Natal describes its role in household livelihoods [7], while recent work examines protection during a crisis [8]. Receipt patterns and barriers to accessing grants are separate questions [2], [6]. A transparent survey screen can identify adults who appear to satisfy observable conditions and nevertheless report non-receipt, without establishing their legal entitlement.

Age eligibility, resource eligibility and reported receipt are different states. A person reporting no OPG may have resources above the programme threshold, may not have applied, may await a decision, or may have incomplete survey information [1]. Income, marital circumstances and missing partner resources can therefore change who enters the apparently eligible denominator. The research problem is both substantive and measurement-related: an explicit population definition is needed before either a non-receipt percentage or a prediction can be interpreted.

The aim is to develop and evaluate an interpretable computational artefact for analysing reported OPG non-receipt among apparently eligible older adults in KwaZulu-Natal using LCS 2014/2015. The four objectives are to document the person-level cohort, describe non-receipt using person weights, internally validate a parsimonious probability model, and evaluate the artefact’s correctness, reproducibility and clarity. Three research questions organise the completed study. RQ1 asks what proportion of the screened population reports OPG non-receipt and how it changes under alternative eligibility assumptions. RQ2 asks how well a small logistic model distinguishes recipients from non-recipients and estimates probabilities in held-out households. RQ3 asks whether a computational artefact can reproduce the analysis and clearly explain screening decisions and model outputs. The contribution combines a versioned screen, survey-weighted description, internally validated prediction and a local research interface. “Apparently eligible” refers to observable research rules, rather than a South African Social Security Agency decision under the full legal test [1].

## II. Related Work and Conceptual Framework

### A. Review approach, programme context and research gap

The approved proposal reported a structured review with thematic narrative synthesis. Searches covered Scopus, Dimensions, IEEE Xplore, SABINET/African Journals Online, Google Scholar and Statistics South Africa/DataFirst resources, using social assistance, eligibility, take-up, non-receipt, exclusion and prediction concepts. Its reported selection was 511 records, 136 duplicates removed, 375 title/abstract screenings, 222 exclusions, 153 full-text assessments and 55 retained sources after 98 further exclusions. These are earlier reported counts, not a new search or 55 OPG-specific studies. Programme, setting, unit and outcome guided synthesis; heterogeneous access stages preclude a pooled estimate.

Table I distinguishes evidence by programme and analytical unit. Ralston’s age-eligible rural Agincourt adults [2] and Godfrey’s Msunduzi household proportions [6] differ from a resource-screened provincial person-level cohort. Livelihood/crisis studies explain OPG’s importance [7], [8], while other-grant studies distinguish contact, application, receipt and payment continuity [9], [10], [13].

TABLE: Table I. Evidence scope informing the study
| Study | Programme/unit/outcome | Contribution and transfer limit |
| --- | --- | --- |
| Ralston et al. [2] | Pension; rural older person; receipt | Person-level precedent; age eligibility and Agincourt setting differ from the provincial resource screen. |
| Godfrey et al. [6] | Grants; Msunduzi household; receipt proportions | Local context; household associations cannot be transferred directly to an individual outcome. |
| Case et al. [9]; Zembe-Mkabile et al. [10] | CSG; enquiry/application and infant receipt | Separate access stages; other grant and age groups do not estimate OPG non-receipt. |
| Heinrich and Brill [13]; Gibbs et al. [14]; Majola and Maharaj [15] | CSG; interruption and application experiences | Motivate burden mechanisms; receipt can coexist with costly access. |
| Gazeaud [11] | Proxy targeting; resource measurement | Motivates sensitivity to income assumptions; Tanzania does not establish South African thresholds. |

Gazeaud’s measurement-error analysis motivates examining resource assumptions without quantifying LCS error or defining South African legal eligibility [11]. Mabala’s logistic analysis concerns a different grant and young applicants, illustrating why the population and event must be stated before comparing predictive findings [18]. The research gap is the integration of transparent screening, weighted description, grouped prediction and inspectable software for this historical KwaZulu-Natal cohort. It does not imply that OPG receipt or grant access has never been studied.

### B. Grant access and administrative burden

Administrative-burden theory distinguishes learning, compliance and psychological costs in citizen–state interactions [12]. South African grant studies describe documentation, repeated visits, interruptions and difficult encounters with administration [13]–[16]. Child Support Grant research in KwaZulu-Natal and elsewhere motivates possible access mechanisms [9], [10]; it does not establish their prevalence or effects among older OPG applicants. Digital access conditions may introduce further constraints [17]. Receiving a grant can coexist with substantial access costs, so a low non-receipt rate does not demonstrate that burden is small.

Statutory entitlement, observable eligibility, reported receipt and prediction remain distinct. LCS cannot establish full legal entitlement. The research screen applies observable age, resources, partnership and grant-compatibility rules; among PASS adults with resolved answers, non-receipt is Y = 1 and receipt Y = 0. Prediction concerns that reported outcome. Missing screen information and contradictory receipt answers remain unresolved. The screen therefore selects a population narrower than all older adults or applicants.

### C. Translating concepts into predictors and an artefact

Table II connects five source predictors to access concepts without assuming association directions. These proxies do not record the experience of applying for OPG: schooling does not measure awareness, office distance does not record a journey, and sex does not measure discrimination. Applications, documents, travel expenditure, waiting, stigma and stress remain unmeasured. Constructs motivate proxies; fitted associations cannot identify the proposed burden mechanisms.

FIGURE: figures/conceptual_framework.png | Fig. 1. Conceptual measurement framework. Theory motivates proxy selection; arrows denote measurement and research workflow, rather than estimated causal effects. Legal entitlement is incompletely observed.

TABLE: Table II. Literature-informed predictors and their limits
| Predictor | Conceptual connection | Observable coding and limit |
| --- | --- | --- |
| Age | Demographic receipt patterns [2] | Per decade above 60; no health or application history. |
| Sex | Demographic differences [2], [6] | Female vs male; no social-role or discrimination measure. |
| Schooling | Possible information resources [12], [15] | Below Grade 7 vs higher; no awareness or literacy measure. |
| Settlement | Service and access context [9], [16], [17] | Two contrasts vs urban formal; no office-capacity measure. |
| Office distance | Potential access effort [15], [16] | At least 5 km/unavailable vs nearer; no visits or travel costs. |

Figure 1 places the observable screen before the separate receipt outcome. Administrative-burden concepts motivate predictor selection, while the survey’s lack of mechanism measures limits causal interpretation. The artefact operationalises these distinctions through separate screen statuses, receipt categories and model probabilities. Person-weighted estimates address prevalence in the screened survey population; household-held-out predictions address internal predictive performance. Frozen application scores are a third output. A probability never changes screening or observed receipt. Correctness and reproducibility can be tested computationally; participant usability requires human evidence. At low event prevalence, precision and calibration must accompany ROC area [20], [19]. Sample size and grouped validation constrain interpretation [21], [22]. Prediction-reporting principles from TRIPOD inform transparent reporting rather than a claim of clinical-checklist compliance [23].

## III. Methods

### A. Data and study population

The person, household and person-income files of Statistics South Africa’s LCS 2014/2015 were interpreted using the released metadata, questionnaire and COICOP codes [3]–[5]. The frame is sampled KwaZulu-Natal residents aged 60 or older in completed years; the person is the analytical unit. Records were linked using survey person and household keys, with duplicate, unmatched and row-count checks. The household survey does not represent institutionalised older adults. Historical screening uses the interview month, not present-day thresholds. Age and sex underwent unflagged hot-deck imputation before release; affected records cannot be isolated. This release-level treatment is distinct from subsequent training-fold predictor imputation.

Table III separates measurement roles. Aggregating income items before linkage avoids duplicate person rows. Household/spouse keys supply context rather than predictors. Receipt defines the outcome; weights define description. The upload contract preserves these boundaries: accepting a screening field does not make it a model predictor.

TABLE: Table III. Data operationalisation and leakage boundaries
| Data concept | LCS measurement | Analytical role and restriction |
| --- | --- | --- |
| Person/household keys | Household and person identifiers | Linkage, spouse context and folds; no model or public-report keys. |
| Age/province | Completed years; province code | Age-60+ KZN frame; age also supplies one slope. |
| Partnership | Marital/resident-partner responses; spouse pointer | Resource rule and spouse link; no primary marital slope. |
| Resources | Annualised income items and source schedule | Private-resource proxy; screening only; no household allocation. |
| OPG receipt | General grant/OPG items with skips | Outcome after PASS; receipt/derived labels are not predictors. |
| Other/prior grants | Own grant items; preceding-year OPG income | Compatibility/period checks; not predictors. |
| Schooling/sex/place | Education, sex, settlement, office distance | Primary features; fitted imputation stays within training. |
| Weight/design | Person weight; derived PSU | Description/named sensitivities; no primary model features. |

NOTE: Survey measurements are interpreted using the released metadata, questionnaire and COICOP definitions [3]–[5]. Upload names are normalized representations of these concepts. Screening/outcome fields are not imputed using predictive preprocessing.

### B. Final observable rules and receipt outcome

The resource proxy sums nominal annualised person-attributable income, excluding social-assistance codes to avoid making grant receipt itself a resource disqualification. Household totals are not allocated to individuals. A missing income row represents zero only when the released income-source convention supports no listed source; unexplained absence remains unresolved. Asset acquisitions are not an assessable asset stock. The proxy does not observe the complete statutory asset test, deemed income or permitted deductions.

The income ceiling is the private annual resource level at which the grant formula still pays R100 monthly. From the April 2014 maximum it is R61,800 for a single person and R123,600 for a couple; from April 2015 it is R64,680 and R129,360 [24], [25]. The interview-month ceiling applies, and an amount exactly at it passes. These are formula-derived research ceilings, rather than an unqualified assertion that income alone establishes statutory eligibility. Alternative threshold and income definitions are reported separately.

A married adult is screened using combined applicant and spouse resources only when a resident spouse can be linked and relationship checks pass. Never-married, widowed and divorced adults use the single ceiling. Living-together, separated, absent-spouse and unresolvable-link cases remain unresolved in the primary analysis. This conservative choice avoids assuming that unavailable partner resources are zero or that ambiguous partners are single; named sensitivities relax it. An own disability or war-veterans grant fails the primary compatibility rule. Caregiver child grants and grant-in-aid do not exclude an adult or define the OPG outcome. A known failure takes precedence over unresolved items while retaining every reason.

Among adults who pass, the general social-grant and OPG questions are interpreted together with structural skips. A consistent “no grant” response may define non-receipt even when the OPG follow-up is not applicable. Contradictory or unexplained answers leave receipt unresolved and exclude that record from the model. Current reported receipt is compared with preceding-year OPG income; disagreement is flagged without changing the primary outcome, because the periods differ. Rule version opg-kzn-primary-v1 identifies these decisions. A passing screen with resolved receipt is the final denominator.

### C. Survey-weighted description and uncertainty

RQ1 reports both the count proportion and the released person-weighted ratio p = Σ(wᵢYᵢ)/Σwᵢ within the final denominator. Recipient/non-recipient comparisons are descriptive, without causal interpretation. Stratum identifiers were not released. A with-replacement variance approximation clusters on derived primary sampling units (PSUs); it is explicitly not a full survey-design interval. Unresolved screening cases remain a separate excluded group, rather than being imputed into that ratio. Bounds assigning unresolved PASS receipt to each outcome are reported as sensitivity checks.

### D. Predictive specification and internal validation

The primary estimator is unweighted logistic regression without class balancing, stepwise selection or a decision threshold. Its inspectable terms describe conditional associations within the screened cohort. Age is linear per decade above 60; reference levels are male, Grade 7 or above, urban formal and an office nearer than 5 km. Five domains supply six slopes plus an intercept because settlement contributes two contrasts. In the attempted seven-slope model, rural formal had one non-recipient and no training events in the fold holding that person out. Logged decision D-052 combined traditional and rural formal for event support, without asserting theoretical equivalence. Marital status defines screening; income, receipt, derived labels and marital status are not primary predictors.

Five folds keep all members of a household together, stratifying households by whether any member reports non-receipt, with seed 201415. Predictor imputation uses training-fold statistics after structural skips are interpreted; eligibility and outcomes are never imputed. Each included adult receives one out-of-fold (OOF) probability from a model that did not train on their household. Pooled unweighted metrics are average precision, ROC area, Brier score, calibration-in-the-large and calibration slope. The intercept-only reference predicts each training fold’s event rate. Intervals resample households 1,000 times around fixed OOF predictions without refitting; they omit uncertainty from repeating model development.

### E. Sensitivity programme

S1 varies thresholds, S2 partnership assumptions, S3 grant compatibility, S4 income definition, S5 receipt period and S6 unresolved-receipt bounds. Each scenario records denominator, events, unweighted/person-weighted prevalence and internally validated model performance. S7 uses complete cases; S8 substitutes a married indicator for welfare access; S9 fits using person weights as frequency weights, retaining unweighted fold imputation and unweighted metrics. S9 is not a full survey-design regression. S10 applies person weights to primary OOF metrics without refitting. S11 groups folds by derived PSU. Primary results are preserved separately from sensitivity outputs.

## IV. Computational Artefact and Evaluation

The offline command, python analysis/run_study.py, links the three survey files, applies the screen, computes the weighted description and fits the grouped-validation model. Run records preserve rule/model settings, input/output checksums, software versions, seed and fold assignments. A separate build freezes full-cohort coefficients and fitted preprocessing in a non-executable JSON artifact, opg-kzn-six-slope-v1. This preserves the original scientific pipeline while supplying reusable inference.

The local Streamlit interface has five sections: study context, upload/validation, eligibility/receipt, prediction/model and export/reproducibility. It accepts the normalized historical opg-screen-v1 CSV, retaining household members needed for spouse context. Validation rejects incompatible schema/context, duplicate keys, invalid categories and malformed numeric values, with limits of 20 MiB and 50,000 rows. Uploads use session memory. Generated row labels replace submitted identifiers in displays and reports; raw income and household pointers are omitted. Filters affect inspected/exported subsets while summary proportions retain the full uploaded resolved-pass denominator.

FIGURE: figures/architecture.png | Fig. 2. Research and local-interface paths. The shared screen preserves measurement decisions; held-out evaluation and frozen full-data scoring remain separate.

The app reuses the original rule engine and loads frozen coefficients and preprocessing; uploads never trigger fitting. Only the supported resolved-pass cohort is scored. Partly missing predictors use frozen training statistics; a record with all categorical predictors absent remains unscored. Integrity checks bind model/evaluation files to scientific and feature code. Historical aggregate OOF evaluation is labelled separately from full-data fitted upload scores with unknown training overlap. CSV, JSON and report-ZIP exports include classifications, reasons, supported scores, versions and an audit manifest. The downloadable MVP package uses synthetic data and excludes raw survey files, historical respondent outputs and Git history.

Evaluation examines independently specified synthetic screening cases, forbidden predictors, data linkage and traceability; repeated research outputs; CLI/native-UI record parity; inference serialization; invalid-input and stale-state behaviour; and report bytes/hashes. The project owner’s Windows walkthrough provides local functional evidence. A task protocol for three to five consenting synthetic-data users exists, but no participant study has been conducted, so usability and user acceptance are not claimed.

## V. Results

### A. Cohort and reported non-receipt

The source contains 15,388 people in 3,686 KwaZulu-Natal households. Table IV records the final denominator. Among 117 failures, 93 exceed the income ceiling and 25 report an own disability grant, with one overlapping record; no war-veterans grant is reported. Among 187 unresolved adults, 105 are married, mostly with a non-resident spouse, and 63 are recorded as living together. The unresolved group exceeds the non-recipient group.

TABLE: Table IV. KwaZulu-Natal cohort flow
| Step | People | Households |
| --- | --- | --- |
| KwaZulu-Natal respondents | 15,388 | 3,686 |
| Aged 60 or older | 1,317 | 1,068 |
| Failed observable rule | 117 | 98 |
| Eligibility unresolved | 187 | 168 |
| PASS and resolved receipt | 1,013 | 827 |
| Reported receipt | 946 | 773 |
| Reported non-receipt | 67 | 60 |

NOTE: Household counts are distinct within each row and can overlap between rows.

FIGURE: figures/cohort_flow.png | Fig. 3. Observed person-level cohort construction. FAIL and UNRESOLVED are retained outside the final denominator. All 1,013 PASS records have resolved receipt; the three screening groups are mutually exclusive.

Reported non-receipt is 67/1,013, or 6.61% unweighted and 7.49% person-weighted. The approximation using 345 derived PSUs has standard error 1.3 percentage points and approximate normal 95% interval 4.9%–10.0%. All 1,013 pass-group answers are resolved and agree with preceding-year OPG income; those checks therefore produce no change. Table V compares all five predictor domains before imputation. The descriptive weights change the composition of each receipt group; those percentages are distinct from within-cohort non-receipt prevalence and predictive probabilities.

TABLE: Table V. Characteristics by reported receipt
| Characteristic | Recipients: U; W | Non-recipients: U; W |
| --- | --- | --- |
| Age, mean years | 70.4; 69.8 | 67.3; 68.4 |
| Female | 686 (72.5%); 70.4% | 33 (49.3%); 53.4% |
| Grade 7 or above | 290 (30.7%); 33.0% | 49 (73.1%); 80.8% |
| Urban formal settlement | 284 (30.0%); 36.2% | 38 (56.7%); 66.2% |
| Welfare office ≥5 km/unavailable | 717 (75.8%); 72.0% | 34 (50.7%); 40.3% |

NOTE: Recipients n = 946; non-recipients n = 67. U reports unweighted means, or counts and within-group percentages; W reports person-weighted means/percentages. Denominators retain missing predictors: schooling is unassigned for three recipients; welfare access is missing for 14 recipients/four non-recipients. These pre-imputation summaries are descriptive and have no inferential intervals.

Non-recipients are younger on the unweighted mean, more often men, more educated and more often urban formal residents in this selected cohort. Weighted mean ages are closer than unweighted means.

### B. Screening sensitivities

Table VI covers all screening assumptions, grouping only scenarios with identical results. Relative to primary, S1b/S1d add two people and two events. S2a, S2b, S2c and S2d add 59/4, 60/2, 8/0 and 68/2 people/events respectively. S3 adds 19 people and 15 events; S4b removes six people without removing events. Weighted prevalence ranges from 7.12% to 9.06%.

TABLE: Table VI. Screen sensitivities and OOF performance
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

NOTE: Events are reported non-recipients. Unw./Wtd. are unweighted/person-weighted prevalence; performance is unweighted. S1b: 2015 ceiling throughout; S1d: zero-payout ceiling. S2a: living-together treated as couple; S2b: living-together as single; S2c: separated as single; S2d: both as single. S3: retain own disability/war-veterans grants (no veterans added). S4b: retain social-assistance income.

*No-change scenarios are S1a (2014 ceiling throughout), S1c (age-75 supplement), S4a (CPI income with nominal ceiling), S4c (exclude UIF/similar transfers), S5 (preceding-year receipt) and S6a/S6b (receipt bounds). Each retains the primary denominator, events and metrics; there are no unresolved PASS outcomes to bound.

### C. Held-out prediction and modelling sensitivities

Table VII reports primary held-out performance and fixed-prediction uncertainty. All five retained folds converge. Figure 4 shows quantile calibration: the highest bin has mean prediction 0.188 and 35/203 events (17.2%); the lowest has mean prediction 0.0107 and 3/206 events (1.5%).

TABLE: Table VII. Primary held-out performance and uncertainty
| Metric | Logistic: estimate [95% interval] | Intercept-only: estimate [95% interval] |
| --- | --- | --- |
| ROC area | .752 [.687–.814] | — |
| Average precision | .203 [.139–.292] | — |
| Brier score | .0578 [.0448–.0706] | .0618 [.0467–.0758] |
| Calibration-in-the-large | .020 [−.316–.273] | .0001 [—] |
| Calibration slope | .836 [.591–1.133] | — |

NOTE: Pooled unweighted OOF predictions: 1,013 people, 67 events. Intervals are percentile bounds from 1,000 household resamples of fixed predictions; all reported intervals have zero invalid resamples. Models and imputation are not refitted. The intercept-only reference uses training-fold prevalence. Dashes indicate unavailable metrics/intervals in the frozen output, rather than zero or asserted chance performance.

FIGURE: figures/calibration.png | Fig. 4. Unweighted OOF calibration from frozen quantile-bin aggregates. Labels give events/people; the diagonal denotes exact calibration. The displayed range is 0–0.22.

The full-cohort fit gives odds ratios 0.39 for women versus men (Wald interval 0.23–0.66) and 0.24 for schooling below Grade 7 versus higher (0.13–0.43). Age, settlement and welfare-distance intervals include 1. These are screened-sample associations from the full-data fit, not cross-validated effects or causes. Table VIII distinguishes further model and validation assumptions.

TABLE: Table VIII. Model/validation sensitivities
| Scenario | N/events | Unw.% | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- |
| S0 primary | 1,013/67 | 6.61 | .752 | .0578 | .836 |
| S7 complete | 992/63 | 6.35 | .758 | .0556 | .819 |
| S8 married | 1,013/67 | 6.61 | .755 | .0578 | .846 |
| S9 wtd. fit | 1,013/67 | 6.61 | .750 | .0583 | .718 |
| S10 wtd. metrics | 1,013/67 | 6.61 | .763 | .0641 | .935 |
| S11 PSU folds | 1,013/67 | 6.61 | .758 | .0575 | .860 |

NOTE: The prevalence column remains unweighted; S8–S11 retain weighted descriptive prevalence 7.49%. S9 uses frequency weights in fitting, with unweighted imputation and held-out metrics. S10 weights existing primary OOF predictions without refitting. S8 replaces welfare access, retaining six slopes. S7 removes 21 people/four events. S11 changes fold grouping, retaining the cohort.

Across screen, model and validation sensitivities AUC ranges from 0.736 to 0.763; Brier scores and calibration slopes also vary.

### D. Actual artefact evidence

Table IX separates verification layers. The original 26 checks comprise 22 synthetic screening cases, two income-schedule checks, one forbidden-predictor check and one run trace. Boundary, spouse, grant and receipt cases match their specified decisions. Two research runs produced the same 14 files byte for byte, preserving the frozen cohort checksum.

TABLE: Table IX. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Rules, schedules, predictor exclusion and tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Backend/UI/state/export behaviour; includes 18 native Streamlit tests. |
| Native UI–CLI parity | 15,388/15,388 agree; 1,013 scored | Frame, screen, receipt, reasons and outcome agreement. |
| JSON inference reload | Maximum score difference 5.55 × 10⁻¹⁷ | Full-fit serialization consistency; not OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Synthetic local workflow and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The Windows walkthrough produced six synthetic classifications, two resolved passes, one recipient and one non-recipient. Both scores are 0.1853 because predictors match; the invented 50% rate is not survey prevalence. Screenshots and six extracted report files, rather than the ZIP container, were supplied. Regenerated outputs, hashes, summaries and model/source provenance passed 50 checks. This supports functional/export consistency, not independent execution attestation or representative usability; recruited-user task times, errors and ease ratings are unavailable.

## VI. Discussion

### A. Denominator and grant access

RQ1 estimates reported non-receipt among apparently eligible, screen-PASS adults with resolved receipt in historical KwaZulu-Natal LCS: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. It does not estimate unlawful denial or non-receipt among all legally entitled adults. The 187 unresolved adults exceed the 67 observed events; their exclusion changes the estimand, independently of sampling uncertainty. A stable point estimate under selected alternatives cannot establish what this unresolved group would report.

Screen assumptions differ substantively. S2d adds 68 people but only two events, reducing weighted prevalence to 7.12%; partnership choices change the denominator more than the rate. S3 retains incompatible own-grant recipients, adds 19 people/15 events and raises prevalence to 9.06%, the largest tested shift. Similar AUC cannot establish equivalent populations or validate those screen choices. Ralston’s rural age-eligible person comparison [2] and Godfrey’s household-level grant analysis [6] use different units, programme scopes, screens and geography; their percentages are not directly comparable. The present study complements those receipt analyses with an explicit provincial resource-screen denominator. High receipt also coexists with access costs [12], [16]; it cannot demonstrate low administrative burden.

### B. Meaning and limits of prediction

RQ2 provides four distinct assessments. AUC 0.752 describes pairwise ranking of held-out non-recipients against recipients, rather than classification accuracy. AP 0.203 summarises precision–recall ranking across thresholds relative to 6.61% event prevalence; it is not precision at an operational cutoff [20]. Brier improvement from 0.0618 to 0.0578 is an absolute reduction of approximately 0.0040 in squared probability error, a modest gain. Calibration-in-the-large is a recalibration intercept with the predicted logit as an offset (slope fixed at 1); its ideal value is zero. The estimate 0.020 and interval spanning zero do not establish perfect agreement. Slope 0.836 suggests possibly overly extreme predictions, but its 0.591–1.133 interval includes the ideal value 1 [19]. With 67 events, probability scaling and subgroup associations remain uncertain [21]; most adults even in the highest calibration bin report receipt.

Table II separates theoretical constructs from observed proxies. Schooling motivates a possible learning-cost connection, while distance and settlement motivate compliance-cost hypotheses [12], [16]. Full-fit odds ratios, including the female and lower-schooling associations, describe the screened cohort; they are neither OOF effects nor estimates of burden. Lower schooling accompanies receipt, contrary to a simple information-barrier expectation. Fewer alternative resources among less-educated adults, or selection induced by screening, could explain that direction; neither hypothesis is tested here. Imprecise office/settlement associations cannot establish the presence or absence of compliance costs. Psychological costs have no direct measure. Without awareness, visits, document demands or administrative decisions, the model cannot identify why non-receipt occurs.

Table VIII distinguishes sample, specification and evaluation changes. S7 excludes 21 people/four events (992/63); its lower Brier score concerns a different sample and cannot establish whether imputation is preferable. S8 replaces welfare access with marriage and gives similar performance. S9 uses frequency weights in fitting with unweighted evaluation, not a full survey-design model. S10 instead reweights the same primary OOF predictions, increasing Brier to 0.0641 without retraining. S11 changes fold grouping to derived PSU and gives similar performance. S8–S11 retain 1,013 people/67 events. These comparisons support a transparent internal benchmark; they do not establish model superiority or external validity [22], [23].

### C. What RQ3 establishes

RQ3 has six verification layers: synthetic cases assess specified rule decisions; repeated bytes assess repeatability; UI–CLI agreement assesses software-path parity; JSON reload assesses inference serialization; the owner walkthrough assesses a functional synthetic workflow; participant testing would assess human usability. Table IX supports the first five within their tested conditions. Automated agreement cannot establish independent user ease, acceptance or field performance. Saved rule sources, run records and validation reports expose versions, checksums and tested conditions for inspection.

Synthetic demonstration, schema checks, session-memory uploads and identifier-suppressed audit exports provide demonstrated controls. Historical OOF evaluation remains separate from frozen full-data app predictions; uploaded records may overlap training data. Serialization agreement therefore verifies inference, not new predictive accuracy. RQ3 is supported for computational inspectability; clarity to representative users remains untested, with the synthetic-data task protocol retained for future work.

### D. External validity

The target is a screened KwaZulu-Natal LCS 2014/2015 population. Provinces differ in settlement, access and administration; later periods differ in policy, thresholds, coverage and reporting. Administrative application, award and payment records measure different events from survey-reported receipt and introduce missingness/linkage errors. No independent province, period or administrative sample has been evaluated. Transfer requires comparable population and outcome definitions, justified target-period screening rules, and independent discrimination/calibration assessment [22], [23]. Passing the historical upload schema or deploying software does not establish suitability for contemporary applicants.

## VII. Limitations and Ethics

Legal eligibility is partially observed: the asset test, deemed income and deductions are absent from the resource proxy. Income and reported receipt may contain measurement error. Cross-sectional associations have no established temporal order. The small event count, unresolved denominator, missing strata and fixed-prediction rather than refitted bootstrap limit inference. Household sampling excludes institutionalised older adults. Formal participant usability and external validation remain outstanding.

Survey use remains subject to access conditions and applicable disclosure requirements. Synthetic records support demonstration and interface testing; the downloadable local package excludes survey records. Result displays and report exports omit submitted identifiers and raw income. These controls do not establish that every historical repository file has been disclosure-reviewed. No DUT ethics determination is documented here, so none is claimed. The artefact explains this study’s measurement decisions and does not issue grant decisions or rank named applicants.

## VIII. Conclusion

Historical screened non-receipt is 6.6% unweighted and 7.5% person-weighted; alternatives yield 7.1%–9.1%. Grant compatibility matters more than the ceiling, and unresolved cases make the denominator central. Five domains/six slopes give AUC 0.752, AP 0.203 and Brier 0.0578: moderate internal ranking with a small probability-error improvement. The software reproduces and exposes screening, receipt and scores within tested conditions. The contribution is an inspectable historical research benchmark. Participant usability, causes, legal entitlement and performance elsewhere remain unestablished.
