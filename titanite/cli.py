from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from .config import Config
from .preprocess import preprocess_data

app = typer.Typer()


@app.command()
def config(load_from: str = "config.toml", show: bool = True):
    """Show configuration"""
    _fname = Path(load_from)
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
    write_to: str = "tmp_preprocessed.csv",
    load_from: str = "config.toml",
):
    """
    Prepare data

    CSV形式で出力したGoogleスプレッドシートの回答を読み込み、
    前処理したデータを生成します。
    """
    cfg = config(load_from, show=False)
    category = cfg.categories()

    data = pd.read_csv(read_from, skiprows=1)
    data = preprocess_data(data, category)
    data.to_csv(write_to, index=False)
    msg = f"Saved as {write_to}"


    logger.info(msg)

@app.command()
def delete(item: str):
    print(f"Deleting item: {item}")


@app.command()
def sell(item: str):
    print(f"Selling item: {item}")


if __name__ == "__main__":
    app()
