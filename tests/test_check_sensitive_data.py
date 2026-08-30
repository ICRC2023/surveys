"""Tests for scripts/check_sensitive_data.py."""

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).parent.parent / "scripts" / "check_sensitive_data.py"
_spec = importlib.util.spec_from_file_location("check_sensitive_data", _SCRIPT)
check_sensitive_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_sensitive_data)

main = check_sensitive_data.main


def test_flags_csv_with_free_text_column(tmp_path):
    """A CSV whose header has a free-text column is rejected."""
    csv_file = tmp_path / "prepared_data.csv"
    csv_file.write_text("timestamp,q01,q02,q15\n2023-07-15,30s,Female,answer\n")
    assert main([str(csv_file)]) == 1


def test_flags_csv_with_translation_column(tmp_path):
    """A CSV with a `_ja` translation column is rejected."""
    csv_file = tmp_path / "sentiment_data.csv"
    csv_file.write_text("q01,q15_polarity,q15_ja\n30s,0.1,訳文\n")
    assert main([str(csv_file)]) == 1


def test_allows_aggregated_csv(tmp_path):
    """A CSV with only categories, counts and sentiment scores is allowed."""
    csv_file = tmp_path / "public_data.csv"
    csv_file.write_text(
        "q01,q02,q03_regional,q15_polarity,q15_subjectivity\n"
        "30s,Female,Europe,0.1,0.4\n"
    )
    assert main([str(csv_file)]) == 0


def test_flags_json_records_with_free_text(tmp_path):
    """A JSON array of records containing a free-text field is rejected."""
    json_file = tmp_path / "comments.json"
    json_file.write_text('[{"q01": "30s", "q16": "a free-text answer"}]')
    assert main([str(json_file)]) == 1


def test_allows_json_without_free_text(tmp_path):
    """A JSON array of aggregated records is allowed."""
    json_file = tmp_path / "chi2.json"
    json_file.write_text('[{"questions": "q01-q02", "p_value": 0.03}]')
    assert main([str(json_file)]) == 0


def test_ignores_non_data_suffixes(tmp_path):
    """A non-CSV/JSON file passed in is ignored."""
    png = tmp_path / "chart.png"
    png.write_bytes(b"\x89PNG\r\n")
    assert main([str(png)]) == 0


def test_unreadable_file_is_an_error(tmp_path):
    """A CSV that cannot be parsed is reported as an error (exit 1)."""
    bad = tmp_path / "broken.json"
    bad.write_text("{ this is not valid json")
    assert main([str(bad)]) == 1


def test_missing_file_is_skipped(tmp_path):
    """A path that does not exist is silently skipped."""
    missing = tmp_path / "gone.csv"
    assert main([str(missing)]) == 0
