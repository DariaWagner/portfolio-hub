import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Produktionsprozess-KPIs (Pandas)")

st.markdown("### Ziel")
st.write("Datenbereinigung und KPI-Berechnung auf einem Produktionsdatensatz.")

st.markdown("### Mini-Demo (Beispiel)")
st.write("Hier kannst du später echte Daten laden und KPI-Charts anzeigen.")

# Placeholder Demo-Daten
df = pd.DataFrame({
    "Monat": ["Jan", "Feb", "Mrz", "Apr"],
    "Ausschuss_%": [2.1, 1.8, 2.5, 1.6]
})

fig = plt.figure()
plt.plot(df["Monat"], df["Ausschuss_%"])
plt.xlabel("Monat")
plt.ylabel("Ausschuss %")
st.pyplot(fig)

st.markdown("### Repo")
st.write("➡️ GitHub-Link kommt hier rein.")
