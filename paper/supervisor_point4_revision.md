# Supervisor feedback point 4: model validation

Revision date: **15 October 2026**. Baseline: `f9bab60378a9b01ce5d6153194720cd52c736253`.

> Page 4, Section III.D (Model Validation): Provide additional methodological
> detail on household-grouped cross-validation, preprocessing and the
> limitations of the bootstrap confidence intervals.

**Status: revised in Section III.D and checked against the frozen outputs.
Awaiting user review.** No model was refitted.

The household-grouped validation paragraph now states the procedure. Households
are sorted, labelled by whether any member reported non-receipt, and assigned
by stratified five-fold cross-validation so that every adult from a household
stays in one fold. Seed 201415 fixes the division. The modelled group is 1,013
adults in 827 households, including 182 households with more than one modelled
adult and 6 households with both receipt and non-receipt. Each adult receives
one out-of-fold probability from a model trained without that household. The
held-out folds contain 199 to 207 adults and 12 to 14 non-recipients. The
intercept-only reference uses the training group's non-receipt rate.

The preprocessing paragraph states the training-fold rule. After skipped
questions are interpreted, each training fold supplies the fill-in for its
held-out adults. Schooling contrasts below Grade 7 with Grade 7 or above, and
office distance contrasts at least 5 km or unavailable with nearer than 5 km.
Other codes stay missing. Missing age, in decades above 60, uses the
training-fold median. A missing category uses the most frequent training-fold
code, or the smaller code when two codes tie. Eligibility, receipt and survey
weights are not filled and do not enter the model. Three recipients lack usable
schooling. Fourteen recipients and four non-recipients lack usable office
distance. Age, sex and settlement are already complete.

The bootstrap paragraph states what the intervals do and do not include.
Average precision, AUC, Brier score, calibration slope and
calibration-in-the-large are calculated on the pooled out-of-fold
probabilities. Calibration-in-the-large is an intercept correction with the
slope fixed at 1. The 95% limits are the 2.5 and 97.5 percentiles of 1,000
with-replacement household samples of those fixed predictions, using the same
seed and retaining every adult in a selected household. All 1,000 samples
contained both outcome classes. The samples do not repeat preprocessing, refit
the model or revisit Decision D-052. They omit a new split, fill-in and fit,
and they omit primary sampling units, unreleased strata and person weights.
They are not design-based confidence intervals.

Only Section III.D and the reference leading in the builder changed. Reference
lines are tighter so the added detail remains within eight Letter pages. Tables,
figures, results, screening rules, model code and the application are unchanged.
The manuscript has **5,635 whitespace tokens** and the unchanged **141-word
abstract**. Section III.D has **422 words** and the added validation detail is
on page 4. The PDF has **eight Letter pages**, nine tables, four figures and
28 references. Fresh checks passed **209 numerical and 103 supporting
comparisons**, with zero failures, **317 claim-register rows** and four
documented limits. This PDF was exported from Microsoft Word with Times New
Roman. No screening rerun, model refit, application-suite run, participant
study or submission is claimed.

See [point 4 validation](supervisor_point4_validation.json),
[current manuscript validation](manuscript_validation.json),
[staged response](supervisor_feedback_response.md),
[PDF](Jawe_OPG_nonreceipt_KZN.pdf) and [Word](Jawe_OPG_nonreceipt_KZN.docx).

Points 5–10 remain pending. Point 3 remains as previously recorded and still
awaits user review.
