# Testing

Testing strategy and guidelines for titanite development.

## Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── test_core.py                    # Core framework tests
├── test_schema.py                  # SurveySchema base class tests
├── test_processor.py               # SurveyProcessor pipeline tests
├── test_icrc2023_schema.py         # ICRC2023 plugin tests
└── test_integration_real_world.py  # Full pipeline integration tests
```

## Running Tests

### Run All Tests

```bash
poetry run pytest tests/ -v
```

### Run Specific Test File

```bash
poetry run pytest tests/test_icrc2023_schema.py -v
```

### Run Specific Test

```bash
poetry run pytest tests/test_processor.py::test_pipeline_basic -v
```

### Run with Coverage

```bash
poetry run pytest --cov=titanite tests/
```

### Run Tests in Watch Mode

```bash
poetry run pytest tests/ -v --tb=short -x
```

## Test Categories

### Unit Tests

Test individual components in isolation.

**Example: Testing SurveySchema**

```python
def test_schema_categorical_headers():
    """Test that categorical headers are properly defined."""
    schema = YourSurveySchema()
    assert isinstance(schema.categorical_headers, list)
    assert len(schema.categorical_headers) > 0

def test_replace_rules_format():
    """Test that replace rules have correct structure."""
    schema = YourSurveySchema()
    rules = schema.get_replace_rules()

    for column, replacements in rules.items():
        assert isinstance(replacements, dict)
        for old_val, new_val in replacements.items():
            assert isinstance(old_val, str)
            assert isinstance(new_val, str)
```

**Example: Testing SurveyProcessor**

```python
def test_processor_initialization():
    """Test that processor initializes correctly."""
    schema = YourSurveySchema()
    processor = SurveyProcessor(schema)
    assert processor.schema is not None

def test_processor_steps():
    """Test individual processing steps."""
    schema = YourSurveySchema()
    processor = SurveyProcessor(schema)

    # Create test data
    df = pd.DataFrame({"q01": ["Male", "Female"]})

    # Process
    result = processor.process(df)

    assert result is not None
    assert "q01" in result.columns
```

### Integration Tests

Test the full pipeline with real or realistic data.

**Example: Full Pipeline Test**

```python
def test_integration_full_pipeline():
    """Test complete data processing pipeline."""
    schema = ICRC2023Schema()
    processor = SurveyProcessor(schema)

    # Load test data
    df = pd.read_csv("data/test_data/icrc2023_sample.csv")

    # Run full pipeline
    result = processor.process(df)

    # Verify output
    assert len(result) == len(df)  # No rows lost
    assert "q01_clustered" in result.columns  # Derived columns created
    assert result["q01"].isna().sum() == 0  # No missing required values
```

### Plugin Tests

Test plugin-specific implementations.

**Example: ICRC2023Schema Tests**

```python
def test_icrc2023_replace_rules():
    """Test ICRC2023-specific value replacements."""
    schema = ICRC2023Schema()
    rules = schema.get_replace_rules()

    # Test gender mappings
    assert rules["q01"]["Man"] == "man"
    assert rules["q01"]["Woman"] == "woman"

def test_icrc2023_geographic_splitting():
    """Test UN geoscheme geographic splitting."""
    schema = ICRC2023Schema()
    rules = schema.get_split_rules()

    # Verify geographic splits are configured
    geo_rules = [r for r in rules if "region" in r.target_columns]
    assert len(geo_rules) > 0

def test_icrc2023_clustering():
    """Test ICRC2023 clustering rules."""
    schema = ICRC2023Schema()
    rules = schema.get_cluster_rules()

    # Verify expected cluster columns
    cluster_names = [r.name for r in rules]
    assert "q13q14_clustered" in cluster_names
```

## Test Data

### Using Fixtures

Create reusable test data fixtures:

```python
import pytest
import pandas as pd

@pytest.fixture
def sample_survey_data():
    """Sample survey data for testing."""
    return pd.DataFrame({
        "q01": ["Male", "Female", "Other"],
        "q02": ["Yes", "No", "Yes"],
        "q03": ["United States - California", "UK - London", "Japan - Tokyo"],
        "q10": [1.5, 2.3, 3.1],
    })

@pytest.fixture
def icrc2023_schema():
    """ICRC2023 survey schema."""
    return ICRC2023Schema()

def test_with_fixture(sample_survey_data, icrc2023_schema):
    processor = SurveyProcessor(icrc2023_schema)
    result = processor.process(sample_survey_data)
    assert len(result) == 3
```

### Test Data Files

Keep test data in `data/test_data/`:

```
data/test_data/
├── icrc2023_sample.csv        # Small sample (5-10 rows)
├── icrc2023_edge_cases.csv    # Edge cases (missing values, etc.)
└── icrc2023_full.csv          # Full test dataset
```

## Coverage Requirements

Current test coverage: **69 tests** covering:

- Core framework (schema, processor, security)
- Plugin implementations
- Integration scenarios
- Real-world data

**Target:** Maintain >80% code coverage

Run coverage report:

```bash
poetry run pytest --cov=titanite --cov-report=html tests/
open htmlcov/index.html
```

## Best Practices

### 1. Test Names

Use clear, descriptive test names:

```python
# Good
def test_processor_splits_geographic_columns():
    pass

# Bad
def test_split():
    pass
```

### 2. Assertions

Use specific assertions:

```python
# Good
assert result["q01"].dtype == "object"
assert len(result) == 100
assert "q01_clustered" in result.columns

# Bad
assert result is not None
assert True
```

### 3. Test Independence

Each test should be independent:

```python
# Good - Fresh data for each test
def test_replace_rules(sample_data):
    df = sample_data.copy()
    result = processor.process(df)
    assert result is not None

# Bad - Tests depend on shared state
shared_df = None
def test_one():
    global shared_df
    shared_df = load_data()

def test_two():
    result = processor.process(shared_df)  # Depends on test_one
```

### 4. Document Complex Tests

Add docstrings explaining what is being tested:

```python
def test_geographic_splitting_with_missing_regions():
    """
    Test that geographic splitting handles missing region data.

    When a row has only country (no region), the split should:
    - Create country column
    - Leave region column as NaN (not empty string)
    - Not fail processing
    """
    # ... test implementation
```

### 5. Test Edge Cases

Include tests for edge cases:

```python
def test_missing_values():
    """Test handling of missing/empty values."""
    df = pd.DataFrame({
        "q01": ["Male", "", None, "Female"],
    })
    result = processor.process(df)
    assert result is not None

def test_unknown_categories():
    """Test handling of unexpected categorical values."""
    df = pd.DataFrame({
        "q01": ["Male", "Female", "Alien"],
    })
    result = processor.process(df)
    # Should either replace with "other" or raise informative error
```

## Continuous Integration

Tests run automatically on:

1. **Pre-commit** - Before each commit
2. **Pull Request** - Before merge
3. **Main branch** - On every push

See `.github/workflows/` for CI configuration.

### Local Pre-commit Checks

Before pushing, run:

```bash
task test              # Run tests
task format            # Format with ruff
task lint              # Lint with ruff
task pre-commit        # Run all pre-commit checks
```

Or run individually:

```bash
poetry run pytest tests/ -v
poetry run ruff check --fix
poetry run pre-commit run --all-files
```

## Troubleshooting Tests

### Import Errors

Ensure poetry environment is activated:

```bash
poetry run pytest tests/
```

### Test Data Not Found

Tests use relative paths from repository root. Run from root:

```bash
cd /path/to/surveys
poetry run pytest tests/
```

### Fixture Conflicts

Clear pytest cache:

```bash
rm -rf .pytest_cache
poetry run pytest tests/ --cache-clear
```

### Test Timeout

Some integration tests may be slow. Run with timeout:

```bash
poetry run pytest tests/ --timeout=300 -v
```

## Writing Tests for New Features

When adding a new feature:

1. Write failing tests first (TDD approach)
2. Implement the feature
3. Verify tests pass
4. Add edge case tests
5. Run coverage check

Example workflow:

```bash
# 1. Write test for new feature
cat > tests/test_new_feature.py << 'EOF'
def test_new_feature():
    # Feature should do X
    assert new_feature() == expected_result
EOF

# 2. Run test (should fail)
poetry run pytest tests/test_new_feature.py

# 3. Implement feature
# ... edit titanite/

# 4. Run test (should pass)
poetry run pytest tests/test_new_feature.py -v

# 5. Check coverage
poetry run pytest --cov=titanite tests/
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pandas testing utilities](https://pandas.pydata.org/docs/reference/testing.html)
- [Coverage.py](https://coverage.readthedocs.io/)
