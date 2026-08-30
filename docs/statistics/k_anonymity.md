# k-Anonymity and Cell Suppression

How titanite turns individual-level survey data into something safe to commit.

## Overview

`prepared_data.csv` has one row per respondent and includes free-text answers,
raw numbers, and a second-precision timestamp. It is never committed — it lives
under `data/private/`, which is git-ignored.

Two commands produce the committable outputs under `data/public/`:

- **`ti anonymize`** — a publication-safe **individual-level** extract
  (`public_data.csv`), protected by **k-anonymity** (row suppression).
- **`ti aggregate`** — **frequency tables** (`aggregates/…`), protected by
  **cell suppression** (dropping small counts).

Both are implemented by `SecureDataHandler` in
[titanite/core/security.py](../../titanite/core/security.py). The survey schema
supplies the column lists; the core code applies the mechanism.

## Threat model

A respondent is re-identified when someone links a published row back to a
person. The realistic attack here is a **linkage attack**: an adversary holds an
external list (a public attendee roster, a mailing log, an event schedule) and
matches it against the published data on the columns both share.

Those shared columns are **quasi-identifiers** — individually harmless, jointly
identifying. For ICRC2023 (`plugins/icrc2023/schema.py`):

```python
quasi_identifiers = ["q01", "q02", "q03_regional"]
```

age band × gender × work region. The coarse `q03_regional` is used, not
`q03_subregional`, so that `k = 5` still retains most rows; the finer geography
is published only as suppressed aggregates.

Other re-identification vectors handled alongside k-anonymity:

| Vector | Mitigation |
|---|---|
| Free-text answers (may name a person, place, or anecdote) | dropped entirely |
| Second-precision `timestamp` (matchable to a mailing log) | floored to the day |
| Raw outlier numbers (e.g. one respondent with `q13 == 100`) | raw `q10`/`q13` dropped; binned versions kept |
| A lone value in a kept binned column (e.g. `q13_binned == "100%"`) | collapsed to `(rare)` |

## k-anonymity

A dataset is **k-anonymous** on a set of quasi-identifiers if every combination
of quasi-identifier values that appears is shared by **at least k rows**. No one
can then be singled out by that combination plus outside knowledge — each
surviving profile describes at least `k` people.

titanite enforces it by **row suppression**: group by the quasi-identifier
columns, drop every group smaller than `k`.

```python
# SecureDataHandler.k_anonymize, simplified
group_sizes = data.groupby(quasi_identifiers, dropna=False)[qi[0]].transform("size")
data = data[group_sizes >= k]
```

- `dropna=False` — a `NaN` quasi-identifier value forms its own group; a unique
  `NaN` combination is suppressed like any other rare one.
- `k = 5` is the default (`ti anonymize --k`). It is the same threshold used for
  cell suppression, and the conventional floor for published microdata.
- Suppression is **all-or-nothing per group**: a group of 4 loses all 4 rows.
  This biases the extract against small intersections (e.g. an age/gender/region
  cell with few respondents) — those respondents are represented only in the
  aggregates.

### What k-anonymity does *not* do

- It does not protect a column that is not in `quasi_identifiers`. If an answer
  is disclosive on its own, drop it or mask it.
- It gives no protection when every row in a k-group shares the same sensitive
  answer (**homogeneity attack**) — knowing someone is in the group reveals the
  answer. titanite does not implement l-diversity or t-closeness; keep this in
  mind when publishing, and prefer aggregates for anything sensitive.
- Larger `k` means more rows dropped. Raising `k` trades utility for privacy;
  lowering it below 5 is not advised.

## `ti anonymize`

```bash
cd sandbox
uv run ti anonymize --plugin plugins.icrc2023.ICRC2023Schema   # --k 5 default
```

Pipeline (`SecureDataHandler.build_public_dataset`), in order:

1. **Drop free text** — every `free_text_columns` entry. Sentiment scores
   (`<col>_polarity` etc.) are non-reversible aggregates and are kept.
2. **Drop `public_drop_columns`** — geography finer than the quasi-identifiers
   (`q03`, `q04`, `*_subregional`), raw numerics (`q10`, `q13`), and bookkeeping
   (`response`).
3. **Generalize the timestamp** — `timestamp` floored to daily resolution.
4. **k-anonymize** — row suppression on `quasi_identifiers` at `k`.
5. **Mask rare categories** — values in `public_mask_columns`
   (`q10_binned`, `q13_binned`) occurring fewer than `k` times become `(rare)`.
   Done **last**, so it also catches values left rare by step 4's row drops.

Output: `data/public/public_data.csv` — **committed**.

## `ti aggregate` — cell suppression

For breakdowns too fine for a k-anonymous microdata release (e.g.
`q03_subregional`), publish counts instead of rows and suppress the small cells.

```bash
uv run ti aggregate --plugin plugins.icrc2023.ICRC2023Schema \
  --pair q01,q02 --pair q05,q02
```

`SecureDataHandler.aggregate_counts` groups the data, counts each combination,
and `suppress_small_cells` drops every row with `count < threshold` (default 5).
The output carries only category values and counts — no cell represents a group
small enough to single anyone out.

- `univariate/<col>.csv` — one file per `categorical_headers` column
- `bivariate/<x>__<y>.csv` — one per repeatable `--pair X,Y`

Output: `data/public/aggregates/` — **committed**.

> **Suppressed totals still leak.** If a published total and the surviving cells
> don't add up, the suppressed cells' combined count is knowable. For a 2-outcome
> split, one suppressed cell implies the other. titanite does not do
> complementary suppression — keep this in mind before publishing marginal totals
> next to suppressed tables.

## Choosing quasi-identifiers for a new survey

1. List every column an outsider could **also** know about a respondent from a
   public source (roster, schedule, social media). Those are quasi-identifiers.
2. Prefer the **coarsest** version of each (regional over subregional, age band
   over age) so `k = 5` keeps enough rows.
3. Put disclosive-on-their-own columns in `public_drop_columns` (drop) or
   `public_mask_columns` (mask rare values), not `quasi_identifiers`.
4. After running `ti anonymize`, check how many rows survived
   (logged as "k-anonymization (k=5): dropped N rows"). If too many are gone,
   coarsen a quasi-identifier rather than lowering `k`.
5. Publish fine breakdowns via `ti aggregate` instead of adding columns to the
   microdata extract.

See [tests/test_security.py](../../tests/test_security.py) and
[tests/test_cli_anonymize.py](../../tests/test_cli_anonymize.py) for worked
examples.

## See Also

- [Binning](binning.md) — `public_mask_columns` and why raw `q10`/`q13` are dropped
- [Chi-Square Test](chi2_test.md) — analysis runs on the private data, before anonymization
- [Architecture](../developer/architecture.md) — where `SecureDataHandler` sits
- [CLI Commands](../user/cli-commands.md) — `anonymize` and `aggregate` options
