# Plugin Development

Guide for creating custom survey plugins for titanite.

## Overview

Plugins allow you to add support for new surveys without modifying the core framework. Each plugin implements the `SurveySchema` abstract base class to define survey-specific rules.

## Quick Start

### 1. Create Plugin Structure

```bash
mkdir -p plugins/your_survey
touch plugins/your_survey/__init__.py
touch plugins/your_survey/schema.py
```

### 2. Implement Schema

```python
# plugins/your_survey/schema.py
from titanite.core import SurveySchema, SplitColumnRule, ClusterRule, BinRule

class YourSurveySchema(SurveySchema):
    # Define question categories
    categorical_headers = ["q01", "q02", "q03"]
    numerical_headers = ["q10", "q13"]
    free_text_columns = ["q15", "q16"]

    def get_replace_rules(self) -> dict[str, dict]:
        """Value standardization rules."""
        return {}

    def get_split_rules(self) -> list[SplitColumnRule]:
        """Column splitting rules."""
        return []

    def get_cluster_rules(self) -> list[ClusterRule]:
        """Derived cluster columns."""
        return []

    def get_bin_rules(self) -> list[BinRule]:
        """Numerical binning rules."""
        return []
```

### 3. Use Plugin

```bash
poetry run ti prepare data.csv --plugin plugins.your_survey.YourSurveySchema
```

## Detailed Implementation

### Categorical and Numerical Headers

Define which columns are categorical (discrete) vs numerical (continuous):

```python
class YourSurveySchema(SurveySchema):
    # Categorical: Used for chi-square tests, heatmaps
    categorical_headers = [
        "q01",  # Gender
        "q02",  # Age group
        "q03_regional",  # Geographic region
    ]

    # Numerical: Used for correlation, box plots
    numerical_headers = [
        "q10",  # Likert scale
        "q13",  # Ratio question
    ]

    # Free-text: Stored separately for privacy
    free_text_columns = [
        "q15",  # Comments
        "q16",  # Suggestions
    ]
```

### Value Replacement Rules

Standardize response values for consistency:

```python
def get_replace_rules(self) -> dict[str, dict]:
    """
    Define value replacements for each column.

    Format: {
        'column_name': {
            'original_value': 'standardized_value',
            ...
        }
    }
    """
    return {
        "q01": {
            "Male": "male",
            "M": "male",
            "male": "male",
            "Female": "female",
            "F": "female",
            "female": "female",
            "Other": "other",
        },
        "q02": {
            "Yes": "yes",
            "No": "no",
            "N/A": "na",
        },
    }
```

### Split Rules

Split composite columns (e.g., geographic regions):

```python
from titanite.core import SplitColumnRule

def get_split_rules(self) -> list[SplitColumnRule]:
    """
    Define how to split composite columns.

    Example: "United States - California" →
             "country": "United States",
             "region": "California"
    """
    return [
        SplitColumnRule(
            source_column="q03",  # Input column
            split_char=" - ",      # Delimiter
            target_columns=["country", "region"],  # Output columns
        ),
        SplitColumnRule(
            source_column="q04",
            split_char="|",
            target_columns=["department", "subdept"],
        ),
    ]
```

### Cluster Rules

Create derived columns combining multiple questions:

```python
from titanite.core import ClusterRule

def get_cluster_rules(self) -> list[ClusterRule]:
    """
    Define derived columns combining related questions.

    Example: Combine gender identity (q01) and gender expression (q02)
             into a single clustered column.
    """
    return [
        ClusterRule(
            name="gender_cluster",
            description="Combined gender identity and expression",
            source_columns=["q01", "q02"],
            aggregation_func="combine",  # or "majority_vote", "concatenate"
        ),
        ClusterRule(
            name="experience_level",
            description="Career experience derived from multiple factors",
            source_columns=["q05", "q06", "q07"],
            aggregation_func="majority_vote",
        ),
    ]
```

### Bin Rules

Convert numerical data to categorical bins:

```python
from titanite.core import BinRule

def get_bin_rules(self) -> list[BinRule]:
    """
    Define numerical binning rules.

    Example: Convert numerical age to age groups.
    """
    return [
        BinRule(
            source_column="age",
            target_column="age_group",
            bins=[0, 18, 30, 40, 50, 65, 100],
            labels=["<18", "18-30", "30-40", "40-50", "50-65", "65+"],
        ),
        BinRule(
            source_column="experience_years",
            target_column="experience_level",
            bins=[0, 2, 5, 10, 20],
            labels=["Entry", "Junior", "Senior", "Principal"],
        ),
    ]
```

## Configuration

Create a `config.toml` for your survey in `sandbox/`:

```toml
[questions]
q01 = "Gender identity"
q02 = "Age group"
q03 = "Geographic location"
q04 = "Organization"
q05 = "Years of experience"

[categorical_headers]
default = ["q01", "q02", "q03", "q03_regional"]

[numerical_headers]
default = ["q05"]
```

## Testing Your Plugin

### Unit Test

```python
# tests/test_your_survey_schema.py
import pytest
from plugins.your_survey import YourSurveySchema
import pandas as pd

def test_schema_initialization():
    schema = YourSurveySchema()
    assert schema.categorical_headers
    assert schema.numerical_headers

def test_replace_rules():
    schema = YourSurveySchema()
    rules = schema.get_replace_rules()
    assert "q01" in rules
    assert rules["q01"]["Male"] == "male"

def test_split_rules():
    schema = YourSurveySchema()
    rules = schema.get_split_rules()
    assert len(rules) > 0
    assert rules[0].target_columns

def test_with_real_data():
    """Test plugin with actual survey data."""
    schema = YourSurveySchema()
    df = pd.read_csv("data/test_data/your_survey.csv")

    # Run processing pipeline
    processor = SurveyProcessor(schema)
    result = processor.process(df)

    assert result is not None
    assert len(result) == len(df)
```

### Integration Test

```bash
# Test full pipeline with real data
cd sandbox
poetry run ti prepare ../data/raw_data/your_survey.csv \
  --plugin plugins.your_survey.YourSurveySchema
```

## Best Practices

### 1. Value Standardization

Always convert values to lowercase and consistent format:

```python
def get_replace_rules(self) -> dict[str, dict]:
    return {
        "q01": {
            "YES": "yes",
            "Yes": "yes",
            "yes": "yes",
        },
    }
```

### 2. Documentation

Document each rule clearly:

```python
def get_split_rules(self) -> list[SplitColumnRule]:
    """
    Split geographic data into components.

    Input format: "Country - Region - Subregion"
    Output columns: ["country", "region", "subregion"]
    """
    return [...]
```

### 3. Handle Edge Cases

Consider missing or invalid values:

```python
def get_replace_rules(self) -> dict[str, dict]:
    return {
        "q01": {
            "": "missing",
            "N/A": "missing",
            "Unknown": "missing",
            "Prefer not to answer": "prefer_not_to_answer",
        },
    }
```

### 4. Keep Rules Maintainable

Group related rules together:

```python
def get_replace_rules(self) -> dict[str, dict]:
    gender_rules = {"M": "male", "F": "female"}
    age_rules = {"<18": "under_18", "18-25": "18_25"}
    return {
        "q01": gender_rules,
        "q02": age_rules,
    }
```

### 5. Test with Sample Data

Always test with representative sample data:

```bash
poetry run ti prepare sample_data.csv \
  --plugin plugins.your_survey.YourSurveySchema
```

Verify output:
- All categorical values are in `config.toml` choices
- No unexpected missing values
- Split columns have correct structure
- Binned columns have correct labels

## Common Issues and Solutions

### Plugin Not Found

Ensure the module path is correct:

```bash
# Correct format: plugins.package.ClassName
poetry run ti prepare data.csv --plugin plugins.your_survey.YourSurveySchema

# NOT: plugins/your_survey/YourSurveySchema
# NOT: your_survey.YourSurveySchema
```

### Import Errors

Add plugin to `pyproject.toml` if needed:

```toml
[tool.poetry.plugins."titanite.surveys"]
your_survey = "plugins.your_survey.YourSurveySchema"
```

### Data Type Mismatches

Ensure categorical values match `config.toml`:

```toml
[categorical_choices]
q01 = ["male", "female", "other"]  # Lowercase
```

### Missing Replacements

Check that all observed values have replacement rules:

```bash
# Run validation to find unmapped values
poetry run ti config --questions
```

## Example: ICRC2023Schema

See `plugins/icrc2023/ICRC2023Schema` for a complete reference implementation covering:
- Complex geographic splitting (UN geoscheme)
- Multiple clustering rules
- Sentiment analysis integration
- Free-text response handling

## Next Steps

1. Review the [ICRC2023Schema](../../plugins/icrc2023/) reference implementation
2. Create your survey plugin following the quick start
3. Write unit and integration tests
4. Document your schema in CLAUDE.md
5. Submit a PR with your plugin

For questions, see [Architecture](architecture.md) for design details or [Testing](testing.md) for test guidelines.
