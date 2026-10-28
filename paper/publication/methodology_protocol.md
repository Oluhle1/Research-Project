# Publication methodology protocol — 28 October 2026

**Status: AI-assisted technical proposal for author review. No new cohort
analysis has been executed.** OpenAI ChatGPT proposed the implementation options
below and assisted with prototype code. This document is not evidence that the
authors independently developed or approved this methodological design. The
supplied IST-Africa policy requires independent author development of the
scientific content and accurate disclosure of AI assistance. The authors'
research choices and policy alignment must be settled before this proposal is
used as the submitted paper's methodology.

## Status and scope

The Honours manuscript was submitted before this work. Commit
`e5fd40302cfcc2da120e2d727b98ae054edbfb80` preserves that paper, its
supplement, scientific code and results. This publication extension uses a
separate branch and new files. It neither changes the submitted paper nor
replaces the application's frozen model.

This plan is fixed before running the analyses described below. Earlier results
and all current KZN outcomes have already been inspected. The extension is
**retrospective methodological development with internal validation**, not a
prospectively registered or confirmatory study. Removing the operational need
for the outcome-informed D-052 merger does not erase that research history.

The author selected **IST-Africa 2027**, a conference, as the target venue.
The supplied call-for-papers URL is
http://www.ist-africa.org/conference2027/default.asp?page=c4p. Direct HTTP and
HTTPS retrievals were blocked in this environment. The author subsequently
supplied the current webpage text and the official two-page brochure. Both
specify the IST-Africa template, 8–10 pages and at most 4,000 words. The webpage
states an extended deadline of 20 November 2026; the brochure still states
31 October 2026. The current portal date requires confirmation. See
`venue_requirements.md` for the source distinctions. The contribution remains the
reproducible screening-to-analysis workflow. Classifier novelty, statutory
entitlement, causal administrative burden and demonstrated user benefit are
outside the available evidence.

## Frozen population and prediction target

Use the existing KZN age-60+ observable screen and resolved reported-receipt
outcome. The final cohort contains 1,013 adults, 67 non-receipt events, 827
households and 345 derived primary sampling units (PSUs). Neither the definition
of eligibility nor the denominator is selected using predictive performance.

Verify the cohort checksum, allowing only the already documented LF/CRLF
newline difference. Check unique household/person keys, binary outcome,
household nesting in PSU and positive person weights. Do not alter the source.

The primary predictive estimand is **unweighted person-average prediction error**
among these screened adults. Person weights continue to describe population
non-receipt in the existing descriptive analysis. A derived-PSU grouping check
addresses broader dependence; it does not recreate the unreleased survey strata.

## Fixed publication candidate

Use ridge logistic regression with five existing predictor groups and seven
slopes: age per decade above 60, female sex, schooling below Grade 7, urban
informal settlement, traditional settlement, rural formal settlement and office
distance at least 5 km or unavailable. Reference categories remain male,
Grade 7 or above, urban formal and distance below 5 km.

Keep the original four settlement categories. Never merge categories based on
events, convergence, outer-fold results or apparent improvement. Ridge handles
sparse categories through shrinkage. Do not add variables, balance classes,
search cutoffs, choose among models using outer-fold scores or infer causes
from coefficients. Income, grant receipt, derived screening labels, weights and
identifiers are excluded from the predictor matrix.

Within every relevant training set, impute age by its median and categorical
predictors by their mode, breaking ties by sorted code. Preserve existing
schooling and office-access mappings, treating unsupported codes as missing.
Then standardise the seven encoded slopes by training means and population
standard deviations; use one for a zero standard deviation. Validation values
and outcomes cannot influence these settings. The intercept is unpenalised.

Use `lbfgs`, at most 2,000 iterations and tolerance 1e-8. Select inverse penalty
C from `[0.01, 0.1, 0.3, 1, 3, 10, 30, 100]` by the **pooled inner held-out
person-level Brier score**, not the unweighted mean of fold scores. Exact ties
select the smaller C. A non-converged inner fit makes that C unavailable; log
all failures and stop a development attempt if none are available. Refit the
preprocessing and selected model on the entire applicable training set.

## Repeated nested validation

Use 20 fixed outer seeds, 201415–201434. Each repetition has five outer folds
and five inner folds for penalty selection inside each outer training set.
Sort households and stratify their allocation by whether any member reports
non-receipt. All adults from one household remain together at both levels.
Use inner seed `outer_seed + outer_fold_number` (fold numbers 1–5).

Each adult receives exactly one held-out probability per repetition. On the
same test adults, evaluate an intercept-only reference equal to the outer
training set's person-level event proportion. Report the paired difference
`Brier(reference) − Brier(ridge)`; positive values favour the candidate.

Report pooled AUC, average precision, Brier, log loss, calibration-in-the-large
and calibration slope. Use seed 201415 as the fixed reference partition, not
the best partition. Summarise the 20 repetitions by median, interquartile range
and range. They reuse participants: these summaries are **partition/refitting
sensitivity, not 20 independent studies or confidence intervals**.

Repeat the same nested procedure for the 20 seeds with the derived PSU as the
group at both levels. Never choose the preferred grouping from its scores.
Record support, C selection and every convergence outcome.

## Full-development household bootstrap

Use 1,000 fixed draws with seeds 730001–731000. Sample 827 original households
with replacement and retain every selected household's adults and multiplicity.
Reset row indices while preserving the original household grouping. All copies
of an original household must remain in one inner fold. A sample with fewer
than five event-containing or five non-event households is invalid; record it
without redrawing or substituting a favourable sample.

For each draw, repeat the complete development algorithm: inner grouped
validation, training-only imputation/scaling, C selection and final refitting.
Evaluate that fitted model on both its bootstrap sample and the original
cohort. Evaluation on the original cohort deliberately overlaps development
data and is used **only for optimism correction**, never as held-out evidence.

For Brier and AUC, calculate:

`corrected = apparent_original + mean(metric_on_original − metric_on_bootstrap)`.

The same paired correction applies to the baseline's Brier and to the Brier
improvement. Compute Monte Carlo standard errors of the mean correction from
the replicate corrections. These measure finite-bootstrap simulation error;
they are **not sampling standard errors or confidence intervals for predictive
performance**. Report failed/invalid draws, valid denominators, event counts,
unique-household support and C/convergence distributions.

Also retain out-of-bag (OOB) household metrics as a labelled diagnostic. OOB
samples vary in size, prevalence and number of events; their quantiles do not
constitute a confidence interval for nested-CV performance. Do not mechanically
optimism-correct average precision or calibration slopes/intercepts. Their
interpretation depends on prevalence and the evaluation target.

Back-transform coefficients to their original encoded units before describing
bootstrap variability or sign stability. Penalised coefficients and their
resampling distributions do not support the old ordinary model's Wald tests,
causal claims or claims of independent replication.

## Tests, reproducibility and publication outputs

Before execution, test training-only preprocessing, fixed category encoding,
household/PSU fold isolation, duplicate-household multiplicity and grouping,
pooled inner scoring, complete held-out coverage, paired baseline calculations,
optimism-correction signs and explicit invalid-draw accounting. Record actual
package versions rather than claiming the archived runtime has been recreated.

Save aggregate metrics, fold/tuning/convergence records, resampling summaries,
protocol/code/data hashes and a plain-language methodological report. Keep any
row-level QA predictions outside Git under controlled local permissions. Preserve
the submitted manuscript, source data, older outputs and production model.

Update a separate publication draft only after the new results pass numerical
and methodological review. Report improvements and adverse results equally.
Never describe this extension as external validation or as proof of usability.

## Remaining evidence needs

Independent population/period validation, direct burden measurement, a complete
statutory means test and participant evaluation require additional evidence.
Other provinces may support a later geographic test, but are not added here.
The original 55-source review lacks original exports and a complete item-level
screening register; modelling improvements cannot reconstruct those records.
Recover genuine author records or conduct a separately documented review update
if required by the target venue. No searches or usability study are invented.
