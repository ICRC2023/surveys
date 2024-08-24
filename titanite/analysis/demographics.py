from pydantic import BaseModel
import pandas as pd


class Data(BaseModel):
    pass
    # _data: pd.DataFrame
    # _grouped_data: pd.DataFrame

    def group_data(self, x: str):
        # x でグループ化してカウント数を計算する
        # | x | response |
        v = "response"
        copied = self._data.copy()
        grouped = copied.groupby(x)[v].count().reset_index()
        # countの合計を計算して、パーセンテージを計算する
        n = grouped[v].sum()
        grouped["percentage"] = grouped[v] / n
        return grouped

    def hbar(self, x: str, y: str, w: int, h: int):
        copied = self._grouped_data.copy()
        tips = list(copied.columns)

        y_max = data[y].max() + 20

        base = (
            alt.Chart(data)
            .encode(
                alt.X(x).axis(labelFontSize=15),
                alt.Y(y).axis(labelFontSize=15).scale(domain=[0, y_max]),
            )
            .properties(
                width=w,
                height=h,
            )
        )

        mark = base.mark_bar().encode(
            alt.Color(x),
            # alt.Color(x).scale(scheme="set1"),
            alt.Tooltip(tips),
        )

        text = base.mark_text(dy=-10, size=15).encode(alt.Text(y))

        return mark + text

    def pie(data: pd.DataFrame, x: str, y: str, w: int, h: int):
        tips = list(data.columns)

        base = (
            alt.Chart(data)
            .encode(
                alt.Theta(y).stack(True),
                alt.Color(x),
                alt.Order(y),
            )
            .properties(
                width=w,
                height=h,
            )
        )

        mark = base.mark_arc(outerRadius=120).encode(
            alt.Tooltip(tips),
        )

        text = base.mark_text(radius=150, size=15).encode(
            alt.Text(y).format(".1%"),
        )

        return mark + text

    def check(data: pd.DataFrame, x: str):
        w, h = 400, 400
        y = "response"
        grouped = group_data(data, x)
        b = hbar(grouped, x, y, w, h)
        y = "percentage"
        p = pie(grouped, x, y, w, h)
        return b | p
