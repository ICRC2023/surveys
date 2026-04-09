# Titanite Plugin Development Guide

This guide explains how to create a new survey schema plugin for the Titanite framework.

## Overview

Titanite is an abstract framework for processing Google Forms survey data.
Survey-specific preprocessing logic (value replacements, geographic splitting, clustering, binning) is implemented as **plugins** and kept separate from the framework core.

### Benefits

- 🔄 **Reusable**: Support multiple surveys with the same framework
- 📦 **Modular**: Encapsulate survey-specific logic
- 🧪 **Testable**: Test each plugin independently
- 🔒 **Safe**: No impact on framework core

---

## Quick Start

### 1. Create Plugin Structure

```bash
mkdir -p plugins/your_survey/
touch plugins/your_survey/__init__.py
touch plugins/your_survey/schema.py
```

### 2. Implement Schema Class

```python
# plugins/your_survey/schema.py
from titanite.core import SurveySchema, SplitColumnRule, BinRule, ClusterRule
import pandas as pd

class YourSurveySchema(SurveySchema):
    """Your survey-specific schema implementation."""

    categorical_headers = ["q01", "q02", "q03", ...]
    numerical_headers = ["q10", "q13", ...]
    free_text_columns = ["q15", "q16", ...]

    def get_replace_rules(self) -> dict[str, dict]:
        """Return value replacements."""
        return {}

    def get_split_rules(self) -> list[SplitColumnRule]:
        """Return column splitting rules."""
        return []

    def get_cluster_rules(self) -> list[ClusterRule]:
        """Return clustering rules."""
        return []

    def get_bin_rules(self) -> list[BinRule]:
        """Return binning rules."""
        return []
```

### 3. Initialize Plugin

```python
# plugins/your_survey/__init__.py
from plugins.your_survey.schema import YourSurveySchema

__all__ = ["YourSurveySchema"]
```

### 4. Use in CLI

```bash
poetry run ti prepare raw_data.csv --plugin plugins.your_survey.YourSurveySchema
```

---

## Detailed Implementation Guide

### Define Class Attributes

```python
class YourSurveySchema(SurveySchema):
    # All categorical variables from your survey questions
    categorical_headers = [
        "q01", "q02", "q03_regional", "q03_subregional",
        "q04", "q04_regional", "q04_subregional",
        ...
    ]

    # All numerical variables
    numerical_headers = ["q10", "q13", ...]

    # Free-text items (require privacy protection)
    free_text_columns = ["q15", "q16", "q18", ...]
```

### 1. Value Replacements (`get_replace_rules()`)

Some survey responses need standardization before processing.

```python
def get_replace_rules(self) -> dict[str, dict]:
    """Return value replacement rules.

    Examples:
    - "No Interest" → "No interest" (capitalize consistently)
    - "Oceania" → "Oceania / Oceania" (unify format)
    """
    return {
        "q03": {
            "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
            "Oceania": "Oceania / Oceania",
        },
        "q14": {
            "No Interest": "No interest",
        },
    }
```

**Processing in SurveyProcessor:**
```python
data["q03"] = data["q03"].replace(rules["q03"])
```

### 2. Geographic Splitting (`get_split_rules()`)

Split composite columns (e.g., "Europe / West") into regional components.

```python
def get_split_rules(self) -> list[SplitColumnRule]:
    """Return geographic splitting rules.

    Format: "Region / Subregion" → separate into components
    """
    from titanite.core import SplitColumnRule

    return [
        SplitColumnRule(
            source_column="q03",
            delimiter="/",
            regional_column="q03_regional",
            subregional_column="q03_subregional",
        ),
        SplitColumnRule(
            source_column="q04",
            delimiter="/",
            regional_column="q04_regional",
            subregional_column="q04_subregional",
        ),
    ]
```

**Processing in SurveyProcessor:**
```python
# If q03 = "Europe / West":
# q03_regional = "Europe"
# q03_subregional = "West"
```

### 3. Clustering (`get_cluster_rules()`)

Combine multiple columns to create derived variables.

```python
def get_cluster_rules(self) -> list[ClusterRule]:
    """Return clustering rules."""
    from titanite.core import ClusterRule

    return [
        ClusterRule(
            output_column="age_cluster",
            description="Age-based cluster: Cluster1 (under 40s) vs Cluster2 (40+)",
            apply=self._cluster_age,  # Named static method
        ),
        ClusterRule(
            output_column="female_ratio_cluster",
            description="Female ratio cluster: Cluster1 (<=20%) vs Cluster2 (>=40%)",
            apply=self._cluster_female_ratio,
        ),
    ]

@staticmethod
def _cluster_age(df: pd.DataFrame) -> pd.Series:
    """Age-based clustering logic.

    Returns a pandas Series with cluster assignments.
    """
    result = pd.Series("Others", index=df.index, dtype=str)
    result[df["q01"] < "40s"] = "Cluster1"
    result[df["q01"] >= "40s"] = "Cluster2"
    return result

@staticmethod
def _cluster_female_ratio(df: pd.DataFrame) -> pd.Series:
    """Female ratio clustering logic."""
    result = pd.Series("Others", index=df.index, dtype=str)
    result[df["q13"] <= 20] = "Cluster1"
    result[df["q13"] >= 40] = "Cluster2"
    return result
```

**Important**: Use named static methods, not lambdas, in `ClusterRule`:
- ✅ Testable (can have docstrings)
- ✅ Easier to debug (clear stack traces)
- ✅ Better error handling

### 4. Binning (`get_bin_rules()`)

Convert continuous values into discrete categories.

```python
def get_bin_rules(self) -> list[BinRule]:
    """Return binning rules."""
    from titanite.core import BinRule

    return [
        BinRule(
            source_column="q10",
            output_column="q10_binned",
            bins=[-1, 0, 1, 2, 3, 4, 5, 10, 25],
            labels=["Prefer not to answer", "0", "1", "2", "3", "4", "5", "10+"],
            right=False,  # Left-closed intervals [bin_i, bin_{i+1})
        ),
        BinRule(
            source_column="q13",
            output_column="q13_binned",
            bins=[-1, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 105],
            labels=[
                "Prefer not to answer", "0%", "10%", "20%", "30%", "40%",
                "50%", "60%", "70%", "80%", "90%", "100%",
            ],
            right=False,
        ),
    ]
```

---

## Writing Tests

### Basic Tests

```python
# tests/test_your_survey_schema.py
import pandas as pd
import pytest
from plugins.your_survey import YourSurveySchema
from titanite.core import SurveyProcessor


@pytest.fixture
def sample_data():
    """Create sample survey data."""
    return pd.DataFrame({
        "timestamp": ["2024-01-15 10:00:00"],
        "q01": ["30s"],
        "q02": ["Female"],
        "q03": ["Europe / West"],
        ...
    })


def test_schema_instantiation():
    """Schema can be instantiated."""
    schema = YourSurveySchema()
    assert schema is not None


def test_get_replace_rules():
    """Replace rules are defined."""
    schema = YourSurveySchema()
    rules = schema.get_replace_rules()
    assert isinstance(rules, dict)


def test_get_split_rules():
    """Split rules are defined."""
    schema = YourSurveySchema()
    rules = schema.get_split_rules()
    assert isinstance(rules, list)


def test_processor_integration(sample_data):
    """SurveyProcessor works with this schema."""
    schema = YourSurveySchema()
    processor = SurveyProcessor(schema)
    result = processor.process(sample_data)

    # Verify expected columns exist
    assert "timestamp" in result.columns
    assert "response" in result.columns
    # Add more assertions for your specific columns
```

---

## Best Practices

### ✅ DO

1. **Use named static methods** — not lambdas
   ```python
   @staticmethod
   def _cluster_age(df: pd.DataFrame) -> pd.Series:
       """Clear docstring explaining the clustering logic."""
       ...
   ```

2. **Define class attributes** — explicitly list all processed columns
   ```python
   categorical_headers = [...]
   numerical_headers = [...]
   free_text_columns = [...]
   ```

3. **Write comprehensive tests** — test each rule individually
   ```python
   def test_get_replace_rules():
   def test_get_split_rules():
   def test_get_cluster_rules():
   def test_get_bin_rules():
   def test_processor_integration():
   ```

4. **Handle errors** — catch exceptions in cluster rules
   ```python
   @staticmethod
   def _cluster_age(df: pd.DataFrame) -> pd.Series:
       try:
           # clustering logic
       except KeyError:
           logger.warning("Required column missing")
           return pd.Series("Unknown", index=df.index)
   ```

### ❌ DON'T

1. **Modify global state** — keep functions pure
   ```python
   # ❌ BAD
   @staticmethod
   def _cluster_age(df):
       df.loc[..., "temp_col"] = ...  # Side effect!

   # ✅ GOOD
   @staticmethod
   def _cluster_age(df):
       result = pd.Series(...)
       return result
   ```

2. **Hardcode values** — define everything as rules
   ```python
   # ❌ BAD
   result[df["q01"] < "40s"] = "Young"  # Hardcoded string

   # ✅ GOOD
   result[df["q01"] < "40s"] = "Cluster1"  # Defined in rule
   ```

3. **Mix responsibilities** — Single Responsibility Principle
   ```python
   # ❌ BAD: Multiple rules in one function
   def _complex_cluster(df):
       # clustering + binning + replacement

   # ✅ GOOD: Each rule is independent
   def _cluster_age(df): ...
   def _bin_age(df): ...
   def _replace_age(df): ...
   ```

---

## Example: ICRC2023Schema

For a complete implementation example, see the existing ICRC2023Schema:

```
plugins/icrc2023/schema.py  — Full implementation (300 lines)
tests/test_icrc2023_schema.py  — Test examples (12 tests)
```

### Usage

```bash
# Use ICRC2023Schema
poetry run ti prepare raw_survey.csv --plugin plugins.icrc2023.ICRC2023Schema

# Default (backward compatible)
poetry run ti prepare raw_survey.csv
```

---

## Troubleshooting

### Plugin cannot be loaded

```
Failed to load plugin 'plugins.your_survey.YourSurveySchema': No module named 'plugins.your_survey'
```

**Solution:**
1. Verify `plugins/your_survey/__init__.py` exists
2. Add `from plugins.your_survey.schema import YourSurveySchema` to __init__.py
3. Check file paths are correct

### Clustering results are unexpected

```python
# Verify with tests
def test_cluster_age():
    df = pd.DataFrame({"q01": ["20s", "30s", "40s", "50s"]})
    result = YourSurveySchema._cluster_age(df)
    assert result[0] == "Cluster1"  # 20s < 40s
    assert result[2] == "Cluster2"  # 40s >= 40s
```

### Processor is removing columns

Check:
- Is the column name in `categorical_headers`?
- Is it in `numerical_headers`?
- Is it in `free_text_columns`?

---

## Next Steps

After creating a plugin:

1. **Run tests** — `poetry run pytest tests/test_your_survey_schema.py -v`
2. **Test CLI** — `poetry run ti prepare data.csv --plugin plugins.your_survey.YourSurveySchema`
3. **Document** — Add plugin description to README.md
4. **Create PR** — Submit a pull request on GitHub

---

## References

- [CLAUDE.md](CLAUDE.md) — Project-wide guidelines
- [titanite/core/schema.py](titanite/core/schema.py) — Framework ABC definitions
- [titanite/core/processor.py](titanite/core/processor.py) — Pipeline implementation
- [plugins/icrc2023/](plugins/icrc2023/) — Complete implementation example

---

## Support

For questions or bug reports, create an issue on [GitHub Issues](https://github.com/ICRC2023/surveys/issues).
