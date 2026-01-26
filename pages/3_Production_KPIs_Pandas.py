import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from services.data_loader import load_production_data


# -----------------------------
# Global Chart Settings
# -----------------------------
FIG_SMALL = (8, 4)
FIG_MED = (8, 4.5)
FIG_WIDE = (10, 4.5)

BAR_WIDTH = 0.6
GRID_ALPHA = 0.3
SHIFT_HOURS_DEFAULT = 8

# Matplotlib Style
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9


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
    "Datum", "Produktionslinie", "Schicht",
    "Stueckzahl", "Ausschuss",
    "Stillstandszeit_Min", "Energieverbrauch_kWh", "Materialkosten",
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

shift_hours = st.sidebar.number_input(
    "Schichtdauer (Stunden)",
    min_value=1,
    max_value=24,
    value=SHIFT_HOURS_DEFAULT,
    step=1,
)

# Apply filters
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df_f = df[
    (df["Datum"] >= start_date) &
    (df["Datum"] <= end_date) &
    (df["Produktionslinie"].isin(selected_lines)) &
    (df["Schicht"].isin(selected_shifts))
].copy()

# --------------------------------------------------
# Datenüberblick
# --------------------------------------------------
st.header("📊 Datenüberblick")
with st.expander("Gefilterte Daten anzeigen", expanded=False):
    st.dataframe(df_f.head(30), use_container_width=True)
st.divider()

# --------------------------------------------------
# KPI table: totals
# --------------------------------------------------
st.header("📈 Gesamtkennzahlen")

total_output = float(df_f["Stueckzahl"].sum())
total_scrap = float(df_f["Ausschuss"].sum())
total_downtime_min = float(df_f["Stillstandszeit_Min"].sum())

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Gesamtstückzahl", f"{total_output:,.0f}")
with col2:
    st.metric("Gesamtausschuss", f"{total_scrap:,.0f}")
with col3:
    scrap_rate = (total_scrap / total_output * 100) if total_output else 0.0
    st.metric("Ausschussquote", f"{scrap_rate:.2f}%")
with col4:
    st.metric("Stillstand", f"{total_downtime_min:,.0f} Min")

col5, col6 = st.columns(2)
with col5:
    st.metric("Energieverbrauch", f"{df_f['Energieverbrauch_kWh'].sum():,.0f} kWh")
with col6:
    st.metric("Materialkosten", f"{df_f['Materialkosten'].sum():,.2f} €")

st.divider()

# --------------------------------------------------
# Chart 1: Scrap rate by line
# --------------------------------------------------
st.header("🔴 Ausschussquote nach Produktionslinie")

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

col1, col2 = st.columns([1, 1])

with col1:
    st.dataframe(
        kpi_line[["Produktionslinie", "Gesamtstückzahl", "Gesamtausschuss", "Ausschussquote (%)"]].sort_values("Ausschussquote (%)", ascending=False),
        use_container_width=True,
        hide_index=True
    )

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        kpi_line["Produktionslinie"].astype(str),
        kpi_line["Ausschussquote (%)"],
        width=BAR_WIDTH,
        color='#e74c3c'
    )
    
    # Werte über Balken
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_ylabel("Ausschussquote (%)")
    ax.set_xlabel("Produktionslinie")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# --------------------------------------------------
# Chart 2: Utilization vs Downtime by shift
# --------------------------------------------------
st.header("⚙️ Maschinennutzung und Stillstand nach Schicht")

kpi_shift = (
    df_f.groupby("Schicht", dropna=False)
    .agg(
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Datensaetze=("Stillstandszeit_Min", "count")
    )
    .reset_index()
)

kpi_shift["Gesamtzeit_Min"] = kpi_shift["Datensaetze"] * shift_hours * 60
kpi_shift["Stillstand_%"] = (kpi_shift["Stillstand_Min"] / kpi_shift["Gesamtzeit_Min"] * 100).round(1)
kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_%"]).round(1)

col1, col2 = st.columns([1, 1])

with col1:
    st.dataframe(
        kpi_shift[["Schicht", "Nutzung_%", "Stillstand_%"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x = np.arange(len(kpi_shift))
    width = 0.5
    
    # Nutzung (grün)
    p1 = ax.bar(x, kpi_shift["Nutzung_%"], width, label='Nutzung', color='#2ecc71')
    # Stillstand (rot, gestapelt)
    p2 = ax.bar(x, kpi_shift["Stillstand_%"], width, bottom=kpi_shift["Nutzung_%"], label='Stillstand', color='#e74c3c')
    
    ax.set_ylabel("Anteil (%)")
    ax.set_xlabel("Schicht")
    ax.set_xticks(x)
    ax.set_xticklabels(kpi_shift["Schicht"])
    ax.set_ylim(0, 105)
    ax.legend(loc='upper right')
    ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
    
    # Beschriftungen
    for i, row in kpi_shift.iterrows():
        ax.text(i, 50, f"{row['Nutzung_%']:.1f}%\n{row['Stillstand_%']:.1f}%",
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# --------------------------------------------------
# Chart 3: Trend over time (monthly)
# --------------------------------------------------
st.header("📅 Zeitlicher Verlauf (monatlich)")

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
    trend["Gesamtausschuss"] / trend["Gesamtstückzahl"].replace(0, np.nan) * 100.0
).fillna(0).round(2)

with st.expander("Monatliche Daten anzeigen", expanded=False):
    st.dataframe(trend, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=FIG_SMALL)
    ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"], marker='o', markersize=4, linewidth=2, color='#3498db')
    ax.set_ylabel("Gesamtstückzahl")
    ax.set_xlabel("Monat")
    
    step = max(1, len(trend) // 10)
    ax.set_xticks(trend["JahrMonat"][::step])
    ax.set_xticklabels(trend["JahrMonat"][::step], rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=FIG_SMALL)
    ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"], marker='o', markersize=4, linewidth=2, color='#e74c3c')
    ax.set_ylabel("Ausschussquote (%)")
    ax.set_xlabel("Monat")
    
    step = max(1, len(trend) // 10)
    ax.set_xticks(trend["JahrMonat"][::step])
    ax.set_xticklabels(trend["JahrMonat"][::step], rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# --------------------------------------------------
# Chart 4: Energy per unit by line
# --------------------------------------------------
st.header("⚡ Energieverbrauch pro Stück nach Produktionslinie")

energy = kpi_line[["Produktionslinie", "Energie_kWh", "Gesamtstückzahl"]].copy()
energy["kWh pro Stück"] = (
    energy["Energie_kWh"] / energy["Gesamtstückzahl"].replace(0, np.nan)
).fillna(0).round(3)

col1, col2 = st.columns([1, 1])

with col1:
    st.dataframe(
        energy[["Produktionslinie", "kWh pro Stück"]].sort_values("kWh pro Stück", ascending=False),
        use_container_width=True,
        hide_index=True
    )

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(energy["Produktionslinie"].astype(str), energy["kWh pro Stück"], 
                   width=BAR_WIDTH, color='#f39c12')
    
    # Werte über Balken
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_ylabel("kWh pro Stück")
    ax.set_xlabel("Produktionslinie")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()
st.markdown("---")
st.markdown("**Repository:** [github.com/DariaWagner/production-kpis-pandas](https://github.com/DariaWagner/production-kpis-pandas)")