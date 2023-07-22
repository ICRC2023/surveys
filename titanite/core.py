from pathlib import Path

import altair as alt
import pandas as pd
from loguru import logger
from scipy.stats import chi2_contingency

from .config import Config


def group_data(data: pd.DataFrame, group: list) -> pd.DataFrame:
    """
    データフレームをグループ化

    Parameters
    ----------
    data : pd.DataFrame
        前処理済みのデータフレーム
    group : list
        X軸やY軸に設定する質問番号

    Returns
    -------
    pd.DataFrame
        グループ化したデータフレーム
    """

    c = "response"
    grouped = data.groupby(group)[c].sum().reset_index()
    return grouped


def heatmap(data: pd.DataFrame, x: str, y: str) -> dict:
    z = "response"
    graph = (
        alt.Chart(grouped)
        .mark_rect()
        .encode(
            alt.X(x),
            alt.Y(y),
            alt.Color(z),
        )
        .properties(
            width=500,
            height=500,
        )
    )

    insight = {
        "data": grouped,
        "chart": graph,
    }
    return insight


def comment_json(data: pd.DataFrame, write_dir: str) -> None:
    """
    Parse comment data

    1. 自由記述の回答を抽出する（無回答を削除）
    2. 自動で翻訳する
    3. 質問番号ごとにJSONファイルに出力する
    """

    attributes = ["q1", "q2", "q3", "q5", "q6", "q7"]
    headers = ["q15", "q16", "q18", "q20", "q21", "q22"]
    for header in headers:
        q = data.dropna(subset=header)
        # print(f"{header}: {len(q)}")
        h = attributes + [
            header,
            f"{header}_ja",
            f"{header}_polarity",
            f"{header}_subjectivity",
        ]
        fname = Path(write_dir) / f"{header}.json"
        q[h].sort_values(by=header).to_json(fname, orient="records")
        logger.info(f"Saved as {fname}")
    return


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

    mark = base.mark_point().encode(
        alt.Color("count()").title("回答数"),
        alt.Size("count()"),
        alt.Shape("q03_regional").title("地域（勤務地）"),
    )
    text = base.mark_text(dx=10, dy=-10).encode(
        alt.Text("count()"),
    )

    chart = (mark + text).properties(
        title="アンケートの回答状況",
        width=800,
        height=800,
    )
    return chart


def crosstab(data: pd.DataFrame, header: tuple):
    h0 = header[0]
    h1 = header[1]
    v = "response"

    ctab = pd.crosstab(data[h0], data[h1])
    chi2 = chi2_contingency(ctab)

    melted = ctab.reset_index().melt(id_vars=h0, var_name=h1, value_name=v)
    base = alt.Chart(melted).encode(
        alt.X(h1),
        alt.Y(h0),
    )

    mark = base.mark_rect().encode(
        alt.Color(v),
    )

    text = base.mark_text().encode(alt.Text(v))

    chart = (mark + text).properties(
        width=800,
        height=800,
    )
    return ctab, chi2, chart


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
