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
    numerical_headers: list[str] = [
        "q10",
        "q13",
        "q15_polarity",
        "q15_subjectivity",
        "q16_polarity",
        "q16_subjectivity",
        "q18_polarity",
        "q18_subjectivity",
        "q20_polarity",
        "q20_subjectivity",
        "q21_polarity",
        "q21_subjectivity",
        "q22_polarity",
        "q22_subjectivity",
    ]
    categorical_headers: list[str] = [
        "q01",
        "q02",
        "q03_regional",
        "q03_subregional",
        "q04_regional",
        "q04_subregional",
        "q05",
        "q06",
        "q07",
        "q08",
        "q09",
        "q10_binned",
        "q11",
        "q12_genderbalance",
        "q12_diversity",
        "q12_equity",
        "q12_inclusion",
        "q13_binned",
        "q14",
        "q17_genderbalance",
        "q17_diversity",
        "q17_equity",
        "q17_inclusion",
        "q19",
    ]
    crosstab_ignore: list[str] = [
        "q03",
        "q04",
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

    def config(self):
        c = Config(fname=self.load_from)
        c.load()
        return c

    def read(self):
        config = self.config()
        config.load()
        category = config.categories()
        data = pd.read_csv(self.read_from, parse_dates=["timestamp"])
        data = categorical_data(data, category)
        return data

    def matches(self, columns: list):
        import itertools

        # 総当たりしたいカラム名を整理
        # カラム名は基本的にデータフレームにあるものを与える
        # クロス集計しないことにしたカラムは除外する
        headers = [h for h in sorted(columns) if h not in self.crosstab_ignore]
        # 総当たりの組み合わせ
        matches = list(itertools.combinations(headers, 2))
        return matches



    def crosstab_headers(self, x: list[str], y: list[str]) -> list:
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
