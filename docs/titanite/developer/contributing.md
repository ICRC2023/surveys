# Contributing

Guidelines for contributing to titanite.

## Development Workflow

### 1. Create a Worktree

Use git worktree to work on isolated branches:

```bash
# Create worktree for feature branch
git worktree add ../worktrees/feature-name -b feature-name
cd ../worktrees/feature-name
```

### 2. Setup Environment

```bash
# Set up development environment
task env:setup

# Install pre-commit hooks
poetry run pre-commit install
```

### 3. Make Changes

Create your implementation following code style guidelines.

### 4. Run Quality Checks

Before committing, run all checks:

```bash
# Run tests
task test

# Format code
task format

# Lint code
task lint

# Run pre-commit hooks
task pre-commit
```

All checks must pass before committing.

### 5. Commit Changes

Use conventional commits with clear messages:

```bash
git add <files>
git commit -m "type(scope): description"
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples:**
- `feat(cli): add new command for data export`
- `fix(processor): handle missing values in binning`
- `docs(guide): improve plugin development documentation`
- `test(schema): add tests for geographic splitting`

### 6. Push and Create PR

```bash
git push origin feature-name
gh pr create --title "Feature description" --body "Detailed description"
```

Reference related issues:

```
Closes #123
```

### 7. Cleanup

After PR is merged:

```bash
cd ../../surveys
git fetch --prune
git pull
git worktree remove ../worktrees/feature-name
```

## Code Style

### Python

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions:

- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Line length: 100 characters (enforced by ruff)
- Use type hints where helpful

**Naming conventions:**

```python
# Functions and variables
def process_data():
    survey_responses = []
    return survey_responses

# Classes
class SurveySchema:
    pass

# Constants
MAX_RESPONSES = 1000
```

### Code Organization

**Imports** - Group and sort:

```python
# Standard library
import os
from pathlib import Path

# Third-party
import pandas as pd
import numpy as np

# Local
from titanite.core import SurveySchema
from titanite.analysis import chi2_test
```

**Functions** - Keep focused and short:

```python
# Good - Clear purpose, <50 lines
def replace_values(df: pd.DataFrame, rules: dict) -> pd.DataFrame:
    """Replace values in DataFrame according to rules."""
    result = df.copy()
    for column, replacements in rules.items():
        result[column] = result[column].replace(replacements)
    return result

# Avoid - Too complex
def process_everything(df, rules, splits, clusters):
    # 200 lines of mixed logic
    pass
```

### Documentation

**Docstrings** - Use Google style:

```python
def split_column(df: pd.DataFrame, column: str, delimiter: str) -> pd.DataFrame:
    """
    Split a composite column into multiple columns.

    Args:
        df: Input DataFrame
        column: Column name to split
        delimiter: String delimiter separating values

    Returns:
        DataFrame with split columns

    Example:
        >>> df = pd.DataFrame({"location": ["USA - California"]})
        >>> split_column(df, "location", " - ")
        # Returns: df with ["country", "state"] columns
    """
    pass
```

**Comments** - Only for non-obvious logic:

```python
# Good - Explains why
# Use majority vote for gender clustering because single response
# may not represent full gender identity
result = majority_vote(gender_columns)

# Bad - Explains what (already clear from code)
# Loop through each row
for idx, row in df.iterrows():
    pass
```

### Type Hints

Use type hints for clarity:

```python
# Good
def process(data: pd.DataFrame) -> pd.DataFrame:
    pass

# Good - Complex types
from typing import list
def get_columns(df: pd.DataFrame, types: list[str]) -> list[str]:
    pass

# Avoid - No hints
def process(data):
    pass
```

## Testing Requirements

All new code must include tests:

1. **Unit tests** - Test individual functions
2. **Integration tests** - Test with real data
3. **Coverage** - Maintain >80% code coverage

```bash
# Write tests in tests/test_new_feature.py
poetry run pytest tests/test_new_feature.py -v

# Check coverage
poetry run pytest --cov=titanite tests/
```

See [Testing](testing.md) for detailed guidelines.

## PR Review Process

### Before Submitting

Ensure your PR:

- [ ] Passes all tests (`task test`)
- [ ] Follows code style (`task format`, `task lint`)
- [ ] Has clear commit messages (conventional commits)
- [ ] Includes relevant tests
- [ ] Updates documentation if needed
- [ ] References related issues

### Review Checklist

Reviewers will check:

- **Functionality** - Does it work as intended?
- **Testing** - Are there adequate tests?
- **Code quality** - Does it follow style guidelines?
- **Documentation** - Are changes documented?
- **Performance** - No obvious performance issues?
- **Security** - No security vulnerabilities?

## Common Contributions

### Adding a New Command

1. **Implement command** in `titanite/cli.py`
2. **Add logic** in `titanite/analysis.py` or `titanite/core.py`
3. **Write tests** in `tests/test_cli.py`
4. **Update docs** in `docs/guides/user/cli-commands.md`

**Example:**

```python
# titanite/cli.py
@click.command()
def my_command():
    """Description of what command does."""
    pass

# tests/test_cli.py
def test_my_command(runner):
    result = runner.invoke(my_command)
    assert result.exit_code == 0

# docs/guides/user/cli-commands.md
### `ti my-command`
Description and usage examples...
```

### Creating a New Plugin

1. **Create plugin directory** - `plugins/your_survey/`
2. **Implement schema** - Inherit from `SurveySchema`
3. **Write tests** - In `tests/test_your_survey_schema.py`
4. **Document** - In `docs/guides/developer/plugin-development.md`

See [Plugin Development](plugin-development.md) for detailed guide.

### Fixing a Bug

1. **Create issue** if one doesn't exist
2. **Write failing test** that reproduces bug
3. **Implement fix**
4. **Verify test passes**
5. **Create PR** referencing issue

**Commit message:**

```
fix(scope): brief description

Closes #123

Detailed explanation of what was wrong and how it was fixed.
```

### Documentation Improvements

Improve docs by:

- Clarifying existing docs
- Adding examples
- Fixing typos/grammar
- Adding missing sections

Docs are in `docs/guides/`, use Markdown format.

## Release Process

Releases follow semantic versioning:

```bash
# Check what needs updating
task deps:check

# Update if needed
task deps:update

# Commit and tag
poetry run cz bump --changelog --check-consistency
git push origin --tags
```

## Getting Help

- **Questions**: Open an issue or discussion
- **Bug reports**: Create issue with reproduction steps
- **Feature requests**: Open issue with use case
- **PR feedback**: Ask reviewers for clarification

## Communication

### Commit Messages

Be clear and descriptive:

```
# Good
feat(plugin): add support for custom survey schema with clustering rules

# Bad
update stuff
fix things
add feature
```

### PR Descriptions

Include:

- **What** - What changes are made?
- **Why** - Why are these changes needed?
- **How** - How do the changes work?
- **Testing** - How was this tested?

**Template:**

```markdown
## Summary
Brief description of changes.

## Changes
- Bullet points of specific changes
- Changed X to improve Y
- Added tests for Z

## Testing
How was this tested?
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing (describe)

Closes #123
```

## Repository Structure

```
├── titanite/          # Main package
├── plugins/           # Survey plugins
├── tests/             # Test suite
├── docs/              # Documentation
├── notebooks/         # Jupyter notebooks
├── data/              # Data files
├── sandbox/           # CLI working directory
├── Taskfile.yml       # Task automation
├── pyproject.toml     # Project configuration
└── CLAUDE.md          # Developer guide
```

## Useful Commands

```bash
# Setup
task env:setup
poetry run pre-commit install

# Development
task test               # Run tests
task format             # Format code
task lint               # Lint code
task pre-commit         # Run pre-commit checks

# Documentation
task docs:serve         # Serve docs locally
task docs:build         # Build docs

# Utilities
task version            # Check version
task deps:check         # Check outdated packages
task deps:update        # Update dependencies
```

## Code Review Expectations

- Respond to feedback promptly
- Be respectful and constructive
- Ask questions if feedback is unclear
- Acknowledge good suggestions even if you don't implement them

## Acknowledgment

All contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes (for significant contributions)

Thank you for contributing!
