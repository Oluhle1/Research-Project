# Reference revision — 21 October 2026

This revision updates the main manuscript, not the proposed-solutions document.
The eight-page limit includes all sections and references. It does not include
the unchanged, separately supplied 11-page supplementary document.

| Requested correction | Outcome | Evidence |
| --- | --- | --- |
| Restore IEEE reference spacing | Completed. The canonical PDF uses unmodified IEEEtran V1.8b conference mode, with 8-point references on the class's 9-point baseline. The editable Word copy uses 8-point references with normal single spacing (`240 AUTO`), replacing compressed leading. | `ieee_template/`, `build_ieee_pdf.py`, `manuscript_validation.json` |
| Complete publisher/DOI and thesis checks | **Pending source access.** Every one of the 18 journal DOIs has a recorded Crossref/resolver/publisher attempt. No authoritative response was obtained. The Mabala report's resolver and Wits repository requests also failed. No fields can honestly be marked freshly verified from those requests. | `reference_verification.csv`, `reference_audit/` |
| Clarify Statistics South Africa dates, versions and access | Completed against three retained primary PDFs, with a documented limit on official website retrieval. The citations identify dated/undated works, stable project archive copies and the actual inspection date. The audit identifies exact copies by SHA-256. | `reference_audit/statistics_south_africa.json` |

## IEEE layout and content

The PDF uses the standard 10-point IEEE conference class with Letter paper;
body, table and reference font sizes remain 10, 9 and 8 points. No class,
geometry or line-spacing compression is applied. The documented
`IEEEtriggeratref{16}` command balances the final reference columns.
The Word document is an editable counterpart; its pagination was separately
checked using LibreOffice. Microsoft Word/font versions can paginate differently.

To fit normal reference spacing, repeated prose was shortened. The abstract,
Section III.B screening rules and Section III.D validation methods remain
byte-identical to the baseline. All nine source tables, four figure directives,
figure files, numerical results, recorded searches and supplementary evidence
remain unchanged. No models were refitted and no application tests were rerun.
The proposed-solutions document remains unchanged.

## Statistics South Africa source decisions

- Published reference [21] (stable ID 3): the metadata document prints
  **Statistical Release P0310 (2017)** and ISBN **978-0-621-45185-6**. The title
  identifies survey 2014/2015; **2017 is the publication year**, not the survey
  year. P0310 was confirmed rather than removed.
- Published reference [22] (stable ID 4): the standalone document is titled
  **Coicop codes**. It contains no printed publication year or numbered edition;
  it is cited as **n.d.** within its LCS supporting-document context. Its PDF
  creation timestamp is not treated as a publication date. The corporate-author
  attribution follows the supporting-release context, not a standalone imprint.
- Published reference [23] (stable ID 5): **Living Conditions Survey 2014/15:
  Household Questionnaire** has no printed publication date or version number;
  it is also **n.d.** The survey period is part of the title, not a claimed
  publication date.

All three citations link to exact project copies at Git commit
`110d84161ffb4ca1821c2c76318a6a13b27e2643`; their bytes match the retained
primary PDFs. “Inspected Oct. 21, 2026” records local document inspection.
It does not claim successful access to an official Stats SA or DataFirst
catalogue. No new publisher deep link, catalogue version or identifier was
invented. Hashes and pinpoint evidence appear in the source audit.

## Remaining publisher and thesis checks

The proxy returned CONNECT HTTP 403 before the source servers could respond.
This is an environment access restriction, not a publisher refusal or evidence
of invalid identifiers. General network permission was granted and a retry
still failed. Default certificate validation was retained.

The minimum domains needed are `api.crossref.org`, `doi.org`,
`hdl.handle.net` and `wiredspace.wits.ac.za`. Registry/publisher exports and the
Mabala repository record/title page can also supply the missing evidence.
For each journal entry, compare authors, title, journal, publication year,
volume/issue, pages/article number and DOI against the authoritative record.
For the thesis/report, confirm author, exact title, document type, institution,
degree/department where required, publication/submission date and persistent
identifier; distinguish a repository deposit date from the work's date.

Existing factual journal and thesis metadata were preserved. Only article-number
style was standardised to “Art. no.”. The six active legal references are carried
forward with their existing evidence; their provisions were not freshly reviewed
in this bibliography revision. No claim is made that article findings, ethics,
participant usability or all publication-readiness requirements have been verified.
