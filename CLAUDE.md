# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an ICRC2023 Diversity Session survey analysis project called "Titanite" - a Python-based tool for analyzing diversity-related survey data from the International Cosmic Ray Conference 2023. The project analyzes pre-conference (2023-07-09 to 07-21) and post-conference (2023-09-15 to 09-22) survey responses from 295 participants out of 1,406 conference attendees.

## Development Environment

### Setup Commands
```bash
poetry install
poetry run ti --help  # Verify installation
```

### Testing
```bash
poetry run pytest
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

## Development Workflow

### Branch Development with Git Worktree

This project uses `git worktree` for isolated branch development to avoid conflicts and enable parallel development:

```bash
# Check available branches
git branch -a

# Create worktree for feature branch
git worktree add ../worktrees/<directory_name> <branch-name>
git worktree list

# Setup and develop in feature branch
cd ../worktrees/<directory_name>
poetry install
# ... develop features ...

# TODO: add Taskfile.yml
# Run tests and format code
task pytest
task format
task pre-commit

# Finish development
git add <files>
git commit
git merge origin/main
git push

# Clean up after merge
cd ../../surveys
git fetch --prune
git pull
git branch -d <branch_name>
git worktree remove ../worktrees/<directory_name>
```

### GitHub Issue and PR Integration

This project follows GitHub's issue-driven development workflow:

```bash
# List open issues
gh issue list

# View specific issue details
gh issue view <issue-number>

# Create branch for issue (use descriptive name based on issue)
git worktree add ../worktrees/<issue-branch-name> -b <issue-branch-name>

# Work on the issue in isolated environment
cd ../worktrees/<issue-branch-name>
poetry install
# ... implement features/fixes ...

# TODO: add Taskfile.yml
# Run development workflow
task pytest
task format
task pre-commit

# Create pull request when ready
gh pr create --title "fix: <issue-description>" --body "Closes #<issue-number>"

# After PR review and approval
# Clean up worktree (see worktree workflow above)
```

**Development Guidelines:**
- Always reference issue numbers in commit messages and PR descriptions
- Use `Closes #<issue-number>` in PR descriptions to auto-close issues
- Follow the existing issue labels and prioritization
- Create PRs for all changes, even small fixes
- Run all tests and pre-commit hooks before creating PR

### Version Management

The project uses semantic versioning with commitizen:
```bash
# Bump version and update changelog
cz bump --changelog --check-consistency

# Push version tags
git push origin --tags

# Version files are automatically updated:
# - pyproject.toml:version
# - titanite/__init__.py:__version__
```

## Directory Structure Notes

- `titanite/`: Main Python package source code
- `tests/`: Test suite with pytest configuration
- `data/`: Survey data
- `docs/`: Sphinx documentation site
- `notebooks/`: Jupyter Notebooks
- `sandbox/`: Example configuration files
- `typst/`: Create PDF document with Typst
- `poetry.lock`: Lock file for reproducible dependency installation

## Common Gotchas

- Always use `poetry run` for command execution to ensure correct Python environment
- Avoid using `poetry shell` (deprecated) - use `poetry run` instead
- Future migration to `uv` planned - maintain compatibility during transition

## DO

- Always respond in **Japanese**, except for code and docstrings.
- Use **English** for all code, comments, and docstrings.
- Output **one function / class at a time**, with explanation.
- Follow **Python (PEP8)** naming conventions (`snake_case` for variables/functions, `PascalCase` for classes)
- Use only predefined modules/functions unless approved.
- Insert `TODO` markers in docstrings when leaving suggestions for improvement.
- Ask when unsure -- never assume functionality or structure.

## DONT

- Do not invent new functions, classes, arguments, or file structures.
- Do not use Japanese in code, comments, docstrings.
- Do not output multiple features or components in one response.
- Do not omit or remove `TODO` or existing discussion points.
- Do not write pseudocode unless explicitly asked.
- Do not change user-established naming, file organization, or conventions.

## Commit Rules

- Use **Conventional Commits** for all Git commit messages.
- Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Use scope where helpful (e.g., `fix(config): handle missing TOML sections`)
- For breaking changes, add `!` after type/scope
- **Do not** include links or email addresses in commit messages (attribution text without links is acceptable)
