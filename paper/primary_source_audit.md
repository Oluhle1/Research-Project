# Primary-source audit: 90-plus revision

Audit date: 11 October 2026 (Africa/Johannesburg).

**Status: incomplete external verification.** Thirteen HTTPS requests to authentic publisher, open-access index and government domains were refused by the environment’s outbound proxy with CONNECT HTTP 403. No remote source text or origin response was accessed. Three authentic Statistics South Africa PDFs already in the repository were read.

This audit distinguishes an independent source-content check from consistency with the previously submitted bibliography. The 18 recorded DOI strings match Submission 1; that does not establish that any DOI resolves or that an article supports the manuscript’s population, outcome, design or finding claims.

## What is directly supported locally

| Stable source / current IEEE number | Primary document and PDF page | Directly verified |
|---|---|---|
| 3 / 21 | LCS Metadata, pp. 2, 4, 8 and 22 | P0310/2017 metadata; household-frame institutional exclusions; released-data age/sex hot-deck imputation; key components. |
| 5 / 23 | LCS Questionnaire, pp. 25 and 35 | General social-grant and grant-specific items/skips; nearest welfare-office distance categories. |
| 4 / 22 | LCS COICOP codes, p. 18 | Listed old-age, disability, caregiver and grant-in-aid/war-veterans income codes. |

PDF page numbers count the cover; they can differ from printed page numbers. The JSON records document SHA-256 hashes and precise limits of each check. The source descriptions support measurement interpretation, rather than certify implementation. Nearest-office distance does not measure an OPG application journey or experienced compliance costs. The metadata’s acknowledgement/use paragraph is not a determination of all raw-microdata redistribution or small-cell disclosure requirements.

## Prioritised original-source checklist

| Stable source / current IEEE number | Current manuscript use | Required original-source check |
|---|---|---|
| 2 / 3 — Ralston et al. | Age-eligible rural Agincourt adults; person-level pension receipt/non-receipt. | Read Methods to confirm age eligibility, sampling frame, analytical unit, pension outcome and study design. Check complete author list, year, volume, article number and DOI against article front matter. Do not introduce an N, prevalence or effect comparison before reading the relevant original table. |
| 6 / 4 — Godfrey et al. | Rural/peri-urban Msunduzi, KwaZulu-Natal; age-eligible household-member grant-receipt proportions. | Read Methods to verify Msunduzi population, rural/peri-urban sampling, household analytical unit and exact old-age/child-grant denominator definitions. Verify which programmes and outcomes were modelled, and complete author list, pages 774–789 and DOI. No numerical sample size, rate or coefficient is independently confirmed here. |
| 12 / 13 — Moynihan, Herd and Harvey | Administrative burden comprises learning, compliance and psychological costs. | Read the original theory article to verify definitions and scope. Check front matter against 2015, volume 25(1), pages 43–69 and DOI. |
| 20 / 16 — Saito and Rehmsmeier | Precision–recall measures add information in imbalanced classification; ROC alone is insufficient. | Read original text to verify the scope of ROC/PR comparison and the relationship to average precision. Avoid equating AP with precision at an operational threshold. Verify article e0118432, 2015 and DOI. |
| 19 / 17 — Van Calster et al. | Calibration concerns agreement between predicted probabilities and outcomes. | Read original definitions of calibration-in-the-large and slope. Confirm that any calibration-intercept convention used locally is stated correctly; this citation does not itself validate the project code. Verify complete author list, 2019, BMC Medicine 17:230 and DOI. |
| 21 / 18 — Riley et al. | Small event counts constrain development and interpretation of a multivariable prediction model. | Read the binary/time-to-event sample-size paper and distinguish its formal criteria from a generic events-per-variable rule. Do not claim that 67 events and six slopes meet its formal minimum sample-size criteria without an actual calculation. Verify PART II title, 2019, volume 38(7), pages 1276–1296 and DOI. |
| 22 / 19 — Roberts et al. | Dependence structures motivate grouped internal validation. | Read original review to confirm hierarchical-dependence recommendations. Do not imply that the source specifically tested this LCS household model or that grouped folds establish external validity. Verify 2017, volume 40(8), pages 913–929 and DOI. |
| 1 / 5 — Social Assistance Act 13 of 2004 | Legal entitlement involves conditions not fully observed in this survey. | Read the original Act and amendments operative during October 2014–October 2015. Verify sections underpinning age, residence/status and grant compatibility. Trace resource-assessment, asset/deemed-income/deduction and payment-formula conditions to the correct operative regulations, not the Act alone. |
| 24 / 24 — 2014 Government Notice 211 / Gazette 37474 | Recorded maximum OPG rate R1,350/month from April 2014. | Obtain the authentic notice from Government Printing Works or the government portal and confirm notice number, date, effective date and the applicable maximum rate. The attempted PDF URL is a candidate official endpoint; its existence was not established because the proxy refused the connection. Separately obtain the operative Annexure A formula and R100 minimum-payment provision; verify that the rate and formula apply to the selected group. |
| 25 / 25 — 2015 Government Notice 277 / Gazette 38647 | Recorded maximum OPG rate R1,410/month from April 2015. | Obtain the authentic notice and confirm notice number, date, effective date, applicable rate and any published income limits. The attempted PDF URL is a candidate official endpoint; its existence was not established because the proxy refused the connection. Verify the operative formula, R100 payment boundary and couple-resource treatment from original regulations/annexure. |

The Ralston and Godfrey populations and units above are the manuscript’s recorded claims, not newly verified source findings. No study sample size, prevalence or numerical association is added on the strength of this audit. No confirmed factual citation error was found in accessible primary material; the remote bibliographic entries remain unverified.

## Historical legal threshold chain

The recorded ceilings are arithmetically consistent with the project’s stated assumptions: annualise A = R1,350/R1,410 per month, impose D = 1.6A − 0.4B and a payable minimum D = R1,200 annually. Solving gives R61,800/R64,680, with double those levels for the recorded couple ceilings. This checks the arithmetic only. The original notices, the operative Annexure A/payment-formula regulation, the R100 boundary and the couple-resource provision have not been independently read. Rate-change notices alone should not be presented as a complete legal source for every resource-assessment rule.

## Citation order and unresolved governance

The current 25-entry map matches first use of stable source IDs and has no unused references. This mechanical check does not verify article content. Rebuild the map if new citations appear earlier in the manuscript.

No DUT ethics approval, exemption or determination was supplied or inferred; the paper must retain that limitation until an official record is available. The same applies to raw-data access/disclosure rules and final course/portal requirements. These checks can be completed by supplying the authentic studies/notices and institutional records or by reading them when primary-source access is available.

The machine-readable companion [`primary_source_audit.json`](primary_source_audit.json) lists every attempted URL, proxy status, claims to verify, stable-to-published citation mapping and document hashes. Failed publisher/government requests do not authenticate candidate URL paths. No downloaded public-source binaries were added to the repository.
