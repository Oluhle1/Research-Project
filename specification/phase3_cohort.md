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

**Current source update — 15 October 2026 (D-074):** The original 2014 and
2015 rate notices and operative formula are now read. GG 37474, 28 March
2014, page 3 (GN 211) sets R1,350 monthly from 1 April 2014. On pages 4–5,
Schedule paragraph 2 substitutes Annexure A(2) with `D = 1.6A − 0.4B`, with printed
commencement paragraph 1 effective 1 April 2014. GN 277/GG 38647,
30 March 2015, page 3 sets R1,410 from 1 April 2015. The 2008 R898
Annexure A(5) supplies the R100 monthly minimum and regulation 19(1)
the half-joint income rule. R621/GG 39007, 21 July 2015, leaves the OPG
formula, means and spouse provisions unchanged. The four standard-rate
ceilings are verified in [the new audit](../paper/historical_thresholds_verified_audit.md)
and its JSON companion. No cohort, code, model or substantive rule changed.

D-073's incomplete source stage and its 5,442/141/374-word build with
28 references are archived at `7d54c18`. Earlier audits retain their dated
findings; their missing-source statements do not describe the current review.

Using annual amounts, the single ceiling is `(1.6A − 1,200) / 0.4`, the
income at which annual payment D is exactly R1,200. Half-joint annual
income doubles that ceiling for a couple. Income at the ceiling passes;
income above it fails the observable research rule.

| Interview month | Grant maximum used as A | Single ceiling | Couple ceiling | People aged 60+ |
| --- | --- | --- | --- | --- |
| October 2014–March 2015 | R1,350 a month, from GN 211, GG 37474, 1 April 2014 | R61,800 | R123,600 | 699 |
| April 2015–October 2015 | R1,410 a month, from GN 277, GG 38647, 1 April 2015 | R64,680 | R129,360 | 618 |

Both original rate notices include an extra R20 monthly from age 75. The
primary rule uses the standard age-60–74 maximum across ages as an explicit
research choice. Including the supplement raises the single ceiling by R960
and the couple ceiling by R1,920; S1c remains the unchanged age-specific
sensitivity. Source verification does not turn the proxy into a full legal means test.

The asset test, deemed income from assets, and the regulation 20 deductions are not in the proxy. The asset file does not measure an assessable stock. Passing this screen means apparently eligible.

## Partnership

| Marital code | Primary treatment |
| --- | --- |
| 1 Married, resident spouse linked and reciprocal | Couple ceiling |
| 1 Married, spouse not in the household, pointer missing, self-pointer, or pointer not returned | Unresolved. The single ceiling is not used |
| 2 Living together, 5 Separated, 9 Unspecified | Unresolved |
| 3 Never married, 4 Widowed, 6 Divorced | Single ceiling |

The original 2008 R898 regulation 1 defines spouse. Regulations 18(2)/(3)
govern joint income and desertion: disregarding spouse means requires the
Agency's approval of continued desertion for at least three months and
unwillingness to support the applicant. Regulation 19(1) uses half-joint
annual income, so resolved spouse resources enter regardless of spouse age.
R621/2015 does not alter these provisions. Survey categories cannot establish
legal spouse status or the desertion conditions, and absent spouse income
is unavailable. Ambiguous and nonresident-spouse cases therefore remain
unresolved under the conservative research rule, not legally ineligible.
Residence and reciprocal household links are research consistency requirements,
not legal eligibility conditions.

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
