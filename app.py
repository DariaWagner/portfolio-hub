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
st.markdown("## Projektübersicht")

left, right = st.columns(2)

# Modern Business Card Style
card_style = """
    padding: 25px;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border: 1px solid #f2f2f2;
"""

# Pandas Card
with left:
    st.markdown(f"""
    <div style="{card_style}">
        <h3 style="margin-bottom:12px; font-weight:600; color:#333;">Pandas KPI Dashboard</h3>
        <hr style="margin-top:0; margin-bottom:18px; border:0; border-top:1px solid #e6e6e6;">

        <p style="color:#444; margin-bottom:4px;"><strong>Funktionen</strong></p>
        <ul style="color:#444; margin-top:0;">
            <li>KPI‑Berechnung (Output, Ausschuss, Energie, Stillstand)</li>
            <li>Interaktive Filter (Zeitraum, Linie, Schicht)</li>
            <li>Zeitreihenanalysen & Linienvergleich</li>
        </ul>

        <p style="color:#444; margin-top:18px;"><strong>Kurzbeschreibung</strong></p>
        <p style="color:#444; margin-top:-8px;">
            Analyse eines synthetischen Produktionsdatensatzes mit Pandas.
            Fokus auf KPI‑Definition, Datenbereinigung und fachliche Interpretation.
        </p>

        <p style="font-size:13px; color:#777; margin-top:20px;">Seite: Production KPIs (Pandas)</p>
    </div>
    """, unsafe_allow_html=True)

# SQL Card
with right:
    st.markdown(f"""
    <div style="{card_style}">
        <h3 style="margin-bottom:12px; font-weight:600; color:#333;">SQL Data Analysis</h3>
        <hr style="margin-top:0; margin-bottom:18px; border:0; border-top:1px solid #e6e6e6;">

        <p style="color:#444; margin-bottom:4px;"><strong>Funktionen</strong></p>
        <ul style="color:#444; margin-top:0;">
            <li>Business‑Fragen beantworten</li>
            <li>SQL‑ähnliche Abfragen (JOIN, GROUP BY, Aggregationen)</li>
            <li>Visualisierung der Ergebnisse</li>
        </ul>

        <p style="color:#444; margin-top:18px;"><strong>Kurzbeschreibung</strong></p>
        <p style="color:#444; margin-top:-8px;">
            Simulation einer SQL‑Analyse mit relationalem Modell
            (Faktentabelle + Dimensionstabellen).
            Fokus auf Query‑Logik und strukturierte Ergebnisdarstellung.
        </p>

        <p style="font-size:13px; color:#777; margin-top:20px;">Seite: SQL Data Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Closing
# =========================
st.write(
    "Alle Projekte sind praxisnah aufgebaut und orientieren sich an realistischen Anforderungen "
    "aus Produktion und Prozessanalyse."
)
