"""Tests for ICRC2023Schema plugin."""

import pandas as pd
import pytest

from plugins.icrc2023 import ICRC2023Schema
from titanite.core import SurveyProcessor


@pytest.fixture
def sample_icrc_data():
    """Create sample ICRC2023 survey data."""
    return pd.DataFrame({
        "timestamp": ["2023-07-15 10:00:00"],
        "q01": ["30s"],
        "q02": ["Female"],
        "q03": ["Europe / West"],
        "q04": ["Asia / East"],
        "q05": ["Postdoc"],
        "q06": ["Astroparticles"],
        "q07": ["Others"],
        "q08": ["5 years"],
        "q09": ["Yes"],
        "q10": [5],
        "q11": ["Yes"],
        "q12_genderbalance": ["Good"],
        "q12_diversity": ["Good"],
        "q12_equity": ["Good"],
        "q12_inclusion": ["Good"],
        "q13": [15],
        "q14": ["Good"],
        "q15": ["Text response"],
        "q16": ["Another text"],
        "q17_genderbalance": ["Agree"],
        "q17_diversity": ["Agree"],
        "q17_equity": ["Agree"],
        "q17_inclusion": ["Agree"],
        "q18": ["Text"],
        "q19": ["University"],
        "q20": ["Text"],
        "q21": ["Text"],
        "q22": ["Text"],
    })


def test_icrc2023_schema_instantiates():
    """ICRC2023Schema can be instantiated."""
    schema = ICRC2023Schema()
    assert schema is not None


def test_icrc2023_schema_has_correct_attributes():
    """ICRC2023Schema has correct class attributes."""
    schema = ICRC2023Schema()
    assert "q01" in schema.categorical_headers
    assert "q03_regional" in schema.categorical_headers
    assert "q10" in schema.numerical_headers
    assert "q13" in schema.numerical_headers
    assert "q15" in schema.free_text_columns


def test_get_replace_rules():
    """get_replace_rules returns correct q03/q04/q14 replacements."""
    schema = ICRC2023Schema()
    rules = schema.get_replace_rules()

    assert "q03" in rules
    assert rules["q03"]["Prefer not to answer"] == "Prefer not to answer / Prefer not to answer"
    assert rules["q03"]["Oceania"] == "Oceania / Oceania"

    assert "q04" in rules
    assert rules["q04"]["Prefer not to answer"] == "Prefer not to answer / Prefer not to answer"

    assert "q14" in rules
    assert rules["q14"]["No Interest"] == "No interest"


def test_get_split_rules():
    """get_split_rules returns q03 and q04 geographic splitting."""
    schema = ICRC2023Schema()
    rules = schema.get_split_rules()

    assert len(rules) == 2
    assert rules[0].source_column == "q03"
    assert rules[0].regional_column == "q03_regional"
    assert rules[0].subregional_column == "q03_subregional"

    assert rules[1].source_column == "q04"
    assert rules[1].regional_column == "q04_regional"
    assert rules[1].subregional_column == "q04_subregional"


def test_get_cluster_rules():
    """get_cluster_rules returns 4 cluster definitions."""
    schema = ICRC2023Schema()
    rules = schema.get_cluster_rules()

    assert len(rules) == 4
    output_columns = [r.output_column for r in rules]
    assert "q01_clustered" in output_columns
    assert "q13_clustered" in output_columns
    assert "q01q02_clustered" in output_columns
    assert "q13q14_clustered" in output_columns


def test_get_bin_rules():
    """get_bin_rules returns q10 and q13 binning."""
    schema = ICRC2023Schema()
    rules = schema.get_bin_rules()

    assert len(rules) == 2
    assert rules[0].source_column == "q10"
    assert rules[0].output_column == "q10_binned"
    assert len(rules[0].labels) == 12

    assert rules[1].source_column == "q13"
    assert rules[1].output_column == "q13_binned"
    assert len(rules[1].labels) == 21


def test_cluster_q01_young():
    """_cluster_q01 classifies under 40s as Cluster1."""
    schema = ICRC2023Schema()
    df = pd.DataFrame({"q01": ["20s", "30s", "40s", "50s"]})
    result = schema._cluster_q01(df)

    assert result.iloc[0] == "Cluster1"  # 20s < 40s
    assert result.iloc[1] == "Cluster1"  # 30s < 40s
    assert result.iloc[2] == "Cluster2"  # 40s >= 40s
    assert result.iloc[3] == "Cluster2"  # 50s >= 40s


def test_cluster_q13_ratio():
    """_cluster_q13 classifies female ratio into three groups."""
    schema = ICRC2023Schema()
    df = pd.DataFrame({"q13": [10, 20, 25, 30, 40, 50]})
    result = schema._cluster_q13(df)

    assert result.iloc[0] == "Cluster1"  # 10 <= 20
    assert result.iloc[1] == "Cluster1"  # 20 <= 20
    assert result.iloc[2] == "Others"     # 25 is between
    assert result.iloc[3] == "Others"     # 30 is between
    assert result.iloc[4] == "Cluster2"  # 40 >= 40
    assert result.iloc[5] == "Cluster2"  # 50 >= 40


def test_cluster_q01q02_young_gender():
    """_cluster_q01q02 classifies young female/male."""
    schema = ICRC2023Schema()
    df = pd.DataFrame({
        "q01": ["20s", "20s", "40s", "40s"],
        "q02": ["Female", "Male", "Female", "Male"]
    })
    result = schema._cluster_q01q02(df)

    assert result.iloc[0] == "Cluster1"  # Young, Female
    assert result.iloc[1] == "Cluster2"  # Young, Male
    assert result.iloc[2] == "Others"     # Senior, Female
    assert result.iloc[3] == "Others"     # Senior, Male


def test_cluster_q13q14_ratio_satisfaction():
    """_cluster_q13q14 classifies ratio-satisfaction."""
    schema = ICRC2023Schema()
    df = pd.DataFrame({
        "q13": [15, 15, 30, 30],
        "q14": ["Poor", "Good", "Poor", "Good"]
    })
    result = schema._cluster_q13q14(df)

    assert result.iloc[0] == "Cluster1"  # <25%, Poor
    assert result.iloc[1] == "Others"     # <25%, Good
    assert result.iloc[2] == "Others"     # >25%, Poor
    assert result.iloc[3] == "Cluster2"  # >25%, Good


def test_survey_processor_with_icrc2023_schema(sample_icrc_data):
    """SurveyProcessor works with ICRC2023Schema."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(sample_icrc_data, config=None)

    # Verify all expected columns exist
    assert "timestamp" in result.columns
    assert "response" in result.columns
    assert "q01_clustered" in result.columns
    assert "q13_clustered" in result.columns
    assert "q01q02_clustered" in result.columns
    assert "q13q14_clustered" in result.columns
    assert "q10_binned" in result.columns
    assert "q13_binned" in result.columns
    assert "q03_regional" in result.columns
    assert "q04_regional" in result.columns


def test_survey_processor_with_icrc2023_processes_values(sample_icrc_data):
    """SurveyProcessor correctly processes ICRC2023 data."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(sample_icrc_data, config=None)

    # Verify clustering
    assert result["q01_clustered"].iloc[0] == "Cluster1"  # 30s < 40s
    assert result["q13_clustered"].iloc[0] == "Cluster1"  # 15 <= 20
    assert result["q01q02_clustered"].iloc[0] == "Cluster1"  # Young, Female

    # Verify geographic split
    assert result["q03_regional"].iloc[0] == "Europe"
    assert result["q03_subregional"].iloc[0] == "West"

    # Verify binning
    assert result["q10_binned"].iloc[0] == "5"  # 5 falls in [4, 5)
    assert result["q13_binned"].iloc[0] == "15%"  # 15 falls in [15, 20)
