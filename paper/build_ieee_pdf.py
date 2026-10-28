#!/usr/bin/env python3
"""Render the compact Markdown manuscript with unmodified IEEEtran conference defaults.

This renderer reads manuscript.md/references.json and existing PNG figures only.
It does not run an analysis, select results, fit a model or alter source files.
The required IEEEtran.cls is copied unchanged into the requested build directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


UNICODE = {
    "’": r"\textquoteright{}", "‘": r"\textquoteleft{}",
    "“": "``", "”": "''", "–": "--", "—": "---",
    "−": r"\ensuremath{-}", "×": r"\ensuremath{\times}",
    "≥": r"\ensuremath{\geq}", "≤": r"\ensuremath{\leq}",
    "Σ": r"\ensuremath{\Sigma}", "ᵢ": r"\textsubscript{i}",
    "≈": r"\ensuremath{\approx}", "→": r"\ensuremath{\rightarrow}",
}
SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+"))
SPECIAL = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
    "#": r"\#", "$": r"\$", "%": r"\%", "&": r"\&",
    "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}
CITATION = re.compile(r"\[(\d+)\](?:[–-]\[(\d+)\])?")
LINK = re.compile(r"https?://[^\s{}]+|(?<=doi: )10\.\d{4,9}/[^\s{}]+")


def escaped(text: str) -> str:
    """Escape literal prose while preserving readable Unicode mathematical signs."""
    parts = []
    for char in text:
        if char in SUPERSCRIPTS:
            parts.append(r"\textsuperscript{" + SUPERSCRIPTS[char] + "}")
        else:
            parts.append(UNICODE.get(char, SPECIAL.get(char, char)))
    return "".join(parts)


def inline(text: str, *, citations: bool = True) -> str:
    tokens = []
    pattern = re.compile(
        r"https?://[^\s{}]+|(?<=doi: )10\.\d{4,9}/[^\s{}]+"
        + (r"|\[\d+\](?:[–-]\[\d+\])?" if citations else "")
    )
    at = 0
    for match in pattern.finditer(text):
        tokens.append(escaped(text[at:match.start()]))
        value = match.group()
        citation = CITATION.fullmatch(value) if citations else None
        if citation:
            lo = int(citation[1])
            hi = int(citation[2]) if citation[2] else lo
            if hi < lo:
                raise ValueError("Reversed reference range")
            tokens.append(r"\cite{" + ",".join(f"ref{i}" for i in range(lo, hi + 1)) + "}")
        else:
            # Keep terminal prose punctuation outside the URL and use the body font.
            trail = "." if value.endswith(".") else ""
            value = value[:-1] if trail else value
            tokens.append(r"\url{" + value + "}" + trail)
        at = match.end()
    tokens.append(escaped(text[at:]))
    return "".join(tokens)


def reference_text(entry: str) -> str:
    """Italicise periodical names and et al.; preserve the supplied reference text."""
    volume = entry.find(", vol. ")
    marker = ',” '
    title = entry.rfind(marker, 0, volume) if volume >= 0 else -1
    if volume >= 0 and title >= 0:
        journal = title + len(marker)
        result = (inline(entry[:journal], citations=False)
                  + r"\emph{" + inline(entry[journal:volume], citations=False) + "}"
                  + inline(entry[volume:], citations=False))
    else:
        result = inline(entry, citations=False)
    return result.replace("et al.", r"\emph{et al.}")


def search_record(caption: str, headers: list[str], rows: list[list[str]], notes: list[str] | None = None) -> str:
    """Unnumbered search grid. It must not change the numbering of Tables I–IX."""
    if headers != ["Search", "Source", "Hits", "Kept", "Query"]:
        raise ValueError("Unexpected search-record columns")
    if any(len(row) != 5 for row in rows):
        raise ValueError("Inconsistent search-record row")
    body = [r"\begin{table*}[!t]", r"\centering\footnotesize",
            r"\textit{" + inline(caption) + r"}\par",
            r"\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}X@{}}", r"\hline"]
    for search, source, hits, kept, query in rows:
        hit_label = "hit" if hits == "1" else "hits"
        label = f"{search} — {source} ({hits} {hit_label}; {kept} retained): "
        body.append(r"\textbf{" + inline(label) + "}" + inline(query) + r" \\")
    body.extend([r"\hline", r"\end{tabularx}"])
    for note in notes or []:
        body.append(r"\par\noindent\textit{" + inline(note) + "}")
    body.extend([r"\end{table*}", ""])
    return "\n".join(body)


def table(caption: str, headers: list[str], rows: list[list[str]], notes: list[str]) -> str:
    n = len(headers)
    descriptive = n == 5 and headers[0] == "Characteristic"
    if any(len(row) != n for row in rows):
        raise ValueError("Inconsistent table column count")
    if descriptive:
        weights = [1.25, 1.04, .835, 1.04, .835]
    elif n == 7:
        weights = [.8, 1.35, .95, .95, .9, 1.1, .95]
    elif n == 6:
        weights = [1.35, 1.2, .85, .85, .9, .85]
    elif headers[0] == "Predictor":
        weights = [.60, 1.10, 1.30]
    elif headers[0] == "Study":
        weights = [.75, .95, 1.30]
    elif headers[0] == "Characteristic":
        weights = [1.10, .95, .95]
    elif headers[0] == "Metric":
        weights = [.95, 1.15, .90]
    else:
        weights = [1.0] * n
    if abs(sum(weights) - n) > 1e-9:
        raise ValueError("Table column weights must sum to the number of columns")
    spec = "".join(
        r">{\hsize=" + str(weight) + r"\hsize\linewidth=\hsize\raggedright\arraybackslash}X"
        for weight in weights
    )
    caption = re.sub(r"^Table\s+[IVXLCDM]+\.\s*", "", caption)
    # Three-point cell padding makes seven-column tables readable at an unchanged
    # nine-point font; no table is scaled, squeezed or converted to an image.
    out = [r"\begin{table}[!t]", r"\caption{" + inline(caption) + "}",
           r"\centering", r"\small", r"\setlength{\tabcolsep}{3pt}",
           r"\begin{tabularx}{\columnwidth}{" + spec + "}", r"\hline"]
    if descriptive:
        recipient = re.fullmatch(r"Recipients, unweighted \(N = (\d+)\)", headers[1])
        nonrecipient = re.fullmatch(r"Non-recipients, unweighted \(N = (\d+)\)", headers[3])
        if (not recipient or not nonrecipient or headers[2] != "Recipients, weighted"
                or headers[4] != "Non-recipients, weighted"):
            raise ValueError("Unexpected descriptive-table columns")
        out.append(
            r" & \multicolumn{2}{c}{\textbf{\shortstack{Recipients\\N = "
            + recipient[1] + r"}}} & \multicolumn{2}{c}{\textbf{\shortstack{Non-recipients\\N = "
            + nonrecipient[1] + r"}}} \\")
        labels = ["Characteristic", "Unweighted", "Weighted", "Unweighted", "Weighted"]
        out.append(" & ".join(r"\textbf{" + inline(v) + "}" for v in labels) + r" \\")
    else:
        out.append(" & ".join(r"\textbf{" + inline(v) + "}" for v in headers) + r" \\")
    out.append(r"\hline")
    for row in rows:
        out.append(" & ".join(inline(v) for v in row) + r" \\")
    out.extend([r"\hline", r"\end{tabularx}"])
    for note in notes:
        out.append(r"\par\noindent{\footnotesize\textit{" + inline(note) + r"}\par}")
    out.append(r"\end{table}")
    return "\n".join(out)


def build(paper_dir: Path, output_dir: Path, class_file: Path, publication: bool,
          balance_at_reference: int | None = None) -> tuple[Path, dict]:
    source_path = paper_dir / "manuscript.md"
    references_path = paper_dir / "references.json"
    source_bytes = source_path.read_bytes()
    references_bytes = references_path.read_bytes()
    source = source_bytes.decode("utf-8")
    references = json.loads(references_bytes)
    ids = []
    for match in CITATION.finditer(source):
        lo, hi = int(match[1]), int(match[2] or match[1])
        if hi < lo:
            raise ValueError("Reversed reference range")
        for value in range(lo, hi + 1):
            if str(value) not in references:
                raise ValueError(f"Missing reference {value}")
            if value not in ids:
                ids.append(value)
    lines = source.strip().splitlines()
    if not lines[0].startswith("# "):
        raise ValueError("Expected manuscript title")
    title = lines[0][2:]
    first_section = next(i for i, line in enumerate(lines) if line.startswith("## "))
    preamble = [line for line in lines[1:first_section] if line.strip()]
    abstract = next(line.removeprefix("Abstract—") for line in preamble if line.startswith("Abstract—"))
    keywords = next(line.removeprefix("Keywords—") for line in preamble if line.startswith("Keywords—"))
    author_lines = [line for line in preamble if not line.startswith(("Abstract—", "Keywords—"))]
    if publication:
        author_lines = [line for line in author_lines if not re.search(r"Honours|APRE402|21634436", line)]
    author = author_lines[0]
    affiliation = r"\\".join(escaped(line) for line in author_lines[1:])
    out = [
        "% Generated from manuscript.md; IEEEtran.cls is unmodified.",
        r"\documentclass[10pt,conference,letterpaper]{IEEEtran}",
        r"\usepackage[T1]{fontenc}", r"\usepackage[utf8]{inputenc}",
        r"\usepackage{textcomp}", r"\usepackage{graphicx}",
        r"\usepackage{array,tabularx}", r"\usepackage{cite}",
        r"\usepackage{placeins}",
        r"\usepackage{url}", r"\urlstyle{same}",
        r"\title{" + escaped(title) + "}",
        r"\author{\IEEEauthorblockN{" + escaped(author) + "}"
        + r"\IEEEauthorblockA{" + affiliation + "}}",
        r"\begin{document}", r"\maketitle",
        r"\begin{abstract}" + inline(abstract) + r"\end{abstract}",
        r"\begin{IEEEkeywords}" + inline(keywords) + r"\end{IEEEkeywords}",
    ]
    figures = []
    tables = 0
    search_records = 0
    i = first_section
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line.startswith("## "):
            section = re.sub(r"^[IVXLCDM]+\.\s*", "", line[3:])
            out.append(r"\section{" + escaped(section) + "}")
        elif line.startswith("### "):
            section = re.sub(r"^[A-Z]\.\s*", "", line[4:])
            out.append(r"\subsection{" + escaped(section) + "}")
        elif line.startswith("RECORD: "):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append([part.strip() for part in lines[i].split("|")[1:-1]])
                i += 1
            if len(table_lines) < 2 or not all(re.fullmatch(r":?-+:?", cell) for cell in table_lines[1]):
                raise ValueError("Malformed search-record table")
            notes = []
            lookahead = i
            while lookahead < len(lines) and not lines[lookahead].strip():
                lookahead += 1
            if lookahead < len(lines) and lines[lookahead].startswith("NOTE: "):
                notes.append(lines[lookahead][6:])
                i = lookahead + 1
            out.append(search_record(line[8:], table_lines[0], table_lines[2:], notes))
            search_records += 1
        elif line.startswith("TABLE: "):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append([part.strip() for part in lines[i].split("|")[1:-1]])
                i += 1
            if len(table_lines) < 2 or not all(re.fullmatch(r":?-+:?", cell) for cell in table_lines[1]):
                raise ValueError("Malformed Markdown table")
            notes = []
            lookahead = i
            while lookahead < len(lines) and not lines[lookahead].strip():
                lookahead += 1
            if lookahead < len(lines) and lines[lookahead].startswith("NOTE: "):
                notes.append(lines[lookahead][6:])
                i = lookahead + 1
            out.append(table(line[7:], table_lines[0], table_lines[2:], notes))
            tables += 1
        elif line.startswith("FIGURE: "):
            file, caption = line[8:].split(" | ", 1)
            figure_relative = Path(file)
            if figure_relative.is_absolute() or ".." in figure_relative.parts:
                raise ValueError("Figure paths must stay inside the paper directory")
            figure = (paper_dir / figure_relative).resolve()
            if not figure.is_file():
                raise ValueError(f"Missing figure {file}")
            caption = re.sub(r"^Fig\.\s*\d+\.\s*", "", caption)
            out.extend([r"\begin{figure}[!t]", r"\centering",
                        r"\includegraphics[width=\columnwidth]{\detokenize{" + figure_relative.as_posix() + "}}",
                        r"\caption{" + inline(caption) + "}", r"\end{figure}"])
            figures.append((file, figure))
        elif line.startswith("NOTE: "):
            out.extend([r"{\footnotesize\textit{" + inline(line[6:]) + r"}\par}", ""])
        else:
            out.extend([inline(line), ""])
    out.append(r"\FloatBarrier")
    if balance_at_reference is not None:
        if not 1 < balance_at_reference <= len(ids):
            raise ValueError("Column balance reference must be a published reference number from 2 onwards")
        # Documented IEEEtran mechanism for manually balancing the last page.
        # This starts a new column; it does not compress bibliography spacing.
        out.append(r"\IEEEtriggeratref{" + str(balance_at_reference) + "}")
    out.append(r"\begin{thebibliography}{" + str(len(ids)) + "}")
    for value in ids:
        out.append(r"\bibitem{ref" + str(value) + "}" + reference_text(references[str(value)]))
    out.extend([r"\end{thebibliography}", r"\end{document}", ""])
    output_dir.mkdir(parents=True, exist_ok=True)
    for file, figure in figures:
        figure_target = output_dir / file
        figure_target.parent.mkdir(parents=True, exist_ok=True)
        if figure.resolve() != figure_target.resolve():
            shutil.copyfile(figure, figure_target)
    class_target = output_dir / "IEEEtran.cls"
    if class_file.resolve() != class_target.resolve():
        shutil.copyfile(class_file, class_target)
    tex_path = output_dir / "Jawe_OPG_nonreceipt_KZN.tex"
    tex_path.write_text("\n".join(out), encoding="utf-8")
    sha = lambda data: hashlib.sha256(data).hexdigest()
    manifest = {
        "source_sha256": sha(source_bytes), "references_sha256": sha(references_bytes),
        "class_sha256": sha(class_target.read_bytes()),
        "class": "IEEEtran 2015/08/26 V1.8b, unmodified",
        "options": ["10pt", "conference", "letterpaper"],
        "source_words": len(source.split()), "tables": tables,
        "unnumbered_search_records": search_records,
        "search_record_font": "IEEEtran footnotesize:8pt/9pt; full-width record",
        "figures": {file: sha(path.read_bytes()) for file, path in figures},
        "reference_source_ids_in_order": ids,
        "student_course_line_omitted": publication,
        "column_balance_trigger_at_published_reference": balance_at_reference,
        "float_barrier_before_references": True,
        "portable_tex_uses_copied_figures_and_class": True,
        "no_geometry_font_scale_or_vertical_spacing_overrides": True,
        "table_font": "IEEEtran small: 9pt / 10pt baseline; three-point cell padding",
    }
    return tex_path, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-dir", type=Path, default=Path.cwd() / "paper")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--class-file", type=Path,
                        default=Path(__file__).resolve().parent / "ieee_template" / "IEEEtran.cls")
    parser.add_argument("--publication", action="store_true", help="Omit student/module line only")
    parser.add_argument("--balance-at-reference", type=int, help="IEEEtran's documented last-page column break before published reference N")
    parser.add_argument("--compile", action="store_true", help="Run pdflatex twice")
    args = parser.parse_args()
    tex, manifest = build(args.paper_dir.resolve(), args.output_dir.resolve(),
                          args.class_file.resolve(), args.publication, args.balance_at_reference)
    if args.compile:
        for run in range(2):
            result = subprocess.run(
                ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", tex.name], cwd=tex.parent, capture_output=True, text=True,
            )
            (tex.parent / f"pdflatex-pass-{run + 1}.txt").write_text(result.stdout + result.stderr)
            if result.returncode:
                raise SystemExit(f"pdflatex pass {run + 1} failed; see {tex.parent}/pdflatex-pass-{run + 1}.txt")
        pdf = tex.with_suffix(".pdf")
        manifest["pdf_sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()
    (tex.parent / "ieee_pdf_build_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"tex": str(tex), "compiled": args.compile, **manifest}, indent=2))


if __name__ == "__main__":
    main()
