from pathlib import Path

import altair as alt
import pandas as pd
import typer
from loguru import logger

from . import core
from .config import Config
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
    fname = Path(write_dir) / "all.csv"
    data.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")

@app.command()
def comment(
    read_from: str = "../data/test_data/all.csv",
    write_dir: str = "../data/test_data/"
) -> None:

    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, parse_dates=["timestamp"])
    comment_json(data, write_dir)
    return


@app.command()
def crosstab(
    read_from: str,
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml"
) -> None:
    cfg = config(load_from, show=False)
    category = cfg.categories()

    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, parse_dates=["timestamp"])
    data = categorical_data(data, category)

    logger.debug(data.info())

    pass

@app.command()
def response(
    read_from: str,
    write_dir: str = "../data/test_data/",
) -> None:
    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, parse_dates=["timestamp"])
    chart = core.response(data)
    fname = Path(write_dir) / "response.png"
    chart.save(fname)
    logger.info(f"Saved chart to : {fname}")



if __name__ == "__main__":
    app()
