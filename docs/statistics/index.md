# Statistics Guide

Background on the statistical processing built into titanite's `prepare` and
`chi2` pipelines, and how the ICRC2023 plugin uses it.

- [Chi-Square Test](chi2_test.md) — the association test behind `ti chi2` and `ti p005`
- [Clustering](clustering.md) — deriving new categorical columns with `ClusterRule`
- [Binning](binning.md) — turning `q10` / `q13` into categories with `BinRule`

## Where the rules live

Clustering and binning are configured on the survey schema, not the core
framework. `ClusterRule`, `BinRule`, and `SplitColumnRule` are dataclasses in
[titanite/core/schema.py](../../titanite/core/schema.py); the `SurveyProcessor`
applies them in [titanite/core/processor.py](../../titanite/core/processor.py).
The ICRC2023 implementation is
[plugins/icrc2023/schema.py](../../plugins/icrc2023/schema.py).

The chi-square code is in [titanite/analysis.py](../../titanite/analysis.py)
(`crosstab_data`, `crosstab_loop`) and is wired to the CLI in
[titanite/cli.py](../../titanite/cli.py).
