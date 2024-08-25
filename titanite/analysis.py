import hvplot
import pandas as pd

from dataclasses import dataclass
from typing import Any


TITLES = {
    "q01": "Q01. Age",
    "q02": "Q02. Gender Identity",
    "q03": "Q03. Workplace",
    "q04": "Q04. Hometown",
    "q05": "Q05. Job Title",
    "q06": "Q06. Research Domain",
    "q07": "Q07. Research Type",
    "q08": "Q08. Research Years",
    "q09": "Q09. Career Satisfaction",
    "q10": "Q10. House Hours",
    "q11": "Q11. Session Signup",
    "q12_genderbalance": "Q12. Gender Balance",
    "q12_diversity": "Q12. Diversity",
    "q12_equity": "Q12. Equity",
    "q12_inclusion": "Q12. Inclusion",
    "q13": "Q13. Female Ratio",
    "q14": "Q14.",
    "q15": "Q15.",
    "q16": "Q16.",
    "q17_genderbalance": "Q17. Gender Balance",
    "q17_diversity": "Q17. Diversity",
    "q17_equity": "Q17. Equity",
    "q17_inclusion": "Q17. Inclusion",
    "q18": "Q18.",
    "q19": "Q19. Science Interest",
    "q20": "Q20.",
    "q21": "Q21.",
    "q22": "Q22.",
    "response": "",
    "q03_regional": "Q03. Workplace",
    "q03_subregional": "Q03. Workplace",
    "q04_regional": "Q04. Hometown",
    "q04_subregional": "Q04. Hometown",
    "q01_clustered": "Q01. Age",
    "q13_clustered": "Q13. Female Ratio",
    "q01q02_clustered": "",
    "q13q14_clustered": "",
    "q10_binned": "Q10. House Hours",
    "q13_binned": "Q13. Female Ratio",
    "q15_polarity": "Q15. Polarity",
    "q15_subjectivity": "Q15. Subjectivity",
    "q15_ja": "",
    "q16_polarity": "Q16. Polarity",
    "q16_subjectivity": "Q16. Subjectivity",
    "q16_ja": "",
    "q18_polarity": "Q18. Polarity",
    "q18_subjectivity": "Q18. Subjectivity",
    "q18_ja": "",
    "q20_polarity": "Q20. Polarity",
    "q20_subjectivity": "Q20. Subjectivity",
    "q20_ja": "",
    "q21_polarity": "Q21. Polarity",
    "q21_subjectivity": "Q21. Subjectivity",
    "q21_ja": "",
    "q22_polarity": "Q21. Polarity",
    "q22_subjectivity": "Q21. Subjectivity",
    "q22_ja": "",
}
"""Columns & Titles"""


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
    xlabel = TITLES.get(x)
    ylabel = "Entries"
    title = xlabel
    by = None

    if len(names) >= 2:
        by = names[1]
        title = TITLES.get(by)

    left = counted.hvplot.bar(
        x=x,
        by=by,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        rot=90,
        grid=True,
        width=1000,
        height=600,
    )

    right = counted.hvplot.table()
    rm = ResultManager(data=counted, graph=(left + right))

    return rm
