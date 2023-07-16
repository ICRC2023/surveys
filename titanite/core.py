import pandas as pd


def insight(data: pd.DataFrame, x: str, y: str, z: str = "response") -> pd.DataFrame:

    names = [x, y]
    grouped = data.groupby(names)[z].sum().reset_index()
    return grouped
