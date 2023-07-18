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


st.title("ICRC2023 Diversity Pre-Surveys")
data_load_state = st.text("Loading data ...")
data = load_data()
data_load_state.text("Loading data ... done!")

st.subheader("Raw data")
st.write(data)