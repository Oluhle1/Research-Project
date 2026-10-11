"""Safe research summaries and downloadable reports; no upload persistence."""
from __future__ import annotations

import hashlib
import importlib.metadata
import io
import json
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

NOTICE = (
    "Historical LCS 2014/2015 KwaZulu-Natal research prototype. Observable "
    "screening is not statutory eligibility or a SASSA grant decision. "
    "Model probabilities estimate reported non-receipt, not eligibility. "
    "Uploaded scores use a frozen full-data fit and are not held-out validation. "
    "Generalisation to other populations or periods has not been established."
)
SAFE_COLUMNS = ["screen_status", "receipt_status", "classification", "reason_codes",
                "model_eligible_for_scoring", "predicted_nonreceipt", "score_context",
                "rule_version", "model_version", "threshold_single", "threshold_couple"]


def safe_results(results: pd.DataFrame) -> pd.DataFrame:
    """Use an explicit allowlist; never derive public IDs from survey IDs."""
    safe = results[[c for c in SAFE_COLUMNS if c in results.columns]].copy()
    safe.insert(0, "research_id", [f"R{i:06d}" for i in range(1, len(safe) + 1)])
    return safe


def summary(results: pd.DataFrame) -> dict:
    resolved = results[(results["screen_status"] == "PASS") &
                       results["receipt_status"].isin(["RECIPIENT", "NON_RECIPIENT"])]
    events = resolved["receipt_status"].eq("NON_RECIPIENT")
    weights = pd.to_numeric(resolved["person_weight"], errors="raise")
    weighted = float(weights[events].sum() / weights.sum()) if len(resolved) and weights.sum() > 0 else None
    return {
        "uploaded_rows": len(results),
        "screen_status_counts": results["screen_status"].value_counts().sort_index().to_dict(),
        "classification_counts": results["classification"].value_counts().sort_index().to_dict(),
        "resolved_pass_denominator": len(resolved),
        "reported_recipients": int((~events).sum()),
        "reported_nonrecipients": int(events.sum()),
        "unweighted_nonreceipt_rate": float(events.mean()) if len(resolved) else None,
        "person_weighted_nonreceipt_rate": weighted,
        "scored_rows": int(results.get("predicted_nonreceipt", pd.Series(dtype=float)).notna().sum()),
        "scope": "Uploaded rows only; not necessarily the original 1,317 older-adult frame.",
        "responsible_use_note": NOTICE,
    }


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")


def summary_csv(value: dict) -> bytes:
    flat = {k: json.dumps(v, sort_keys=True) if isinstance(v, dict) else v for k, v in value.items()}
    return pd.DataFrame([flat]).to_csv(index=False, lineterminator="\n").encode("utf-8")


def _git_provenance(root: Path) -> tuple[str | None, bool | None]:
    """Git is optional for extracted local app packages; retain unknown as null."""
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
    except OSError:
        return None, None
    return (
        commit.stdout.strip() if commit.returncode == 0 else None,
        bool(dirty.stdout.strip()) if dirty.returncode == 0 else None,
    )


def build_report(results: pd.DataFrame, upload: bytes, validation, model_manifest: dict,
                 filtered_ids: list[str] | None = None) -> dict[str, bytes]:
    """Return exact download bytes and their hashes; names/IDs never enter manifest."""
    safe = safe_results(results)
    filtered = safe if filtered_ids is None else safe[safe["research_id"].isin(filtered_ids)]
    value = summary(results)
    files = {
        "results.csv": safe.to_csv(index=False, lineterminator="\n").encode("utf-8"),
        "filtered_results.csv": filtered.to_csv(index=False, lineterminator="\n").encode("utf-8"),
        "summary.json": json_bytes(value), "summary.csv": summary_csv(value),
        "responsible_use.txt": (NOTICE + "\n").encode("utf-8"),
    }
    root = Path(__file__).resolve().parents[1]
    commit, dirty = _git_provenance(root)
    manifest = {
        "timestamp_local": datetime.now(ZoneInfo("Africa/Johannesburg")).isoformat(),
        "timezone": "Africa/Johannesburg", "schema_version": "opg-screen-v1",
        "rule_version": "opg-kzn-primary-v1", "model_version": model_manifest["model_version"],
        "model_artifact_sha256": model_manifest.get("artifact_sha256"),
        "script_commit": commit,
        "working_tree_dirty": dirty,
        "application_source_sha256": {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted([*root.glob("opg_core/*.py"), *root.glob("app/*.py")])
        },
        "dataset_sha256": hashlib.sha256(upload).hexdigest(),
        "accepted_rows": len(results), "rejected_rows": 0,
        "filtered_rows": len(filtered), "checks_performed": list(validation.checks),
        "validation_warnings": list(validation.warnings),
        "output_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
        "dependencies": {name: importlib.metadata.version(name) for name in
                         ("pandas", "numpy", "statsmodels", "scikit-learn", "streamlit")},
        "responsible_use_note": NOTICE,
    }
    files["audit_manifest.json"] = json_bytes(manifest)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    files["report.zip"] = buffer.getvalue()
    return files
