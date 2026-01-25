from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "produktionsdaten_premium_5Jahre.csv"

@st.cache_data
def load_data(uploaded_file=None) -> pd.DataFrame:
    """
    Loads the production CSV either from upload or from repo /data.
    Performs minimal parsing & column normalization.
    """
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(DATA_PATH)

    # Parse date if available
    if "Datum" in df.columns:
        df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

    # Normalize common columns if present (no renaming here except safe)
    # Keep original German column names as they are in your CSV.
    return df
