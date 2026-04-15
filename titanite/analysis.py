from dataclasses import dataclass
from typing import Any

import altair as alt
import pandas as pd
import hvplot.pandas
from scipy.stats import chi2_contingency

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
    "q12_genderbalance": "Q12. Gender Balance (Group)",
    "q12_diversity": "Q12. Diversity (Group)",
    "q12_equity": "Q12. Equity (Group)",
    "q12_inclusion": "Q12. Inclusion (Group)",
    "q13": "Q13. Female Ratio",
    "q14": "Q14.",
    "q15": "Q15.",
    "q16": "Q16.",
    "q17_genderbalance": "Q17. Gender Balance (Individual)",
    "q17_diversity": "Q17. Diversity (Individual)",
    "q17_equity": "Q17. Equity (Individual)",
    "q17_inclusion": "Q17. Inclusion (Individual)",
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
    data: pd.DataFrame,
    names: list[str],
    sort: bool = False,
    width: int = 1000,
    height: int = 600,
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
        width=width,
        height=height,
    )

    right = counted.hvplot.table()
    rm = ResultManager(data=counted, graph=(left + right))

    return rm


def comment_data(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Parse comment data.

    Extracts free-text responses from q15, q16, q18, q20, q21, and q22,
    dropping rows with no answer. Each question's comments are returned as a
    separate DataFrame that includes demographic cluster columns and the
    corresponding sentiment and translation columns.

    Parameters
    ----------
    data : pd.DataFrame
        preprocessed survey DataFrame containing free-text and sentiment columns

    Returns
    -------
    dict[str, pd.DataFrame]
        mapping from question name (e.g. "q15") to DataFrame of non-null responses
    """

    clusters = [
        "q01",
        "q02",
        "q03",
        "q03_regional",
        "q03_subregional",
        "q05",
        "q06",
        "q07",
        "q11",
    ]
    headers = ["q15", "q16", "q18", "q20", "q21", "q22"]
    comments = {}
    for header in headers:
        q = data.dropna(subset=header)
        h = clusters + [
            header,
            f"{header}_ja",
            f"{header}_polarity",
            f"{header}_subjectivity",
        ]
        comment = q[h]
        comments.update({header: comment.sort_values(by="q11")})

    return comments


def response(data: pd.DataFrame) -> alt.LayerChart:
    """
    アンケートの回答状況

    アンケートの回答日時を使って、日時と時刻のヒートマップを作成します。
    関係するメールを送った反応があったかどうかを調べることができます。
    （回答日時は日本時間（UTC+0900）で保存されているようです）

    Parameters
    ----------
    data : pd.DataFrame
        前処理したデータフレーム

    Returns
    -------
    alt.LayerChart
        回答状況のヒートマップ
    """

    base = alt.Chart(data).encode(
        alt.X("yearmonthdate(timestamp)").title("回答した日時"),
        alt.Y("hours(timestamp)").title("回答した時刻"),
    )

    mark = base.mark_rect().encode(
        alt.Color("count()").title("回答数").scale(scheme="blues"),
    )

    text = base.mark_text(dx=30, dy=-15).encode(
        alt.Text("count()"),
    )

    chart = (mark + text).properties(
        title="アンケートの回答状況",
        width=800,
        height=800,
    )
    return chart


def group_data(data: pd.DataFrame, x: str, color: str) -> pd.DataFrame:
    """データフレームをグループ化

    Parameters
    ----------
    - `data : pd.DataFrame`
        前処理済みのデータフレーム
    - `x: str`
        X軸に設定するカラム名
    - `color: str`
        色のグループ化に設定するカラム名

    Returns
    -------
    - `pd.DataFrame`
        グループ化したデータフレーム
    """

    g = [x, color]
    c = "response"
    grouped = data.groupby(g)[c].sum().reset_index()
    return grouped


def group_hbar(data: pd.DataFrame, x: str, color: str, title: str, y: str = "response"):
    """
    groupbyで集計したデータをヒストグラムにする

    ヒストグラムは、積み上げ棒グラフと、割合グラフの2種類作成します。
    割合グラフには、回答数をテキストでオーバーレイ表示します。
    Jupyter Notebookで開く場合、受け取ったLayeredChartをinteractiveすることで、
    tooltipをホバー表示できます。

    Parameters
    ----------
    data : pd.DataFrame
        grouped DataFrame produced by group_data(), with columns for x, color, and y
    x : str
        X軸に設定するカラム名
    color : str
        色のグループ化に設定するカラム名
    title : str
        プロットのタイトル
    y : str, optional
        Y軸に設定するカラム名, by default "response" or "count()"

    Returns
    -------
    tuple[alt.Chart, alt.LayerChart]
        a tuple of (mark, stack + text) where mark is a stacked bar chart and
        stack + text is a normalized bar chart with count annotations overlaid
    """
    color = f"{color}:N"
    base = (
        alt.Chart(data)
        .encode(
            alt.X(x),
            alt.Y(y),
        )
        .properties(
            title=title,
            width=400,
        )
    )
    opacity = 0.5

    mark = base.mark_bar(tooltip=True, opacity=opacity).encode(
        alt.Y(y),
        alt.Color(color),
    )

    stack = base.mark_bar(tooltip=True, opacity=opacity).encode(
        alt.Y(y).stack("normalize"),
        alt.Color(color),
    )

    text = base.mark_text(dy=10).encode(
        alt.Y(y).stack("normalize"),
        alt.Text(y),
        alt.Color(color),
    )

    return (mark, stack + text)


def hbar(data: pd.DataFrame, x: str, color: str, title: str):
    """
    Create grouped histogram for a single (x, color) pair.

    Parameters
    ----------
    data : pd.DataFrame
        preprocessed survey DataFrame
    x : str
        column name to use as the x-axis
    color : str
        column name to use for color grouping
    title : str
        chart title

    Returns
    -------
    tuple[pd.DataFrame, alt.LayerChart]
        a tuple of (grouped, histograms) where grouped is the aggregated DataFrame
        and histograms is a side-by-side Altair chart (stacked | normalized)
    """
    grouped = group_data(data, x, color)
    h1, h2 = group_hbar(grouped, x, color, title)
    histograms = h1 | h2
    return grouped, histograms


def hbar_loop(data: pd.DataFrame, headers: list):
    """
    Create grouped histograms for all (x, color) pairs in headers.

    Parameters
    ----------
    data : pd.DataFrame
        preprocessed survey DataFrame
    headers : list
        list of (x, color) tuples specifying column pairs to plot

    Returns
    -------
    tuple[dict[str, pd.DataFrame], dict[str, alt.LayerChart]]
        a tuple of (grouped_data, hbars_data) where each dict maps
        "x-color" pair names to the corresponding grouped DataFrame or chart
    """
    grouped_data: dict = {}
    hbars_data: dict = {}
    for pair in headers:
        x, color = pair
        name = f"{x}-{color}"
        grouped, chart = hbar(data, x=x, color=color, title=name)
        grouped_data.update({name: grouped})
        hbars_data.update({name: chart})
    return grouped_data, hbars_data


def crosstab(data: pd.DataFrame, x: str, y: str):
    """
    Compute cross-tabulation and chi-square test, then build a heatmap.

    Parameters
    ----------
    data : pd.DataFrame
        preprocessed survey DataFrame
    x : str
        column name for the x-axis (rows in cross-tabulation)
    y : str
        column name for the y-axis (columns in cross-tabulation)

    Returns
    -------
    tuple[pd.DataFrame, scipy.stats.Chi2ContingencyResult, alt.LayerChart]
        a tuple of (cross_tab, chi2_test, chart) where cross_tab is the
        contingency table, chi2_test is the scipy result object, and chart
        is an Altair heatmap with count annotations
    """
    cross_tab, chi2_test = crosstab_data(data, x, y)

    z = "count"
    melted = cross_tab.reset_index().melt(id_vars=x, var_name=y, value_name=z)
    melted[x] = melted[x].astype(data[x].dtype)
    melted[y] = melted[y].astype(data[y].dtype)

    chart = crosstab_heatmap(melted, x, y, z)

    return cross_tab, chi2_test, chart


def crosstab_data(data: pd.DataFrame, x: str, y: str):
    """
    クロス集計とカイ二乗検定

    カラムXとカラムYの2つの離散変数に対して、
    ``pd.crosstab(index, columns)``でクロス集計し、
    ``scipy.stats.chi2_contingency(observed)``で
    （ピアソンの）カイ二乗検定します。

    カイ二乗検定はデフォルトで``correction=True``となっていて、
    自由度が1のとき、Yates'の連続補正がかかります。
    これは集計数が少ないときにp値を大きくするための補正です。

    クロス集計したデータフレーム（``cross_tab``）と、
    検定の結果（``statistic``、``pvalue``、``dof``、``expected``）を返します。

    Parameters
    ----------
    data : pd.DataFrame
        前処理済のデータフレーム
    x : str
        集計するカラム名（X軸）
    y : str
        集計するカラム名（Y軸）

    Returns
    -------
    tuple[pd.DataFrame, scipy.stats.Chi2ContingencyResult]
        a tuple of (cross_tab, chi2_test) where cross_tab is the contingency
        table DataFrame and chi2_test contains statistic, pvalue, dof, and
        expected_freq attributes
    """

    cross_tab = pd.crosstab(data[x], data[y])
    chi2_test = chi2_contingency(cross_tab)
    return cross_tab, chi2_test


def crosstab_heatmap(data: pd.DataFrame, x: str, y: str, z: str) -> alt.LayerChart:
    """
    クロス集計のヒートマップを作成

    入力データは、クロス集計表をロングデータに変換したものを与えてください。
    クロス集計表をヒートマップ（``mark_rect``）に描いた上に、
    頻度をテキスト表示（``mark_text``）をした``altair.LayerChart``を返します。

    プロットサイズはデフォルトで800x800にしていますが、
    受け取ったあとに自由に変更してください。

    Parameters
    ----------
    data : pd.DataFrame
        クロス集計したデータフレーム
    x : str
        集計結果のカラム名（X軸）
    y : str
        集計結果のカラム名（Y軸）
    z : str
        集計結果のカラム名（Z軸・カラー）

    Returns
    -------
    alt.LayerChart
        集計結果のヒートマップ
    """

    base = alt.Chart(data).encode(
        alt.X(x).axis(labelFontSize=20, titleFontSize=50),
        alt.Y(y).axis(labelFontSize=20, titleFontSize=50),
    )
    mark = base.mark_rect().encode(
        alt.Color(z).scale(scheme="blues"),
    )
    text = base.mark_text(fontSize=20).encode(
        text=alt.condition(
            alt.datum[z] > 0,
            alt.Text(f"{z}:Q"),
            alt.value(""),
        )
    )
    chart = (mark + text).properties(
        width=800,
        height=800,
    )
    return chart


def crosstab_loop(data: pd.DataFrame, headers: list):
    """
    クロス集計のループ

    集計したい離散変数（カラムXとカラムYのペア）のリストを与えて、
    一括してクロス集計とカイ二乗検定した結果を返します。

    Parameters
    ----------
    data : pd.DataFrame
        前処理済みのデータフレーム
    headers : list
        カラム名のペアのリスト

    Returns
    -------
    tuple[dict[str, pd.DataFrame], dict[str, alt.LayerChart], pd.DataFrame]
        a tuple of (cross_tabs, heatmaps, chi2_data) where cross_tabs maps pair
        names to contingency tables, heatmaps maps pair names to Altair heatmap
        charts, and chi2_data is a DataFrame of chi-square test statistics for
        all pairs
    """

    cross_tabs = {}
    heatmaps = {}
    chi2_tests = []

    for h in headers:
        x, y = h
        name = f"{x}-{y}"

        cross_tab, chi2_test, heatmap = crosstab(data, x, y)
        cross_tabs.update({name: cross_tab})
        heatmaps.update({name: heatmap})

        _data = [name, chi2_test.pvalue, chi2_test.statistic, chi2_test.dof, x, y]
        chi2_tests.append(_data)

    chi2_data = pd.DataFrame(
        chi2_tests, columns=["questions", "p_value", "statistic", "dof", "x", "y"]
    )

    return cross_tabs, heatmaps, chi2_data
