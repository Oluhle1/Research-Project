# Reported Non-Receipt of the Older Person’s Grant among Apparently Eligible Adults in KwaZulu-Natal

Oluhle Jawe
ICT Honours (21634436), PRIC401
Durban University of Technology, Durban, South Africa

Abstract—Reported non-receipt of South Africa’s Older Person’s Grant (OPG) was examined among adults aged 60 or older in KwaZulu-Natal using the Living Conditions Survey 2014/2015. Administrative-burden theory motivates candidate predictors while distinguishing observable screening, reported receipt and prediction from legal entitlement. A documented screen identified 1,013 adults with resolved receipt, including 67 non-recipients: 6.6% unweighted and 7.5% person-weighted. Across screening alternatives the weighted rate ranged from 7.1% to 9.1%. A logistic model with five predictor domains and six slopes achieved household-held-out AUC 0.752, average precision 0.203 and Brier score 0.0578, compared with 0.0618 for an intercept-only reference. Correctness and reproducibility evidence includes 22 original synthetic screening cases, 220 automated tests, agreement on all 15,388 reference records, and 50 checks of synthetic report files from a Windows walkthrough. A local Streamlit interface exposes rules, reason codes, frozen scores and audited exports. Participant usability has not been evaluated. Neither the historical screen nor the model establishes statutory eligibility, causes of non-receipt or external validity.

Keywords—Older Person’s Grant, reported non-receipt, administrative burden, Living Conditions Survey, logistic regression, reproducibility.

## I. Introduction

The Older Person’s Grant supports older adults and their households in South Africa. Research in KwaZulu-Natal describes its role in household livelihoods [1], while recent work examines protection during a crisis [2]. Receipt patterns and barriers to accessing grants are separate questions [3], [4]. A transparent survey screen can identify adults who appear to satisfy observable conditions and nevertheless report non-receipt, without establishing their legal entitlement.

This study preserves three research questions. RQ1 asks what proportion of the screened population reports OPG non-receipt and how it changes under alternative eligibility assumptions. RQ2 asks how well a small logistic model distinguishes recipients from non-recipients and estimates probabilities in held-out households. RQ3 asks whether a computational artefact can reproduce the analysis and clearly explain screening decisions and model outputs. The contribution combines a versioned screen, survey-weighted description, internally validated prediction and a local research interface. “Apparently eligible” refers to observable research rules, rather than a South African Social Security Agency decision under the full legal test [5].

## II. Related Work and Conceptual Framework

### A. Grant access and administrative burden

Administrative-burden theory distinguishes learning, compliance and psychological costs in citizen–state interactions [6]. South African grant studies describe documentation, repeated visits, interruptions and difficult encounters with administration [7], [8], [9], [10]. Child Support Grant research in KwaZulu-Natal and elsewhere motivates possible access mechanisms [11], [12]; it does not establish their prevalence or effects among older OPG applicants. Digital access conditions may introduce further constraints [13]. Receiving a grant can coexist with substantial access costs, so a low non-receipt rate does not demonstrate that burden is small.

Four concepts remain distinct. Statutory eligibility is legal entitlement, which LCS cannot fully establish. Observable eligibility is a result of explicit age, resources, partnership and grant-compatibility rules. Reported receipt is a survey answer among screen-passing adults with resolved responses: non-receipt is Y = 1 and receipt Y = 0. A predicted probability estimates that reported outcome from available characteristics. Missing screen information and contradictory receipt answers remain unresolved; they do not become non-receipt events. Conditioning on the screen defines a selected population rather than all older adults or grant applicants.

### B. Translating concepts into predictors and an artefact

Table I connects the five source predictors to the literature. They are limited proxies for circumstances accompanying access. No direction of association is assumed. Schooling does not measure knowledge of OPG; office distance does not record an application journey; sex does not measure discrimination. The data lack application histories, awareness, documents, actual travel expenditure, waiting time, stigma and stress. Associations cannot identify learning, compliance or psychological mechanisms.

TABLE: Table I. Literature-informed predictors and their limits
| Predictor | Conceptual connection | Observable coding and limit |
| --- | --- | --- |
| Age | Demographic receipt patterns [3] | Per decade above 60; no health or application history. |
| Sex | Demographic differences [3], [4] | Female vs male; no social-role or discrimination measure. |
| Schooling | Possible information resources [6], [9] | Below Grade 7 vs higher; no awareness or literacy measure. |
| Settlement | Service and access context [10], [11], [13] | Two contrasts vs urban formal; no office-capacity measure. |
| Office distance | Potential access effort [9], [10] | At least 5 km/unavailable vs nearer; no visits or travel costs. |

The artefact operationalises these distinctions through separate screen statuses, receipt categories and model probabilities. Person-weighted estimates address prevalence in the screened survey population; household-held-out predictions address internal predictive performance. Frozen application scores are a third output. A probability never changes screening or observed receipt. Correctness and reproducibility can be tested computationally; participant usability requires human evidence. At low event prevalence, precision and calibration must accompany ROC area [14], [15]. Sample size and grouped validation constrain interpretation [16], [17]. Prediction-reporting principles from TRIPOD inform transparent reporting rather than a claim of clinical-checklist compliance [18].

## III. Methods

### A. Data and study population

The person, household and person-income files of Statistics South Africa’s LCS 2014/2015 were interpreted using the released metadata, questionnaire and COICOP codes [19], [20], [21]. The frame is sampled KwaZulu-Natal residents aged 60 or older in completed years; the person is the analytical unit. Records were linked using survey person and household keys, with duplicate, unmatched and row-count checks. The household survey does not represent institutionalised older adults. Historical screening uses the interview month, not present-day thresholds.

### B. Final observable rules and receipt outcome

The resource proxy sums nominal annualised person-attributable income, excluding social-assistance codes to avoid making grant receipt itself a resource disqualification. Household totals are not allocated to individuals. A missing income row represents zero only when the released income-source convention supports no listed source; unexplained absence remains unresolved. Asset acquisitions are not an assessable asset stock. The proxy does not observe the complete statutory asset test, deemed income or permitted deductions.

The income ceiling is the private annual resource level at which the grant formula still pays R100 monthly. From the April 2014 maximum it is R61,800 for a single person and R123,600 for a couple; from April 2015 it is R64,680 and R129,360 [22], [23]. The interview-month ceiling applies, and an amount exactly at it passes. These are formula-derived research ceilings, rather than an unqualified assertion that income alone establishes statutory eligibility. Alternative threshold and income definitions are reported separately.

A married adult is screened using combined applicant and spouse resources only when a resident spouse can be linked and relationship checks pass. Never-married, widowed and divorced adults use the single ceiling. Living-together, separated, absent-spouse and unresolvable-link cases remain unresolved in the primary analysis. This conservative choice avoids assuming that unavailable partner resources are zero or that ambiguous partners are single; named sensitivities relax it. An own disability or war-veterans grant fails the primary compatibility rule. Caregiver child grants and grant-in-aid do not exclude an adult or define the OPG outcome. A known failure takes precedence over unresolved items while retaining every reason.

Among adults who pass, the general social-grant and OPG questions are interpreted together with structural skips. A consistent “no grant” response may define non-receipt even when the OPG follow-up is not applicable. Contradictory or unexplained answers leave receipt unresolved and exclude that record from the model. Current reported receipt is compared with preceding-year OPG income; disagreement is flagged without changing the primary outcome, because the periods differ. Rule version opg-kzn-primary-v1 identifies these decisions. A passing screen with resolved receipt is the final denominator.

### C. Survey-weighted description and uncertainty

RQ1 reports both the count proportion and the released person-weighted ratio p = Σ(wᵢYᵢ)/Σwᵢ within the final denominator. Recipient/non-recipient comparisons are descriptive, without causal interpretation. Stratum identifiers were not released. A with-replacement variance approximation clusters on derived primary sampling units (PSUs); it is explicitly not a full survey-design interval. Unresolved screening cases remain a separate excluded group, rather than being imputed into that ratio. Bounds assigning unresolved PASS receipt to each outcome are reported as sensitivity checks.

### D. Predictive specification and internal validation

The primary estimator is unweighted logistic regression without class balancing, stepwise selection or a decision threshold. Age is linear per decade above 60; reference levels are male, Grade 7 or above, urban formal and a welfare office nearer than 5 km. Settlement supplies two slopes, giving six slopes plus an intercept from five source domains. In the attempted seven-slope specification, rural formal settlement had one non-recipient and no training events in the fold that held that person out. Traditional and rural formal settlement were therefore combined in logged decision D-052. This addresses event support and does not assert theoretical equivalence. Marital status defines screening context and is not a primary predictor. Income, receipt and derived outcome labels are excluded from predictor preparation.

Five folds keep all members of a household together, stratifying households by whether any member reports non-receipt, with seed 201415. Predictor imputation uses training-fold statistics after structural skips are interpreted; eligibility and outcomes are never imputed. Each included adult receives one out-of-fold (OOF) probability from a model that did not train on their household. Pooled unweighted metrics are average precision, ROC area, Brier score, calibration-in-the-large and calibration slope. The intercept-only reference predicts each training fold’s event rate. Intervals resample households 1,000 times around fixed OOF predictions without refitting; they omit uncertainty from repeating model development.

### E. Sensitivity programme

S1 varies thresholds, S2 partnership assumptions, S3 grant compatibility, S4 income definition, S5 receipt period and S6 unresolved-receipt bounds. Each scenario records denominator, events, unweighted/person-weighted prevalence and internally validated model performance. S7 uses complete cases; S8 substitutes a married indicator for welfare access; S9 fits using person weights as frequency weights, retaining unweighted fold imputation and unweighted metrics. S9 is not a full survey-design regression. S10 applies person weights to primary OOF metrics without refitting. S11 groups folds by derived PSU. Primary results are preserved separately from sensitivity outputs.

## IV. Computational Artefact and Evaluation

The offline command, python analysis/run_study.py, links the three survey files, applies the screen, computes the weighted description and fits the grouped-validation model. Run records preserve rule/model settings, input/output checksums, software versions, seed and fold assignments. A separate build freezes full-cohort coefficients and fitted preprocessing in a non-executable JSON artifact, opg-kzn-six-slope-v1. This preserves the original scientific pipeline while supplying reusable inference.

The local Streamlit interface has five sections: study context, upload/validation, eligibility/receipt, prediction/model and export/reproducibility. It accepts the normalized historical opg-screen-v1 CSV, retaining household members needed for spouse context. Validation rejects incompatible schema/context, duplicate keys, invalid categories and malformed numeric values, with limits of 20 MiB and 50,000 rows. Uploads use session memory. Generated row labels replace submitted identifiers in displays and reports; raw income and household pointers are omitted. Filters affect inspected/exported subsets while summary proportions retain the full uploaded resolved-pass denominator.

FIGURE: figures/architecture.png | Fig. 1. Research and local-interface paths. The shared screen preserves measurement decisions; held-out evaluation and frozen full-data scoring remain separate.

The app reuses the original rule engine and loads frozen coefficients and preprocessing; uploads never trigger fitting. Only the supported resolved-pass cohort is scored. Partly missing predictors use frozen training statistics; a record with all categorical predictors absent remains unscored. Integrity checks bind model/evaluation files to scientific and feature code. Historical aggregate OOF evaluation is labelled separately from full-data fitted upload scores with unknown training overlap. CSV, JSON and report-ZIP exports include classifications, reasons, supported scores, versions and an audit manifest. The downloadable MVP package uses synthetic data and excludes raw survey files, historical respondent outputs and Git history.

Evaluation examines independently specified synthetic screening cases, forbidden predictors, data linkage and traceability; repeated research outputs; CLI/native-UI record parity; inference serialization; invalid-input and stale-state behaviour; and report bytes/hashes. The project owner’s Windows walkthrough provides local functional evidence. A task protocol for three to five consenting synthetic-data users exists, but no participant study has been conducted, so usability and user acceptance are not claimed.

## V. Results

### A. Cohort and reported non-receipt

The source contains 15,388 people in 3,686 KwaZulu-Natal households. Table II records the final denominator. Among 117 failures, 93 exceed the income ceiling and 25 report an own disability grant, with one overlapping record; no war-veterans grant is reported. Among 187 unresolved adults, 105 are married, mostly with a non-resident spouse, and 63 are recorded as living together. The unresolved group exceeds the non-recipient group.

TABLE: Table II. KwaZulu-Natal cohort flow
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

Reported non-receipt is 67/1,013, or 6.61% unweighted and 7.49% person-weighted. The approximation using 345 derived PSUs has standard error 1.3 percentage points and approximate normal 95% interval 4.9%–10.0%. All 1,013 pass-group answers are resolved and agree with preceding-year OPG income; those checks therefore produce no change. Men comprise 34/67 non-recipients versus 260/946 recipients; Grade 7 or above is recorded for 49/67 versus 290/946. These are sample composition comparisons, not causal effects.

### B. Screening sensitivities

Table III covers all screening assumptions, grouping only scenarios with identical results. Relative to primary, S1b/S1d add two people and two events. S2a, S2b, S2c and S2d add 59/4, 60/2, 8/0 and 68/2 people/events respectively. S3 adds 19 people and 15 events; S4b removes six people without removing events. Weighted prevalence ranges from 7.12% to 9.06%, with grant compatibility producing the largest change. Comparable AUC does not imply unchanged populations or probability error.

TABLE: Table III. Screen sensitivities and OOF performance
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

Primary household-held-out AUC is 0.752 (fixed-prediction household-resample interval 0.69–0.81). Average precision is 0.203 beside prevalence 0.066. Brier score is 0.0578 versus 0.0618 for the intercept-only reference. Calibration-in-the-large is 0.020 (interval −0.32–0.27); slope is 0.836 (0.59–1.13). All five retained folds converge. Figure 2 shows five quantile bins: the highest has mean prediction 0.188 and 35/203 events (17.2%); the lowest has mean prediction 0.0107 and 3/206 events (1.5%). Most adults even in the highest bin report receipt.

FIGURE: figures/calibration.png | Fig. 2. Unweighted OOF calibration from frozen quantile-bin aggregates. Labels give events/people; the diagonal denotes exact calibration. The displayed range is 0–0.22.

The full-cohort fit gives odds ratios 0.39 for women versus men (Wald interval 0.23–0.66) and 0.24 for schooling below Grade 7 versus higher (0.13–0.43). Age, settlement and welfare-distance intervals include 1. These are screened-sample associations from the full-data fit, not cross-validated effects or causes. Table IV distinguishes further model and validation assumptions.

TABLE: Table IV. Model/validation sensitivities
| Scenario | N/events | Unw.% | AUC | Brier | Slope |
| --- | --- | --- | --- | --- | --- |
| S0 primary | 1,013/67 | 6.61 | .752 | .0578 | .836 |
| S7 complete | 992/63 | 6.35 | .758 | .0556 | .819 |
| S8 married | 1,013/67 | 6.61 | .755 | .0578 | .846 |
| S9 wtd. fit | 1,013/67 | 6.61 | .750 | .0583 | .718 |
| S10 wtd. metrics | 1,013/67 | 6.61 | .763 | .0641 | .935 |
| S11 PSU folds | 1,013/67 | 6.61 | .758 | .0575 | .860 |

NOTE: The prevalence column remains unweighted; S8–S11 retain weighted descriptive prevalence 7.49%. S9 uses frequency weights in fitting, with unweighted imputation and held-out metrics. S10 weights existing primary OOF predictions without refitting. S8 replaces welfare access, retaining six slopes. S7 removes 21 people/four events. S11 changes fold grouping, retaining the cohort.

Across screen, model and validation sensitivities AUC ranges from 0.736 to 0.763. Brier scores and calibration slopes vary with event prevalence and evaluation basis. Neither sensitivity analysis nor internal partitioning supplies external validation.

### D. Actual artefact evidence

Table V distinguishes evaluation layers. The original 26 passing checks comprise 22 synthetic screening cases, two income-schedule checks, one forbidden-predictor check and one run-trace check. They are not 26 screening decisions or 26 participant tasks. Income exactly at a ceiling passes and one cent above fails; unavailable spouse resources remain unresolved; caregiver grants do not determine OPG labels. Two research runs produced the same 14 files byte for byte, preserving the frozen cohort checksum.

TABLE: Table V. Completed verification and its scope
| Evidence | Observed result | What it supports |
| --- | --- | --- |
| Original checks | 26/26, including 22 screen cases | Rules, schedules, predictor exclusion and tracing. |
| Complete automated suite | 220 pass; 0 fail/skip | Backend/UI/state/export behaviour; includes 18 native Streamlit tests. |
| Native UI–CLI parity | 15,388/15,388 agree; 1,013 scored | Frame, screen, receipt, reasons and outcome agreement. |
| JSON inference reload | Maximum score difference 5.55 × 10⁻¹⁷ | Full-fit serialization consistency; not OOF performance. |
| Owner Windows exports | 50/50 checks of six files | Synthetic local workflow and report consistency. |
| Participant usability | Not conducted | No representative task-time, error or ease evidence. |

The owner’s Windows walkthrough produced the six intended synthetic classifications, two resolved passes, one recipient and one non-recipient. Both scored records have probability 0.1853 because their predictor values are identical. The example’s 50% rate is invented and does not estimate survey prevalence. Screenshots and six extracted report files were supplied; the ZIP container was not independently inspected. Regenerated data outputs, hashes, summary values, versions and model/source provenance passed 50 checks. This is functional/export evidence, rather than independent execution attestation or representative usability. No recruited-user task results, times, error rates or ease ratings are available.

## VI. Discussion

### A. Denominator and grant access

Reported receipt is the usual outcome within these observable rules, but the result depends on the denominator. The 187 unresolved adults exceed the 67 non-recipients. The estimate describes adults whose resources, partnerships and grant answers can be resolved, rather than everyone who might qualify legally. Partnership assumptions change headcounts more than prevalence because most added adults report receipt. Retaining own disability-grant recipients raises weighted non-receipt more than threshold alternatives. The systematic sensitivities expose these choices instead of presenting one screening definition as certain.

Prior receipt studies show demographic patterns [3], [4]; studies of other grants describe costly application and payment processes [6], [10], [11]. The observed high receipt rate cannot establish that these costs are small, because recipients may also experience them and LCS does not measure the relevant mechanisms. The approximate interval around the weighted rate remains wide and omits strata; uncertainty about unresolved screening is a different limitation from sampling error.

### B. Meaning and limits of prediction

The five domains provide moderate ranking information and a small improvement in probability error. Average precision must be interpreted beside the low event prevalence [14]. AUC alone would overstate how reliably a high score identifies a non-recipient. The slope interval is too wide for a strong claim about probability scaling with 67 events [15], [16]. Full-data odds ratios concentrate information in sex and schooling; the place/access terms are imprecise.

Schooling was a plausible information-resource proxy, yet lower schooling accompanies reported receipt in the screened cohort. It may mark fewer alternative resources after screening, or conditioning on the screen may alter associations. The survey cannot distinguish those explanations. Recorded schooling, distance and settlement do not directly test administrative-burden theory. No fitted coefficient determines legal eligibility or identifies why a person reports non-receipt. Weighting descriptions, weighting a sensitivity fit and weighting existing performance metrics answer different questions; their numerical differences do not demonstrate that one model is superior.

### C. What RQ3 establishes

The CLI and Streamlit interface make classifications, reason codes and probabilities inspectable while preserving provenance. Record-level parity and repeated bytes support correctness and reproducibility. Frozen JSON reload agreement supports application inference, while the OOF evaluation remains the evidence for internal predictive performance. A user-uploaded score can overlap training records and does not create a held-out test. The owner walkthrough confirms the local synthetic upload-to-export flow. It cannot establish participant usability, clarity for nontechnical users or acceptance. RQ3 is supported for reproducibility and computational inspectability; human interpretation remains untested. The documented synthetic-data usability protocol is retained as future work.

### D. External validity

The target is a screened KwaZulu-Natal LCS 2014/2015 population. Provinces differ in settlement, access and administration; later periods differ in policy, thresholds, coverage and reporting. Administrative application, award and payment records measure different events from survey-reported receipt and introduce their own missingness/linkage errors. The historical upload schema restricts supported context, but passing validation does not establish suitability for contemporary applicants. No independent province, period or administrative sample has been evaluated. Transport requires a compatible outcome, justified target-context screening rules and independent discrimination/calibration assessment [17], [18]. Deploying software does not supply that evidence.

## VII. Limitations and Ethics

Legal eligibility is partially observed: the asset test, deemed income and deductions are absent from the resource proxy. Income and reported receipt may contain measurement error. Cross-sectional associations have no established temporal order. The small event count, unresolved denominator, missing strata and fixed-prediction rather than refitted bootstrap limit inference. Household sampling excludes institutionalised older adults. Formal participant usability and external validation remain outstanding.

Survey use remains subject to access conditions and applicable disclosure requirements. Synthetic records support demonstration and interface testing; the downloadable local package excludes survey records. Result displays and report exports omit submitted identifiers and raw income. These controls do not establish that every historical repository file has been disclosure-reviewed. No DUT ethics determination is documented here, so none is claimed. The artefact explains this study’s measurement decisions and does not issue grant decisions or rank named applicants.

## VIII. Conclusion

In the historical KwaZulu-Natal observable screen, reported OPG non-receipt is 6.6% unweighted and 7.5% person-weighted. Alternatives yield weighted rates of 7.1%–9.1%; grant compatibility is more influential than the income ceiling, and unresolved cases make the denominator central. Five predictor domains with six slopes provide moderate internal ranking and only a small probability-error improvement. The artefact reproduces the analysis and exposes screening, receipt and model outputs through a verified local workflow. Participant usability, causal explanations, statutory eligibility and performance in other populations are not established.


## References

[1] T. Raniga and B. Simpson, “Poverty, HIV/AIDS and the old age pension in Bhambayi, KwaZulu-Natal, South Africa,” Dev. South. Afr., vol. 28, no. 1, pp. 75–85, 2011, doi: 10.1080/0376835X.2011.545171.

[2] M. Alloush, J. R. Bloem, and J. G. Malacarne, “Social protection amid a crisis: New evidence from South Africa’s Older Person’s Grant,” World Bank Econ. Rev., vol. 38, no. 2, pp. 371–393, 2024, doi: 10.1093/wber/lhad037.

[3] M. Ralston, E. Schatz, J. Menken, F. X. Gómez-Olivé, and S. Tollman, “Who benefits—or does not—from South Africa’s old age pension? Evidence from characteristics of rural pensioners and non-pensioners,” Int. J. Environ. Res. Public Health, vol. 13, no. 1, Art. 85, 2016, doi: 10.3390/ijerph13010085.

[4] E. B. Godfrey et al., “Which eligible households get grants? Demographic correlates of receipt in South Africa,” Dev. South. Afr., vol. 33, no. 6, pp. 774–789, 2016, doi: 10.1080/0376835X.2016.1231059.

[5] Republic of South Africa, Social Assistance Act 13 of 2004, Government Gazette 26446, Jun. 10, 2004.

[6] D. P. Moynihan, P. Herd, and H. Harvey, “Administrative burden: Learning, psychological, and compliance costs in citizen-state interactions,” J. Public Adm. Res. Theory, vol. 25, no. 1, pp. 43–69, 2015, doi: 10.1093/jopart/muu009.

[7] C. J. Heinrich and R. Brill, “Stopped in the name of the law: Administrative burden and its implications for cash transfer program effectiveness,” World Dev., vol. 72, pp. 277–295, 2015, doi: 10.1016/j.worlddev.2015.03.015.

[8] A. Gibbs, L. Washington, N. Jama Shai, Y. Sikweyiya, and S. Willan, “Systematically excluded: Young women’s experiences of accessing child support grants in South Africa,” Global Public Health, vol. 13, no. 12, pp. 1820–1830, 2018, doi: 10.1080/17441692.2018.1449231.

[9] T. N. Majola and P. Maharaj, “The challenges associated with the Child Support Grant application process: A case of young mothers in a South African township,” J. Soc. Serv. Res., vol. 51, nos. 5–6, pp. 1140–1150, 2025, doi: 10.1080/01488376.2025.2502004.

[10] S. Granlund, “They are not leaving without their money: Exploring encounters with the state through cash transfers in the rural Eastern Cape, South Africa,” South. Afr. J. Soc. Work Soc. Dev., vol. 34, no. 1, Art. 9052, 2022, doi: 10.25159/2708-9355/9052.

[11] A. Case, V. Hosegood, and F. Lund, “The reach and impact of Child Support Grants: Evidence from KwaZulu-Natal,” Dev. South. Afr., vol. 22, no. 4, pp. 467–482, 2005, doi: 10.1080/03768350500322925.

[12] W. Zembe-Mkabile, T. Doherty, D. Sanders, and D. Jackson, “Child Support Grant access and receipt among 12-week-old infants in an urban township setting in South Africa,” Global Health Action, vol. 7, no. 1, Art. 25310, 2014, doi: 10.3402/gha.v7.25310.

[13] A. N. Vujovic, G. M. Jonathan, and S. Hacks, “Digitalisation and its impact on social protection programmes effectiveness: A case from South Africa,” Procedia Comput. Sci., vol. 237, pp. 882–890, 2024, doi: 10.1016/j.procs.2024.05.177.

[14] T. Saito and M. Rehmsmeier, “The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,” PLOS ONE, vol. 10, no. 3, Art. e0118432, 2015, doi: 10.1371/journal.pone.0118432.

[15] B. Van Calster et al., “Calibration: The Achilles heel of predictive analytics,” BMC Med., vol. 17, Art. 230, 2019, doi: 10.1186/s12916-019-1466-7.

[16] R. D. Riley et al., “Minimum sample size for developing a multivariable prediction model: Part II—binary and time-to-event outcomes,” Stat. Med., vol. 38, no. 7, pp. 1276–1296, 2019, doi: 10.1002/sim.7992.

[17] D. R. Roberts et al., “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” Ecography, vol. 40, no. 8, pp. 913–929, 2017, doi: 10.1111/ecog.02881.

[18] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, “Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement,” Ann. Intern. Med., vol. 162, no. 1, pp. 55–63, 2015, doi: 10.7326/M14-0697.

[19] Statistics South Africa, Living Conditions Survey 2014/2015: Metadata, Statistical Release P0310. Pretoria, South Africa, 2017.

[20] Statistics South Africa, Living Conditions Survey: COICOP Codes. LCS 2014/2015 code list.

[21] Statistics South Africa, Living Conditions Survey 2014/2015: Household Questionnaire.

[22] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 211, Government Gazette 37474, Mar. 28, 2014.

[23] Dept. of Social Development, “Increase in respect of social grants,” Government Notice 277, Government Gazette 38647, Mar. 30, 2015.
