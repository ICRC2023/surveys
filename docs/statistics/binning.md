# Binning

Turning a numeric column into an ordered categorical column with `pd.cut`.

## Overview

`ti prepare` collects two numeric answers in the ICRC2023 survey — `q10` (number
of invited speakers) and `q13` (female-ratio percentage). Binning discretises
them so they can be:

- used in chi-square tests and cross-tabulations, which need categorical data
- shown as bar charts (`ti hbars`) with a fixed, readable set of bars
- published in the k-anonymised extract without exposing a raw outlier (the lone
  `q13 == 100` respondent is a quasi-identifier)

## `BinRule`

Defined in [titanite/core/schema.py](../../titanite/core/schema.py):

```python
@dataclass
class BinRule:
    source_column: str  # numeric column to bin, e.g. "q10"
    output_column: str  # categorical column to create, e.g. "q10_binned"
    bins: list  # bin edges, passed straight to pd.cut
    labels: list[str]  # one label per interval; len(labels) == len(bins) - 1
    right: bool = False  # pd.cut right= ; False → [left, right) intervals
```

`SurveyProcessor._apply_bin_rules`
([processor.py](../../titanite/core/processor.py)) calls:

```python
df[rule.output_column] = pd.cut(
    df[rule.source_column], rule.bins, labels=rule.labels, right=rule.right
)
```

That is the whole mechanism. There is no equal-frequency / quantile option in
`BinRule` — `pd.cut` with explicit edges only. If you want quantile bins, compute
the edges yourself (e.g. `df[col].quantile([...])`) and pass them as `bins`.

Bin rules run **last** in the schema pipeline (after replace, split, and cluster
rules), so a binned column cannot be read by a `ClusterRule`.

### Edges and `right=False`

With `right=False`, each interval is `[edge_i, edge_{i+1})` — left-inclusive,
right-exclusive. To capture a value `v` in its own bin you need edges that
bracket it, e.g. `..., v, v+1, ...`. The ICRC2023 rules use this to give each
integer speaker count and each 5-point ratio step its own bar. Values equal to
the first edge or `>=` the last edge become `NaN`; that is why the ICRC2023 rules
start the edges at `-1` (so `0` and `"Prefer not to answer"`, coded as `0`, land
in the first bin) and end past the maximum.

## ICRC2023 rules

[plugins/icrc2023/schema.py](../../plugins/icrc2023/schema.py):

```python
BinRule(
    source_column="q10",
    output_column="q10_binned",
    bins=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25],
    labels=[
        "Prefer not to answer",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10+",
    ],
    right=False,
)

BinRule(
    source_column="q13",
    output_column="q13_binned",
    bins=[
        -1,
        0,
        10,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50,
        55,
        60,
        65,
        70,
        75,
        80,
        85,
        90,
        95,
        100,
        105,
    ],
    labels=[
        "Prefer not to answer",
        "0%",
        "10%",
        "15%",
        "20%",
        "25%",
        "30%",
        "35%",
        "40%",
        "45%",
        "50%",
        "55%",
        "60%",
        "65%",
        "70%",
        "75%",
        "80%",
        "85%",
        "90%",
        "95%",
        "100%",
    ],
    right=False,
)
```

- `q10_binned`: one bin per speaker count 0–9, then `10+` collects `[10, 25)`.
- `q13_binned`: `0%` is its own bin `[0, 10)`; the rest are 5-percentage-point
  steps `[10, 15)`, `[15, 20)`, …, `[100, 105)`.
- `-1` as the first edge routes the sentinel value `0` (used for "Prefer not to
  answer") into the first labelled bin.

Both output columns are in `categorical_headers`, and both are listed in
`public_mask_columns` so their rare extreme bins are collapsed to `(rare)` in
`data/public/public_data.csv`.

## Workflow

### 1. Look at the distribution

```python
import pandas as pd

df = pd.read_csv("../data/private/prepared_data.csv")
print(df["q13"].describe())
```

### 2. Choose edges and labels

Pick edges that are interpretable (multiples of 5 or 10, natural thresholds) and
make sure `len(labels) == len(bins) - 1`. Decide what happens to the minimum and
maximum values — extend the outer edges so nothing silently becomes `NaN`.

### 3. Add the `BinRule` and re-run prepare

```bash
cd sandbox
uv run ti prepare ../data/downloaded/icrc2023.csv \
  --plugin plugins.icrc2023.ICRC2023Schema
```

### 4. Check the result

```bash
uv run ti config --choices          # confirm the labels are registered
uv run ti hbars --save              # eyeball the per-bin counts
```

If a bin is empty or has `< 5` respondents, merge it with a neighbour.

## Common issues

### `NaN` after binning

A value fell outside `[bins[0], bins[-1])`, or (with `right=False`) equalled the
last edge. Widen the outer edges.

### Label / edge length mismatch

`pd.cut` raises `ValueError: Bin labels must be one fewer than the number of bin
edges`. Count again: N edges → N−1 labels.

### Sparse cells break chi-square

Fine bins (like the per-integer `q10` bins) produce many small cells. For
association testing, either bin more coarsely or expect the chi-square
assumptions to be violated — see
[Chi-Square Test](chi2_test.md#assumptions-and-limitations).

### Choosing edges after seeing results

Deciding bin boundaries to make an association appear (or disappear) is a form of
p-hacking. Fix the edges from the survey design, not the outcome.

## See Also

- [Chi-Square Test](chi2_test.md) — using binned columns in association tests
- [Clustering](clustering.md) — `ClusterRule` for rule-based recodes
- [Plugin Development](../developer/plugin-development.md) — implementing a schema
