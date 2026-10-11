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

## Rebuild

From the repository root, using the project's Python environment with Matplotlib
and Node.js/npm:

```text
python paper/build_figures.py
python paper/build_expansion_figures.py
npm --prefix paper ci
npm --prefix paper run build
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

The manuscript separates person-weighted description, unweighted internal model
validation and frozen full-data application scores. Participant usability has
not been evaluated, as directed by the user; the Windows owner walkthrough is
functional evidence. Independent publisher/official-notice verification and the
institution's ethics determination still require confirmation before submission.
