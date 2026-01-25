import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from services.data_loader import load_production_data

df = load_production_data()

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Production KPIs with Pandas", layout="wide")

st.title("Production KPIs – Pandas Analysis")

st.write(
    "Diese Seite zeigt eine datenanalytische Auswertung des Produktionsdatensatzes mit Python und pandas. "
    "Der Fokus liegt auf Datenaufbereitung, KPI-Berechnung und Visualisierung mit matplotlib."
)

st.write(
    "Data Disclaimer: Die verwendeten Daten sind synthetisch (KI-generiert) und simulieren reale industrielle "
    "Produktions- und Prozessdaten. Es werden keine echten Unternehmensdaten verwendet."
)

st.divider()

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = load_production_data().copy()

# --------------------------------------------------
# Basic cleaning / typing
# --------------------------------------------------
if "Datum" in df.columns:
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

numeric_cols = [
    "Stueckzahl",
    "Ausschuss",
    "Betriebsstunden",
    "Stillstandszeit_Min",
    "Materialkosten",
    "Energieverbrauch_kWh",
    "Mitarbeiter_Produktion",
    "MaxTemperatur",
    "Durchschnittstemperatur",
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

required_cols = [
    "Datum", "Produktionslinie", "Schicht", "Produkt", "Modifikation",
    "Stueckzahl", "Ausschuss", "Stillstandszeit_Min", "Energieverbrauch_kWh", "Materialkosten"
]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error("Fehlende Spalten im Datensatz. Bitte prüfe CSV/Loader.")
    st.write(missing)
    st.stop()

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("Filter")

min_date = df["Datum"].min()
max_date = df["Datum"].max()

date_range = st.sidebar.date_input(
    "Zeitraum",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

lines = sorted(df["Produktionslinie"].dropna().unique().tolist())
selected_lines = st.sidebar.multiselect("Produktionslinie", options=lines, default=lines)

shifts = sorted(df["Schicht"].dropna().unique().tolist())
selected_shifts = st.sidebar.multiselect("Schicht", options=shifts, default=shifts)

# Apply filters
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df_f = df[
    (df["Datum"] >= start_date) &
    (df["Datum"] <= end_date) &
    (df["Produktionslinie"].isin(selected_lines)) &
    (df["Schicht"].isin(selected_shifts))
].copy()

st.header("Datenüberblick")

st.write("Auszug der gefilterten Daten:")
st.dataframe(df_f.head(50), use_container_width=True)

st.divider()

# --------------------------------------------------
# KPI table: totals
# --------------------------------------------------
st.header("Gesamtkennzahlen")

total_output = df_f["Stueckzahl"].sum()
total_scrap = df_f["Ausschuss"].sum()

kpi_total = pd.DataFrame(
    {
        "Gesamtstückzahl": [total_output],
        "Gesamtausschuss": [total_scrap],
        "Ausschussquote (%)": [round((total_scrap / total_output * 100) if total_output else 0.0, 2)],
        "Gesamtstillstand (Min)": [df_f["Stillstandszeit_Min"].sum()],
        "Gesamtenergie (kWh)": [df_f["Energieverbrauch_kWh"].sum()],
        "Gesamtkosten Material": [df_f["Materialkosten"].sum()],
    }
)

st.dataframe(kpi_total, use_container_width=True)

st.divider()

# --------------------------------------------------
# Chart 1: Scrap rate by line
# --------------------------------------------------
st.header("Ausschussquote nach Produktionslinie")

kpi_line = (
    df_f.groupby("Produktionslinie", dropna=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Energie_kWh=("Energieverbrauch_kWh", "sum"),
        Materialkosten=("Materialkosten", "sum"),
    )
    .reset_index()
)

kpi_line["Ausschussquote (%)"] = (
    (kpi_line["Gesamtausschuss"] / kpi_line["Gesamtstückzahl"]) * 100
).replace([pd.NA, float("inf")], pd.NA).fillna(0).round(2)

st.dataframe(kpi_line.sort_values("Ausschussquote (%)", ascending=False), use_container_width=True)

fig = plt.figure()
plt.bar(kpi_line["Produktionslinie"].astype(str), kpi_line["Ausschussquote (%)"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Ausschussquote (%)")
plt.xlabel("Produktionslinie")
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 2: Downtime by shift
# --------------------------------------------------
st.header("Stillstandszeit nach Schicht")

kpi_shift = (
    df_f.groupby("Schicht", dropna=False)
    .agg(
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
    )
    .reset_index()
)

kpi_shift["Ausschussquote (%)"] = (
    (kpi_shift["Gesamtausschuss"] / kpi_shift["Gesamtstückzahl"]) * 100
).replace([pd.NA, float("inf")], pd.NA).fillna(0).round(2)

st.dataframe(kpi_shift.sort_values("Stillstand_Min", ascending=False), use_container_width=True)

fig = plt.figure()
plt.bar(kpi_shift["Schicht"].astype(str), kpi_shift["Stillstand_Min"])
plt.ylabel("Stillstand (Minuten)")
plt.xlabel("Schicht")
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 3: Trend over time (monthly)
# --------------------------------------------------
st.header("Zeitlicher Verlauf (monatlich)")

df_t = df_f.dropna(subset=["Datum"]).copy()
df_t["JahrMonat"] = df_t["Datum"].dt.to_period("M").astype(str)

trend = (
    df_t.groupby("JahrMonat", dropna=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
    )
    .reset_index()
)

trend["Ausschussquote (%)"] = (
    (trend["Gesamtausschuss"] / trend["Gesamtstückzahl"]) * 100
).replace([pd.NA, float("inf")], pd.NA).fillna(0).round(2)

st.dataframe(trend, use_container_width=True)

fig = plt.figure()
plt.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Gesamtstückzahl")
plt.xlabel("Monat")
plt.tight_layout()
st.pyplot(fig)

fig = plt.figure()
plt.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Ausschussquote (%)")
plt.xlabel("Monat")
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 4: Energy per unit by line
# --------------------------------------------------
st.header("Energieverbrauch pro Stück nach Produktionslinie")

energy = kpi_line[["Produktionslinie", "Energie_kWh", "Gesamtstückzahl"]].copy()
energy["kWh pro Stück"] = (energy["Energie_kWh"] / energy["Gesamtstückzahl"]).replace(
    [pd.NA, float("inf")], pd.NA
).fillna(0).round(3)

st.dataframe(energy[["Produktionslinie", "kWh pro Stück"]].sort_values("kWh pro Stück", ascending=False),
             use_container_width=True)

fig = plt.figure()
plt.bar(energy["Produktionslinie"].astype(str), energy["kWh pro Stück"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("kWh pro Stück")
plt.xlabel("Produktionslinie")
plt.tight_layout()
st.pyplot(fig)

st.divider()

st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
