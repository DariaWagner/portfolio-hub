import streamlit as st
import pandas as pd
from dataclasses import dataclass

from services.data_loader import load_data

st.set_page_config(page_title="OOP Reporting", layout="wide")
st.title("🧩 OOP: Business-Reporting auf Produktionsdaten")

st.write(
    "Diese Seite zeigt, wie man Business-Logik mit OOP kapselt: "
    "Daten laden → Report erzeugen → Top-Insights als strukturierte Ausgabe."
)

with st.expander("📥 Optional: CSV hochladen (überschreibt Repo-Datei)", expanded=False):
    uploaded = st.file_uploader("CSV auswählen", type=["csv"])

df = load_data(uploaded_file=uploaded)

required = ["Datum", "Produktionslinie", "Stueckzahl", "Ausschuss", "Stillstandszeit_Min", "Energieverbrauch_kWh", "Materialkosten", "Produkt", "Schicht"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Es fehlen Spalten: {missing}")
    st.stop()

df = df.dropna(subset=["Datum"])

# --- Filters (light) ---
min_d, max_d = df["Datum"].min(), df["Datum"].max()
start_end = st.date_input("Zeitraum", (min_d.date(), max_d.date()))
if isinstance(start_end, tuple) and len(start_end) == 2:
    start, end = start_end
else:
    start, end = min_d.date(), max_d.date()

df_f = df[(df["Datum"] >= pd.to_datetime(start)) & (df["Datum"] <= pd.to_datetime(end))].copy()

linien = sorted(df_f["Produktionslinie"].dropna().unique().tolist())
sel_linien = st.multiselect("Produktionslinie", linien, default=linien)
df_f = df_f[df_f["Produktionslinie"].isin(sel_linien)].copy()

# --- OOP model ---
@dataclass(frozen=True)
class ReportConfig:
    top_n: int = 5

class ProductionReport:
    def __init__(self, data: pd.DataFrame, cfg: ReportConfig):
        self.data = data.copy()
        self.cfg = cfg

    def kpis(self) -> dict:
        units = float(self.data["Stueckzahl"].sum())
        scrap = float(self.data["Ausschuss"].sum())
        downtime = float(self.data["Stillstandszeit_Min"].sum())
        energy = float(self.data["Energieverbrauch_kWh"].sum())
        material = float(self.data["Materialkosten"].sum())
        scrap_rate = (scrap / units) if units else 0.0
        return {
            "units": units,
            "scrap": scrap,
            "scrap_rate": scrap_rate,
            "downtime": downtime,
            "energy": energy,
            "material": material,
        }

    def top_lines_by_scrap_rate(self) -> pd.DataFrame:
        g = self.data.groupby("Produktionslinie").agg(
            units=("Stueckzahl", "sum"),
            scrap=("Ausschuss", "sum"),
            downtime=("Stillstandszeit_Min", "sum"),
        )
        g["scrap_rate"] = g["scrap"] / g["units"].replace(0, pd.NA)
        return g.sort_values("scrap_rate", ascending=False).head(self.cfg.top_n).reset_index()

    def top_products_by_material_cost(self) -> pd.DataFrame:
        g = self.data.groupby("Produkt")["Materialkosten"].sum().sort_values(ascending=False)
        return g.head(self.cfg.top_n).reset_index().rename(columns={"Materialkosten": "material_costs"})

    def anomalies(self) -> pd.DataFrame:
        # Simple rule-based anomalies: very high downtime or scrap rate
        tmp = self.data.copy()
        tmp["scrap_rate_row"] = tmp["Ausschuss"] / tmp["Stueckzahl"].replace(0, pd.NA)
        a = tmp[
            (tmp["Stillstandszeit_Min"] >= tmp["Stillstandszeit_Min"].quantile(0.99)) |
            (tmp["scrap_rate_row"] >= tmp["scrap_rate_row"].quantile(0.99))
        ].sort_values("Datum", ascending=False)
        cols = ["Datum", "Produktionslinie", "Produkt", "Schicht", "Stueckzahl", "Ausschuss", "Stillstandszeit_Min", "scrap_rate_row"]
        return a[cols].head(20)

# --- UI ---
col1, col2 = st.columns([1, 2])
with col1:
    top_n = st.slider("Top N", 3, 10, 5)

cfg = ReportConfig(top_n=top_n)
report = ProductionReport(df_f, cfg)

if df_f.empty:
    st.warning("Keine Daten für die gewählten Filter.")
    st.stop()

st.markdown("### ✅ Report-Ausgabe (OOP)")
k = report.kpis()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Stückzahl", f"{k['units']:,.0f}")
m2.metric("Ausschuss", f"{k['scrap']:,.0f}")
m3.metric("Ausschussrate", f"{k['scrap_rate']*100:.2f}%")
m4.metric("Stillstand (Min)", f"{k['downtime']:,.0f}")
m5.metric("Energie (kWh)", f"{k['energy']:,.0f}")
m6.metric("Materialkosten (€)", f"{k['material']:,.0f}")

st.markdown("---")

cA, cB = st.columns(2)
with cA:
    st.subheader("Top Linien nach Ausschussrate")
    st.dataframe(report.top_lines_by_scrap_rate(), use_container_width=True)

with cB:
    st.subheader("Top Produkte nach Materialkosten")
    st.dataframe(report.top_products_by_material_cost(), use_container_width=True)

st.subheader("⚠️ Auffälligkeiten (regelbasiert)")
st.dataframe(report.anomalies(), use_container_width=True)

st.markdown("---")
st.markdown("### 🔗 Repo")
st.markdown("[➡️ python-oop-basics ansehen](https://github.com/DariaWagner/python-oop-basics)")
