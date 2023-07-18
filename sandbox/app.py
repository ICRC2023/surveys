import altair as alt
import pandas as pd
import streamlit as st
from loguru import logger

import titanite as ti

logger.debug(f"Pandas {pd.__version__}")
logger.debug(f"Altair {alt.__version__}")
logger.debug(f"Streamlit {st.__version__}")
logger.debug(f"Pandas {ti.__version__}")



@st.cache_data
def load_data():
    f_cfg = "./config.toml"
    cfg = ti.Config(fname=f_cfg)
    cfg.load()
    category = cfg.categories()

    f_csv = "./tmp_preprocessed.csv"
    data = pd.read_csv(f_csv, parse_dates=["timestamp"])
    data = ti.categorical_data(data, category)
    return data

st.set_page_config(layout="wide")

data_load_state = st.text("Loading data ...")
data = load_data()
data_load_state.text("Loading data ... done!")


date_min = data["timestamp"].iat[0].date()
date_max = data["timestamp"].iat[-1].date()
st.text(date_min)
st.text(date_max)


st.title("ICRC2023 Diversity Pre-Surveys")
st.sidebar.title("Dashboard")
st.sidebar.markdown("Settings")

date_start, date_end = st.sidebar.slider(
    "period",
    min_value=date_min,
    max_value=date_max,
    value=(date_min, date_max)

)

st.sidebar.text(f"Start: {date_start}")
st.sidebar.text(f"End: {date_end}")


base = alt.Chart(data).properties(
    height=300,
    width=600,
    )

gender = base.mark_rect().encode(
    alt.X("yearmonthdate(timestamp)"),
    alt.Y("hours(timestamp)"),
    alt.Color("count()")
)

left_column, right_column = st.columns(2)
left_column.altair_chart(gender)