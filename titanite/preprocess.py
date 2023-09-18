from pathlib import Path

import pandas as pd
from loguru import logger


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
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

    logger.info("Start preprocessing data ...")
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["response"] = 1

    data = replace_data(data)
    data = split_data(data)
    data = cluster_data(data)
    data = binned_data(data)
    logger.info("... Finished !")

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
    logger.info("Replace")
    data["q03"] = data["q03"].replace(
        {
            "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
            "Oceania": "Oceania / Oceania",
        }
    )
    data["q04"] = data["q04"].replace(
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
    logger.info("Split")
    _q3 = data["q03"].str.split("/", expand=True)
    _q3[0] = _q3[0].str.strip()
    _q3[1] = _q3[1].str.strip()
    _q3 = _q3.rename(columns={0: "q03_regional", 1: "q03_subregional"})

    _q4 = data["q04"].str.split("/", expand=True)
    _q4[0] = _q4[0].str.strip()
    _q4[1] = _q4[1].str.strip()
    _q4 = _q4.rename(columns={0: "q04_regional", 1: "q04_subregional"})

    data = pd.concat([data, _q3], axis=1)
    data = pd.concat([data, _q4], axis=1)
    return data


def categorical_data(data: pd.DataFrame, categories: dict) -> pd.DataFrame:
    """
    カテゴリー型に変換する

    Parameters
    ----------
    data : pd.DataFrame
        データフレーム
    categories : dict
        カテゴリー型

    Returns
    -------
    pd.DataFrame
        データフレーム
    """
    logger.info("Categorize")

    # key: category_type
    convert_map = {
        "q01": "age",
        "q02": "gender",
        "q03": "geoscheme",
        "q03_regional": "regional",
        "q03_subregional": "subregional",
        "q04": "geoscheme",
        "q04_regional": "regional",
        "q04_subregional": "subregional",
        "q05": "job_title",
        "q06": "research_group",
        "q07": "research_field",
        "q08": "research_years",
        "q09": "yes_no",
        "q11": "yes_no",
        "q12_genderbalance": "good_poor",
        "q12_diversity": "good_poor",
        "q12_equity": "good_poor",
        "q12_inclusion": "good_poor",
        "q14": "good_poor",
        "q17_genderbalance": "agree_disagree",
        "q17_diversity": "agree_disagree",
        "q17_equity": "agree_disagree",
        "q17_inclusion": "agree_disagree",
        "q19": "school",
        "q01_clustered": "cluster",
        "q01q02_clustered": "cluster",
        "q13q14_clustered": "cluster",
    }

    for k, v in convert_map.items():
        c = categories.get(v, "category")
        data[k] = data[k].astype(c)

    data["q07"] = data["q07"].fillna("Others")
    data["q10"] = data["q10"].astype(int)
    data["q13"] = data["q13"].astype(int)
    # # data["q15"]
    # # data["q16"]
    # # data["q18"]
    # # data["q20"]
    # # data["q21"]
    # # data["q22"]

    return data


def sentiment_data(data):
    import numpy as np
    from textblob import TextBlob
    from tqdm import tqdm

    logger.info("Sentiment")

    def polarity(text):
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except TypeError as e:
            # logger.debug(e)
            return np.nan

    def subjectivity(text):
        try:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
        except TypeError as e:
            # logger.debug(e)
            return np.nan

    def translation(text):
        try:
            blob = TextBlob(text)
            return blob.translate(from_lang="en", to="ja")
        except TypeError as e:
            # logger.debug(e)
            return np.nan

    # やりたいこと
    # data["q15_polarity"] = data["q15"].apply(polarity)
    # data["q15_subjectivity"] = data["q15"].apply(subjectivity)

    # 自由記述の回答のカラム
    headers = ["q15", "q16", "q18", "q20", "q21", "q22"]

    tqdm.pandas()
    for header in headers:
        logger.info(f"Processing {header} ...")
        h = f"{header}_polarity"
        data[h] = data[header].progress_apply(polarity)
        h = f"{header}_subjectivity"
        data[h] = data[header].progress_apply(subjectivity)
        h = f"{header}_ja"
        data[h] = data[header].progress_apply(translation)
        logger.info(f"Processing {header} ... done !")

    return data


def cluster_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    クラスター分割

    Parameters
    ----------
    data : pd.DataFrame
        入力データ

    Returns
    -------
    pd.DataFrame
        クラスター分類を追加したデータ
    """
    logger.info("Clustered")
    # q01 cluster : 若手（40歳以下） / シニア
    header = "q01_clustered"
    data[header] = "Others"
    isT = data["q01"] < "40s"
    data.loc[isT, header] = "Cluster1"
    isT = data["q01"] >= "40s"
    data.loc[isT, header] = "Cluster2"

    # q13 cluster : 女性比率 20%以下 / 30%以上
    header = "q13_clustered"
    data[header] = "Others"
    isT = data["q13"] <= 20
    data.loc[isT, header] = "Cluster1"
    isT = data["q13"] >= 40
    data.loc[isT, header] = "Cluster2"

    # q01 x q02 cluster : 若手女性 / 若手男性
    header = "q01q02_clustered"
    data[header] = "Others"
    is_q01 = data["q01"] < "40s"
    is_q02 = data["q02"].isin(["Female"])
    isT = is_q01 & is_q02
    data.loc[isT, header] = "Cluster1"
    is_q01 = data["q01"] < "40s"
    is_q02 = data["q02"].isin(["Male"])
    isT = is_q01 & is_q02
    data.loc[isT, header] = "Cluster2"

    # q13 x q14 cluster : 20%以下・不満 / 30%以上・満足
    header = "q13q14_clustered"
    data[header] = "Others"
    is_q13 = data["q13"] < 25
    is_q14 = data["q14"].isin(["Very Poor", "Poor"])
    isT = is_q13 & is_q14
    data.loc[isT, header] = "Cluster1"
    is_q13 = data["q13"] > 25
    is_q14 = data["q14"].isin(["Very Good", "Good"])
    isT = is_q13 & is_q14
    data.loc[isT, header] = "Cluster2"

    return data


def binned_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    ビン分割


    Parameters
    ----------
    data : pd.DataFrame
        入力データ

    Returns
    -------
    pd.DataFrame
        ビン分割したカラムを追加したデータ
    """
    logger.info("Binned")
    data["q10_binned"] = pd.cut(
        data["q10"],
        [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25],
        labels=[
            "Prefer not to answer",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10+",
        ],
        right=False,
    )
    data["q13_binned"] = pd.cut(
        data["q13"],
        [
            -1,
            0,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            65,
            70,
            75,
            80,
            85,
            90,
            95,
            100,
            105,
        ],
        labels=[
            "Prefer not to answer",
            "0%",
            "10%",
            "15%",
            "20%",
            "25%",
            "30%",
            "35%",
            "40%",
            "45%",
            "50%",
            "55%",
            "60%",
            "65%",
            "70%",
            "75%",
            "80%",
            "85%",
            "90%",
            "95%",
            "100%",
        ],
        right=False,
    )
    return data


def save_data(data: pd.DataFrame, write_dir: str):
    logger.info("Save data")

    # Write only categorical data
    headers = [
        "timestamp",
        "q01",
        "q02",
        "q03",
        "q03_regional",
        "q03_subregional",
        "q04",
        "q04_regional",
        "q04_subregional",
        "q05",
        "q06",
        "q07",
        "q08",
        "q09",
        "q10",
        "q10_binned",
        "q11",
        "q12_genderbalance",
        "q12_diversity",
        "q12_equity",
        "q12_inclusion",
        "q13",
        "q13_binned",
        "q14",
        "q17_genderbalance",
        "q17_diversity",
        "q17_equity",
        "q17_inclusion",
        "q19",
    ]
    fname = Path(write_dir) / "categorical_data.csv"
    data[headers].to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")

    # Write only categorical data
    headers = [
        "timestamp",
        "q01",
        "q02",
        "q03",
        "q03_regional",
        "q03_subregional",
        "q04",
        "q04_regional",
        "q04_subregional",
        "q05",
        "q06",
        "q07",
        "q08",
        "q09",
        "q11",
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
    fname = Path(write_dir) / "sentiment_data.csv"
    data[headers].to_csv(fname, index=False)
    logger.info(f"Saved data to: {fname}")


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
