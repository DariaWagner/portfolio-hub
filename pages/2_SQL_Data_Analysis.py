import streamlit as st
import pandas as pd


# Page config

st.set_page_config(page_title="SQL Data Analysis", layout="wide")

st.title("SQL Data Analysis")
st.write(
    "Diese Seite zeigt SQL-nahe, relationale Analysen "
    "auf Basis eines normalisierten Produktionsdatenmodells."
)


# Data loading

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/produktionsdaten_premium_5Jahre.csv"
    )

df = load_data()


# Data Disclaimer

st.markdown(
    """
    **Data Disclaimer**

    Die verwendeten Daten sind synthetisch (KI-generiert) und simulieren
    reale industrielle Produktions- und Prozessdaten.
    Es werden keine echten Unternehmensdaten verwendet.
    """
)

st.divider()


# Relational data model (logical split)

st.header("Relationales Datenmodell (logisch)")

st.write(
    "Der ursprüngliche CSV-Datensatz wird logisch in "
    "mehrere relationale Tabellen aufgeteilt."
)

# Dimension tables
dim_date = (
    df[["Datum", "Jahr", "Monat"]]
    .drop_duplicates()
    .sort_values("Datum")
    .reset_index(drop=True)
)
dim_date["date_id"] = dim_date.index + 1

dim_line = (
    df[["Linie"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_line["line_id"] = dim_line.index + 1

dim_shift = (
    df[["Schicht"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_shift["shift_id"] = dim_shift.index + 1

dim_product = (
    df[["Produkt"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_product["product_id"] = dim_product.index + 1

# Fact table
fact_production = df.merge(dim_date, on=["Datum", "Jahr", "Monat"]) \
    .merge(dim_line, on="Linie") \
    .merge(dim_shift, on="Schicht") \
    .merge(dim_product, on="Produkt")

fact_production = fact_production[
    [
        "date_id",
        "line_id",
        "shift_id",
        "product_id",
        "Output",
        "Ausschuss",
        "Stillstand_min",
        "Energie_kWh",
        "Materialkosten"
    ]
]


# Display tables (SQL-style)

st.subheader("Dimension: Datum")
st.dataframe(dim_date, use_container_width=True)

st.subheader("Dimension: Produktionslinie")
st.dataframe(dim_line, use_container_width=True)

st.subheader("Dimension: Schicht")
st.dataframe(dim_shift, use_container_width=True)

st.subheader("Dimension: Produkt")
st.dataframe(dim_product, use_container_width=True)

st.subheader("Faktentabelle: Produktion")
st.dataframe(fact_production, use_container_width=True)

st.divider()


# SQL-like KPI queries (tabular only)

st.header("SQL-nahe KPI-Abfragen")

# KPI 1: Ausschussquote nach Linie
kpi_scrap = (
    fact_production
    .merge(dim_line, on="line_id")
    .groupby("Linie", as_index=False)
    .agg(
        Output=("Output", "sum"),
        Ausschuss=("Ausschuss", "sum")
    )
)

kpi_scrap["Ausschussquote_%"] = (
    kpi_scrap["Ausschuss"] / kpi_scrap["Output"] * 100
).round(2)

st.subheader("Ausschussquote nach Produktionslinie")
st.dataframe(kpi_scrap, use_container_width=True)

# KPI 2: Stillstandszeit nach Schicht
kpi_downtime = (
    fact_production
    .merge(dim_shift, on="shift_id")
    .groupby("Schicht", as_index=False)
    .agg(
        Stillstand_min=("Stillstand_min", "sum")
    )
)

st.subheader("Stillstandszeit nach Schicht")
st.dataframe(kpi_downtime, use_container_width=True)

# KPI 3: Energieverbrauch pro Produkt
kpi_energy = (
    fact_production
    .merge(dim_product, on="product_id")
    .groupby("Produkt", as_index=False)
    .agg(
        Energie_kWh=("Energie_kWh", "sum"),
        Output=("Output", "sum")
    )
)

kpi_energy["Energie_pro_Stück"] = (
    kpi_energy["Energie_kWh"] / kpi_energy["Output"]
).round(2)

st.subheader("Energieverbrauch pro Produkt")
st.dataframe(kpi_energy, use_container_width=True)

st.divider()


# Repository link

st.markdown(
    "Repository: "
    "[sql-data-analysis ansehen]"
    "(https://github.com/DariaWagner/sql-data-analysis)"
)
