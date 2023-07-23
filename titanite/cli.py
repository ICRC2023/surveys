from pathlib import Path

import altair as alt
import pandas as pd
import typer
from loguru import logger

from . import core
from .config import Config, Data
from .preprocess import categorical_data, preprocess_data

app = typer.Typer()


@app.command()
def config(load_from: str = "config.toml", show: bool = True):
    """Show configuration"""
    _fname = Path(load_from)
    logger.info(f"Loaded config from: {_fname}")

    if not _fname.exists():
        msg = f"File Not Found: {_fname} ({_fname.resolve()})"
        logger.error(msg)
        raise typer.Exit(code=1)

    cfg = Config(fname=_fname)
    cfg.load()

    if show:
        cfg.show()
        return

    return cfg


@app.command()
def prepare(
    read_from: str,
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml",
) -> None:
    """
    Prepare data

    CSV形式で出力したGoogleスプレッドシートの回答を読み込み、
    前処理したデータを生成します。
    """
    cfg = config(load_from, show=False)
    category = cfg.categories()

    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, skiprows=1)
    data = preprocess_data(data)
    data = categorical_data(data, category)
    fname = Path(write_dir) / "prepared_data.csv"
    data.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")


@app.command()
def comments(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml",
) -> None:

    cfg = config(load_from, show=False)

    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()
    comments = core.comment_data(data)
    for name, comment in comments.items():
        fname = Path(write_dir) / "comment" / f"{name}.csv"
        comment.to_csv(fname, index=False)
        logger.info(f"Saved as {fname}")
        fname = fname.with_suffix(".json")
        comment.to_json(fname, orient="records")
        logger.info(f"Saved as {fname}")
    return


@app.command()
def crosstabs(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml",
    save: bool = False,
) -> None:
    """
    Run crosstab

    アンケート項目をクロス集計し、相関関係を調べます。
    離散変数になっている2つの質問を総当たりして、相関データを生成します。
    相関関係はカイ二乗検定で評価します。

    Parameters
    ----------
    read_from : str, optional
        path to preprocessed data file, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        path to save processed files, by default "../data/test_data/"
    load_from : str, optional
        path to configuration file, by default "config.toml"
    """
    import itertools

    cfg = config(load_from, show=False)

    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()

    # 総当たりを組みたいカラム名を整理
    # headers = [header for header in sorted(data.columns) if header not in ignored]
    headers = []
    for h in sorted(data.columns):
        if h not in d.crosstab_ignore:
            headers.append(h)

    # 総当たりの組み合わせ
    matches = list(itertools.combinations(headers, 2))

    # 総当たりでクロス集計
    cross_tabs, heatmaps, chi2_data = core.crosstab_loop(data, matches)

    if save:
        for name, cross_tab in cross_tabs.items():
            fname = Path(write_dir) / "crosstab" / f"{name}.csv"
            cross_tab.to_csv(fname)
            logger.info(f"Saved data to: {fname}")

        for name, heatmap in heatmaps.items():
            fname = Path(write_dir) / "crosstab" / f"{name}.png"
            heatmap.save(fname)
            logger.info(f"Saved chart to: {fname}")

    # カイ二乗検定の結果を保存
    fname = Path(write_dir) / "crosstab"
    chi2_data["png"] = str(fname) + "/" + chi2_data["questions"] + ".png"
    fname = Path(write_dir) / "chi2_test" / "chi2_test.csv"
    chi2_data.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")
    fname = fname.with_suffix(".json")
    chi2_data.to_json(fname, orient="records")
    logger.info(f"Saved data to: {fname}")

    chi2_p005 = chi2_data.query("p_value < 0.05")
    fname = Path(write_dir) / "chi2_test" / "chi2_test_p005.csv"
    chi2_p005.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")
    fname = fname.with_suffix(".json")
    chi2_p005.to_json(fname, orient="records")
    logger.info(f"Saved data to: {fname}")

    return


@app.command()
def response(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/",
) -> None:
    """
    Check responses

    アンケートに回答した日時を調べる

    Parameters
    ----------
    read_from : str, optional
        path to preprocessed data file, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        path to save processed files, by default "../data/test_data/"
    """
    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, parse_dates=["timestamp"])
    chart = core.response(data)
    fname = Path(write_dir) / "response.png"
    chart.save(fname)
    logger.info(f"Saved chart to: {fname}")


if __name__ == "__main__":
    app()
