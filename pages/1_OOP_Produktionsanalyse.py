"""
OOP Production Analysis
=======================
Objektorientierte Modellierung von Produktionsdaten.
Fokus: Klassenstruktur, Geschäftslogik, SOLID-Prinzipien.
"""

import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional
from services.data_loader import load_production_data

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="OOP Production Analysis",
    page_icon="⚙️",
    layout="wide"
)


# =========================
# OOP Classes
# =========================

@dataclass
class ProductionRecord:
    """
    Repräsentiert einen einzelnen Produktionsdatensatz.

    Enthält alle relevanten Informationen zu einem Produktionsvorgang
    sowie Methoden zur Berechnung von KPIs auf Record-Ebene.
    """
    datum: pd.Timestamp
    linie: str
    schicht: str
    stueckzahl: int
    ausschuss: int
    energie_kwh: float
    stillstand_min: float

    def scrap_rate(self) -> float:
        """
        Berechnet die Ausschussquote in Prozent.

        Returns:
            float: Ausschussquote (0-100)
        """
        if self.stueckzahl == 0:
            return 0.0
        return (self.ausschuss / self.stueckzahl) * 100

    def energy_per_unit(self) -> float:
        """
        Berechnet den Energieverbrauch pro produziertem Stück.

        Returns:
            float: kWh pro Stück
        """
        if self.stueckzahl == 0:
            return 0.0
        return self.energie_kwh / self.stueckzahl

    def productivity_rate(self) -> float:
        """
        Berechnet die Produktivitätsrate (Good Units / Total Units).

        Returns:
            float: Produktivitätsrate (0-100)
        """
        if self.stueckzahl == 0:
            return 0.0
        good_units = self.stueckzahl - self.ausschuss
        return (good_units / self.stueckzahl) * 100


@dataclass
class ProductionLine:
    """
    Repräsentiert eine Produktionslinie mit mehreren Records.

    Aggregiert Daten über mehrere Produktionsvorgänge und
    berechnet KPIs auf Linienebene.
    """
    name: str
    records: List[ProductionRecord]

    def total_output(self) -> int:
        """Gesamte produzierte Stückzahl"""
        return sum(r.stueckzahl for r in self.records)

    def total_scrap(self) -> int:
        """Gesamter Ausschuss"""
        return sum(r.ausschuss for r in self.records)

    def total_downtime(self) -> float:
        """Gesamte Stillstandszeit in Minuten"""
        return sum(r.stillstand_min for r in self.records)

    def total_energy(self) -> float:
        """Gesamter Energieverbrauch in kWh"""
        return sum(r.energie_kwh for r in self.records)

    def avg_scrap_rate(self) -> float:
        """Durchschnittliche Ausschussquote über alle Records"""
        if not self.records:
            return 0.0
        return sum(r.scrap_rate() for r in self.records) / len(self.records)

    def avg_energy_per_unit(self) -> float:
        """Durchschnittlicher Energieverbrauch pro Stück"""
        if not self.records:
            return 0.0
        return sum(r.energy_per_unit() for r in self.records) / len(self.records)

    def avg_productivity(self) -> float:
        """Durchschnittliche Produktivitätsrate"""
        if not self.records:
            return 0.0
        return sum(r.productivity_rate() for r in self.records) / len(self.records)

    def good_units(self) -> int:
        """Anzahl fehlerfreier produzierter Einheiten"""
        return self.total_output() - self.total_scrap()

    def get_summary(self) -> dict:
        """
        Erstellt eine Zusammenfassung aller KPIs.

        Returns:
            dict: Dictionary mit allen relevanten KPIs
        """
        return {
            "Produktionslinie": self.name,
            "Datensätze": len(self.records),
            "Gesamtstückzahl": self.total_output(),
            "Gesamtausschuss": self.total_scrap(),
            "Fehlerfreie Einheiten": self.good_units(),
            "Ø Ausschussquote (%)": round(self.avg_scrap_rate(), 2),
            "Gesamtstillstand (Min)": round(self.total_downtime(), 1),
            "Gesamtenergie (kWh)": round(self.total_energy(), 2),
            "Ø Energie/Stück (kWh)": round(self.avg_energy_per_unit(), 3),
            "Ø Produktivität (%)": round(self.avg_productivity(), 2)
        }


class ProductionAnalyzer:
    """
    Analyzer-Klasse für erweiterte Analysen über mehrere Linien.

    Demonstriert das Strategy Pattern und Separation of Concerns.
    """

    def __init__(self, lines: List[ProductionLine]):
        self.lines = lines

    def compare_scrap_rates(self) -> pd.DataFrame:
        """Vergleicht Ausschussquoten zwischen Linien"""
        data = []
        for line in self.lines:
            data.append({
                "Linie": line.name,
                "Ausschussquote_%": round(line.avg_scrap_rate(), 2)
            })
        return pd.DataFrame(data).sort_values("Ausschussquote_%", ascending=False)

    def compare_energy_efficiency(self) -> pd.DataFrame:
        """Vergleicht Energieeffizienz zwischen Linien"""
        data = []
        for line in self.lines:
            data.append({
                "Linie": line.name,
                "kWh_pro_Stück": round(line.avg_energy_per_unit(), 3)
            })
        return pd.DataFrame(data).sort_values("kWh_pro_Stück", ascending=False)

    def get_best_performing_line(self) -> Optional[ProductionLine]:
        """Findet die Linie mit der besten Produktivität"""
        if not self.lines:
            return None
        return max(self.lines, key=lambda x: x.avg_productivity())

    def get_worst_performing_line(self) -> Optional[ProductionLine]:
        """Findet die Linie mit der schlechtesten Produktivität"""
        if not self.lines:
            return None
        return min(self.lines, key=lambda x: x.avg_productivity())


# =========================
# Header
# =========================
st.title("⚙️ OOP Production Analysis")
st.markdown("""
Diese Seite demonstriert eine **objektorientierte Modellierung** von Produktionsdaten.
Der Fokus liegt auf **Klassenstruktur, Geschäftslogik und SOLID-Prinzipien**.
""")

st.info(
    "📊 **Data Disclaimer:** Die verwendeten Daten sind synthetisch (KI-generiert) und simulieren "
    "reale industrielle Produktionsdaten. Es werden keine echten Unternehmensdaten verwendet."
)
st.divider()

# =========================
# Architecture Overview
# =========================
st.header("🏗️ Architektur-Übersicht")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### ProductionRecord
    📝 **Verantwortung:**
    - Einzelner Datensatz
    - Record-Level KPIs
    - Datenvalidierung

    **Methoden:**
    - `scrap_rate()`
    - `energy_per_unit()`
    - `productivity_rate()`
    """)

with col2:
    st.markdown("""
    #### ProductionLine
    🏭 **Verantwortung:**
    - Sammlung von Records
    - Aggregierte KPIs
    - Linien-Analyse

    **Methoden:**
    - `total_output()`
    - `avg_scrap_rate()`
    - `get_summary()`
    """)

with col3:
    st.markdown("""
    #### ProductionAnalyzer
    📊 **Verantwortung:**
    - Cross-Line Analysen
    - Vergleiche
    - Reporting

    **Methoden:**
    - `compare_scrap_rates()`
    - `get_best_performing_line()`
    """)

st.divider()


# =========================
# Data Loading
# =========================
@st.cache_data
def load_and_prepare_data():
    """Lädt und bereitet Produktionsdaten vor"""
    df = load_production_data().copy()

    # Typkonvertierung
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

    numeric_cols = [
        "Stueckzahl", "Ausschuss",
        "Energieverbrauch_kWh", "Stillstandszeit_Min"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Bereinigung
    df = df.dropna(subset=[
        "Datum", "Produktionslinie", "Schicht",
        "Stueckzahl", "Ausschuss",
        "Energieverbrauch_kWh", "Stillstandszeit_Min"
    ])

    return df


df = load_and_prepare_data()

# =========================
# Interactive Filters
# =========================
st.header("🔍 Filter")

col1, col2, col3 = st.columns(3)

with col1:
    min_date = df["Datum"].min().date()
    max_date = df["Datum"].max().date()

    date_range = st.date_input(
        "Zeitraum",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

with col2:
    linien = sorted(df["Produktionslinie"].unique())
    linie = st.selectbox("Produktionslinie", linien)

with col3:
    schichten = sorted(df["Schicht"].unique())
    selected_shifts = st.multiselect(
        "Schicht",
        options=schichten,
        default=schichten
    )

# Filter anwenden
df_filtered = df[
    (df["Datum"] >= pd.to_datetime(date_range[0])) &
    (df["Datum"] <= pd.to_datetime(date_range[1])) &
    (df["Produktionslinie"] == linie) &
    (df["Schicht"].isin(selected_shifts))
    ].copy()

st.divider()

# =========================
# Create OOP Objects
# =========================

# ProductionRecords erstellen
records = [
    ProductionRecord(
        datum=row["Datum"],
        linie=row["Produktionslinie"],
        schicht=row["Schicht"],
        stueckzahl=int(row["Stueckzahl"]),
        ausschuss=int(row["Ausschuss"]),
        energie_kwh=float(row["Energieverbrauch_kWh"]),
        stillstand_min=float(row["Stillstandszeit_Min"])
    )
    for _, row in df_filtered.iterrows()
]

# ProductionLine erstellen
line_obj = ProductionLine(name=linie, records=records)

# =========================
# Results Display
# =========================
st.header("📊 Analyse-Ergebnisse")

if not records:
    st.warning("⚠️ Keine Daten für die aktuelle Auswahl.")
else:
    # KPI Summary
    summary = line_obj.get_summary()

    # Als strukturierte Tabelle anzeigen
    summary_df = pd.DataFrame({
        "Kennzahl": summary.keys(),
        "Wert": summary.values()
    })

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # Zusätzliche Metriken
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Gesamtstückzahl",
            f"{line_obj.total_output():,}",
            help="Alle produzierten Einheiten"
        )

    with col2:
        st.metric(
            "Ausschussquote",
            f"{line_obj.avg_scrap_rate():.2f}%",
            help="Durchschnittliche Ausschussquote"
        )

    with col3:
        st.metric(
            "Produktivität",
            f"{line_obj.avg_productivity():.2f}%",
            help="Anteil fehlerfreier Einheiten"
        )

    with col4:
        st.metric(
            "Energieeffizienz",
            f"{line_obj.avg_energy_per_unit():.3f} kWh",
            help="Durchschnittlicher Verbrauch pro Stück"
        )

st.divider()

# =========================
# Detailed Records
# =========================
st.header("📋 Detaillierte Records")

with st.expander("🔎 Detaildaten anzeigen", expanded=False):
    if records:
        detail_data = []
        for r in records:
            detail_data.append({
                "Datum": r.datum.date(),
                "Schicht": r.schicht,
                "Stückzahl": r.stueckzahl,
                "Ausschuss": r.ausschuss,
                "Ausschussquote_%": round(r.scrap_rate(), 2),
                "Produktivität_%": round(r.productivity_rate(), 2),
                "Energie_kWh": round(r.energie_kwh, 2),
                "kWh_pro_Stück": round(r.energy_per_unit(), 3),
                "Stillstand_Min": round(r.stillstand_min, 1)
            })

        detail_df = pd.DataFrame(detail_data).sort_values("Datum")
        st.dataframe(detail_df, use_container_width=True)

st.divider()

# =========================
# Cross-Line Analysis
# =========================
st.header("🔄 Linienvergleich")

st.markdown("""
Hier wird die `ProductionAnalyzer`-Klasse verwendet, um mehrere Linien zu vergleichen.
Dies demonstriert das **Strategy Pattern** für wiederverwendbare Analyse-Logik.
""")

# Alle Linien analysieren
all_lines = []
for line_name in df["Produktionslinie"].unique():
    df_line = df[df["Produktionslinie"] == line_name]

    line_records = [
        ProductionRecord(
            datum=row["Datum"],
            linie=row["Produktionslinie"],
            schicht=row["Schicht"],
            stueckzahl=int(row["Stueckzahl"]),
            ausschuss=int(row["Ausschuss"]),
            energie_kwh=float(row["Energieverbrauch_kWh"]),
            stillstand_min=float(row["Stillstandszeit_Min"])
        )
        for _, row in df_line.iterrows()
    ]

    all_lines.append(ProductionLine(name=line_name, records=line_records))

# Analyzer erstellen
analyzer = ProductionAnalyzer(all_lines)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ausschussquoten-Vergleich")
    scrap_comparison = analyzer.compare_scrap_rates()
    st.dataframe(scrap_comparison, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Energieeffizienz-Vergleich")
    energy_comparison = analyzer.compare_energy_efficiency()
    st.dataframe(energy_comparison, use_container_width=True, hide_index=True)

# Best/Worst Performers
best_line = analyzer.get_best_performing_line()
worst_line = analyzer.get_worst_performing_line()

col1, col2 = st.columns(2)

with col1:
    if best_line:
        st.success(f"🏆 **Beste Linie:** {best_line.name} ({best_line.avg_productivity():.2f}% Produktivität)")

with col2:
    if worst_line:
        st.error(f"⚠️ **Schwächste Linie:** {worst_line.name} ({worst_line.avg_productivity():.2f}% Produktivität)")

st.divider()

# =========================
# Code Example
# =========================
st.header("💻 Code-Beispiel")

st.markdown("""
Hier ist ein Ausschnitt der `ProductionRecord`- und `ProductionLine`-Klassen,
die das **Dataclass Pattern** und **Single Responsibility Principle** demonstrieren:
""")

st.code("""
from dataclasses import dataclass
from typing import List

@dataclass
class ProductionRecord:
    '''Einzelner Produktionsdatensatz'''
    datum: pd.Timestamp
    linie: str
    schicht: str
    stueckzahl: int
    ausschuss: int
    energie_kwh: float
    stillstand_min: float

    def scrap_rate(self) -> float:
        '''Berechnet Ausschussquote'''
        if self.stueckzahl == 0:
            return 0.0
        return (self.ausschuss / self.stueckzahl) * 100

    def energy_per_unit(self) -> float:
        '''Berechnet Energie pro Stück'''
        if self.stueckzahl == 0:
            return 0.0
        return self.energie_kwh / self.stueckzahl


@dataclass
class ProductionLine:
    '''Produktionslinie mit mehreren Records'''
    name: str
    records: List[ProductionRecord]

    def total_output(self) -> int:
        '''Gesamter Output'''
        return sum(r.stueckzahl for r in self.records)

    def avg_scrap_rate(self) -> float:
        '''Durchschnittliche Ausschussquote'''
        if not self.records:
            return 0.0
        return sum(r.scrap_rate() for r in self.records) / len(self.records)


# Verwendung
line = ProductionLine(name="Linie_A", records=records)
print(f"Output: {line.total_output()}")
print(f"Ausschussquote: {line.avg_scrap_rate():.2f}%")
""", language="python")

st.divider()

# =========================
# SOLID Principles
# =========================
st.header("🎯 SOLID-Prinzipien in diesem Code")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **S - Single Responsibility**
    - `ProductionRecord`: Verwaltet einzelne Records
    - `ProductionLine`: Verwaltet Line-Level Logik
    - `ProductionAnalyzer`: Cross-Line Analysen

    **O - Open/Closed**
    - Klassen können erweitert werden (neue Methoden)
    - Ohne bestehenden Code zu ändern

    **L - Liskov Substitution**
    - Subklassen könnten hinzugefügt werden
    - Ohne Basisverhalten zu brechen
    """)

with col2:
    st.markdown("""
    **I - Interface Segregation**
    - Klare, fokussierte Schnittstellen
    - Keine überladenen Interfaces

    **D - Dependency Inversion**
    - Analyzer hängt von Abstraktion ab
    - Nicht von konkreter Implementierung
    """)

st.divider()

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("""
**🔗 Repository:** [github.com/DariaWagner/python-oop-basics](https://github.com/DariaWagner/python-oop-basics)

**📊 Technologie-Stack:** Python | Dataclasses | Type Hints | SOLID Principles | OOP Design Patterns
""")
