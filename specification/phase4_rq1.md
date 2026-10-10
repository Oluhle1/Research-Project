# Phase 4: RQ1

**Date:** 2026-09-25  
**Frozen cohort:** `output/phase3/cohort_person.csv`, rule version `opg-kzn-primary-v1`  
**Script:** `analysis/phase4_rq1.py`  
The script checks the frozen file’s SHA-256 before it reads it. It does not edit that file and it does not fit a model.

## Answer to RQ1

Under the primary screen, 67 of 1,013 apparently eligible adults report OPG non-receipt. That is 6.6% unweighted. The person-weighted estimate, using `Persns_wgt`, is 7.5%.

A further 187 adults aged 60 or older are unresolved, and 117 fail a known rule. They are not in the 1,013. Nobody who passed the screen had an unresolved OPG answer, so assigning those unresolved outcomes to receipt or to non-receipt does not move the estimate. Current receipt and preceding-year OPG income also agree for all 1,013, so that comparison does not move it either.

The eligibility alternatives change the unweighted estimate to between 6.4% and 7.9%, and the weighted estimate to between 7.1% and 9.1%. The largest change comes from retaining adults who report their own disability grant. Threshold, price, and receipt-period alternatives change the estimate by at most 0.2 percentage points.

Strata were not released. The interval below is a with-replacement approximation that clusters on the 345 derived primary sampling units in the final cohort. It is not a full design-based interval. On that approximation the weighted estimate has a standard error of 1.3 percentage points, and a normal 95% interval runs from 4.9% to 10.0%.

## Primary estimate

| Estimate | Numerator | Denominator | Value |
| --- | ---: | ---: | ---: |
| Unweighted | 67 | 1,013 | 0.0661 |
| Weighted | 67 | 1,013 | 0.0749 |
| PSU-clustered 95% interval | 67 | 1,013 | 0.0495 to 0.1003 |
| Outcome bound, unresolved assigned to receipt | 67 | 1,013 | 0.0661 unweighted; 0.0749 weighted |
| Outcome bound, unresolved assigned to non-receipt | 67 | 1,013 | 0.0661 unweighted; 0.0749 weighted |

No final-cohort person has private income exactly equal to the ceiling, so the inclusive boundary and a strict less-than boundary select the same people.

Recipients are 946 people in 773 households. Non-recipients are 67 people in 60 households.

## Who is outside the denominator

| Status | Married | Living together | Never married | Widowed | Separated | Divorced | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pass | 352 | 0 | 202 | 454 | 0 | 5 | 1,013 |
| Unresolved | 105 | 63 | 4 | 6 | 8 | 1 | 187 |
| Fail | 59 | 2 | 13 | 36 | 1 | 6 | 117 |

The unresolved married adults are mostly people whose spouse is not in the household. Living-together and separated adults are unresolved by the primary partnership rule.

## Description of recipients and non-recipients

These are unweighted counts and weighted shares inside each group. They are not effects, and they do not say why someone did not receive the grant. Non-recipients are 67 people, so a level with one or two people is a description of those people rather than a stable group share. One divorced non-recipient has a large person weight, which is why the weighted divorced share among non-recipients is 6.8% from a count of 1. One non-recipient lives in a rural formal area.

| Characteristic | Recipients (946) | Non-recipients (67) |
| --- | --- | --- |
| Mean age, unweighted | 70.4 years | 67.3 years |
| Mean age, weighted | 69.8 years | 68.4 years |
| Aged 60–69 | 509 (53.8%; weighted 56.4%) | 45 (67.2%; weighted 55.3%) |
| Aged 70–74 | 167 (17.7%; weighted 18.3%) | 12 (17.9%; weighted 28.6%) |
| Aged 75 or older | 270 (28.5%; weighted 25.3%) | 10 (14.9%; weighted 16.1%) |
| Female | 686 (72.5%; weighted 70.4%) | 33 (49.3%; weighted 53.4%) |
| Male | 260 (27.5%; weighted 29.6%) | 34 (50.7%; weighted 46.6%) |
| Below Grade 7 | 653 (69.0%; weighted 66.6%) | 18 (26.9%; weighted 19.2%) |
| Grade 7 or above | 290 (30.7%; weighted 33.0%) | 49 (73.1%; weighted 80.8%) |
| Schooling not assigned | 3 | 0 |
| Traditional area | 575 (60.8%; weighted 53.6%) | 22 (32.8%; weighted 26.8%) |
| Urban formal | 284 (30.0%; weighted 36.2%) | 38 (56.7%; weighted 66.2%) |
| Urban informal | 57 (6.0%; weighted 6.7%) | 6 (9.0%; weighted 6.7%) |
| Rural formal | 30 (3.2%; weighted 3.6%) | 1 (1.5%; weighted 0.4%) |
| Welfare office at least 5 km or unavailable | 717 (75.8%; weighted 72.0%) | 34 (50.7%; weighted 40.3%) |
| Welfare office nearer than 5 km | 215 (22.7%; weighted 26.2%) | 29 (43.3%; weighted 52.6%) |
| Welfare distance missing | 14 | 4 |
| Widowed | 429 (45.3%; weighted 44.8%) | 25 (37.3%; weighted 36.3%) |
| Married | 321 (33.9%; weighted 36.7%) | 31 (46.3%; weighted 47.0%) |
| Never married | 192 (20.3%; weighted 17.8%) | 10 (14.9%; weighted 9.9%) |
| Divorced | 4 (0.4%; weighted 0.7%) | 1 (1.5%; weighted 6.8%) |

Marital status is a screening variable. It is not a predictor in the primary model. Living-together and separated adults do not appear here because the primary screen leaves them unresolved.

## Eligibility sensitivities

Each row re-screens the same linked records. The primary file is unchanged. Change is in percentage points from the primary rate.

| Scenario | Cohort | Recipients | Non-recipients | Unweighted | Weighted | Unweighted change | Weighted change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S0 Primary | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S1a 2014 ceiling for every interview | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S1b 2015 ceiling for every interview | 1,015 | 946 | 69 | 6.80% | 7.68% | +0.18 | +0.19 |
| S1c Age-75 supplement added to the ceiling | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S1d Ceiling where the formula pays nothing | 1,015 | 946 | 69 | 6.80% | 7.68% | +0.18 | +0.19 |
| S2a Living together screened as a couple | 1,072 | 1,001 | 71 | 6.62% | 7.42% | +0.01 | −0.07 |
| S2b Living together screened as single | 1,073 | 1,004 | 69 | 6.43% | 7.17% | −0.18 | −0.31 |
| S2c Separated screened as single | 1,021 | 954 | 67 | 6.56% | 7.43% | −0.05 | −0.06 |
| S2d Living together and separated screened as single | 1,081 | 1,012 | 69 | 6.38% | 7.12% | −0.23 | −0.37 |
| S3 Disability and war-veterans recipients retained | 1,032 | 950 | 82 | 7.95% | 9.06% | +1.33 | +1.57 |
| S4a CPI-adjusted income, nominal ceilings | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S4b Social-assistance income kept in the proxy | 1,007 | 940 | 67 | 6.65% | 7.55% | +0.04 | +0.06 |
| S4c UIF and similar funds also excluded | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S5 Income record used where it disagrees with current receipt | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S6a Unresolved outcomes assigned to receipt | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |
| S6b Unresolved outcomes assigned to non-receipt | 1,013 | 946 | 67 | 6.61% | 7.49% | 0 | 0 |

S1a does not remove anyone: no person who passes under the later ceiling would fail the earlier one. S1b and S1d add the same two non-recipients. S1c adds nobody.

S2a brings in 59 living-together adults who can be linked to a resident partner, 4 of them non-recipients. S2b brings in 60 on the single ceiling, 2 of them non-recipients. S2c brings in 8 separated adults, all recipients. The rate moves less than the cohort size because most of the added adults report receipt.

S3 retains 19 adults who had been excluded only by an own disability grant. Fifteen of them report OPG non-receipt. That is why this row moves the rate more than the others. No war-veterans recipient is added, because the file has none.

S4b removes 6 recipients whose proxy crosses the ceiling once social-assistance income is counted. The non-recipient count stays 67. S4a and S4c change no screen. S5 finds 0 disagreements. S6 has 0 unresolved outcomes among people who passed.
