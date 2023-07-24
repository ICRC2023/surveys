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
def config(
    load_from: str = "config.toml",
    questions: bool = False,
    choices: bool = False
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
    cfg = Config(fname=load_from)
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
    write_dir: str = "../data/test_data/comment/",
    load_from: str = "config.toml",
) -> None:
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
def hbars(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
    save: bool = False
    ):

    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()
    matches = d.matches(list(data.columns))

    grouped_data = {}
    hbars = {}
    for m in list(matches):
        x, z = m
        name = f"{x}_{z}"
        grouped = core.group_data(data, list(m))
        grouped_data.update({name: grouped})

        y = "response"
        h = core.hbar(grouped, x, y, z)
        hbars.update({name: h})

    if save:
        for name, gdata in grouped_data.items():
            fname = Path(write_dir) / f"{name}.csv"
            gdata.to_csv(fname, index=False)
            logger.info(f"Saved data to: {fname}")


        for name, hbar in hbars.items():
            fname = Path(write_dir) / f"{name}.png"
            hbar.save(fname)
            logger.info(f"Saved chart to: {fname}")

    return



@app.command()
def crosstabs(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/crosstab/",
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

    for name, cross_tab in cross_tabs.items():
        fname = Path(write_dir) / f"{name}.csv"
        cross_tab.to_csv(fname)
        logger.info(f"Saved data to: {fname}")

    for name, heatmap in heatmaps.items():
        fname = Path(write_dir) / f"{name}.png"
        heatmap.save(fname)
        logger.info(f"Saved chart to: {fname}")

    return

@app.command()
def chi2(
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/chi2_test/",
    load_from: str = "config.toml",
    )-> tuple:

    import itertools
    logger.info(f"Read data from: {read_from}")
    d = Data(read_from=read_from, load_from=load_from)
    data = d.read()

    # 総当たりしたいカラム名を整理
    headers = [h for h in sorted(data.columns) if h not in d.crosstab_ignore]

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
    Show p < 0.05

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
    data = d.read()

    # header がデータフレームにない場合は終了する
    if not header in data.columns:
        logger.error(f"Given header '{header}' is not in dataframe.")
        logger.warning(f"Please choose from  '{list(data.columns)}'.")
        raise typer.Exit(code=1)

    # header が crosstab_ignore に含まれている場合は終了する
    if header in d.crosstab_ignore:
        logger.error(f"Given header '{header}' is in crosstab_ignore.")
        logger.warning(f"Please avoid choosing from  '{d.crosstab_ignore}'.")
        raise typer.Exit(code=1)

    save_dir = Path(write_dir) / header
    if not save_dir.exists():
        logger.error(f"No directory found: {save_dir}.")
        logger.warning(f"Make sure if the path is correct or please create it first.")
        raise typer.Exit(code=1)


    data = d.read()
    headers = d.crosstab_headers([header], list(data.columns))
    cross_tabs, heatmaps, chi2_data = core.crosstab_loop(data, headers)

    # p < 0.05 の項目を抽出
    chi2_p005 = chi2_data.query("p_value < 0.05").copy()
    chi2_p005["png"] = (str(save_dir) + "/" + chi2_p005["questions"] + ".png")
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
def hbar(
    header: str,
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
    ):
    """
    Create histograms.

    保存先:
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.csv"
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.json"
        - "../data/test/data/hbar/カラム名/カラム名-色カラム名.png"
    """
    pass

@app.command()
def crosstab(
    header: str,
    read_from: str = "../data/test_data/prepared_data.csv",
    write_dir: str = "../data/test_data/hbar/",
    load_from: str = "config.toml",
    ):
    """
    Create crosstabs.

    保存先:
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.csv"
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.json"
        - "../data/test/data/crosstab/カラム名/カラム名-相手カラム名.png"
    """
    pass


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
