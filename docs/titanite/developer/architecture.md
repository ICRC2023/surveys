# Architecture

Overview of titanite's design and core components.

## Core Framework

Titanite is a **pluggable survey processing framework** with a modular architecture designed to support multiple surveys without modifying the core.

### Design Principles

1. **Pluggable** - Survey-specific logic is isolated in plugins
2. **Extensible** - New surveys can be added by implementing a schema interface
3. **Secure** - Built-in privacy protection and data handling
4. **Configurable** - Flexible configuration system for different survey types

## Component Overview

### Core Framework (`titanite/core/`)

**Base Classes:**

- `SurveySchema` - Abstract base class defining survey-specific rules
- `SurveyProcessor` - 8-step processing pipeline for data transformation

**Data Classes:**

- `SplitColumnRule` - Define how to split composite columns (e.g., geographic regions)
- `ClusterRule` - Define derived cluster columns from multiple questions
- `BinRule` - Define numerical column binning rules

**Security:**

- `SecureDataHandler` - Privacy protection (load, suppress, anonymize)

### Plugin System (`plugins/`)

Each survey gets its own plugin implementing `SurveySchema`:

**Example: ICRC2023 Survey**

```
plugins/icrc2023/
├── __init__.py
└── ICRC2023Schema
    ├── categorical_headers
    ├── numerical_headers
    ├── free_text_columns
    └── Methods:
        ├── get_replace_rules()
        ├── get_split_rules()
        ├── get_cluster_rules()
        ├── get_bin_rules()
```

### CLI Interface (`titanite/cli.py`)

Main entry point via `ti` command. Commands are organized by function:

- **Configuration**: `config`
- **Data Preparation**: `prepare`
- **Analysis**: `chi2`, `p005`, `crosstabs`, `crosstab`
- **Visualization**: `response`, `hbars`, `hbar`
- **Text Analysis**: `comments`

## Data Processing Pipeline

The `SurveyProcessor` implements an 8-step pipeline:

```
1. Timestamp Normalization
   ↓
2. Response Counting
   ↓
3. Value Replacement (standardization)
   ↓
4. Column Splitting (geographic/composite)
   ↓
5. Clustering (derived columns)
   ↓
6. Binning (numerical → categorical)
   ↓
7. Data Validation
   ↓
8. Output Generation
```

### Step Details

**1. Timestamp Normalization**
- Standardize timestamp formats
- Handle timezone conversions
- Create response timeline data

**2. Response Counting**
- Track total responses per variable
- Identify missing/invalid responses

**3. Value Replacement**
- Standardize response values (plugin-specific)
- Map synonyms to canonical forms
- Handle encoding issues

**4. Column Splitting**
- Split composite columns (e.g., "Country - Region" → "country", "region", "subregion")
- Apply geographic schema (UN geoscheme)
- Create derived location columns

**5. Clustering**
- Create derived columns combining multiple questions
- Example: combine q13 and q14 gender ratio questions into q13q14_clustered

**6. Binning**
- Convert numerical variables to categorical bins
- Apply equal-width or equal-frequency binning
- Create interpretable categories

**7. Data Validation**
- Check for missing values
- Validate categorical values against schema
- Flag outliers and anomalies

**8. Output Generation**
- Write processed datasets
- Generate metadata
- Create data quality reports

## File Structure

```
titanite/
├── __init__.py
├── cli.py              # CLI entry point
├── config.py           # Configuration management
├── core/
│   ├── __init__.py
│   ├── schema.py       # SurveySchema base class
│   ├── processor.py    # SurveyProcessor pipeline
│   └── security.py     # SecureDataHandler
├── analysis.py         # Statistical analysis functions
└── preprocess.py       # Preprocessing utilities

plugins/
├── __init__.py
└── icrc2023/
    ├── __init__.py
    └── ICRC2023Schema  # Survey-specific implementation

tests/
├── test_core.py
├── test_schema.py
├── test_processor.py
└── test_icrc2023_schema.py

sandbox/
├── config.toml         # Survey configuration
└── app.py              # Streamlit dashboard

data/
├── raw_data/           # Raw survey CSV files
└── test_data/          # Test datasets
```

## Data Structure

### Categorical Variables

Questions treated as discrete categories:
- q01, q02, q03 (demographic data)
- q03_regional, q03_subregional (geographic splits)
- Derived: q01_clustered, q13q14_clustered

Each categorical variable has defined valid choices in `config.toml`.

### Numerical Variables

Questions treated as continuous values:
- q10, q13 (ratio/scale questions)
- Sentiment scores (derived from text analysis)

### Free-text Columns

Questions with written responses:
- q15-q22 (participant comments and feedback)

Stored separately for privacy protection.

## Key Workflows

### Adding a New Survey

1. Create plugin: `plugins/your_survey/`
2. Implement `SurveySchema` with rule methods
3. Define `categorical_headers`, `numerical_headers`, `free_text_columns`
4. Implement rule methods:
   - `get_replace_rules()` - value standardization
   - `get_split_rules()` - column splitting
   - `get_cluster_rules()` - derived columns
   - `get_bin_rules()` - numerical binning
5. Register plugin in `pyproject.toml` entry points
6. Add configuration to `sandbox/config.toml`

### Custom Analysis

1. Create analysis function in `titanite/analysis.py`
2. Add CLI command in `titanite/cli.py`
3. Use `SurveyProcessor` for data preparation
4. Implement visualization with Altair/Matplotlib
5. Add tests to `tests/`

## Testing Strategy

- **Unit Tests** - Test individual components (schema, rules)
- **Integration Tests** - Test full pipeline with real data
- **Plugin Tests** - Test survey-specific implementations

Run with:

```bash
poetry run pytest tests/ -v
```

See [Testing](testing.md) for comprehensive guide.

## Security Considerations

### Privacy Protection

- Free-text responses stored separately
- Cell suppression for small groups (n < 5)
- Anonymization support via `SecureDataHandler`

### Data Validation

- Input validation at system boundaries
- Type checking in dataclasses
- Configuration validation

### Access Control

- Configuration-based access rules
- Plugin isolation
- No credentials in code (use environment variables)

## Dependencies

Core dependencies:

- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scipy** - Statistical analysis
- **altair** - Visualization
- **click** - CLI framework
- **pydantic** - Data validation
- **pyarrow** - Data I/O

Development dependencies:

- **pytest** - Testing framework
- **sphinx** - Documentation
- **ruff** - Code linting/formatting
- **pre-commit** - Git hooks

See `pyproject.toml` for complete dependency list.

## Performance Considerations

- **Data Loading** - Uses pandas for efficient I/O
- **Processing** - Vectorized operations where possible
- **Memory** - Streaming large files to avoid loading entire dataset
- **Caching** - Configuration caching for repeated CLI calls

## Visualization Stack

- **Altair** - Interactive statistical visualizations
- **Matplotlib** - Static plots and fine-grained control
- **Streamlit** - Interactive dashboard (`sandbox/app.py`)

Visualization types:

- Categorical vs Categorical → Heatmaps (`mark_rect`)
- Categorical vs Numerical → Box plots (`mark_boxplot`)
- Numerical vs Numerical → Scatter plots (`mark_point`)
