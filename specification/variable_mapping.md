# Variable mapping

**Phase:** 2. Data audit only. This file does not screen eligibility and does not estimate non-receipt.  
**Date:** 2026-09-25  
**Sources:** released LCS 2014/2015 CSV files; `Dataset/metadata/Living Conditions Survey Metadata.pdf`; `Living Conditions Survey Questionnaire.pdf`; `Living Conditions Survey Coicopcodes.pdf`.  
**Audit script:** `analysis/phase2_data_audit.py`  
**Audit tables:** `output/phase2/`

Each row is one research concept from Submission 1. Nothing in this table is a substitute variable. Where a concept cannot be built, the row says so.

## 1. Files

| File | Rows | Columns in the release | Role |
| --- | --- | --- | --- |
| `LCS2015PERSONSFINAL.csv` | 88,906 | 207 | Person file. One row per person |
| `LCS2015HOUSEHOLD.csv` | 23,380 | 307 | Household file. One row per household. Holds welfare-office distance |
| `LCS2015PERSONINCOME.csv` | 51,656 | 9 | Person-attributable annual income. One row per person per COICOP code |
| `LCS2015HOUSEHOLDASSETS.csv` | 23,380 | 116 | Durable-goods acquisitions. Not an eligibility input |
| `LCS2015TOTALLCS.csv` | 997,717 | 35 | Household item file. Not person-attributable income |

The final release contains 23,380 households. Submission 1’s figure of 27,527 is the realised sample in the metadata, before households without a completed questionnaire (Sections 1 and 6) or without diary information were removed. The KwaZulu-Natal response rate of 89.6% matches the metadata. Neither figure is the study cohort.

Fieldwork, from the metadata: 13 October 2014 to 25 October 2015. `SURVEYDATE` values cover October 2014 through October 2015.

## 2. Keys and joins

| Concept | File | Variable | Coding | Transformation | Purpose |
| --- | --- | --- | --- | --- | --- |
| Household identifier | All five files | `UQNO` | 18-digit string. Digits 1–11 PSU, 12–16 dwelling unit, 17–18 household, as documented in the metadata | None | Link person, household, income, assets, and the total file |
| Person identifier | Person file and person-income file | `UQNO` + `PERSONNO` | `PERSONNO` is the person number within the household. Metadata range 01–27. Stored without leading zeros | None | Person-level unit |
| Spouse pointer | Person file | `Q19SPOUSNO` | Person number of the spouse or partner in the same household. `88` not applicable. `99` unspecified. Metadata valid range for a real pointer is 1–12 | Link to `PERSONNO` within `UQNO` | Couple income screen |
| Derived PSU | Person file | first 11 characters of `UQNO` | Metadata says the PSU number is those digits | Derive at read time. Do not treat it as a released column | S11 grouping sensitivity. 2,974 PSUs nationally, 454 in KwaZulu-Natal, none crossing a province |
| Stratum | — | Not in any released file | The metadata describes strata in the weight construction and does not release a stratum id | Cannot be constructed | Full design-based variance is not available |

Join results are in `output/phase2/join_audit.csv` and in `specification/phase2_data_audit.md`.

## 3. Population frame

| Concept | File | Variable | Coding | Transformation | Purpose |
| --- | --- | --- | --- | --- | --- |
| Province | Person file and household file | `province_code` | `5` = KwaZulu-Natal. `1` Western Cape, `2` Eastern Cape, `3` Northern Cape, `4` Free State, `6` North West, `7` Gauteng, `8` Mpumalanga, `9` Limpopo | Keep `province_code == "5"` | Study frame. The two files agree on every person |
| Age | Person file | `Q14AGE` | Age in completed years. Metadata: `000` = less than one year; valid ages 1–105. The release stores these as numbers, including 0. No non-numeric values | Frame rule later: completed age 60 or older, so `Q14AGE >= 60` includes people recorded as 60 | Study frame |
| Sex | Person file | `Q12SEX` | `1` male, `2` female. No other codes and no blanks | Table I binary. Reference category not yet chosen | Predictor, 1 df |

The metadata says age was hot-deck imputed for 0.2% of respondents and sex for 0.4% before release. The public file has no missing age or sex and no imputation flag, so those people cannot be separated. They stay in the frame. This limit is recorded in the decision log.

Age-frame availability, not an eligibility result: KwaZulu-Natal has 15,388 people in 3,686 households. Of those, 1,317 people in 1,068 households are aged 60 or older. Screening has not been applied.

## 4. Partnership and the spouse link

Questionnaire routing is a data fact. The legal single-versus-couple class for two categories stays open until Phase 3 checks the official spouse definition. Phase 2 does not assign those two categories to a threshold.

| `Q17MARITAL` | Label | `Q18PARTINHH` route | Phase 2 classification |
| --- | --- | --- | --- |
| 1 | Married | Spouse module is asked | Couple path when a resident spouse can be linked |
| 2 | Living together like married partners | Spouse module is asked | Ambiguous. Not placed on the single or the couple threshold in this phase |
| 3 | Never married | Skip to Q1.10 | Unpartnered route on the questionnaire |
| 4 | Widower/widow | Skip to Q1.10 | Unpartnered route on the questionnaire |
| 5 | Separated | Skip to Q1.10 | Ambiguous for the means test. The questionnaire does not collect that spouse |
| 6 | Divorced | Skip to Q1.10 | Unpartnered route on the questionnaire |
| 9 | Unspecified | No spouse module | Unresolved |

`Q18PARTINHH`: `1` yes, the spouse or partner lives in the household; `2` no; `8` not applicable; `9` unspecified.

`Q19SPOUSNO`: person number, or `88` not applicable, or `99` unspecified. Married people whose partner is not in the household are coded `88`. That is the paper’s unresolved income screen, not a single-person threshold.

`Q16RELATION`, used only as a consistency check: `01` head or acting head; `02` husband, wife, or partner of person 01; `03` child; `04` sibling; `05` parent; `06` grandparent; `07` grandchild; `08` other relative; `09` non-related; `10` live-in domestic paid in kind.

Consistency rule adopted for the later screen, because of how code `02` is defined:

- The pointer resolves to a different person in the same household.
- That person’s `Q19SPOUSNO` points back.
- A self-pointer, an unmatched pointer, or a pointer that is not returned is an unresolved link.
- Code `02` means partner of the head only. A reciprocal pointer between two people who are not the head and the head’s partner is still a consistent link. Requiring codes `01` and `02` would drop married couples who are not the head’s couple.

Among people who are married and whose partner lives in the household: 12,835 reciprocal links, 812 of them not a head–partner pair, 106 self-pointers, 127 non-reciprocal pointers, and 3 unmatched pointers. In the KwaZulu-Natal age-60 frame the same group has 424 reciprocal links (12 of them not a head–partner pair), 4 self-pointers, 1 non-reciprocal pointer, and no unmatched pointer.

## 5. Income

| Concept | File | Variable | Coding | Transformation | Purpose |
| --- | --- | --- | --- | --- | --- |
| Annual nominal income | Person-income file | `Valueannualized` | Already annualised by Statistics South Africa. Metadata range R100–R3,200,000. No zeros, no negatives, no non-numeric values in the release | Sum across COICOP rows for the person after dropping social-assistance codes. Do not multiply by 12 or 26 again | Resource proxy |
| CPI-adjusted annual income | Person-income file | `Valueannualized_adj` | Inflated or deflated with CPI. The metadata benchmarks the survey year to April 2015 prices | Not the primary proxy | Income-definition sensitivity |
| Person weight on an income row | Person-income file | `Persns_wgt` | Same value as the person file for every matched person | Check only | Join integrity |
| No income from any listed source | Person file | `Q11714NOTOALL` | `1` = no to all sources Q1.17.01–13; `8` = not applicable because at least one source is yes; `9` = unspecified | See the zero rule below | Decides when a missing income row is a supported zero |
| Social-grant income in the last year, yes/no | Person file | `Q11710GRANTS` | `1` yes, `2` no, `3` don’t know, `9` unspecified | Not an amount. Not the OPG outcome | Supports the reading of Q1.17 |
| Household total income | Household file | `income` | Household total | Do not allocate it to people | Out of scope for the proxy |

COICOP labels below are from the income section of the COICOP code list. The person-income file contains 22 codes. Two codebook entries have no rows: `50243100` (exchange-traded funds) and `50333400` (war veterans grant).

**Exclude from the primary resource proxy** (social-assistance grants and social relief):

| Code | Label |
| --- | --- |
| `50331000` | Old age grant |
| `50332000` | Disability grants |
| `50332100` | Child support grant |
| `50333100` | Care dependency grant |
| `50333200` | Foster care grant |
| `50333300` | Grant-in-aid |
| `50333400` | War veterans grant |
| `50333500` | Other assistance from government, including social relief |

**Keep in the primary proxy:** salaries and business (`50110000`, `50120000`, `50121000`); property, royalties, interest, dividends, and share trading (`50210000`–`50243200`); pension from previous employment (`50310000`); annuities from own investment (`50320000`); alimony and other income from individuals (`50410000`, `50420000`).

`50333600` (workmen’s compensation, UIF, and similar funds) is not a social-welfare grant in questionnaire section 4.1. It stays in the primary proxy. Dropping it is an income-definition sensitivity, not the primary rule.

**Preceding-year OPG income** is `50331000` only. The amount is `Valueannualized` on that row. A person with no such row has no recorded OPG income in this file.

**Zero rule:**

| `Q11714NOTOALL` | Income row | Reading |
| --- | --- | --- |
| 1 | None | Supported zero. The no-to-all item was marked and the income schedule has no amount |
| 1 | Present | Contradiction. 11 people nationally, none in the KwaZulu-Natal age-60 frame. Do not treat as a clean zero |
| 8 | None | Unresolved amount. The person reported a source and the file has no annual value. 186 nationally; 7 in the KwaZulu-Natal age-60 frame |
| 8 | Present | Sum the non-social-assistance codes |
| 9 | Either | Unresolved. 161 nationally; none in the KwaZulu-Natal age-60 frame |

In the KwaZulu-Natal age-60 frame, 1,282 people have an income row, 28 have a supported zero, and 7 have an unresolved missing amount.

The income file must be aggregated to the person before it is joined. Joining the 51,656 item rows straight onto the person file would duplicate people. Aggregation changes 51,656 item rows into 41,507 person keys. That change is expected.

## 6. Grant receipt

Section 4.1 of the questionnaire. Ask 4.1a for every person. If the answer is No or Don’t know, skip 4.1b. Child grants are linked to a caregiver.

| Concept | Variable | Codes | Use |
| --- | --- | --- | --- |
| Any social grant | `Q41ASOCGRANT` | `1` yes, `2` no, `3` don’t know, `9` unspecified | Read with the OPG item. Code `2` with a not-applicable OPG item is a consistent report of no grant |
| OPG, current | `Q41B1OLDAGE` | `1` yes, `2` no, `8` not applicable, `9` unspecified | Outcome item. `1` → Y = 0. A consistent no → Y = 1 |
| Own disability grant | `Q41B2DISAB` | same 1 / 2 / 8 / 9 | Primary exclusion when code is `1`. Code `9` does not prove absence |
| Child support grant, caregiver | `Q41B3CHILD` | same | Does not exclude and does not set Y |
| Care dependency grant, caregiver | `Q41B4CAREDEP` | same | Caregiver-linked. Does not exclude |
| Foster care grant, caregiver | `Q41B5FOSTER` | same | Caregiver-linked. Does not exclude |
| War veterans grant | `Q41B6WARVET` | same | Primary exclusion when code is `1`. The national file has no code `1` |
| Grant-in-aid | `Q41B7INAID` | same | Does not exclude |

Skip pattern in the whole person file: people who answer No to 4.1a are almost all code `8` on the OPG item. Three people are code `2` instead, and eight people with an unspecified 4.1a answer are code `2` on the OPG item. Those cases are contradictions for Phase 3, not clean non-receipt.

In the KwaZulu-Natal age-60 frame the 4.1a / OPG skip is consistent: 1,158 people report a grant, of whom 1,132 report OPG and 26 report a grant that is not OPG; 159 report no grant and are code `8` on the OPG item. There is no don’t-know or unspecified on 4.1a in that frame, and no unspecified OPG item. Disability is unspecified for 18 people in that frame, and the war-veterans item is unspecified for 20. Those 9-codes are not a No.

## 7. Predictors

| Concept | File | Variable | Coding | Transformation | Purpose |
| --- | --- | --- | --- | --- | --- |
| Age | Person | `Q14AGE` | Completed years | `(Q14AGE - 60) / 10` inside the 60+ frame | Table I, 1 df |
| Sex | Person | `Q12SEX` | `1` male, `2` female | Binary. Reference level still open | Table I, 1 df |
| Schooling | Person | `Q21HIGHLEVEL` | See below. Grade 7 is code `08`, not code `07` | Binary. Codes that do not say which side of Grade 7 they fall on stay missing | Table I, 1 df |
| Settlement | Person and household | `SETTLEMENT_TYPE` | Four categories, and no code 3: `1` urban formal, `2` urban informal, `4` traditional area, `5` rural formal | Four-level factor, 3 df. Reference level still open. Person and household values match on every row | Table I |
| Welfare-office access | Household | `Q531WELFARE` | Distance from the dwelling. Codes below | Join onto the person on `UQNO`. Household key is unique, so the join does not duplicate people | Table I, 1 df |

`Q21HIGHLEVEL` and the Grade 7 cut:

| Class | Codes |
| --- | --- |
| Below Grade 7 | `98` no schooling; `01` Grade R; `02`–`07` Grade 1 through Grade 6 |
| Grade 7 or above | `08` Grade 7 through `20` N6; `23`–`30` certificates and degrees that state Grade 12 or a higher qualification |
| Not assigned | `21` certificate with less than Grade 12; `22` diploma with less than Grade 12; `31` other; `32` don’t know; `99` unspecified |

Codes `21` and `22` do not say whether the qualification is below Grade 7. They are predictor missing, not a guessed class. In the KwaZulu-Natal age-60 frame this missing schooling class is codes `21` (1 person), `22` (3), and `32` (3).

`Q531WELFARE`, from the metadata code list for distance to the nearest welfare office:

| Codes | Label | Table I class |
| --- | --- | --- |
| 1, 2, 3, 4 | Less than 500 m; 500 m to under 1 km; 1 km to under 2 km; 2 km to under 5 km | Nearer than 5 km |
| 5, 6, 7 | 5 km to under 10 km; 10 km to under 20 km; 20 km or more | At least 5 km |
| 8 | Not available | Unavailable, grouped with at least 5 km |
| 9 | Don’t know | Predictor missing |
| 99 | Unspecified | Predictor missing |

`Q532WELFARE` is the usual mode of transport to the welfare office (walking, taxi, bus, train, own transport, other). It is not the distance measure in Table I and is not used as that predictor.

## 8. Weights and design

| Concept | File | Variable | Coding | Transformation | Purpose |
| --- | --- | --- | --- | --- | --- |
| Person weight | Person file | `Persns_wgt` | Positive on every row. Observed range 50 to 5,739.891763, matching the metadata | Use as released. No missing values | Weighted non-receipt proportion |
| Household weight | Household file | `hholds_wgt` | Positive on every row. Metadata range about 107.05 to 7,564.64 | Not the person-level weight | Not used for the person proportion |
| PSU | Derived | `UQNO` digits 1–11 | Documented decomposition | Derive | S11 only |
| Stratum | Not released | — | — | Cannot be constructed | Design-based intervals that need stratum are not available. Weighted proportions can still be calculated. Any variance figure later must be labelled as an approximation |

## 9. Concepts that cannot be constructed

| Submission 1 concept | Finding |
| --- | --- |
| Stratum / full survey design | No stratum variable in the person, household, income, asset, or total file |
| Imputation flag for age or sex | Hot-deck imputation happened before release and is not marked |
| Legal asset stock | The asset file records acquisitions of listed durables. It is not a stock of assessable assets. It is not an eligibility input |
| Person income from the household total | `income` on the household file, and every amount on `LCS2015TOTALLCS.csv`, is a household total or a household item. They are not allocated to people |
| War-veterans grant receipt as a positive case | The item exists. The national file contains no `Q41B6WARVET = 1` and no COICOP `50333400` row. The rule can be coded. On this release it excludes nobody |
| Official rand thresholds | Not in the LCS files. Still open for Phase 3 |

## 10. What Phase 3 still has to decide

- The rand thresholds and the at-threshold boundary for 13 October 2014–25 October 2015.
- Whether marital code `2` (living together) and code `5` (separated) use the couple threshold, the single threshold, or stay unresolved on the primary screen.
- Reference categories for sex, schooling, settlement, and welfare access.
- The random seed and the other implementation settings already listed as G18–G22.
