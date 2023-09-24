import tomllib
from pathlib import Path

import pandas as pd
from deprecated import deprecated
from loguru import logger
from pydantic import BaseModel

from .preprocess import categorical_data

NUMERICAL_HEADERS: list[str] = [
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

CATEGORICAL_HEADERS: list[str] = [
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


class Config(BaseModel):
    # fname: str | Path = "config.toml"
    load_from: str = "config.toml"
    config: dict = {}
    categories: dict = {}
    options: dict = {}
    names: list = []
    titles: dict = {}
    descriptions: dict = {}
    category_maps: dict = {}
    categorical_headers: list = []
    numerical_headers: list = []
    comment_headers: list = []

    def load(self):
        self.config = self.load_config()
        self.categories = self.load_categories()
        self.options = self.load_options()
        self.names = self.get_names()
        self.titles = self.get_titles()
        self.descriptions = self.get_descriptions()
        self.category_maps = self.get_category_maps()
        self.categorical_headers = self.get_categorical_headers()
        self.numerical_headers = self.get_numerical_headers()
        self.comment_headers = self.get_comment_headers()

    def load_toml(self) -> dict:
        import typer

        fname = Path(self.load_from)
        if not fname.exists():
            logger.error(f"File not found: {fname}")
            raise typer.Exit(code=1)

        with fname.open("rb") as f:
            config = tomllib.load(f)
        return config

    def load_config(self) -> dict:
        config = self.load_toml()
        return config

    @deprecated(
        version="0.4.2",
        reason="Migrated to load_categories(). Loaded inside load(). Get with self.categories.",
    )
    def categorical(self):
        from pandas.api.types import CategoricalDtype

        config = self.load_config()
        categories = {}

        for k, v in config.get("choices").items():
            dtype = CategoricalDtype(categories=v, ordered=True)
            categories.update({k: dtype})

        self.categories = categories

        return categories

    def load_categories(self):
        from pandas.api.types import CategoricalDtype

        config = self.config
        categories = {}
        for k, v in config.get("choices").items():
            dtype = CategoricalDtype(categories=v, ordered=True)
            categories.update({k: dtype})
        return categories

    def load_options(self):
        config = self.config
        _options = config.get("options", "Not defined")
        options = pd.DataFrame(_options)
        return options

    def get_option(self, name: str):
        """Get values of options as dict"""
        options = self.options
        options.index = options["name"]
        option = options[[name]].dropna()
        option = option.to_dict().get(name)
        return option

    def get_names(self) -> list[str]:
        names = self.get_option("name")
        names = sorted(names.keys())
        return names

    def get_titles(self) -> dict[str, str]:
        titles = self.get_option("title")
        return titles

    def get_descriptions(self) -> dict[str, str]:
        descriptions = self.get_option("description")
        return descriptions

    def get_category_maps(self) -> dict[str, str]:
        category_maps = self.get_option("category")
        return category_maps

    def get_headers(self, type: str) -> list[str]:
        options = self.options
        q = f"type == '{type}'"
        headers = sorted(options.query(q)["name"].to_list())
        return headers

    def get_categorical_headers(self) -> list[str]:
        headers = self.get_headers("categorical")
        return headers

    def get_numerical_headers(self) -> list[str]:
        headers = self.get_headers("numerical")
        return headers

    def get_comment_headers(self) -> list[str]:
        headers = self.get_headers("comment")
        return headers

    def get_roundrobin_headers(self, columns: list):
        """
        総当たりしたいカラム名
        """
        import itertools

        # 総当たりしたいカラム名を整理
        # カラム名は基本的にデータフレームにあるものを与える
        # クロス集計しないことにしたカラムは除外する
        categorical_headers = self.categorical_headers
        headers = [h for h in sorted(columns) if h in categorical_headers]
        # 総当たりの組み合わせ
        matches = list(itertools.combinations(headers, 2))
        return matches

    def get_crosstab_headers(self, x: list[str], y: list[str]) -> list:
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

        categorical_headers = self.categorical_headers
        columns = [col for col in y if col in categorical_headers]
        headers = [[_x, _y] for _x, _y in itertools.product(x, columns) if _x != _y]
        return headers

    def show(self):
        """
        Print configuration
        """
        f = Path(self.load_from)
        config = self.load_config()
        q = config.get("questions")
        c = config.get("choices")

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

    def config(self):
        c = Config(load_from=self.load_from)
        return c.load_config()

    def read(self):
        c = Config(load_from=self.load_from)
        # categories = c.categorical()
        c.load()
        categories = c.categories
        data = pd.read_csv(self.read_from, parse_dates=["timestamp"])
        data = categorical_data(data, categories)
        return data

    @deprecated(version="0.5.0", reason="Moved to Config.get_roundrobin_headers.")
    def matches(self, columns: list):
        """
        総当たりしたいカラム名
        """
        import itertools

        # 総当たりしたいカラム名を整理
        # カラム名は基本的にデータフレームにあるものを与える
        # クロス集計しないことにしたカラムは除外する
        headers = [h for h in sorted(columns) if h in CATEGORICAL_HEADERS]
        # 総当たりの組み合わせ
        matches = list(itertools.combinations(headers, 2))
        return matches

    @deprecated(version="0.5.0", reason="Moved to Config.get_crosstab_headers.")
    def headers(self, x: list[str], y: list[str]) -> list:
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

        columns = [col for col in y if col in CATEGORICAL_HEADERS]
        return [[_x, _y] for _x, _y in itertools.product(x, columns) if _x != _y]


if __name__ == "__main__":
    logger.debug("Test config.py")

    settings = {"load_from": "../sandbox/config.toml"}
    c = Config(**settings)
    c.load()
    # logger.debug(c.load_from)
    logger.debug(c.categories.keys())
    logger.debug(c.options.columns)
    logger.debug(c.config.keys())
