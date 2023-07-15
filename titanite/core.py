import pandas as pd
from loguru import logger


def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """
    データの前処理

    1. 各カラムを順番ありのカテゴリ変数に変換する
        - プロットを作成するときに、軸の値がアルファベット順で自動ソートされる
        - 順番ありにすることで、任意の並びにできる
    2. 自由記述あり／なしのカラムを追加する
        - 自由記述できるカラム名を指定し、入力がある／なしのフラグをたてる
        - 自由記述を埋める＝関心が高い、という傾向があると仮定し、その相関を調べたい
    3. 自由記述の内容を数値化したカラムを追加する
        - 自由記述の内容から、プラス／マイナスの感情を判断する
        - これも2と同じような仮定をしている
            - プラス感情 = 関心が高い = 好意的
            - マイナス感情 = 関心が高い = 嫌悪的
    """

    return pd.DataFrame()


if __name__ == "__main__":
    logger.debug("Test core.py")

    data = pd.read_csv("データ.csv")
    p = preprocess(data)
    logger.info(p)
