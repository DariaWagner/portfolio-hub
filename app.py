import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Data & Process Analytics – Portfolio",
    page_icon="📊",
    layout="wide"
)
with st.sidebar:
    st.markdown("### 🔧 Tech‑Stack")
    st.markdown("""
    ![Python](https://img.shields.io/badge/Python-3.10-blue)
    ![Pandas](https://img.shields.io/badge/Pandas-2.1-green)
    ![Plotly](https://img.shields.io/badge/Plotly-5.x-orange)
    ![Streamlit](https://img.shields.io/badge/Streamlit-latest-red)
    """)

# =========================
# Header
# =========================
st.title("📊 Data & Process Analytics – Portfolio")

st.info(
    "ℹ️ Die in diesem Portfolio verwendeten Datensätze sind synthetisch (KI-generiert) und dienen der realistischen "
    "Simulation industrieller Produktions- und Prozessdaten. Der Fokus liegt auf Analyse-Logik, KPI-Definition, "
    "Datenstruktur und Visualisierung – nicht auf sensiblen Echtdaten."
)

st.write(
    "Willkommen in meinem Portfolio. Hier sehen Sie praxisnahe Analysen auf Basis eines konsistenten "
    "Produktionsdatensatzes – umgesetzt mit **Pandas**, **SQL-Denkweise** und **OOP-Struktur**."
)

st.divider()

# =========================
# About Me + Portfolio
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Über mich")
    st.write(
        "Ich befinde mich aktuell in einer Umschulung im Bereich **Data & Process Analytics**. "
        "Mein Fokus liegt auf der strukturierten Analyse von Daten, der Ableitung von KPIs und dem Verständnis "
        "von Geschäftsprozessen."
    )
    st.write(
        "Ich arbeite gerne praxisnah: Daten werden nicht nur ausgewertet, sondern fachlich sinnvoll interpretiert "
        "und in eine saubere Struktur überführt."
    )

with col2:
    st.subheader("Über dieses Portfolio")
    st.write(
        "Dieses Portfolio zeigt mehrere Projekte auf Basis eines einheitlichen, synthetischen Produktionsdatensatzes."
    )
    st.write(
        "Ziel ist es zu zeigen, wie derselbe Datensatz aus unterschiedlichen Perspektiven analysiert werden kann – "
        "mit **Pandas**, **SQL** und **objektorientierter Modellierung (OOP)**."
    )

st.divider()

# =========================
# Project Overview
# =========================
# =========================
# Projektübersicht – verbessert
# =========================
st.markdown("## 📁 Projektübersicht")

left, right = st.columns(2)

with left:
    st.container()
    st.subheader("🐼 Pandas KPI Dashboard")
    st.markdown("""
    **Funktionen**
    - KPI‑Berechnung (Output, Ausschuss, Energie, Stillstand)
    - Interaktive Filter (Zeitraum, Linie, Schicht, Produkt)
    - Zeitreihen‑Analysen & Linienvergleich

    **Kurzbeschreibung**  
    Analyse eines Produktionsdatensatzes mit Pandas.  
    Fokus auf KPI‑Definition, Datenbereinigung und fachlicher Interpretation.
    """)
    st.caption("➡️ Seite: *Production KPIs (Pandas)*")

with right:
    st.container()
    st.subheader("🗄️ SQL Data Analysis")
    st.markdown("""
    **Funktionen**
    - Typische Business‑Fragen (z. B. „Welche Linie hat die höchste Ausschussquote?“)
    - SQL‑ähnliche Abfragen (JOINs, GROUP BY, Aggregationen)
    - Visualisierung der Ergebnisse

    **Kurzbeschreibung**  
    Simulation einer SQL‑Datenanalyse mit relationalem Modell  
    (Faktentabelle + Dimensionstabellen).  
    Fokus auf Query‑Logik und strukturierte Ergebnisdarstellung.
    """)
    st.caption("➡️ Seite: *SQL Data Analysis*")


st.subheader("🧩 OOP – Produktionsanalyse")
st.write(
    "Objektorientierte Modellierung von Produktionsdaten. "
    "Trennung von Datenlogik, Analyse und Auswertung zur Simulation einer realistischen Software-Struktur."
)
st.caption("➡️ Seite: *OOP_Produktionsanalyse*")
st.subheader("Architektur der OOP‑Produktionsanalyse")
st.markdown("""
**ProductionDataProcessor**  
→ Lädt Rohdaten, bereinigt sie und führt Typkonvertierungen durch.

**KPIBuilder**  
→ Berechnet KPIs wie Ausschussquote, OEE, Stillstandszeiten und Durchlaufzeiten.

**ReportGenerator**  
→ Aggregiert Ergebnisse, erstellt Tabellen und Visualisierungen für das Dashboard.

Diese Struktur simuliert eine realistische Trennung von Datenlogik, Analyse und Reporting.
""")

st.subheader("Identifizierte Prozessengpässe")
st.markdown("""
1. **Auffällig hohe Ausschussquote in Linie 3**  
   → Deutlich über dem Durchschnitt der anderen Linien. Mögliche Ursachen: Maschinenkalibrierung, Materialqualität.

2. **Erhöhte Stillstandszeiten in der Spätschicht (22–02 Uhr)**  
   → Muster deutet auf Personalengpässe oder Wartungsbedarf hin.

3. **Materialnachschub vor Station X verzögert**  
   → Wiederkehrende Wartezeiten zeigen Optimierungspotenzial in der Logistikplanung.
""")

st.divider()

# =========================
# Closing
# =========================
st.write(
    "Alle Projekte sind praxisnah aufgebaut und orientieren sich an realistischen Anforderungen "
    "aus Produktion und Prozessanalyse."
)
