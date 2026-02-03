import streamlit as st
import pandas as pd

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Data & Process Analytics Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Custom CSS - Kompakte Sticky Notes
# =========================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        line-height: 1.6;
    }

    /* Info Cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }

    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    /* Kompakte Sticky Notes */
    .sticky-note-compact {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        padding: 1.3rem;
        border-radius: 3px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        border-left: 3px solid #fbc02d;
        position: relative;
        min-height: 280px;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }

    .sticky-note-compact::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0 30px 30px 0;
        border-color: transparent #f9a825 transparent transparent;
    }

    .sticky-note-compact:hover {
        transform: translateY(-3px) rotate(-0.5deg);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }

    /* Pandas (Blau) */
    .sticky-note-compact.pandas {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 3px solid #1976d2;
    }

    .sticky-note-compact.pandas::before {
        border-color: transparent #1565c0 transparent transparent;
    }

    /* SQL (Grün) */
    .sticky-note-compact.sql {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 3px solid #388e3c;
    }

    .sticky-note-compact.sql::before {
        border-color: transparent #2e7d32 transparent transparent;
    }

    /* OOP (Orange) */
    .sticky-note-compact.oop {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 3px solid #f57c00;
    }

    .sticky-note-compact.oop::before {
        border-color: transparent #e65100 transparent transparent;
    }

    .sticky-title-compact {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sticky-content-compact {
        color: #34495e;
        line-height: 1.6;
        font-size: 0.9rem;
    }

    .sticky-content-compact h4 {
        color: #2c3e50;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .sticky-content-compact ul {
        list-style: none;
        padding-left: 0;
        margin-bottom: 0.8rem;
    }

    .sticky-content-compact li {
        padding: 0.25rem 0 0.25rem 1.2rem;
        position: relative;
        font-size: 0.85rem;
    }

    .sticky-content-compact li:before {
        content: "▸";
        position: absolute;
        left: 0;
        font-weight: bold;
        color: #667eea;
    }

    .sticky-content-compact p {
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0.3rem 0;
    }

    .sticky-badge-compact {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background: rgba(0,0,0,0.1);
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }

    /* Stat Box */
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-top: 3px solid #667eea;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.3rem;
    }

    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Tech Badges */
    .tech-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        margin: 0.3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }

    /* Custom Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
    }

    /* Code Window */
    .code-window {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 0;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        overflow: hidden;
    }

    .code-header {
        background: #323232;
        padding: 0.8rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid #444;
    }

    .code-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    .code-dot.red { background: #ff5f56; }
    .code-dot.yellow { background: #ffbd2e; }
    .code-dot.green { background: #27c93f; }

    .code-title {
        color: #a0a0a0;
        font-size: 0.85rem;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    st.markdown("Nutzen Sie die Seitenleiste, um zwischen den verschiedenen Analyseansätzen zu navigieren.")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    st.markdown("### 💻 Technologie-Stack")
    st.markdown("""
    <div style='margin-top: 1rem;'>
        <span class='tech-badge'>Python 3.10+</span>
        <span class='tech-badge'>Pandas 2.1</span>
        <span class='tech-badge'>Plotly</span>
        <span class='tech-badge'>Streamlit</span>
        <span class='tech-badge'>NumPy</span>
        <span class='tech-badge'>SQLite</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    st.markdown("### 📚 Kompetenzen")
    st.markdown("""
    - **Datenanalyse & -visualisierung**
    - **KPI-Definition & Reporting**
    - **Prozessoptimierung**
    - **SQL & Datenbanken**
    - **Python-Entwicklung**
    - **OOP & Software-Design**
    """)

# =========================
# Hero Section
# =========================
st.markdown("""
<div class='hero-section'>
    <div class='hero-title'>📊 Data & Process Analytics Portfolio</div>
    <div class='hero-subtitle'>
        Professionelle Analyse industrieller Produktionsdaten mit modernen Data-Science-Methoden
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Statistiken
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>3</div>
        <div class='stat-label'>Analyse-Methoden</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>100%</div>
        <div class='stat-label'>Synthetische Daten</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>∞</div>
        <div class='stat-label'>Skalierbarkeit</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Projektüberblick
# =========================
st.markdown("<h2 class='section-header'>🎯 Projektüberblick</h2>", unsafe_allow_html=True)

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    <div class='info-card'>
        <h3 style='color: #667eea; margin-bottom: 1rem;'>🎓 Über mich</h3>
        <p style='line-height: 1.8; color: #495057;'>
            Als angehender <strong>Data & Process Analyst</strong> befinde ich mich aktuell in einer 
            praxisorientierten Umschulung. Mein Fokus liegt auf der strukturierten Analyse von 
            Produktions- und Prozessdaten, der Entwicklung aussagekräftiger KPIs sowie der 
            Identifikation von Optimierungspotenzialen.
        </p>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div class='info-card'>
        <h3 style='color: #764ba2; margin-bottom: 1rem;'>📋 Projektziel</h3>
        <p style='line-height: 1.8; color: #495057;'>
            Dieses Portfolio demonstriert die <strong>methodische Vielfalt</strong> in der Datenanalyse. 
            Ein identischer Produktionsdatensatz wird mit drei komplementären Ansätzen untersucht:
        </p>
        <ul style='line-height: 1.8; color: #495057;'>
            <li><strong>Explorativ</strong> – Schnelle Insights mit Pandas</li>
            <li><strong>Strukturiert</strong> – Business Intelligence mit SQL</li>
            <li><strong>Skalierbar</strong> – Enterprise-ready mit OOP</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Kompakte Sticky Notes
# =========================
st.markdown("<h2 class='section-header'>📝 Drei Perspektiven – Ein Datensatz</h2>", unsafe_allow_html=True)

method_col1, method_col2, method_col3 = st.columns(3)

# Pandas Note
with method_col1:
    st.markdown("""
    <div class='sticky-note-compact pandas'>
        <div class='sticky-title-compact'>
            <span style='font-size: 1.5rem;'>🐼</span>
            Pandas Dashboard
        </div>
        <div class='sticky-content-compact'>
            <h4>✨ Features</h4>
            <ul>
                <li>KPI-Berechnung & Filter</li>
                <li>Zeitreihen-Analysen</li>
                <li>Interaktive Visualisierungen</li>
            </ul>
            <h4>📝 Fokus</h4>
            <p>Explorative Datenanalyse mit schnellen Insights und flexibler Auswertung.</p>
            <span class='sticky-badge-compact'>➡️ Production KPIs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_pandas = st.checkbox("💻 Code", key="pandas")
    if show_pandas:
        st.markdown("""<div class='code-window'><div class='code-header'>
            <span class='code-dot red'></span><span class='code-dot yellow'></span><span class='code-dot green'></span>
            <span class='code-title'>pandas_analysis.py</span></div></div>""", unsafe_allow_html=True)
        st.code("""# Pandas KPI Dashboard
import pandas as pd

df = load_production_data()
kpi = df.groupby("Produktionslinie").agg({
    "Stueckzahl": "sum",
    "Ausschuss": "sum"
}).reset_index()
kpi["Ausschussquote_%"] = (kpi["Ausschuss"] / kpi["Stueckzahl"] * 100).round(2)
""", language="python")

# SQL Note
with method_col2:
    st.markdown("""
    <div class='sticky-note-compact sql'>
        <div class='sticky-title-compact'>
            <span style='font-size: 1.5rem;'>🗄️</span>
            SQL Analysis
        </div>
        <div class='sticky-content-compact'>
            <h4>✨ Features</h4>
            <ul>
                <li>SQL-ähnliche Abfragen</li>
                <li>Relationales Datenmodell</li>
                <li>Business Intelligence</li>
            </ul>
            <h4>📝 Fokus</h4>
            <p>Strukturierte Analysen mit Dimensionstabellen und Query-Logik.</p>
            <span class='sticky-badge-compact'>➡️ SQL Data Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_sql = st.checkbox("💻 Code", key="sql")
    if show_sql:
        st.markdown("""<div class='code-window'><div class='code-header'>
            <span class='code-dot red'></span><span class='code-dot yellow'></span><span class='code-dot green'></span>
            <span class='code-title'>sql_analysis.py</span></div></div>""", unsafe_allow_html=True)
        st.code("""# SQL Data Analysis
import pandas as pd

# Dimensionstabellen
dim_linie = df[["Produktionslinie"]].drop_duplicates()
dim_linie["linie_id"] = dim_linie.index + 1

# Faktentabelle
fact = df.merge(dim_linie, on="Produktionslinie")
kpi = fact.groupby("linie_id").agg({"Stueckzahl": "sum"})
""", language="python")

# OOP Note
with method_col3:
    st.markdown("""
    <div class='sticky-note-compact oop'>
        <div class='sticky-title-compact'>
            <span style='font-size: 1.5rem;'>⚙️</span>
            OOP Design
        </div>
        <div class='sticky-content-compact'>
            <h4>✨ Features</h4>
            <ul>
                <li>Modulare Klassenstruktur</li>
                <li>SOLID-Prinzipien</li>
                <li>Skalierbare Architektur</li>
            </ul>
            <h4>📝 Fokus</h4>
            <p>Enterprise-ready Code mit Trennung von Daten, Logik und Reporting.</p>
            <span class='sticky-badge-compact'>➡️ OOP Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_oop = st.checkbox("💻 Code", key="oop")
    if show_oop:
        st.markdown("""<div class='code-window'><div class='code-header'>
            <span class='code-dot red'></span><span class='code-dot yellow'></span><span class='code-dot green'></span>
            <span class='code-title'>oop_production.py</span></div></div>""", unsafe_allow_html=True)
        st.code("""# OOP Produktionsanalyse
from dataclasses import dataclass

@dataclass
class ProductionRecord:
    stueckzahl: int
    ausschuss: int

    def scrap_rate(self) -> float:
        return (self.ausschuss / self.stueckzahl * 100)

@dataclass
class ProductionLine:
    name: str
    records: List[ProductionRecord]
""", language="python")

st.divider()

# =========================
# Methodenvergleich
# =========================
st.markdown("<h2 class='section-header'>📊 Methodenvergleich</h2>", unsafe_allow_html=True)

comparison_data = {
    "Kriterium": ["Lernkurve", "Geschwindigkeit", "Skalierbarkeit", "Wartbarkeit", "Performance"],
    "Pandas": ["Mittel", "Sehr hoch", "Mittel", "Mittel", "Hoch"],
    "SQL": ["Niedrig", "Hoch", "Hoch", "Hoch", "Sehr hoch"],
    "OOP": ["Hoch", "Mittel", "Sehr hoch", "Sehr hoch", "Hoch"]
}

df_comparison = pd.DataFrame(comparison_data)
st.dataframe(df_comparison, use_container_width=True, hide_index=True)

# =========================
# Call to Action
# =========================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; color: white; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);'>
    <h2 style='margin-bottom: 1rem; font-size: 1.6rem;'>🚀 Bereit für die Analyse?</h2>
    <p style='font-size: 1rem; opacity: 0.95; margin-bottom: 0;'>
        Wählen Sie in der Seitenleiste eine Analyse-Methode aus und erkunden Sie die verschiedenen 
        Perspektiven auf denselben Produktionsdatensatz.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **📫 Kontakt**  
    Portfolio-Projekt im Rahmen  
    der Data Analytics Umschulung
    """)

with footer_col2:
    st.markdown("""
    **🔗 Ressourcen**  
    - [Pandas Documentation](https://pandas.pydata.org/)
    - [SQL Tutorial](https://www.w3schools.com/sql/)
    - [Python OOP Guide](https://docs.python.org/3/tutorial/classes.html)
    """)

with footer_col3:
    st.markdown("""
    **⚖️ Datenhinweis**  
    Alle verwendeten Datensätze sind  
    vollständig synthetisch generiert.
    """)
