"""
SQL Data Analysis
=================
Relationale Datenmodellierung und SQL-ähnliche Analysen mit Pandas.
Fokus: Dimensionstabellen, Faktentabellen und strukturierte Queries.
"""

import sys
from pathlib import Path

# Path Setup
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from services.data_loader import load_production_data

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="SQL Data Analysis",
    page_icon="🗄️",
    layout="wide"
)

# =========================
# Header
# =========================
st.title("🗄️ SQL Data Analysis")
st.markdown("""
Diese Seite zeigt eine **SQL-nahe Analyse** auf Basis eines normalisierten Datenmodells.
Der Fokus liegt auf **relationaler Datenmodellierung** und strukturierter Query-Logik.
""")

st.info(
    "📊 **Data Disclaimer:** Die verwendeten Daten sind synthetisch (KI-generiert) und simulieren "
    "reale industrielle Produktions- und Prozessdaten. Es werden keine echten Unternehmensdaten verwendet."
)
st.divider()


# =========================
# Data Loading & Validation
# =========================
@st.cache_data
def load_and_validate_data():
    """Lädt und validiert Produktionsdaten"""
    df = load_production_data().copy()

    # Datum konvertieren
    if "Datum" in df.columns:
        df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

    return df


df_raw = load_and_validate_data()

# Spalten-Validierung
required_cols = [
    "Datum", "Unternehmen", "Produkt", "Modifikation",
    "Produktionslinie", "Schicht", "Auftragsnummer", "Status", "Fehlercode",
    "Stueckzahl", "Ausschuss", "Betriebsstunden", "Stillstandszeit_Min",
    "Materialkosten", "Energieverbrauch_kWh", "Mitarbeiter_Produktion",
    "Softwareversion", "Firmwareversion", "EndOfLine_Test",
    "MaxTemperatur", "Durchschnittstemperatur"
]

missing = [c for c in required_cols if c not in df_raw.columns]
if missing:
    st.error(f"⚠️ Fehlende Spalten im CSV: {', '.join(missing)}")
    st.stop()

# =========================
# Relational Model Explanation
# =========================
st.header("📐 Relationales Datenmodell")

st.markdown("""
Der CSV-Datensatz wird logisch in **Dimensionstabellen** (Stammdaten) und eine 
**Faktentabelle** (Messwerte) aufgeteilt. Dies entspricht dem **Star Schema** 
in relationalen Datenbanken und Data Warehouses.

**Vorteile:**
- ✅ Normalisierung reduziert Redundanz
- ✅ Strukturierte Abfragen mit JOINs
- ✅ Einfache Erweiterbarkeit
- ✅ Optimierte Performance bei Aggregationen
""")

st.divider()

# =========================
# Build Dimension Tables
# =========================
st.header("📊 Dimensionstabellen")

# Dimension: Datum
dim_datum = (
    df_raw[["Datum"]]
    .dropna()
    .drop_duplicates()
    .sort_values("Datum")
    .reset_index(drop=True)
)
dim_datum["datum_id"] = dim_datum.index + 1
dim_datum["jahr"] = dim_datum["Datum"].dt.year
dim_datum["monat"] = dim_datum["Datum"].dt.month
dim_datum["tag"] = dim_datum["Datum"].dt.day

# Dimension: Unternehmen
dim_unternehmen = (
    df_raw[["Unternehmen"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_unternehmen["unternehmen_id"] = dim_unternehmen.index + 1

# Dimension: Produkt
dim_produkt = (
    df_raw[["Produkt", "Modifikation"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_produkt["produkt_id"] = dim_produkt.index + 1

# Dimension: Produktionslinie
dim_linie = (
    df_raw[["Produktionslinie"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_linie["linie_id"] = dim_linie.index + 1

# Dimension: Schicht
dim_schicht = (
    df_raw[["Schicht"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_schicht["schicht_id"] = dim_schicht.index + 1

# Dimension: Software
dim_software = (
    df_raw[["Softwareversion", "Firmwareversion"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_software["software_id"] = dim_software.index + 1

# Dimension: Status
dim_status = (
    df_raw[["Status", "Fehlercode"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_status["status_id"] = dim_status.index + 1

# Dimensionstabellen anzeigen
with st.expander("📅 dim_datum"):
    st.dataframe(dim_datum.head(20), use_container_width=True)

with st.expander("🏢 dim_unternehmen"):
    st.dataframe(dim_unternehmen, use_container_width=True)

with st.expander("📦 dim_produkt"):
    st.dataframe(dim_produkt.head(20), use_container_width=True)

with st.expander("🏭 dim_produktionslinie"):
    st.dataframe(dim_linie, use_container_width=True)

with st.expander("🕐 dim_schicht"):
    st.dataframe(dim_schicht, use_container_width=True)

with st.expander("💾 dim_software"):
    st.dataframe(dim_software.head(20), use_container_width=True)

with st.expander("⚠️ dim_status"):
    st.dataframe(dim_status.head(20), use_container_width=True)

st.divider()

# =========================
# Build Fact Table
# =========================
st.header("📋 Faktentabelle")

st.markdown("""
Die Faktentabelle enthält nur **Messwerte** und **Foreign Keys** zu den Dimensionstabellen.
Dies entspricht dem Prinzip der **Normalisierung** in relationalen Datenbanken.
""")

# JOINs durchführen
fact = (
    df_raw
    .merge(dim_datum[["Datum", "datum_id"]], on="Datum", how="left")
    .merge(dim_unternehmen[["Unternehmen", "unternehmen_id"]], on="Unternehmen", how="left")
    .merge(dim_produkt[["Produkt", "Modifikation", "produkt_id"]], on=["Produkt", "Modifikation"], how="left")
    .merge(dim_linie[["Produktionslinie", "linie_id"]], on="Produktionslinie", how="left")
    .merge(dim_schicht[["Schicht", "schicht_id"]], on="Schicht", how="left")
    .merge(dim_software[["Softwareversion", "Firmwareversion", "software_id"]],
           on=["Softwareversion", "Firmwareversion"], how="left")
    .merge(dim_status[["Status", "Fehlercode", "status_id"]], on=["Status", "Fehlercode"], how="left")
)

# Faktentabelle mit nur IDs und Messwerten
fact_produktion = fact[[
    "datum_id", "unternehmen_id", "produkt_id", "linie_id", "schicht_id",
    "software_id", "status_id", "Auftragsnummer",
    "Stueckzahl", "Ausschuss", "Betriebsstunden", "Stillstandszeit_Min",
    "Materialkosten", "Energieverbrauch_kWh", "Mitarbeiter_Produktion",
    "MaxTemperatur", "Durchschnittstemperatur", "EndOfLine_Test"
]].copy()

# Primary Key hinzufügen
fact_produktion.insert(0, "produktion_id", range(1, len(fact_produktion) + 1))

st.dataframe(fact_produktion.head(100), use_container_width=True)

# Statistiken
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Anzahl Records", f"{len(fact_produktion):,}")
with col2:
    st.metric("Dimensionen", 7)
with col3:
    st.metric("Messwerte", 11)

st.divider()

# =========================
# SQL-like Queries
# =========================
st.header("📊 SQL-ähnliche Abfragen")

st.markdown("""
Die folgenden Analysen simulieren typische **SQL-Queries** mit Pandas:
- `JOIN` - Verknüpfung von Fakten- und Dimensionstabellen
- `GROUP BY` - Gruppierung nach Dimensionen
- `AGGREGATE` - Summen, Durchschnitte, Counts
- `ORDER BY` - Sortierung der Ergebnisse
""")

# =========================
# Query 1: KPIs by Line
# =========================
st.subheader("Query 1: KPIs nach Produktionslinie")

with st.expander("🔍 SQL-Äquivalent anzeigen"):
    st.code("""
SELECT 
    l.Produktionslinie,
    SUM(f.Stueckzahl) as stueckzahl,
    SUM(f.Ausschuss) as ausschuss,
    SUM(f.Stillstandszeit_Min) as stillstand_min,
    SUM(f.Energieverbrauch_kWh) as energie_kwh,
    SUM(f.Materialkosten) as materialkosten,
    ROUND(SUM(f.Ausschuss) * 100.0 / SUM(f.Stueckzahl), 2) as ausschussquote_prozent
FROM fact_produktion f
JOIN dim_produktionslinie l ON f.linie_id = l.linie_id
GROUP BY l.Produktionslinie
ORDER BY ausschussquote_prozent DESC;
    """, language="sql")

# Pandas-Implementierung
kpi_linie = (
    fact_produktion
    .merge(dim_linie, on="linie_id")
    .groupby("Produktionslinie", as_index=False)
    .agg({
        "Stueckzahl": "sum",
        "Ausschuss": "sum",
        "Stillstandszeit_Min": "sum",
        "Energieverbrauch_kWh": "sum",
        "Materialkosten": "sum"
    })
)

kpi_linie.columns = [
    "Produktionslinie", "stueckzahl", "ausschuss",
    "stillstand_min", "energie_kwh", "materialkosten"
]

kpi_linie["ausschussquote_prozent"] = (
        kpi_linie["ausschuss"] * 100.0 / kpi_linie["stueckzahl"].replace(0, pd.NA)
).round(2)

st.dataframe(
    kpi_linie.sort_values("ausschussquote_prozent", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# Query 2: KPIs by Shift
# =========================
st.subheader("Query 2: KPIs nach Schicht")

with st.expander("🔍 SQL-Äquivalent anzeigen"):
    st.code("""
SELECT 
    s.Schicht,
    SUM(f.Stueckzahl) as stueckzahl,
    SUM(f.Ausschuss) as ausschuss,
    SUM(f.Stillstandszeit_Min) as stillstand_min,
    ROUND(SUM(f.Ausschuss) * 100.0 / SUM(f.Stueckzahl), 2) as ausschussquote_prozent
FROM fact_produktion f
JOIN dim_schicht s ON f.schicht_id = s.schicht_id
GROUP BY s.Schicht
ORDER BY ausschussquote_prozent DESC;
    """, language="sql")

# Pandas-Implementierung
kpi_schicht = (
    fact_produktion
    .merge(dim_schicht, on="schicht_id")
    .groupby("Schicht", as_index=False)
    .agg({
        "Stueckzahl": "sum",
        "Ausschuss": "sum",
        "Stillstandszeit_Min": "sum"
    })
)

kpi_schicht.columns = ["Schicht", "stueckzahl", "ausschuss", "stillstand_min"]

kpi_schicht["ausschussquote_prozent"] = (
        kpi_schicht["ausschuss"] * 100.0 / kpi_schicht["stueckzahl"].replace(0, pd.NA)
).round(2)

st.dataframe(
    kpi_schicht.sort_values("ausschussquote_prozent", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# Query 3: Top Products by Scrap Rate
# =========================
st.subheader("Query 3: Top 15 Produkte nach Ausschussquote")

with st.expander("🔍 SQL-Äquivalent anzeigen"):
    st.code("""
SELECT 
    p.Produkt,
    p.Modifikation,
    SUM(f.Stueckzahl) as stueckzahl,
    SUM(f.Ausschuss) as ausschuss,
    ROUND(SUM(f.Ausschuss) * 100.0 / SUM(f.Stueckzahl), 2) as ausschussquote_prozent
FROM fact_produktion f
JOIN dim_produkt p ON f.produkt_id = p.produkt_id
GROUP BY p.Produkt, p.Modifikation
ORDER BY ausschussquote_prozent DESC
LIMIT 15;
    """, language="sql")

# Pandas-Implementierung
kpi_produkt = (
    fact_produktion
    .merge(dim_produkt, on="produkt_id")
    .groupby(["Produkt", "Modifikation"], as_index=False)
    .agg({
        "Stueckzahl": "sum",
        "Ausschuss": "sum"
    })
)

kpi_produkt.columns = ["Produkt", "Modifikation", "stueckzahl", "ausschuss"]

kpi_produkt["ausschussquote_prozent"] = (
        kpi_produkt["ausschuss"] * 100.0 / kpi_produkt["stueckzahl"].replace(0, pd.NA)
).round(2)

st.dataframe(
    kpi_produkt.sort_values("ausschussquote_prozent", ascending=False).head(15),
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# Query 4: Monthly Trend
# =========================
st.subheader("Query 4: Monatlicher Trend")

with st.expander("🔍 SQL-Äquivalent anzeigen"):
    st.code("""
SELECT 
    d.jahr,
    d.monat,
    SUM(f.Stueckzahl) as stueckzahl,
    SUM(f.Ausschuss) as ausschuss,
    ROUND(SUM(f.Ausschuss) * 100.0 / SUM(f.Stueckzahl), 2) as ausschussquote_prozent
FROM fact_produktion f
JOIN dim_datum d ON f.datum_id = d.datum_id
GROUP BY d.jahr, d.monat
ORDER BY d.jahr, d.monat;
    """, language="sql")

# Pandas-Implementierung
trend = (
    fact_produktion
    .merge(dim_datum, on="datum_id")
    .groupby(["jahr", "monat"], as_index=False)
    .agg({
        "Stueckzahl": "sum",
        "Ausschuss": "sum"
    })
)

trend.columns = ["jahr", "monat", "stueckzahl", "ausschuss"]

trend["ausschussquote_prozent"] = (
        trend["ausschuss"] * 100.0 / trend["stueckzahl"].replace(0, pd.NA)
).round(2)

trend["periode"] = trend["jahr"].astype(str) + "-" + trend["monat"].astype(str).str.zfill(2)

st.dataframe(
    trend[["periode", "stueckzahl", "ausschuss", "ausschussquote_prozent"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# Summary
# =========================
st.header("📝 Zusammenfassung")

st.markdown("""
Diese Seite demonstriert:

✅ **Relationale Datenmodellierung** mit Dimensions- und Faktentabellen  
✅ **SQL-ähnliche Queries** mit Pandas (JOIN, GROUP BY, AGGREGATE)  
✅ **Star Schema** - bewährtes Pattern für Data Warehousing  
✅ **Strukturierte Analyse** - wiederholbar und skalierbar  

**Nächste Schritte:**
- Implementierung in echter SQL-Datenbank (PostgreSQL, MySQL)
- ETL-Pipeline für automatisierte Datenintegration
- OLAP-Cubes für multidimensionale Analysen
""")

st.divider()

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("""
**🔗 Repository:** [github.com/DariaWagner/sql-data-analysis](https://github.com/DariaWagner/sql-data-analysis)

**📊 Technologie-Stack:** Python | Pandas | SQL-Logik | Relationale Datenmodellierung
""")
