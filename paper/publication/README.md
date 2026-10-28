# Publication methodology extension

This branch follows the supervisor's validation comments while preserving the
submitted Honours paper at `e5fd403`. The original paper, screening rules,
cohort, application and production model remain unchanged. IST-Africa 2027 is
the target venue; this folder supplies technical evidence and author-review
material, not a completed conference-format submission.

## Completed validation

- Original four settlement categories retained in a seven-slope ridge model.
- Twenty repeated nested five-by-five validations grouped by household, plus
  twenty grouped by derived PSU, with training-only imputation and scaling.
- Penalty C selected using pooled inner held-out person-level Brier loss.
- Paired training-prevalence reference evaluated on identical outer test rows.
- One thousand whole-household bootstrap samples repeat preprocessing,
  tuning and final fitting. Original household copies stay together.
- All 48,040 inner and 1,201 final ridge fits converged. All 40 nested
  repetitions and 1,000 bootstrap draws were valid for Brier/AUC evaluation.
- Calibration slopes were available for 993/1,000 draws in each bootstrap,
  original-cohort and out-of-bag evaluation set. The seven unavailable diagnostic
  fits per set are recorded; they are not ridge-fit convergence failures.

The new reference household split gives AUC 0.749929, average precision
0.204861 and Brier 0.0576875, compared with 0.0617721 for the prevalence
reference. These results support a better-audited estimation procedure without
requiring the outcome-informed merger. They do not demonstrate superior
prediction over the original model, external validity or participant usability.

## Read and review

- `methodology_results.md`: findings, limitations and proposed methods/results
  wording for author review.
- `Jawe_Publication_Methodology_Revision.docx` and `.pdf`: readable review note.
- `methodology_protocol.md` and `validation_config.json`: recorded settings;
  the numerical design preceded the extension runs.
- `methodological_review.json`: independent numerical and scope checks.
- `../../output/publication_validation/run_record.json`: executed settings,
  fit counts, actual runtime, hashes and limitations.
- `venue_requirements.md`: sourced IST-Africa requirements and date discrepancy.
- `preparation_status.json`: an earlier preparation snapshot, made before the
  actual cohort runs; the run record describes the later completed work.

The original six-slope model remains exploratory. The unmerged ridge candidate
is a retrospective internal sensitivity analysis, not a production replacement
or independent confirmation. Repeated-partition ranges are not confidence
intervals. Bootstrap optimism-correction Monte Carlo errors quantify simulation
error, not sampling uncertainty. Nested CV and corrected apparent performance
concern different training-support settings and must be reported separately.

## Reproduce the extension

Use Python 3 with the actual recorded versions in
`analysis/requirements-publication.txt`, and the unchanged frozen cohort at
`output/phase3/cohort_person.csv`. The loader checks both the raw and
newline-normalised checksum. Preparing that cohort requires the original
provider-accessed data and the repository's documented preparation workflow;
survey rows are excluded from the review package.

```text
python -m unittest discover -s tests -p "test_publication*.py" -v
python analysis/run_publication_validation.py --jobs 4
```

The test command runs 22 focused safeguards. The second command writes only to
the new `output/publication_validation` directory. `--pilot` is restricted to
an output directory outside the repository. Optional `--qa-dir` must also be
outside the repository and contains controlled respondent-level arrays; it is
never part of the public review package.

Figures use those controlled arrays only to calculate five aggregate
calibration bins. They export no respondent-level predictions. The figure
manifest and independent review record bind the public diagnostics to the
validated results.

The review-note renderer additionally uses the document dependency in
`paper/requirements-docs.txt`. Run `python analysis/render_publication_note.py
--diagram` to rebuild the editable note and workflow diagram. Its PDF can be
exported using Word or LibreOffice. These review documents use their own
readable layout and do not claim to implement the conference template.

## Conference-paper work remaining

The supplied call specifies the updated IST-Africa template, 8–10 pages,
maximum 4,000 words, double-blind review and accurate AI-assistance disclosure.
The actual `.dot` template has not been supplied or inspected. The uploaded
brochure lists 31 October 2026 while the supplied webpage text gives an extended
20 November 2026 deadline; the current portal date needs confirmation.

The existing Honours paper therefore still needs a separate venue-format,
word-count and anonymity pass. This extension adds no new provinces, participant
study or recovered literature-screening register. Authors must review the
scientific interpretation and describe AI assistance accurately; the work here
includes technical code, methodological options, figures and draft review prose.
