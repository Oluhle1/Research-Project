# Phase 2 data audit

**Date:** 2026-09-25  
**Script:** `analysis/phase2_data_audit.py`  
**Tables:** `output/phase2/join_audit.csv`, `code_frequencies.csv`, `income_absence_by_q11714.csv`, `spouse_link_audit.csv`, `file_inventory.csv`  
**Mapping:** `specification/variable_mapping.md`

The script reads the released files and writes the checks below. It does not assign PASS, FAIL, or UNRESOLVED, and it does not fit a model. Counts for KwaZulu-Natal adults aged 60 and older describe whether the required items are present. They are not the eligible cohort and they are not a non-receipt rate.

## Join and key checks

| Check | Result |
| --- | --- |
| Person rows | 88,906 |
| Duplicate `UQNO` + `PERSONNO` | 0 |
| Person households | 23,380 |
| `UQNO` not 18 digits | 0 |
| Household rows | 23,380 |
| Duplicate household `UQNO` | 0 |
| Persons with no household | 0 |
| Households with no person | 0 |
| Province mismatch after the household join | 0 |
| Settlement mismatch after the household join | 0 |
| Person-income rows | 51,656 |
| Duplicate person + COICOP | 0 |
| Distinct people with an income row | 41,507 |
| Income person keys missing from the person file | 0 |
| People with no income row | 47,399 |
| Person-weight disagreements between the person file and the income file | 0 |
| Missing or non-positive person weights | 0 |
| Asset households matching the household file | 23,380 of 23,380 |
| `LCS2015TOTALLCS.csv` households matching the household file | 23,380 of 23,380 |
| Derived PSUs | 2,974 nationally; 454 in KwaZulu-Natal; 0 crossing a province |
| Non-numeric age | 0 |

The household join leaves the person count at 88,906. The income file is an item file: 51,656 rows collapse to 41,507 people. That reduction is the required aggregation, not a loss of people at the join. Joining income before aggregation would create duplicate person rows.

## Age frame, before any eligibility rule

| Group | People | Households |
| --- | --- | --- |
| KwaZulu-Natal (`province_code` 5) | 15,388 | 3,686 |
| KwaZulu-Natal and completed age 60 or older | 1,317 | 1,068 |

## Income absence

`Q11714NOTOALL = 1` means the person was marked “no” to every income source. `8` means that item is not applicable because a source was reported.

| Frame | No-to-all, no income row | No-to-all, but an income row exists | Source reported, no income row | Unspecified |
| --- | --- | --- | --- | --- |
| National | 47,054 | 11 | 186 | 161 |
| KwaZulu-Natal, age 60+ | 28 | 0 | 7 | 0 |

The 47,054 and the 28 are supported zeros. The 186 and the 7 are unresolved amounts. The 11 national contradictions are unresolved, and none of them are in the KwaZulu-Natal age-60 frame.

## Spouse pointer, married people with the partner in the household

| Link result | National | KwaZulu-Natal, age 60+ |
| --- | --- | --- |
| Reciprocal, head and partner of the head | 12,023 | 412 |
| Reciprocal, another relationship pair | 812 | 12 |
| Self-pointer | 106 | 4 |
| Pointer does not return | 127 | 1 |
| Pointer matches nobody | 3 | 0 |
| Total | 13,071 | 429 |

The 812 and the 12 stay eligible to link. Relationship code `02` is defined as the partner of person 01, so other married people in the household cannot have that code. Self-pointers, non-returned pointers, and unmatched pointers are the unresolved links.

## Design variables

Person weights are complete and positive. A stratum identifier is not in the release. Primary sampling unit can be taken from the first 11 digits of `UQNO`, which is the decomposition given in the metadata. Weighted point estimates can be produced. A variance estimator that needs stratum cannot be produced as the full design. The PSU-grouping sensitivity can use the derived PSU.

## Concepts left unbuilt

Stratum, an imputation flag for the pre-release age and sex hot deck, a legal asset stock, and a person amount derived from household income. Details are in the mapping, Section 9. No replacement variable was introduced.
