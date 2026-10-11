"""Start the local MVP on Windows, macOS, or Linux using this Python environment."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cache = root / ".local" / "cache"
    plotting_cache = cache / "matplotlib"
    plotting_cache.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.update({
        "MPLCONFIGDIR": str(plotting_cache),
        "XDG_CACHE_HOME": str(cache),
        "OPENBLAS_NUM_THREADS": "2",
        "OMP_NUM_THREADS": "2",
    })
    command = [
        sys.executable, "-m", "streamlit", "run", "app/Home.py",
        "--server.address", "127.0.0.1", "--server.port", "8501",
        "--server.headless", "true", "--browser.gatherUsageStats", "false",
    ]
    print("Open http://localhost:8501 in your browser. Press Ctrl+C here to stop.", flush=True)
    try:
        return subprocess.call(command, cwd=root, env=environment)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
