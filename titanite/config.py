import tomllib
from pathlib import Path

import pandas as pd
from loguru import logger
from pydantic import BaseModel

from .preprocess import categorical_data


class Config(BaseModel):
    fname: str | Path = "config.toml"
    questions: dict | None = {}
    choices: dict | None = {}

    def load(self):
        config = self.load_toml()
        self.questions = config.get("questions")
        self.choices = config.get("choices")

    def load_toml(self):
        fname = Path(self.fname)
        with fname.open("rb") as f:
            config = tomllib.load(f)
        return config

    def categories(self):
        from pandas.api.types import CategoricalDtype

        _categories = {}

        for k, v in self.choices.items():
            _categories[k] = CategoricalDtype(categories=v, ordered=True)

        return _categories

    def show(self):
        """
        Print configuration
        """
        f = Path(self.fname)
        q = self.questions
        c = self.choices

        print("=" * 80)
        print("Configuration file")
        print("=" * 80)
        print(f)
        print(f.absolute())
        print("\n")

        # List questions
        print("=" * 80)
        print("Questions")
        print("=" * 80)
        for k, v in q.items():
            print(f"{k}= {v}")
        print("\n")

        # List Choices
        print("=" * 80)
        print("Choices")
        print("=" * 80)
        for k, v in c.items():
            print(f"{k}= {v}")
        print("\n")

        return

class Data(BaseModel):
    read_from: str | Path
    load_from: str = "config.toml"

    def read(self):
        config = Config(fname=self.load_from)
        config.load()
        category = config.categories()
        data = pd.read_csv(self.read_from, parse_dates=["timestamp"])
        data = categorical_data(data, category)
        return data

if __name__ == "__main__":
    settings = {"confd": "../sandbox/", "fname": "config.toml"}

    c = Config(**settings)
    c.load()
    logger.debug(c.fname)
    logger.debug(c.get("questions").keys())
    logger.debug(c.get("choices").keys())
