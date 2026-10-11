"""One application/CLI processing path: validate, screen, frozen score, report."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from opg_core.schema import ValidationResult, validate_csv
from opg_core.screening import screen_frame
from opg_core.reporting import build_report, summary


@dataclass
class ProcessedRun:
    validation: ValidationResult
    results: pd.DataFrame | None = None
    summary: dict = field(default_factory=dict)
    model_manifest: dict = field(default_factory=dict)
    reports: dict[str, bytes] = field(default_factory=dict)


def process_upload(content: bytes) -> ProcessedRun:
    """Fatal input errors stop before model loading; uploads never trigger fitting."""
    validation = validate_csv(content)
    if validation.errors:
        return ProcessedRun(validation)
    from opg_core.inference import load_model, score_frame

    screened = screen_frame(validation.frame)
    model = load_model()
    results = score_frame(screened, model)
    return ProcessedRun(validation, results, summary(results), model.manifest,
                        build_report(results, content, validation, model.manifest))
