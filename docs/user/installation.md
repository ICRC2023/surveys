# Installation

## Prerequisites

- Python 3.11
- Git
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)

## Step 1: Clone the repository

```bash
git clone git@github.com:ICRC2023/surveys.git
cd surveys
```

## Step 2: Install dependencies

```bash
uv sync --all-groups
```

This creates a virtual environment in `.venv/` and installs titanite plus
everything in `pyproject.toml` (the `docs` and `dev` groups included).

## Step 3: Verify the installation

```bash
uv run ti --help
```

You should see the titanite CLI help message.

## Development environment

If you plan to contribute:

```bash
# One-time project setup
task env:setup

# Install the pre-commit hooks
uv run pre-commit install
```

## Troubleshooting

### `uv` not found

Install it from the [official guide](https://docs.astral.sh/uv/getting-started/installation/).

### Python version

The project pins Python 3.11 (`requires-python = ">=3.11, <3.12"`). `uv sync`
downloads a matching interpreter automatically; to point at your own:

```bash
uv python pin 3.11
```

### Running commands

Prefix commands with `uv run` so they use the project's environment:

```bash
uv run ti prepare data.csv
```
