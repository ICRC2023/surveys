"""Integration tests for real-world survey processing scenarios."""

import pandas as pd
import pytest

from plugins.icrc2023 import ICRC2023Schema
from titanite.core import SurveyProcessor


@pytest.fixture
def minimal_survey_data():
    """Minimal ICRC2023 survey data with required columns."""
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


@pytest.fixture
def diverse_survey_data():
    """Survey data with diverse demographics and responses."""
    return pd.DataFrame({
        "timestamp": [
            "2023-07-15 09:00:00",
            "2023-07-15 10:00:00",
            "2023-07-15 11:00:00",
            "2023-07-15 12:00:00",
        ],
        "q01": ["20s", "30s", "40s", "50s"],
        "q02": ["Female", "Male", "Female", "Male"],
        "q03": [
            "Europe / West",
            "Asia / East",
            "Americas / North America",
            "Africa / West Africa",
        ],
        "q04": [
            "Europe / West",
            "Asia / East",
            "Americas / North America",
            "Africa / West Africa",
        ],
        "q05": ["Postdoc", "Faculty", "Graduate student", "Senior faculty"],
        "q06": ["Astroparticles", "Cosmology", "Instrumentation", "Theory"],
        "q07": ["High energy physics", "Astrophysics", "Others", "Astroparticles"],
        "q08": ["3 years", "10 years", "2 years", "15 years"],
        "q09": ["Yes", "Yes", "No", "Yes"],
        "q10": [3, 8, 0, 12],
        "q11": ["Yes", "No", "Yes", "No"],
        "q12_genderbalance": ["Good", "Poor", "Fair", "Excellent"],
        "q12_diversity": ["Fair", "Poor", "Good", "Good"],
        "q12_equity": ["Fair", "Poor", "Good", "Excellent"],
        "q12_inclusion": ["Good", "Poor", "Fair", "Good"],
        "q13": [10, 30, 25, 45],
        "q14": ["Poor", "Very Poor", "Good", "Very Good"],
        "q15": ["Response 1", "Response 2", "Response 3", "Response 4"],
        "q16": ["Text 1", "Text 2", "Text 3", "Text 4"],
        "q17_genderbalance": ["Disagree", "Strongly Disagree", "Agree", "Strongly Agree"],
        "q17_diversity": ["Agree", "Disagree", "Agree", "Strongly Agree"],
        "q17_equity": ["Neutral", "Disagree", "Agree", "Agree"],
        "q17_inclusion": ["Agree", "Disagree", "Neutral", "Strongly Agree"],
        "q18": ["T1", "T2", "T3", "T4"],
        "q19": ["University", "Institute", "University", "Lab"],
        "q20": ["X", "Y", "Z", "W"],
        "q21": ["A", "B", "C", "D"],
        "q22": ["P", "Q", "R", "S"],
    })


def test_processor_handles_minimal_data(minimal_survey_data):
    """Processor works with minimal required data."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(minimal_survey_data)

    assert len(result) == 1
    assert "response" in result.columns
    assert result["response"].iloc[0] == 1


def test_processor_handles_diverse_demographics(diverse_survey_data):
    """Processor correctly clusters diverse demographic groups."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # Verify clustering results
    assert result["q01_clustered"].iloc[0] == "Cluster1"  # 20s < 40s
    assert result["q01_clustered"].iloc[2] == "Cluster2"  # 40s >= 40s

    # Verify female ratio clustering
    assert result["q13_clustered"].iloc[0] == "Cluster1"  # 10 <= 20
    assert result["q13_clustered"].iloc[2] == "Others"     # 25 is in between
    assert result["q13_clustered"].iloc[3] == "Cluster2"  # 45 >= 40


def test_geographic_splitting_multiple_regions(diverse_survey_data):
    """Geographic splitting works across different regions."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # Verify q03 splitting
    assert result["q03_regional"].iloc[0] == "Europe"
    assert result["q03_subregional"].iloc[0] == "West"

    assert result["q03_regional"].iloc[2] == "Americas"
    assert result["q03_subregional"].iloc[2] == "North America"

    # Verify q04 splitting
    assert result["q04_regional"].iloc[3] == "Africa"
    assert result["q04_subregional"].iloc[3] == "West Africa"


def test_binning_invited_speakers(diverse_survey_data):
    """Binning correctly categorizes number of invited speakers."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # q10 = [3, 8, 0, 12]
    assert result["q10_binned"].iloc[0] == "3"     # 3 falls in [3, 4)
    assert result["q10_binned"].iloc[1] == "8"     # 8 falls in [8, 9)
    assert result["q10_binned"].iloc[2] == "0"     # 0 falls in [0, 1)
    assert result["q10_binned"].iloc[3] == "10+"   # 12 >= 10


def test_binning_female_ratio(diverse_survey_data):
    """Binning correctly categorizes female ratio percentages."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # q13 = [10, 30, 25, 45]
    assert result["q13_binned"].iloc[0] == "10%"   # 10 falls in [10, 15)
    assert result["q13_binned"].iloc[1] == "30%"   # 30 falls in [30, 35)
    assert result["q13_binned"].iloc[2] == "25%"   # 25 falls in [25, 30)
    assert result["q13_binned"].iloc[3] == "45%"   # 45 falls in [45, 50)


def test_young_female_male_clustering(diverse_survey_data):
    """Young female/male clustering correctly identifies demographic subgroups."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # q01q02_clustered
    # Row 0: q01="20s" (young), q02="Female" → Cluster1
    assert result["q01q02_clustered"].iloc[0] == "Cluster1"
    # Row 1: q01="30s" (young), q02="Male" → Cluster2
    assert result["q01q02_clustered"].iloc[1] == "Cluster2"
    # Row 2: q01="40s" (not young), q02="Female" → Others
    assert result["q01q02_clustered"].iloc[2] == "Others"
    # Row 3: q01="50s" (not young), q02="Male" → Others
    assert result["q01q02_clustered"].iloc[3] == "Others"


def test_ratio_satisfaction_clustering(diverse_survey_data):
    """Ratio-satisfaction clustering identifies extremes."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    # q13q14_clustered
    # Row 0: q13=10 (<25), q14="Poor" → Cluster1
    assert result["q13q14_clustered"].iloc[0] == "Cluster1"
    # Row 1: q13=30 (>25), q14="Very Poor" → Others (not exactly good)
    assert result["q13q14_clustered"].iloc[1] == "Others"
    # Row 2: q13=25 (not >25), q14="Good" → Others
    assert result["q13q14_clustered"].iloc[2] == "Others"
    # Row 3: q13=45 (>25), q14="Very Good" → Cluster2
    assert result["q13q14_clustered"].iloc[3] == "Cluster2"


def test_value_replacements_applied(minimal_survey_data):
    """Value replacements are correctly applied."""
    # Create data with values that need replacement
    data = minimal_survey_data.copy()
    data["q03"] = ["Oceania"]
    data["q14"] = ["No Interest"]

    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(data)

    # Verify replacements
    assert result["q03"].iloc[0] == "Oceania / Oceania"
    assert result["q14"].iloc[0] == "No interest"


def test_pipeline_preserves_row_count(diverse_survey_data):
    """Processing pipeline preserves the number of rows."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(diverse_survey_data)

    assert len(result) == len(diverse_survey_data)


def test_pipeline_adds_derived_columns(minimal_survey_data):
    """Pipeline adds all expected derived columns."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)
    result = processor.process(minimal_survey_data)

    # Added by pipeline
    expected_columns = [
        "timestamp",
        "response",
        "q03_regional",
        "q03_subregional",
        "q04_regional",
        "q04_subregional",
        "q01_clustered",
        "q13_clustered",
        "q01q02_clustered",
        "q13q14_clustered",
        "q10_binned",
        "q13_binned",
    ]

    for col in expected_columns:
        assert col in result.columns, f"Missing column: {col}"


def test_multiple_responses_independence(diverse_survey_data):
    """Each response is processed independently (no data leakage)."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)

    # Process all at once
    result_batch = processor.process(diverse_survey_data)

    # Process each row individually
    results_individual = []
    for idx in range(len(diverse_survey_data)):
        single_row = diverse_survey_data.iloc[[idx]]
        result_single = processor.process(single_row)
        results_individual.append(result_single)

    # Compare clusterings for first row
    for col in ["q01_clustered", "q13_clustered", "q01q02_clustered", "q13q14_clustered"]:
        assert result_batch[col].iloc[0] == results_individual[0][col].iloc[0]
