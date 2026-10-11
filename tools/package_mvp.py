"""Package the local MVP with an explicit file allowlist and no survey data."""
from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "OPG-Streamlit-MVP"
FILES = (
    "app/Home.py",
    "analysis/phase3_build_cohort.py",
    "analysis/phase4_rq1.py",
    "analysis/phase5_model.py",
    "models/logistic_model.json",
    "models/manifest.json",
    "models/evaluation.json",
    "requirements.txt",
    "requirements-app.txt",
    ".streamlit/config.toml",
    "tools/run_app.py",
    "tools/run_app.sh",
    "docs/windows_setup.md",
    "docs/data_dictionary.md",
    "docs/rulebook.md",
)
README = """# OPG Streamlit MVP — local demonstration

Extract this entire folder and use Python 3.12 (64-bit).
Open PowerShell in this folder on Windows, then run:

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
.\\.venv\\Scripts\\python.exe -m pip install -r requirements-app.txt
.\\.venv\\Scripts\\python.exe tools\\run_app.py
```

Open http://localhost:8501 on your computer. Click **Use synthetic example**,
then **Run analysis**. Explore results, predictions and report exports using
the sidebar. Leave the terminal open. Press Ctrl+C to stop the app.
For future sessions, run only the last command.

See [Windows setup](docs/windows_setup.md) for Python installation and
troubleshooting, and [the data dictionary](docs/data_dictionary.md) for uploads.
Virtual-environment activation and Git are unnecessary.

On macOS/Linux, use `python3.12 -m venv .venv`, then
`.venv/bin/python -m pip install -r requirements-app.txt` and
`.venv/bin/python tools/run_app.py`.

This package contains app code, a frozen JSON model, aggregate evaluation,
and the scientific source modules needed at runtime. It contains no historical
survey datasets, respondent outputs or Git history. Preserve the scientific
source files unchanged; the model verifies their exact bytes.

The app is a historical LCS 2014/2015 KwaZulu-Natal research prototype.
Observable screening is not a statutory eligibility or grant decision.
Model probabilities describe reported non-receipt; upload scoring does not
train a model or establish held-out performance on the uploaded data.

`PACKAGE_CONTENTS.sha256` records the files included in this package.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".local/distribution/OPG-Streamlit-MVP.zip")
    destination = parser.parse_args().output.resolve()
    files = {name: (ROOT / name).read_bytes() for name in FILES}
    for path in sorted((ROOT / "opg_core").glob("*.py")):
        files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    files["README.md"] = README.encode("utf-8")
    checksums = "".join(
        f"{hashlib.sha256(content).hexdigest()}  {name}\n"
        for name, content in sorted(files.items())
    )
    files["PACKAGE_CONTENTS.sha256"] = checksums.encode("utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            archive.writestr(f"{PACKAGE_ROOT}/{name}", content)
    print(f"Created {destination} ({destination.stat().st_size:,} bytes; {len(files)} files)")


if __name__ == "__main__":
    main()
