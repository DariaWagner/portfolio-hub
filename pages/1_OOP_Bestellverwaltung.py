import streamlit as st

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="OOP Bestellverwaltung",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("OOP-Projekt: Bestellverwaltung")

st.write(
    """
    Diese Seite zeigt ein **objektorientiertes Python-Projekt**
    mit klarer Klassenstruktur und fachlicher Modellierung
    eines einfachen Bestellprozesses.
    """
)

st.divider()

# --------------------------------------------------
# Ziel
# --------------------------------------------------
st.header("Projektziel")

st.write(
    """
    Entwicklung einer kleinen Bestellverwaltung als OOP-Projekt
    mit Fokus auf:
    
    - saubere Klassenstruktur
    - klare Verantwortlichkeiten
    - nachvollziehbare Geschäftslogik
    """
)

# --------------------------------------------------
# Klassenmodell
# --------------------------------------------------
st.header("Klassen & Modell")

st.write(
    """
    Das Projekt besteht aus mehreren logisch getrennten Klassen:
    """
)

st.markdown(
    """
    - **Produkt** – Artikelstammdaten (Name, Preis)
    - **Kunde** – Kundendaten
    - **Bestellposition** – Produkt + Menge
    - **Bestellung** – enthält mehrere Positionen
    - **Zahlung** – Zahlungsart und Status
    """
)

# --------------------------------------------------
# OOP-Prinzipien
# --------------------------------------------------
st.header("Eingesetzte OOP-Prinzipien")

st.markdown(
    """
    - Kapselung von Daten und Logik  
    - Trennung von Modell- und Serviceklassen  
    - Klare Abhängigkeiten zwischen Objekten  
    - Erweiterbarkeit ohne Code-Duplikation  
    """
)

# --------------------------------------------------
# Tech Stack
# --------------------------------------------------
st.header("Technischer Stack")

st.code(
    "Python | OOP | Git | GitHub",
    language="text"
)

# --------------------------------------------------
# Repo Link
# --------------------------------------------------
st.header("Repository")

st.markdown(
    "[GitHub Repository – python-oop-basics](https://github.com/DariaWagner/python-oop-basics)"
)

st.divider()

st.write("Diese Seite dient als **strukturierte OOP-Demo** ohne Datenanalyse.")
