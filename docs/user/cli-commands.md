# CLI Commands

Reference for the `ti` command. Run it from `sandbox/`, where `config.toml`
lives, or pass `--load-from` / `--read-from` / `--write-dir` from elsewhere.

```bash
cd sandbox
uv run ti --help
```

## config

Show the survey configuration from `config.toml`.

```bash
uv run ti config --questions   # question text
uv run ti config --choices     # answer choices / categories
```

## prepare

Preprocess a raw Google Forms CSV: categorical conversion, geographic
splitting, clustering, binning, sentiment scoring.

```bash
uv run ti prepare <input.csv> --plugin plugins.icrc2023.ICRC2023Schema
```

| Option | Default | Meaning |
|--------|---------|---------|
| `--plugin` | *(none)* | Schema class `plugins.pkg.ClassName`. Without it, the legacy `preprocess_data()` path runs. |
| `--write-dir` | `../data/private/` | Output directory (git-ignored) |
| `--load-from` | `config.toml` | Config file |

Writes `prepared_data.csv` (one row per respondent, with free text),
`categorical_data.csv`, `sentiment_data.csv` — all under `data/private/`,
which is never committed.

## anonymize

Turn `prepared_data.csv` into a publication-safe individual-level extract.

```bash
uv run ti anonymize --plugin plugins.icrc2023.ICRC2023Schema
```

- drops the free-text columns and their `_ja` translations (sentiment scores kept)
- truncates `timestamp` to the day
- drops the schema's `public_drop_columns` (geography finer than the quasi-identifiers)
- masks rare values in `public_mask_columns` to `(rare)`
- enforces k-anonymity (`--k`, default 5) on the schema's `quasi_identifiers`

Writes `data/public/public_data.csv`, which **is** committed.

## aggregate

Build suppressed frequency tables from `prepared_data.csv`.

```bash
uv run ti aggregate --plugin plugins.icrc2023.ICRC2023Schema \
  --pair q01,q02 --pair q05,q02
```

- `univariate/<col>.csv` for every `categorical_headers` column
- `bivariate/<x>__<y>.csv` for each repeatable `--pair X,Y`
- cells below `--threshold` (default 5) are omitted

Writes to `data/public/aggregates/`, which is committed.

## chi2

Chi-square tests for every pair of categorical questions.

```bash
uv run ti chi2
```

Writes `chi2_test.csv` (and `_p005.csv` for p < 0.05) with the test
statistics only — no counts.

## p005

Significant correlations (p < 0.05) for one column.

```bash
uv run ti p005 q13 --save
```

## crosstabs

Cross-tabulation for all variable pairs (heatmaps + chi-square).

```bash
uv run ti crosstabs --save
```

## response

Response-timeline heatmap (day x hour).

```bash
uv run ti response
```

## hbars

Histograms for all variables.

```bash
uv run ti hbars --save
```

## comments

Extract free-text responses (q15–q22) with their sentiment scores. Reads
`data/private/` and writes there — the output contains verbatim answers and
must not be committed.

```bash
uv run ti comments
```

## WIP

`ti crosstab` and `ti hbar` (single-pair / single-variable) are
placeholders and not yet implemented.
