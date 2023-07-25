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

    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["response"] = 1

    logger.info("Replace")
    data = replace_data(data)

    logger.info("Split")
    data = split_data(data)

    logger.info("Cluster")
    data = cluster_data(data)

    logger.info("Sentiment Analysis")
    data = sentiment_data(data)

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

    age = categories.get("age", "category")
    gender = categories.get("gender", "category")
    geoscheme = categories.get("geoscheme", "category")
    regional = categories.get("regional", "category")
    subregional = categories.get("subregional", "category")
    job_title = categories.get("job_title", "category")
    research_group = categories.get("research_group", "category")
    research_field = categories.get("research_field", "category")
    research_years = categories.get("research_years", "category")
    yes_no = categories.get("yes_no", "category")
    good_poor = categories.get("good_poor", "category")
    agree_disagree = categories.get("agree_disagree", "category")
    school = categories.get("school", "category")
    cluster = categories.get("cluster", "category")

    data["q01"] = data["q01"].astype(age)
    data["q02"] = data["q02"].astype(gender)
    data["q03"] = data["q03"].astype(geoscheme)
    data["q03_regional"] = data["q03_regional"].astype(regional)
    data["q03_subregional"] = data["q03_subregional"].astype(subregional)
    data["q04"] = data["q04"].astype(geoscheme)
    data["q04_regional"] = data["q04_regional"].astype(regional)
    data["q04_subregional"] = data["q04_subregional"].astype(subregional)
    data["q05"] = data["q05"].astype(job_title)
    data["q06"] = data["q06"].astype(research_group)
    data["q07"] = data["q07"].astype(research_field).fillna("Others")
    data["q08"] = data["q08"].astype(research_years)
    data["q09"] = data["q09"].astype(yes_no)
    data["q10"] = data["q10"].astype(int)
    data["q11"] = data["q11"].astype(yes_no)
    data["q12_genderbalance"] = data["q12_genderbalance"].astype(good_poor)
    data["q12_diversity"] = data["q12_diversity"].astype(good_poor)
    data["q12_equity"] = data["q12_equity"].astype(good_poor)
    data["q12_inclusion"] = data["q12_inclusion"].astype(good_poor)
    data["q13"] = data["q13"].astype(int)
    data["q14"] = data["q14"].astype(good_poor)
    # data["q15"]
    # data["q16"]
    data["q17_genderbalance"] = data["q17_genderbalance"].astype(agree_disagree)
    data["q17_diversity"] = data["q17_diversity"].astype(agree_disagree)
    data["q17_equity"] = data["q17_equity"].astype(agree_disagree)
    data["q17_inclusion"] = data["q17_inclusion"].astype(agree_disagree)
    # data["q18"]
    data["q19"] = data["q19"].astype(school)
    # data["q20"]
    # data["q21"]
    # data["q22"]

    # cluster
    data["q01_clustered"] = data["q01_clustered"].astype(cluster)
    data["q01q02_clustered"] = data["q01q02_clustered"].astype(cluster)
    data["q13q14_clustered"] = data["q13q14_clustered"].astype(cluster)

    data = binned_data(data)

    return data


def sentiment_data(data):
    import numpy as np
    from textblob import TextBlob
    from tqdm import tqdm

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
