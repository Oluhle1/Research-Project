#!/usr/bin/env bash
# Run from the repository root. Override OPG_PYTHON for an existing environment.
set -euo pipefail
export MPLCONFIGDIR="${PWD}/.local/cache/matplotlib"
export XDG_CACHE_HOME="${PWD}/.local/cache"
export OPENBLAS_NUM_THREADS=2
export OMP_NUM_THREADS=2
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME"
exec "${OPG_PYTHON:-.venv/bin/python}" -m streamlit run app/Home.py \
  --server.address 127.0.0.1 --server.port 8501 --server.headless true \
  --browser.gatherUsageStats false
