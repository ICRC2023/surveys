# Quick Start

Get up and running with titanite in minutes.

## Installation

```bash
git clone git@github.com:ICRC2023/surveys.git
cd surveys
poetry install
```

## Verify Installation

```bash
poetry run ti --help
```

## Basic Workflow

### 1. Prepare Data

Process raw CSV data from Google Forms:

```bash
cd sandbox
poetry run ti prepare ../data/raw_data/survey.csv
```

This generates:
- `prepared_data.csv` - Processed data with all transformations
- `categorical_data.csv` - Categorical variables only
- `sentiment_data.csv` - Sentiment analysis results

### 2. Run Analysis

Analyze the prepared data:

```bash
cd sandbox

# Chi-square tests for all variable pairs
poetry run ti chi2

# Extract significant correlations (p < 0.05)
poetry run ti p005 q13 --save

# Cross-tabulation analysis
poetry run ti crosstabs --save
```

### 3. Generate Visualizations

Create statistical visualizations:

```bash
cd sandbox

# Timeline of survey responses
poetry run ti response

# Histograms for all variables
poetry run ti hbars --save
```

## Next Steps

- See [CLI Commands](cli-commands.md) for full command reference
- See [Configuration](configuration.md) for customizing survey settings
- Check [Development Guide](../developer/index.md) for plugin development
