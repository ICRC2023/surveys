from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from .config import Config
from .core import preprocess_data

app = typer.Typer()


@app.command()
def config(fname: str = "config.toml", show: bool = True):
    """Show configuration"""
    _fname = Path(fname)
    if not _fname.exists():
        msg = f"File Not Found: {_fname} ({_fname.resolve()})"
        logger.error(msg)
        raise typer.Exit(code=1)

    c = Config(fname=_fname)
    c.load()
    if show:
        c.show()
        return
    return c


@app.command()
def create(i: str, o: str = "tmp_preprocessed.csv", c: str = "config.toml"):
    """
    Create preprocessed data
    """
    _config = config(c, show=False)
    category = _config.categories()

    data = pd.read_csv(i, skiprows=1)
    data = preprocess_data(data, category)
    data.to_csv(o, index=False)
    msg = f"Saved as {o}"
    logger.info(msg)


@app.command()
def delete(item: str):
    print(f"Deleting item: {item}")


@app.command()
def sell(item: str):
    print(f"Selling item: {item}")


if __name__ == "__main__":
    app()
