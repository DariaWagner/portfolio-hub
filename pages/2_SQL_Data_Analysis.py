import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="SQL Data Analysis",
    layout="wide"
)

st.title("SQL Data Analysis")

st.write(
    "Diese Seite zeigt SQL-nahe, relationale Analysen "
    "auf Basis eines normalisierten Produktionsdatenmodells."
)

st.write(
    "Die verwendeten Daten sind synthetisch (KI-generiert) "
    "und simulieren reale industrielle Produktions- und Prozessdaten. "
    "Es werden keine echten Unternehmensdaten verwendet."
)

st.divider()

# --------------------------------------------------
# Data loading
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/produktionsdaten_premium_5Jahre.csv")

df = load_data()

# --------------------------------------------------
# Relationales Datenmodell (logisch)
# --------------------------------------------------
st.header("Relationales Datenmodell (logisch)")

st.write(
    "Der ursprüngliche CSV-Datensatz wird logisch in mehrere "
    "relationale Tabellen aufgeteilt. Jede Tabelle besitzt "
    "eine eindeutige ID und eine klare fachliche Bedeutung."
)

# Dimension: Datum
dim_datum = (
    df[["Datum"]]
    .drop_duplicates()
    .assign(
        Jahr=lambda x: pd.to_datetime(x["Datum"]).dt.year,
        Monat=lambda x: pd.to_datetime(x["Datum"]).dt.month
    )
    .reset_index(drop=True)
)
dim_datum["datum_id"] = dim_datum.index + 1

# Dimension: Produktionslinie
dim_linie = (
    df[["Produktionslinie"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_linie["linie_id"] = dim_linie.index + 1

# Dimension: Schicht
dim_schicht = (
    df[["Schicht"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_schicht["schicht_id"] = dim_schicht.index + 1

# Fact-Tabelle
fact = df.merge(dim_datum, on="Datum") \
         .merge(dim_linie, on="Produktionslinie") \
         .merge(dim_schicht, on="Schicht")

fact_produktion = fact[[
    "datum_id",
    "linie_id",
    "schicht_id",
    "Stueckzahl",
    "Ausschuss",
    "Stillstandszeit_Min",
    "Energieverbrauch_kWh"
]]

# --------------------------------------------------
# Tabellen anzeigen
# --------------------------------------------------
st.subheader("Dimension: Datum")
st.dataframe(dim_datum, use_container_width=True)

st.subheader("Dimension: Produktionslinie")
st.dataframe(dim_linie, use_container_width=True)

st.subheader("Dimension: Schicht")
st.dataframe(dim_schicht, use_container_width=True)

st.subheader("Fact: Produktion")
st.dataframe(fact_produktion.head(50), use_container_width=True)

st.divider()

# --------------------------------------------------
# KPI 1 – Gesamtproduktion
# --------------------------------------------------
st.header("KPI: Gesamtproduktion & Ausschussquote")

kpi_gesamt = pd.DataFrame({
    "Gesamtstückzahl": [fact_produktion["Stueckzahl"].sum()],
    "Gesamtausschuss": [fact_produktion["Ausschuss"].sum()],
})

kpi_gesamt["Ausschussquote (%)"] = (
    kpi_gesamt["Gesamtausschuss"]
    / kpi_gesamt["Gesamtstückzahl"] * 100
).round(2)

st.dataframe(kpi_gesamt, use_container_width=True)

# --------------------------------------------------
# KPI 2 – Nach Produktionslinie
# --------------------------------------------------
st.header("KPI: Produktion nach Produktionslinie")

kpi_linie = (
    fact_produktion
    .merge(dim_linie, on="linie_id")
    .groupby("Produktionslinie", as_index=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum")
    )
)

kpi_linie["Ausschussquote (%)"] = (
    kpi_linie["Gesamtausschuss"]
    / kpi_linie["Gesamtstückzahl"] * 100
).round(2)

st.dataframe(kpi_linie, use_container_width=True)

# --------------------------------------------------
# KPI 3 – Nach Schicht
# --------------------------------------------------
st.header("KPI: Produktion nach Schicht")

kpi_schicht = (
    fact_produktion
    .merge(dim_schicht, on="schicht_id")
    .groupby("Schicht", as_index=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum")
    )
)

kpi_schicht["Ausschussquote (%)"] = (
    kpi_schicht["Gesamtausschuss"]
    / kpi_schicht["Gesamtstückzahl"] * 100
).round(2)

st.dataframe(kpi_schicht, use_container_width=True)

# --------------------------------------------------
# KPI 4 – Energie pro Stück
# --------------------------------------------------
st.header("KPI: Energieverbrauch pro Stück")

kpi_energie = (
    fact_produktion
    .merge(dim_linie, on="linie_id")
    .groupby("Produktionslinie", as_index=False)
    .agg(
        Energie_kWh=("Energieverbrauch_kWh", "sum"),
        Stueckzahl=("Stueckzahl", "sum")
    )
)

kpi_energie["kWh pro Stück"] = (
    kpi_energie["Energie_kWh"]
    / kpi_energie["Stueckzahl"]
).round(2)

st.dataframe(kpi_energie[["Produktionslinie", "kWh pro Stück"]], use_container_width=True)

st.divider()

st.write(
    "Diese Tabellen entsprechen fachlich den SQL-Queries "
    "im zugehörigen GitHub-Repository."
)
