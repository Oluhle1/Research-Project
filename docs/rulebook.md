# Historical screening rulebook

**Current source update — 15 October 2026 (D-074):** Original GG 37474,
28 March 2014, verifies GN 211's R1,350 monthly standard rate from 1 April
2014 (page 3). Its Schedule paragraph 2 substitutes Annexure A(2), specifying
`D = 1.6A − 0.4B` (pages 4–5); printed commencement paragraph 1 applies
from 1 April 2014. GN 277/GG 38647, 30 March 2015, verifies R1,410 from
1 April 2015 (page 3). The original 2008 R898 Annexure A(5) supplies the
R100 monthly minimum; regulation 19(1) uses half-joint annual income,
18(2)/(3) governs joint income and desertion subject to Agency approval,
and regulation 1 defines spouse. R621/GG 39007, 21 July 2015, leaves these
OPG formula, means and spouse provisions unchanged. The four standard-rate
ceilings below are source-verified. See the [verified thresholds audit](../paper/historical_thresholds_verified_audit.md)
and its JSON companion. No screening rule, cohort, application or model changed.

D-073's earlier source gap and 5,442/141/374-word build with 28 references
are archived at `7d54c18`. The [2008 audit](../paper/historical_2008_source_audit.md),
[uploaded-source audit](../paper/uploaded_legal_source_audit.md) and
[initial screening audit](../paper/historical_screening_source_audit.md) record
their dated evidence stages; their missing-source statements are not current findings.

Rule version **`opg-kzn-primary-v1`** is implemented in `analysis/phase3_build_cohort.py`. `opg_core.screening` adapts validated normalized rows and calls the original `resolve_link()` and `screen()` functions. It does not independently reimplement the substantive income, grant or receipt rules, fit a model or write files.

These are observable historical research rules, not a determination of statutory eligibility. Assets, deemed asset income, allowable deductions and other incompletely observed legal conditions remain limitations. The historical thresholds must not be presented as current policy.

| Condition | Result / reason |
| --- | --- |
| Age below 60 | `OUT_OF_FRAME`; `OUT_AGE_BELOW_60`; receipt is not assessed |
| Own disability or war-veterans grant reported (`1`) | `FAIL_DISABILITY_GRANT` / `FAIL_WAR_VETERAN_GRANT` |
| Either incompatible grant unspecified (`9`) | `UNRES_INCOMPATIBLE_GRANT_UNSPECIFIED` |
| Never married, widowed or divorced (`3`, `4`, `6`) | Compare own private income with the single-person ceiling |
| Living together, separated or unspecified (`2`, `5`, `9`) | `UNRES_PARTNERSHIP_AMBIGUOUS`; no assumed ceiling |
| Married, resident spouse, reciprocal different-person pointer in the household | Combine the two private incomes and compare with the couple ceiling |
| Married, spouse nonresident | `UNRES_SPOUSE_NONRESIDENT`; do not substitute the single ceiling |
| Missing/unspecified pointer or residence response | `UNRES_SPOUSE_MISSING` |
| Self-pointer or nonreciprocal pointer | `UNRES_SPOUSE_RELATIONSHIP` |
| Pointer does not identify an uploaded household member | `UNRES_SPOUSE_NOT_IN_HOUSEHOLD` |
| Own / linked spouse private income missing | `UNRES_INCOME_ABSENT` / `UNRES_INCOME_SPOUSE` |
| Comparable income exceeds the relevant ceiling | `FAIL_INCOME_ABOVE_THRESHOLD` |
| Caregiver child, care-dependency or foster grant | Corresponding `FLAG_CAREGIVER_*`; does not exclude or establish OPG receipt |
| Grant-in-aid | `FLAG_GRANT_IN_AID`; does not exclude |

| Interview period | Single annual ceiling | Couple annual ceiling |
| --- | ---: | ---: |
| October 2014–March 2015 | R61,800.00 | R123,600.00 |
| April–October 2015 | R64,680.00 | R129,360.00 |

With annual maximum `A` and minimum annual payment R1,200, the single
ceiling is `(1.6A − 1,200) / 0.4`; half-joint income doubles it for a couple.
Both notices also provide an extra R20 a month from age 75. Using the
standard age-60–74 maximum across all ages is an explicit primary research
choice, rather than a claim that the notices omit the supplement; S1c remains
the unchanged age-specific sensitivity. The income proxy omits assessable
assets, deemed asset income and legal deductions. Resident reciprocal spouse
links are survey consistency requirements, not statutory conditions.
Ambiguous or nonresident-spouse cases remain unresolved, not legally ineligible.

Equality passes; one cent above fails. Annual income is already annualized and is not multiplied by twelve again. The original proxy excludes social-assistance COICOP codes `50331000`, `50332000`, `50332100`, `50333100`, `50333200`, `50333300`, `50333400`, `50333500`. Workmen's compensation/UIF-like code `50333600` remains in the primary private-income proxy. See `specification/variable_mapping.md` for source aggregation and zero-schedule evidence.

A known failure wins over unresolved items while preserving both reason codes. Without failure, unresolved items produce `UNRESOLVED`. Otherwise the observable screen passes and appends `PASS_PRIMARY`. The age frame runs before these rules. Row order is retained; duplicate keys are blocked before constructing the spouse lookup.

Receipt is assessed separately, only for `PASS` rows. `any_grant=1` with `oldage=1` is `RECIPIENT` (`y=0`). `any_grant=1` with `oldage=2`, or `any_grant=2` with `oldage=2/8`, is `NON_RECIPIENT` (`y=1`). Other combinations are `UNRESOLVED`, with `UNRES_GRANT_RESPONSE`; their screen can still be `PASS`. A difference between current receipt and preceding-year OPG income adds `FLAG_RECEIPT_PERIOD_DISAGREE` without changing the observed current response.

| Screen / receipt | App classification |
| --- | --- |
| `PASS` / `RECIPIENT` | `APPARENTLY_ELIGIBLE_REPORTED_RECEIPT` |
| `PASS` / `NON_RECIPIENT` | `APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT` |
| `FAIL` / `NOT_ASSESSED` | `FAILED_OBSERVABLE_RULE` |
| `UNRESOLVED` / `NOT_ASSESSED` | `ELIGIBILITY_UNRESOLVED` |
| `PASS` / `UNRESOLVED` | `RECEIPT_UNRESOLVED` |
| `OUT_OF_FRAME` / `NOT_ASSESSED` | `OUT_OF_STUDY_FRAME` |

`model_eligible_for_scoring` initially requires `PASS` and resolved observed receipt, reproducing the study cohort. Model feature suitability is checked separately by inference. A risk score never changes the screening or receipt label.

Phase 1 tests recover the original **22 synthetic screening cases** and add actual spouse linkage, age-60 boundaries, separated status, invalid uploads, missing values, duplicate-key rejection and historical-date tests. The older “26 checks” combine those 22 with two income-schedule checks, a structural leakage check and one run trace; they are not 26 distinct synthetic screening scenarios. Local reference parity compares all 15,388 KZN records' screen status, receipt status, ordered reason codes and outcome with frozen CLI output. No respondent-level comparison report is committed; mismatch assertions expose counts only.
