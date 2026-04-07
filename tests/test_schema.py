"""Tests for titanite.core.schema module."""

import pytest

from titanite.core.schema import SurveySchema, SplitColumnRule, BinRule, ClusterRule


def test_survey_schema_is_abstract():
    """SurveySchema cannot be instantiated directly."""
    with pytest.raises(TypeError, match="abstract"):
        SurveySchema()


def test_partial_implementation_not_instantiable():
    """Concrete subclass must implement all abstract methods."""

    class PartialSchema(SurveySchema):
        def get_replace_rules(self):
            return {}

        # Missing: get_split_rules, get_cluster_rules, get_bin_rules

    with pytest.raises(TypeError, match="abstract"):
        PartialSchema()


def test_minimal_schema_instantiates():
    """Minimal concrete implementation is instantiable."""

    class MinimalSchema(SurveySchema):
        def get_replace_rules(self):
            return {}

        def get_split_rules(self):
            return []

        def get_cluster_rules(self):
            return []

        def get_bin_rules(self):
            return []

    schema = MinimalSchema()
    assert schema.categorical_headers == []
    assert schema.numerical_headers == []
    assert schema.free_text_columns == []


def test_schema_class_attributes_can_be_overridden():
    """Class-level attributes override correctly."""

    class CustomSchema(SurveySchema):
        categorical_headers = ["q01", "q02"]
        numerical_headers = ["q10"]
        free_text_columns = ["q15", "q16"]

        def get_replace_rules(self):
            return {}

        def get_split_rules(self):
            return []

        def get_cluster_rules(self):
            return []

        def get_bin_rules(self):
            return []

    schema = CustomSchema()
    assert schema.categorical_headers == ["q01", "q02"]
    assert schema.numerical_headers == ["q10"]
    assert schema.free_text_columns == ["q15", "q16"]


def test_split_column_rule_dataclass():
    """SplitColumnRule stores and retrieves values correctly."""
    rule = SplitColumnRule(
        source_column="q03",
        delimiter="/",
        regional_column="q03_regional",
        subregional_column="q03_subregional",
    )
    assert rule.source_column == "q03"
    assert rule.delimiter == "/"
    assert rule.regional_column == "q03_regional"
    assert rule.subregional_column == "q03_subregional"


def test_bin_rule_dataclass_defaults():
    """BinRule has correct defaults."""
    rule = BinRule(
        source_column="q10",
        output_column="q10_binned",
        bins=[-1, 0, 10],
        labels=["low", "high"],
    )
    assert rule.source_column == "q10"
    assert rule.output_column == "q10_binned"
    assert rule.bins == [-1, 0, 10]
    assert rule.labels == ["low", "high"]
    assert rule.right is False  # default


def test_bin_rule_right_parameter():
    """BinRule right parameter can be overridden."""
    rule = BinRule(
        source_column="q10",
        output_column="q10_binned",
        bins=[-1, 0, 10],
        labels=["low", "high"],
        right=True,
    )
    assert rule.right is True


def test_cluster_rule_dataclass():
    """ClusterRule stores description and callable."""

    def apply_func(df):
        return df

    rule = ClusterRule(
        output_column="q01_clustered",
        description="Age cluster",
        apply=apply_func,
    )
    assert rule.output_column == "q01_clustered"
    assert rule.description == "Age cluster"
    assert rule.apply is apply_func
