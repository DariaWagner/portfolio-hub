from __future__ import annotations

import pandas as pd
import streamlit as st


CSV_PATH = "data/produktionsdaten_premium_5Jahre.csv"


@st.cache_data(show_spinner=False)
def load_production_data() -> pd.DataFrame:
    """
    Lädt den Produktionsdatensatz aus dem Repository.
    Wird gecached, damit Streamlit schneller bleibt.
    """
    df = pd.read_csv(CSV_PATH)
    return df
