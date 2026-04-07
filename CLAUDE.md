# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an ICRC2023 Diversity Session survey analysis project called "Titanite" - a Python-based tool for analyzing diversity-related survey data from the International Cosmic Ray Conference 2023. The project analyzes pre-conference (2023-07-09 to 07-21) and post-conference (2023-09-15 to 09-22) survey responses from 295 participants out of 1,406 conference attendees.

## Quick Start

```bash
# Clone and setup
git clone git@github.com:ICRC2023/surveys.git
cd surveys
poetry install

# Verify installation
poetry run ti --help

# Run tests
task test

# Serve documentation
task docs:serve
```

## Directory Structure

- **`titanite/`** - Main Python package (cli.py, config.py, core.py, analysis.py, preprocess.py)
- **`tests/`** - Test suite with pytest configuration
- **`sandbox/`** - Configuration file (config.toml) and CLI working directory
- **`data/`** - Survey data (raw_data/, test_data/)
- **`docs/`** - Sphinx documentation site
- **`notebooks/`** - Development and analysis Jupyter Notebooks
- **`Taskfile.yml`** - Task automation for common operations
- **`pyproject.toml`**, **`poetry.lock`** - Dependency management

## Architecture

### Core Components

**CLI Interface (`titanite.cli`)**
- Main entry point via `ti` command (use `poetry run ti`)
- Commands operate from `sandbox/` directory with `config.toml`
- Most commands support `--read_from`, `--write-dir`, `--load_from` parameters

**Available CLI Commands:**

- `ti config` - Show configuration (supports `--questions`, `--choices` flags)
- `ti prepare` - Preprocess raw CSV data and generate prepared_data.csv
- `ti comments` - Extract and analyze free-text responses (q15-q22)
- `ti response` - Create response timeline heatmap
- `ti hbar` - Create histogram for a single variable (WIP)
- `ti hbars` - Create histograms for all variables
- `ti crosstab` - Create single crosstab (WIP)
- `ti crosstabs` - Create crosstabs for all variable pairs
- `ti chi2` - Run chi-square tests for all variable pairs
- `ti p005` - Extract significant correlations (p < 0.05) for specific column with `--save` flag

**Data Pipeline**

1. **Raw Data**: CSV files from Google Forms in `data/raw_data/`
2. **Preprocessing** (`titanite.preprocess`): Categorical conversion, sentiment analysis, clustering
3. **Analysis** (`titanite.analysis`, `titanite.core`): Statistical analysis and visualization
4. **Configuration** (`titanite.config`): Categorical/numerical headers and survey question mappings

**Data Structure**

- Questions numbered q01-q22 with specific data types
- Categorical headers (q01, q02, q03_regional, etc.) vs numerical headers (q10, q13, sentiment scores)
- Geographic data split into regional/subregional components (UN geoscheme)
- Cluster analysis creates derived columns (q01_clustered, q13q14_clustered, etc.)

### Key Workflows

**Data Preprocessing**
```bash
cd sandbox
poetry run ti prepare ../data/raw_data/survey.csv
# Outputs: prepared_data.csv, categorical_data.csv, sentiment_data.csv
```

**Statistical Analysis**
```bash
cd sandbox
poetry run ti chi2                    # Chi-square tests for all variable pairs
poetry run ti p005 q13 --save         # Extract significant correlations (p < 0.05)
poetry run ti crosstabs --save        # Cross-tabulation analysis
```

**Visualization**
```bash
cd sandbox
poetry run ti response                # Timeline of survey responses
poetry run ti hbars --save            # Histograms for all variables
```

### Data Handling Considerations

**Privacy Protection Requirements**
- Free-text responses (q15-q22) may contain personal information
- Small group statistics risk individual identification
- Implement cell suppression for n<5 cases
- All analysis outputs require privacy review before publication

**Configuration System**
- Survey questions and categories defined in `sandbox/config.toml`
- Categorical variables use ordered categories for consistent plotting
- Geographic data follows UN geoscheme (regional/subregional)

### Visualization Stack

Uses Altair for statistical visualizations:
- Categorical vs Categorical → Heatmaps (`mark_rect`)
- Categorical vs Numerical → Box plots (`mark_boxplot`)
- Numerical vs Numerical → Scatter plots (`mark_point`)
- Text annotations with `mark_text`

Streamlit dashboard available in `sandbox/app.py` for interactive exploration.

## Development Environment

### Common Tasks (Taskfile.yml)

The project uses Taskfile for task automation. Run `task` to see all available tasks:

```bash
# Development setup
task env:setup          # Set up development environment
task env:clean          # Clean build artifacts

# Code quality
task test               # Run pytest
task format             # Format code with ruff
task lint               # Lint code with ruff
task pre-commit         # Run pre-commit hooks

# Documentation
task docs:build         # Build Sphinx docs
task docs:serve         # Serve docs at http://localhost:8000 with auto-reload

# Dependencies
task deps:check         # Check for outdated packages
task deps:update        # Update all dependencies

# CLI
task cli:help           # Show CLI help
```

### Documentation Generation

```bash
# Using Taskfile (recommended)
task docs:serve         # Auto-reload at http://localhost:8000
task docs:build         # One-time build

# Manual build
cd docs
poetry run sphinx-build -b html . _build/html
open _build/html/index.html
```

### Jupyter Notebooks

Development notebooks are organized by purpose:
- **Module Development**: `00_config.ipynb`, `01_preprocess.ipynb`, `03_crosstab.ipynb`
- **Analysis**: `10_quick_summary.ipynb`, `30_comments.ipynb`
- **Question-specific**: `q02_gender.ipynb`, `q13_gender_ratio.ipynb`, etc.

## Development Workflow

### Git Worktree for Branch Development

This project uses `git worktree` for isolated branch development to avoid conflicts and enable parallel development:

```bash
# Create worktree for feature branch
git worktree add ../worktrees/<directory_name> -b <new-branch-name>
cd ../worktrees/<directory_name>

# Setup and develop
task env:setup         # Set up isolated environment
# ... implement features ...

# Test and format before committing
task test              # Run tests
task format            # Format with ruff
task lint              # Lint with ruff
task pre-commit        # Run pre-commit hooks

# Commit and push
git add <files>
git commit -m "type(scope): message"
git push origin <new-branch-name>

# After PR merge, clean up
cd ../../surveys
git fetch --prune
git pull
git worktree remove ../worktrees/<directory_name>
```

### GitHub Issue-Driven Development

```bash
# List and view issues
gh issue list
gh issue view <issue-number>

# Create worktree for issue
git worktree add ../worktrees/<issue-branch-name> -b <issue-branch-name>
cd ../worktrees/<issue-branch-name>

# Develop (same workflow as above)
task env:setup
# ... implement fix/feature ...
task test && task format && task pre-commit

# Create PR referencing the issue
gh pr create --title "fix: <description>" --body "Closes #<issue-number>"

# Clean up after merge (see worktree workflow above)
```

**Development Guidelines:**
- Always reference issue numbers in commit messages and PR descriptions
- Use `Closes #<issue-number>` in PR descriptions to auto-close issues
- Create PRs for all changes, even small fixes
- Run all tests and hooks before creating PR

### Package Updates

Use `update-packages` branch only (GitHub Actions restriction):

```bash
# Create isolated worktree for updates
git worktree add ../worktrees/update-packages -b update-packages
cd ../worktrees/update-packages

# Update and test
task deps:check        # Check outdated packages
task deps:update       # Update all dependencies
task test              # Verify tests pass

# Commit and push
git add poetry.lock
git commit -m "build(poetry.lock): update dependencies"
git push origin update-packages

# Clean up after PR merge
cd ../../surveys
git fetch --prune
git pull
git worktree remove ../worktrees/update-packages
```

### Version Management

The project uses semantic versioning with commitizen:

```bash
# Check version
task version

# Bump version (auto-detect from commits)
poetry run cz bump --changelog --check-consistency

# Push tags
git push origin --tags

# Version files are automatically updated:
# - pyproject.toml:version
# - titanite/__init__.py:__version__
```

## Code Style and Conventions

### DO

- Always respond in **Japanese**, except for code and docstrings.
- Use **English** for all code, comments, and docstrings.
- Output **one function / class at a time**, with explanation.
- Follow **Python (PEP8)** naming conventions (`snake_case` for variables/functions, `PascalCase` for classes)
- Use only predefined modules/functions unless approved.
- Insert `TODO` markers in docstrings when leaving suggestions for improvement.
- Ask when unsure -- never assume functionality or structure.

### DONT

- Do not invent new functions, classes, arguments, or file structures.
- Do not use Japanese in code, comments, docstrings.
- Do not output multiple features or components in one response.
- Do not omit or remove `TODO` or existing discussion points.
- Do not write pseudocode unless explicitly asked.
- Do not change user-established naming, file organization, or conventions.

### Commit Rules

- Use **Conventional Commits** for all Git commit messages.
- Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Use scope where helpful (e.g., `fix(config): handle missing TOML sections`)
- For breaking changes, add `!` after type/scope
- **Do not** include links or email addresses in commit messages (attribution text without links is acceptable)

## Common Gotchas

- Always use `poetry run` for command execution to ensure correct Python environment
- Avoid using `poetry shell` (deprecated) - use `poetry run` instead
- Commands typically run from `sandbox/` directory where `config.toml` is located
- Use `task` commands instead of manual workflows for consistency
