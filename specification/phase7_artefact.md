# Phase 7: command-line artefact

**Date:** 2026-09-25  
**Command:** `python analysis/run_study.py`  
**Run folder:** `output/runs/primary/`

The command reads the three LCS files the primary analysis uses, builds the cohort, writes the RQ1 tables, and fits the held-out six-slope model. It does not open a review interface and it does not fit a random forest.

## What one run writes

| File | Contents |
| --- | --- |
| `cohort_person.csv` | Every KwaZulu-Natal person, with status, reason codes, and outcome |
| `cohort_flow.csv` | People and households at each step |
| `reason_frequencies.csv` | Reason codes in the age-60 frame |
| `rq1_estimate.csv` | Unweighted rate, weighted rate, and the sampling-unit approximation |
| `rq1_characteristics.csv` | Recipients and non-recipients on the model variables |
| `oof_predictions.csv` | Held-out probability, intercept-only probability, and fold id |
| `metrics.csv` | ROC area, average precision, Brier score, calibration |
| `calibration_plot.png` | Five quantile bins |
| `fold_support.csv` | People and events in each fold |
| `fold_coefficients.csv` | Training-fold coefficients |
| `fold_imputers.csv` | Training-fold medians and modes |
| `bootstrap_intervals.csv` | 1,000 household resamples of the fixed predictions |
| `run_record.json` | Rule version, model specification, seed, software versions, input and output checksums |

The active rule is `opg-kzn-primary-v1`. The model seed is 201415. The six slopes and their reference levels are in the run record.

## Check against the frozen results

The cohort file written by the command has SHA-256 `50c73c5ca88592dc426ae79f708dcc18cb057832fd2e00174a0257b4b1f6adc2`, the same hash as the Phase 3 freeze. The command stops if that hash differs.

The run reports 1,013 people in the final cohort, 67 non-recipients, an unweighted rate of 0.0661, a weighted rate of 0.0749, a ROC area of 0.752248, and a Brier score of 0.057780. Those match Phase 4 and Phase 5.

## A person can be read from the files

The run record stores one example. Household `237001150000006101`, person 1, passed the primary screen with reason codes `FLAG_CAREGIVER_CHILD_GRANT` and `PASS_PRIMARY`. The outcome is receipt (`Y = 0`). Fold 5 produced a held-out probability of 0.016. The same columns are on the files for every person.

## Second run

The command was run a second time. All 14 files in `output/runs/primary/`, including `run_record.json`, were byte-for-byte the same as the first run.
