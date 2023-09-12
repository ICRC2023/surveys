from pathlib import Path

import altair as alt
import pandas as pd
import typer
from loguru import logger

from . import core
from .config import Config, Data
from .preprocess import categorical_data, preprocess_data, sentiment_data

app = typer.Typer()


@app.command()
def config(
    load_from: str = "config.toml", questions: bool = False, choices: bool = False
):
    """Show configuration"""
    _fname = Path(load_from)
    logger.info(f"Loaded config from: {_fname}")
    cfg = Config(fname=_fname)
    cfg.load()

    if questions:
        print("=== Questions ===")
        for k, v in cfg.questions.items():
            print(k, v)

    if choices:
        print("=== Choices ===")
        for k, v in cfg.choices.items():
            print(k, v)

    if not (questions and choices):
        cfg.show()

    return


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
    c = Config(load_from=load_from)
    categories = c.categorical()

    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, skiprows=1)
    data = preprocess_data(data)
    data = categorical_data(data, categories)
    data = sentiment_data(data)

    fname = Path(write_dir) / "prepared_data.csv"
    data.to_csv(fname, index=False)

    # Write only categorical data
    d = Data(read_from="")
    headers = ["timestamp", "response"] + d.categorical_headers
    fname = Path(write_dir) / "categorical_data.csv"
    data[headers].to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")


@app.command()
def comments(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/comment/",
    load_from: str = "config.toml",
) -> None:
    """
    Create comment sentiment analysis data.

    Parameters
    ----------
    read_from : str, optional
        _description_, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        _description_, by default "../data/test_data/comment/"
    load_from : str, optional
        _description_, by default "config.toml"
    """
    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()
    comments = core.comment_data(data)

    for name, comment in comments.items():
        fname = Path(write_dir) / f"{name}.csv"
        comment.to_csv(fname, index=False)
        logger.info(f"Saved as {fname}")
        fname = fname.with_suffix(".json")
        comment.to_json(fname, orient="records")
        logger.info(f"Saved as {fname}")

    return


@app.command()
def hbar(
    header: str,
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
):
    """
    (WIP) Create histogram.

    保存先:
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.csv"
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.json"
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.png"
    """
    d = Data(read_from=read_from, load_from=load_from)
    config = d.config()
    questions = config.get("questions")

    key = header.split("_")[0]
    t = questions.get(key, "no_title")

    data = d.read()
    headers = d.headers([header], sorted(data.columns))
    grouped_data, hbar_data = core.hbar_loop(data, headers)

    fnames = {}

    for name, grouped in grouped_data.items():
        fname = Path(write_dir) / header / f"{name}.csv"
        grouped.to_csv(fname, index=False)
        logger.info(f"Saved data to: {fname}")
        info = {name: {"csv": fname}}
        fnames.update(info)

    for name, hbar in hbar_data.items():
        fname = Path(write_dir) / header / f"{name}.png"
        hbar.save(fname)
        logger.info(f"Saved chart to: {fname}")
        info = {name: {"png": fname}}
        fnames.update(info)

    return


@app.command()
def hbars(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
    save: bool = False,
):
    """
    Run hbar for round-robin headers.

    Parameters
    ----------
    read_from : str, optional
        _description_, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        _description_, by default "../data/test_data/hbar/"
    load_from : str, optional
        _description_, by default "config.toml"
    save : bool, optional
        _description_, by default False
    """

    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    config = d.config()
    questions = config.get("questions")

    data = d.read()
    matches = d.matches(list(data.columns))
    grouped_data, hbar_data = core.hbar_loop(data, list(matches))

    if save:
        for name, gdata in grouped_data.items():
            fname = Path(write_dir) / f"{name}.csv"
            gdata.to_csv(fname, index=False)
            logger.info(f"Saved data to: {fname}")

        for name, hbar in hbar_data.items():
            fname = Path(write_dir) / f"{name}.png"
            hbar.save(fname)
            logger.info(f"Saved chart to: {fname}")

    logger.info("Finished !")
    return


@app.command()
def crosstabs(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/crosstab/",
    load_from: str = "config.toml",
    save: bool = False,
) -> None:
    """
    Run crosstab for all headers.

    アンケート項目をクロス集計し、相関関係を調べます。
    離散変数になっている2つの質問を総当たりして、相関データを生成します。
    相関関係はカイ二乗検定で評価します。

    Parameters
    ----------
    read_from : str, optional
        path to preprocessed data file, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        path to save processed files, by default "../data/test_data/crosstab/"
    load_from : str, optional
        path to configuration file, by default "config.toml"
    """

    # 総当たりでクロス集計
    cross_tabs, heatmaps = chi2(
        read_from=read_from,
        write_dir=write_dir,
        load_from=load_from,
    )

    if save:
        for name, cross_tab in cross_tabs.items():
            fname = Path(write_dir) / f"{name}.csv"
            cross_tab.to_csv(fname)
            logger.info(f"Saved data to: {fname}")

        for name, heatmap in heatmaps.items():
            fname = Path(write_dir) / f"{name}.png"
            heatmap.save(fname)
            logger.info(f"Saved chart to: {fname}")

    logger.info("Finished !")
    return


@app.command()
def chi2(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/chi2_test/",
    load_from: str = "config.toml",
) -> tuple:
    """
    Create chi2_test

    Parameters
    ----------
    read_from : str, optional
        _description_, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        _description_, by default "../data/test_data/chi2_test/"
    load_from : str, optional
        _description_, by default "config.toml"

    Returns
    -------
    tuple
        _description_
    """

    import itertools

    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()

    # 総当たりしたいカラム名を整理
    headers = [h for h in sorted(data.columns) if h in d.categorical_headers]

    # 総当たりの組み合わせ
    matches = list(itertools.combinations(headers, 2))

    # 総当たりでクロス集計
    cross_tabs, heatmaps, chi2_data = core.crosstab_loop(data, matches)

    # カイ二乗検定の結果を保存する
    fname = Path(write_dir) / "chi2_test.csv"
    chi2_data.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")
    fname = fname.with_suffix(".json")
    chi2_data.to_json(fname, orient="records")
    logger.info(f"Saved data to: {fname}")

    # p < 0.05 の結果を保存する
    p005 = chi2_data.query("p_value < 0.05")
    fname = Path(write_dir) / "chi2_test_p005.csv"
    p005.to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")
    fname = fname.with_suffix(".json")
    p005.to_json(fname, orient="records")
    logger.info(f"Saved data to: {fname}")

    return cross_tabs, heatmaps


@app.command()
def p005(
    header: str,
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/p005/",
    load_from: str = "config.toml",
    save: bool = False,
) -> None:
    """
    Create p < 0.05 data.

    引数 header に対してクロス集計し、相関がある（＝``p< 0.05``）の項目のみデータを生成します。

    Parameters
    ----------
    header : str
        name of column
    read_from : str, optional
        path to preprocessed data file, by default "../data/test_data/prepared_data.csv"
    write_dir : str, optional
        path to save processed files, by default "../data/test_data/p005/"
    """

    d = Data(read_from=read_from, load_from=load_from)
    is_valid_header(header, d.categorical_headers)

    save_dir = Path(write_dir) / header
    is_valid_path(save_dir)

    data = d.read()
    headers = d.headers([header], sorted(data.columns))
    cross_tabs, heatmaps, chi2_data = core.crosstab_loop(data, headers)

    # p < 0.05 の項目を抽出
    chi2_p005 = chi2_data.query("p_value < 0.05").copy()
    chi2_p005["png"] = str(save_dir) + "/" + chi2_p005["questions"] + ".png"
    # データフレームをCSVとJSONで保存
    fname = Path(write_dir) / header / f"chi2_test_p005_{header}.csv"
    chi2_p005.to_csv(fname, index=False)
    logger.info(f"Saved data to {fname}")
    fname = fname.with_suffix(".json")
    chi2_p005.to_json(fname, orient="records")
    logger.info(f"Saved data to {fname}")

    if save:
        for index, row in chi2_p005.iterrows():
            name = row.questions
            fname = row.png
            hm = heatmaps.get(name)
            hm = hm.properties(
                title={
                    "text": name,
                    "fontSize": 40,
                },
                width=800,
                height=800,
            )
            hm.save(fname)
            logger.info(f"Saved chart to {fname}")
    return


@app.command()
def crosstab(
    header: str,
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
):
    """
    (WIP) Create crosstab.

    保存先:
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.csv"
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.json"
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.png"
    """
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()

    pass


def is_valid_header(test_header: str, valid_headers: list) -> None:
    """
    header が処理してよい値か確認する

    Parameters
    ----------
    data : pd.DataFrame
        description_
    header : str
        _description_

    Raises
    ------
    typer.Exit
        _description_
    """

    if not test_header in valid_headers:
        logger.error(f"Given header '{test_header}' is invalid.")
        logger.warning(f"Please choose from {valid_headers}")
        raise typer.Exit(code=1)


def is_valid_path(path: Path) -> None:
    if not path.exists():
        logger.error(f"No file/directory found: {path}")
        logger.error(f"Make sure if the path is correct or please create it first.")
        raise typer.Exit(code=1)


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
