import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import List

from services.data_loader import load_production_data

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="OOP – Produktionsmodell", layout="wide")

st.title("OOP-Modellierung eines Produktionsprozesses")
st.write(
    """
    Diese Seite zeigt eine **objektorientierte Modellierung** von Produktionsdaten
    (aus dem gleichen CSV wie die KPI-Analyse) – inklusive **interaktiver Auswertung**.
    """
)
st.divider()

# --------------------------------------------------
# OOP-Modelle
# --------------------------------------------------
@dataclass
class ProductionRecord:
    datum: pd.Timestamp
    linie: str
    schicht: str
    stueckzahl: int
    ausschuss: int
    energie_kwh: float
    stillstand_min: float

    def scrap_rate(self) -> float:
        return (self.ausschuss / self.stueckzahl) * 100 if self.stueckzahl else 0.0

    def energy_per_unit(self) -> float:
        return self.energie_kwh / self.stueckzahl if self.stueckzahl else 0.0


@dataclass
class ProductionLine:
    name: str
    records: List[ProductionRecord]

    def total_output(self) -> int:
        return int(sum(r.stueckzahl for r in self.records))

    def total_scrap(self) -> int:
        return int(sum(r.ausschuss for r in self.records))

    def total_downtime(self) -> float:
        return float(sum(r.stillstand_min for r in self.records))

    def total_energy(self) -> float:
        return float(sum(r.energie_kwh for r in self.records))

    def avg_scrap_rate(self) -> float:
        if not self.records:
            return 0.0
        return float(sum(r.scrap_rate() for r in self.records) / len(self.records))

    def avg_energy_per_unit(self) -> float:
        if not self.records:
            return 0.0
        return float(sum(r.energy_per_unit() for r in self.records) / len(self.records))


# --------------------------------------------------
# Daten laden
# --------------------------------------------------
df = load_production_data().copy()

# Minimal typing safety (falls CSV-Parsing mal anders ist)
if "Datum" in df.columns:
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

for col in ["Stueckzahl", "Ausschuss", "Energieverbrauch_kWh", "Stillstandszeit_Min"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

required_cols = ["Datum", "Produktionslinie", "Schicht", "Stueckzahl", "Ausschuss", "Energieverbrauch_kWh", "Stillstandszeit_Min"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error("Fehlende Spalten im Datensatz. Bitte prüfe CSV/Loader.")
    st.write(missing)
    st.stop()

df = df.dropna(subset=["Datum", "Produktionslinie", "Schicht"]).copy()

# --------------------------------------------------
# Interaktive Filter
# --------------------------------------------------
st.header("Interaktive Analyse")

min_date = df["Datum"].min().date()
max_date = df["Datum"].max().date()

date_range = st.date_input(
    "Zeitraum auswählen",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

lines_all = sorted(df["Produktionslinie"].dropna().unique().tolist())
selected_line = st.selectbox("Produktionslinie auswählen", options=lines_all)

shifts_all = sorted(df["Schicht"].dropna().unique().tolist())
selected_shifts = st.multiselect("Schicht (optional)", options=shifts_all, default=shifts_all)

kpi = st.radio(
    "Kennzahl auswählen",
    [
        "Gesamtstückzahl",
        "Gesamtausschuss",
        "Ø Ausschussquote (%)",
        "Gesamtstillstand (Min)",
        "Ø Energie pro Stück (kWh)",
    ],
    horizontal=True,
)

# Filter anwenden
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

df_f = df[
    (df["Datum"] >= start_date) &
    (df["Datum"] <= end_date) &
    (df["Produktionslinie"] == selected_line) &
    (df["Schicht"].isin(selected_shifts))
].copy()

# --------------------------------------------------
# Objekte bauen (nur gefilterte Daten)
# --------------------------------------------------
records = [
    ProductionRecord(
        datum=row["Datum"],
        linie=row["Produktionslinie"],
        schicht=row["Schicht"],
        stueckzahl=int(row["Stueckzahl"]) if pd.notna(row["Stueckzahl"]) else 0,
        ausschuss=int(row["Ausschuss"]) if pd.notna(row["Ausschuss"]) else 0,
        energie_kwh=float(row["Energieverbrauch_kWh"]) if pd.notna(row["Energieverbrauch_kWh"]) else 0.0,
        stillstand_min=float(row["Stillstandszeit_Min"]) if pd.notna(row["Stillstandszeit_Min"]) else 0.0,
    )
    for _, row in df_f.iterrows()
]

line_obj = ProductionLine(name=selected_line, records=records)

st.divider()

# --------------------------------------------------
# Ergebnis-Panel
# --------------------------------------------------
st.subheader("Ergebnis")

if len(records) == 0:
    st.warning("Keine Daten für diese Auswahl. Bitte Zeitraum/Filter anpassen.")
else:
    col1, col2, col3 = st.columns(3)

    col1.metric("Datensätze", f"{len(records):,}")
    col2.metric("Zeitraum", f"{date_range[0]} bis {date_range[1]}")
    col3.metric("Linie", selected_line)

    if kpi == "Gesamtstückzahl":
        st.metric("Gesamtstückzahl", f"{line_obj.total_output():,}")

    elif kpi == "Gesamtausschuss":
        st.metric("Gesamtausschuss", f"{line_obj.total_scrap():,}")

    elif kpi == "Ø Ausschussquote (%)":
        st.metric("Ø Ausschussquote", f"{line_obj.avg_scrap_rate():.2f} %")

    elif kpi == "Gesamtstillstand (Min)":
        st.metric("Gesamtstillstand", f"{line_obj.total_downtime():,.0f} Min")

    elif kpi == "Ø Energie pro Stück (kWh)":
        st.metric("Ø Energie pro Stück", f"{line_obj.avg_energy_per_unit():.3f} kWh")

st.divider()

# --------------------------------------------------
# Detaildaten (optional)
# --------------------------------------------------
with st.expander("Detaildaten anzeigen"):
    if len(records) == 0:
        st.info("Keine Detaildaten vorhanden (Filter anpassen).")
    else:
        df_detail = pd.DataFrame(
            [
                {
                    "Datum": r.datum.date(),
                    "Schicht": r.schicht,
                    "Stückzahl": r.stueckzahl,
                    "Ausschuss": r.ausschuss,
                    "Ausschussquote (%)": round(r.scrap_rate(), 2),
                    "Energie (kWh)": round(r.energie_kwh, 2),
                    "kWh pro Stück": round(r.energy_per_unit(), 3),
                    "Stillstand (Min)": round(r.stillstand_min, 1),
                }
                for r in records
            ]
        ).sort_values("Datum")

        st.dataframe(df_detail, use_container_width=True)

st.divider()

# --------------------------------------------------
# Code-Ausschnitt (kurz & HR-tauglich)
# --------------------------------------------------
st.header("Code-Beispiel (Ausschnitt)")

st.code(
    """@dataclass
class ProductionRecord:
    stueckzahl: int
    ausschuss: int

    def scrap_rate(self) -> float:
        return (self.ausschuss / self.stueckzahl) * 100 if self.stueckzahl else 0.0""",
    language="python",
)

st.divider()

st.write("Repository: https://github.com/DariaWagner/python-oop-basics")
