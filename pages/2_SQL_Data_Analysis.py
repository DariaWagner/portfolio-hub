import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from services.data_loader import load_data

try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

st.set_page_config(page_title="SQL Data Analysis", layout="wide")
st.title("🗄️ SQL Data Analysis (auf Basis des CSV)")

st.caption(
    "Hinweis: Die verwendeten Daten sind synthetisch (KI-generiert) "
    "und dienen der Demonstration von SQL-Analyse- und Reporting-Workflows."
)


st.write(
    "Diese Seite zeigt typische Business-Fragen und die passenden SQL-Queries. "
    "Die Ergebnisse werden direkt aus dem Datensatz berechnet und visualisiert."
)

with st.expander("📥 Optional: CSV hochladen (überschreibt Repo-Datei)", expanded=False):
    uploaded = st.file_uploader("CSV auswählen", type=["csv"])

df = load_data(uploaded_file=uploaded)

required = ["Datum", "Produktionslinie", "Stueckzahl", "Ausschuss", "Materialkosten", "Energieverbrauch_kWh", "Produkt", "Schicht"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Es fehlen Spalten: {missing}")
    st.stop()

df = df.dropna(subset=["Datum"])

use_plotly = HAS_PLOTLY and st.toggle("Interaktiv (Plotly)", value=False)

# Filter
min_d, max_d = df["Datum"].min(), df["Datum"].max()
start_end = st.date_input("Zeitraum", (min_d.date(), max_d.date()))
if isinstance(start_end, tuple) and len(start_end) == 2:
    start, end = start_end
else:
    start, end = min_d.date(), max_d.date()

df_f = df[(df["Datum"] >= pd.to_datetime(start)) & (df["Datum"] <= pd.to_datetime(end))].copy()

tab1, tab2, tab3 = st.tabs(["1) Ausschussrate je Linie", "2) Kosten je Produkt", "3) Energie & Output Trend"])

# --- 1) Scrap rate by line ---
with tab1:
    st.subheader("Business-Frage")
    st.write("Welche Produktionslinie hat die höchste Ausschussrate?")

    st.code(
        """
SELECT Produktionslinie,
       SUM(Stueckzahl)   AS total_units,
       SUM(Ausschuss)    AS total_scrap,
       SUM(Ausschuss) / NULLIF(SUM(Stueckzahl), 0) AS scrap_rate
FROM production
WHERE Datum BETWEEN :start AND :end
GROUP BY Produktionslinie
ORDER BY scrap_rate DESC;
        """.strip(),
        language="sql"
    )

    r = df_f.groupby("Produktionslinie").agg(
        total_units=("Stueckzahl", "sum"),
        total_scrap=("Ausschuss", "sum")
    )
    r["scrap_rate"] = r["total_scrap"] / r["total_units"].replace(0, pd.NA)
    r = r.sort_values("scrap_rate", ascending=False).reset_index()

    st.dataframe(r, use_container_width=True)

    st.write("**Visual**")
    top = r.head(10)
    if use_plotly:
        fig = px.bar(top, x="Produktionslinie", y="scrap_rate")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plt.figure()
        plt.bar(top["Produktionslinie"].astype(str), top["scrap_rate"].values)
        plt.xticks(rotation=30, ha="right")
        plt.ylabel("Ausschussrate")
        plt.xlabel("Produktionslinie")
        st.pyplot(fig)

# --- 2) Costs per product ---
with tab2:
    st.subheader("Business-Frage")
    st.write("Welche Produkte verursachen die höchsten Materialkosten?")

    st.code(
        """
SELECT Produkt,
       SUM(Materialkosten) AS material_costs
FROM production
WHERE Datum BETWEEN :start AND :end
GROUP BY Produkt
ORDER BY material_costs DESC
LIMIT 10;
        """.strip(),
        language="sql"
    )

    r = (
        df_f.groupby("Produkt")["Materialkosten"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(r, use_container_width=True)

    st.write("**Visual**")
    if use_plotly:
        fig = px.bar(r, x="Produkt", y="Materialkosten")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plt.figure()
        plt.bar(r["Produkt"].astype(str), r["Materialkosten"].values)
        plt.xticks(rotation=30, ha="right")
        plt.ylabel("Materialkosten")
        plt.xlabel("Produkt")
        st.pyplot(fig)

# --- 3) Energy & output trend ---
with tab3:
    st.subheader("Business-Frage")
    st.write("Wie entwickeln sich Energieverbrauch und Stückzahl über die Zeit?")

    st.code(
        """
SELECT DATE_TRUNC('month', Datum) AS month,
       SUM(Stueckzahl) AS units,
       SUM(Energieverbrauch_kWh) AS energy_kwh
FROM production
WHERE Datum BETWEEN :start AND :end
GROUP BY month
ORDER BY month;
        """.strip(),
        language="sql"
    )

    tmp = df_f.copy()
    tmp["Monat"] = tmp["Datum"].dt.to_period("M").dt.to_timestamp()

    r = tmp.groupby("Monat").agg(
        units=("Stueckzahl", "sum"),
        energy_kwh=("Energieverbrauch_kWh", "sum"),
    ).reset_index()

    st.dataframe(r, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Stückzahl (Monat)**")
        if use_plotly:
            fig = px.line(r, x="Monat", y="units")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = plt.figure()
            plt.plot(r["Monat"], r["units"])
            plt.xlabel("Monat")
            plt.ylabel("Stückzahl")
            st.pyplot(fig)

    with c2:
        st.write("**Energieverbrauch (Monat)**")
        if use_plotly:
            fig = px.line(r, x="Monat", y="energy_kwh")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = plt.figure()
            plt.plot(r["Monat"], r["energy_kwh"])
            plt.xlabel("Monat")
            plt.ylabel("Energie (kWh)")
            st.pyplot(fig)

st.markdown("---")
st.markdown("### 🔗 Repo")
st.markdown("[➡️ sql-data-analysis ansehen](https://github.com/DariaWagner/sql-data-analysis)")
