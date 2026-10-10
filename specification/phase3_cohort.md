# Phase 3 cohort

**Rule version:** `opg-kzn-primary-v1`  
**Date:** 2026-09-25  
**Script:** `analysis/phase3_build_cohort.py`  
**Frozen file:** `output/phase3/cohort_person.csv`  
**SHA-256:** `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`  
A second run of the same script reproduced this hash. No model was fit.

The file contains every KwaZulu-Natal person. People under 60 are marked out of frame. The age-60 group is screened. Household counts below are distinct household identifiers in that row. They are not a partition: 914 households contain both someone under 60 and someone aged 60 or older, so the household columns do not add to 3,686.

## Flow

| Step | People | Households |
| --- | --- | --- |
| KZN sample | 15,388 | 3,686 |
| Age missing | 0 | 0 |
| Age under 60 | 14,071 | 3,532 |
| Age 60+ | 1,317 | 1,068 |
| Eligibility FAIL | 117 | 98 |
| Eligibility UNRESOLVED | 187 | 168 |
| Eligibility PASS | 1,013 | 827 |
| Outcome unresolved | 0 | 0 |
| Recipients (Y = 0) | 946 | 773 |
| Non-recipients (Y = 1) | 67 | 60 |
| Final analysis cohort | 1,013 | 827 |

These are cohort counts. The weighted non-receipt proportion is Phase 4.

## Thresholds

Annexure A of the social-assistance regulations sets the annual grant at D = 1.6A − 0.4B, and no grant below R100 a month is payable. B at the ceiling is the private income at which D is still exactly R1,200 a year. Income at that ceiling passes. Income above it fails.

| Interview month | Grant maximum used as A | Single ceiling | Couple ceiling | People aged 60+ |
| --- | --- | --- | --- | --- |
| October 2014–March 2015 | R1,350 a month, from GN 211, GG 37474, 1 April 2014 | R61,800 | R123,600 | 699 |
| April 2015–October 2015 | R1,410 a month, from GN 277, GG 38647, 1 April 2015 | R64,680 | R129,360 | 618 |

The October 2014 adjustment applied to the child support grant and grant-in-aid, not to the older person’s grant. The couple ceiling is twice the single ceiling because, in a spousal relationship, the income used in the formula is half of the joint private income. The April 2015 published means test, R64,680 and R129,360, matches that calculation.

The extra R20 a month paid from age 75 is not included in A. Published means-test tables use one older-person ceiling. Including the R20 would raise a single person’s ceiling by R960. That alternative is named and is not the primary rule.

The asset test, deemed income from assets, and the regulation 20 deductions are not in the proxy. The asset file does not measure an assessable stock. Passing this screen means apparently eligible.

## Partnership

| Marital code | Primary treatment |
| --- | --- |
| 1 Married, resident spouse linked and reciprocal | Couple ceiling |
| 1 Married, spouse not in the household, pointer missing, self-pointer, or pointer not returned | Unresolved. The single ceiling is not used |
| 2 Living together, 5 Separated, 9 Unspecified | Unresolved |
| 3 Never married, 4 Widowed, 6 Divorced | Single ceiling |

The regulations’ spouse definition covers the Marriage Act, customary marriage, a civil union, and marriage under the tenets of an Asiatic religion. It does not cover unmarried cohabitation. A separated spouse still counts unless desertion for three months is established. The survey cannot show that, and it does not record the absent spouse’s income. Both categories therefore stay unresolved, which is the conservative primary rule from Submission 1.

## What the reason counts show

Reason codes overlap. A person who fails one rule keeps any other reason as well. Counts are people in the age-60 frame who carry that code.

| Reason | People |
| --- | --- |
| Income above the ceiling | 93 |
| Own disability grant | 25 |
| Own war-veterans grant | 0 |
| Ambiguous partnership | 74 |
| Spouse not in the household | 81 |
| Spouse pointer missing | 6 |
| Spouse link inconsistent | 5 |
| Applicant income unresolved | 7 |
| Spouse income unresolved | 4 |
| Incompatible-grant item unspecified | 20 |
| Pass | 1,013 |

Of the 117 fails, 93 are above the income ceiling and 25 report a disability grant. One person is in both groups. No one reports a war-veterans grant.

Of the 187 unresolved people, the largest groups are a married person whose spouse is not in the household (81) and an ambiguous partnership (74, including 3 who also fail on a disability grant). Seven people have an income source marked but no annual amount.

Every one of the 1,013 passes has a resolved OPG answer: 946 recipients and 67 non-recipients. For all 946, preceding-year OPG income (COICOP `50331000`) is positive. For all 67, it is zero. The receipt-period flag is therefore present for nobody in the final cohort. The flag was checked with synthetic cases in which the two measures disagree, and those cases keep the current-receipt label.

Caregiver child grants, care-dependency grants, foster-care grants, and grant-in-aid are stored as flags. They do not exclude anyone and they do not set Y.
