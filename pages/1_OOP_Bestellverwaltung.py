import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import List

from services.data_loader import load_production_data

st.set_page_config(page_title="OOP – Produktionsmodell", layout="wide")
st.title("OOP-Modellierung eines Produktionsprozesses")

st.write(
    """
    Diese Seite zeigt, wie ein Produktionsdatensatz **objektorientiert modelliert**
    und ausgewertet werden kann – auf Basis desselben CSVs wie die KPI-Analyse.
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
        return sum(r.stueckzahl for r in self.records)

    def total_downtime(self) -> float:
        return sum(r.stillstand_min for r in self.records)

    def avg_scrap_rate(self) -> float:
        if not self.records:
            return 0.0
        return sum(r.scrap_rate() for r in self.records) / len(self.records)


# --------------------------------------------------
# Daten laden & Objekte bauen
# --------------------------------------------------
df = load_production_data()

records = [
    ProductionRecord(
        datum=row["Datum"],
        linie=row["Produktionslinie"],
        stueckzahl=row["Stueckzahl"],
        ausschuss=row["Ausschuss"],
        energie_kwh=row["Energieverbrauch_kWh"],
        stillstand_min=row["Stillstandszeit_Min"],
    )
    for _, row in df.iterrows()
]

linien_namen = sorted(df["Produktionslinie"].dropna().unique())
linien_objekte = {
    name: ProductionLine(
        name=name,
        records=[r for r in records if r.linie == name],
    )
    for name in linien_namen
}

# --------------------------------------------------
# Live-Demo
# --------------------------------------------------
st.header("Live-Demo: Produktionslinie analysieren")

linie = st.selectbox("Produktionslinie", linien_namen)
obj = linien_objekte[linie]

col1, col2, col3 = st.columns(3)

col1.metric("Gesamtstückzahl", f"{obj.total_output():,}")
col2.metric("Gesamtstillstand (Min)", f"{obj.total_downtime():,.0f}")
col3.metric("Ø Ausschussquote (%)", f"{obj.avg_scrap_rate():.2f}")

st.divider()

# --------------------------------------------------
# Code-Ausschnitt
# --------------------------------------------------
st.header("Code-Beispiel (OOP-Modell)")

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

st.write(
    "Dieses OOP-Modell ist bewusst einfach gehalten, aber direkt "
    "auf reale Produktionsdaten übertragbar."
)
