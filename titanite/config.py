import tomllib
from pathlib import Path

from loguru import logger
from pydantic import BaseModel


class Config(BaseModel):
    fname: str = "config.toml"
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


if __name__ == "__main__":
    settings = {"confd": "../sandbox/", "fname": "config.toml"}

    c = Config(**settings)
    c.load()
    logger.debug(c.fname)
    logger.debug(c.get("questions").keys())
    logger.debug(c.get("choices").keys())
