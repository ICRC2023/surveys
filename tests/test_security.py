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


def test_generalize_timestamp_truncates_to_day():
    """generalize_timestamp floors timestamps to daily resolution."""
    df = pd.DataFrame({"timestamp": ["2023-07-15 10:23:45", "2023-07-15 18:59:00"]})
    result = SecureDataHandler.generalize_timestamp(df)
    assert list(result["timestamp"]) == [
        pd.Timestamp("2023-07-15"),
        pd.Timestamp("2023-07-15"),
    ]


def test_generalize_timestamp_custom_freq():
    """generalize_timestamp accepts a coarser or finer offset alias."""
    df = pd.DataFrame({"timestamp": ["2023-07-15 10:23:45"]})
    result = SecureDataHandler.generalize_timestamp(df, freq="h")
    assert result["timestamp"].iloc[0] == pd.Timestamp("2023-07-15 10:00:00")


def test_generalize_timestamp_missing_column_warns():
    """generalize_timestamp returns an unchanged copy if column is absent."""
    df = pd.DataFrame({"q01": ["30s"]})
    result = SecureDataHandler.generalize_timestamp(df, column="timestamp")
    assert list(result.columns) == ["q01"]
    df.loc[0, "q01"] = "modified"
    assert result.loc[0, "q01"] == "30s"


def test_k_anonymize_drops_rare_combinations():
    """k_anonymize removes quasi-identifier groups smaller than k."""
    df = pd.DataFrame(
        {
            "q01": ["20s"] * 5 + ["30s"] * 2,
            "q02": ["Female"] * 5 + ["Male"] * 2,
            "value": range(7),
        }
    )
    result = SecureDataHandler.k_anonymize(df, ["q01", "q02"], k=5)
    assert len(result) == 5
    assert set(result["q01"]) == {"20s"}


def test_k_anonymize_keeps_all_when_groups_large_enough():
    """k_anonymize keeps every row when all groups have size >= k."""
    df = pd.DataFrame({"q01": ["20s"] * 6, "q02": ["Female"] * 6, "value": range(6)})
    result = SecureDataHandler.k_anonymize(df, ["q01", "q02"], k=5)
    assert len(result) == 6


def test_k_anonymize_returns_copy():
    """k_anonymize returns a copy, not a view."""
    df = pd.DataFrame({"q01": ["20s"] * 5, "value": range(5)})
    result = SecureDataHandler.k_anonymize(df, ["q01"], k=5)
    df.loc[0, "value"] = 999
    assert result.loc[0, "value"] == 0


def test_k_anonymize_missing_columns_warns():
    """k_anonymize returns an unchanged copy if no quasi-identifiers exist."""
    df = pd.DataFrame({"value": [1, 2, 3]})
    result = SecureDataHandler.k_anonymize(df, ["q01", "q02"], k=5)
    assert len(result) == 3


def test_build_public_dataset_full_pipeline():
    """build_public_dataset drops free-text, coarsens time, and k-anonymizes."""
    df = pd.DataFrame(
        {
            "timestamp": ["2023-07-15 10:23:45"] * 6 + ["2023-07-16 09:00:00"] * 2,
            "q01": ["20s"] * 6 + ["70s"] * 2,
            "q02": ["Female"] * 6 + ["Male"] * 2,
            "q15": ["text"] * 8,
            "q15_ja": ["訳"] * 8,
            "q15_polarity": [0.1] * 8,
            "response": [1] * 8,
        }
    )
    result = SecureDataHandler.build_public_dataset(
        df,
        free_text_columns=["q15"],
        quasi_identifiers=["q01", "q02"],
        k=5,
        extra_drop_columns=["response"],
    )
    # Free-text original and translation removed; sentiment score kept
    assert "q15" not in result.columns
    assert "q15_ja" not in result.columns
    assert "q15_polarity" in result.columns
    assert "response" not in result.columns
    # Timestamp coarsened to day
    assert result["timestamp"].iloc[0] == pd.Timestamp("2023-07-15")
    # Rare (70s, Male) group of 2 dropped, 6 rows retained
    assert len(result) == 6


def test_aggregate_counts_univariate_suppresses_small_groups():
    """aggregate_counts drops categories seen fewer than threshold times."""
    df = pd.DataFrame({"q02": ["Male"] * 6 + ["Female"] * 3})
    result = SecureDataHandler.aggregate_counts(df, ["q02"], threshold=5)
    assert list(result.columns) == ["q02", "count"]
    assert result.to_dict("records") == [{"q02": "Male", "count": 6}]


def test_aggregate_counts_bivariate():
    """aggregate_counts cross-tabulates two columns."""
    df = pd.DataFrame(
        {
            "q01": ["20s"] * 5 + ["30s"] * 5 + ["40s"] * 2,
            "q02": ["Female"] * 5 + ["Male"] * 5 + ["Male"] * 2,
        }
    )
    result = SecureDataHandler.aggregate_counts(df, ["q01", "q02"], threshold=5)
    rows = {(r["q01"], r["q02"]): r["count"] for r in result.to_dict("records")}
    assert rows == {("20s", "Female"): 5, ("30s", "Male"): 5}


def test_aggregate_counts_missing_column_returns_empty():
    """aggregate_counts returns an empty table if no column is present."""
    df = pd.DataFrame({"q01": ["20s"] * 5})
    result = SecureDataHandler.aggregate_counts(df, ["nope"], threshold=5)
    assert result.empty
    assert list(result.columns) == ["nope", "count"]


def test_aggregate_counts_carries_only_categories_and_count():
    """The output never carries free-text or identifying columns."""
    df = pd.DataFrame(
        {
            "q02": ["Male"] * 6,
            "q15": ["verbatim answer"] * 6,
            "timestamp": ["2023-07-15 10:00:00"] * 6,
        }
    )
    result = SecureDataHandler.aggregate_counts(df, ["q02"], threshold=5)
    assert set(result.columns) == {"q02", "count"}


def test_mask_rare_categories_collapses_rare_values():
    """mask_rare_categories replaces values below the threshold."""
    df = pd.DataFrame({"q13_binned": ["20%"] * 6 + ["100%"] * 1 + ["70%"] * 2})
    result = SecureDataHandler.mask_rare_categories(df, ["q13_binned"], threshold=5)
    counts = result["q13_binned"].value_counts().to_dict()
    assert counts == {"20%": 6, "(rare)": 3}


def test_mask_rare_categories_keeps_common_values_and_nan():
    """Common values are untouched and NaN is not masked."""
    df = pd.DataFrame({"c": ["a"] * 5 + ["b"] * 5 + [None] * 2})
    result = SecureDataHandler.mask_rare_categories(df, ["c"], threshold=5)
    assert set(result["c"].dropna()) == {"a", "b"}
    assert result["c"].isna().sum() == 2


def test_mask_rare_categories_custom_placeholder():
    df = pd.DataFrame({"c": ["a"] * 6 + ["z"] * 1})
    result = SecureDataHandler.mask_rare_categories(
        df, ["c"], threshold=5, placeholder="OTHER"
    )
    assert set(result["c"]) == {"a", "OTHER"}


def test_mask_rare_categories_missing_column_warns():
    df = pd.DataFrame({"c": ["a"] * 6})
    result = SecureDataHandler.mask_rare_categories(df, ["nope"], threshold=5)
    assert list(result["c"]) == ["a"] * 6


def test_build_public_dataset_masks_after_k_anonymity():
    """mask_columns is applied after row suppression, catching newly-rare values."""
    # 6 "kept" rows: q10_binned "1" x5, "8" x1 (rare from the start).
    # 2 "rare" rows: a (70s, Male) group dropped by k=5, and they also carry
    # q10_binned "1" -- so "1" stays common, "8" gets masked.
    df = pd.DataFrame(
        {
            "timestamp": ["2023-07-15 10:00:00"] * 8,
            "q01": ["20s"] * 6 + ["70s"] * 2,
            "q02": ["Female"] * 6 + ["Male"] * 2,
            "q10_binned": ["1"] * 5 + ["8"] + ["1"] * 2,
        }
    )
    result = SecureDataHandler.build_public_dataset(
        df,
        free_text_columns=[],
        quasi_identifiers=["q01", "q02"],
        k=5,
        mask_columns=["q10_binned"],
    )
    assert len(result) == 6
    assert set(result["q10_binned"]) == {"1", "(rare)"}
