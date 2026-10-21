# Supplementary tables for the supervisor solutions

These tables accompany the eight-page manuscript. They answer the seven proposed solutions in `Jawe_OPG_Feedback_Proposed_Solutions.docx`. Counts and performance for S0–S11 come from `output/phase4/rq1_sensitivity.csv` and `output/phase6/model_sensitivity.csv`. The ridge comparison is in `output/phase5_ridge_settlement/`. The repeated refits are in `output/phase5_refit_repeats/`. Rule version `opg-kzn-primary-v1` and the six-slope model use seed 201415. The frozen cohort SHA-256 is `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`.

## Supplementary Table S1. Every screening scenario

Changed cohorts were refitted with household-grouped folds and training-only imputation. Unchanged cohorts reused the primary predictions. Identical results do not make different rules equivalent. S1b and S1d admitted the same two adults. No PASS adult had an unresolved receipt outcome for S5 or S6 to change. Every refitted scenario converged in five of five folds. Reused rows keep the primary predictions.

| ID | Rule relative to the primary screen | Fit | Households | N | Events | Unw.% | Wtd.% | AUC | AP | Brier | CITL | Slope |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S0 | Interview-month ceilings; private-income proxy excludes social assistance; conservative spouse link; own disability or war-veterans receipt fails | Primary | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1a | Apply R61,800/R123,600 at every interview | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1b | Apply R64,680/R129,360 at every interview | Refit | 829 | 1,015 | 69 | 6.80 | 7.68 | 0.763 | 0.211 | 0.0584 | 0.012 | 0.875 |
| S1c | For an applicant aged 75 or older, add R960 to the single ceiling. The couple ceiling is twice that single ceiling. This is an applicant-age simplification, not a spouse-specific age rule | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S1d | Zero-payment boundary, where equality fails. S0 uses the R1,200 annual minimum-payment boundary | Refit | 829 | 1,015 | 69 | 6.80 | 7.68 | 0.763 | 0.211 | 0.0584 | 0.012 | 0.875 |
| S2a | Screen living together as a couple when a resident partner can be linked | Refit | 870 | 1,072 | 71 | 6.62 | 7.42 | 0.749 | 0.174 | 0.0588 | −0.012 | 0.779 |
| S2b | Screen living together as single | Refit | 871 | 1,073 | 69 | 6.43 | 7.17 | 0.756 | 0.180 | 0.0564 | 0.008 | 0.841 |
| S2c | Screen separated adults as single | Refit | 831 | 1,021 | 67 | 6.56 | 7.43 | 0.753 | 0.205 | 0.0571 | 0.002 | 0.839 |
| S2d | Screen both living together and separated as single | Refit | 875 | 1,081 | 69 | 6.38 | 7.12 | 0.751 | 0.183 | 0.0565 | 0.002 | 0.808 |
| S3 | Retain own disability or war-veterans grant recipients. No war-veterans recipient was added | Refit | 840 | 1,032 | 82 | 7.95 | 9.06 | 0.736 | 0.224 | 0.0682 | 0.009 | 0.864 |
| S4a | Compare CPI-adjusted income with nominal ceilings. The price bases differ | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S4b | Keep social-assistance income in the resource proxy | Refit | 822 | 1,007 | 67 | 6.65 | 7.55 | 0.755 | 0.209 | 0.0576 | 0.010 | 0.854 |
| S4c | Also exclude workmen’s compensation, UIF and similar-fund income | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S5 | Where current receipt and preceding-year OPG income disagree, use the income record. No disagreement occurred | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S6a | Assign unresolved PASS receipt to receipt. No such case occurred | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |
| S6b | Assign unresolved PASS receipt to non-receipt. No such case occurred | Reused | 827 | 1,013 | 67 | 6.61 | 7.49 | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 |

S4a is a price-base mismatch diagnostic, not a preferred means test. S6a and S6b do not bound the 187 adults whose eligibility stayed unresolved.

## Model checks, S7–S11

These are not screening rules. S8, S9 and S11 were refitted on the primary cohort. S7 was refitted on complete cases. S10 reweights the primary predictions and is not a new fit. Changed cohorts can also change fold membership, so their performance does not isolate one rule.

| ID | Check | Fit | Households | N | Events | AUC | AP | Brier | CITL | Slope |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S7 | Complete cases for schooling and office distance | Refit | 811 | 992 | 63 | 0.758 | 0.211 | 0.0556 | −0.029 | 0.819 |
| S8 | Married indicator replaces welfare access | Refit | 827 | 1,013 | 67 | 0.755 | 0.207 | 0.0578 | 0.014 | 0.846 |
| S9 | Frequency weights when fitting; unweighted imputation and evaluation | Refit | 827 | 1,013 | 67 | 0.750 | 0.193 | 0.0583 | −0.032 | 0.718 |
| S10 | Person-weighted measures of the primary predictions | Reweighted | 827 | 1,013 | 67 | 0.763 | 0.222 | 0.0641 | 0.078 | 0.935 |
| S11 | Folds grouped by derived primary sampling unit | Refit | 827 | 1,013 | 67 | 0.758 | 0.204 | 0.0575 | 0.003 | 0.860 |

## Supplementary Table S2. Ridge settlement comparison

Both codings use the same 1,013 adults, the primary household folds, and training-only imputation. Predictors were standardised inside each training set for the ridge fits only. The penalty grid was C = 0.01, 0.1, 0.3, 1, 3, 10, 30 and 100. Each outer training set chose the C with the lowest mean Brier score on five inner household folds. Every outer fold selected C = 0.1, so the two ridge rows use the same penalty. All ten outer fits converged. The ordinary row is the retained maximum-likelihood model. The small differences do not show that merging improved generalisable performance, and they do not remove the outcome information used in Decision D-052.

| Coding | Estimator | AUC | AP | Brier | CITL | Slope | Converged folds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Merged settlement, six slopes | Ordinary logistic, reference | 0.752 | 0.203 | 0.0578 | 0.020 | 0.836 | 5/5 |
| Merged settlement, six slopes | Ridge, C = 0.1 | 0.756 | 0.205 | 0.0576 | 0.013 | 0.994 | 5/5 |
| Separate rural-formal contrast, seven slopes | Ridge, C = 0.1 | 0.750 | 0.205 | 0.0577 | 0.010 | 0.978 | 5/5 |

The earlier seven-slope maximum-likelihood fit remains diagnostic only: four of five folds converged, and the unsupported coefficient was about −21.88.

## Supplementary Table S3. Twenty repeated refits

Seeds 201415–201434 were fixed before the results were examined. Seed 201415 reproduces the primary AUC of 0.752 and Brier score of 0.0578. Each repetition makes a new household-grouped partition, imputes from its training folds, and refits the six-slope model. Decision D-052 stays fixed. All 100 fits converged. The repetitions share the same adults, so the spread is not a 95% confidence interval and the predictions must not be stacked as independent people.

| Measure | Median | Interquartile range | Range |
| --- | ---: | --- | --- |
| AUC | 0.753 | 0.748–0.757 | 0.733–0.773 |
| Average precision | 0.208 | 0.199–0.227 | 0.173–0.246 |
| Brier score | 0.0578 | 0.0571–0.0580 | 0.0565–0.0588 |
| Calibration-in-the-large | 0.004 | −0.002–0.012 | −0.014–0.020 |
| Calibration slope | 0.837 | 0.812–0.865 | 0.738–0.943 |

Training-fold coefficients on the log-odds scale, across the same 100 fits. A negative count is not a significance test. These overlapping fits do not create additional events.

| Coefficient | Negative fits | Median | Range |
| --- | ---: | ---: | --- |
| Female versus male | 100/100 | −0.93 | −1.30 to −0.61 |
| Schooling below Grade 7 | 100/100 | −1.46 | −1.97 to −1.14 |
| Age per decade above 60 | 99/100 | −0.39 | −0.81 to 0.01 |
| Traditional or rural formal versus urban formal | 100/100 | −0.46 | −0.99 to −0.02 |
| Urban informal versus urban formal | 27/100 | 0.16 | −0.69 to 0.87 |
| Office at least 5 km or unavailable | 97/100 | −0.41 | −0.92 to 0.17 |

The sex and schooling directions were stable. The urban-informal contrast changed sign. The manuscript odds ratios remain the full-sample estimates, not these fold-level ranges.

## Supplementary Table S4. Table V in separate columns

The values are the manuscript Table V summaries. N is the observed sample size, not a weighted population count. Except for age, unweighted entries are counts and percentages, and weighted entries are percentages. Missing predictors remain in the denominators. No uncertainty intervals are available for these descriptions.

| Characteristic | Recipients, unweighted | Recipients, weighted | Non-recipients, unweighted | Non-recipients, weighted |
| --- | --- | --- | --- | --- |
| Age, mean years | 70.4 | 69.8 | 67.3 | 68.4 |
| Female | 686 (72.5%) | 70.4% | 33 (49.3%) | 53.4% |
| Grade 7 or above | 290 (30.7%) | 33.0% | 49 (73.1%) | 80.8% |
| Schooling missing | 3 (0.3%) | 0.4% | 0 (0.0%) | 0.0% |
| Urban formal settlement | 284 (30.0%) | 36.2% | 38 (56.7%) | 66.2% |
| Welfare office at least 5 km or unavailable | 717 (75.8%) | 72.0% | 34 (50.7%) | 40.3% |
| Welfare-office access missing | 14 (1.5%) | 1.8% | 4 (6.0%) | 7.2% |

## Future-research statement

The conclusion states the two future studies. Neither has been done. Geographical validation means applying the frozen KwaZulu-Natal model to an independently held-out province with comparable measurements, before updating it. Temporal validation means a later dataset with documented period-specific thresholds. A usability study would recruit consenting intended users, use synthetic data, and record task success, errors, completion time and perceived ease. Testing by the owner does not replace that study.

## Bibliographic and formatting record

Checked against the files in this revision:

- Published references run from [1] to [28] in order of first use.
- Reference [26] names Government Notice R211 and pages 4–5, distinct from rate notice Government Notice 211 in reference [24]. The 2015 amendment, Government Notice R621, identifies the 2014 instrument as Government Notice R211.
- Reference [21], the metadata report, prints 2017 and ISBN 978-0-621-45185-6. Both are in the reference.
- The supplied COICOP list, published as [22], and the household questionnaire, published as [23], do not print a publication year. No year was added.
- The exported manuscript is eight US Letter pages. Body type is 10 point, tables are 9 point, and references are 8 point. The builder defines one Heading 1 style and one Heading 2 style.

Not completed in this revision: publisher-page checks of the journal DOI strings, and a fresh comparison of thesis reference [12] with its repository landing page. Those checks remain open. No DOI or thesis field was changed without that comparison.
