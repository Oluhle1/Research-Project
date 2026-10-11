# Revised Submission 2 manuscript

The revised IEEE draft is `Jawe_OPG_nonreceipt_KZN.docx` and
`Jawe_OPG_nonreceipt_KZN.pdf`. Its eight-page PDF integrates the approved
Submission 1 with the completed study, local Streamlit artefact and lecturer
feedback supplied on 11 October 2026. The original title and aim are restored;
the baseline Submission 1 PDF remains unchanged.
See `feedback_response.md` for all seven comments and remaining limitations.
This is a review draft; no institutional submission has been performed.

## Editable sources

- `manuscript.md`: compact manuscript consumed by the build.
- `conceptual_framework.md`, `results.md`, `discussion.md`: detailed working
  sections and evidence provenance. They support the compact manuscript; the
  builder does not automatically incorporate future changes to these files.
- `references.json`: existing source identifiers, reconciled with Submission 1.
- `manuscript_numbered.md`: generated readable copy using published citation
  numbers; `citation_map.json` maps source identifiers to first-appearance IEEE
  numbers. Edit `manuscript.md`, rather than this generated copy.
- `build_figures.py`: architecture diagram and calibration figure. It reads only
  the frozen aggregate calibration bins; it does not fit or recompute a model.
- `build_expansion_figures.py`: conceptual framework and observed cohort-flow
  diagrams; cohort counts come from the frozen aggregate flow CSV.
- `submission1_integration_notes.md`: source comparison and provenance,
  including the distinction between the proposal's reported review counts and
  a newly conducted review.
- `expansion_empirical.md`, `empirical_expansion_validation.json`: detailed
  descriptive/performance additions and the 209-value numerical audit.
- `targeted_revision_plan.md`, `targeted_revision_response.md`: the supplied
  improvement plan and the evidence-linked response to its five priorities.
- `claim_source_register.csv`, `claim_source_validation.json`, `verify_claims.py`:
  claim provenance, saved verification results and a reusable read-only check
  against the retained outputs. Prior application test runs remain historical
  evidence; this manuscript check does not refit or rerun the application suite.
- `primary_source_audit.md`, `primary_source_audit.json`: source-specific checks,
  local primary-document evidence and recorded remote-access limits. A matching
  submitted reference is distinguished from independently reading its source.

## Rebuild

From the repository root, using the project's Python environment with Matplotlib
and Node.js/npm:

```text
python paper/build_figures.py
python paper/build_expansion_figures.py
npm --prefix paper ci
npm --prefix paper run build
```

Recheck the numerical claims and regenerate their local evidence register:

```text
python paper/verify_claims.py --write
```

The pinned npm lockfile supplies `docx` 9.6.1. Output paths resolve relative to
these scripts rather than a particular user's Windows home directory.

Export to PDF using LibreOffice's `soffice` executable on PATH:

```text
soffice --headless --convert-to pdf --outdir paper paper/Jawe_OPG_nonreceipt_KZN.docx
```

Alternatively, open the DOCX in Microsoft Word and export to PDF. Pagination can
differ with fonts and renderer versions; inspect the exported PDF and retain the
maximum-eight-page requirement. The checked PDF was rendered with LibreOffice
26.8 on Linux, Times New Roman falling back to Liberation Serif, with Letter
paper, two columns, 10-point body text, 9-point tables and 8-point references.

## Validation and limits

`manuscript_validation.json` records the checked artifact hashes, page limit,
citation checks and frozen-source protection. Independent review verified 209
numeric table values against frozen CSV outputs and visually inspected all eight
pages. The expanded paper contains nine tables, four figures and 25 references
numbered by first appearance. The previous
220-test application result is cited as existing evidence; editing the paper
has not rerun or expanded that suite.

The targeted revision strengthens the RQ discussion, links theory to findings,
explains screen/model sensitivity differences, and distinguishes ranking,
precision–recall, probability error and calibration. Its 314-row claim register
passes 209 table comparisons and 100 supporting checks. Three local authentic
Stats SA documents were read; thirteen external source requests were refused
by the outbound proxy. Those retrievals supplied no original article or legal
text, so the response matrix records P5 as partially complete.

The manuscript separates person-weighted description, unweighted internal model
validation and frozen full-data application scores. Participant usability has
not been evaluated, as directed by the user; the Windows owner walkthrough is
functional evidence. Independent publisher/official-notice verification and the
institution's ethics determination still require confirmation before submission.
APRE402 is the final-paper module code confirmed by the user; PRIC401 remains in
the unchanged original Submission 1. The plan's deadline and other portal
requirements require confirmation from the actual submission brief.
