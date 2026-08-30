# Quick Start

Get up and running with titanite in minutes.

## Installation

```bash
git clone git@github.com:ICRC2023/surveys.git
cd surveys
uv sync --all-groups
uv run ti --help
```

## Basic workflow

CLI commands run from `sandbox/`, where `config.toml` lives.

### 1. Prepare the data

Process a raw CSV export from Google Forms. Individual-level output goes to
`data/private/` (git-ignored):

```bash
cd sandbox
uv run ti prepare ../data/downloaded/survey.csv --plugin plugins.icrc2023.ICRC2023Schema
```

This writes to `../data/private/`:

- `prepared_data.csv` — one row per respondent, all transformations applied
- `categorical_data.csv` — categorical columns only
- `sentiment_data.csv` — free-text sentiment scores

### 2. Build the publishable extract

Turn the individual-level data into something safe to commit:

```bash
# k-anonymized extract (free text removed, timestamps to the day)
uv run ti anonymize --plugin plugins.icrc2023.ICRC2023Schema

# suppressed frequency tables and cross-tabs (n<5 cells hidden)
uv run ti aggregate --plugin plugins.icrc2023.ICRC2023Schema --pair q01,q02
```

Both write to `../data/public/`, which is committed.

### 3. Analyse

```bash
uv run ti chi2                 # chi-square tests for all variable pairs
uv run ti p005 q13 --save      # significant correlations (p < 0.05) for a column
uv run ti crosstabs --save     # cross-tabulation analysis
```

### 4. Visualise

```bash
uv run ti response             # response timeline heatmap
uv run ti hbars --save         # histograms for all variables
```

## Next steps

- [CLI Commands](cli-commands.md) — full command reference
- [Configuration](configuration.md) — customising survey settings
- [Developer Guide](../developer/index.md) — writing a plugin for a new survey
