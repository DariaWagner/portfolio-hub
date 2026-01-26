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
# Page config (MUSS ganz oben vor allen st.* Calls stehen!)
# --------------------------------------------------
st.set_page_config(page_title="Production KPIs with Pandas", layout="wide")

# --------------------------------------------------
# Plot settings (einheitlich)
# --------------------------------------------------
FIG_WIDE = (10, 4)
FIG_TREND = (12, 4)
BAR_WIDTH = 0.45
GRID_ALPHA = 0.30

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

# Apply filters
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df_f = df[
    (df["Datum"] >= start_date)
    & (df["Datum"] <= end_date)
    & (df["Produktionslinie"].isin(selected_lines))
    & (df["Schicht"].isin(selected_shifts))
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
total_downtime_h = total_downtime_min / 60.0

# Maschinen-Nutzungslogik:
# Wir nehmen "Betriebsstunden" wenn vorhanden, sonst approximieren wir verfügbare Zeit aus Zeitraum.
has_operating_hours = "Betriebsstunden" in df_f.columns and df_f["Betriebsstunden"].notna().any()

if has_operating_hours:
    operating_h = float(df_f["Betriebsstunden"].fillna(0).sum())
    planned_h = operating_h + total_downtime_h
else:
    # Fallback: geplante Zeit = Tage im Zeitraum * 24h * Anzahl ausgewählter Linien (sehr grobe Annäherung)
    days = max(1, (end_date.date() - start_date.date()).days + 1)
    planned_h = float(days * 24 * max(1, len(selected_lines)))
    operating_h = max(0.0, planned_h - total_downtime_h)

utilization_pct = (operating_h / planned_h * 100) if planned_h > 0 else 0.0
downtime_share_pct = (total_downtime_h / planned_h * 100) if planned_h > 0 else 0.0

kpi_total = pd.DataFrame(
    {
        "Gesamtstückzahl": [round(total_output, 0)],
        "Gesamtausschuss": [round(total_scrap, 0)],
        "Ausschussquote (%)": [round((total_scrap / total_output * 100) if total_output else 0.0, 2)],
        "Stillstand (h)": [round(total_downtime_h, 2)],
        "Stillstand-Anteil (%)": [round(downtime_share_pct, 2)],
        "Maschinen-Nutzung (%)": [round(utilization_pct, 2)],
        "Gesamtenergie (kWh)": [round(float(df_f["Energieverbrauch_kWh"].sum()), 2)],
        "Gesamtkosten Material": [round(float(df_f["Materialkosten"].sum()), 2)],
    }
)

st.dataframe(kpi_total, use_container_width=True)

if not has_operating_hours:
    st.info(
        "Hinweis: 'Maschinen-Nutzung (%)' wird hier grob aus Zeitraum*24h*Linien approximiert, "
        "weil keine Spalte 'Betriebsstunden' vorhanden/gefüllt ist."
    )

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

# Dynamische Y-Achse: rund um die Werte, aber max 0–6 wenn sinnvoll
min_y = max(0.0, float(kpi_line["Ausschussquote (%)"].min()) - 0.3)
max_y = float(kpi_line["Ausschussquote (%)"].max()) + 0.3
min_y = np.floor(min_y * 10) / 10
max_y = np.ceil(max_y * 10) / 10

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.bar(
    kpi_line["Produktionslinie"].astype(str),
    kpi_line["Ausschussquote (%)"],
    width=BAR_WIDTH,
)

ax.set_ylim(min_y, max_y)
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)

plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 2: Downtime + Utilization by shift (Anteile in %)
# --------------------------------------------------
st.header("Stillstand & Maschinen-Nutzung nach Schicht")

kpi_shift = (
    df_f.groupby("Schicht", dropna=False)
    .agg(
        Stillstand_Min=("Stillstandszeit_Min", "sum"),
        Gesamtstückzahl=("Stueckzahl", "sum"),
        Gesamtausschuss=("Ausschuss", "sum"),
        Betriebsstunden=("Betriebsstunden", "sum") if "Betriebsstunden" in df_f.columns else ("Stillstandszeit_Min", "size"),
    )
    .reset_index()
)

# Minuten -> Stunden
kpi_shift["Stillstand_h"] = (kpi_shift["Stillstand_Min"] / 60).fillna(0)

# Nutzungsanteil: wenn Betriebsstunden da sind -> Anteil bezogen auf (Betriebsstunden + Stillstand)
if "Betriebsstunden" in df_f.columns:
    kpi_shift["Betriebs_h"] = pd.to_numeric(kpi_shift["Betriebsstunden"], errors="coerce").fillna(0)
    kpi_shift["Geplant_h"] = (kpi_shift["Betriebs_h"] + kpi_shift["Stillstand_h"]).replace(0, np.nan)
    kpi_shift["Stillstand_Anteil_%"] = (kpi_shift["Stillstand_h"] / kpi_shift["Geplant_h"] * 100).fillna(0).round(2)
    kpi_shift["Nutzung_%"] = (kpi_shift["Betriebs_h"] / kpi_shift["Geplant_h"] * 100).fillna(0).round(2)
else:
    # Fallback: pro Schicht geplante Zeit approximieren: Zeitraum*8h*Linien
    days = max(1, (end_date.date() - start_date.date()).days + 1)
    planned_h_shift = float(days * 8 * max(1, len(selected_lines)))
    kpi_shift["Geplant_h"] = planned_h_shift
    kpi_shift["Stillstand_Anteil_%"] = (kpi_shift["Stillstand_h"] / planned_h_shift * 100).fillna(0).round(2)
    kpi_shift["Nutzung_%"] = (100 - kpi_shift["Stillstand_Anteil_%"]).clip(lower=0).round(2)

kpi_shift["Ausschussquote (%)"] = (
    kpi_shift["Gesamtausschuss"] / kpi_shift["Gesamtstückzahl"].replace(0, np.nan) * 100
).fillna(0).round(2)

st.dataframe(
    kpi_shift.sort_values("Stillstand_Anteil_%", ascending=False)[
        ["Schicht", "Stillstand_h", "Stillstand_Anteil_%", "Nutzung_%", "Ausschussquote (%)"]
    ],
    use_container_width=True,
)

# Balkendiagramm: Stillstand-Anteil (%)
fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.bar(
    kpi_shift["Schicht"].astype(str),
    kpi_shift["Stillstand_Anteil_%"],
    width=BAR_WIDTH,
)

ax.set_ylabel("Stillstand-Anteil (%)")
ax.set_xlabel("Schicht")
ax.set_ylim(0, max(5, float(kpi_shift["Stillstand_Anteil_%"].max()) * 1.2))
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)

plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 3: Trend over time (monthly) - cleaner x labels + consistent size
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

trend["Stillstand_h"] = (trend["Stillstand_Min"] / 60).fillna(0).round(2)

st.dataframe(trend, use_container_width=True)

# X-Achse lesbar
step = 6 if len(trend) > 24 else 3 if len(trend) > 12 else 1
xt = trend["JahrMonat"][::step]

fig, ax = plt.subplots(figsize=FIG_TREND)
ax.plot(trend["JahrMonat"], trend["Gesamtstückzahl"])
ax.set_ylabel("Gesamtstückzahl")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=FIG_TREND)
ax.plot(trend["JahrMonat"], trend["Ausschussquote (%)"])
ax.set_ylabel("Ausschussquote (%)")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=FIG_TREND)
ax.plot(trend["JahrMonat"], trend["Stillstand_h"])
ax.set_ylabel("Stillstand (h)")
ax.set_xlabel("Monat")
ax.set_xticks(xt)
ax.set_xticklabels(xt, rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()

# --------------------------------------------------
# Chart 4: Energy per unit by line (FIXED)
# --------------------------------------------------
st.header("Energieverbrauch pro Stück nach Produktionslinie")

energy = kpi_line[["Produktionslinie", "Energie_kWh", "Gesamtstückzahl"]].copy()
energy["kWh pro Stück"] = (
    energy["Energie_kWh"] / energy["Gesamtstückzahl"].replace(0, np.nan)
).fillna(0).round(3)

st.dataframe(
    energy[["Produktionslinie", "kWh pro Stück"]].sort_values("kWh pro Stück", ascending=False),
    use_container_width=True,
)

fig, ax = plt.subplots(figsize=FIG_WIDE)
ax.bar(
    energy["Produktionslinie"].astype(str),
    energy["kWh pro Stück"],
    width=BAR_WIDTH,
)
ax.set_ylabel("kWh pro Stück")
ax.set_xlabel("Produktionslinie")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=GRID_ALPHA)
plt.tight_layout()
st.pyplot(fig)

st.divider()

st.write("Repository: https://github.com/DariaWagner/production-kpis-pandas")
