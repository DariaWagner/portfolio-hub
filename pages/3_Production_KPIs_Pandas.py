import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

from services.data_loader import load_production_data


# --------------------------------------------------
# Page config (WICHTIG: muss vor anderen st.* Calls stehen)
# --------------------------------------------------
st.set_page_config(page_title="Production KPIs with Pandas", layout="wide")


# --------------------------------------------------
# Plot settings (kleiner + schmale Balken)
# --------------------------------------------------
BAR_WIDTH = 0.35
FIG_BAR = (6.2, 3.2)   # Balkendiagramme klein
FIG_LINE = (7.0, 3.2)  # Liniencharts klein
GRID_ALPHA = 0.35

SHIFT_HOURS = 8
SHIFT_MINUTES = SHIFT_HOURS * 60


def percent_fmt(x, _pos=None):
    return f"{x:.0f}%"


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
    "Datum", "Produktionslinie", "Schicht",
    "Stueckzahl", "Ausschuss", "Stillstandszeit_Min",
    "Energieverbrauch_kWh", "Materialkosten"
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

total_output = float(df_f["Stueckzahl"].sum())
total_scrap = float(df_f["Ausschuss"].sum())
total_downtime_min = float(df_f["Stillstandszeit_Min"].sum())
total_energy = float(df_f["Energieverbrauch_kWh"].sum())
total_material = float(df_f["Materialkosten"].sum())

scrap_rate_total = (total_scrap / total_output * 100) if total_output > 0 else 0.0

kpi_total = pd.DataFrame(
    {
        "Gesamtstückzahl": [int(total_output)],
        "Gesamtausschuss": [int(total_scrap)],
        "Ausschussquote (%)": [round(scrap_rate_total, 2)],
        "Gesamtstillstand (Min)": [int(total_downtime_min)],
        "Gesamtenergie (kWh)": [round(total_energy, 2)],
        "Gesamtkosten Material": [round(total_material, 2)],
    }
)

st.dataframe(kpi_total, use_container_width=True)
st.divider()


# --------------------------------------------------
# Chart 1: Scrap rate by line (y: 4..6, step 0.1)
# --------------------------------------------------
st.header("Ausschussquote nach Produktionslinie")

kpi_line = (
    df_f.groupby("Produktionslinie", dropna=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
        Energie_kWh=("Energieverbrauch_kWh", "sum"),
    )
    .reset_index()
)

kpi_line["Ausschussquote (%)"] = (
    kpi_line["Gesamtausschuss"]
    / kpi_line["Gesamtstückzahl"].replace(0, np.nan)
    * 100
).fillna(0).round(2)

st.dataframe(
    kpi_line.sort_values("Ausschussquote (%)", ascending=False),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=FIG_BAR)
ax.bar(
    kpi_line["Produktionslinie"].astype(str),
    kpi_line["Ausschussquote (%)"],
    width=BAR_WIDTH
)

ax.set_ylim(4.0, 6.0)
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.tick_params(axis="y", labelsize=9)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)

plt.tight_layout()
st.pyplot(fig)
st.divider()


# --------------------------------------------------
# Chart 2: Utilization vs Downtime by shift (100% stacked, green+red)
# Logic: verfügbare Zeit = Anzahl Datensätze * 8h
# --------------------------------------------------
st.header("Maschinennutzung und Stillstand nach Schicht")

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

kpi_shift["Verfuegbar_Min"] = kpi_shift["Records"] * SHIFT_MINUTES

kpi_shift["Stillstand_%"] = (
    kpi_shift["Stillstand_Min"] / kpi_shift["Verfuegbar_Min"].replace(0, np.nan) * 100
).fillna(0)

# clamp sauber (nur falls Daten komisch sind)
kpi_shift["Stillstand_%"] = kpi_shift["Stillstand_%"].clip(lower=0, upper=100)
kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_%"]).clip(lower=0, upper=100)

kpi_shift["Ausschussquote (%)"] = (
    kpi_shift["Gesamtausschuss"]
    / kpi_shift["Gesamtstückzahl"].replace(0, np.nan)
    * 100
).fillna(0).round(2)

# Für Tabelle runden
kpi_shift_view = kpi_shift.copy()
kpi_shift_view["Stillstand_h"] = (kpi_shift_view["Stillstand_Min"] / 60).round(2)
kpi_shift_view["Stillstand_%"] = kpi_shift_view["Stillstand_%"].round(2)
kpi_shift_view["Nutzung_%"] = kpi_shift_view["Nutzung_%"].round(2)

st.dataframe(
    kpi_shift_view[["Schicht", "Records", "Stillstand_h", "Stillstand_%", "Nutzung_%", "Ausschussquote (%)"]]
    .sort_values("Stillstand_%", ascending=False),
    use_container_width=True
)

# Plot
x = kpi_shift["Schicht"].astype(str).tolist()
use = kpi_shift["Nutzung_%"].to_numpy()
down = kpi_shift["Stillstand_%"].to_numpy()

fig, ax = plt.subplots(figsize=FIG_BAR)

# unten grün (Nutzung), oben rot (Stillstand)
bars_use = ax.bar(x, use, width=BAR_WIDTH, color="green", label="Nutzung (%)")
bars_down = ax.bar(x, down, width=BAR_WIDTH, bottom=use, color="red", label="Stillstand (%)")

ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
ax.yaxis.set_major_formatter(FuncFormatter(percent_fmt))
ax.set_ylabel("Anteil (%)")
ax.set_xlabel("Schicht")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)

# Legend über dem Plot (nicht auf den Balken)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

# Beschriftung ÜBER dem Balken (einmal pro Schicht)
for i, (u, d) in enumerate(zip(use, down)):
    ax.text(
        i, 102, f"N {u:.1f}% | S {d:.1f}%",
        ha="center", va="bottom", fontsize=9
    )

plt.tight_layout()
st.pyplot(fig)
st.divider()


# --------------------------------------------------
# Chart 3: Trend over time (monthly) - lesbare Monate
# --------------------------------------------------
st.header("Zeitlicher Verlauf (monatlich)")

df_t = df_f.dropna(subset=["Datum"]).copy()
df_t["JahrMonat"] = df_t["Datum"].dt.to_period("M").astype(str)

trend = (
    df_t.groupby("JahrMonat", dropna=False)
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
    )
    .reset_index()
)

trend["Ausschussquote (%)"] = (
    trend["Gesamtausschuss"] / trend["Gesamtstückzahl"].replace(0, np.nan) * 100
).fillna(0).round(2)

st.dataframe(trend, use_container_width=True)

step = 6 if len(trend) > 36 else 4 if len(trend) > 24 else 3 if len(trend) > 12 else 1
xt = trend["JahrMonat"][::step].tolist()

fig, ax = plt.subplots(figsize=FIG_LINE)
ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
ax.set_ylabel("Gesamtstückzahl")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right", fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=FIG_LINE)
ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right", fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()


# --------------------------------------------------
# Chart 4: Energy per unit by line
# --------------------------------------------------
st.header("Energieverbrauch pro Stück nach Produktionslinie")

energy = kpi_line[["Produktionslinie", "Energie_kWh", "Gesamtstückzahl"]].copy()
energy["kWh pro Stück"] = (
    energy["Energie_kWh"] / energy["Gesamtstückzahl"].replace(0, np.nan)
).fillna(0).round(3)

st.dataframe(
    energy[["Produktionslinie", "kWh pro Stück"]]
    .sort_values("kWh pro Stück", ascending=False),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=FIG_BAR)
ax.bar(
    energy["Produktionslinie"].astype(str),
    energy["kWh pro Stück"],
    width=BAR_WIDTH
)
ax.set_ylabel("kWh pro Stück")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.tick_params(axis="y", labelsize=9)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()
st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
