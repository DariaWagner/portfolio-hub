import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_production_data() -> pd.DataFrame:
    """
    Lädt den Produktionsdatensatz aus dem data-Ordner.
    Wird von allen Streamlit-Pages verwendet.
    """

    base_path = Path(__file__).resolve().parent.parent
    data_path = base_path / "data" / "produktionsdaten_premium_5Jahre.csv"

    df = pd.read_csv(data_path)

    # Datum korrekt parsen
    df["Datum"] = pd.to_datetime(df["Datum"])

    return df
