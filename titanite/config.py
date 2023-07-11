
from pathlib import Path

from loguru import logger
from pydantic import BaseModel


class Config(BaseModel):
    confd: str = "."
    fname: str = "config.toml"

if __name__ == "__main__":

    config_data = {
        "confd": "John Doe",
        "fname": "johndoe@example.com"
    }

    config = Config(**config_data)
    logger.debug(config.confd)
    logger.debug(config.fname)