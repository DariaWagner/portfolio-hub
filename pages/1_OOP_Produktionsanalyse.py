import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import List

from services.data_loader import load_production_data

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="OOP – Produktionsanalyse", layout="wide")

st.title("OOP-Projekt: Produktionsanalyse")
st.write(
    """
    Diese Seite zeigt eine **objektorientierte Modellierung von Produktionsdaten**
    auf Basis eines realistischen (synthetischen) CSV-Datensatzes.
    Fokus: **Datenstruktur, Geschäftslogik und interaktive Analyse**.
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

    def avg_scrap_rate(self) -> float:
        if not self.records:
            return 0.0
        return float(sum(r.scrap_rate() for r in self.records) / len(self.records))

    def avg_energy_per_unit(self) -> float:
        if not self.records:
            return 0.0
        return float(sum(r.energy_per_unit() for r in self.records) / len(self.records))


# --------------------------------------------------
# Daten laden & vorbereiten
# --------------------------------------------------
df = load_production_data().copy()

df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

for col in [
    "Stueckzahl",
    "Ausschuss",
    "Energieverbrauch_kWh",
    "Stillstandszeit_Min",
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(
    subset=[
        "Datum",
        "Produktionslinie",
        "Schicht",
        "Stueckzahl",
        "Ausschuss",
        "Energieverbrauch_kWh",
        "Stillstandszeit_Min",
    ]
)

# --------------------------------------------------
# Interaktive Filter
# --------------------------------------------------
st.header("Filter")

min_date = df["Datum"].min().date()
max_date = df["Datum"].max().date()

date_range = st.date_input(
    "Zeitraum",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

linien = sorted(df["Produktionslinie"].unique())
linie = st.selectbox("Produktionslinie", linien)

schichten = sorted(df["Schicht"].unique())
selected_shifts = st.multiselect(
    "Schicht",
    options=schichten,
    default=schichten,
)

df_f = df[
    (df["Datum"] >= pd.to_datetime(date_range[0]))
    & (df["Datum"] <= pd.to_datetime(date_range[1]))
    & (df["Produktionslinie"] == linie)
    & (df["Schicht"].isin(selected_shifts))
].copy()

# --------------------------------------------------
# OOP-Objekte erzeugen
# --------------------------------------------------
records = [
    ProductionRecord(
        datum=row["Datum"],
        linie=row["Produktionslinie"],
        schicht=row["Schicht"],
        stueckzahl=int(row["Stueckzahl"]),
        ausschuss=int(row["Ausschuss"]),
        energie_kwh=float(row["Energieverbrauch_kWh"]),
        stillstand_min=float(row["Stillstandszeit_Min"]),
    )
    for _, row in df_f.iterrows()
]

line_obj = ProductionLine(name=linie, records=records)

st.divider()

# --------------------------------------------------
# Ergebnis als Tabelle (kompakt!)
# --------------------------------------------------
st.subheader("Ergebnis (Übersicht)")

if not records:
    st.warning("Keine Daten für die aktuelle Auswahl.")
else:
    result_table = pd.DataFrame(
        {
            "Kennzahl": [
                "Produktionslinie",
                "Zeitraum",
                "Datensätze",
                "Gesamtstückzahl",
                "Gesamtausschuss",
                "Ø Ausschussquote (%)",
                "Gesamtstillstand (Min)",
                "Ø Energie pro Stück (kWh)",
            ],
            "Wert": [
                linie,
                f"{date_range[0]} bis {date_range[1]}",
                f"{len(records):,}",
                f"{line_obj.total_output():,}",
                f"{line_obj.total_scrap():,}",
                f"{line_obj.avg_scrap_rate():.2f}",
                f"{line_obj.total_downtime():,.0f}",
                f"{line_obj.avg_energy_per_unit():.3f}",
            ],
        }
    )

    st.dataframe(result_table, hide_index=True)

st.divider()

# --------------------------------------------------
# Detaildaten
# --------------------------------------------------
with st.expander("Detaildaten anzeigen"):
    if records:
        detail_df = pd.DataFrame(
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

        st.dataframe(detail_df, use_container_width=True)

st.divider()

# --------------------------------------------------
# Code-Beispiel
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
