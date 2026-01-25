import streamlit as st
import pandas as pd

from services.data_loader import load_production_data

st.set_page_config(page_title="SQL Data Analysis", layout="wide")

st.title("SQL Data Analysis")

st.write(
    "Diese Seite zeigt eine SQL-nahe Analyse auf Basis eines normalisierten Datenmodells. "
    "Die Ergebnisse werden ausschließlich tabellarisch dargestellt."
)

st.write(
    "Data Disclaimer: Die verwendeten Daten sind synthetisch (KI-generiert) und simulieren "
    "reale industrielle Produktions- und Prozessdaten. Es werden keine echten Unternehmensdaten verwendet."
)

st.divider()

# --------------------------------------------------
# Load data via central loader
# --------------------------------------------------
df_raw = load_production_data().copy()

# --------------------------------------------------
# Minimal cleaning / typing
# --------------------------------------------------
if "Datum" in df_raw.columns:
    df_raw["Datum"] = pd.to_datetime(df_raw["Datum"], errors="coerce")

required_cols = [
    "Datum",
    "Unternehmen",
    "Produkt",
    "Modifikation",
    "Produktionslinie",
    "Schicht",
    "Auftragsnummer",
    "Status",
    "Fehlercode",
    "Stueckzahl",
    "Ausschuss",
    "Betriebsstunden",
    "Stillstandszeit_Min",
    "Materialkosten",
    "Energieverbrauch_kWh",
    "Mitarbeiter_Produktion",
    "Softwareversion",
    "Firmwareversion",
    "EndOfLine_Test",
    "MaxTemperatur",
    "Durchschnittstemperatur",
]

missing = [c for c in required_cols if c not in df_raw.columns]
if missing:
    st.error("Fehlende Spalten im CSV. Bitte prüfe die Spaltennamen.")
    st.write(missing)
    st.stop()

st.header("Relationales Datenmodell (logisch)")

st.write(
    "Der CSV-Datensatz wird logisch in atomare Dimensionstabellen und eine Faktentabelle aufgeteilt. "
    "Dimensionstabellen enthalten Stammdaten, die Faktentabelle enthält Messwerte und verweist über IDs."
)

# --------------------------------------------------
# Dimension tables
# --------------------------------------------------
dim_datum = (
    df_raw[["Datum"]]
    .dropna()
    .drop_duplicates()
    .sort_values("Datum")
    .reset_index(drop=True)
)
dim_datum["jahr"] = dim_datum["Datum"].dt.year
dim_datum["monat"] = dim_datum["Datum"].dt.month
dim_datum["datum_id"] = dim_datum.index + 1

dim_unternehmen = (
    df_raw[["Unternehmen"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_unternehmen["unternehmen_id"] = dim_unternehmen.index + 1

dim_produkt = (
    df_raw[["Produkt", "Modifikation"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_produkt["produkt_id"] = dim_produkt.index + 1

dim_linie = (
    df_raw[["Produktionslinie"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_linie["linie_id"] = dim_linie.index + 1

dim_schicht = (
    df_raw[["Schicht"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_schicht["schicht_id"] = dim_schicht.index + 1

dim_software = (
    df_raw[["Softwareversion", "Firmwareversion"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_software["software_id"] = dim_software.index + 1

dim_status = (
    df_raw[["Status", "Fehlercode"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_status["status_id"] = dim_status.index + 1

# --------------------------------------------------
# Fact table (IDs only + measures)
# --------------------------------------------------
fact = (
    df_raw.merge(dim_datum, on="Datum", how="left")
          .merge(dim_unternehmen, on="Unternehmen", how="left")
          .merge(dim_produkt, on=["Produkt", "Modifikation"], how="left")
          .merge(dim_linie, on="Produktionslinie", how="left")
          .merge(dim_schicht, on="Schicht", how="left")
          .merge(dim_software, on=["Softwareversion", "Firmwareversion"], how="left")
          .merge(dim_status, on=["Status", "Fehlercode"], how="left")
)

fact_produktion = fact[[
    "datum_id",
    "unternehmen_id",
    "produkt_id",
    "linie_id",
    "schicht_id",
    "software_id",
    "status_id",
    "Auftragsnummer",
    "Stueckzahl",
    "Ausschuss",
    "Betriebsstunden",
    "Stillstandszeit_Min",
    "Materialkosten",
    "Energieverbrauch_kWh",
    "Mitarbeiter_Produktion",
    "MaxTemperatur",
    "Durchschnittstemperatur",
    "EndOfLine_Test",
]].copy()

fact_produktion.insert(0, "produktion_id", range(1, len(fact_produktion) + 1))

# --------------------------------------------------
# Show tables
# --------------------------------------------------
st.subheader("Dimensionstabellen")

with st.expander("dim_datum"):
    st.dataframe(dim_datum, use_container_width=True)

with st.expander("dim_unternehmen"):
    st.dataframe(dim_unternehmen, use_container_width=True)

with st.expander("dim_produkt"):
    st.dataframe(dim_produkt, use_container_width=True)

with st.expander("dim_produktionslinie"):
    st.dataframe(dim_linie, use_container_width=True)

with st.expander("dim_schicht"):
    st.dataframe(dim_schicht, use_container_width=True)

with st.expander("dim_software"):
    st.dataframe(dim_software, use_container_width=True)

with st.expander("dim_status"):
    st.dataframe(dim_status, use_container_width=True)

st.subheader("Faktentabelle")
st.dataframe(fact_produktion.head(300), use_container_width=True)

st.divider()

# --------------------------------------------------
# KPI tables (SQL-like, tabular only)
# --------------------------------------------------
st.header("KPI-Ergebnisse (tabellarisch)")

# 1) Ausschussquote nach Linie
kpi_linie = (
    fact_produktion.merge(dim_linie, on="linie_id")
    .groupby("Produktionslinie", as_index=False)
    .agg(
        stueckzahl=("Stueckzahl", "sum"),
        ausschuss=("Ausschuss", "sum"),
        stillstand_min=("Stillstandszeit_Min", "sum"),
        energie_kwh=("Energieverbrauch_kWh", "sum"),
        materialkosten=("Materialkosten", "sum"),
    )
)
kpi_linie["ausschussquote_prozent"] = (
    kpi_linie["ausschuss"] * 100.0 / kpi_linie["stueckzahl"].replace(0, pd.NA)
).round(2)

st.subheader("KPIs nach Produktionslinie")
st.dataframe(kpi_linie.sort_values("ausschussquote_prozent", ascending=False), use_container_width=True)

# 2) KPIs nach Schicht
kpi_schicht = (
    fact_produktion.merge(dim_schicht, on="schicht_id")
    .groupby("Schicht", as_index=False)
    .agg(
        stueckzahl=("Stueckzahl", "sum"),
        ausschuss=("Ausschuss", "sum"),
        stillstand_min=("Stillstandszeit_Min", "sum"),
    )
)
kpi_schicht["ausschussquote_prozent"] = (
    kpi_schicht["ausschuss"] * 100.0 / kpi_schicht["stueckzahl"].replace(0, pd.NA)
).round(2)

st.subheader("KPIs nach Schicht")
st.dataframe(kpi_schicht.sort_values("ausschussquote_prozent", ascending=False), use_container_width=True)

# 3) Top Produkte nach Ausschussquote
kpi_produkt = (
    fact_produktion.merge(dim_produkt, on="produkt_id")
    .groupby(["Produkt", "Modifikation"], as_index=False)
    .agg(
        stueckzahl=("Stueckzahl", "sum"),
        ausschuss=("Ausschuss", "sum"),
    )
)
kpi_produkt["ausschussquote_prozent"] = (
    kpi_produkt["ausschuss"] * 100.0 / kpi_produkt["stueckzahl"].replace(0, pd.NA)
).round(2)

st.subheader("Top Produkte nach Ausschussquote")
st.dataframe(
    kpi_produkt.sort_values("ausschussquote_prozent", ascending=False).head(15),
    use_container_width=True
)

st.divider()

st.write("Repository: https://github.com/DariaWagner/sql-data-analysis")
