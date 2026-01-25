import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Produktionsprozess-KPIs (Pandas)")

st.write("Interaktives KPI-Dashboard mit Filter, KPIs, Tabelle und Charts.")

# --- 1) Datenquelle: Upload oder Demo ---
uploaded = st.file_uploader("CSV hochladen (optional)", type=["csv"])

@st.cache_data
def load_demo():
    # kleine Demo-Daten (HR kann sofort sehen, dass es „echt“ ist)
    return pd.DataFrame({
        "Datum": pd.date_range("2025-01-01", periods=180, freq="D"),
        "Linie": (["A"]*60) + (["B"]*60) + (["C"]*60),
        "Output": ([520]*60) + ([480]*60) + ([510]*60),
        "Ausschuss": ([12]*60) + ([18]*60) + ([10]*60),
        "Stillstand_min": ([35]*60) + ([55]*60) + ([28]*60),
        "Temp": ([72]*60) + ([75]*60) + ([71]*60),
    })

@st.cache_data
def load_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    # Versuch, Datum zu finden/konvertieren
    for col in ["Datum", "date", "Date", "timestamp", "Timestamp"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df = df.rename(columns={col: "Datum"})
            break
    return df

df = load_csv(uploaded) if uploaded is not None else load_demo()

# --- 2) Minimaler „Datencheck“ ---
st.caption(f"Zeilen: {len(df):,} | Spalten: {len(df.columns)}")
with st.expander("Spalten anzeigen"):
    st.write(list(df.columns))

# --- 3) Filter ---
if "Datum" in df.columns:
    df = df.dropna(subset=["Datum"])
    min_d, max_d = df["Datum"].min(), df["Datum"].max()
    start, end = st.date_input("Zeitraum", (min_d.date(), max_d.date()))
    df = df[(df["Datum"] >= pd.to_datetime(start)) & (df["Datum"] <= pd.to_datetime(end))]

if "Linie" in df.columns:
    lines = sorted(df["Linie"].dropna().unique().tolist())
    sel = st.multiselect("Linie", lines, default=lines)
    df = df[df["Linie"].isin(sel)]

# --- 4) KPIs ---
def safe_div(a, b):
    return float(a) / float(b) if b else 0.0

total_output = df["Output"].sum() if "Output" in df.columns else 0
total_scrap = df["Ausschuss"].sum() if "Ausschuss" in df.columns else 0
scrap_rate = safe_div(total_scrap, total_output) if total_output else 0
downtime = df["Stillstand_min"].sum() if "Stillstand_min" in df.columns else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Output (Summe)", f"{total_output:,.0f}")
c2.metric("Ausschuss (Summe)", f"{total_scrap:,.0f}")
c3.metric("Ausschussrate", f"{scrap_rate*100:.2f}%")
c4.metric("Stillstand (min)", f"{downtime:,.0f}")

st.markdown("---")

# --- 5) Tabelle ---
st.subheader("📋 Daten (Ausschnitt)")
st.dataframe(df.head(200), use_container_width=True)

# --- 6) Charts ---
st.subheader("📊 Visuals")

# Chart 1: Ausschussrate über Zeit (täglich aggregiert)
if "Datum" in df.columns and "Ausschuss" in df.columns and "Output" in df.columns:
    daily = df.groupby(df["Datum"].dt.date).agg({"Ausschuss":"sum","Output":"sum"}).reset_index()
    daily["Ausschussrate"] = daily["Ausschuss"] / daily["Output"].replace(0, pd.NA)

    fig = plt.figure()
    plt.plot(daily["Datum"], daily["Ausschussrate"] * 100)
    plt.xlabel("Datum")
    plt.ylabel("Ausschussrate (%)")
    st.pyplot(fig)

# Chart 2: Output nach Linie (Balken)
if "Linie" in df.columns and "Output" in df.columns:
    by_line = df.groupby("Linie")["Output"].sum().sort_values(ascending=False)
    fig2 = plt.figure()
    plt.bar(by_line.index.astype(str), by_line.values)
    plt.xlabel("Linie")
    plt.ylabel("Output (Summe)")
    st.pyplot(fig2)

# Chart 3: Stillstand nach Linie (Balken)
if "Linie" in df.columns and "Stillstand_min" in df.columns:
    dt_line = df.groupby("Linie")["Stillstand_min"].sum().sort_values(ascending=False)
    fig3 = plt.figure()
    plt.bar(dt_line.index.astype(str), dt_line.values)
    plt.xlabel("Linie")
    plt.ylabel("Stillstand (min)")
    st.pyplot(fig3)

st.markdown("### 🔗 Repo")
st.markdown("[➡️ data-cleaning-analysis-pandas-visualization ansehen](https://github.com/DariaWagner/data-cleaning-analysis-pandas-visualization)")
