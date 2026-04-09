"""Tests for titanite.core.security module."""

import pandas as pd
import pytest

from titanite.core import SecureDataHandler


def test_load_raises_on_missing_file(tmp_path):
    """load_sensitive_data raises FileNotFoundError for missing file."""
    missing = tmp_path / "no_such_file.csv"
    with pytest.raises(FileNotFoundError, match="not found"):
        SecureDataHandler.load_sensitive_data(missing)


def test_load_reads_csv_successfully(tmp_path):
    """load_sensitive_data successfully reads a CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b,c\n1,2,3\n4,5,6")

    data = SecureDataHandler.load_sensitive_data(csv_file)
    assert len(data) == 2
    assert list(data.columns) == ["a", "b", "c"]


def test_suppress_small_cells_removes_low_counts():
    """suppress_small_cells filters out rows with count < threshold."""
    df = pd.DataFrame({"label": ["a", "b", "c", "d"], "count": [1, 3, 5, 10]})
    result = SecureDataHandler.suppress_small_cells(df, threshold=5)
    assert len(result) == 2
    assert list(result["count"]) == [5, 10]


def test_suppress_small_cells_default_threshold():
    """suppress_small_cells uses threshold=5 by default."""
    df = pd.DataFrame({"count": [1, 4, 5, 6]})
    result = SecureDataHandler.suppress_small_cells(df)
    assert len(result) == 2
    assert list(result["count"]) == [5, 6]


def test_suppress_small_cells_custom_column_name():
    """suppress_small_cells accepts custom count column name."""
    df = pd.DataFrame({"frequency": [2, 5, 10]})
    result = SecureDataHandler.suppress_small_cells(
        df, threshold=5, count_column="frequency"
    )
    assert len(result) == 2
    assert list(result["frequency"]) == [5, 10]


def test_suppress_small_cells_missing_column_warning():
    """suppress_small_cells returns data unchanged if count column not found."""
    df = pd.DataFrame({"value": [1, 2, 3]})
    result = SecureDataHandler.suppress_small_cells(
        df, threshold=5, count_column="nonexistent"
    )
    # Should return data unchanged when column not found
    assert len(result) == 3
    assert list(result.columns) == ["value"]


def test_anonymize_removes_sensitive_columns():
    """anonymize_for_publication drops specified columns."""
    df = pd.DataFrame(
        {
            "q01": ["30s", "20s"],
            "timestamp": ["2023-01-01", "2023-01-02"],
            "q15": ["text1", "text2"],
            "safe_column": ["a", "b"],
        }
    )
    result = SecureDataHandler.anonymize_for_publication(
        df, sensitive_columns=["timestamp", "q15"]
    )
    assert "timestamp" not in result.columns
    assert "q15" not in result.columns
    assert "q01" in result.columns
    assert "safe_column" in result.columns


def test_anonymize_ignores_nonexistent_columns(caplog):
    """anonymize_for_publication silently skips nonexistent columns."""
    df = pd.DataFrame({"q01": ["30s"]})
    result = SecureDataHandler.anonymize_for_publication(
        df, sensitive_columns=["nonexistent1", "nonexistent2"]
    )
    assert list(result.columns) == ["q01"]
    # No warning for nonexistent columns


def test_anonymize_returns_copy():
    """anonymize_for_publication returns a copy, not a view."""
    df = pd.DataFrame({"q01": ["30s"], "q15": ["text"]})
    result = SecureDataHandler.anonymize_for_publication(df, ["q15"])
    # Verify it's a copy by modifying the original
    df.loc[0, "q01"] = "modified"
    assert result.loc[0, "q01"] == "30s"


def test_suppress_small_cells_returns_copy():
    """suppress_small_cells returns a copy."""
    df = pd.DataFrame({"count": [1, 5, 10]})
    result = SecureDataHandler.suppress_small_cells(df, threshold=5)
    # Modify original
    df.loc[0, "count"] = 999
    # Result should be unchanged
    assert list(result["count"]) == [5, 10]
