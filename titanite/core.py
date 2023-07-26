from pathlib import Path

import altair as alt
import pandas as pd
from loguru import logger
from scipy.stats import chi2_contingency

from .config import Config


def comment_data(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Parse comment data

    1. 自由記述の回答を抽出する（無回答を削除）
    2. 自動で翻訳する
    3. 質問番号ごとにJSONファイルに出力する
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
        # print(f"{header}: {len(q)}")
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

    # mark = base.mark_point().encode(
    #     alt.Color("count()").title("回答数"),
    #     alt.Size("count()"),
    #     alt.Shape("q03_regional").title("地域（勤務地）"),
    # )
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

def group_data(data: pd.DataFrame, x:str, color:str) -> pd.DataFrame:
    """
    データフレームをグループ化

    Parameters
    ----------
    data : pd.DataFrame
        前処理済みのデータフレーム
    x: str
        X軸に設定するカラム名
    color: str
        色のグループ化に設定するカラム名

    Returns
    -------
    pd.DataFrame
        グループ化したデータフレーム
    """

    group = [x, color]
    c = "response"
    grouped = data.groupby(group)[c].sum().reset_index()
    return grouped

def group_hbar(data: pd.DataFrame, x: str, color: str, y:str = "response", title="no_title"):
    """
    groupbyで集計したデータをヒストグラムにする

    ヒストグラムは、積み上げ棒グラフと、割合グラフの2種類作成します。
    割合グラフには、回答数をテキストでオーバーレイ表示します。
    Jupyter Notebookで開く場合、受け取ったLayeredChartをinteractiveすることで、
    tooltipをホバー表示できます。

    Parameters
    ----------
    data : pd.DataFrame
        _description_
    x : str
        X軸に設定するカラム名
    color : str
        色のグループ化に設定するカラム名
    y : str, optional
        Y軸に設定するカラム名, by default "response" or "count()"
    title : str, optional
        プロットのタイトル, by default "no_title"

    Returns
    -------
    _type_
        _description_
    """
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


def crosstab(data: pd.DataFrame, x: str, y: str):
    # クロス集計とカイ二乗検定
    cross_tab, chi2_test = crosstab_data(data, x, y)

    # データをロングデータに変換
    z = "count"
    melted = cross_tab.reset_index().melt(id_vars=x, var_name=y, value_name=z)
    # 元データのカテゴリ型で上書き
    melted[x] = melted[x].astype(data[x].dtype)
    melted[y] = melted[y].astype(data[y].dtype)

    # ヒートマップを作成
    chart = crosstab_heatmap(melted, x, y, z)

    return cross_tab, chi2_test, chart


def crosstab_data(data: pd.DataFrame, x: str, y: str):
    """
    クロス集計とカイ二乗検定

    カラムXとカラムYの2つの離散変数に対して、
    ``pd.crosstab(index, columns)``でクロス集計し、
    ``scipy.stats.chi2_contigency(observed)``で
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
    _type_
        _description_
    """

    # クロス集計とカイ二乗検定
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
    color : str
        集計結果のカラム名（Z軸・カラー）

    Returns
    -------
    alt.LayerChart
        集計結果のヒートマップ
    """

    # グラフを作成
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
    _type_
        いろいろ
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

        _data = [name, chi2_test.pvalue, chi2_test.statistic, chi2_test.dof]
        chi2_tests.append(_data)

    chi2_data = pd.DataFrame(
        chi2_tests, columns=["questions", "p_value", "statistic", "dof"]
    )

    return cross_tabs, heatmaps, chi2_data


if __name__ == "__main__":
    import titanite as ti

    fname = "../sandbox/config.toml"
    cfg = ti.Config(fname=fname)
    cfg.load()
    category = cfg.categories()

    fname = "../sandbox/tmp_preprocessed.csv"
    data = pd.read_csv(fname, parse_dates=["timestamp"])
    data = ti.categorical_data(data, category)
    logger.debug(len(sorted(data.columns)))

    grouped = group_data(data, x="q1", y="q2")
    logger.debug(len(sorted(grouped.columns)))
