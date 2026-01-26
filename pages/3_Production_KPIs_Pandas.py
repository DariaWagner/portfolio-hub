import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from services.data_loader import load_production_data


# --------------------------------------------------
# Page config (muss ganz am Anfang stehen)
# --------------------------------------------------
st.set_page_config(page_title="Production KPIs with Pandas", layout="wide")


# --------------------------------------------------
# Style / Konstanten (einheitliche Charts)
# --------------------------------------------------
FIG_WIDE = (10, 4)
FIG_SMALL = (8, 4)

BAR_WIDTH_NARROW = 0.35
GRID_ALPHA = 0.35


# --------------------------------------------------
# Titel / Intro
# --------------------------------------------------
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
    "Datum",
    "Produktionslinie",
    "Schicht",
    "Produkt",
    "Modifikation",
    "Stueckzahl",
    "Ausschuss",
    "Stillstandszeit_Min",
    "Energieverbrauch_kWh",
    "Materialkosten",
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

start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

df_f = df[
    (df["Datum"] >= start_date)
    & (df["Datum"] <= end_date)
    & (df["Produktionslinie"].isin(selected_lines))
    & (df["Schicht"].isin(selected_shifts))
].copy()

if df_f.empty:
    st.warning("Keine Daten für die ausgewählten Filter gefunden.")
    st.stop()


# --------------------------------------------------
# Data preview
# --------------------------------------------------
st.header("Datenüberblick")
st.write("Auszug der gefilterten Daten:")
st.dataframe(df_f.head(50), use_container_width=True)
st.divider()


# --------------------------------------------------
# KPI table: totals
# --------------------------------------------------
st.header("Gesamtkennzahlen")

total_output = float(df_f["Stueckzahl"].sum())
total_scrap = float(df_f["Ausschuss"].sum())

kpi_total = pd.DataFrame(
    {
        "Gesamtstückzahl": [int(total_output)],
        "Gesamtausschuss": [int(total_scrap)],
        "Ausschussquote (%)": [round((total_scrap / total_output * 100) if total_output else 0.0, 2)],
        "Gesamtstillstand (Min)": [round(float(df_f["Stillstandszeit_Min"].sum()), 2)],
        "Gesamtenergie (kWh)": [round(float(df_f["Energieverbrauch_kWh"].sum()), 2)],
        "Gesamtkosten Material": [round(float(df_f["Materialkosten"].sum()), 2)],
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
    kpi_line["Gesamtausschuss"] / kpi_line["Gesamtstückzahl"].replace(0, np.nan) * 100
).fillna(0).round(2)

st.dataframe(
    kpi_line.sort_values("Ausschussquote (%)", ascending=False),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=FIG_SMALL)
ax.bar(
    kpi_line["Produktionslinie"].astype(str),
    kpi_line["Ausschussquote (%)"],
    width=BAR_WIDTH_NARROW,
)

# Fixe Achse + saubere Ticks (0.1 Schritte, aber lesbar)
ax.set_ylim(4, 6)
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=9)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)

plt.tight_layout()
st.pyplot(fig)

st.divider()


# --------------------------------------------------
# Chart 2: Utilization vs Downtime by shift (100% stacked)
# --------------------------------------------------
st.header("Maschinennutzung vs. Stillstand nach Schicht (8h-Schicht)")

kpi_shift = (
    df_f.groupby("Schicht", dropna=False)
    .agg(
        Records=("Schicht", "size"),
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
    )
    .reset_index()
)

# 8h pro Datensatz => geplante Minuten
kpi_shift["Geplant_Min"] = kpi_shift["Records"] * 8 * 60

# Stillstand in Stunden (für Tabelle)
kpi_shift["Stillstand_h"] = (kpi_shift["Stillstand_Min"] / 60).round(2)

# Anteil Stillstand/Nutzung in %
kpi_shift["Stillstand_Anteil_%"] = (
    kpi_shift["Stillstand_Min"] / kpi_shift["Geplant_Min"].replace(0, np.nan) * 100
).fillna(0).clip(0, 100).round(2)

kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_Anteil_%"]).round(2)

# Ausschussquote (für Tabelle)
kpi_shift["Ausschussquote (%)"] = (
    kpi_shift["Gesamtausschuss"] / kpi_shift["Gesamtstückzahl"].replace(0, np.nan) * 100
).fillna(0).round(2)

# Tabelle
show_cols = ["Schicht", "Records", "Geplant_Min", "Stillstand_h", "Stillstand_Anteil_%", "Nutzung_%", "Ausschussquote (%)"]
st.dataframe(
    kpi_shift[show_cols].sort_values("Stillstand_Anteil_%", ascending=False),
    use_container_width=True
)

# 100%-Stacked Balken: unten Nutzung (grün), oben Stillstand (rot)
fig, ax = plt.subplots(figsize=FIG_SMALL)

ax.bar(
    kpi_shift["Schicht"].astype(str),
    kpi_shift["Nutzung_%"],
    width=BAR_WIDTH_NARROW,
    color="#4CAF50",
    label="Nutzung (%)",
)

ax.bar(
    kpi_shift["Schicht"].astype(str),
    kpi_shift["Stillstand_Anteil_%"],
    bottom=kpi_shift["Nutzung_%"],
    width=BAR_WIDTH_NARROW,
    color="#E53935",
    label="Stillstand (%)",
)

ax.set_ylabel("Anteil (%)")
ax.set_xlabel("Schicht")
ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
ax.legend(loc="upper center", ncol=2, frameon=False)

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
    trend["Gesamtausschuss"] / trend["Gesamtstückzahl"].replace(0, np.nan) * 100
).fillna(0).round(2)

st.dataframe(trend, use_container_width=True)

# nur jeden n-ten Monat beschriften (lesbar)
step = 6 if len(trend) > 24 else 3 if len(trend) > 12 else 1
xt = trend["JahrMonat"][::step].tolist()

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
ax.set_ylabel("Gesamtstückzahl")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()


# --------------------------------------------------
# Chart 4: Energy per unit by line
# --------------------------------------------------
st.header("Energieverbrauch pro Stück nach Produktionslinie")

energy = kpi_line[["Produktionslinie", "Energie_kWh", "Gesamtstückzahl"]].copy()
energy["kWh pro Stück"] = (energy["Energie_kWh"] / energy["Gesamtstückzahl"].replace(0, np.nan)).fillna(0).round(3)

st.dataframe(
    energy[["Produktionslinie", "kWh pro Stück"]].sort_values("kWh pro Stück", ascending=False),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=FIG_SMALL)
ax.bar(
    energy["Produktionslinie"].astype(str),
    energy["kWh pro Stück"],
    width=BAR_WIDTH_NARROW,
)
ax.set_ylabel("kWh pro Stück")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()

st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
