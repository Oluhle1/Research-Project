# Supplementary material

Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal

This supplement documents screening alternatives, model-validation sensitivities, descriptive statistics and the recorded literature searches. Tables S1–S4 use retained aggregate outputs; Table S5 reproduces the author’s search record. Full-precision computational results remain in the cited CSV files. No respondent identifiers or new primary estimates are included.

The computational analyses use rule version `opg-kzn-primary-v1` and primary seed 201415. The frozen cohort’s archived CRLF representation has SHA-256 `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`; the equivalent LF workspace representation has SHA-256 `6edcc6e93eda3f0c58243a64ab3281513abc7a5222f2b2f8836d373c98cf4625`. AUC denotes area under the receiver operating characteristic curve; AP, average precision; CITL, calibration-in-the-large; and OOF, out-of-fold prediction. N and events count sampled adults and reported non-recipients. Household counts are distinct within each scenario. Displayed values are rounded.

## Supplementary Table S1. Screening and model sensitivity scenarios

### Panel A. Operational screening rules

Each row changes the stated component of S0 while retaining the remaining research rules. These alternatives test measurement assumptions; they are not complete determinations of statutory entitlement. Changed cohorts were refitted using five household-grouped folds and training-only imputation. Unchanged cohorts reused the primary predictions. All eight changed-cohort screening scenarios converged in five of five folds. Reused rows represent no additional fit. S1b and S1d selected the same additional people, although their rules differ.

| ID | Change relative to S0 | Prediction source |
| --- | --- | --- |
| S0 | Interview-month single/couple ceilings; nominal private-income proxy excludes social assistance; conservative spouse linkage; own disability or war-veterans receipt fails; resolved current OPG receipt defines the outcome. | Primary |
| S1a | Apply R61,800/R123,600 at every interview. | Reused |
| S1b | Apply R64,680/R129,360 at every interview. | Refit |
| S1c | For an applicant aged 75+, add R960 to the single ceiling and double that ceiling for couples (+R1,920). This applicant-age simplification does not model spouse-specific age supplements. | Reused |
| S1d | Use zero-payment single/couple boundaries R64,800/R129,600 before April 2015 and R67,680/R135,360 thereafter; equality fails. S0 instead uses the R1,200 annual minimum-payment boundary. | Refit |
| S2a | Treat living together (marital code 2) as a couple when a resident partner can be linked; retain spouse-link and resource checks. | Refit |
| S2b | Treat living together as single. | Refit |
| S2c | Treat separated adults (marital code 5) as single. | Refit |
| S2d | Treat both living together and separated as single. | Refit |
| S3 | Retain own disability/war-veterans grant recipients. No war-veterans recipient was added in these data. | Refit |
| S4a | Replace nominal annualised income with the released CPI-adjusted values while retaining nominal ceilings. This deliberately mismatches price bases. | Reused |
| S4b | Keep social-assistance income in the resource proxy. | Refit |
| S4c | Also exclude workmen’s compensation, UIF and similar-fund income (COICOP 50333600). | Reused |
| S5 | If current receipt disagrees with preceding-year OPG income, use the income record while retaining the eligibility screen. No such disagreement occurred among PASS adults. | Reused |
| S6a | Assign unresolved receipt after PASS to receipt. No such outcome occurred. | Reused |
| S6b | Assign unresolved receipt after PASS to non-receipt. No such outcome occurred. | Reused |

### Panel B. Cohort size and reported non-receipt

Changes are relative to S0. Unweighted percentages are events divided by N; person-weighted percentages divide the sum of non-recipient weights by the sum of all weights within the scenario’s resolved PASS cohort.

| ID | Households | N | Events | ΔN | Δevents | Unw. % | Person-weighted % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S0 | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S1a | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S1b | 829 | 1,015 | 69 | +2 | +2 | 6.80 | 7.68 |
| S1c | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S1d | 829 | 1,015 | 69 | +2 | +2 | 6.80 | 7.68 |
| S2a | 870 | 1,072 | 71 | +59 | +4 | 6.62 | 7.42 |
| S2b | 871 | 1,073 | 69 | +60 | +2 | 6.43 | 7.17 |
| S2c | 831 | 1,021 | 67 | +8 | 0 | 6.56 | 7.43 |
| S2d | 875 | 1,081 | 69 | +68 | +2 | 6.38 | 7.12 |
| S3 | 840 | 1,032 | 82 | +19 | +15 | 7.95 | 9.06 |
| S4a | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S4b | 822 | 1,007 | 67 | −6 | 0 | 6.65 | 7.55 |
| S4c | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S5 | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S6a | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |
| S6b | 827 | 1,013 | 67 | 0 | 0 | 6.61 | 7.49 |

### Panel C. Scenario-specific held-out performance

Performance is unweighted. Changed cohorts can change case mix, event frequency and fold membership; differences therefore do not isolate a screening rule’s effect on predictive quality. Matching values for unchanged cohorts arise from reusing the primary predictions, not independent replications.

| ID | AUC | AP | Brier | CITL | Calibration slope |
| --- | --- | --- | --- | --- | --- |
| S0 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1a | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1b | 0.763 | 0.211 | 0.0584 | 0.012 | 0.875 |
| S1c | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1d | 0.763 | 0.211 | 0.0584 | 0.012 | 0.875 |
| S2a | 0.749 | 0.174 | 0.0588 | −0.012 | 0.779 |
| S2b | 0.756 | 0.180 | 0.0564 | 0.008 | 0.841 |
| S2c | 0.753 | 0.205 | 0.0571 | 0.002 | 0.839 |
| S2d | 0.751 | 0.183 | 0.0565 | 0.002 | 0.808 |
| S3 | 0.736 | 0.224 | 0.0682 | 0.009 | 0.864 |
| S4a | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S4b | 0.755 | 0.209 | 0.0576 | 0.010 | 0.854 |
| S4c | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S5 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S6a | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S6b | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |

S4a deliberately compares different price bases and is not a preferred means-test specification. S5 found no disagreement between current receipt and preceding-year OPG income among PASS adults. S6a/S6b found no unresolved receipt after PASS; they do not bound the 187 adults whose eligibility remained unresolved. S1c uses applicant age only and retains its stated spouse-age simplification.

Sources: `output/phase4/rq1_sensitivity.csv` supplies scenario counts, rate estimates and changes; `output/phase6/model_sensitivity.csv` supplies household counts, fit/reuse status and performance. The S6 household counts come from the latter file because those cells are blank in the former. `output/phase6/run_record.json` records the S1b/S1d cohort equality. Operational definitions are implemented in `analysis/phase4_rq1.py` and `analysis/phase6_sensitivity.py`; their grouped-fold seed is 201415.

### Model checks S7–S11

These checks change samples, fitting or evaluation rather than screening rules. S7 refits complete cases; S8, S9 and S11 refit the primary cohort. S10 reweights the primary predictions without refitting. S9 uses person weights as frequency weights when fitting, with unweighted imputation and unweighted held-out evaluation; this is not full survey-design regression. S11 retains five folds while grouping by derived primary sampling unit.

| ID | Check | Fit | Households | N | Events | AUC | AP | Brier | CITL | Slope |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S7 | Complete cases for schooling and office distance | Refit | 811 | 992 | 63 | 0.758 | 0.211 | 0.0556 | −0.029 | 0.819 |
| S8 | Married indicator replaces welfare access | Refit | 827 | 1,013 | 67 | 0.755 | 0.207 | 0.0578 | 0.014 | 0.846 |
| S9 | Frequency weights when fitting; unweighted imputation and evaluation | Refit | 827 | 1,013 | 67 | 0.750 | 0.193 | 0.0583 | −0.032 | 0.718 |
| S10 | Person-weighted measures of the primary predictions | Reweighted | 827 | 1,013 | 67 | 0.763 | 0.222 | 0.0641 | 0.078 | 0.935 |
| S11 | Folds grouped by derived primary sampling unit | Refit | 827 | 1,013 | 67 | 0.758 | 0.204 | 0.0575 | 0.003 | 0.860 |

Source: `output/phase6/model_sensitivity.csv`, rows S7–S11. All refitted checks converged in five of five folds. The S10 performance measures are person-weighted; the other rows use unweighted performance.

## Supplementary Table S2. Ridge comparison of settlement coding

Both codings use the same 1,013 adults, 67 events and five primary household-grouped outer folds (seed 201415). The reference is the retained, unpenalised six-slope logistic model. Ridge regression compares the merged six-slope coding with a separate rural-formal contrast requiring seven slopes. The comparison keeps participants and outer folds fixed rather than deleting the sparsely supported category.

Within each outer training set, five inner folds keep households intact and stratify households by whether any member reports non-receipt. Inner seeds equal 201415 plus the outer-fold number. Each inner training fold supplies its own age median, categorical modes and predictor means and population standard deviations. Mode ties select the smallest code. These statistics are applied to that inner validation fold. A zero standard deviation is replaced by one. After tuning, preprocessing is relearned from the complete outer training set before predicting its held-out households. No inner or outer validation observations supply imputation or scaling statistics.

The inverse-penalty grid is C = 0.01, 0.1, 0.3, 1, 3, 10, 30 and 100; smaller C implies stronger shrinkage. The selected value minimises the unweighted mean of the five inner-fold Brier scores. Exact ties select the smallest C. The estimator uses an L2 penalty, an unpenalised intercept, the lbfgs solver and a maximum of 1,000 iterations. Scaling applies to ridge predictors only. The coding decision D-052 stays fixed, so this sensitivity does not remove the outcome information used to combine settlement categories or establish independent validation of that decision.

| Coding | Estimator | AUC | AP | Brier | CITL | Slope | Converged outer folds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Merged settlement, six slopes | Ordinary logistic reference | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 | 5/5 |
| Merged settlement, six slopes | Ridge, inner-fold tuned | 0.756 | 0.205 | 0.0576 | 0.013 | 0.994 | 5/5 |
| Separate rural-formal contrast, seven slopes | Ridge, inner-fold tuned | 0.750 | 0.205 | 0.0577 | 0.010 | 0.978 | 5/5 |

### Outer-fold penalty and convergence record

| Coding | Outer fold | Selected C | Converged | Iterations | Inner folds complete |
| --- | --- | --- | --- | --- | --- |
| merged six slope | 1 | 0.1 | Yes | 8 | Yes |
| merged six slope | 2 | 0.1 | Yes | 8 | Yes |
| merged six slope | 3 | 0.1 | Yes | 8 | Yes |
| merged six slope | 4 | 0.1 | Yes | 8 | Yes |
| merged six slope | 5 | 0.1 | Yes | 8 | Yes |
| separate seven slope | 1 | 0.1 | Yes | 8 | Yes |
| separate seven slope | 2 | 0.1 | Yes | 8 | Yes |
| separate seven slope | 3 | 0.1 | Yes | 8 | Yes |
| separate seven slope | 4 | 0.1 | Yes | 10 | Yes |
| separate seven slope | 5 | 0.1 | Yes | 8 | Yes |

All 400 inner fits and all 10 outer fits converged. The 400 candidate/fold scores and 80 candidate/outer-fold mean scores are retained in `inner_fold_scores.csv` and `inner_grid_scores.csv`, respectively. Every outer fold selected C = 0.1.

Sources: `output/phase5_ridge_settlement/metrics.csv`, `fold_penalties.csv`, `inner_fold_scores.csv`, `inner_grid_scores.csv` and `run_record.json`; implementation: `analysis/phase5_ridge_settlement.py`. The earlier seven-slope maximum-likelihood attempt produced diagnostic AUC 0.739 and calibration slope 0.673, but only four of five folds converged and its unsupported coefficient was approximately −21.88. These failed-attempt summaries are retained in `output/phase5_original_7slope/metrics.csv` and `fold_coefficients.csv`; they do not provide a valid superiority ranking against the converged six-slope reference (AUC 0.752; slope 0.836). Small differences between the ridge codings also do not establish superior generalisable performance from merging.

## Supplementary Table S3. Twenty repeated household-grouped refits

Twenty consecutive seeds, 201415–201434, repeat the five-fold household-grouped validation. Each repetition relearns imputation and refits the six-slope model inside its training folds. Settlement decision D-052 and the predictor specification remain fixed. Every repetition uses the same 1,013 adults and 67 events. Seed 201415 reproduces the primary performance.

The retained record contains all 20 requested repetitions: 100 fits were attempted, 100 converged and none was reported non-convergent. Each adult has one held-out prediction within each repetition. Repetitions share participants; their spread describes sensitivity to the partition, imputation and refitting under the fixed coding. It is not a 95% confidence interval, adds no independent events and does not repeat the outcome-informed coding decision. Predictions from different repetitions must not be stacked as independent observations.

### Panel A. Every repetition

| Seed | AUC | AP | Brier | CITL | Slope | Converged folds |
| --- | --- | --- | --- | --- | --- | --- |
| 201415 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 | 5/5 |
| 201416 | 0.733 | 0.173 | 0.0588 | 0.005 | 0.738 | 5/5 |
| 201417 | 0.763 | 0.229 | 0.0568 | 0.005 | 0.904 | 5/5 |
| 201418 | 0.762 | 0.234 | 0.0571 | −0.001 | 0.858 | 5/5 |
| 201419 | 0.754 | 0.196 | 0.0578 | −0.014 | 0.846 | 5/5 |
| 201420 | 0.749 | 0.226 | 0.0574 | −0.001 | 0.838 | 5/5 |
| 201421 | 0.750 | 0.199 | 0.0581 | −0.013 | 0.817 | 5/5 |
| 201422 | 0.759 | 0.246 | 0.0568 | 0.010 | 0.893 | 5/5 |
| 201423 | 0.754 | 0.214 | 0.0578 | 0.015 | 0.835 | 5/5 |
| 201424 | 0.746 | 0.216 | 0.0582 | 0.003 | 0.814 | 5/5 |
| 201425 | 0.746 | 0.209 | 0.0577 | 0.007 | 0.805 | 5/5 |
| 201426 | 0.752 | 0.199 | 0.0579 | −0.011 | 0.817 | 5/5 |
| 201427 | 0.749 | 0.207 | 0.0579 | −0.002 | 0.805 | 5/5 |
| 201428 | 0.757 | 0.236 | 0.0569 | 0.013 | 0.892 | 5/5 |
| 201429 | 0.758 | 0.207 | 0.0571 | 0.019 | 0.887 | 5/5 |
| 201430 | 0.738 | 0.177 | 0.0585 | −0.002 | 0.758 | 5/5 |
| 201431 | 0.757 | 0.197 | 0.0576 | 0.013 | 0.843 | 5/5 |
| 201432 | 0.755 | 0.220 | 0.0574 | −0.000 | 0.852 | 5/5 |
| 201433 | 0.773 | 0.238 | 0.0565 | −0.004 | 0.943 | 5/5 |
| 201434 | 0.743 | 0.187 | 0.0584 | 0.012 | 0.792 | 5/5 |

### Panel B. Distribution across 20 repetitions

| Measure | Median | Interquartile range | Range |
| --- | --- | --- | --- |
| AUC | 0.753 | 0.748–0.757 | 0.733–0.773 |
| Average precision | 0.208 | 0.199–0.227 | 0.173–0.246 |
| Brier score | 0.0578 | 0.0571–0.0580 | 0.0565–0.0588 |
| Calibration-in-the-large | 0.004 | −0.002–0.012 | −0.014–0.020 |
| Calibration slope | 0.837 | 0.812–0.865 | 0.738–0.943 |

### Panel C. Training-fold coefficient stability

Coefficients are log-odds estimates from the same 100 overlapping training fits. Sign counts and ranges describe stability; they are neither significance tests nor confidence intervals. The manuscript’s odds ratios remain the full-cohort model estimates.

| Coefficient | Negative fits | Positive fits | Median | Range |
| --- | --- | --- | --- | --- |
| Female versus male | 100/100 | 0/100 | −0.93 | −1.30 to −0.61 |
| Schooling below Grade 7 | 100/100 | 0/100 | −1.46 | −1.97 to −1.14 |
| Age per decade above 60 | 99/100 | 1/100 | −0.39 | −0.81 to 0.01 |
| Urban informal versus urban formal | 27/100 | 73/100 | 0.16 | −0.69 to 0.87 |
| Traditional/rural formal versus urban formal | 100/100 | 0/100 | −0.46 | −0.99 to −0.02 |
| Office ≥5 km or unavailable | 97/100 | 3/100 | −0.41 | −0.92 to 0.17 |

Sources: `output/phase5_refit_repeats/repetition_metrics.csv` supplies Panel A; `summary.csv` supplies Panel B; `coefficient_summary.csv` and `fold_coefficients.csv` supply Panel C; `run_record.json` records seeds and fit counters. Implementation: `analysis/phase5_refit_repeats.py`.

## Supplementary Table S4. Descriptive statistics in separate columns

Main-paper Table V presents the descriptive estimates in separate weighted and unweighted columns. This guide documents their interpretation and source.

| Reporting element | Interpretation |
| --- | --- |
| Sample and timing | N is an observed receipt-group sample size, not a weighted population count. Summaries precede model imputation. |
| Unweighted summaries | Age is a mean in completed years. Other entries are counts and within-receipt-group percentages. |
| Person-weighted summaries | Age is a person-weighted mean; other entries are person-weighted percentages. |
| Denominators | Both denominators include missing predictors. Selected categories are displayed; omitted comparison categories remain in their receipt-group denominators. |
| Missing categories | Missing/unassigned schooling and missing office access are shown explicitly. A recorded office-unavailable category differs from missing office access. |
| Interpretation and uncertainty | Percentages describe receipt-group composition, not non-receipt rates, adjusted effects or predictions. No uncertainty intervals were calculated for these summaries. |

Source: `output/phase4/rq1_characteristics.csv` (also retained in `output/runs/primary/rq1_characteristics.csv`).

## Supplementary Table S5. Recorded literature searches and selection flow

The following details reproduce the author’s retained manuscript search record dated 17 August 2026, archived in `paper/manuscript.md` at Git revision `e0b29b9bebb2a573245dc70bf72048da9a7f9b96`. They document the reported procedure; no search was rerun to prepare this supplement. Historical search IDs S1–S7, including S1b, identify searches here and are distinct from the sensitivity-scenario IDs in Table S1.

The author record states that Web of Science could not be authenticated through DUT on the search date and Dimensions was used instead. Recorded relevance criteria covered grant access, exclusion, take-up, targeting or classification of household-survey data; English-language peer-reviewed articles, theses and institutional reports; and a preference for South African evidence. The stated empirical-study window was 2015–2026, with foundational theory exempt. Earlier empirical programme studies are also cited in the manuscript, but the retained record does not identify their exception or additional search route. The year window is therefore reported as a recorded search setting, rather than independently verified compliance for every retained or cited source.

### Panel A. Sources and counts recorded on 17 August 2026

| Historical search ID | Source | Recorded hits | Retained sources |
| --- | --- | --- | --- |
| S1 | Scopus | 43 | 9 |
| S1b | Scopus, widened | 149 | 10 |
| S2 | Scopus, method | 100 | 11 |
| S3 | Dimensions | 36 | 5 |
| S4 | IEEE Xplore | 47 | 0 |
| S5 | SABINET/AJOL | 100 | 9 |
| S6 | Google Scholar | 35 | 11 |
| S7 | DataFirst/Stats SA | 1 | 0 |

The 511 recorded hits include duplicates across searches. Removing the reported 136 duplicates leaves 375 records for screening. The retained counts total 55 distinct literature sources: the author record assigns each retained source once, to its earliest search. S7's zero retained count refers to literature sources, not the LCS dataset used for analysis. Original exports, record identifiers, a complete 55-source extraction register and item-level screening decisions were not supplied with this record. The allocation of individual sources to searches and the duplicate-removal decisions therefore cannot be independently reproduced from these totals. Recorded hits are historical author-reported counts, not current database result totals.

### Panel B. Queries reproduced verbatim from the retained record

### Recorded query S1 — Scopus

TITLE-ABS-KEY(("social grant*" OR "social assistance" OR "cash transfer*" OR "social protection") AND (exclusion OR "non-take-up" OR "take-up" OR "coverage gap*" OR "targeting error*" OR "access barrier*") AND ("South Africa*" OR "KwaZulu-Natal"))

### Recorded query S1b — Scopus, widened

TITLE-ABS-KEY(("social grant*" OR "social assistance" OR "cash transfer*" OR "social protection" OR "social security" OR SASSA OR "child support grant" OR "social relief of distress" OR SRD) AND (exclusion OR exclud* OR "non-take-up" OR "take-up" OR uptake OR "coverage gap*" OR "targeting error*" OR "access barrier*" OR "non-receipt" OR eligib*) AND ("South Africa*" OR "KwaZulu-Natal"))

### Recorded query S2 — Scopus, method

TITLE-ABS-KEY(("machine learning" OR "random forest" OR XGBoost OR "gradient boosting" OR "proxy means test*" OR "predictive model*") AND (poverty OR "social protection" OR "social assistance" OR "cash transfer*" OR "food insecur*") AND ("household survey" OR "survey data" OR "household data")) AND NOT TITLE-ABS-KEY(cancer OR tumour OR HIV OR malaria OR clinical OR patient*)

### Recorded query S3 — Dimensions

("social grant" OR "social assistance" OR "cash transfer" OR "social protection") AND (exclusion OR "take-up" OR "non-receipt" OR "access barriers") AND ("South Africa" OR "KwaZulu-Natal")

### Recorded query S4 — IEEE Xplore

("machine learning" OR "classification") AND ("poverty" OR "social welfare" OR "socioeconomic") AND ("survey data")

### Recorded query S5 — SABINET/AJOL

social grant AND exclusion AND (KwaZulu-Natal OR "South Africa")

### Recorded query S6 — Google Scholar

"social grant" exclusion "South Africa" -site:pinterest.com

### Recorded query S7 — DataFirst/Stats SA

Living Conditions Survey 2014/2015 metadata KwaZulu-Natal

### Panel C. Reported aggregate selection flow

| Stage | Records |
| --- | --- |
| Identified by the eight recorded searches | 511 |
| Duplicates removed | 136 |
| Remaining for title/abstract screening | 375 |
| Excluded at title/abstract screening | 222 |
| Assessed at full text | 153 |
| Excluded at full text | 98 |
| Retained in the broader social-grant review | 55 |

The arithmetic is consistent: 511 − 136 = 375; 375 − 222 = 153; and 153 − 98 = 55. These are reported aggregate counts, not an independently rerun selection audit. The 55 sources span several grants and populations; they are not 55 OPG-specific empirical studies. The synthesis compares programme, setting, unit of analysis, outcome definition, findings and limitations. Heterogeneous populations and access stages prevent a pooled OPG non-receipt estimate. The retained query record improves transparency without establishing exhaustive coverage or record-level reproducibility.
