import typer

from .config import Config

app = typer.Typer()


@app.command()
def config(fname: str = "config.toml", confd: str = ".", show: bool = False):
    """Show configuration"""
    settings = {
        "confd": confd,
        "fname": fname,
    }
    c = Config(**settings)
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
