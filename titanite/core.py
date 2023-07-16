import altair as alt
import pandas as pd

from .config import Config


def group_data(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    """
    データフレームをグループ化

    Parameters
    ----------
    data : pd.DataFrame
        前処理済みのデータフレーム
    x : str
        X軸に設定する質問の番号
    y : str
        Y軸に設定する質問の番号

    Returns
    -------
    pd.DataFrame
        グループ化したデータフレーム
    """

    names = [x, y]
    z = "response"
    grouped = data.groupby(names)[z].sum().reset_index()
    return grouped


def heatmap(data: pd.DataFrame, x: str, y: str) -> dict:
    grouped = group_data(data, x, y)
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


if __name__ == "__main__":
    from loguru import logger

    import titanite as ti

    fname = "../sandbox/config.toml"
    cfg = ti.Config(fname=fname)
    cfg.load()
    category = cfg.categories()

    fname = "../sandbox/tmp_preprocessed.csv"
    data = pd.read_csv(fname, parse_dates=["timestamp"])
    data = ti.categorical_data(data, category)
    logger.debug(len(sorted(data.columns)))

    grouped = group(data, x="q1", y="q2")
    logger.debug(len(sorted(grouped.columns)))
