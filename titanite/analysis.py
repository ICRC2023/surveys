import hvplot
import pandas as pd

from dataclasses import dataclass
from typing import Any


@dataclass
class ResultManager:
    """データとグラフ"""

    data: pd.DataFrame
    graph: Any


def breakdowns(
    data: pd.DataFrame, names: list[str], sort: bool = False
) -> ResultManager:
    """内訳を集計

    :Args:
        - `data (pd.DataFrame)`: 全体のデータフレーム
        - `names (list[str])`: 内訳集計するカラム名
        - `sort (bool, optional)`: 集計結果をソート（合計が大きい順）. Defaults to False.

    Returns:
        - `ResultManager`: データとグラフ
    """

    counted = data[names].value_counts(sort=sort).reset_index()

    x = names[0]
    by = names[1] if len(names) >= 2 else None

    left = counted.hvplot.bar(
        x=x,
        by=by,
        rot=90,
        grid=True,
        width=1000,
        height=600,
    )

    right = counted.hvplot.table()
    rm = ResultManager(data=counted, graph=(left + right))

    return rm
