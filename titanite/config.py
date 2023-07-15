import tomllib
from pathlib import Path

from loguru import logger
from pydantic import BaseModel


class Config(BaseModel):
    confd: str = "."
    fname: str = "config.toml"
    questions: dict | None = {}
    choices: dict | None = {}

    def init(self):
        config = self.load_toml()
        self.questions = config.get("questions")
        self.choices = config.get("choices")

    def load_toml(self):
        fname = Path(self.confd) / self.fname
        with fname.open("rb") as f:
            config = tomllib.load(f)
        return config


if __name__ == "__main__":
    settings = {"confd": "../sandbox/", "fname": "config.toml"}

    c = Config(**settings)
    c.init()
    logger.debug(c.confd)
    logger.debug(c.fname)
    logger.debug(c.get("questions").keys())
    logger.debug(c.get("choices").keys())
