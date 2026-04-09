# Installation

## Prerequisites

- Python 3.9 or higher
- Git
- Poetry (Python package manager)

## Step 1: Clone Repository

```bash
git clone git@github.com:ICRC2023/surveys.git
cd surveys
```

## Step 2: Install Dependencies

```bash
poetry install
```

This installs titanite and all required dependencies defined in `pyproject.toml`.

## Step 3: Verify Installation

```bash
poetry run ti --help
```

You should see the titanite CLI help message.

## Development Environment Setup

If you're planning to contribute or develop:

```bash
# Set up development environment
task env:setup

# Install pre-commit hooks
poetry run pre-commit install
```

## Troubleshooting

### Poetry not found

Install Poetry following the [official guide](https://python-poetry.org/docs/#installation).

### Python version mismatch

Check your Python version:

```bash
python --version
```

Ensure you have Python 3.9 or higher. If you have multiple versions, specify the version:

```bash
poetry env use /path/to/python3.9
```

### Environment activation

Always use `poetry run` to execute commands:

```bash
poetry run ti prepare data.csv
```

Avoid using `poetry shell` (deprecated). Instead, prefix commands with `poetry run`.
