import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Data & Process Analytics – Portfolio",
    page_icon="📊",
    layout="wide"
)

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
left, right = st.columns(2)

with left:
    st.subheader("🐼 Pandas KPI Dashboard")
    st.markdown(
        "- **KPIs & Filter**\n"
        "- **Zeitreihen & Vergleich**\n"
        "- **Produktions-, Kosten- & Energiedaten**\n\n"
        "**Kurzbeschreibung:** Analyse von Produktions-, Kosten- und Energiedaten mit Pandas. "
        "Berechnung zentraler KPIs, Zeitreihenanalysen und Vergleich verschiedener Produktionslinien."
    )
    st.caption("➡️ Seite: *Production KPIs (Pandas)*")

with right:
    st.subheader("🗄️ SQL Data Analysis")
    st.markdown(
        "- **Business-Fragen**\n"
        "- **SQL-Queries**\n"
        "- **Ergebnis + Visualisierung**\n\n"
        "**Kurzbeschreibung:** Beantwortung typischer Business-Fragen mit SQL-Logik. "
        "Fokus auf saubere Queries, strukturierte Ergebnisse und verständliche Visualisierungen."
    )
    st.caption("➡️ Seite: *SQL Data Analysis*")

st.subheader("🧩 OOP – Produktionsanalyse")
st.write(
    "Objektorientierte Modellierung von Produktionsdaten. "
    "Trennung von Datenlogik, Analyse und Auswertung zur Simulation einer realistischen Software-Struktur."
)
st.caption("➡️ Seite: *OOP_Produktionsanalyse*")

st.divider()

# =========================
# Closing
# =========================
st.write(
    "Alle Projekte sind praxisnah aufgebaut und orientieren sich an realistischen Anforderungen "
    "aus Produktion und Prozessanalyse."
)
