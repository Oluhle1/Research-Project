# Supervisor feedback point 6: results tables

Revision date: **15 October 2026**. Parent: `abec397`. Series baseline:
`f9bab60378a9b01ce5d6153194720cd52c736253`.

> Tables IV–VIII: Review the presentation of statistical results, improve
> table readability and ensure that uncertainty estimates and performance
> measures are interpreted appropriately.

**Status: revised in Sections V and VI and in the table layout. Awaiting user
review.** No displayed result was changed. No model was refitted, and the
application suite was not rerun.

Table IV is read as nested people counts. Adults aged 60 or older equal the
failed, unresolved and passed rows: 117 + 187 + 1,013. Reported receipt and
non-receipt divide the passed row: 946 + 67. Adding every people cell would
count the same adults more than once. Household cells are distinct counts and
do not follow that partition.

Table V states that each cell gives the unweighted figure and then the
person-weighted figure. Category percentages describe the composition of each
receipt group. They are not non-receipt rates and they are not predictions.
The table reports no standard errors, so the age, sex, schooling, settlement
and office contrasts are descriptions of the 946 and 67 adults. They are not
tests.

Table VI keeps the same nine rows and the same counts, rates and performance
values. The note defines each column. AUC, Brier and calibration slope are
unweighted out-of-fold point estimates, and the table gives them no intervals.
Held-out AUC in that table runs from 0.736 to 0.763. A close AUC does not make
the screened groups the same population and does not show which rule predicts
better. Same* repeats the S0 row for the scenarios that left the sample and
the measures unchanged. S1b and S1d remain different settings displayed on one
row because the saved counts and measures match.

Table VII keeps the five logistic estimates and their percentile intervals.
The logistic column is wide enough for each interval to sit on one line. The
intercept-only calibration-in-the-large remains .0001, and the note states
that no resampling interval was saved for it. Dashes remain exactly the
measures the intercept-only model does not supply. The note separates three
uncertainty calculations: the Section V.A survey approximation, the Table VII
household resampling of fixed predictions, and the Wald intervals from the
model fitted to all included adults. The resampling intervals are not
design-based confidence intervals.

Section VI.B reads the displayed intervals. The AUC interval 0.687–0.814 lies
above 0.5 for these fixed predictions and still describes ranking, not accuracy
at a cutoff. The average-precision interval 0.139–0.292 lies above the 6.61%
event rate and is not precision at one cutoff. The two Brier intervals
overlap, and no interval was calculated for the 0.0040 difference. The
calibration-in-the-large interval includes 0. The slope interval includes 1.

Table VIII keeps its six rows and its point estimates. It reports no intervals
for AUC, Brier or slope. In that table AUC runs from 0.750 to 0.763. The
lowest Brier is the complete-case row, on a smaller sample. The highest Brier
is the weighted-score row, which reuses the primary predictions. Those
differences do not rank the specifications. S9 remains a frequency-weighted
fit, not a full survey-design regression. S10 does not refit.

The abstract is unchanged at **141 whitespace tokens**. The manuscript has
**6,588 whitespace tokens**. Column widths for Tables V–VIII were adjusted so
the counts and intervals are not broken across lines. Reference leading was
not changed. The Word export remains **nine Letter pages**. The user deferred
the eight-page limit. Pages 5, 6 and 7 were inspected. Fresh checks passed
**209 numerical and 103 supporting comparisons**, with zero failures, **317
claim-register rows** and four documented limits. This PDF was exported from
Microsoft Word with Times New Roman. No independent second-reviewer pass is
claimed. No screening rerun, model refit, application-suite run, participant
study or submission is claimed.

See [point 6 validation](supervisor_point6_validation.json),
[current manuscript validation](manuscript_validation.json),
[staged response](supervisor_feedback_response.md),
[PDF](Jawe_OPG_nonreceipt_KZN.pdf) and [Word](Jawe_OPG_nonreceipt_KZN.docx).

Points 3, 4 and 5 remain as previously recorded and still await user review.
Points 7–10 remain pending.
