# Supervisor feedback point 7: model interpretation

Revision date: **15 October 2026**. Parent: `a9f91ea`. Series baseline:
`f9bab60378a9b01ce5d6153194720cd52c736253`.

> Section V.C (Model Interpretation): Further clarify the distinction between
> statistical associations, predictive performance and causal explanations.

**Status: revised in Section V.C, with one linking sentence in Section VI.B.
Awaiting user review.** No displayed result was changed. No model was refitted,
and the application suite was not rerun.

Section V.C is now headed "Predictive performance and associations." The
opening states that the section reports two different results. Predictive
performance uses one out-of-fold probability for each adult. Associations use
odds ratios from the model fitted to all 1,013 included adults. Neither result
explains why an adult reported non-receipt. The study did not test a
mechanism, a time order or an intervention.

Table VII and Figure 4 stay the predictive results. The prose names what AUC,
average precision, the Brier score and calibration summarise. It states that
those measures do not identify the separate contribution of age, sex,
schooling, settlement or office distance.

The odds ratios remain 0.39 (0.23–0.66) for women versus men and 0.24
(0.13–0.43) for schooling below Grade 7 versus Grade 7 or above. The prose
states that these come from another fit, the model trained on all included
adults with the other predictors in the same model. The Wald intervals
exponentiate that model's coefficients and standard errors. They are not the
Table VII resampling intervals. An odds ratio multiplies odds. It is not a
change in the probability of non-receipt and it is not a held-out performance
measure. Age, settlement and welfare-distance intervals still include 1. The
associations describe the fitted model. They do not establish that sex,
schooling, place or office distance produced non-receipt. The predictors are
proxies, the data are cross-sectional, and the screen selects the 1,013 adults.

Table VIII is identified as a set of predictive checks under a changed sample,
predictor or calculation. Those rows are not a second set of odds ratios, and
they do not establish a cause. Their displayed values are unchanged.

Section VI.B keeps the numeric reading of AUC, average precision, Brier score
and calibration. It adds that the full-sample odds ratios are associations, and
that held-out ranking, probability error and calibration do not convert them
into effects of sex, schooling, settlement or office distance.

The abstract is unchanged at **141 whitespace tokens**. The manuscript has
**6,796 whitespace tokens**. Tables, figures, screening rules, model code and
the builder were not changed. The Word export remains **nine Letter pages**.
Pages 6, 7 and 8 were inspected. Fresh checks passed **209 numerical and 103
supporting comparisons**, with zero failures, **317 claim-register rows** and
four documented limits. This PDF was exported from Microsoft Word with Times
New Roman. No independent second-reviewer pass is claimed. No screening rerun,
model refit, application-suite run, participant study or submission is claimed.

See [point 7 validation](supervisor_point7_validation.json),
[current manuscript validation](manuscript_validation.json),
[staged response](supervisor_feedback_response.md),
[PDF](Jawe_OPG_nonreceipt_KZN.pdf) and [Word](Jawe_OPG_nonreceipt_KZN.docx).

Points 3, 4, 5 and 6 remain as previously recorded and still await user review.
Points 8–10 remain pending.
