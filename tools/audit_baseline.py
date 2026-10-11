"""Reproduce research phases without overwriting committed outputs.

Run: /workspace/research-venv/bin/python tools/audit_baseline.py
Local respondent-level artefacts remain in the ignored .local directory.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local" / "baseline"
os.linesep = "\r\n"  # Original freeze used Windows CSV serialization.
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL / "cache" / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL / "cache"))
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("OMP_NUM_THREADS", "2")
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "analysis"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    import pandas as pd
    import numpy as np
    import phase3_build_cohort as cohort
    import phase4_rq1 as rq1
    import phase5_model as model
    import phase8_evaluate as evaluation
    import run_study as study

    LOCAL.mkdir(parents=True, exist_ok=True)
    cohort.OUT = LOCAL / "phase3"
    rq1.OUT = LOCAL / "phase4"
    rq1.FROZEN = cohort.OUT / "cohort_person.csv"
    model.OUT = LOCAL / "phase5"
    model.FROZEN = rq1.FROZEN
    study.RUN = LOCAL / "primary"
    evaluation.RUN = study.RUN
    evaluation.OUT = LOCAL / "phase8"
    for name, run in (("phase3", cohort.main), ("phase4", rq1.main),
                      ("phase5", model.main), ("primary", study.main),
                      ("phase8", evaluation.main)):
        print(f"Running {name}", flush=True)
        run()
        print(f"Completed {name}: exit 0", flush=True)

    comparisons = []
    for folder in ("phase3", "phase4", "phase5", "primary"):
        source = ROOT / "output" / ("runs/primary" if folder == "primary" else folder)
        for generated in sorted((LOCAL / folder).glob("*.csv")):
            reference = source / generated.name
            left = pd.read_csv(reference, dtype=str).fillna("")
            right = pd.read_csv(generated, dtype=str).fillna("")
            # Numeric serialization can differ across operating systems.
            try:
                pd.testing.assert_frame_equal(left, right)
                same = True
            except AssertionError:
                same = False
            assert left.shape == right.shape and list(left.columns) == list(right.columns)
            max_delta = 0.0
            for column in left.columns:
                if left[column].equals(right[column]):
                    continue
                x = pd.to_numeric(left[column].replace("", np.nan), errors="raise")
                y = pd.to_numeric(right[column].replace("", np.nan), errors="raise")
                assert np.allclose(x, y, rtol=1e-10, atol=1e-10, equal_nan=True), (folder, generated.name, column)
                max_delta = max(max_delta, float(np.nanmax(abs(x - y))))
            comparisons.append({"file": str(generated.relative_to(LOCAL)),
                                "rows": len(right), "exact_parsed_match": same,
                                "numeric_and_text_parity": "pass",
                                "max_absolute_numeric_delta": max_delta})

    reference = pd.read_csv(ROOT / "output/phase3/cohort_person.csv", dtype=str).fillna("")
    generated = pd.read_csv(rq1.FROZEN, dtype=str).fillna("")
    pd.testing.assert_frame_equal(reference, generated)
    record = json.loads((study.RUN / "run_record.json").read_text())
    assert record["results"]["final_cohort"] == 1013
    assert record["results"]["nonrecipients"] == 67
    assert pd.read_csv(model.OUT / "fold_coefficients.csv")["converged"].all()
    baseline = {
        "timestamp": datetime.now(ZoneInfo("Africa/Johannesburg")).isoformat(),
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "python": platform.python_version(), "rule_version": cohort.RULE_VERSION,
        "selected_model": "opg-kzn-six-slope-v1",
        "results": record["results"], "software": record["software"],
        "commands": {name: {"exit_code": 0} for name in ("phase3", "phase4", "phase5", "primary", "phase8")},
        "input_sha256": record["input_sha256"],
        "frozen_cohort_crlf_sha256": digest(rq1.FROZEN),
        "cohort_parity": {"rows": len(generated), "matched": len(generated), "mismatched": 0},
        "csv_comparisons": comparisons,
        "output_sha256": {str(p.relative_to(LOCAL)): digest(p) for folder in ("phase3", "phase4", "phase5", "primary", "phase8") for p in sorted((LOCAL / folder).iterdir()) if p.is_file()},
    }
    (LOCAL / "baseline_reference.json").write_text(json.dumps(baseline, indent=2) + "\n")
    print("Baseline reference saved", flush=True)


if __name__ == "__main__":
    main()
