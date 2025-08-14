# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an ICRC2023 Diversity Session survey analysis project called "Titanite" - a Python-based tool for analyzing diversity-related survey data from the International Cosmic Ray Conference 2023. The project analyzes pre-conference (2023-07-09 to 07-21) and post-conference (2023-09-15 to 09-22) survey responses from 295 participants out of 1,406 conference attendees.

## Development Environment

### Setup Commands
```bash
poetry shell
poetry install
ti --help  # Verify installation
```

### Testing
```bash
pytest
```

### Documentation Generation
```bash
cd docs
make html
open _build/html/index.html
```

### Package Updates
Use `update-packages` branch only (GitHub Actions restriction):
```bash
git branch update-packages
git checkout update-packages
poetry show --outdated
poetry add package@latest
# Use conventional commit format: build(pyproject.toml): updated package: x.y.z -> X.Y.Z
```

## Architecture

### Core Components

**CLI Interface (`titanite.cli`)**
- Main entry point via `ti` command
- Commands operate from `sandbox/` directory with `config.toml`
- All commands support `--read_from`, `--write-dir`, `--load_from` parameters

**Data Pipeline**
1. **Raw Data**: CSV files from Google Forms in `data/raw_data/`
2. **Preprocessing** (`titanite.preprocess`): Handles categorical conversion, sentiment analysis, clustering
3. **Analysis** (`titanite.analysis`, `titanite.core`): Statistical analysis and visualization
4. **Configuration** (`titanite.config`): Manages categorical/numerical headers and survey question mappings

**Data Structure**
- Questions numbered q01-q22 with specific data types
- Categorical headers (q01, q02, q03_regional, etc.) vs numerical headers (q10, q13, sentiment scores)
- Geographic data split into regional/subregional components
- Cluster analysis creates derived columns (q01_clustered, q13q14_clustered, etc.)

### Key Workflows

**Data Preprocessing**
```bash
cd sandbox
ti prepare ../data/raw_data/survey.csv
# Outputs: prepared_data.csv, categorical_data.csv, sentiment_data.csv
```

**Statistical Analysis**
```bash
ti chi2  # Chi-square tests for all variable pairs
ti p005 q13 --save  # Extract significant correlations (p < 0.05) for specific column
ti crosstabs --save  # Cross-tabulation analysis
```

**Visualization**
```bash
ti response  # Timeline of survey responses
ti hbars --save  # Histograms for all variables
```

## Data Handling Considerations

**Privacy Protection Requirements**
- Free-text responses (q15-q22) may contain personal information
- Small group statistics risk individual identification
- Implement cell suppression for n<5 cases
- All analysis outputs require privacy review before publication

**Configuration System**
- Survey questions and categories defined in `sandbox/config.toml`
- Categorical variables use ordered categories for consistent plotting
- Geographic data follows UN geoscheme (regional/subregional)

## Jupyter Notebooks

Development notebooks are organized by purpose:
- **Module Development**: `00_config.ipynb`, `01_preprocess.ipynb`, `03_crosstab.ipynb`
- **Analysis**: `10_quick_summary.ipynb`, `30_comments.ipynb`
- **Question-specific**: `q02_gender.ipynb`, `q13_gender_ratio.ipynb`, etc.

## Visualization Stack

Uses Altair for statistical visualizations:
- Categorical vs Categorical → Heatmaps (`mark_rect`)
- Categorical vs Numerical → Box plots (`mark_boxplot`) 
- Numerical vs Numerical → Scatter plots (`mark_point`)
- Text annotations with `mark_text`

Streamlit dashboard available in `sandbox/app.py` for interactive exploration.

## Important File Locations

- **Main package**: `titanite/` (cli.py, preprocess.py, analysis.py, config.py, core.py)
- **Configuration**: `sandbox/config.toml` 
- **Raw data**: `data/raw_data/`
- **Processed data**: `data/test_data/`
- **Documentation**: `docs/` (Sphinx + MyST-NB for Jupyter integration)
- **Analysis notebooks**: `notebooks/`