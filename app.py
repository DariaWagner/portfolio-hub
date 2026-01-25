import streamlit as st

st.set_page_config(
    page_title="Data & Process Analytics Portfolio",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data & Process Analytics – Portfolio")

st.write(
    "Willkommen in meinem Portfolio. "
    "Hier sehen Sie praxisnahe Analysen auf Basis eines konsistenten Produktionsdatensatzes "
    "– umgesetzt mit **Pandas**, **SQL-Denkweise** und **OOP-Struktur**."
)

st.markdown("---")

# ---- Quick Overview Cards ----
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🐼 Pandas KPI Dashboard")
    st.write(
        "- KPIs & Filter\n"
        "- Zeitreihen & Vergleich\n"
        "- Produktions-, Kosten- & Energiedaten"
    )
    st.markdown("➡️ *Seite: Production KPIs (Pandas)*")

with c2:
    st.subheader("🗄️ SQL Data Analysis")
    st.write(
        "- Business-Fragen\n"
        "- SQL-Queries\n"
        "- Ergebnis + Visualisierung"
    )
