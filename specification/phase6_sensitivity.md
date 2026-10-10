# Phase 6: sensitivity of the model

**Date:** 2026-09-25  
**Primary result:** the six-slope model in `specification/phase5_rq2.md`.  
**Script:** `analysis/phase6_sensitivity.py`  
The script checks the frozen cohort hash and checks that it reproduces the Phase 5 ROC area of 0.752 before it reports anything else. Sensitivity outputs are written to `output/phase6/`. They do not replace the primary file.

## What stays the same

The primary out-of-fold ROC area is 0.75 and the Brier score is 0.058. Scenarios that select the same 1,013 people leave those figures unchanged: the 2014 ceiling for every interview, the age-75 supplement, CPI-adjusted income against the nominal ceilings, dropping UIF-type income, the receipt-period relabel, and the outcome bounds. The receipt-period and outcome-bound checks have nothing to move, because the primary pass group has no disagreements and no unresolved outcomes.

Where a scenario changes who is included, the change in ROC area or Brier score is read together with the change in the number of people and non-recipients.

## Model metrics

Every refit below used the retained six-slope coding, except S8, which swaps one slope. All five folds converged in every scenario that was fit.

| Scenario | People | Non-recipients | ROC AUC | Average precision | Brier | Calibration slope |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S0 Primary | 1,013 | 67 | 0.752 | 0.203 | 0.058 | 0.836 |
| S1b and S1d Higher ceiling, same two extra people | 1,015 | 69 | 0.763 | 0.211 | 0.058 | 0.875 |
| S2a Living together as a couple | 1,072 | 71 | 0.749 | 0.174 | 0.059 | 0.779 |
| S2b Living together as single | 1,073 | 69 | 0.756 | 0.180 | 0.056 | 0.841 |
| S2c Separated as single | 1,021 | 67 | 0.753 | 0.205 | 0.057 | 0.839 |
| S2d Both of those as single | 1,081 | 69 | 0.751 | 0.183 | 0.056 | 0.808 |
| S3 Disability-grant recipients retained | 1,032 | 82 | 0.736 | 0.224 | 0.068 | 0.864 |
| S4b Social-assistance income kept in the means test | 1,007 | 67 | 0.755 | 0.209 | 0.058 | 0.854 |
| S7 Complete cases | 992 | 63 | 0.758 | 0.211 | 0.056 | 0.819 |
| S8 Married indicator instead of welfare access | 1,013 | 67 | 0.755 | 0.207 | 0.058 | 0.846 |
| S9 Survey-weighted fit, unweighted score of held-out people | 1,013 | 67 | 0.750 | 0.193 | 0.058 | 0.718 |
| S10 Weighted metrics on the primary predictions | 1,013 | 67 | 0.763 | 0.222 | 0.064 | 0.935 |
| S11 Folds grouped by sampling unit | 1,013 | 67 | 0.758 | 0.204 | 0.057 | 0.860 |

S1b and S1d are the same 1,015 people. Their higher ROC area comes with two extra non-recipients.

S3 moves the metrics the most. Retaining adults who report their own disability grant adds 19 people and 15 non-recipients. The ROC area falls from 0.75 to 0.74 and the Brier score rises from 0.058 to 0.068. Part of that Brier change is the higher event rate, 82/1,032 rather than 67/1,013. Average precision rises to 0.224 beside that higher rate. No war-veterans recipient is added.

S7 drops 21 people with a missing schooling class or a missing welfare distance, including 4 non-recipients. The ROC area is 0.76. Predictor missingness is not carrying the primary result.

S8 keeps six slopes and replaces welfare-office access with an indicator for marital code 1 (married). Living-together adults are not in this cohort, so the indicator is married versus not married. The ROC area is 0.755 and the Brier score is unchanged at 0.058. The swap does not improve prediction.

S9 fits the same predictors with `Persns_wgt` as frequency weights. Imputation inside each training fold stays unweighted. Judged on the held-out people without weights, the ROC area is 0.750 and the calibration slope is 0.72, weaker than the primary slope of 0.84. The weighted fit is not adopted.

S10 does not refit the model. It applies person weights to the primary out-of-fold predictions. The weighted ROC area is 0.76 and the weighted Brier score is 0.064, beside the weighted prevalence of 7.5%.

S11 keeps each derived primary sampling unit inside one fold. There are 345 such units in the cohort. The ROC area is 0.758 and the Brier score is 0.057. Grouping by sampling unit instead of household does not change the conclusion.

## Random forest

A random-forest comparison was not run. The specification places that exploratory check after the logistic model, its validation, these sensitivities, and the artefact evaluation. It also asks that any tuning stay inside training folds. With 67 non-recipients, that check can wait until the artefact has been evaluated. The primary model remains the six-slope logistic regression.
