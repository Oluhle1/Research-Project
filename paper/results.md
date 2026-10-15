# V. Results

The primary results use rule version `opg-kzn-primary-v1` and the retained six-slope logistic model. Cohort counts, held-out metrics and intervals come from the complete frozen run in `output/runs/primary/`. Descriptive sensitivities are in `output/phase4/rq1_sensitivity.csv`; predictive sensitivities are in `output/phase6/model_sensitivity.csv`. Survey-weighted description, unweighted predictive validation and local application scoring are reported separately.

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

Among the 1,013 apparently eligible adults, 67 report non-receipt. The unweighted proportion is 6.6%. Using the released person weights, the proportion is 7.5%. Stratum identifiers were not released. A with-replacement approximation that clusters on the 345 derived primary sampling units in the cohort has a standard error of 1.3 percentage points and a normal 95% interval from 4.9% to 10.0%. That interval is not a full design-based interval. This descriptive calculation uses the released person weights; the primary logistic fit and its performance metrics below are unweighted. No pass-group outcome is unresolved, and current receipt agrees with preceding-year grant income for all 1,013 people, so those two checks leave the estimate where it stands.

Recipients and non-recipients differ in composition. The comparison is descriptive. Among non-recipients, 34 of 67 are men, compared with 260 of 946 recipients. Schooling of Grade 7 or above is recorded for 49 of 67 non-recipients and 290 of 946 recipients. Urban formal residence is recorded for 38 of 67 non-recipients and 284 of 946 recipients. A welfare office at least 5 km away, or unavailable, is recorded for 34 of 67 non-recipients and 717 of 946 recipients. Mean age is 67.3 years among non-recipients and 70.4 years among recipients. One non-recipient is divorced and one lives in a rural formal area.

## C. Sensitivity of the denominator and prediction

Table II reports every screen or outcome scenario, grouping scenarios only when their cohort, outcome and metrics are identical. Events are reported non-recipients. The denominator ranges from 1,007 to 1,081 people, the unweighted event rate from 6.38% to 7.95%, and the person-weighted descriptive rate from 7.12% to 9.06%. Predictive metrics in this table use unweighted household-grouped out-of-fold probabilities. Changes to the cohort can change event mix and validation partitions, so a lower Brier score across rows does not itself establish a better model.

**Table II. Screen/outcome sensitivities: denominator, event prevalence and held-out performance**

| Scenario | People | Events | Unweighted rate | Weighted rate | AUC | Brier | Slope |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S0: primary | 1,013 | 67 | 6.61% | 7.49% | 0.752 | 0.0578 | 0.836 |
| S1b, S1d: higher ceilings | 1,015 | 69 | 6.80% | 7.68% | 0.763 | 0.0584 | 0.875 |
| S2a: living together as couple | 1,072 | 71 | 6.62% | 7.42% | 0.749 | 0.0588 | 0.779 |
| S2b: living together as single | 1,073 | 69 | 6.43% | 7.17% | 0.756 | 0.0564 | 0.841 |
| S2c: separated as single | 1,021 | 67 | 6.56% | 7.43% | 0.753 | 0.0571 | 0.839 |
| S2d: both groups as single | 1,081 | 69 | 6.38% | 7.12% | 0.751 | 0.0565 | 0.808 |
| S3: own incompatible grants retained | 1,032 | 82 | 7.95% | 9.06% | 0.736 | 0.0682 | 0.864 |
| S4b: social assistance kept in income | 1,007 | 67 | 6.65% | 7.55% | 0.755 | 0.0576 | 0.854 |
| S1a, S1c, S4a, S4c, S5, S6a, S6b: unchanged | 1,013 | 67 | 6.61% | 7.49% | 0.752 | 0.0578 | 0.836 |

S1a applies the 2014 income ceiling to every interview; S1b applies the 2015 ceiling; S1c adds the named age-75 supplement simplification; and S1d uses the income point at which the payment formula reaches zero, excluding income at that point. S2a requires a linkable resident partner; S2b–S2d instead apply single-person ceilings to the specified partnership groups. S3 removes the own disability/war-veterans exclusion; no war-veterans grant is observed in these data. S4a compares CPI-adjusted income with nominal ceilings, S4b retains social-assistance income, and S4c additionally removes compensation/UIF-type funds. S5 uses preceding-year OPG income to resolve receipt-period disagreement; there are no such disagreements in the primary pass group. S6a and S6b assign unresolved PASS outcomes to receipt or non-receipt; there are no such outcomes. The last row therefore reports observed null changes, rather than missing analyses.

The largest change is S3: 19 additional people include 15 additional events, raising the weighted rate by 1.57 percentage points and the Brier score by 0.0105. S2d adds 68 people but only two events, reducing the weighted rate by 0.37 points. S1b/S1d add two events and two people; their weighted change is 0.19 points. Each reported predictive refit converged in all five folds.

## D. Held-out prediction

Each of the 1,013 adults received a probability from a logistic model fitted without that adult’s household. The model has six slopes. The separate rural-formal contrast in Table I of the proposal was not retained: that category has one non-recipient, and the training fold that held that person out did not converge. Traditional area and rural formal are one contrast in the model that was evaluated.

The out-of-fold ROC area is 0.75, with a household-resample interval of 0.69 to 0.81. Average precision is 0.20, beside a prevalence of 0.066. The Brier score is 0.058, compared with 0.062 when every adult is assigned the training-fold prevalence. Calibration-in-the-large is 0.02. The calibration slope is 0.84, and its resample interval of 0.59 to 1.13 includes 1. These intervals describe the fixed predictions. They do not refit the model.

Fig. 1 shows the five quantile bins. In the highest fifth, the mean predicted probability is 0.19 and 35 of 203 adults report non-receipt (17%). In the lowest fifth, the mean prediction is 0.011 and 3 of 206 adults report non-receipt (1.5%).

**Fig. 1. Out-of-fold calibration.** Observed non-receipt against mean predicted probability in five quantile bins. The diagonal is perfect calibration. Source file: `output/runs/primary/calibration_plot.png`.

On the full cohort, after the same coding, women have lower odds of reported non-receipt than men (odds ratio 0.39, Wald interval 0.23 to 0.66). Adults with schooling below Grade 7 have lower odds than those with Grade 7 or above (odds ratio 0.24, interval 0.13 to 0.43). The intervals for age, settlement, and welfare-office distance include 1. These coefficients are associations in the screened sample. They are not cross-validated effects and they do not identify causes.

Table III separates modelling and validation assumptions from the screening scenarios. All metrics are unweighted except S10, which applies person weights to the existing primary out-of-fold predictions and does not refit the model. S9 fits a binomial model using released person weights as frequency weights, retains unweighted training-fold imputation, and evaluates unweighted held-out people. It is a sensitivity fit, not a full survey-design regression. The event-rate column remains the observed unweighted cohort prevalence for all rows; S8–S11 retain the primary 7.49% weighted descriptive prevalence.

**Table III. Modelling/validation sensitivities**

| Scenario | People | Events | Unweighted rate | AUC | Brier | Slope |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S7: complete cases | 992 | 63 | 6.35% | 0.758 | 0.0556 | 0.819 |
| S8: married replaces welfare access | 1,013 | 67 | 6.61% | 0.755 | 0.0578 | 0.846 |
| S9: person-weighted fit | 1,013 | 67 | 6.61% | 0.750 | 0.0583 | 0.718 |
| S10: person-weighted metrics, no refit | 1,013 | 67 | 6.61% | 0.763 | 0.0641 | 0.935 |
| S11: PSU-grouped folds | 1,013 | 67 | 6.61% | 0.758 | 0.0575 | 0.860 |

Complete-case analysis removes 21 people and four events. Changing grouping from household to derived sampling unit leaves the primary cohort intact. Across the screen, model and validation sensitivities, AUC remains between 0.736 and 0.763; Brier scores and calibration slopes vary with population and evaluation basis. No sensitivity establishes external validity.

## E. Artefact checks

The original evaluation log contains 26 passing checks: 22 synthetic screening cases, two income-schedule checks, one structural forbidden-predictor check and one run-trace check. These are not 26 screening decisions. Income at each statutory ceiling passes, and one cent above it fails. A missing resident spouse stays unresolved and is not moved onto the single-person ceiling. An own disability grant fails the screen. A caregiver child grant does not exclude the adult and does not set the grant label. An unspecified grant answer stays out of the model. The structural check rejects outcome and OPG-income columns as predictors; it does not alone establish that all possible leakage has been eliminated.

Running the study command twice produced the same 14 output files, byte for byte. The cohort checksum equals the checksum frozen before modelling. For the example adult stored in the run record, the status, reason codes, outcome, fold, and held-out probability can be read from the cohort file and the prediction file under rule version `opg-kzn-primary-v1`.

The implemented Streamlit research interface adds validated CSV upload, inspectable classifications and reason codes, a frozen model display and report downloads. All 15,388 native-UI reference-upload records agreed with the CLI on frame membership, screening, receipt, reasons and outcome; the 1,013 supported records were scored. Reloaded frozen full-cohort scores differed from the corresponding full-cohort reference fit by at most 5.55 × 10^-17. This score comparison establishes serialization/inference consistency, not held-out predictive performance.

The expanded automated suite passed 220 tests with no failures or skips, including 18 native Streamlit tests. A separate local Windows walkthrough by the project owner produced the six intended synthetic classifications, two resolved passes, one recipient, one non-recipient and two scored records. Verification of the six supplied report files passed all 50 checks: output hashes, summary agreement, versions, source/model provenance and regenerated synthetic outputs. The two synthetic probabilities were both 0.1853; their identical predictor values explain the equality. The displayed 50% non-receipt is an invented two-person example and is not a study estimate.

The owner supplied screenshots and extracted report files, rather than the downloaded ZIP container. This evidence supports local workflow completion and export consistency. It is not independent execution attestation or a representative participant-usability study. No task times, error rates or ease ratings from recruited users are available; the documented synthetic-data usability protocol remains unperformed. The application uses generated row labels and omits original identifiers and raw income from displays and reports. Uploads are processed in session memory. Uploaded probabilities use a frozen full-data fit and are explicitly separated from the historical out-of-fold evaluation; the application does not fit a new model on uploaded data.
