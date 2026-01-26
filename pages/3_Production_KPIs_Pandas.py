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


# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Production KPIs with Pandas",
    layout="wide"
)

st.title("Production KPIs – Pandas Analysis")

st.write(
    "Diese Seite zeigt eine datenanalytische Auswertung eines "
    "synthetischen Produktionsdatensatzes. Fokus: KPI-Berechnung, "
    "Datenstruktur und klare Visualisierung."
)

st.write(
    "Hinweis: Die Daten sind synthetisch (KI-generiert) und dienen "
    "ausschließlich Demonstrationszwecken."
)

st.divider()


# --------------------------------------------------
# Load & prepare data
# --------------------------------------------------
df = load_production_data().copy()

df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

numeric_cols = [
    "Stueckzahl",
    "Ausschuss",
    "Stillstandszeit_Min",
    "Energieverbrauch_kWh",
    "Materialkosten",
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("Filter")

date_range = st.sidebar.date_input(
    "Zeitraum",
    (df["Datum"].min().date(), df["Datum"].max().date())
)

lines = sorted(df["Produktionslinie"].dropna().unique())
shifts = sorted(df["Schicht"].dropna().unique())

selected_lines = st.sidebar.multiselect(
    "Produktionslinie", lines, default=lines
)
selected_shifts = st.sidebar.multiselect(
    "Schicht", shifts, default=shifts
)

df_f = df[
    (df["Datum"] >= pd.to_datetime(date_range[0])) &
    (df["Datum"] <= pd.to_datetime(date_range[1])) &
    (df["Produktionslinie"].isin(selected_lines)) &
    (df["Schicht"].isin(selected_shifts))
].copy()


# --------------------------------------------------
# KPI: Gesamtkennzahlen
# --------------------------------------------------
st.header("Gesamtkennzahlen")

total_output = df_f["Stueckzahl"].sum()
total_scrap = df_f["Ausschuss"].sum()

kpi_total = pd.DataFrame({
    "Gesamtstückzahl": [total_output],
    "Gesamtausschuss": [total_scrap],
    "Ausschussquote (%)": [
        round(total_scrap / total_output * 100, 2) if total_output else 0
    ],
    "Gesamtstillstand (Min)": [df_f["Stillstandszeit_Min"].sum()],
    "Gesamtenergie (kWh)": [df_f["Energieverbrauch_kWh"].sum()],
    "Materialkosten gesamt": [df_f["Materialkosten"].sum()],
})

st.dataframe(kpi_total, use_container_width=True)

st.divider()


# ==================================================
# Chart 1: Ausschussquote nach Produktionslinie
# ==================================================
st.header("Ausschussquote nach Produktionslinie")

kpi_line = (
    df_f.groupby("Produktionslinie")
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
    )
    .reset_index()
)

kpi_line["Ausschussquote (%)"] = (
    kpi_line["Gesamtausschuss"]
    / kpi_line["Gesamtstückzahl"].replace(0, np.nan)
    * 100
).round(2)

st.dataframe(kpi_line, use_container_width=True)

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(
    kpi_line["Produktionslinie"],
    kpi_line["Ausschussquote (%)"],
    width=0.35
)

ax.set_ylim(4, 6)
ax.set_yticks(np.arange(4, 6.1, 0.2))
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Produktionslinie")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
st.pyplot(fig)

st.divider()


# ==================================================
# Chart 2: Nutzung vs Stillstand (100 %)
# ==================================================
st.header("Maschinennutzung und Stillstand nach Schicht")

kpi_shift = (
    df_f.groupby("Schicht")
    .agg(
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
    )
    .reset_index()
)

HOURS_PER_SHIFT = 8
kpi_shift["Stillstand_%"] = (
    kpi_shift["Stillstand_Min"] / (HOURS_PER_SHIFT * 60) * 100
).round(2)
kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_%"]).round(2)

st.dataframe(
    kpi_shift[["Schicht", "Nutzung_%", "Stillstand_%"]],
    use_container_width=True
)

fig, ax = plt.subplots(figsize=(6, 3))
x = np.arange(len(kpi_shift))
width = 0.35

ax.bar(x, kpi_shift["Nutzung_%"], width, label="Nutzung (%)")
ax.bar(
    x,
    kpi_shift["Stillstand_%"],
    width,
    bottom=kpi_shift["Nutzung_%"],
    label="Stillstand (%)"
)

ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_xticks(x)
ax.set_xticklabels(kpi_shift["Schicht"])
ax.set_ylabel("Anteil (%)")
ax.set_xlabel("Schicht")
ax.grid(axis="y", linestyle="--", alpha=0.4)

for i, row in kpi_shift.iterrows():
    ax.text(
        i,
        102,
        f"{row['Nutzung_%']}% / {row['Stillstand_%']}%",
        ha="center",
        fontsize=9
    )

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.15),
    ncol=2,
    frameon=False
)

plt.tight_layout()
st.pyplot(fig)

st.divider()


# ==================================================
# Chart 3: Zeitlicher Verlauf (monatlich)
# ==================================================
st.header("Zeitlicher Verlauf (monatlich)")

df_f["JahrMonat"] = df_f["Datum"].dt.to_period("M").astype(str)

trend = (
    df_f.groupby("JahrMonat")
    .agg(
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Ausschussquote=("Ausschuss", "sum"),
    )
    .reset_index()
)

trend["Ausschussquote (%)"] = (
    trend["Ausschussquote"]
    / trend["Gesamtstückzahl"].replace(0, np.nan)
    * 100
).round(2)

step = 6 if len(trend) > 24 else 3
xt = trend["JahrMonat"][::step]

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.set_ylabel("Stückzahl")
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.set_ylabel("Ausschussquote (%)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
st.pyplot(fig)

st.divider()


# ==================================================
# Chart 4: Energie pro Stück
# ==================================================
st.header("Energieverbrauch pro Stück")

energy = (
    df_f.groupby("Produktionslinie")
    .agg(
        Energie=("Energieverbrauch_kWh", "sum"),
        Menge=("Stueckzahl", "sum"),
    )
    .reset_index()
)

energy["kWh pro Stück"] = (
    energy["Energie"] / energy["Menge"].replace(0, np.nan)
).round(3)

st.dataframe(energy, use_container_width=True)

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(
    energy["Produktionslinie"],
    energy["kWh pro Stück"],
    width=0.35
)

ax.set_ylabel("kWh pro Stück")
ax.set_xlabel("Produktionslinie")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
st.pyplot(fig)

st.divider()

st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
