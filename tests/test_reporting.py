import hashlib
import io
import json
import zipfile
from types import SimpleNamespace

import pandas as pd
import pytest

from opg_core.reporting import build_report, safe_results, summary


def example():
    return pd.DataFrame([
        {"record_id": "PRIVATE-ID-1", "household_id": "PRIVATE-HOUSEHOLD", "personno": "91",
         "private_income": "123456.78", "screen_status": "PASS", "receipt_status": "NON_RECIPIENT",
         "classification": "APPARENTLY_ELIGIBLE_REPORTED_NONRECEIPT", "reason_codes": "PASS_PRIMARY",
         "person_weight": "3", "predicted_nonreceipt": .2, "model_eligible_for_scoring": True},
        {"record_id": "PRIVATE-ID-2", "screen_status": "PASS", "receipt_status": "RECIPIENT",
         "classification": "APPARENTLY_ELIGIBLE_REPORTED_RECEIPT", "reason_codes": "PASS_PRIMARY",
         "person_weight": "1", "predicted_nonreceipt": .1, "model_eligible_for_scoring": True},
        {"record_id": "PRIVATE-ID-3", "screen_status": "UNRESOLVED", "receipt_status": "NOT_ASSESSED",
         "classification": "ELIGIBILITY_UNRESOLVED", "reason_codes": "UNRES_INCOME_ABSENT",
         "person_weight": "10", "predicted_nonreceipt": None, "model_eligible_for_scoring": False},
    ])


def test_denominator_uses_only_observed_resolved_passes():
    value = summary(example())
    assert value["resolved_pass_denominator"] == 2
    assert value["unweighted_nonreceipt_rate"] == .5
    assert value["person_weighted_nonreceipt_rate"] == .75
    assert value["scored_rows"] == 2


def test_exports_are_allowlisted_and_manifest_hashes_exact_download_bytes():
    files = build_report(example(), b"synthetic dataset", SimpleNamespace(checks=["schema"], warnings=[]),
                         {"model_version": "test", "artifact_sha256": "known"}, ["R000002"])
    safe = safe_results(example())
    assert safe["research_id"].tolist() == ["R000001", "R000002", "R000003"]
    assert "record_id" not in safe and "household_id" not in safe and "private_income" not in safe
    archive = zipfile.ZipFile(io.BytesIO(files["report.zip"]))
    for name in archive.namelist():
        assert archive.read(name) == files[name]
        assert b"PRIVATE-" not in archive.read(name)
        assert b"123456.78" not in archive.read(name)
    filtered = pd.read_csv(io.BytesIO(files["filtered_results.csv"]))
    assert filtered["research_id"].tolist() == ["R000002"]
    manifest = json.loads(files["audit_manifest.json"])
    assert manifest["filtered_rows"] == 1
    assert manifest["accepted_rows"] == 3 and manifest["rejected_rows"] == 0
    assert manifest["timezone"] == "Africa/Johannesburg"
    for name, expected in manifest["output_sha256"].items():
        assert hashlib.sha256(files[name]).hexdigest() == expected


def test_same_dataset_has_repeatable_result_and_summary_bytes():
    args = (example(), b"synthetic", SimpleNamespace(checks=[], warnings=[]), {"model_version": "test"})
    a = build_report(*args); b = build_report(*args)
    for name in ("results.csv", "summary.csv", "summary.json"):
        assert a[name] == b[name]


def test_empty_resolved_denominator_is_null_not_zero_prevalence():
    frame = example().iloc[2:]
    value = summary(frame)
    assert value["resolved_pass_denominator"] == 0
    assert value["unweighted_nonreceipt_rate"] is None
    assert value["person_weighted_nonreceipt_rate"] is None


@pytest.mark.parametrize("missing_git", [True, False], ids=["git-not-installed", "extracted-without-git-history"])
def test_local_package_analysis_and_reports_work_without_git_provenance(monkeypatch, missing_git):
    from opg_core.schema import synthetic_template
    from opg_core.workflow import process_upload

    def unavailable_git(*args, **kwargs):
        if missing_git:
            raise FileNotFoundError("git is not installed")
        return SimpleNamespace(returncode=128, stdout="", stderr="not a git repository")

    monkeypatch.setattr("opg_core.reporting.subprocess.run", unavailable_git)
    upload = synthetic_template().to_csv(index=False, lineterminator="\n").encode("utf-8")
    run = process_upload(upload)
    assert not run.validation.errors
    assert run.summary["uploaded_rows"] == 6
    assert run.summary["scored_rows"] == 2
    manifest = json.loads(run.reports["audit_manifest.json"])
    assert manifest["script_commit"] is None
    assert manifest["working_tree_dirty"] is None
    assert manifest["application_source_sha256"]
    with zipfile.ZipFile(io.BytesIO(run.reports["report.zip"])) as archive:
        for name, expected in manifest["output_sha256"].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
