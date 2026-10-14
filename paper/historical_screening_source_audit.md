# Historical screening: source and implementation audit

Audit date: **14 October 2026**. Baseline: `c95b786`.
**Status: implementation, conditional arithmetic and survey checks passed;
original legal verification remains incomplete.**

The user requested verification of historical thresholds and clarification of
marital status, spouse resources and ambiguous arrangements. Twelve fresh
requests to government/SASSA/GPW endpoints and Gazette facsimile candidates
failed with proxy-tunnel or HTTP 403 responses. No original legal text, verified
quotation or source-page reference was obtained. The attempted URLs do not
establish that the candidate files exist. The older 11 October audit remains a
separate historical record and has not been overwritten.

## Conditional threshold calculation

| Implemented interview period | Recorded monthly maximum | Annual A | Single ceiling | Couple ceiling |
| --- | ---: | ---: | ---: | ---: |
| October 2014–March 2015 | R1,350 | R16,200 | R61,800 | R123,600 |
| April–October 2015 | R1,410 | R16,920 | R64,680 | R129,360 |

Assuming the annual individual grant is D = 1.6A − 0.4B, with annual maximum A,
annual private income B and minimum annual D = R1,200, the single ceiling is
(1.6A − 1,200)/0.4. Assuming B is half the joint annual income doubles the
couple ceiling. Decimal arithmetic matches the implemented constants. Equality
passes in the primary code. The zero-payment boundary and age-75 supplement
are separate S1 sensitivity assumptions. These checks verify arithmetic and
implementation; they do not authenticate the maximum rates, effective dates,
operative formula, R100 rule or couple-resource law.

## Partnership decisions actually implemented

| Survey response or link | Primary research treatment |
| --- | --- |
| Never married, widowed or divorced (3/4/6) | Own resolved private income against the single ceiling. |
| Married (1), reported resident spouse, different-person same-household pointer returned by spouse | Both resolved private incomes summed against the couple ceiling, regardless of spouse age. |
| Married with nonresident spouse | Unresolved; no assumed single status or zero absent resources. |
| Missing/unspecified residence or person number; self, unmatched or nonreciprocal pointer | Unresolved. |
| Living together, separated or unspecified status (2/5/9) | Unresolved in the primary analysis; S2 examines alternatives. |
| Missing applicant or linked-spouse income | Unresolved unless the individual no-income response and absent schedule support zero. |
| Known incompatible-grant failure and an unresolved item | FAIL takes priority; all reason codes remain. |

Survey categories and reciprocal roster pointers do not establish statutory
spouse status. Questionnaire Q1.7–1.9 routes separated respondents past the
spouse module, so the survey does not provide that partner's details. This
motivates the unresolved research treatment; it is not a verified legal rule
about separation, desertion or cohabitation. Income is already annualised,
nominal and person-attributable; no household-income allocation or second
annualisation occurs. Survey preceding-year income is a proxy for legal resource
assessment, not a complete assessment of assets, deemed income or deductions.

## Primary survey sources read

| Document | PDF pages / items | What the source supports |
| --- | --- | --- |
| LCS Questionnaire | 5–6, Q1.7–1.9 | Marital categories, resident spouse/partner, household person number and routing. |
| LCS Metadata | 125–126 | Released marital, residence and spouse-pointer codes. |
| LCS Questionnaire / Metadata | 8 / 130, Q1.17.14 | Explicit no-to-all income-source response. |
| LCS Metadata | 182, Valueannualized | Annual individual income already annualised. |
| LCS Questionnaire | 93–96, Section 24 | Preceding-year regular-income reference period. |

Page numbers count the PDF cover. File checksums, implementation line anchors,
aggregate checks and exact failed requests appear in the
[machine-readable audit](historical_screening_source_audit.json).

The 187 unresolved adults comprise 105 married, 63 living together, eight
separated and 11 other single-status adults. Of the 105 married unresolved
adults, 80 have nonresident spouses. The older reason-code frequency of 81
includes one FAIL; likewise 74 ambiguous-partnership reasons include three
FAILs. Reason frequencies overlap and must not be presented as mutually
exclusive unresolved counts. The manuscript's existing 105/63 figures remain
correct. S2a–d add 59/4, 60/2, 8/0 and 68/2 people/events respectively; these
are assumption checks, not evidence that one legal classification is correct.

## What remains necessary

Read authentic 2014/2015 notices and the regulations/amendments operative in the
survey period. Check rate/effective-date identity, the payment formula and
minimum boundary, joint-resource treatment, statutory spouse definition,
separation exceptions and the age-75 supplement. Rate notices alone do not
establish all means-test rules. The older Phase 3 specification's legal spouse
and desertion statements remain recorded development assumptions, rather than
newly authenticated provisions. No screening-rule or numerical-result change
was justified from the accessible evidence.
