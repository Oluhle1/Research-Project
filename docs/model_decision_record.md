# Phase 0 model reconciliation record

Audit date: 2026-10-10. This document records the existing research results and the sources selected for the Streamlit implementation. It does not introduce a new model, refit the primary model, or change the scientific scripts.

## Primary model and source of truth

The retained primary model is the **unweighted logistic regression with six slopes and an intercept** in `analysis/phase5_model.py`. The integrated reproducible workflow is `analysis/run_study.py`, which imports that module and writes `output/runs/primary/`. Use that run folder for primary results displayed by the interface. Its metrics, calibration bins, validation folds, coefficients, imputers, and bootstrap intervals agree with the corresponding artifacts in `output/phase5/`, allowing numerical roundoff in CSV representations.

The authoritative methodological revision is decision **D-052** in `specification/decision_log.md`: merge traditional and rural-formal settlement into one contrast because the separate rural-formal coefficient was unsupported in one training fold. Decisions D-049 through D-051 specify reference levels, household stratification, and uncertainty settings. `specification/phase5_rq2.md`, `specification/phase7_artefact.md`, and `paper/results.md` describe the retained model and current interval set.

`phase5_completed_outputs/` contains another completed export of the same six-slope primary model, with a different bootstrap realization and complete-case validation partitions. It remains historical evidence and must not supply selected intervals while the rest of a display comes from the current CLI run. `output/phase5_original_7slope/` and `output/phase5/table_i_attempt/` retain the original seven-slope diagnostic run. They are not primary performance sources.

## Cohort, outcome, and predictor coding

The primary modeling cohort has **1,013 people, 67 reported non-receipt events, and 827 households**. The positive outcome is reported OPG non-receipt (`Y = 1`); receipt is `Y = 0`. The observed unweighted event prevalence is `0.06614017769002961`.

| Slope | Transformation | Reference |
| --- | --- | --- |
| `age_per_10` | `(age - 60) / 10` | Age 60 corresponds to zero |
| `sex_female` | Female, sex code `2` | Male, code `1` |
| `school_below` | Schooling below Grade 7 | Grade 7 or above |
| `settle_urban_informal` | Settlement code `2` | Urban formal, code `1` |
| `settle_traditional_or_rural` | Settlement code `4` or `5` | Urban formal, code `1` |
| `welfare_far` | Welfare office at least 5 km away or unavailable | Nearer than 5 km |

`analysis/phase5_model.py` explicitly constructs these six columns. Schooling and welfare classes come from `analysis/phase4_rq1.py`. The primary model does not include income, OPG receipt items, eligibility statuses, reason codes, or survey weights as predictors. It selects no classification threshold and performs no class balancing.

There are three missing/unassigned schooling values and 18 missing welfare values; age, sex, and settlement have no missing values in this cohort. Categorical imputation learns modes from each training fold only, with ties resolved by the smallest code sorted as text. Age imputation learns the training median. The outcome and screening fields are not imputed.

## Household validation

The existing model assigns five folds at household level. Household labels are positive when any member reports non-receipt. Households are sorted by identifier before a shuffled `StratifiedKFold` split using seed **201415**. Six households contain both outcomes. Every household remains within one validation fold.

| Validation fold | People | Households | Events | Non-events |
| --- | ---: | ---: | ---: | ---: |
| 1 | 205 | 166 | 14 | 191 |
| 2 | 202 | 166 | 13 | 189 |
| 3 | 200 | 165 | 14 | 186 |
| 4 | 199 | 165 | 12 | 187 |
| 5 | 207 | 165 | 14 | 193 |

Sources: `output/runs/primary/fold_support.csv`, `output/phase5/fold_support.csv`, and `analysis/phase5_model.py::assign_folds`. All 1,013 primary observations have a held-out prediction. Primary performance is computed from those predictions, not from a fit on the whole sample.

## Why the original seven-slope model is diagnostic

The original specification uses separate settlement indicators for traditional and rural formal, creating seven slopes. Rural formal contains **31 people and one event overall**. Fold-4 training contains 30 rural-formal people and zero events, because its single event is held out. The fold-4 rural-formal coefficient reaches approximately **-21.882332445878347**, and convergence is false. Original folds 1, 2, 3, and 5 converge; all five retained six-slope folds converge.

This is sparse outcome support/separation, rather than a significance-based predictor selection. Combining traditional and rural formal addresses the unsupported contrast while retaining the other proposed predictors.

Sources: `phase5_completed_outputs/categorical_support_by_training_fold.csv`, `output/phase5_original_7slope/fold_coefficients.csv`, `output/phase5/fold_coefficients.csv`, and decision D-052.

| Metric | Primary six slopes | Original seven slopes |
| --- | ---: | ---: |
| Prevalence | 0.06614017769002961 | 0.06614017769002961 |
| Average precision | 0.203224143682155 | 0.2012848210007042 |
| ROC AUC | 0.752248272380171 | 0.7391530718500521 |
| Brier score | 0.05777950123934818 | 0.05794573704005396 |
| Intercept-only Brier score | 0.06177210985746963 | 0.06177210985746963 |
| Calibration-in-the-large | 0.019536390686919782 | 0.014419591056857124 |
| Calibration slope | 0.836191031254337 | 0.6734396751247408 |

These values come from `output/runs/primary/metrics.csv` and `output/phase5_original_7slope/metrics.csv`. Tiny differences in the last digits of diagnostic exports reflect numerical representation; the seven-slope non-convergence remains material.

## Primary uncertainty intervals

Use `output/runs/primary/bootstrap_intervals.csv` for the primary display. It agrees with `output/phase5/bootstrap_intervals.csv` within floating-point roundoff. The interval method is the 95% percentile interval from **1,000 household resamples of the fixed out-of-fold predictions**, seed 201415. All 1,000 resamples are valid for each listed metric.

| Metric | 2.5th percentile | 97.5th percentile |
| --- | ---: | ---: |
| ROC AUC | 0.6869008628081367 | 0.8141743737809212 |
| Average precision | 0.1385531608498784 | 0.29214536276114955 |
| Brier score | 0.044824127691685985 | 0.0705597887081662 |
| Intercept-only Brier score | 0.04670850222678325 | 0.0758100842844614 |
| Calibration-in-the-large | -0.3160650777646731 | 0.2732381497609123 |
| Calibration slope | 0.5913277591051985 | 1.1327892908134007 |

These intervals do not refit the model within resamples, so they do not include the additional uncertainty from repeating model fitting. They are not a full survey-design uncertainty analysis.

### Reconciliation with the completed-output archive

`phase5_completed_outputs/revised_primary_bootstrap_intervals.csv` has the following historical intervals:

| Metric | 2.5th percentile | 97.5th percentile |
| --- | ---: | ---: |
| ROC AUC | 0.684871324234824 | 0.8105817758290982 |
| Average precision | 0.1317909409442341 | 0.30049519615056164 |
| Brier score | 0.04498826868335669 | 0.07060858679188618 |
| Intercept-only Brier score | 0.04779878885596403 | 0.0755624921489105 |
| Calibration-in-the-large | -0.2900152625200243 | 0.27779093495207724 |
| Calibration slope | 0.5924042502712156 | 1.093722253493088 |

A read-only comparison of `output/phase5/oof_predictions.csv` and `phase5_completed_outputs/revised_primary_oof_predictions.csv` established identical person-key sets, fold assignments, and outcomes. Key-aligned predicted probabilities differ by at most **2.220446049250313e-16**. Their row order differs. The current primary file has sorted household order; the archived file does not.

`analysis/phase5_model.py::bootstrap` builds its sampling array with `work["uqno"].drop_duplicates()`, retaining first-appearance household order. The same random seed maps draws to different households when that order changes. A read-only replay of 1,000 draws for each existing file reproduced its respective **AUC, average-precision, and Brier interval endpoints exactly**. This establishes why those endpoints differ without implying a different fitted primary model. Calibration endpoints were compared from the saved files; they were not separately replayed during this audit.

## Weighted metrics and complete-case sensitivity

The weighted primary row in `output/phase5/metrics.csv` evaluates the same unweighted-model predictions using person weights. These are **weighted metrics, not a weighted model fit**:

| Metric | Weighted primary summary |
| --- | ---: |
| Prevalence | 0.07487682625805854 |
| Average precision | 0.2217458247247804 |
| ROC AUC | 0.763483977984584 |
| Brier score | 0.06411137529513251 |
| Calibration-in-the-large | 0.0778183955421315 |
| Calibration slope | 0.9353219656218223 |

Phase 6 S10 repeats this weighted metric summary. Phase 6 S9 is a separate survey-weighted fitting sensitivity, using binomial frequency weights and unweighted held-out metrics. Keep those descriptions distinct.

Two complete-case exports share **992 people and 63 events**, but use different validation partitions:

| Metric | Current Phase 6 S7 | Completed-output archive |
| --- | ---: | ---: |
| ROC AUC | 0.7582995882242383 | 0.7574196524680916 |
| Average precision | 0.2114394789786256 | 0.20235123583113926 |
| Brier score | 0.05556148889369386 | 0.055664394429225446 |
| Calibration-in-the-large | -0.028663735487587994 | 0.019957435079865832 |
| Calibration slope | 0.8192830071819349 | 0.8110707062853004 |

The archived `complete_case_oof_predictions.csv` preserves the primary fold assignment for every retained person. Current `analysis/phase6_sensitivity.py::cross_validate` reassigns stratified household folds after removing incomplete observations, on the reduced set of 811 households. Both report convergence in all five folds. Prefer the current script-generated `output/phase6/model_sensitivity.csv` S7 row for the sensitivity display; label the archived version as an alternative partition if it is ever shown.

## Frozen-cohort checksum and line-ending compatibility

The pinned frozen cohort SHA-256 is:

`50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`

In the audited cloud checkout, both `output/phase3/cohort_person.csv` and `output/runs/primary/cohort_person.csv` used LF line endings and therefore had raw SHA-256:

`6edcc6e93eda3f0c58243a64ab3281513abc7a5222f2b2f8836d373c98cf4625`

A read-only byte transformation from LF to CRLF reproduced the pinned cohort checksum exactly. Likewise, `output/runs/primary/oof_predictions.csv` had raw LF checksum `50af25b9d440c8539b5d49b00ff141962ec869eec26e7bf147197eec8785d36a`; CRLF conversion reproduced its recorded checksum `721a466c23b28ec2b57b9930ad00643f3d85d4623d6438060d09356b8e55613c` exactly.

This is a byte-format compatibility issue with the frozen Windows-style CSV artifacts, not evidence of changed records. Keep the scientific checksum guard intact. Restore the established line-ending setup before executing the frozen pipeline, and preserve the tracked artifact format. Do not substitute a new expected checksum merely to make a check pass.

## Documentation cautions and implementation implications

- `analysis/phase5_model.py::model_matrix` still has a docstring saying seven slopes, but its explicit column list contains six.
- The model revision comment references D-050; the revision is D-052. D-050 concerns household fold stratification.
- `specification/phase5_rq2.md` says rural formal contains 30 people overall. The frozen cohort and completed diagnostics establish 31 overall, with 30 in fold-4 training.
- `analysis/phase5_model_original_7slope.py` retains `OUT = output/phase5`. Executing it directly can overwrite primary artifacts; it must not be used by the interface to generate primary outputs.
- `output/runs/primary/run_record.json` includes an `inspection` example with survey identifiers. Public downloads must use an explicit aggregate/metadata field selection that excludes person-level examples and identifiers.

The interface must describe the model as an internally validated research model for reported non-receipt among the screened cohort. Neither apparently eligible status nor a predicted non-receipt probability determines official legal eligibility or a grant decision. Full-sample coefficients remain apparent associations; they must not be presented as held-out performance or causal effects.

## Audit boundary

This Phase 0 audit read existing scripts and artifacts, checked key-aligned predictions, verified aggregate category counts, replayed existing AUC/AP/Brier bootstrap calculations in memory, and checked newline-dependent hashes. It did not change research code, refit primary models, regenerate output files, or implement inference. The next gate is the shared Streamlit data-loading and artifact-selection layer.
