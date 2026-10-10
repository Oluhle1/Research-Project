# V. Results

The results below come from rule version `opg-kzn-primary-v1` and the retained six-slope logistic model. Counts and metrics match the frozen cohort and the command `python analysis/run_study.py`.

## A. Cohort

The released files contain 15,388 people in 3,686 KwaZulu-Natal households. None of those people has a missing age. Of the 1,317 adults aged 60 or older, 1,013 pass the observable screen and have a resolved Older Person’s Grant answer. They form the final analysis cohort: 946 report receipt and 67 report non-receipt. A further 117 fail a known rule and 187 remain unresolved. No one who passed the screen has an unresolved grant answer. Table I shows the flow. Household counts are distinct households in each row, so a household can appear in more than one row.

**Table I. Construction of the KwaZulu-Natal analysis cohort**

| Step | People | Households |
| --- | ---: | ---: |
| KwaZulu-Natal respondents | 15,388 | 3,686 |
| Aged 60 or older | 1,317 | 1,068 |
| Failed a known eligibility rule | 117 | 98 |
| Eligibility unresolved | 187 | 168 |
| Passed, with a resolved grant answer | 1,013 | 827 |
| Reported receipt | 946 | 773 |
| Reported non-receipt | 67 | 60 |

Of the 117 failures, 93 are above the income ceiling and 25 report an own disability grant, with one person in both groups. The file contains no reported war-veterans grant. Of the 187 unresolved adults, 105 are married, mostly because the spouse is not in the household, and 63 are recorded as living together. Those partnership groups are outside the final cohort by the primary rule.

## B. Reported non-receipt

Among the 1,013 apparently eligible adults, 67 report non-receipt. The unweighted proportion is 6.6%. Using the released person weights, the proportion is 7.5%. Stratum identifiers were not released. A with-replacement approximation that clusters on the 345 derived primary sampling units in the cohort has a standard error of 1.3 percentage points and a normal 95% interval from 4.9% to 10.0%. That interval is not a full design-based interval. No pass-group outcome is unresolved, and current receipt agrees with preceding-year grant income for all 1,013 people, so those two checks leave the estimate where it stands.

Recipients and non-recipients differ in composition. The comparison is descriptive. Among non-recipients, 34 of 67 are men, compared with 260 of 946 recipients. Schooling of Grade 7 or above is recorded for 49 of 67 non-recipients and 290 of 946 recipients. Urban formal residence is recorded for 38 of 67 non-recipients and 284 of 946 recipients. A welfare office at least 5 km away, or unavailable, is recorded for 34 of 67 non-recipients and 717 of 946 recipients. Mean age is 67.3 years among non-recipients and 70.4 years among recipients. One non-recipient is divorced and one lives in a rural formal area.

## C. Sensitivity of the estimate

Alternative eligibility rules move the unweighted proportion to between 6.4% and 7.9%, and the weighted proportion to between 7.1% and 9.1% (Table II). The largest change is retention of adults who report an own disability grant: the denominator becomes 1,032, non-recipients become 82, and the weighted proportion rises to 9.1%. Using one statutory ceiling for every interview, adding the age-75 supplement, comparing price-adjusted income with the nominal ceilings, and relabelling receipt from earlier grant income each change the primary proportion by at most 0.2 percentage points. Treating adults who live together, or who are separated, as single changes the cohort by up to 68 people. Most of those adults report receipt, so the proportion moves by less than half a percentage point.

**Table II. Non-receipt under the primary screen and the eligibility checks that change it**

| Screen | People | Non-recipients | Unweighted | Weighted |
| --- | ---: | ---: | ---: | ---: |
| Primary | 1,013 | 67 | 6.6% | 7.5% |
| 2015 ceiling applied to every interview | 1,015 | 69 | 6.8% | 7.7% |
| Living together and separated, screened as single | 1,081 | 69 | 6.4% | 7.1% |
| Own disability-grant recipients retained | 1,032 | 82 | 7.9% | 9.1% |

## D. Held-out prediction

Each of the 1,013 adults received a probability from a logistic model fitted without that adult’s household. The model has six slopes. The separate rural-formal contrast in Table I of the proposal was not retained: that category has one non-recipient, and the training fold that held that person out did not converge. Traditional area and rural formal are one contrast in the model that was evaluated.

The out-of-fold ROC area is 0.75, with a household-resample interval of 0.69 to 0.81. Average precision is 0.20, beside a prevalence of 0.066. The Brier score is 0.058, compared with 0.062 when every adult is assigned the training-fold prevalence. Calibration-in-the-large is 0.02. The calibration slope is 0.84, and its resample interval of 0.59 to 1.13 includes 1. These intervals describe the fixed predictions. They do not refit the model.

Fig. 1 shows the five quantile bins. In the highest fifth, the mean predicted probability is 0.19 and 35 of 203 adults report non-receipt (17%). In the lowest fifth, the mean prediction is 0.011 and 3 of 206 adults report non-receipt (1.5%).

**Fig. 1. Out-of-fold calibration.** Observed non-receipt against mean predicted probability in five quantile bins. The diagonal is perfect calibration. Source file: `output/runs/primary/calibration_plot.png`.

On the full cohort, after the same coding, women have lower odds of reported non-receipt than men (odds ratio 0.39, Wald interval 0.23 to 0.66). Adults with schooling below Grade 7 have lower odds than those with Grade 7 or above (odds ratio 0.24, interval 0.13 to 0.43). The intervals for age, settlement, and welfare-office distance include 1. These coefficients are associations in the screened sample. They are not cross-validated effects and they do not identify causes.

Refits that change the cohort or the specification leave the ROC area between 0.74 and 0.76. Retaining disability-grant recipients, the change that most affects the descriptive rate, lowers the ROC area to 0.74 and raises the Brier score to 0.068, alongside the higher event rate. Replacing welfare-office access with a married indicator leaves the Brier score at 0.058. A survey-weighted fit has a held-out ROC area of 0.75 and a calibration slope of 0.72. Grouping folds by sampling unit instead of household gives a ROC area of 0.76. Complete cases, 992 adults and 63 non-recipients, give a ROC area of 0.76.

## E. Artefact checks

The rule engine was compared with 26 decisions stated before the run. All 26 agreed with the program. Income at each statutory ceiling passes, and one cent above it fails. A missing resident spouse stays unresolved and is not moved onto the single-person ceiling. An own disability grant fails the screen. A caregiver child grant does not exclude the adult and does not set the grant label. An unspecified grant answer stays out of the model. The outcome and grant-income amount are rejected as predictors.

Running the study command twice produced the same 14 output files, byte for byte. The cohort checksum equals the checksum frozen before modelling. For the example adult stored in the run record, the status, reason codes, outcome, fold, and held-out probability can be read from the cohort file and the prediction file under rule version `opg-kzn-primary-v1`.
