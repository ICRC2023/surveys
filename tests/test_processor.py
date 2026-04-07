"""Tests for titanite.core.processor module."""

import pandas as pd
import pytest

from titanite.core import SurveyProcessor
from titanite.core.schema import SurveySchema, SplitColumnRule, ClusterRule, BinRule


class MockSchema(SurveySchema):
    """Minimal schema for testing."""

    categorical_headers = ["q01"]
    numerical_headers = []
    free_text_columns = []

    def get_replace_rules(self):
        return {"q01": {"old_value": "new_value"}}

    def get_split_rules(self):
        return [
            SplitColumnRule(
                source_column="geo",
                delimiter="/",
                regional_column="geo_regional",
                subregional_column="geo_subregional",
            )
        ]

    def get_cluster_rules(self):
        def apply_cluster(df):
            result = pd.Series("Cluster1", index=df.index, dtype=str)
            return result

        return [ClusterRule("clustered", "test cluster", apply_cluster)]

    def get_bin_rules(self):
        return [
            BinRule(
                source_column="num",
                output_column="num_binned",
                bins=[-1, 0, 10, 100],
                labels=["low", "mid", "high"],
                right=False,
            )
        ]


@pytest.fixture
def sample_df():
    """Create a minimal test DataFrame."""
    return pd.DataFrame({
        "timestamp": ["2023-07-15 10:00:00"],
        "q01": ["old_value"],
        "geo": ["Europe / West"],
        "num": [5],
    })


def test_processor_instantiation():
    """SurveyProcessor can be instantiated with a schema."""
    schema = MockSchema()
    processor = SurveyProcessor(schema)
    assert processor.schema is schema


def test_processor_adds_timestamp_column(sample_df):
    """Processor converts timestamp to datetime."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_processor_adds_response_counter(sample_df):
    """Processor adds response counter column."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert "response" in result.columns
    assert result["response"].iloc[0] == 1


def test_processor_applies_replace_rules(sample_df):
    """Processor applies value replacements."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert result["q01"].iloc[0] == "new_value"


def test_processor_splits_geographic_column(sample_df):
    """Processor splits composite columns."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert "geo_regional" in result.columns
    assert "geo_subregional" in result.columns
    assert result["geo_regional"].iloc[0] == "Europe"
    assert result["geo_subregional"].iloc[0] == "West"


def test_processor_applies_cluster_rules(sample_df):
    """Processor applies cluster derivation."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert "clustered" in result.columns
    assert result["clustered"].iloc[0] == "Cluster1"


def test_processor_applies_bin_rules(sample_df):
    """Processor applies binning rules."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)
    assert "num_binned" in result.columns
    # 5 falls into [0, 10) which maps to "mid"
    assert result["num_binned"].iloc[0] == "mid"


def test_processor_full_pipeline(sample_df):
    """Full pipeline produces expected structure."""
    processor = SurveyProcessor(MockSchema())
    result = processor.process(sample_df, config=None)

    # Check all columns are present
    expected_cols = ["timestamp", "q01", "geo", "num", "response",
                     "geo_regional", "geo_subregional", "clustered", "num_binned"]
    for col in expected_cols:
        assert col in result.columns

    # Check data integrity
    assert len(result) == 1
    assert result["q01"].iloc[0] == "new_value"
    assert result["response"].iloc[0] == 1
    assert result["clustered"].iloc[0] == "Cluster1"
