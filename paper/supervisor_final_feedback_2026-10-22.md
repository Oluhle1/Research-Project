# Supervisor feedback response — 22 October 2026

The main paper was revised only at the six locations identified in `Jawe FEEDBACK.pdf`.
Its structure, headings, abstract, literature review, screening rules, other eight
tables, four figures, estimator, numerical results and unrelated paragraphs are
preserved. The native IEEE PDF and Word export remain **eight Letter pages**.

| Point | Change in the main paper | Status |
| --- | --- | --- |
| 1. Outcome-informed settlement merging | III.D explicitly retains the ordinary merged model as an **exploratory primary reference** conditional on D-052. Household-held-out testing does not validate the complete selection process; ridge comparisons do not remove that selection uncertainty or establish equivalent/superior codings. The supervisor's qualification option was used, preserving the estimator and results. | Addressed |
| 2. Bootstrap versus repeated refits | III.D distinguishes the conditional 95% intervals from fixed-prediction household bootstrap samples from the separate 20 repeated-refit sensitivity distributions. Medians, interquartile ranges and ranges across repeated splits are not confidence intervals or independent coding validation. | Addressed |
| 3. Coefficient interpretation | V.C labels full-sample odds ratios exploratory and explains sparse-data/Wald instability with 67 events and six slopes, omitted coding uncertainty and overlapping training fits. Existing odds ratios, intervals and repeated-fit results are preserved. | Addressed |
| 4. Grouped sensitivity scenarios | Table VI lists all **16 scenario IDs separately**, replacing `S1b,d` and `Same*`. Seven columns and every numerical result are preserved. Notes distinguish refitted changed cohorts from unchanged cohorts that reused predictions; matching results do not imply equivalent rules. | Addressed |
| 5. Ethics, access and repository release | VII now records the supervisor's advice supplied by the author: formal clearance was not required for existing anonymised secondary data, with no direct human participation or primary collection. It acknowledges Stats SA and DataFirst and the author's own processing, and retains data-use/confidentiality obligations. No committee letter/reference number was invented. | Ethics explanation addressed; redistribution permission remains unconfirmed |
| 6. Official sources and document release | References [21]–[23] now cite the original documents without GitHub archive URLs. [21] uses the DataFirst catalogue record supplied by the author. The metadata's own page 2 states public availability on the Stats SA website. The other supporting documents remain undated, without fabricated official download links or release terms. | Citations corrected; full provider/release verification remains pending |

## Ethics and access evidence

The author supplied the supervisor's guidance in this conversation on 22 October
2026. That guidance states that formal clearance is not required because this
study uses existing secondary LCS 2014/2015 data without direct interaction with
human participants or primary data collection. It requests a clear anonymised
secondary-data statement, appropriate acknowledgement/citation, and observance
of data-use and confidentiality conditions. The revised paragraph reflects that
guidance; it does not claim a research-ethics committee certificate.

The author identified this provider record as the dataset source:
https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/608#study_desc1684331430702

The metadata PDF, page 2, states that the report is available on the Stats SA
website and permits application of information with source acknowledgement and
attribution of the user's own processing. This supports the metadata's public
publication status. It does not establish blanket rights to redistribute survey
records or every supporting document through GitHub.

Eight legitimate official-site/catalogue/documentation requests were refused by
the environment proxy with CONNECT HTTP403 before origin content was obtained.
The exact provider link came from the author; its page content, file listings and
licence terms were not independently retrieved. No successful website access
date, direct PDF URL or redistribution authorisation was invented. The remaining
confirmations require the actual applicable provider terms or authorisation.
[The request record](supervisor_official_source_attempts_2026-10-22.json) records
successful and unsuccessful evidence separately.

## Scope and verification

A comparison with commit `58c4da0a87fe66396de5726fc16ad294d866cca7` confirms
that every part of the main source outside the five authorised text/table blocks
is byte-identical. Only reference catalogue entries 3, 4 and 5 changed; published
numbers remain 21, 22 and 23. All headings, citation order and figures are preserved.
The other eight tables retain identical source and Word-cell text. Table VI's
16 scenarios passed **112 numerical comparisons** with retained outputs.
No models, data, analysis, application, tests, document builders, supplementary
material, earlier proposed-solutions document or README were changed.

Independent read-only reviewers checked the methods corrections and the strict
scope, pagination and rendered layout. Both paper renders remain eight pages;
Table VI and the references are readable. A relocated build of the portable TeX
source reproduces the native PDF text. Detailed checks and current file hashes
are in [manuscript validation](manuscript_validation.json).
