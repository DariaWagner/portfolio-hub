import streamlit as st
from dataclasses import dataclass
from typing import List

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="OOP Bestellverwaltung", layout="wide")

st.title("OOP-Projekt: Bestellverwaltung")
st.write(
    "Diese Seite zeigt ein **objektorientiertes Python-Beispiel**: "
    "ein Bestellprozess mit Klassen, Beziehungen und Business-Logik."
)
st.divider()

# --------------------------------------------------
# 1) Mini-Klassenmodell (kurz)
# --------------------------------------------------
st.header("Mini-Klassenmodell (Übersicht)")

st.markdown(
    """
    - **Produkt**: Name, Preis  
    - **Bestellposition**: Produkt + Menge  
    - **Bestellung**: Liste von Positionen, berechnet Summe  
    - **Zahlung**: Zahlungsart + Status (vereinfacht)
    """
)

st.divider()

# --------------------------------------------------
# 2) Live-Demo: “Ergebnis zeigen”
# --------------------------------------------------
st.header("Live-Demo: Bestellung berechnen")

# --- Demo-Klassen (klein, aber „echt“)
@dataclass(frozen=True)
class Produkt:
    name: str
    preis: float

@dataclass
class Bestellposition:
    produkt: Produkt
    menge: int

    def positionswert(self) -> float:
        return self.produkt.preis * self.menge

@dataclass
class Bestellung:
    kunde: str
    positionen: List[Bestellposition]

    def gesamtbetrag(self) -> float:
        return sum(p.positionswert() for p in self.positionen)

    def artikelanzahl(self) -> int:
        return sum(p.menge for p in self.positionen)

# --- UI: Beispielprodukte
produkte = [
    Produkt("Apfelsaft", 1.99),
    Produkt("Brot", 2.49),
    Produkt("Käse", 3.79),
]

col1, col2 = st.columns([1, 1])

with col1:
    kunde = st.text_input("Kunde", value="Max Mustermann")
    p1 = st.selectbox("Produkt 1", produkte, format_func=lambda x: f"{x.name} ({x.preis:.2f}€)")
    m1 = st.number_input("Menge 1", min_value=0, value=2, step=1)

    p2 = st.selectbox("Produkt 2", produkte, index=1, format_func=lambda x: f"{x.name} ({x.preis:.2f}€)")
    m2 = st.number_input("Menge 2", min_value=0, value=1, step=1)

with col2:
    st.subheader("Ergebnis")
    positionen = []
    if m1 > 0:
        positionen.append(Bestellposition(p1, int(m1)))
    if m2 > 0:
        positionen.append(Bestellposition(p2, int(m2)))

    bestellung = Bestellung(kunde=kunde, positionen=positionen)

    st.metric("Artikel (gesamt)", bestellung.artikelanzahl())
    st.metric("Gesamtbetrag", f"{bestellung.gesamtbetrag():.2f} €")

    if positionen:
        st.write("Positionen:")
        for pos in positionen:
            st.write(f"- {pos.produkt.name} × {pos.menge} = {pos.positionswert():.2f} €")
    else:
        st.info("Wähle mindestens eine Menge > 0.")

st.divider()

# --------------------------------------------------
# 3) Code-Beispiel (kurz & HR-tauglich)
# --------------------------------------------------
st.header("Code-Beispiel (Ausschnitt)")

st.code(
    """@dataclass
class Bestellposition:
    produkt: Produkt
    menge: int

    def positionswert(self) -> float:
        return self.produkt.preis * self.menge

@dataclass
class Bestellung:
    kunde: str
    positionen: List[Bestellposition]

    def gesamtbetrag(self) -> float:
        return sum(p.positionswert() for p in self.positionen)""",
    language="python",
)

st.divider()

# --------------------------------------------------
# Repo Link
# --------------------------------------------------
st.header("Repository")
st.markdown("[GitHub Repository – python-oop-basics](https://github.com/DariaWagner/python-oop-basics)")
