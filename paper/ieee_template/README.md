# IEEE conference template provenance

The submission PDFs use the **unmodified IEEEtran.cls, 2015/08/26 version V1.8b**,
with `10pt,conference,letterpaper` options. It does not imitate IEEE geometry in a
different document class. The class supplies page dimensions, margins, columns,
title, abstract, index terms, headings, captions and bibliography typography.
No margins, column widths, baseline spacing, document font sizes, float spacing
or page geometry are overridden. Tables use the class's `small` size (9 points,
10-point baseline), three-point cell padding and ordinary `tabularx` wrapping.
Figures occupy one column at their original aspect ratio.

## Retrieval and exact file

- Retrieval: authenticated platform HTTPS Git proxy, read-only public Git clone.
- Repository: https://github.com/rstudio/rticles
- Commit: `accdfa39225570a8ad9b786fbb3077060d1e12a5`
- File: `inst/rmarkdown/templates/ieee/skeleton/IEEEtran.cls`
- Permanent source link: https://github.com/rstudio/rticles/blob/accdfa39225570a8ad9b786fbb3077060d1e12a5/inst/rmarkdown/templates/ieee/skeleton/IEEEtran.cls
- SHA-256: `a9d9562028ce6e8af1ea0b5740e435d04be3d6c745ca2a3c2979564274b44cea`
- Retrieved copy: `/workspace/research-validation/ieee-rticles-source/inst/rmarkdown/templates/ieee/skeleton/IEEEtran.cls`.

The file header credits the original contributors and Michael Shell (maintainer
of versions 1.3–1.8b), identifies the IEEE Transactions/conference purpose and
points to IEEE, CTAN and Michael Shell support sites. The mirror's
`resources/template.tex` retains the `bare_conf.tex` V1.4b, 2015/08/26 header,
license notice and standard conference-class guidance. The renderer does not
copy the Pandoc-specific mirror template or use its added configuration.

## License

The **class file's own license is the LaTeX Project Public License (LPPL),
version 1.3**, as stated in its retained header. Retain the complete class file,
all credits and contribution notices when vendoring it. This project does
not modify the class. Modified copies would need the renaming and notice
requirements stated in that header. The LPPL text is distributed with LaTeX;
the local installation has `/usr/share/texlive/texmf-dist/tex/latex/base/lppl.tex`.
License information: https://www.latex-project.org/lppl/.

## Access and scope limits

Direct HTTPS retrieval of the IEEE template landing page, two Word-template
URLs and the CTAN class URL failed with outbound-proxy HTTP 403 before origin
content was read. The class was therefore obtained from the identified public
RStudio/Posit mirror rather than directly from IEEE or CTAN. Its header/version
and bytes are recorded above; no claim is made that a current publisher-hosted
file was downloaded or compared byte for byte.

An exact target venue has not been supplied. The renderer uses ordinary IEEE
conference mode and US Letter as a declared default; it does not infer special
venue rules, Computer Society mode, review anonymisation, copyright notices,
submission IDs, page-number requirements or ethics approval.

## Rebuild

From the Research-Project repository root:

```text
python paper/build_ieee_pdf.py --output-dir .local/paper-ieee --compile
```

The optional `--publication` flag omits the student/module line only. No author
is anonymised and no email, ORCID or affiliation is invented. The generated
manifest binds the exact source, reference catalog, class and four figures to
each built PDF. The renderer does not edit any manuscript or run any analysis.

The current manuscript produces **eight Letter pages**, with the original nine
numbered tables, four figures and 29 references, plus the full-width Table S5
search record. The record uses the class's ordinary `footnotesize` (8-point text
with a 9-point baseline); existing body/table/reference typography is unchanged.
The current version uses natural column flow, without a manual
`--balance-at-reference` trigger. An inherited trigger can force an unnecessary
ninth page after inserting S5. No source text, font size, margin or line spacing
was compressed to fit the record. See [current validation](../manuscript_validation.json).
