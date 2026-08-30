"""Shared helpers for the ICRC2023 survey-results Quarto pages.

The pages read only the anonymized, suppressed extract under ``data/public/``:

- ``public_data.csv``          - 245-row k=5 individual-level extract
- ``aggregates/univariate/``   - per-column frequency tables (n<5 suppressed)
- ``aggregates/bivariate/``    - demographic x question cross-tabs (n<5 suppressed)

Never point these at ``data/private/`` or a raw export.
"""

from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd

_PUBLIC = Path(__file__).resolve().parent.parent / "data" / "public"

#: Suppression threshold used when the aggregates were built (for captions).
SUPPRESSION_THRESHOLD = 5


def load_public() -> pd.DataFrame:
    """Return the anonymized individual-level extract (``public_data.csv``)."""
    return pd.read_csv(_PUBLIC / "public_data.csv")


def load_univariate(column: str) -> pd.DataFrame:
    """Return the suppressed frequency table for ``column``.

    Columns: the category column plus ``count``. Rows for categories seen
    fewer than :data:`SUPPRESSION_THRESHOLD` times are absent.
    """
    return pd.read_csv(_PUBLIC / "aggregates" / "univariate" / f"{column}.csv")


def load_bivariate(x: str, y: str) -> pd.DataFrame:
    """Return the suppressed cross-tab for ``x`` x ``y``.

    The aggregate was written under one column order; try both, and always
    return it with ``x`` first so callers can pass either order.
    """
    bi = _PUBLIC / "aggregates" / "bivariate"
    forward = bi / f"{x}__{y}.csv"
    reverse = bi / f"{y}__{x}.csv"
    if forward.exists():
        return pd.read_csv(forward)
    if reverse.exists():
        table = pd.read_csv(reverse)
        return table[[x, y, "count"]]
    raise FileNotFoundError(
        f"no aggregate for {x} x {y}; add '--pair {x},{y}' to "
        f"scripts/build_public_data.sh and rerun it"
    )


def bar(
    table: pd.DataFrame,
    category: str,
    *,
    title: str = "",
    sort: list[str] | None = None,
) -> alt.Chart:
    """Horizontal bar chart of a univariate frequency table."""
    enc_y = alt.Y(f"{category}:N", title=None)
    if sort is not None:
        enc_y = enc_y.sort([s for s in sort if s in set(table[category])])
    return (
        alt.Chart(table)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Responses"),
            y=enc_y,
            tooltip=[category, "count"],
        )
        .properties(title=title, width="container", height=max(120, 26 * len(table)))
    )


def grouped_bar(
    table: pd.DataFrame,
    category: str,
    group: str,
    *,
    title: str = "",
    normalize: bool = False,
) -> alt.Chart:
    """Grouped/stacked bar chart of a bivariate cross-tab.

    With ``normalize`` the bars are scaled to proportions within each
    ``category`` value.
    """
    x = alt.X("count:Q", title="Share" if normalize else "Responses")
    if normalize:
        x = x.stack("normalize")
    return (
        alt.Chart(table)
        .mark_bar()
        .encode(
            x=x,
            y=alt.Y(f"{category}:N", title=None),
            color=alt.Color(f"{group}:N", title=group),
            tooltip=[category, group, "count"],
        )
        .properties(
            title=title,
            width="container",
            height=max(140, 30 * table[category].nunique()),
        )
    )


def suppression_note() -> str:
    """Standard caption noting the suppression rule."""
    return (
        f"Cells with fewer than {SUPPRESSION_THRESHOLD} responses are omitted "
        f"(privacy suppression). Percentages, where shown, are of the "
        f"non-suppressed total."
    )


# -- Free-text questions ---------------------------------------------------
#
# Verbatim free-text answers are never published. These helpers report only
# how many people answered and the distribution of the (non-reversible)
# TextBlob sentiment scores from the anonymized extract.


def free_text_answered(question: str) -> int:
    """Number of respondents who wrote a free-text answer to ``question``.

    Counted from the non-null sentiment score in ``public_data.csv`` (the
    answer text itself is not in the extract).
    """
    df = load_public()
    return int(df[f"{question}_polarity"].notna().sum())


def sentiment_hist(question: str, *, title: str = "") -> alt.Chart:
    """Histogram of polarity and subjectivity for a free-text question."""
    df = load_public()
    long = (
        df[[f"{question}_polarity", f"{question}_subjectivity"]]
        .rename(
            columns={
                f"{question}_polarity": "polarity",
                f"{question}_subjectivity": "subjectivity",
            }
        )
        .melt(var_name="score", value_name="value")
        .dropna()
    )
    return (
        alt.Chart(long)
        .mark_bar(opacity=0.7)
        .encode(
            x=alt.X("value:Q", bin=alt.Bin(maxbins=20), title="Score"),
            y=alt.Y("count()", title="Respondents"),
            color=alt.Color("score:N", title=None),
            column=alt.Column("score:N", title=None),
        )
        .properties(title=title, width=260, height=180)
    )


def free_text_note() -> str:
    """Caption for the free-text pages."""
    return (
        "Verbatim answers are not published. Polarity (negative to positive) "
        "and subjectivity (factual to opinionated) are TextBlob sentiment "
        "scores computed on the English text; they cannot be used to "
        "reconstruct it."
    )
