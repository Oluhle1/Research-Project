"""Validate the explicit, normalized historical research upload contract.

This module performs no screening, modelling, file writes, or zero imputation.
Original survey identifiers are accepted only for controlled local parity work;
public examples and downloadable reports must use synthetic or pseudonymous IDs.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

import pandas as pd

SCHEMA_VERSION = "opg-screen-v1"
CONTEXT = "LCS_KZN_2014_2015"
MAX_ROWS = 50_000
MAX_BYTES = 20 * 1024 * 1024
COLUMNS = (
    "schema_version", "context", "record_id", "household_id", "personno",
    "survey_year", "survey_month", "province_code", "age", "sex", "marital",
    "partner_in_hh", "spouse_no", "schooling_raw", "settlement", "welfare_distance",
    "person_weight", "any_grant", "oldage", "disability", "child", "caredep",
    "foster", "warvet", "inaid", "private_income", "opg_income", "income_schedule",
)
MODEL_FIELDS = ("age", "sex", "schooling_raw", "settlement", "welfare_distance")
CATEGORY_CODES = {
    "province_code": {"5"},
    "sex": {"1", "2", ""},
    "marital": {"1", "2", "3", "4", "5", "6", "9"},
    "partner_in_hh": {"1", "2", "8", "9"},
    "schooling_raw": {str(n) for n in range(1, 33)} | {"98", "99", ""},
    "settlement": {"1", "2", "4", "5", ""},
    "welfare_distance": {str(n) for n in range(1, 10)} | {"99", ""},
    "any_grant": {"1", "2", "3", "9"},
    **{name: {"1", "2", "8", "9"} for name in (
        "oldage", "disability", "child", "caredep", "foster", "warvet", "inaid"
    )},
    "income_schedule": {"supported_zero", "summed", "absent", "unspecified", "contradiction"},
}
UNSPECIFIED_FIELDS = (
    "marital", "partner_in_hh", "any_grant", "oldage", "disability", "child",
    "caredep", "foster", "warvet", "inaid",
)
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
_INTEGER = re.compile(r"[0-9]+\Z")


@dataclass
class ValidationResult:
    frame: pd.DataFrame | None
    errors: list[str]
    warnings: list[str]
    checks: list[str]


def _text(value) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def validate_csv(content: bytes) -> ValidationResult:
    """Read bounded UTF-8 CSV bytes; return structural errors without data rows."""
    checks = ["file_size", "utf8_encoding", "csv_structure"]
    if not isinstance(content, bytes):
        return ValidationResult(None, ["Upload must contain CSV bytes."], [], checks)
    if len(content) > MAX_BYTES:
        return ValidationResult(None, ["CSV exceeds the 20 MiB limit."], [], checks)
    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return ValidationResult(None, ["CSV must use UTF-8 encoding."], [], checks)
    if not decoded.strip() or "\x00" in decoded:
        return ValidationResult(None, ["CSV is empty or contains invalid null bytes."], [], checks)
    try:
        reader = csv.reader(io.StringIO(decoded), strict=True)
        header = next(reader)
        if len(header) != len(set(header)):
            return ValidationResult(None, ["CSV has duplicate column names."], [], checks)
        rows = []
        for row in reader:
            if len(row) != len(header):
                return ValidationResult(None, ["CSV contains a row with the wrong number of fields."], [], checks)
            rows.append(row)
            if len(rows) > MAX_ROWS:
                return ValidationResult(None, ["CSV exceeds the 50,000-row limit."], [], checks)
    except (csv.Error, StopIteration):
        return ValidationResult(None, ["CSV syntax is malformed."], [], checks)
    result = validate_frame(pd.DataFrame(rows, columns=header))
    result.checks = checks + result.checks
    return result


def validate_frame(frame: pd.DataFrame) -> ValidationResult:
    """Validate and normalize values while retaining scientifically missing data.

    Errors identify columns and row counts only, never identifier or income values.
    A frame is returned only when all blocking checks pass.
    """
    checks = [
        "row_count", "exact_columns", "schema_version", "study_context",
        "identifiers", "duplicate_record_ids", "duplicate_person_keys",
        "historical_dates", "categorical_codes", "numeric_values", "income_schedule",
        "predictor_missingness",
    ]
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(frame, pd.DataFrame):
        return ValidationResult(None, ["Input must be a table."], warnings, checks)
    if frame.columns.duplicated().any():
        return ValidationResult(None, ["Table has duplicate column names."], warnings, checks)
    missing = set(COLUMNS) - set(frame.columns)
    extra = set(frame.columns) - set(COLUMNS)
    if missing or extra:
        if missing:
            errors.append("Missing required columns: " + ", ".join(sorted(missing)))
        if extra:
            # Do not echo arbitrary uploaded header text into logs or the interface.
            errors.append(f"Unexpected columns: {len(extra)}. Use the exact documented schema.")
        return ValidationResult(None, errors, warnings, checks)
    if not 1 <= len(frame) <= MAX_ROWS:
        return ValidationResult(None, ["Table must contain 1 to 50,000 rows."], warnings, checks)
    work = frame.loc[:, COLUMNS].copy().reset_index(drop=True)
    for name in COLUMNS:
        work[name] = work[name].map(_text)

    if (work["schema_version"] != SCHEMA_VERSION).any():
        errors.append(f"Every schema_version must be {SCHEMA_VERSION}.")
    if (work["context"] != CONTEXT).any():
        errors.append(f"Every context must be {CONTEXT}.")
    for name in ("record_id", "household_id"):
        invalid = ~work[name].map(lambda value: bool(_ID.fullmatch(value)))
        if invalid.any():
            errors.append(f"{name}: {int(invalid.sum())} missing or invalid identifiers.")

    for name, lower, upper in (
        ("personno", 1, 27), ("survey_year", 2014, 2015),
        ("survey_month", 1, 12), ("age", 0, 105),
    ):
        parsed = work[name].map(lambda value: int(value) if _INTEGER.fullmatch(value) and len(value) <= 4 else None)
        valid = parsed.map(lambda value: value is not None and lower <= value <= upper)
        if not valid.all():
            errors.append(f"{name}: {int((~valid).sum())} values must be integers from {lower} to {upper}.")
        elif name == "personno":
            work[name] = parsed.map(str)
        else:
            work[name] = parsed.astype(int)
    if not any(message.startswith(("survey_year:", "survey_month:")) for message in errors):
        dates = work["survey_year"] * 100 + work["survey_month"]
        invalid = ~dates.between(201410, 201510)
        if invalid.any():
            errors.append("survey_year/survey_month must be October 2014 through October 2015.")

    if work["record_id"].duplicated().any():
        errors.append("record_id must be unique.")
    if work.duplicated(["household_id", "personno"]).any():
        errors.append("Duplicate normalized household_id/personno keys are not permitted.")

    for name in UNSPECIFIED_FIELDS:
        blanks = work[name] == ""
        if blanks.any():
            warnings.append(f"{name}: {int(blanks.sum())} blank responses treated as unspecified code 9.")
            work.loc[blanks, name] = "9"
    work.loc[work["spouse_no"] == "", "spouse_no"] = "99"
    for name in CATEGORY_CODES:
        if name != "income_schedule":
            work[name] = work[name].map(lambda value: str(int(value)) if _INTEGER.fullmatch(value) and len(value) <= 3 else value)
        invalid = ~work[name].isin(CATEGORY_CODES[name])
        if invalid.any():
            errors.append(f"{name}: {int(invalid.sum())} unsupported category values.")
    spouse = work["spouse_no"].map(
        lambda value: int(value) if _INTEGER.fullmatch(value) and len(value) <= 3 else None
    )
    valid_spouse = spouse.map(lambda value: value is not None and (1 <= value <= 27 or value in {88, 99}))
    if not valid_spouse.all():
        errors.append(f"spouse_no: {int((~valid_spouse).sum())} unsupported pointers.")
    else:
        work["spouse_no"] = spouse.map(str)

    for name in ("private_income", "opg_income", "person_weight"):
        parsed = []
        invalid = 0
        for value in work[name]:
            if not value and name != "person_weight":
                parsed.append(None)
                continue
            try:
                amount = Decimal(value)
                usable = amount.is_finite() and amount >= 0 and amount <= Decimal("1e12")
                if name == "person_weight":
                    usable = usable and amount > 0 and float(amount) > 0
                if not usable:
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                invalid += 1
                parsed.append(None)
            else:
                parsed.append(float(amount) if name == "person_weight" else amount)
        if invalid:
            errors.append(f"{name}: {invalid} invalid, nonfinite, negative or missing required amounts.")
        work[name] = pd.Series(parsed, dtype=object)

    known = work["income_schedule"].isin(["supported_zero", "summed"])
    complete = work["private_income"].notna() & work["opg_income"].notna()
    invalid = (known & ~complete) | (~known & complete)
    unresolved_has_amount = (~known) & (work["private_income"].notna() | work["opg_income"].notna())
    invalid |= unresolved_has_amount
    zero = work["income_schedule"] == "supported_zero"
    invalid |= zero & ((work["private_income"] != Decimal(0)) | (work["opg_income"] != Decimal(0)))
    if invalid.any():
        errors.append(f"income_schedule: {int(invalid.sum())} rows have inconsistent missingness or unsupported zero income.")

    missing_predictor = (
        (work["sex"] == "") | work["schooling_raw"].isin(["", "21", "22", "31", "32", "99"])
        | (work["settlement"] == "") | work["welfare_distance"].isin(["", "9", "99"])
    )
    if missing_predictor.any():
        warnings.append(f"{int(missing_predictor.sum())} rows have missing model predictors; frozen training preprocessing is required.")
    warnings.append("Historical research data only: compatible schema does not establish external predictive validity.")
    return ValidationResult(None if errors else work, errors, warnings, checks)


def synthetic_template() -> pd.DataFrame:
    """Return a small, entirely invented upload example spanning screen outcomes."""
    base = {
        "schema_version": SCHEMA_VERSION, "context": CONTEXT,
        "record_id": "SYN-001", "household_id": "SYN-H001", "personno": "1",
        "survey_year": 2014, "survey_month": 11, "province_code": "5", "age": 60,
        "sex": "2", "marital": "4", "partner_in_hh": "8", "spouse_no": "88",
        "schooling_raw": "8", "settlement": "1", "welfare_distance": "3",
        "person_weight": 1, "any_grant": "2", "oldage": "8", "disability": "2",
        "child": "2", "caredep": "2", "foster": "2", "warvet": "2", "inaid": "2",
        "private_income": "0", "opg_income": "0", "income_schedule": "supported_zero",
    }
    variants = [
        {},
        {"any_grant": "1", "oldage": "1", "opg_income": "16200", "income_schedule": "summed"},
        {"private_income": "61800.01", "income_schedule": "summed"},
        {"income_schedule": "absent", "private_income": "", "opg_income": ""},
        {"any_grant": "1", "oldage": "9"},
        {"age": 59},
    ]
    rows = []
    for index, change in enumerate(variants, start=1):
        row = {**base, **change}
        row["record_id"] = f"SYN-{index:03d}"
        row["household_id"] = f"SYN-H{index:03d}"
        rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)


def from_research_people(people: dict, welfare: dict) -> pd.DataFrame:
    """LOCAL ONLY: adapt the existing KZN source pipeline for parity verification.

    No data are written. Original household/person keys remain inside this local
    input and must never be used as a committed fixture or public example.
    """
    rows = []
    for person in people.values():
        if person["province_code"] != "5":
            continue
        row = {
            "schema_version": SCHEMA_VERSION, "context": CONTEXT,
            "record_id": f"{person['uqno']}:{person['personno']}",
            "household_id": person["uqno"], "personno": person["personno"],
            "private_income": person["private"], "opg_income": person["opg"],
            "income_schedule": person["schedule"],
            "sex": person["sex"], "schooling_raw": person["schooling_raw"],
            "welfare_distance": welfare.get(person["uqno"], ""),
        }
        for name in (
            "survey_year", "survey_month", "province_code", "age", "marital", "partner_in_hh",
            "spouse_no", "settlement", "person_weight", "any_grant", "oldage", "disability",
            "child", "caredep", "foster", "warvet", "inaid",
        ):
            row[name] = person[name]
        rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)

