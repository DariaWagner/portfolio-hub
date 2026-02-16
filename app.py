"""
Daria Wagner - Interaktiver Magazin-Lebenslauf  
Portfolio & CV - FINALE VERSION
"""

import streamlit as st
from datetime import datetime

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Bewerbung",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
    .main {
        background-color: #1a1d23;
    }
    
    .cover-container {
        background: linear-gradient(135deg, #F4A58A 0%, #ED8F7C 100%);
        padding: 4rem 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    
    .cover-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    
    .cover-subtitle {
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    
    .page-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: black;
    }
    
    .timeline-item {
        background: #f7f7f7;
        padding: 1rem;
        margin: 0.8rem 0;
        border-left: 4px solid #F4A58A;
        border-radius: 6px;
    }
    
    .section-title {
        color: #F4A58A;
        font-size: 1.8rem;
        font-weight: 600;
        border-bottom: 3px solid #F4A58A;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    .page-nav {
        background: #2d3035;
        padding: 1rem;
        border-radius: 6px;
        color: white;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Session State
# =========================
if "page" not in st.session_state:
    st.session_state.page = 0

def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_to_page(page_num):
    st.session_state.page = page_num

# =========================
# Sidebar Navigation
# =========================
# Titel in Sidebar (ersetzt "app")
st.sidebar.markdown("# 📘 Bewerbung")
st.sidebar.markdown("---")

with st.sidebar:
    st.markdown("## 📘 Navigation")
    
    if st.button("📄 Cover", use_container_width=True):
        go_to_page(0)
    if st.button("👤 Über mich", use_container_width=True):
        go_to_page(1)
    if st.button("📅 Werdegang", use_container_width=True):
        go_to_page(2)
    if st.button("🎯 Kompetenzen", use_container_width=True):
        go_to_page(3)
    if st.button("📜 Zertifikate", use_container_width=True):
        go_to_page(4)
    if st.button("💼 Projekt", use_container_width=True):
        go_to_page(5)
    if st.button("📊 Portfolio", use_container_width=True):
        go_to_page(6)
    
    st.markdown("---")
    st.markdown("### 📥 Downloads")
    
    # Lebenslauf PDF laden
    try:
        with open("Lebenslauf_Daria_Wagner.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button("📄 Lebenslauf", data=pdf_data, file_name="Lebenslauf_Daria_Wagner.pdf", mime="application/pdf")
    except:
        st.info("📄 Lebenslauf-PDF bitte als 'Lebenslauf_Daria_Wagner.pdf' im Hauptordner ablegen")

# =========================
# PAGE 0: COVER
# =========================
if st.session_state.page == 0:
    st.markdown("""
    <div class='cover-container'>
        <div class='cover-title'>DARIA WAGNER</div>
        <div class='cover-subtitle'>Fachinformatikerin für</div>
        <div class='cover-subtitle'>Data & Process Analytics</div>
        <p style='font-size: 1.1rem; margin: 1rem 0;'>Portfolio • Lebenslauf • Praxisprojekt</p>
        <p style='font-size: 0.9rem; margin-top: 2rem; opacity: 0.9;'>Praktikum: 01.06.2026 – 02.04.2027</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PAGE 1: ÜBER MICH
# =========================
elif st.session_state.page == 1:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Über mich</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Foto aus assets
        try:
            st.image("assets/portrait.JPG", width=260)
        except:
            st.markdown("""
            <div style='width: 260px; height: 260px; border-radius: 50%; 
                        background: linear-gradient(135deg, #F4A58A 0%, #ED8F7C 100%);
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-size: 4rem; margin: 0 auto 2rem auto;'>
                👤
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Kontakt")
        st.write("**📍 Ort:** Verl, NRW")
        st.write("**📧 Email:** dariawag.aw@gmail.com")

    with col2:
        st.markdown("### Meine Geschichte")
        
        st.write("""
        Zur Zeit befinde ich mich in der Umschulung zur Fachinformatikerin für Daten- und 
        Prozessanalyse und verbinde meine praktische Produktionserfahrung mit moderner 
        Datenanalyse.
        """)
        
        st.write("""
        Mein beruflicher Weg führte mich von Russland nach Deutschland, wo ich bei 
        Beckhoff Automation wertvolle Einblicke in industrielle Abläufe und Qualitätssicherung 
        gewann.
        """)
        
        st.write("""
        Heute nutze ich dieses Praxiswissen, um Produktions- und Prozessdaten so aufzubereiten, 
        dass daraus fundierte und verständliche Entscheidungen entstehen.
        """)
        
        st.info("🎯 **Was mich antreibt:** Daten in verständliche Insights zu verwandeln und damit Prozesse messbar zu verbessern.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PAGE 2: WERDEGANG (VOLLSTÄNDIG AUS PDF)
# =========================
elif st.session_state.page == 2:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Beruflicher Werdegang</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Umschulung
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**08/2025 – HEUTE**")
        st.markdown("### Umschulung Fachinformatikerin")
        st.markdown("*Institut für berufliche Bildung, Münster*")
        st.write("**Praxisprojekt – Produktionsdatenanalyse**")
        st.write("• Datenanalyse mit Python, SQL")
        st.write("• KPI-Berechnung, Prozessoptimierung")
        st.write("• Scrum/Kanban, DSGVO")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sprachkurs
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**05/2025 – 07/2025**")
        st.markdown("### Wirtschaftsenglisch B1")
        st.markdown("*Institut für berufliche Bildung, Münster*")
        st.write("Erfolgreich teilgenommen")
        st.write("• Business-Kommunikation")
        st.write("• Technischer Wortschatz")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Beckhoff
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/2021 – 12/2024**")
        st.markdown("### Produktionshelferin")
        st.markdown("*Beckhoff Automation GmbH & Co. KG, Verl*")
        st.write("*eingesetzt über Piening GmbH bis 12/2022*")
        st.write("• Montage")
        st.write("• Sicht- und Funktionskontrolle")
        st.write("• Sicherheitsvorschriften")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Elternzeit
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/2017 – 09/2021**")
        st.markdown("### Eltern- und Erziehungszeit")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Interstaff
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**06/2016 – 09/2017**")
        st.markdown("### Produktionshelferin")
        st.markdown("*Interstaff GmbH, Rietberg*")
        st.write("• Kunststoffbearbeitung")
        st.write("• Erstkontrolle")
        st.write("• Elektrogeräte")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Reinigungskraft
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**03/2015 – 05/2016**")
        st.markdown("### Reinigungskraft")
        st.markdown("*Horst Scheitzke Gebäudereinigung, Bad Salzuflen*")
        st.write("• Büro- und Produktionsflächen")
        st.write("• Sanitär- und Maschinenräume")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Integrationskurs
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/2013 – 06/2014**")
        st.markdown("### Deutsch- und Integrationskurs")
        st.markdown("*VHS, Lemgo*")
        st.write("Erfolgreich mit B1-Niveau")
        st.write("• Sprachliche Integration")
        st.write("• Schriftlicher Ausdruck")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Russland
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/2008 – 09/2012**")
        st.markdown("### Beruflicher Werdegang in Russland")
        st.markdown("*Volgograd, Russland*")
        st.write("• Kindersanatorium")
        st.write("• Einzelhandel")
        st.write("• Kundenservice")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Studium
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/2005 – 09/2009**")
        st.markdown("### Wirtschaftsstudium")
        st.markdown("*Russische Staatsuniversität, Moskau*")
        st.write("Angewandte Informatik in der Ökonomik")
        st.write("**Anerkannt als Fachgebundene Hochschulreife**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mittelschule
        st.markdown("<div class='timeline-item'>", unsafe_allow_html=True)
        st.markdown("**09/1994 – 06/2005**")
        st.markdown("### Mittelschule № 13")
        st.markdown("*Balakowo, Russland*")
        st.write("Abschlussnote: 2,5")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PAGE 3: KOMPETENZEN
# =========================
elif st.session_state.page == 3:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Kompetenzen & Skills</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### Core Skills")
        st.write("• Python")
        st.write("• SQL")
        st.write("• Power BI")
        st.write("• Prozessanalyse")
        st.write("• KPI-Logik")
    
    with col2:
        st.markdown("### Tools")
        st.write("• Pandas & NumPy")
        st.write("• Matplotlib")
        st.write("• Streamlit")
        st.write("• Git & GitHub")
        st.write("• MS Office")
    
    with col3:
        st.markdown("### Methoden")
        st.write("• Scrum/Kanban")
        st.write("• DSGVO Basics")
        st.write("• OOP-Design")
        st.write("• Data Analytics")
        st.write("• Reporting")
    
    with col4:
        st.markdown("### Soft Skills")
        st.write("• Zuverlässigkeit")
        st.write("• Teamarbeit")
        st.write("• Kommunikation")
        st.write("• Belastbarkeit")
        st.write("• Kreativität")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌍 Sprachen")
        st.write("**Russisch:** Muttersprache")
        st.write("**Deutsch:** B2 (Zertifikat 24.01.2026)")
        st.write("**Englisch:** B1 (Wirtschaftsenglisch)")
    
    with col2:
        st.markdown("### 🚗 Mobilität")
        st.write("**Führerschein:** Klasse B")
        st.write("**Eigener PKW:** Vorhanden")
    
    with col3:
        st.markdown("### 💡 Interessen")
        st.write("• Reisen & Kulturen")
        st.write("• Lesen & Lernen")
        st.write("• Garten & Natur")
        st.write("• Tech & Innovation")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PAGE 4: ZERTIFIKATE (MIT DOWNLOAD-LINKS)
# =========================
elif st.session_state.page == 4:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Zertifikate & Qualifikationen</h1>", unsafe_allow_html=True)
    
    st.info("💡 **Hinweis:** Lege deine Zertifikate als PDF im `assets/` Ordner ab, um sie downloadbar zu machen.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📜 Deutsch B2")
        st.write("**Datum:** 24.01.2026")
        st.write("Deutsch-Test für Zuwanderer")
        st.write("*Ergebnis: Ende Februar*")
        try:
            with open("assets/zertifikat_deutsch_b2.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="Deutsch_B2_Zertifikat.pdf", 
                                 mime="application/pdf", key="cert1")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
        
        st.markdown("---")
        
        st.markdown("### 🇬🇧 Wirtschaftsenglisch B1.1")
        st.write("**Datum:** 19.05 - 13.06.2025")
        st.write("200 Stunden")
        st.write("Business Communication")
        try:
            with open("assets/zertifikat_english_b11.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="Englisch_B11_Zertifikat.pdf",
                                 mime="application/pdf", key="cert2")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
    
    with col2:
        st.markdown("### 🇬🇧 Wirtschaftsenglisch B1.2")
        st.write("**Datum:** 16.06 - 11.07.2025")
        st.write("200 Stunden")
        st.write("Advanced Business English")
        try:
            with open("assets/zertifikat_english_b12.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="Englisch_B12_Zertifikat.pdf",
                                 mime="application/pdf", key="cert3")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
        
        st.markdown("---")
        
        st.markdown("### 💻 Digitale Arbeitswelt 4.0")
        st.write("**Datum:** 19.05 - 17.07.2025")
        st.write("Lernen in virtuellen Teams")
        try:
            with open("assets/zertifikat_digital.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="Digital_4.0_Zertifikat.pdf",
                                 mime="application/pdf", key="cert4")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
    
    with col3:
        st.markdown("### 📊 Leistungsübersicht VIONA")
        st.write("**Stand:** 28.01.2026")
        st.write("**Durchschnittsnote: 1,2**")
        try:
            with open("assets/zertifikat_viona.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="VIONA_Leistungsuebersicht.pdf",
                                 mime="application/pdf", key="cert5")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
        
        st.markdown("---")
        
        st.markdown("### 🎓 Fachgebundene Hochschulreife")
        st.write("**Jahr:** 2016")
        st.write("Anerkannt in Deutschland")
        st.write("Wirtschaftsstudium Russland")
        try:
            with open("assets/zertifikat_hochschulreife.pdf", "rb") as f:
                st.download_button("📄 Zertifikat herunterladen", f, file_name="Hochschulreife_Anerkennung.pdf",
                                 mime="application/pdf", key="cert6")
        except:
            st.warning("📄 Zertifikat noch nicht verfügbar")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PAGE 5: PROJEKT (DUNKLE SCHRIFT)
# =========================
elif st.session_state.page == 5:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Praxisprojekt</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #F4A58A 0%, #ED8F7C 100%); 
                padding: 1.5rem; border-radius: 8px; color: white; margin-bottom: 2rem;'>
        <h2 style='margin: 0;'>Data & Process Analytics Portfolio</h2>
        <p style='margin: 0.5rem 0 0 0; font-size: 1.05rem;'>
            Interaktive Analyse von Produktions- und Prozessdaten
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Projektziel")
        st.write("""
        Entwicklung eines Analyse-Portfolios zur strukturierten Auswertung, 
        Interpretation und Visualisierung von Produktionsdaten.
        """)
        
        st.markdown("### 💻 Technologien")
        st.write("• **Python:** Pandas, NumPy, Matplotlib, Plotly")
        st.write("• **SQL-Denkweise:** Relationale Datenmodellierung")
        st.write("• **Streamlit:** Interaktive Dashboards")
        st.write("• **Git & GitHub:** Versionskontrolle")
        st.write("• **OOP:** Saubere Architektur")
    
    with col2:
        st.markdown("### 📋 Projektinhalt")
        
        st.markdown("""
        <div style='background: #e3f2fd; padding: 1rem; border-radius: 6px; 
                    margin: 0.5rem 0; border-left: 3px solid #1976d2;'>
            <strong style='color: #1976d2;'>1. Datenaufbereitung</strong><br>
            <span style='color: #333;'>Import, Bereinigung und Qualitätsprüfung</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #e8f5e9; padding: 1rem; border-radius: 6px; 
                    margin: 0.5rem 0; border-left: 3px solid #388e3c;'>
            <strong style='color: #388e3c;'>2. KPI-Berechnung</strong><br>
            <span style='color: #333;'>Ableitung relevanter KPIs</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #fff3e0; padding: 1rem; border-radius: 6px; 
                    margin: 0.5rem 0; border-left: 3px solid #f57c00;'>
            <strong style='color: #f57c00;'>3. OOP-Programmierung</strong><br>
            <span style='color: #333;'>Kapselung der Business-Logik</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #f3e5f5; padding: 1rem; border-radius: 6px; 
                    margin: 0.5rem 0; border-left: 3px solid #7b1fa2;'>
            <strong style='color: #7b1fa2;'>4. Visualisierung</strong><br>
            <span style='color: #333;'>Grafana-Style Dashboard</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Ergebnis")
    st.success("✅ Voll funktionsfähiges Analyse-Portfolio")
    st.success("✅ Interaktive Dashboards im Browser")
    st.success("✅ Klare Trennung von Daten, Logik und Visualisierung")
    st.success("✅ Übertragbar auf reale Produktionsprozesse")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PAGE 6: PORTFOLIO (MIT ERKL ÄRUNG)
# =========================
elif st.session_state.page == 6:
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='section-title'>Portfolio Dashboard</h1>", unsafe_allow_html=True)
    
    st.markdown("### 🚀 Interaktives Analytics Dashboard")
    
    st.write("""
    Mein Portfolio zeigt drei verschiedene Analyse-Methoden für denselben Produktionsdatensatz.
    """)
    
    st.info("""
    **💡 Navigation zum Portfolio:**  
    Verwenden Sie das **Hauptmenü oben links** (☰), um zu den Portfolio-Seiten zu navigieren:
    - **Home** - Hauptübersicht mit Sticky Notes
    - **Production KPIs Pandas** - Pandas Dashboard
    - **SQL Data Analysis** - SQL Analyse
    - **OOP Produktionsanalyse** - OOP Design
    """)
    
    st.markdown("### 📊 Drei Analyse-Perspektiven")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Drei farbige Info-Boxen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1.5rem; border-radius: 8px; border-left: 4px solid #1976d2; 
                    min-height: 180px;'>
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 1rem;'>🐼</div>
            <h3 style='color: #1976d2; text-align: center; margin: 0 0 0.5rem 0;'>Pandas Dashboard</h3>
            <p style='color: #333; text-align: center; margin: 0; font-size: 0.9rem;'>
                Explorative Datenanalyse mit Pandas & Matplotlib
            </p>
            <p style='text-align: center; margin-top: 1rem; color: #1976d2; font-weight: 600; font-size: 0.85rem;'>
                → Production KPIs Pandas
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                    padding: 1.5rem; border-radius: 8px; border-left: 4px solid #388e3c; 
                    min-height: 180px;'>
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 1rem;'>🗄️</div>
            <h3 style='color: #388e3c; text-align: center; margin: 0 0 0.5rem 0;'>SQL Analysis</h3>
            <p style='color: #333; text-align: center; margin: 0; font-size: 0.9rem;'>
                Business Intelligence mit SQL-Denkweise
            </p>
            <p style='text-align: center; margin-top: 1rem; color: #388e3c; font-weight: 600; font-size: 0.85rem;'>
                → SQL Data Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    padding: 1.5rem; border-radius: 8px; border-left: 4px solid #f57c00; 
                    min-height: 180px;'>
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 1rem;'>⚙️</div>
            <h3 style='color: #f57c00; text-align: center; margin: 0 0 0.5rem 0;'>OOP Design</h3>
            <p style='color: #333; text-align: center; margin: 0; font-size: 0.9rem;'>
                Enterprise Architecture mit OOP
            </p>
            <p style='text-align: center; margin-top: 1rem; color: #f57c00; font-weight: 600; font-size: 0.85rem;'>
                → OOP Produktionsanalyse
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.success("""
    **✨ Portfolio Features:**
    - Interaktive Grafana-Style Dashboards
    - Drei verschiedene Analyse-Methoden
    - Live-Datenvisualisierung
    - KPI-Berechnungen in Echtzeit
    - Professionelle Reporting-Struktur
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Navigation Controls
# =========================
st.markdown("<div class='page-nav'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.session_state.page > 0:
        st.button("⬅️ Zurück", on_click=prev_page, use_container_width=True)

with col2:
    st.markdown(f"**Seite {st.session_state.page + 1} von 7**")

with col3:
    if st.session_state.page < 6:
        st.button("Weiter ➡️", on_click=next_page, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; padding: 1rem;'>
    <p><strong>Daria Wagner</strong> • Data & Process Analytics</p>
    <p>dariawag.aw@gmail.com</p>
</div>
""", unsafe_allow_html=True)
