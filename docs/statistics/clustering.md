# Clustering

Deriving new categorical columns from one or more existing answers.

## Overview

A *cluster* in titanite is a derived column computed by a plain Python function
during `ti prepare`. It is not statistical cluster analysis (k-means, hierarchical
clustering); it is a rule-based recode. Use it to:

- collapse a fine-grained answer into a few analysis groups (e.g. age band → two
  cohorts)
- combine two answers into one joint category (e.g. age × gender)
- encode a condition that spans several columns (e.g. "low female ratio *and*
  dissatisfied")

The output column is added to the prepared DataFrame and, if listed in the
schema's `categorical_headers`, picked up by every downstream command
(`ti chi2`, `ti crosstabs`, `ti hbars`, `ti aggregate`).

## `ClusterRule`

Defined in [titanite/core/schema.py](../../titanite/core/schema.py):

```python
@dataclass
class ClusterRule:
    output_column: str  # name of the column to create, e.g. "q01_clustered"
    description: str  # human-readable description of the logic
    apply: Callable  # Callable[[pd.DataFrame], pd.Series]
```

`apply` receives the **whole** DataFrame and returns a `pd.Series` aligned to its
index. That Series becomes `df[output_column]`. There is no built-in aggregation
mode, no `source_columns` list, and no missing-value handling — the function does
whatever you write.

`SurveyProcessor._apply_cluster_rules`
([processor.py](../../titanite/core/processor.py)) simply loops over
`schema.get_cluster_rules()` and assigns each result:

```python
for rule in self.schema.get_cluster_rules():
    df[rule.output_column] = rule.apply(df)
```

Cluster rules run **after** replace and split rules and **before** bin rules, so
`apply` can read split columns (`q03_regional`) but not binned columns
(`q10_binned`).

## Defining rules in a plugin

Implement `get_cluster_rules` and point each rule at a `@staticmethod` on the
schema class. Named static methods keep the logic testable and readable:

```python
class ICRC2023Schema(SurveySchema):
    def get_cluster_rules(self) -> list[ClusterRule]:
        return [
            ClusterRule(
                output_column="q01_clustered",
                description="Age cluster: Cluster1 (under 40s) vs Cluster2 (40s and over)",
                apply=self._cluster_q01,
            ),
        ]

    @staticmethod
    def _cluster_q01(df: pd.DataFrame) -> pd.Series:
        result = pd.Series("Others", index=df.index, dtype=str)
        result[df["q01"] < "40s"] = "Cluster1"
        result[df["q01"] >= "40s"] = "Cluster2"
        return result
```

A common pattern: start from a default (`"Others"`), then overwrite the rows that
match each cluster with boolean indexing. Rows that match no branch keep the
default.

## ICRC2023 clusters

[plugins/icrc2023/schema.py](../../plugins/icrc2023/schema.py) defines four
derived columns, all three-valued (`Cluster1` / `Cluster2` / `Others`):

| Column | Logic | `Cluster1` | `Cluster2` |
|---|---|---|---|
| `q01_clustered` | age band (`q01`) | under 40s | 40s and over |
| `q13_clustered` | female-ratio percentage (`q13`) | ≤ 20% | ≥ 40% |
| `q01q02_clustered` | age (`q01`) × gender (`q02`) | under 40s, Female | under 40s, Male |
| `q13q14_clustered` | female ratio (`q13`) × satisfaction (`q14`) | < 25% and Very Poor/Poor | > 25% and Very Good/Good |

`q13_clustered` deliberately leaves a gap: respondents between 20% and 40% fall
into `Others`. `q01q02_clustered` and `q13q14_clustered` are joint conditions —
anything that doesn't satisfy the full `Cluster1` or `Cluster2` predicate is
`Others`.

All four output names are in `categorical_headers`, so `ti chi2` tests them
against every other categorical question.

### Analysing a cluster

```bash
cd sandbox
uv run ti chi2                 # every categorical pair, incl. the clusters
uv run ti p005 q13_clustered   # pairs with p < 0.05 involving this column
uv run ti crosstabs --save     # contingency tables + heatmaps
uv run ti hbars --save         # per-column distributions
```

## Practical notes

### Values must match `config.toml`

`ti prepare` runs `categorical_data()` after the schema rules. Any value in a
cluster column that is not listed under `[choices]` for that column becomes
`NaN`. Keep the labels your `apply` function emits (`"Cluster1"`, `"Cluster2"`,
`"Others"`) in sync with the config.

### Comparisons rely on category ordering

`df["q01"] < "40s"` works because `q01` is an **ordered** categorical (or a
string that happens to sort correctly). If you convert a column to an unordered
`Categorical`, use `.isin([...])` with an explicit list instead of `<` / `>=`.

### Small cells

Joint clusters (`q01q02_clustered`) split the sample finely and can leave `< 5`
respondents in a cell. `ti aggregate` and the public extract suppress cells below
`--threshold` (default 5); chi-square on a sparse table is unreliable — see
[Chi-Square Test](chi2_test.md#assumptions-and-limitations).

### Testing

Add a unit test that feeds a small synthetic DataFrame through the static method
and asserts the resulting Series. See
[tests/test_icrc2023_schema.py](../../tests/test_icrc2023_schema.py).

## See Also

- [Binning](binning.md) — `BinRule` for numeric columns
- [Chi-Square Test](chi2_test.md) — testing derived columns for association
- [Plugin Development](../developer/plugin-development.md) — implementing a schema
