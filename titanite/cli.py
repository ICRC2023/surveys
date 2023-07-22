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
def comment(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/",
) -> None:
    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, parse_dates=["timestamp"])
    comment_json(data, write_dir)
    return


@app.command()
def crosstab(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml",
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

    headers = []
    for h in sorted(data.columns):
        if h not in d.ignore_from_crosstab:
            headers.append(h)
    # headers = [header for header in sorted(data.columns) if header not in ignored]
    matches = list(itertools.combinations(headers, 2))

    chi2_tests = []
    for m in matches:
        cross_tab, chi2_test, heatmap = core.crosstab(data, m)

        x, y = m
        name = f"{x}-{y}"
        _data = [name, chi2_test.statistic, chi2_test.pvalue, chi2_test.dof]
        chi2_tests.append(_data)

        fname = Path(write_dir) / "crosstab" / f"{name}.csv"
        cross_tab.to_csv(fname)
        logger.info(f"Saved data to: {fname}")

        fname = Path(write_dir) / "crosstab" / f"{name}.png"
        heatmap.save(fname)
        logger.info(f"Saved chart to: {fname}")

    chi2_data = pd.DataFrame(chi2_tests, columns=["questions", "statistic", "p-value", "dof"])
    fname = Path(write_dir) / "chi2_test.csv"
    chi2_data.to_csv(fname, index=False)
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
