from pathlib import Path

import typer
from loguru import logger

from .config import Config

app = typer.Typer()


@app.command()
def config(fname: str = "config.toml", confd: str = ".", show: bool = False):
    """Show configuration"""
    _fname = Path(confd) / fname
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
def create(item: str):
    print(f"Creating item: {item}")


@app.command()
def delete(item: str):
    print(f"Deleting item: {item}")


@app.command()
def sell(item: str):
    print(f"Selling item: {item}")


if __name__ == "__main__":
    app()
