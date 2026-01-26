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
FIG_SMALL = (6.2, 3.2)
FIG_MED = (7.2, 3.4)
FIG_WIDE = (8.2, 3.6)

BAR_WIDTH = 0.35  # enger = kleiner Wert
GRID_ALPHA = 0.25

SHIFT_HOURS_DEFAULT = 8  # <-- wie du geschrieben hast: 8h pro Schicht


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
    "Schichtdauer (Stunden) – falls Betriebsstunden fehlen",
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

st.header("Datenüberblick")
st.write("Auszug der gefilterten Daten:")
st.dataframe(df_f.head(30), use_container_width=True)
st.divider()

# --------------------------------------------------
# KPI table: totals
# --------------------------------------------------
st.header("Gesamtkennzahlen")

total_output = float(df_f["Stueckzahl"].sum())
total_scrap = float(df_f["Ausschuss"].sum())
total_downtime_min = float(df_f["Stillstandszeit_Min"].sum())

kpi_total = pd.DataFrame(
    {
        "Gesamtstückzahl": [round(total_output, 0)],
        "Gesamtausschuss": [round(total_scrap, 0)],
        "Ausschussquote (%)": [round((total_scrap / total_output * 100) if total_output else 0.0, 2)],
        "Gesamtstillstand (Min)": [round(total_downtime_min, 0)],
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

st.dataframe(kpi_line.sort_values("Ausschussquote (%)", ascending=False), use_container_width=True)

fig, ax = plt.subplots(figsize=FIG_MED)
ax.bar(
    kpi_line["Produktionslinie"].astype(str),
    kpi_line["Ausschussquote (%)"],
    width=BAR_WIDTH
)
ax.set_ylim(4.0, 6.0)
ax.set_yticks(np.arange(4.0, 6.01, 0.1))
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=30)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 2: Utilization vs Downtime (100% stacked) by shift
# --------------------------------------------------
st.header("Maschinennutzung und Stillstand nach Schicht")

# Annahme: 1 Schicht = 8 Stunden
SHIFT_HOURS = 8

kpi_shift = (
    df_f.groupby("Schicht", dropna=False)
    .agg(
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Datensaetze=("Stillstandszeit_Min", "count")
    )
    .reset_index()
)

# Gesamtzeit in Minuten
kpi_shift["Gesamtzeit_Min"] = kpi_shift["Datensaetze"] * SHIFT_HOURS * 60

# Prozentwerte (sauber & logisch)
kpi_shift["Stillstand_%"] = (
    kpi_shift["Stillstand_Min"] / kpi_shift["Gesamtzeit_Min"] * 100
).round(1)

kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_%"]).round(1)

st.dataframe(
    kpi_shift[["Schicht", "Nutzung_%", "Stillstand_%"]],
    use_container_width=True
)

# ---------------- Diagramm ----------------
fig, ax = plt.subplots(figsize=(6, 3))  # klein & ruhig

x = np.arange(len(kpi_shift))
bar_width = 0.35

fig, ax = plt.subplots(figsize=(6, 3))  # klein & ruhig

x = np.arange(len(kpi_shift))
bar_width = 0.35

# Nutzung (grün, unten)
ax.bar(
    x,
    kpi_shift["Nutzung_%"],
    width=bar_width,
    color="#2ca02c",
    label="Nutzung (%)"
)

# Stillstand (rot, oben)
ax.bar(
    x,
    kpi_shift["Stillstand_%"],
    bottom=kpi_shift["Nutzung_%"],
    width=bar_width,
    color="#d62728",
    label="Stillstand (%)"
)

# Beschriftung ÜBER dem Balken (weißes Feld)
for i, row in kpi_shift.iterrows():
    ax.text(
        x[i],
        102,
        f"Nutzung {row['Nutzung_%']:.1f}%\nStillstand {row['Stillstand_%']:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

# Achsen & Gitter
ax.set_xticks(x)
ax.set_xticklabels(kpi_shift["Schicht"])
ax.set_ylabel("Anteil (%)")
ax.set_xlabel("Schicht")
ax.set_ylim(0, 110)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.legend(loc="upper center", ncol=2)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
st.pyplot(fig)


# Achsen & Gitter
ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_ylabel("Anteil (%)")

ax.set_xticks(x)
ax.set_xticklabels(kpi_shift["Schicht"])
ax.set_xlabel("Schicht")

ax.grid(axis="y", linestyle="--", alpha=0.4)

# Beschriftung UNTER dem Balken
for i, row in kpi_shift.iterrows():
    ax.text(
        i,
        -25,
        f"Nutzung {row['Nutzung_%']} %\nStillstand {row['Stillstand_%']} %",
        ha="center",
        va="top",
        fontsize=7
    )

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
    )
    .reset_index()
)

trend["Ausschussquote (%)"] = (
    trend["Gesamtausschuss"] / trend["Gesamtstückzahl"].replace(0, np.nan) * 100.0
).fillna(0).round(2)

st.dataframe(trend, use_container_width=True)

# weniger Labels, damit es sauber bleibt
step = 6 if len(trend) > 24 else 3 if len(trend) > 12 else 1
xt = trend["JahrMonat"][::step]

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
ax.set_ylabel("Gesamtstückzahl")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=30, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=30, ha="right")
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
    energy[["Produktionslinie", "kWh pro Stück"]].sort_values("kWh pro Stück", ascending=False),
    use_container_width=True
)

fig, ax = plt.subplots(figsize=FIG_MED)
ax.bar(energy["Produktionslinie"].astype(str), energy["kWh pro Stück"], width=BAR_WIDTH)
ax.set_ylabel("kWh pro Stück")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=30)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()
st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
