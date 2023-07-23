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
    crosstab_ignore: list[str] = [
        "q10",
        "q13",
        "q15",
        "q15_ja",
        "q15_polarity",
        "q15_subjectivity",
        "q16",
        "q16_ja",
        "q16_polarity",
        "q16_subjectivity",
        "q18",
        "q18_ja",
        "q18_polarity",
        "q18_subjectivity",
        "q20",
        "q20_ja",
        "q20_polarity",
        "q20_subjectivity",
        "q21",
        "q21_ja",
        "q21_polarity",
        "q21_subjectivity",
        "q22",
        "q22_ja",
        "q22_polarity",
        "q22_subjectivity",
        "response",
        "timestamp",
    ]

    def read(self):
        config = Config(fname=self.load_from)
        config.load()
        category = config.categories()
        data = pd.read_csv(self.read_from, parse_dates=["timestamp"])
        data = categorical_data(data, category)
        return data

    def crosstab_headers(self, x:list[str], y:list[str]) -> list:
        """
        クロス集計のカラム名

        x と y の二つの文字列リストを引数として受け取り、
        x の各要素と y の各要素のすべての組み合わせを生成します。

        ただし、y のリストからは以下の要素を除外しています。
        - クロス集計から除外したいカラム名
        - x の値（自分自身とクロス集計できないため）

        Parameters
        ----------
        x : list[str]
            とくにフォーカスしたい集計カラム名
        y : list[str]
            クロス集計結果に含まれるすべてのカラム名

        Returns
        -------
        _type_
            集計するカラム名のリスト
        """
        import itertools
        ignored = self.crosstab_ignore
        columns = [col for col in y if col not in ignored]
        return [[_x, _y] for _x, _y in itertools.product(x, columns) if _x != _y]



if __name__ == "__main__":
    settings = {"confd": "../sandbox/", "fname": "config.toml"}

    c = Config(**settings)
    c.load()
    logger.debug(c.fname)
    logger.debug(c.get("questions").keys())
    logger.debug(c.get("choices").keys())
