# Phase 5: RQ2

**Date:** 2026-09-25  
**Cohort:** frozen final cohort, 1,013 people, 67 non-recipients, 827 households.  
**Script:** `analysis/phase5_model.py`  
The script checks the Phase 3 hash before it reads the file. It does not edit that file.

## Answer to RQ2

On held-out households, the logistic model ranks non-recipients above a chance ranking and improves probability error by a small amount over predicting the same risk for everyone.

The out-of-fold area under the ROC curve is 0.75. A 95% household-resample interval for that fixed set of predictions is 0.69 to 0.81. Average precision is 0.20, beside a non-receipt prevalence of 0.066. The Brier score is 0.058, compared with 0.062 for an intercept-only prediction from the same folds. Calibration-in-the-large is 0.02, and the household-resample interval (−0.32 to 0.27) includes zero. The calibration slope is 0.84, with an interval of 0.59 to 1.13.

In the highest fifth of predicted probability, the mean prediction is 0.19 and the observed non-receipt rate is 0.17 (35 of 203 people). In the lowest fifth the mean prediction is 0.011 and the observed rate is 0.015 (3 of 206). The plot is `output/phase5/calibration_plot.png`.

These figures describe prediction inside the screened sample. They do not explain why a person did not receive the grant. No classification threshold is used.

## Why the model has six slopes

Table I specified seven slopes, including a separate rural-formal settlement contrast. That category contains 30 people and one non-recipient. In the training fold that held that person out, every remaining rural-formal adult was a recipient, the rural-formal coefficient ran to about −22, and that fold did not converge. The unrevised outputs are in `output/phase5/table_i_attempt/`.

The retained model merges traditional area and rural formal into one contrast. Urban formal stays the reference, and urban informal stays separate. The other Table I terms are unchanged. All five folds of the retained model converged. No household appears in more than one fold. Each fold contains both outcome classes (12 to 14 non-recipients).

## Coding fixed before the fit

| Term | Coding | Reference |
| --- | --- | --- |
| Age | `(age − 60) / 10` | — |
| Sex | Female indicator | Male |
| Schooling | Below Grade 7 | Grade 7 or above |
| Settlement | Urban informal; traditional or rural formal | Urban formal |
| Welfare-office access | At least 5 km or unavailable | Nearer than 5 km |

Six households contain both a recipient and a non-recipient. Fold assignment keeps every household together and stratifies households by whether any member is a non-recipient. The seed is 201415.

Three people have a schooling code that cannot be placed against Grade 7, and 18 have a missing welfare distance. Within each training fold those codes are filled with the training mode. A tie uses the smallest code sorted as text. Age, sex, and settlement have no missing values in this cohort. The outcome and the eligibility fields are not imputed. The income proxy and the grant items are not predictors. Variance-inflation factors for the six slopes are between 1.0 and 1.8.

There are 11.2 events per slope. Using Riley and colleagues’ shrinkage formula with an anticipated Cox–Snell R² of 0.05 and a target shrinkage of 0.9 gives a sample size of about 1,050, close to the 1,013 people in the cohort. That calculation informed the feasibility note. It was not used to drop a term.

## Apparent associations

The coefficients below are from one fit on the whole cohort, after filling the missing predictor codes with the cohort mode. They are associations, not cross-validated performance and not effects.

| Term | Coefficient | Odds ratio | Wald 95% interval for the odds ratio |
| --- | ---: | ---: | --- |
| Age, per 10 years above 60 | −0.38 | 0.68 | 0.46 to 1.02 |
| Female, versus male | −0.93 | 0.39 | 0.23 to 0.66 |
| Below Grade 7, versus Grade 7 or above | −1.45 | 0.24 | 0.13 to 0.43 |
| Urban informal, versus urban formal | 0.17 | 1.19 | 0.45 to 3.17 |
| Traditional or rural formal, versus urban formal | −0.47 | 0.62 | 0.32 to 1.22 |
| Welfare office at least 5 km or unavailable, versus nearer | −0.43 | 0.65 | 0.35 to 1.20 |

Female sex and schooling below Grade 7 have the clearest associations with lower odds of reported non-receipt. The settlement and welfare intervals are wide.

## Out-of-fold metrics

| Metric | Logistic model | Intercept-only |
| --- | ---: | ---: |
| Prevalence | 0.066 | 0.066 |
| Average precision | 0.203 | — |
| ROC AUC | 0.752 | — |
| Brier score | 0.058 | 0.062 |
| Calibration-in-the-large | 0.020 | 0.000 |
| Calibration slope | 0.836 | — |

The intercept-only row uses the training-fold prevalence as the prediction. Its ROC area and average precision are not used as a comparison, because a constant prediction does not rank people.

Household resampling of these fixed predictions, 1,000 draws, produced no invalid resamples.

| Metric | 2.5 percentile | 97.5 percentile |
| --- | ---: | ---: |
| ROC AUC | 0.687 | 0.814 |
| Average precision | 0.139 | 0.292 |
| Brier score | 0.045 | 0.071 |
| Intercept-only Brier score | 0.047 | 0.076 |
| Calibration-in-the-large | −0.316 | 0.273 |
| Calibration slope | 0.591 | 1.133 |

The intervals describe uncertainty in this fixed set of predictions. They do not include the extra uncertainty from fitting the model again inside each resample.

Weighted versions of the same out-of-fold predictions, using `Persns_wgt`, are a separate summary: prevalence 0.075, average precision 0.222, ROC AUC 0.763, Brier score 0.064, calibration-in-the-large 0.078, calibration slope 0.935. They are not a survey-weighted model fit.
