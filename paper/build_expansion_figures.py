"""Draw additional manuscript figures from concepts and frozen aggregate counts.

No respondent-level data is read, no scientific output is changed, and no model
is fitted. Run with the project's Python environment from any working directory.
The cohort counts come only from output/runs/primary/cohort_flow.csv.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
FONT_SIZE = 16  # Approximately 8 pt when the 7-inch source is set at 3.5 inches.


def canvas(height: float):
    fig, ax = plt.subplots(figsize=(7, height))
    ax.set(xlim=(0, 7), ylim=(0, height))
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    return fig, ax


def box(ax, x, y, width, height, text, *, shade="#f5f5f5", dashed=False):
    patch = FancyBboxPatch(
        (x, y), width, height, boxstyle="round,pad=0.025",
        facecolor=shade, edgecolor="black", linewidth=1.1,
        linestyle="--" if dashed else "-",
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2, y + height / 2, text,
        ha="center", va="center", fontsize=FONT_SIZE, linespacing=1.08,
    )


def arrow(ax, start, end):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "black"},
    )


def line(ax, points):
    ax.plot(*zip(*points), color="black", lw=1.2, solid_capstyle="round")


def save(fig, stem):
    for extension in ("png", "svg"):
        path = OUT / f"{stem}.{extension}"
        fig.savefig(
            path, dpi=300, facecolor="white",
            metadata={"Date": None} if extension == "svg" else None,
        )
        if extension == "svg":
            # Keep generated SVG source clean without changing path geometry.
            path.write_text(
                "\n".join(row.rstrip() for row in path.read_text().splitlines())
                + "\n"
            )
    plt.close(fig)


def conceptual_framework():
    """Separate conceptual rationale from measures and analytical operations.

    Dashed arrows describe why predictors were selected, not measured causal
    paths. The artefact boundary implements the analytical design; it is not
    an explanatory variable. All figure content is conceptual, not new data.
    """
    fig, ax = canvas(7.5)

    def node(x, y, width, height, rows, *, shade="#f4f4f4", dashed=False):
        box(ax, x, y, width, height, "", shade=shade, dashed=dashed)
        # At the manuscript's half-size display, 16-point source text is 8 pt.
        top = y + height / 2 + .115 * (len(rows) - 1)
        for index, row in enumerate(rows):
            ax.text(
                x + width / 2, top - .23 * index, row,
                ha="center", va="center", fontsize=FONT_SIZE,
                fontweight="bold" if index == 0 else "normal",
            )

    def rationale(start, end):
        ax.annotate(
            "", xy=end, xytext=start,
            arrowprops={
                "arrowstyle": "->", "lw": 1.2, "color": "black",
                "linestyle": "--",
            },
        )

    node(.15, 7.03, 6.7, .32, ["Social problem: OPG non-receipt"], shade="white")
    rationale((3.5, 7.00), (3.5, 6.76))
    node(.15, 5.93, 6.7, .80, [
        "Theoretical constructs: administrative burden",
        "Learning, compliance and psychological costs",
        "Not directly measured in LCS",
    ], shade="#e8e8e8")

    ax.text(
        3.4, 5.72, "Observable measurements", ha="center", va="center",
        fontsize=FONT_SIZE, fontweight="bold",
    )
    node(.25, 4.56, 2.12, .96, [
        "Screen inputs", "Age, income,", "partnership,", "other grants",
    ], shade="white")
    node(2.53, 4.56, 1.96, .96, [
        "OPG response", "Reported OPG", "receipt answer",
    ], shade="white")
    node(4.61, 4.56, 2.25, .96, [
        "Predictors", "Age, sex, schooling", "Settlement and", "office distance",
    ], shade="white")
    rationale((5.735, 5.90), (5.735, 5.55))

    # Enclosure denotes implementation, not a downstream causal influence.
    boundary = FancyBboxPatch(
        (.15, .17), 6.7, 4.13, boxstyle="round,pad=0.025",
        facecolor="white", edgecolor="black", linewidth=1.1,
        linestyle="--", zorder=-1,
    )
    ax.add_patch(boundary)
    ax.text(
        5.57, 3.68, "Artefact\nimplementation", ha="center", va="center",
        fontsize=FONT_SIZE, fontweight="bold", linespacing=1.1,
    )

    node(.25, 3.19, 2.12, .94, [
        "Screen status", "PASS / FAIL /", "UNRESOLVED", "No legal decision",
    ])
    node(2.53, 3.19, 1.96, .94, [
        "PASS receipt", "Receipt /", "non-receipt /", "unresolved",
    ])
    arrow(ax, (1.31, 4.53), (1.31, 4.16))
    arrow(ax, (3.51, 4.53), (3.51, 4.16))

    node(.25, 2.48, 5.82, .55, [
        "Analysis cohort: PASS + resolved receipt",
        "FAIL / unresolved excluded and reported",
    ])
    arrow(ax, (1.31, 3.16), (1.31, 3.06))
    arrow(ax, (3.51, 3.16), (3.51, 3.06))

    node(.25, 1.04, 3.10, 1.05, [
        "Descriptive outcome", "Person-weighted rate of", "reported non-receipt",
    ])
    node(3.60, 1.04, 3.10, 1.05, [
        "Predictive workflow", "Unweighted logistic model", "Household-held-out tests",
        "Non-receipt probability",
    ])
    line(ax, [(3.16, 2.45), (3.16, 2.34), (1.80, 2.34)])
    arrow(ax, (1.80, 2.34), (1.80, 2.12))
    line(ax, [(3.16, 2.34), (5.15, 2.34)])
    arrow(ax, (5.15, 2.34), (5.15, 2.12))

    # Predictor data enter prediction, never the screening or receipt decision.
    line(ax, [(5.735, 4.53), (5.735, 4.43), (6.73, 4.43), (6.73, 2.30), (6.48, 2.30)])
    arrow(ax, (6.48, 2.30), (6.48, 2.12))

    ax.text(
        3.5, .60,
        "App: frozen full-data upload scores\n"
        "Separate from household-held-out tests\n"
        "Scores do not change screening or receipt",
        ha="center", va="center", fontsize=FONT_SIZE, linespacing=1.08,
    )
    save(fig, "conceptual_framework")


def cohort_flow():
    source = ROOT.parent / "output" / "runs" / "primary" / "cohort_flow.csv"
    with source.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    counts = {row["step"]: int(row["people"]) for row in rows}
    required = {
        "KZN sample", "Age missing", "Age under 60", "Age 60+",
        "Eligibility FAIL", "Eligibility UNRESOLVED", "Eligibility PASS",
        "Outcome unresolved", "Recipients", "Non-recipients",
        "Final analysis cohort",
    }
    if not required.issubset(counts):
        raise ValueError("Frozen cohort-flow aggregate is missing required steps.")
    if counts["KZN sample"] != sum(counts[key] for key in (
        "Age missing", "Age under 60", "Age 60+"
    )):
        raise ValueError("Age-frame counts do not sum to the frozen KZN sample.")
    if counts["Age 60+"] != sum(counts[key] for key in (
        "Eligibility FAIL", "Eligibility UNRESOLVED", "Eligibility PASS"
    )):
        raise ValueError("Screen classifications do not sum to the older-adult frame.")
    if counts["Final analysis cohort"] != counts["Recipients"] + counts["Non-recipients"]:
        raise ValueError("Receipt counts do not sum to the final analysis cohort.")
    if counts["Eligibility PASS"] != counts["Final analysis cohort"] + counts["Outcome unresolved"]:
        raise ValueError("Resolved and unresolved outcomes do not sum to PASS.")
    if counts["Age missing"] != 0 or counts["Outcome unresolved"] != 0:
        raise ValueError("This frozen-primary layout requires zero unresolved age/receipt.")

    def n(key):
        return f"{counts[key]:,}"

    fig, ax = canvas(5.4)
    box(ax, .15, 4.49, 6.7, .65,
        f"KwaZulu-Natal survey records\n{n('KZN sample')} people")
    box(ax, .15, 3.37, 3.15, .78,
        f"Age below 60: {n('Age under 60')}\nAge missing: {n('Age missing')}",
        shade="white")
    box(ax, 3.7, 3.37, 3.15, .78,
        f"Age 60 or older\n{n('Age 60+')} people")
    line(ax, [(3.5, 4.46), (3.5, 4.3), (1.725, 4.3)])
    arrow(ax, (1.725, 4.3), (1.725, 4.18))
    line(ax, [(3.5, 4.3), (5.275, 4.3)])
    arrow(ax, (5.275, 4.3), (5.275, 4.18))

    for x, status, key in (
        (.15, "FAIL", "Eligibility FAIL"),
        (2.45, "UNRESOLVED", "Eligibility UNRESOLVED"),
        (4.75, "PASS", "Eligibility PASS"),
    ):
        box(ax, x, 2.22, 2.1, .72, f"{status}\n{n(key)} people")
    line(ax, [(5.275, 3.34), (5.275, 3.14), (1.2, 3.14)])
    arrow(ax, (1.2, 3.14), (1.2, 2.97))
    arrow(ax, (3.5, 3.14), (3.5, 2.97))
    line(ax, [(5.275, 3.14), (5.8, 3.14)])
    arrow(ax, (5.8, 3.14), (5.8, 2.97))

    box(ax, 2.35, 1.05, 2.1, .75,
        f"Recipients\n{n('Recipients')} people")
    box(ax, 4.75, 1.05, 2.1, .75,
        f"Non-recipients\n{n('Non-recipients')} people")
    line(ax, [(5.8, 2.19), (5.8, 1.98), (3.4, 1.98)])
    arrow(ax, (3.4, 1.98), (3.4, 1.83))
    arrow(ax, (5.8, 1.98), (5.8, 1.83))
    box(ax, .15, .15, 6.7, .55,
        f"Final study group: {n('Final analysis cohort')}\n"
        f"PASS with unclear receipt: {n('Outcome unresolved')}",
        shade="white")
    save(fig, "cohort_flow")
    return counts


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Serif", "font.size": FONT_SIZE,
        "svg.fonttype": "none", "svg.hashsalt": "opg-submission-two-v1",
    })
    conceptual_framework()
    counts = cohort_flow()
    print(
        "Wrote conceptual_framework/cohort_flow PNG and SVG; "
        f"frozen cohort {counts['Final analysis cohort']:,} people / "
        f"{counts['Non-recipients']:,} reported non-receipt events."
    )


if __name__ == "__main__":
    main()
