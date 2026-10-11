# Controlled local deployment

Default: local demonstration using synthetic inputs. Run the README command
from the repository root with Python 3.12 and `requirements-app.txt`. In the
prepared cloud machine the environment is `/workspace/research-venv`.

For a Windows computer, follow [Windows setup](windows_setup.md). The standalone
MVP ZIP runs without Git or the historical survey datasets. It contains the
frozen model, app/core code, required scientific source modules and synthetic
demonstration instructions; it excludes raw data, historical outputs and Git
history. Run `tools/run_app.py` using the local virtual environment's Python.

Streamlit binds to loopback on port 8501. No secrets, external database or SASSA
service are used. Turn off usage statistics with the documented startup flag.
The app does not write uploads or reports to disk; session data remain in
Streamlit process memory until session/process lifecycle removes them. This is
not a guarantee of immediate memory erasure. Avoid sensitive upload contents.

The schema bounds uploads at 20 MiB and 50,000 rows. CSV extension, UTF-8,
structure, columns and values are checked. Fatal validation errors prevent
screening and scoring. Unknown raw survey formats are outside the MVP.

Only trusted local JSON coefficients/preprocessing are loaded. Model generation
is an explicit offline build using the frozen research specification. Updating
source or dependencies requires rerunning tests and retaining the evidence log;
upload actions do not refresh the model. Streamlit processes must restart in a
new environment even when dependencies and files are restored.

## Public demonstration — not deployed

A public synthetic-only package must contain the app, core adapters, synthetic
fixtures, shared scientific Python modules used by the adapters, aggregate
evaluation evidence and the data-only model. Preserve verified source hashes. Exclude
`Dataset/`, `output/`, archived respondent exports, `.local/`, private audit logs,
original person-level examples and Git history that contains them. Ignoring
paths does not remove already tracked data. Confirm source-data licence and
permissions before hosting any survey-derived content.

No public deployment, external validation or participant usability result is
claimed by this local implementation. See `usability_protocol.md` for a future
consented task evaluation. Paper integration is also a separate phase.
