import pandas as pd
from loguru import logger


def preprocess_data(data: pd.DataFrame, category: dict) -> pd.DataFrame:
    """
    データの前処理

    1. タイムスタンプをdatetimeオブジェクトに変換する
    2. 回答数の集計に使うカラムを追加する



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

    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["response"] = 1
    data = replace_data(data)
    data = split_data(data)
    data = categorical_data(data, category)

    return data


def replace_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    いくつかのカラムの値を置換する

    アンケートの選択肢のままだと前処理が面倒な場合があります。
    そのような選択肢はこの関数で整えてください。

    Parameters
    ----------
    data : pd.DataFrame
        入力データフレーム

    Returns
    -------
    pd.DataFrame
        データフレーム
    """
    data["q3"] = data["q3"].replace(
        {
            "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
            "Oceania": "Oceania / Oceania",
        }
    )
    data["q4"] = data["q4"].replace(
        {
            "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
            "Oceania": "Oceania / Oceania",
        }
    )
    data["q14"] = data["q14"].replace({"No Interest": "No interest"})
    return data


def split_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    五大州／地域を分割して、新しいカラムとして追加する

    アンケートの勤務地／出身地の選択肢は"/"で区切って集計することも想定して作成しました。
    それぞれの質問の回答に、五大州（regional）と地域（subregional）のカラムを追加しています。

    Parameters
    ----------
    data : pd.DataFrame
        データフレーム

    Returns
    -------
    pd.DataFrame
        データフレーム
    """
    _q3 = data["q3"].str.split("/", expand=True)
    _q3[0] = _q3[0].str.strip()
    _q3[1] = _q3[1].str.strip()
    _q3 = _q3.rename(columns={0: "q3_regional", 1: "q3_subregional"})

    _q4 = data["q4"].str.split("/", expand=True)
    _q4[0] = _q4[0].str.strip()
    _q4[1] = _q4[1].str.strip()
    _q4 = _q4.rename(columns={0: "q4_regional", 1: "q4_subregional"})

    data = pd.concat([data, _q3], axis=1)
    data = pd.concat([data, _q4], axis=1)
    return data


def categorical_data(data: pd.DataFrame, category: dict) -> pd.DataFrame:
    """
    カテゴリー型に変換する

    Parameters
    ----------
    data : pd.DataFrame
        データフレーム
    category : dict
        カテゴリー型

    Returns
    -------
    pd.DataFrame
        データフレーム
    """
    data["q1"] = data["q1"].astype(category["age"])
    data["q2"] = data["q2"].astype(category["gender"])
    data["q3"] = data["q3"].astype(category["geoscheme"])
    data["q3_regional"] = data["q3_regional"].astype(category["regional"])
    data["q3_subregional"] = data["q3_subregional"].astype(category["subregional"])
    data["q4"] = data["q4"].astype(category["geoscheme"])
    data["q4_regional"] = data["q4_regional"].astype(category["regional"])
    data["q4_subregional"] = data["q4_subregional"].astype(category["subregional"])
    data["q5"] = data["q5"].astype(category["job_title"])
    data["q6"] = data["q6"].astype(category["research_group"])
    data["q7"] = data["q7"].astype(category["research_field"])
    data["q8"] = data["q8"].astype(category["research_years"])
    data["q9"] = data["q9"].astype(category["yes_no"])
    data["q10"] = data["q10"].astype(int)
    data["q11"] = data["q11"].astype(category["yes_no"])
    data["q12_genderbalance"] = data["q12_genderbalance"].astype(category["good_poor"])
    data["q12_diversity"] = data["q12_diversity"].astype(category["good_poor"])
    data["q12_equity"] = data["q12_equity"].astype(category["good_poor"])
    data["q12_inclusion"] = data["q12_inclusion"].astype(category["good_poor"])
    data["q13"] = data["q13"].astype(int)
    data["q14"] = data["q14"].astype(category["good_poor"])
    # data["q15"]
    # data["q16"]
    data["q17_genderbalance"] = data["q17_genderbalance"].astype(
        category["agree_disagree"]
    )
    data["q17_diversity"] = data["q17_diversity"].astype(category["agree_disagree"])
    data["q17_equity"] = data["q17_equity"].astype(category["agree_disagree"])
    data["q17_inclusion"] = data["q17_inclusion"].astype(category["agree_disagree"])
    # data["q18"]
    data["q19"] = data["q19"].astype(category["school"])
    # data["q20"]
    # data["q21"]
    # data["q22"]
    return data


def sentiment_data(data):
    from textblob import TextBlob

    # 自由記述の回答のカラム
    cols = ["q15", "q16", "q18", "q20", "q21", "q22"]

    for col in cols:
        responses = data[col].tolist()
        for response in responses:
            sentiment = TextBlob(response).sentiment.polarity
            print(f"Sentiment score: {sentiment}")

if __name__ == "__main__":
    logger.debug("Test core.py")

    import titanite as ti

    fname = "../sandbox/config.toml"
    config = ti.Config(fname=fname)
    config.load()
    category = config.categories()
    logger.debug(category)

    fname = "../data/test_data/20230715_icrc2023_diversity_presurvey_answers.csv"
    data = pd.read_csv(fname, skiprows=1)
    data = preprocess_data(data, category)
    logger.info(data)
