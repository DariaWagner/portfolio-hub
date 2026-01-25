import streamlit as st

st.set_page_config(
    page_title="Portfolio | Data & Process Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📌 Mein Portfolio (Live-Demos)")
st.write(
    "Hier finden Sie meine Projekte aus Python, SQL und Data Analytics – "
    "inklusive Visualisierungen und kurzer fachlicher Zusammenfassung."
)

st.markdown("### 🔎 Was Sie hier sehen")
cols = st.columns(3)
with cols[0]:
    st.info("🧩 **Python/OOP**\n\nBestellverwaltung (OOP, Struktur, Tests/Logik)")
with cols[1]:
    st.info("🗄️ **SQL**\n\nAnalysen mit SQL + Business-Fragen + KPIs")
with cols[2]:
    st.info("📈 **Pandas & KPIs**\n\nDatenbereinigung, KPI-Berechnung, Charts")

st.markdown("---")
st.markdown("### 👩‍💻 Über mich (kurz)")
st.write(
    "Ich befinde mich in einer Umschulung im Bereich **IT Data & Process Analytics** "
    "und baue praxisnahe Projekte mit Fokus auf Datenanalyse, Struktur und Reporting."
)

st.markdown("➡️ **Links:**")
st.write("- GitHub: (kommt rein)")
st.write("- LinkedIn: (kommt rein)")
st.write("- CV (PDF): (optional)")


import streamlit as st

st.set_page_config(
    page_title="Portfolio Hub",
    layout="wide"
)

st.title("📊 Portfolio Hub")
st.write("Startseite funktioniert ✅")
