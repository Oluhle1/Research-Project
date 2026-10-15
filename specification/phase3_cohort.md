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

**D073 source update —15 October 2026:** The correct original 2008 regulations,
GN R898/GG31356, are now read. They verify original spouse/joint/half-joint means,
desertion, deductions and the R100 minimum, with commencement 22 August 2008.
Their original formula is 1.3A−0.5B; the 2011 amendment uses 1.4A−0.4B and the 2022
replacement uses 1.6A−0.4B. The intervening operative 2014–2015 chain and original
rate notices remain missing. The2008 income list includes dependent-child and
ex-gratia items; it is not identical to 2022. Research ceilings and all code/cohort
results remain fixed. See [the new source audit](../paper/historical_2008_source_audit.md).
The earlier verification updates below describe their dated evidence stages.

**Uploaded-source update — 15 October 2026 (D072):** Two genuine uploaded legal
originals have now been read: GN R286/GG34169 specifies 1.4A − 0.4B from
1 April 2011; GN R2119/GG46459 specifies 1.6A − 0.4B and the R100 minimum,
but commenced on 31 May 2022. The supplied 2008 `415.pdf` is the wrong Gazette.
The correct base is GN R898/GG31356. Its full text, the intervening amendments
and original 2014/2015 rate notices are still needed to establish the survey-period
law. The ceilings and partnership rules below remain fixed research assumptions.
See [the uploaded-source audit](../paper/uploaded_legal_source_audit.md).
No screening, cohort, data, application or model was changed.

**Verification update — 14 October 2026:** The point 3 audit checked the code,
conditional threshold arithmetic and original LCS questionnaire/metadata.
Official notices and operative formula, minimum-payment, couple-resource and
statutory spouse provisions remain unverified because source retrieval failed.
The historical legal rationale below records the study's assumptions; it is
not authenticated law. See [the screening source audit](../paper/historical_screening_source_audit.md).
No substantive rule, cohort or model changed.

The recorded research calculation assumes D = 1.6A − 0.4B and a minimum payment of R100 a month. The uploaded 2022 Annexure A contains these terms; their historical applicability remains unresolved. B at the ceiling is the private income at which D is still exactly R1,200 a year. Income at that ceiling passes. Income above it fails.

| Interview month | Grant maximum used as A | Single ceiling | Couple ceiling | People aged 60+ |
| --- | --- | --- | --- | --- |
| October 2014–March 2015 | R1,350 a month, from GN 211, GG 37474, 1 April 2014 | R61,800 | R123,600 | 699 |
| April 2015–October 2015 | R1,410 a month, from GN 277, GG 38647, 1 April 2015 | R64,680 | R129,360 | 618 |

The recorded development rationale treats the October 2014 adjustment as applying to child support and grant-in-aid, and assumes half-joint income for spouses. That assumption doubles the single ceiling. The recorded April 2015 means-test figures match the calculation. These notice-based statements still require original historical authentication; they do not replace the source check above.

The extra R20 a month paid from age 75 is not included in A. Published means-test tables use one older-person ceiling. Including the R20 would raise a single person’s ceiling by R960. That alternative is named and is not the primary rule.

The asset test, deemed income from assets, and the regulation 20 deductions are not in the proxy. The asset file does not measure an assessable stock. Passing this screen means apparently eligible.

## Partnership

| Marital code | Primary treatment |
| --- | --- |
| 1 Married, resident spouse linked and reciprocal | Couple ceiling |
| 1 Married, spouse not in the household, pointer missing, self-pointer, or pointer not returned | Unresolved. The single ceiling is not used |
| 2 Living together, 5 Separated, 9 Unspecified | Unresolved |
| 3 Never married, 4 Widowed, 6 Divorced | Single ceiling |

The uploaded 2022 regulation 1 links the spouse definition to specified marriage, customary-marriage, civil-union and religious bases. Regulation 20(3) requires Agency satisfaction that desertion continued for at least three months and the spouse is unwilling to support the applicant before disregarding spouse means. These later clauses do not authenticate the historical law. Survey categories alone cannot establish legal spouse status or the desertion conditions; absent spouse income is also unavailable. Ambiguous partnership cases therefore remain unresolved under the conservative primary research rule. Residence and reciprocal household links are research consistency requirements, not legal eligibility conditions.

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
