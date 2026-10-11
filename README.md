# OPG historical research prototype

A local Streamlit interface for the LCS 2014/2015 KwaZulu-Natal OPG study.
It separates historical observable screening, reported receipt and statistical
non-receipt probability. It does not determine legal eligibility or issue grant
decisions. The scientific scripts in `analysis/` and original outputs remain
the research baseline.

## Run locally

Use Python 3.12. From the repository root or extracted MVP folder, on Windows
PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-app.txt
.\.venv\Scripts\python.exe tools\run_app.py
```

Open **http://localhost:8501** on your computer. Keep the terminal open; press
Ctrl+C to stop. See [Windows setup](docs/windows_setup.md) for installation,
first-use steps and troubleshooting. These commands do not require activating
the environment or changing PowerShell execution policy.

On macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-app.txt
.venv/bin/python tools/run_app.py
```

In the prepared cloud workspace use `/workspace/research-venv/bin/python` instead
of `.venv/bin/python`; start it with
`OPG_PYTHON=/workspace/research-venv/bin/python bash tools/run_app.sh`.
The launchers set writable plotting caches and two numerical threads.
The app loads a frozen model; it never trains on uploads.
Download the synthetic template or select the synthetic example, validate,
inspect classifications and reasons, then download a report. Supported uploads
must follow [the data dictionary](docs/data_dictionary.md); arbitrary survey
columns and pre-screened cohort exports are not accepted as screen-ready inputs.

Uploads stay in session memory. Displays and reports omit submitted record,
household and person IDs, spouse pointers and raw income. Generated research
IDs are row labels, not proof that every source dataset is anonymous. Use
controlled local research access. Existing historical raw data and outputs are
already tracked in this repository; this is not a public deployment package.

## Validate

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python tools/audit_baseline.py
```

The audit reads the local historical datasets and writes only ignored
`.local/baseline/`. It reproduces phases 3–5, the integrated CLI and existing
evaluation. On other machines, private-reference tests explicitly skip when
the required datasets are unavailable; synthetic app tests remain runnable.

The original scientific checksum assumes Windows CRLF serialization. The audit
sets the runtime newline convention for newly generated CSVs and retains the
original expected checksum. Running the legacy scripts directly can overwrite
tracked outputs; use the provided audit entry point for baseline reproduction.

## Evidence and limits

- [Current state audit](docs/current_state_audit.md)
- [Model decision record](docs/model_decision_record.md)
- [Architecture](docs/architecture.md) and [rulebook](docs/rulebook.md)
- [Implementation evidence](docs/evidence_log.md)
- [Verified Windows synthetic report](examples/synthetic_report/README.md)
- [Local deployment](docs/deployment.md) and [usability protocol](docs/usability_protocol.md)

Held-out research performance is displayed separately from full-data fitted
scores. The dashboard introduces no predictive algorithm or current-policy
claim. Public hosting, participant usability testing and paper revisions are
separate steps and must not be described as completed without evidence.

Current validation: **220 automated checks passed, with no failures or skips**,
including full 15,388-record native UI/CLI parity. The local app and documented
launcher were started and restarted successfully. See the evidence log for
test scope and unresolved human/publication steps. The standalone ZIP also
passed a fresh dependency installation, extracted-folder synthetic workflow,
report exports and launcher health check. Automated package verification ran on
Linux. The user also ran the MVP on Windows and supplied screenshots and six
exported synthetic report files: all 50 cross-file, checksum and reference
comparison checks passed. See [Windows evidence](docs/windows_validation.json).
