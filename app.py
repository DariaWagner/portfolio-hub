import streamlit as st

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
# Custom CSS für modernes Design
# =========================
st.markdown("""
<style>
    /* Hauptcontainer */
    .main {
        padding: 2rem;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        line-height: 1.6;
    }

    /* Info Cards */
    .info-card {
        background: white;
        padding: 2rem;
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

    /* Method Cards */
    .method-card {
        background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        height: 100%;
        transition: all 0.3s ease;
    }

    .method-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }

    .method-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .method-divider {
        height: 3px;
        background: linear-gradient(to right, #667eea, #764ba2);
        border: none;
        border-radius: 2px;
        margin: 1rem 0 1.5rem 0;
    }

    .method-section {
        margin-bottom: 1.5rem;
    }

    .method-section h4 {
        color: #495057;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .method-list {
        list-style: none;
        padding-left: 0;
    }

    .method-list li {
        padding: 0.4rem 0 0.4rem 1.5rem;
        position: relative;
        color: #6c757d;
        line-height: 1.6;
    }

    .method-list li:before {
        content: "▸";
        position: absolute;
        left: 0;
        color: #667eea;
        font-weight: bold;
    }

    .method-description {
        color: #6c757d;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    .method-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #667eea;
        color: white;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
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

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    /* Custom Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    st.markdown("""
    Nutzen Sie die Seitenleiste, um zwischen den verschiedenen Analyseansätzen zu navigieren.
    """)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    st.markdown("### 💻 Technologie-Stack")
    st.markdown("""
    <div style='margin-top: 1rem;'>
        <span class='tech-badge'>Python 3.10+</span>
        <span class='tech-badge'>Pandas 2.1</span>
        <span class='tech-badge'>Plotly 5.x</span>
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
# Einleitung
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
# Über das Projekt
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
        <p style='line-height: 1.8; color: #495057;'>
            Durch die Kombination aus technischem Verständnis und analytischem Denken 
            schaffe ich datengetriebene Lösungen für komplexe betriebliche Herausforderungen.
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
        <p style='line-height: 1.8; color: #495057; margin-top: 1rem;'>
            Alle Datensätze sind synthetisch generiert und simulieren realistische 
            industrielle Produktionsszenarien ohne sensible Informationen.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Analyse-Methoden
# =========================
st.markdown("<h2 class='section-header'>🔬 Drei Perspektiven – Ein Datensatz</h2>", unsafe_allow_html=True)

method_col1, method_col2, method_col3 = st.columns(3)

# Pandas Card
with method_col1:
    st.markdown("""
    <div class='method-card'>
        <div class='method-title'>
            <span style='font-size: 1.8rem;'>🐼</span>
            Pandas KPI Dashboard
        </div>
        <hr class='method-divider'>

        <div class='method-section'>
            <h4>✨ Funktionen</h4>
            <ul class='method-list'>
                <li>KPI-Berechnung (Output, Ausschuss, Energie, Stillstand)</li>
                <li>Interaktive Filter (Zeitraum, Linie, Schicht, Produkt)</li>
                <li>Zeitreihen-Analysen & Linienvergleich</li>
                <li>Trendanalysen und Mustererkennungen</li>
            </ul>
        </div>

        <div class='method-section'>
            <h4>📝 Kurzbeschreibung</h4>
            <p class='method-description'>
                Analyse eines Produktionsdatensatzes mit Pandas.
                Fokus auf KPI-Definition, Datenbereinigung und fachlicher Interpretation.
                Ermöglicht schnelle explorative Analysen und flexible Datenauswertung.
            </p>
        </div>

        <span class='method-badge'>➡️ Seite: Production KPIs (Pandas)</span>
    </div>
    """, unsafe_allow_html=True)

# SQL Card
with method_col2:
    st.markdown("""
    <div class='method-card'>
        <div class='method-title'>
            <span style='font-size: 1.8rem;'>🗄️</span>
            SQL Data Analysis
        </div>
        <hr class='method-divider'>

        <div class='method-section'>
            <h4>✨ Funktionen</h4>
            <ul class='method-list'>
                <li>Typische Business-Fragen (z.B. "Welche Linie hat die höchste Ausschussquote?")</li>
                <li>SQL-ähnliche Abfragen (JOINs, GROUP BY, Aggregationen)</li>
                <li>Visualisierung der Ergebnisse</li>
                <li>Strukturierte Datenmodellierung</li>
            </ul>
        </div>

        <div class='method-section'>
            <h4>📝 Kurzbeschreibung</h4>
            <p class='method-description'>
                Simulation einer SQL-Datenanalyse mit relationalem Modell
                (Faktentabelle + Dimensionstabellen).
                Fokus auf Query-Logik und strukturierte Ergebnisdarstellung für Business Intelligence.
            </p>
        </div>

        <span class='method-badge'>➡️ Seite: SQL Data Analysis</span>
    </div>
    """, unsafe_allow_html=True)

# OOP Card
with method_col3:
    st.markdown("""
    <div class='method-card'>
        <div class='method-title'>
            <span style='font-size: 1.8rem;'>⚙️</span>
            OOP Produktionsanalyse
        </div>
        <hr class='method-divider'>

        <div class='method-section'>
            <h4>✨ Architektur</h4>
            <p class='method-description' style='margin-bottom: 0.8rem;'>
                <strong>ProductionDataProcessor</strong><br>
                → Lädt Rohdaten, bereinigt sie und führt Typkonvertierungen durch.
            </p>
            <p class='method-description' style='margin-bottom: 0.8rem;'>
                <strong>KPIBuilder</strong><br>
                → Berechnet KPIs wie Ausschussquote, OEE, Stillstandszeiten und Durchlaufzeiten.
            </p>
            <p class='method-description' style='margin-bottom: 0.8rem;'>
                <strong>ReportGenerator</strong><br>
                → Aggregiert Ergebnisse, erstellt Tabellen und Visualisierungen für das Dashboard.
            </p>
        </div>

        <div class='method-section'>
            <h4>📝 Kurzbeschreibung</h4>
            <p class='method-description'>
                Diese Struktur simuliert eine realistische Trennung von Datenlogik, 
                Analyse und Reporting. Ermöglicht modulare, wartbare und skalierbare Analysepipelines.
            </p>
        </div>

        <span class='method-badge'>➡️ Seite: OOP Produktionsanalyse</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Methodenvergleich
# =========================
st.markdown("<h2 class='section-header'>📊 Methodenvergleich</h2>", unsafe_allow_html=True)

comparison_data = {
    "Kriterium": ["Lernkurve", "Entwicklungsgeschwindigkeit", "Skalierbarkeit", "Wartbarkeit", "Performance",
                  "Team-Eignung"],
    "Pandas": ["Mittel", "Sehr hoch", "Mittel", "Mittel", "Hoch", "Data Scientists"],
    "SQL": ["Niedrig", "Hoch", "Hoch", "Hoch", "Sehr hoch", "Analysten & Engineers"],
    "OOP": ["Hoch", "Mittel", "Sehr hoch", "Sehr hoch", "Hoch", "Software Engineers"]
}

import pandas as pd

df_comparison = pd.DataFrame(comparison_data)

st.dataframe(
    df_comparison,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Kriterium": st.column_config.TextColumn("Kriterium", width="medium"),
        "Pandas": st.column_config.TextColumn("🐼 Pandas", width="medium"),
        "SQL": st.column_config.TextColumn("🗄️ SQL", width="medium"),
        "OOP": st.column_config.TextColumn("⚙️ OOP", width="medium"),
    }
)

# =========================
# Call to Action
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2.5rem; border-radius: 15px; color: white; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);'>
    <h2 style='margin-bottom: 1rem; font-size: 1.8rem;'>🚀 Bereit für die Analyse?</h2>
    <p style='font-size: 1.1rem; opacity: 0.95; margin-bottom: 1.5rem; line-height: 1.6;'>
        Wählen Sie in der Seitenleiste eine Analyse-Methode aus und erkunden Sie die verschiedenen 
        Perspektiven auf denselben Produktionsdatensatz. Jeder Ansatz bietet einzigartige Einblicke 
        und demonstriert unterschiedliche analytische Kompetenzen.
    </p>
    <p style='font-size: 0.95rem; opacity: 0.85;'>
        💡 Tipp: Beginnen Sie mit dem Pandas-Dashboard für einen ersten Überblick
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
    Keine realen Produktionsdaten.
    """)
