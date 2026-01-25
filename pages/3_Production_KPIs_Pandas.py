import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from services.data_loader import load_data

# Optional: Plotly (interaktiv)
try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

st.set_page_config(page_title="Produktions-KPIs (Pandas)", layout="wide")

st.title("📈 Produktionsprozess-KPIs (Pandas)")
st.write("Interaktives KPI-Dashboard auf Basis des Produktionsdatensatzes.")

with st.expander("📥 Optional: CSV hochladen (überschreibt Repo-Datei)", expanded=False):
    uploaded = st.file_uploader("CSV auswählen", type=["csv"])
df = load_data(uploaded_file=uploaded)

# --- Basic checks ---
required = ["Datum", "Produktionslinie", "Stueckzahl", "Ausschuss", "Stillstandszeit_Min", "Energieverbrauch_kWh", "Materialkosten", "Produkt", "Schicht"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Es fehlen Spalten für das Dashboard: {missing}")
    st.stop()

df = df.dropna(subset=["Datum"])

# --- Controls ---
colA, colB, colC, colD = st.columns([2, 2, 2, 2])

min_d, max_d = df["Datum"].min(), df["Datum"].max()

with colA:
    start_end = st.date_input("Zeitraum", (min_d.date(), max_d.date()))
    if isinstance(start_end, tuple) and len(start_end) == 2:
        start, end = start_end
    else:
        start, end = min_d.date(), max_d.date()

with colB:
    linien = sorted(df["Produktionslinie"].dropna().unique().tolist())
    sel_linien = st.multiselect("Produktionslinie", linien, default=linien)

with colC:
    schichten = sorted(df["Schicht"].dropna().unique().tolist())
    sel_schichten = st.multiselect("Schicht", schichten, default=schichten)

with colD:
    products = sorted(df["Produkt"].dropna().unique().tolist())
    sel_products = st.multiselect("Produkt", products, default=products[: min(len(products), 10)] if len(products) > 10 else products)

use_plotly = False
if HAS_PLOTLY:
    use_plotly = st.toggle("Interaktiv (Plotly)", value=False)
else:
    st.caption("Plotly nicht installiert → es wird matplotlib verwendet.")

# --- Filter data ---
df_f = df[
    (df["Datum"] >= pd.to_datetime(start)) &
    (df["Datum"] <= pd.to_datetime(end)) &
    (df["Produktionslinie"].isin(sel_linien)) &
    (df["Schicht"].isin(sel_schichten)) &
    (df["Produkt"].isin(sel_products))
].copy()

if df_f.empty:
    st.warning("Keine Daten für die gewählten Filter. Bitte Filter anpassen.")
    st.stop()

# --- KPIs ---
total_units = float(df_f["Stueckzahl"].sum())
total_scrap = float(df_f["Ausschuss"].sum())
scrap_rate = (total_scrap / total_units) if total_units else 0.0
total_downtime = float(df_f["Stillstandszeit_Min"].sum())
total_energy = float(df_f["Energieverbrauch_kWh"].sum())
total_material = float(df_f["Materialkosten"].sum())

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Stückzahl", f"{total_units:,.0f}")
k2.metric("Ausschuss", f"{total_scrap:,.0f}")
k3.metric("Ausschussrate", f"{scrap_rate*100:.2f}%")
k4.metric("Stillstand (Min)", f"{total_downtime:,.0f}")
k5.metric("Energie (kWh)", f"{total_energy:,.0f}")
k6.metric("Materialkosten (€)", f"{total_material:,.0f}")

st.markdown("---")

# --- Tables ---
left, right = st.columns([2, 1])

with left:
    st.subheader("📋 Daten (Ausschnitt)")
    st.dataframe(df_f.sort_values("Datum", ascending=False).head(500), use_container_width=True)

with right:
    st.subheader("🔎 Quick Insights")
    # Top line by scrap rate
    by_line = df_f.groupby("Produktionslinie").agg(
        stueck=("Stueckzahl", "sum"),
        ausschuss=("Ausschuss", "sum"),
        stillstand=("Stillstandszeit_Min", "sum"),
        energie=("Energieverbrauch_kWh", "sum"),
        material=("Materialkosten", "sum")
    )
    by_line["ausschussrate"] = by_line["ausschuss"] / by_line["stueck"].replace(0, pd.NA)
    top_bad = by_line.sort_values("ausschussrate", ascending=False).head(5)
    st.write("**Top 5 Linien nach Ausschussrate**")
    st.dataframe(top_bad[["ausschussrate", "stueck", "ausschuss", "stillstand"]], use_container_width=True)

st.markdown("---")

# --- Charts ---
st.subheader("📊 Visualisierung")

# 1) Monthly trend: scrap rate + units
monthly = df_f.copy()
monthly["Monat"] = monthly["Datum"].dt.to_period("M").dt.to_timestamp()
m = monthly.groupby("Monat").agg(
    stueck=("Stueckzahl", "sum"),
    ausschuss=("Ausschuss", "sum"),
    stillstand=("Stillstandszeit_Min", "sum"),
    energie=("Energieverbrauch_kWh", "sum"),
    material=("Materialkosten", "sum")
).reset_index()
m["Ausschussrate_%"] = (m["ausschuss"] / m["stueck"].replace(0, pd.NA)) * 100

c1, c2 = st.columns(2)

with c1:
    st.write("**Ausschussrate (%) über Zeit (Monat)**")
    if use_plotly:
        fig = px.line(m, x="Monat", y="Ausschussrate_%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plt.figure()
        plt.plot(m["Monat"], m["Ausschussrate_%"])
        plt.xlabel("Monat")
        plt.ylabel("Ausschussrate (%)")
        st.pyplot(fig)

with c2:
    st.write("**Stückzahl über Zeit (Monat)**")
    if use_plotly:
        fig = px.line(m, x="Monat", y="stueck")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plt.figure()
        plt.plot(m["Monat"], m["stueck"])
        plt.xlabel("Monat")
        plt.ylabel("Stückzahl")
        st.pyplot(fig)

# 2) Units by line
st.write("**Stückzahl nach Produktionslinie**")
line_units = df_f.groupby("Produktionslinie")["Stueckzahl"].sum().sort_values(ascending=False).reset_index()
if use_plotly:
    fig = px.bar(line_units, x="Produktionslinie", y="Stueckzahl")
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = plt.figure()
    plt.bar(line_units["Produktionslinie"].astype(str), line_units["Stueckzahl"].values)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Stückzahl")
    plt.xlabel("Produktionslinie")
    st.pyplot(fig)

# 3) Energy by product (Top 10)
st.write("**Energieverbrauch nach Produkt (Top 10)**")
prod_energy = df_f.groupby("Produkt")["Energieverbrauch_kWh"].sum().sort_values(ascending=False).head(10).reset_index()
if use_plotly:
    fig = px.bar(prod_energy, x="Produkt", y="Energieverbrauch_kWh")
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = plt.figure()
    plt.bar(prod_energy["Produkt"].astype(str), prod_energy["Energieverbrauch_kWh"].values)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Energie (kWh)")
    plt.xlabel("Produkt")
    st.pyplot(fig)

# 4) Downtime by line
st.write("**Stillstandszeit nach Produktionslinie**")
line_dt = df_f.groupby("Produktionslinie")["Stillstandszeit_Min"].sum().sort_values(ascending=False).reset_index()
if use_plotly:
    fig = px.bar(line_dt, x="Produktionslinie", y="Stillstandszeit_Min")
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = plt.figure()
    plt.bar(line_dt["Produktionslinie"].astype(str), line_dt["Stillstandszeit_Min"].values)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Stillstandszeit (Min)")
    plt.xlabel("Produktionslinie")
    st.pyplot(fig)