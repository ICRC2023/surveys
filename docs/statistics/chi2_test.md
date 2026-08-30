# Chi-Square Test

The association test behind `ti chi2`, `ti p005`, and `ti crosstabs`.

## Overview

The chi-square test of independence checks whether two categorical variables are
associated — whether the joint distribution differs from what independence would
predict. In titanite it is run over every pair of `categorical_headers` columns
in the prepared dataset to surface which question pairs are related.

**Use it for:**

- associations between categorical answers (e.g. `q02` gender vs `q05` field)
- testing independence of a derived cluster (`q13_clustered`) against other answers
- ranking which pairs, out of many, look non-random

## The statistic

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

- **O** — observed count in a contingency-table cell
- **E** — count expected under independence,
  $E_{ij} = (\text{row}_i\ \text{total}) \times (\text{col}_j\ \text{total}) / n$

Degrees of freedom: $df = (r - 1)(c - 1)$ for an $r \times c$ table.

titanite computes this with
[`scipy.stats.chi2_contingency`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)
on `pd.crosstab(data[x], data[y])` — see `crosstab_data` in
[titanite/analysis.py](../../titanite/analysis.py). `chi2_contingency` defaults
to `correction=True`, so **Yates' continuity correction is applied when
`df == 1`** (2×2 tables). This inflates the p-value slightly to compensate for
small counts.

## Interpreting the p-value

The p-value is the probability of a $\chi^2$ this large or larger if the two
variables were independent.

- **p < 0.05** — conventionally "significant"; the observed association is
  unlikely under independence
- **p ≥ 0.05** — no evidence against independence

A small p-value says the association is unlikely to be noise. It says **nothing**
about how strong the association is, or which variable drives the other.

## Using it in titanite

### `ti chi2` — every pair

```bash
cd sandbox
uv run ti chi2
```

Reads `../data/private/prepared_data.csv`, takes every 2-combination of the
`categorical_headers` present, and writes to `../data/private/chi2_test/`:

| File | Contents |
|---|---|
| `chi2_test.csv` / `.json` | one row per pair |
| `chi2_test_p005.csv` / `.json` | the subset with `p_value < 0.05` |

Columns in those files (`crosstab_loop` in
[analysis.py](../../titanite/analysis.py)):

| Column | Meaning |
|---|---|
| `questions` | `"<x>-<y>"` pair label |
| `p_value` | `chi2_contingency` p-value |
| `statistic` | the $\chi^2$ value |
| `dof` | degrees of freedom |
| `x`, `y` | the two column names |

There is **no effect-size column** (no Cramér's V) and **no multiple-comparison
adjustment** — `chi2_test_p005.csv` is a raw `p_value < 0.05` filter. If you need
those, compute them from the CSV yourself (see below).

### `ti p005` — one focus column

```bash
uv run ti p005 q13_clustered          # writes ../data/private/p005/q13_clustered/
uv run ti p005 q13_clustered --save   # also saves heatmap PNGs for each pair
```

Cross-tabulates `header` against every other column and keeps the pairs with
`p_value < 0.05`, writing `chi2_test_p005_<header>.csv` / `.json` under
`../data/private/p005/<header>/`. `--save` renders an Altair heatmap PNG per
significant pair.

### `ti crosstabs` — tables and heatmaps

```bash
uv run ti crosstabs --save
```

Builds the full contingency table and heatmap for every pair (the same
`crosstab_loop`), for visual inspection alongside the numbers.

## Assumptions and limitations

**Assumptions**

1. **Independent observations** — one row per respondent
2. **Categorical data** — bin numeric columns first (see [Binning](binning.md))
3. **Adequate expected counts** — the usual rule of thumb is $E \ge 5$ in ~80%
   of cells; sparse tables make the p-value unreliable. `chi2_contingency`
   returns the `expected` array but titanite does not check it or warn — inspect
   the cross-tab from `ti crosstabs` when a table looks thin.

For small or sparse tables, Fisher's exact test is more appropriate; titanite
does not implement it. Collapsing rare categories (or using a coarser
`ClusterRule` / `BinRule`) is the practical fix.

**Limitations**

- **Association, not causation** — a significant pair may be driven by a
  confounder (e.g. age relating to both answers).
- **Sample-size sensitivity** — with a large `n`, trivially small differences
  reach `p < 0.05`. Always look at the contingency table, not just the p-value.
- **Multiple comparisons** — `ti chi2` tests many pairs at once. At $\alpha =
  0.05$, roughly 5% of truly-independent pairs land in `chi2_test_p005.csv` by
  chance.

## Effect size and multiple comparisons (do this yourself)

titanite reports raw p-values only. To go further, load `chi2_test.csv` and add:

**Cramér's V** (effect size, 0–1):

```python
import numpy as np
import pandas as pd

df = pd.read_csv("../data/private/chi2_test/chi2_test.csv")
# k = min(rows, cols) for each pair; recompute from the crosstab, or read n and k
# from ti crosstabs output. With n and k in hand:
df["cramers_v"] = np.sqrt(df["statistic"] / (df["n"] * (df["k"] - 1)))
```

Rough guide: V < 0.1 negligible, 0.1–0.3 weak, 0.3–0.5 moderate, ≥ 0.5 strong.

**Bonferroni** (family-wise error control):

```python
m = len(df)  # number of pairs tested
df["significant"] = df["p_value"] < 0.05 / m
```

Or use `statsmodels.stats.multitest.multipletests(df["p_value"], method="fdr_bh")`
for a less conservative Benjamini–Hochberg FDR.

## Further reading

- [Chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test)
- [Cramér's V](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)
- [Multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem)

## See Also

- [Binning](binning.md) — making numeric columns testable
- [Clustering](clustering.md) — derived categorical columns to test
