"""Upload boundary tests use invented records only."""

import pandas as pd
import pytest

from opg_core import schema


def one_row():
    return schema.synthetic_template().iloc[:1].copy()


def test_synthetic_csv_and_bom_are_valid():
    content = schema.synthetic_template().to_csv(index=False).encode("utf-8-sig")
    result = schema.validate_csv(content)
    assert not result.errors
    assert len(result.frame) == 6
    assert "utf8_encoding" in result.checks
    assert result.frame.loc[0, "private_income"] == 0


@pytest.mark.parametrize("content", [b"", b"\xff", b"a,b\n\"unfinished", b"a,b\n1,2,3", b"a,a\n1,2", b"\0"])
def test_bad_csv_is_rejected(content):
    result = schema.validate_csv(content)
    assert result.frame is None
    assert result.errors


def test_size_limit_and_row_limit():
    assert schema.validate_csv(b"x" * (schema.MAX_BYTES + 1)).frame is None
    too_many = pd.concat([one_row()] * (schema.MAX_ROWS + 1), ignore_index=True)
    assert schema.validate_frame(too_many).frame is None


def test_header_only_and_missing_columns_fail():
    assert schema.validate_csv((",".join(schema.COLUMNS) + "\n").encode()).errors
    result = schema.validate_frame(one_row().drop(columns="oldage"))
    assert result.frame is None
    assert any("oldage" in message for message in result.errors)


def test_unknown_columns_fail_without_echoing_values():
    frame = one_row()
    frame["PRIVATE-UNTRUSTED-HEADER"] = "private-value"
    result = schema.validate_frame(frame)
    assert result.errors
    assert "PRIVATE-UNTRUSTED-HEADER" not in str(result.errors)
    assert "private-value" not in str(result.errors)


@pytest.mark.parametrize("field,value", [
    ("schema_version", "another-version"), ("context", "CURRENT_POLICY"),
    ("age", "60.5"), ("age", ""), ("age", "106"), ("survey_month", "13"),
    ("survey_year", "2026"), ("province_code", "4"), ("sex", "9"),
    ("settlement", "3"), ("schooling_raw", "100"), ("warvet", "3"),
    ("person_weight", "0"), ("person_weight", "NaN"), ("person_weight", ""),
    ("person_weight", "1e-10000"),
    ("private_income", "Infinity"), ("opg_income", "-1"),
    ("spouse_no", "50"), ("personno", "0"), ("income_schedule", "guessed_zero"),
    ("record_id", "=HYPERLINK(private)"), ("household_id", "@private"),
])
def test_invalid_values_fail_without_echoing_cell_content(field, value):
    frame = one_row()
    frame[field] = value
    result = schema.validate_frame(frame)
    assert result.frame is None
    assert result.errors
    if "private" in value.lower():
        assert value not in str(result.errors)


def test_historical_date_bounds_and_reordered_columns():
    frame = one_row()
    frame["survey_month"] = 9
    assert schema.validate_frame(frame).errors
    frame["survey_month"] = 10
    assert not schema.validate_frame(frame[list(reversed(schema.COLUMNS))]).errors
    frame["survey_year"] = 2015
    frame["survey_month"] = 11
    assert schema.validate_frame(frame).errors


def test_duplicate_normalized_keys_and_record_ids_fail():
    frame = pd.concat([one_row(), one_row()], ignore_index=True)
    frame.loc[1, "record_id"] = "SYN-other"
    frame.loc[1, "personno"] = "01"
    result = schema.validate_frame(frame)
    assert any("normalized" in message for message in result.errors)
    frame.loc[1, "household_id"] = "SYN-another-household"
    frame.loc[1, "record_id"] = frame.loc[0, "record_id"]
    assert any("record_id" in message for message in schema.validate_frame(frame).errors)


@pytest.mark.parametrize("schedule,private,opg", [
    ("supported_zero", "", ""), ("supported_zero", "1", "0"),
    ("summed", "", "0"), ("summed", "0", ""),
    ("absent", "0", ""), ("unspecified", "", "0"), ("contradiction", "0", "0"),
])
def test_income_missingness_is_not_imputed(schedule, private, opg):
    frame = one_row()
    frame["income_schedule"] = schedule
    frame["private_income"] = private
    frame["opg_income"] = opg
    assert any("income_schedule" in message for message in schema.validate_frame(frame).errors)


def test_unresolved_amounts_and_blank_codes_stay_unresolved():
    frame = one_row()
    frame["income_schedule"] = "absent"
    frame["private_income"] = ""
    frame["opg_income"] = ""
    frame["disability"] = ""
    result = schema.validate_frame(frame)
    assert not result.errors
    assert result.frame.loc[0, "private_income"] is None
    assert result.frame.loc[0, "disability"] == "9"
    assert result.warnings


def test_model_missingness_is_warned_and_never_guessed():
    frame = one_row()
    frame["sex"] = ""
    frame["schooling_raw"] = "21"
    frame["settlement"] = ""
    frame["welfare_distance"] = "99"
    result = schema.validate_frame(frame)
    assert not result.errors
    assert result.frame.loc[0, "sex"] == ""
    assert any("missing model predictors" in message for message in result.warnings)

