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
st.markdown("## Projektübersicht")

left, right = st.columns(2)

with left:
    st.markdown("""
    <div style="padding:20px; border:1px solid #e0e0e0; border-radius:8px;">
        <h3 style="margin-bottom:8px;">Pandas KPI Dashboard</h3>
        <hr style="margin-top:0; margin-bottom:15px;">

        <strong>Funktionen</strong>
        <ul>
            <li>KPI‑Berechnung (Output, Ausschuss, Energie, Stillstand)</li>
            <li>Interaktive Filter (Zeitraum, Linie, Schicht)</li>
            <li>Zeitreihenanalysen & Linienvergleich</li>
        </ul>

        <strong>Kurzbeschreibung</strong>
        <p>
            Analyse eines synthetischen Produktionsdatensatzes mit Pandas.
            Fokus auf KPI‑Definition, Datenbereinigung und fachliche Interpretation.
        </p>

        <p style="font-size:13px; color:#666;">Seite: Production KPIs (Pandas)</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="padding:20px; border:1px solid #e0e0e0; border-radius:8px;">
        <h3 style="margin-bottom:8px;">SQL Data Analysis</h3>
        <hr style="margin-top:0; margin-bottom:15px;">

        <strong>Funktionen</strong>
        <ul>
            <li>Business‑Fragen beantworten</li>
            <li>SQL‑ähnliche Abfragen (JOIN, GROUP BY, Aggregationen)</li>
            <li>Visualisierung der Ergebnisse</li>
        </ul>

        <strong>Kurzbeschreibung</strong>
        <p>
            Simulation einer SQL‑Analyse mit relationalem Modell
            (Faktentabelle + Dimensionstabellen).
            Fokus auf Query‑Logik und strukturierte Ergebnisdarstellung.
        </p>

        <p style="font-size:13px; color:#666;">Seite: SQL Data Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Closing
# =========================
st.write(
    "Alle Projekte sind praxisnah aufgebaut und orientieren sich an realistischen Anforderungen "
    "aus Produktion und Prozessanalyse."
)
