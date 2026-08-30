# Configuration

## The config file

`sandbox/config.toml` holds the survey's question text, answer choices, and
per-column metadata. It is read by `ti config`, `ti prepare`, and the
analysis commands (via the `Config` / `Data` classes).

Data-processing rules — value replacements, geographic splitting, clustering,
binning — live in the **schema** (`plugins/<survey>/schema.py`), not here.

## Sections

### `[volumes]`

Named data directories.

```toml
[volumes]
main = "../data/main_data"
test = "../data/test_data"
```

### `[questions]`

Question id → the full question text.

```toml
[questions]
q01 = "【Q1】What is your age ?"
q02 = "【Q2】What gender do you identify as ?"
```

### `[choices]`

Named ordered category lists, referenced by `[[options]].category`.

```toml
[choices]
age = ["10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s+", "Prefer not to answer"]
gender = ["Male", "Female", "Non-binary", "Prefer to self-identify", "Prefer not to answer"]
```

### `[[options]]`

One entry per analysable column: its display title, description, type, and
(for categoricals) which `[choices]` list orders it.

```toml
[[options]]
name = "q01"
title = "Age Group"
description = "【Q1】What is your age?"
type = "categorical"    # or "numerical" / "comment"
category = "age"
```

`Config.get_categorical_headers()` / `get_numerical_headers()` /
`get_comment_headers()` derive their lists from the `type` field.

## Pointing at a different config

```bash
uv run ti config --load-from /path/to/config.toml
uv run ti prepare data.csv --load-from /path/to/config.toml --write-dir /path/to/output
```

## Verifying

```bash
uv run ti config --questions   # every question is mapped
uv run ti config --choices     # every category list is defined
```

If a categorical column has values not in its `[choices]` list, they become
NaN after `categorical_data()` — check with `--choices`.
