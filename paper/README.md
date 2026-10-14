# Revised Submission 2 manuscript

The revised IEEE draft is `Jawe_OPG_nonreceipt_KZN.docx` and
`Jawe_OPG_nonreceipt_KZN.pdf`. Its eight-page PDF integrates the approved
Submission 1 with the completed study, local Streamlit artefact and lecturer
feedback supplied on 11 October 2026. The original title and aim are restored;
the baseline Submission 1 PDF remains unchanged.
See `feedback_response.md` for all seven comments and remaining limitations.
This is a review draft; no institutional submission has been performed.

The current **14 October 2026** draft retains the user's accepted point 1 revision
to Section II.A and applies the three subsequent framework corrections. The
final subsection of Section II, **II.D Conceptual Framework**, connects the access
problem, administrative-burden theory, observable screening, predictors and
artefact. Figure 1 on page 3 distinguishes constructs, measurements, screening,
description and prediction; its dashed boundary identifies implementation scope,
not another causal factor. **VI.E** on page 8 returns to the framework and
distinguishes supported comparisons, the unexpected schooling result and
unresolved mechanisms. The specialist, clear professional style continues.

The manuscript has **5,423 whitespace tokens**, including a **141-word abstract**.
The PDF retains eight Letter pages, nine tables, four figures and 25 references,
with the existing fonts and build engine. All table cells and scientific results
remain unchanged; the conceptual figure has been revised. See
[the framework revision](conceptual_framework_revision.md),
[its validation](conceptual_framework_validation.json) and
[the staged supervisor response](supervisor_feedback_response.md). The theory
relationship in supervisor point 2 is now addressed; Table II formatting and
supervisor points 3–10 remain pending.

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
- `plain_language_revision.md`, `plain_language_validation.json`: the language
  history at commit `e70b300`, before the current professional rewrite. These
  records bind the earlier manuscript and do not establish participant usability.
- `plain_language_negative_controls.json`: four deliberate temporary errors
  rejected by the earlier claim verifier; retained as a historical record.
- `professional_language_revision.md`, `professional_language_validation.json`:
  the professional-language history at commit `17e1b05`; its earlier 90-term
  definition review has been superseded by the user's specialist-audience scope.
- `professional_language_negative_controls.json`: four deliberate temporary
  errors rejected for that historical manuscript.
- `specialist_language_revision.md`, `specialist_language_validation.json`:
  audience-fit and literature-continuity history at commit `e83b504`; the
  specialist writing policy continues in the current draft.
- `specialist_language_negative_controls.json`: four deliberate temporary
  errors rejected for that historical manuscript; not rerun for point 1.
- `supervisor_feedback_response.md`, `supervisor_point1_validation.json`:
  the staged supervisor response and historical first-point validation at
  commit `1fe4820`, before the accepted framework follow-up.
- `conceptual_framework_revision.md`, `conceptual_framework_validation.json`:
  the current three framework corrections, source/scope checks and retained
  scientific limits. `manuscript_validation.json` records the current artifacts.

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
numeric table values and 100 supporting comparisons against retained evidence.
Primary and independent reviewers visually inspected all eight freshly rendered
pages, including the revised conceptual figure. The paper contains nine tables,
four figures and 25 references numbered by first appearance. The previous
220-test application result is cited as existing evidence; editing the paper
has not rerun or expanded that suite.

The targeted revision strengthens the RQ discussion, links theory to findings,
explains screen/model sensitivity differences, and distinguishes ranking,
precision–recall, probability error and calibration. Its 314-row claim register
passes 209 table comparisons and 100 supporting checks after the language rewrite.
The retained **11 October** primary-source audit records three local authentic
Stats SA documents read and thirteen external requests refused by the outbound
proxy. That historical audit supplied no remote article or legal text; it has
not been rerun for the language or framework revisions. P5 remains partially
complete.

The manuscript separates person-weighted description, unweighted internal model
validation and frozen full-data application scores. Participant usability has
not been evaluated, as directed by the user; the Windows owner walkthrough is
functional evidence. Independent publisher/official-notice verification and the
institution's ethics determination still require confirmation before submission.
APRE402 is the final-paper module code confirmed by the user; PRIC401 remains in
the unchanged original Submission 1. The plan's deadline and other portal
requirements require confirmation from the actual submission brief.
