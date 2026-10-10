# Phase 8: RQ3

**Date:** 2026-09-25  
**Script:** `analysis/phase8_evaluate.py`  
**Log:** `output/phase8/evaluation_log.csv`

## Answer to RQ3

The artefact reproduces the primary analysis, and its screening decisions match the decisions specified before the program is run. Twenty-six checks passed and none failed.

Correctness is the expected-versus-actual log. Income of R61,800 in November 2014 passes. One cent more fails. The same boundary holds at the April 2015 ceiling of R64,680. A couple whose private incomes sum to R123,600 passes, and one cent more fails. A married adult whose spouse is outside the household stays unresolved even when that adult’s own income is R200,000, so the single-person ceiling is not applied. An own disability grant fails the screen, and that failure is kept together with the missing-spouse reason. An own war-veterans grant fails. A caregiver child grant does not exclude the adult and does not count as OPG receipt. Grant-in-aid does not exclude. An unspecified OPG answer leaves the person out of the model. A consistent report of no grant is non-receipt. Current non-receipt stays non-receipt when earlier OPG income is positive, and the disagreement is stored as a flag. A missing income amount is not treated as zero. A completed no-to-all schedule is treated as zero.

Data integrity uses the run folder from the command. The cohort has no duplicate person key. The flow counts are 1,013 in the final cohort and 67 non-recipients. The example person in the run record matches both `cohort_person.csv` and `oof_predictions.csv`.

Leakage prevention: a column list that adds the outcome or OPG income is rejected. The matrix that is actually fit contains the six slopes only: age, sex, schooling, urban informal settlement, the combined traditional-or-rural contrast, and welfare-office access.

Reproducibility was checked by running `python analysis/run_study.py` twice. All 14 files in `output/runs/primary/`, including the run record, were byte-for-byte the same. The cohort hash is the Phase 3 hash.

Transparency: household `237001150000006101`, person 1, has status PASS, reasons `FLAG_CAREGIVER_CHILD_GRANT` and `PASS_PRIMARY`, outcome receipt, fold 5, and a held-out probability of 0.016. The rule version on that record is `opg-kzn-primary-v1`.

| Check group | Cases | Passed |
| --- | ---: | ---: |
| Income ceiling, including equality and one cent either side | 7 | 7 |
| Spouse missing, self-pointer, or spouse income missing | 3 | 3 |
| Disability grant, war-veterans grant, caregiver grant, grant-in-aid | 5 | 5 |
| Grant answer, including contradiction and receipt-period flag | 4 | 4 |
| Income schedule zero rule | 3 | 3 |
| Forbidden predictor rejected | 1 | 1 |
| Run-folder person and flow trace | 1 | 1 |
| Total | 26 | 26 |
