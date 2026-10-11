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
    fig, ax = canvas(6.8)
    box(
        ax, .15, 5.65, 6.7, .98,
        "Administrative-burden theory\n"
        "Learning, compliance and psychological costs\n"
        "Literature informs proxies; costs not measured",
    )
    box(
        ax, .15, 4.62, 6.7, .68,
        "Candidate circumstances: age, sex, schooling,\n"
        "settlement and welfare-office distance",
    )
    arrow(ax, (3.5, 5.62), (3.5, 5.33))

    # Legal entitlement remains outside the observable research workflow.
    box(
        ax, .15, 3.32, 2.28, .95,
        "Legal entitlement\nNot fully observed\nNo legal decision",
        shade="white", dashed=True,
    )
    box(
        ax, 2.55, 3.32, 4.3, .95,
        "Observable research screen\n"
        "Age, income, partnership,\n"
        "grant compatibility",
    )
    box(
        ax, 2.55, 2.30, 4.3, .74,
        "PASS + resolved receipt\nY = 1 non-receipt; Y = 0 receipt",
    )
    arrow(ax, (4.7, 3.29), (4.7, 3.07))

    box(
        ax, .15, 1.19, 3.15, .76,
        "Person-weighted\nreported prevalence",
    )
    box(
        ax, 3.7, 1.19, 3.15, .76,
        "Unweighted model\nReported non-receipt",
    )
    line(ax, [(4.7, 2.27), (4.7, 2.12), (1.725, 2.12)])
    arrow(ax, (1.725, 2.12), (1.725, 1.98))
    line(ax, [(4.7, 2.12), (5.275, 2.12)])
    arrow(ax, (5.275, 2.12), (5.275, 1.98))

    # The outside route explicitly connects the proxies to prediction, rather
    # than depicting theory as an observed mediator of eligibility or receipt.
    line(ax, [(6.875, 4.96), (6.96, 4.96), (6.96, 2.1), (6.65, 2.1)])
    arrow(ax, (6.65, 2.1), (6.65, 1.98))

    box(
        ax, .15, .18, 6.7, .67,
        "Artefact: separate statuses, scores and audited exports\n"
        "Workflow links are not tested causal pathways",
        shade="white",
    )
    arrow(ax, (1.725, 1.16), (1.725, .88))
    arrow(ax, (5.275, 1.16), (5.275, .88))
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
        f"Final resolved cohort: {n('Final analysis cohort')}\n"
        f"Unresolved receipt among PASS: {n('Outcome unresolved')}",
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
