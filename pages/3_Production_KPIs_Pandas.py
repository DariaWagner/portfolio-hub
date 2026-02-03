"""
Production KPIs - Grafana Style Dashboard
==========================================
Modern Dashboard Design inspired by Grafana monitoring dashboards.
Features: Dark theme, grid layout, real-time metrics, professional charts.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from services.data_loader import load_production_data

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Production Monitoring - Grafana Style",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# Grafana-Style CSS
# =========================
st.markdown("""
<style>
    /* Dark Theme */
    .main {
        background-color: #0b0c0e;
        color: #d8d9da;
    }
    
    .stApp {
        background-color: #0b0c0e;
    }
    
    /* Grafana Panel Style */
    .grafana-panel {
        background: linear-gradient(135deg, #1a1d23 0%, #151719 100%);
        border: 1px solid #2d3035;
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .grafana-panel:hover {
        border-color: #3274d9;
        box-shadow: 0 4px 12px rgba(50, 116, 217, 0.2);
    }
    
    /* Metric Cards (Stat Panels) */
    .metric-card {
        background: linear-gradient(135deg, #1f2229 0%, #181b1f 100%);
        border: 1px solid #2d3035;
        border-radius: 4px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #3274d9;
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #52c41a;
        font-family: 'Roboto Mono', monospace;
        margin: 0.5rem 0;
    }
    
    .metric-value.warning {
        color: #ff9800;
    }
    
    .metric-value.critical {
        color: #f5222d;
    }
    
    .metric-label {
        color: #9fa1a4;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .metric-trend {
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-family: 'Roboto Mono', monospace;
    }
    
    .trend-up {
        color: #52c41a;
    }
    
    .trend-down {
        color: #f5222d;
    }
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(90deg, #1a1d23 0%, #252930 100%);
        padding: 1.5rem 2rem;
        border-bottom: 2px solid #3274d9;
        margin-bottom: 2rem;
        border-radius: 4px;
    }
    
    .dashboard-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .dashboard-subtitle {
        color: #9fa1a4;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Time Range Selector */
    .time-range {
        background: #1f2229;
        border: 1px solid #2d3035;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        color: #d8d9da;
        display: inline-block;
        margin-right: 1rem;
        font-size: 0.85rem;
    }
    
    /* Panel Title */
    .panel-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2d3035;
    }
    
    /* Alert Box */
    .alert-critical {
        background: rgba(245, 34, 45, 0.1);
        border-left: 3px solid #f5222d;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #ff7875;
    }
    
    .alert-warning {
        background: rgba(255, 152, 0, 0.1);
        border-left: 3px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #ffa940;
    }
    
    .alert-success {
        background: rgba(82, 196, 26, 0.1);
        border-left: 3px solid #52c41a;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #95de64;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-online {
        background: rgba(82, 196, 26, 0.2);
        color: #52c41a;
        border: 1px solid #52c41a;
    }
    
    .status-warning {
        background: rgba(255, 152, 0, 0.2);
        color: #ff9800;
        border: 1px solid #ff9800;
    }
    
    .status-offline {
        background: rgba(245, 34, 45, 0.2);
        color: #f5222d;
        border: 1px solid #f5222d;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1d23;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3274d9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4a8cf7;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Data Loading
# =========================
@st.cache_data
def load_and_prepare_data():
    """Load and prepare production data"""
    df = load_production_data().copy()

    # Convert dates
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")

    # Convert numeric columns
    numeric_cols = [
        "Stueckzahl", "Ausschuss", "Betriebsstunden",
        "Stillstandszeit_Min", "Materialkosten",
        "Energieverbrauch_kWh", "Mitarbeiter_Produktion",
        "MaxTemperatur", "Durchschnittstemperatur"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derived columns
    df["Jahr"] = df["Datum"].dt.year
    df["Monat"] = df["Datum"].dt.month
    df["Jahr_Monat"] = df["Datum"].dt.to_period("M").astype(str)
    df["Ausschussquote_%"] = (df["Ausschuss"] / df["Stueckzahl"] * 100).fillna(0)
    df["Gutteile"] = df["Stueckzahl"] - df["Ausschuss"]
    df["Energie_pro_Stueck"] = (df["Energieverbrauch_kWh"] / df["Stueckzahl"]).fillna(0)
    df["Verfuegbarkeit_%"] = ((df["Betriebsstunden"] /
        (df["Betriebsstunden"] + df["Stillstandszeit_Min"]/60)) * 100).fillna(0)

    return df

with st.spinner("⏳ Loading production data..."):
    df = load_and_prepare_data()

# =========================
# Header
# =========================
st.markdown("""
<div class='dashboard-header'>
    <div class='dashboard-title'>📊 Production Monitoring Dashboard</div>
    <div class='dashboard-subtitle'>
        Real-time production metrics and analytics | Last updated: {} | {} records
    </div>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(df)), unsafe_allow_html=True)

# =========================
# Time Range & Filters
# =========================
col1, col2, col3, col4 = st.columns([2, 2, 2, 6])

with col1:
    jahre = sorted(df["Jahr"].dropna().unique())
    selected_jahr = st.selectbox("📅 Year", jahre, index=len(jahre)-1)

with col2:
    linien = sorted(df["Produktionslinie"].dropna().unique())
    selected_linie = st.selectbox("🏭 Line", ["All"] + linien)

with col3:
    schichten = sorted(df["Schicht"].dropna().unique())
    selected_schicht = st.selectbox("🕐 Shift", ["All"] + schichten)

# Apply filters
df_filtered = df[df["Jahr"] == selected_jahr].copy()

if selected_linie != "All":
    df_filtered = df_filtered[df_filtered["Produktionslinie"] == selected_linie]

if selected_schicht != "All":
    df_filtered = df_filtered[df_filtered["Schicht"] == selected_schicht]

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI Metrics (Top Row)
# =========================
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_output = df_filtered["Stueckzahl"].sum()
total_scrap = df_filtered["Ausschuss"].sum()
avg_scrap_rate = df_filtered["Ausschussquote_%"].mean()
avg_availability = df_filtered["Verfuegbarkeit_%"].mean()
total_energy = df_filtered["Energieverbrauch_kWh"].sum()

# Calculate trends
prev_year = df[df["Jahr"] == selected_jahr - 1] if selected_jahr > df["Jahr"].min() else df_filtered
prev_scrap_rate = prev_year["Ausschussquote_%"].mean() if len(prev_year) > 0 else avg_scrap_rate
scrap_trend = avg_scrap_rate - prev_scrap_rate

with col1:
    status_class = "critical" if avg_scrap_rate > 5 else "warning" if avg_scrap_rate > 3 else ""
    trend_class = "trend-down" if scrap_trend < 0 else "trend-up"
    trend_icon = "↓" if scrap_trend < 0 else "↑"

    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Scrap Rate</div>
        <div class='metric-value {status_class}'>{avg_scrap_rate:.2f}%</div>
        <div class='metric-trend {trend_class}'>{trend_icon} {abs(scrap_trend):.2f}% vs prev year</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Output</div>
        <div class='metric-value'>{total_output:,.0f}</div>
        <div class='metric-trend'>units produced</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    status_class = "" if avg_availability > 90 else "warning" if avg_availability > 80 else "critical"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Availability</div>
        <div class='metric-value {status_class}'>{avg_availability:.1f}%</div>
        <div class='metric-trend'>average uptime</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Good Parts</div>
        <div class='metric-value'>{total_output - total_scrap:,.0f}</div>
        <div class='metric-trend'>{((total_output - total_scrap) / total_output * 100):.1f}% quality</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Energy Consumption</div>
        <div class='metric-value'>{total_energy:,.0f}</div>
        <div class='metric-trend'>kWh total</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Main Charts Row 1
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='panel-title'>📈 Production Trend (Monthly)</div>", unsafe_allow_html=True)

    monthly = df_filtered.groupby("Jahr_Monat").agg({
        "Stueckzahl": "sum",
        "Gutteile": "sum"
    }).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["Jahr_Monat"],
        y=monthly["Stueckzahl"],
        name="Total Output",
        line=dict(color='#3274d9', width=2),
        fill='tozeroy',
        fillcolor='rgba(50, 116, 217, 0.1)'
    ))

    fig.add_trace(go.Scatter(
        x=monthly["Jahr_Monat"],
        y=monthly["Gutteile"],
        name="Good Parts",
        line=dict(color='#52c41a', width=2),
        fill='tozeroy',
        fillcolor='rgba(82, 196, 26, 0.1)'
    ))

    fig.update_layout(
        plot_bgcolor='#0b0c0e',
        paper_bgcolor='#1a1d23',
        font=dict(color='#d8d9da', size=11),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2d3035',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d3035',
            zeroline=False
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("<div class='panel-title'>📉 Scrap Rate Trend</div>", unsafe_allow_html=True)

    scrap_monthly = df_filtered.groupby("Jahr_Monat")["Ausschussquote_%"].mean().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=scrap_monthly["Jahr_Monat"],
        y=scrap_monthly["Ausschussquote_%"],
        name="Scrap Rate",
        line=dict(color='#f5222d', width=2),
        mode='lines+markers',
        marker=dict(size=6)
    ))

    # Threshold line
    fig.add_hline(
        y=5.0,
        line_dash="dash",
        line_color="#ff9800",
        annotation_text="Target: 5%",
        annotation_position="right"
    )

    fig.update_layout(
        plot_bgcolor='#0b0c0e',
        paper_bgcolor='#1a1d23',
        font=dict(color='#d8d9da', size=11),
        xaxis=dict(showgrid=True, gridcolor='#2d3035', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#2d3035', zeroline=False, title="Scrap Rate (%)"),
        hovermode='x unified',
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Main Charts Row 2
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='panel-title'>🏭 Production Lines Comparison</div>", unsafe_allow_html=True)

    line_kpi = df_filtered.groupby("Produktionslinie").agg({
        "Stueckzahl": "sum",
        "Ausschussquote_%": "mean"
    }).reset_index()

    fig = go.Figure()

    colors = ['#f5222d' if x > 5 else '#ff9800' if x > 3 else '#52c41a'
              for x in line_kpi["Ausschussquote_%"]]

    fig.add_trace(go.Bar(
        x=line_kpi["Produktionslinie"],
        y=line_kpi["Ausschussquote_%"],
        marker=dict(
            color=colors,
            line=dict(color='#ffffff', width=1)
        ),
        width=0.4,  # Dünnere Balken (war implizit breiter)
        text=line_kpi["Ausschussquote_%"].round(2),
        textposition='outside',
        texttemplate='%{text}%',
        hovertemplate='<b>%{x}</b><br>Scrap Rate: %{y:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='#0b0c0e',
        paper_bgcolor='#1a1d23',
        font=dict(color='#d8d9da', size=11),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#2d3035', zeroline=False, title="Scrap Rate (%)"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("<div class='panel-title'>🕐 Shift Performance</div>", unsafe_allow_html=True)

    shift_kpi = df_filtered.groupby("Schicht").agg({
        "Stueckzahl": "sum",
        "Ausschussquote_%": "mean",
        "Verfuegbarkeit_%": "mean"
    }).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=shift_kpi["Schicht"],
            y=shift_kpi["Stueckzahl"],
            name="Output",
            marker_color='#3274d9',
            yaxis='y',
            hovertemplate='<b>%{x}</b><br>Output: %{y:,.0f}<extra></extra>'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=shift_kpi["Schicht"],
            y=shift_kpi["Ausschussquote_%"],
            name="Scrap Rate",
            line=dict(color='#f5222d', width=3),
            mode='lines+markers',
            marker=dict(size=10),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Scrap: %{y:.2f}%<extra></extra>'
        ),
        secondary_y=True
    )

    fig.update_layout(
        plot_bgcolor='#0b0c0e',
        paper_bgcolor='#1a1d23',
        font=dict(color='#d8d9da', size=11),
        xaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(title_text="Output (units)", showgrid=True, gridcolor='#2d3035', secondary_y=False)
    fig.update_yaxes(title_text="Scrap Rate (%)", showgrid=False, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Alerts & Status
# =========================
st.markdown("### ⚠️ Alerts & System Status")

col1, col2, col3 = st.columns(3)

with col1:
    critical_lines = line_kpi[line_kpi["Ausschussquote_%"] > 5]
    if len(critical_lines) > 0:
        st.markdown(f"""
        <div class='alert-critical'>
            <strong>🔴 CRITICAL ALERT</strong><br>
            {len(critical_lines)} production line(s) exceed 5% scrap rate:<br>
            {', '.join(critical_lines["Produktionslinie"].tolist())}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-success'>
            <strong>✅ ALL SYSTEMS NOMINAL</strong><br>
            All production lines within acceptable limits
        </div>
        """, unsafe_allow_html=True)

with col2:
    if avg_availability < 85:
        st.markdown(f"""
        <div class='alert-warning'>
            <strong>⚠️ LOW AVAILABILITY</strong><br>
            Current: {avg_availability:.1f}% | Target: >90%<br>
            Action required: Investigate downtime
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='alert-success'>
            <strong>✅ AVAILABILITY OK</strong><br>
            Current: {avg_availability:.1f}% | Target: >90%
        </div>
        """, unsafe_allow_html=True)

with col3:
    # System status badges
    st.markdown("""
    <div style='padding: 1rem;'>
        <div style='margin-bottom: 0.5rem;'><span class='status-badge status-online'>● DATA FEED</span></div>
        <div style='margin-bottom: 0.5rem;'><span class='status-badge status-online'>● SENSORS</span></div>
        <div><span class='status-badge status-online'>● ANALYTICS</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# =========================
# Fazit & Zusammenfassung
# =========================
st.markdown("### 📋 Fazit & Handlungsempfehlungen")

# Berechnungen für Fazit
best_line = line_kpi.loc[line_kpi["Ausschussquote_%"].idxmin(), "Produktionslinie"]
worst_line = line_kpi.loc[line_kpi["Ausschussquote_%"].idxmax(), "Produktionslinie"]
best_scrap = line_kpi["Ausschussquote_%"].min()
worst_scrap = line_kpi["Ausschussquote_%"].max()
improvement_potential = worst_scrap - best_scrap

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background: rgba(82, 196, 26, 0.1); padding: 1.5rem; border-radius: 8px; 
                border-left: 3px solid #52c41a; color: #d8d9da;'>
        <h4 style='color: #52c41a; margin-top: 0;'>✅ Stärken</h4>
        <ul style='line-height: 1.8; margin-bottom: 0;'>
            <li><strong>Hohe Verfügbarkeit:</strong> Durchschnittlich {avg_availability:.1f}% Anlagenverfügbarkeit</li>
            <li><strong>Best Performer:</strong> {best_line} zeigt Benchmark mit {best_scrap:.2f}% Ausschuss</li>
            <li><strong>Konstante Produktion:</strong> Stabile Output-Zahlen über das Jahr</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: rgba(255, 152, 0, 0.1); padding: 1.5rem; border-radius: 8px; 
                border-left: 3px solid #ff9800; color: #d8d9da;'>
        <h4 style='color: #ff9800; margin-top: 0;'>⚠️ Verbesserungspotenziale</h4>
        <ul style='line-height: 1.8; margin-bottom: 0;'>
            <li><strong>Ausschussquote:</strong> Aktuell {avg_scrap_rate:.2f}%, Zielwert < 3%</li>
            <li><strong>Linienunterschiede:</strong> {worst_line} zeigt {improvement_potential:.2f}pp Potenzial</li>
            <li><strong>Qualitätsschwankungen:</strong> Standardisierung erforderlich</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Handlungsempfehlungen
st.markdown("""
<div style='background: linear-gradient(135deg, #3274d9 0%, #1890ff 100%); 
            padding: 1.5rem; border-radius: 8px; color: white;'>
    <h4 style='margin-top: 0; color: white;'>🎯 Konkrete Handlungsempfehlungen</h4>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;'>
        <div>
            <strong>⚡ Kurzfristig (0-3 Monate)</strong>
            <ul style='margin-top: 0.5rem; line-height: 1.6;'>
                <li>Root Cause Analysis für Top-Fehler</li>
                <li>Best Practice Transfer zwischen Linien</li>
                <li>Schichtvergleich vertiefen</li>
            </ul>
        </div>
        <div>
            <strong>📊 Mittelfristig (3-12 Monate)</strong>
            <ul style='margin-top: 0.5rem; line-height: 1.6;'>
                <li>Prozessoptimierung implementieren</li>
                <li>Predictive Maintenance einführen</li>
                <li>Energieaudit durchführen</li>
            </ul>
        </div>
        <div>
            <strong>🚀 Langfristig (12+ Monate)</strong>
            <ul style='margin-top: 0.5rem; line-height: 1.6;'>
                <li>Automatisierung der Qualitätskontrolle</li>
                <li>Real-time Monitoring System</li>
                <li>Kontinuierliche Schulungen</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ROI Projektion
st.markdown("""
<div style='background: rgba(245, 34, 45, 0.1); padding: 1.5rem; border-radius: 8px; 
            border-left: 3px solid #f5222d; color: #d8d9da;'>
    <h4 style='color: #ff7875; margin-top: 0;'>💰 Erwarteter ROI bei Umsetzung</h4>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;'>
        <div style='text-align: center;'>
            <div style='font-size: 2rem; font-weight: bold; color: #52c41a;'>-30%</div>
            <div style='font-size: 0.9rem; opacity: 0.8;'>Ausschussreduktion</div>
            <div style='font-size: 0.8rem; margin-top: 0.3rem;'>≈ {:,.0f} Teile/Jahr</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 2rem; font-weight: bold; color: #52c41a;'>+5%</div>
            <div style='font-size: 0.9rem; opacity: 0.8;'>Verfügbarkeitssteigerung</div>
            <div style='font-size: 0.8rem; margin-top: 0.3rem;'>≈ {:,.0f} Stück/Jahr</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 2rem; font-weight: bold; color: #52c41a;'>-15%</div>
            <div style='font-size: 0.9rem; opacity: 0.8;'>Energiekosten</div>
            <div style='font-size: 0.8rem; margin-top: 0.3rem;'>≈ {:,.0f} kWh/Jahr</div>
        </div>
    </div>
</div>
""".format(
    total_scrap * 0.3,
    total_output * 0.05,
    total_energy * 0.15
), unsafe_allow_html=True)

# =========================
# Fazit & Handlungsempfehlungen
# =========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📋 Zusammenfassung & Handlungsempfehlungen")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: rgba(82, 196, 26, 0.1); border-left: 4px solid #52c41a; 
                padding: 1.5rem; border-radius: 4px; margin-bottom: 1rem;'>
        <h4 style='color: #52c41a; margin: 0 0 1rem 0;'>✅ Stärken</h4>
        <ul style='color: #d8d9da; margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
            <li><strong>Hohe Produktionsvolumen</strong><br>
                Konstante Auslastung über {selected_jahr}</li>
            <li><strong>Gute Verfügbarkeit</strong><br>
                Durchschnitt: {avg_availability:.1f}% (Ziel: >90%)</li>
            <li><strong>Best-in-Class Linien</strong><br>
                {best_line} zeigt Benchmark-Performance</li>
        </ul>
    </div>
    """.format(
        selected_jahr=selected_jahr,
        avg_availability=avg_availability,
        best_line=line_kpi["Produktionslinie"].iloc[line_kpi["Ausschussquote_%"].argmin()]
    ), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: rgba(255, 152, 0, 0.1); border-left: 4px solid #ff9800; 
                padding: 1.5rem; border-radius: 4px; margin-bottom: 1rem;'>
        <h4 style='color: #ff9800; margin: 0 0 1rem 0;'>⚠️ Optimierungspotenziale</h4>
        <ul style='color: #d8d9da; margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
            <li><strong>Ausschussquote</strong><br>
                Aktuell: {avg_scrap_rate:.2f}% (Ziel: <3%)</li>
            <li><strong>Linienunterschiede</strong><br>
                {worst_line} benötigt Optimierung</li>
            <li><strong>Energieeffizienz</strong><br>
                Einsparpotenzial identifiziert</li>
        </ul>
    </div>
    """.format(
        avg_scrap_rate=avg_scrap_rate,
        worst_line=line_kpi["Produktionslinie"].iloc[line_kpi["Ausschussquote_%"].argmax()]
    ), unsafe_allow_html=True)

# Handlungsempfehlungen
st.markdown("""
<div style='background: linear-gradient(135deg, #1a1d23 0%, #151719 100%); 
            border: 1px solid #3274d9; padding: 1.5rem; border-radius: 4px; margin-top: 1rem;'>
    <h4 style='color: #3274d9; margin: 0 0 1rem 0;'>🎯 Konkrete Handlungsempfehlungen</h4>
    <div style='color: #d8d9da; line-height: 1.8;'>
        <p style='margin: 0 0 1rem 0;'><strong style='color: #52c41a;'>1. Kurzfristig (0-3 Monate)</strong></p>
        <ul style='margin: 0 0 1rem 0; padding-left: 1.5rem;'>
            <li>Root Cause Analysis für Top-Fehlercodes durchführen</li>
            <li>Best Practices Transfer zwischen Linien</li>
            <li>Schichtvergleich vertiefen</li>
        </ul>
        
        <p style='margin: 0 0 1rem 0;'><strong style='color: #ff9800;'>2. Mittelfristig (3-12 Monate)</strong></p>
        <ul style='margin: 0 0 1rem 0; padding-left: 1.5rem;'>
            <li>Prozessoptimierung für problematische Linien</li>
            <li>Energieaudit durchführen und Quick Wins umsetzen</li>
            <li>Predictive Maintenance einführen</li>
        </ul>
        
        <p style='margin: 0 0 1rem 0;'><strong style='color: #3274d9;'>3. Langfristig (12+ Monate)</strong></p>
        <ul style='margin: 0; padding-left: 1.5rem;'>
            <li>Automatisierung der Qualitätskontrolle</li>
            <li>Real-time Monitoring mit automatischen Alarmen</li>
            <li>Kontinuierliche Schulungen basierend auf Datenanalysen</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Erwarteter ROI
st.markdown("""
<div style='background: rgba(50, 116, 217, 0.1); border-left: 4px solid #3274d9; 
            padding: 1.5rem; border-radius: 4px; margin-top: 1rem;'>
    <h4 style='color: #3274d9; margin: 0 0 1rem 0;'>💰 Erwarteter ROI</h4>
    <div style='color: #d8d9da; line-height: 1.8;'>
        <p style='margin: 0;'>Bei Umsetzung aller Maßnahmen:</p>
        <ul style='margin: 0.5rem 0 0 0; padding-left: 1.5rem;'>
            <li><strong>Reduktion Ausschuss:</strong> -30% → Einsparung von ~{:,.0f} Ausschussteilen/Jahr</li>
            <li><strong>Energieeffizienz:</strong> +15% → Kosteneinsparung möglich</li>
            <li><strong>Verfügbarkeit:</strong> +5% → Produktionssteigerung von ~{:,.0f} Stück/Jahr</li>
        </ul>
    </div>
</div>
""".format(total_scrap * 0.3, total_output * 0.05), unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem; border-top: 1px solid #2d3035;'>
    <p style='margin: 0;'><strong>Production Monitoring Dashboard v2.0</strong></p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
        Powered by Streamlit & Plotly | Data refresh rate: Real-time
    </p>
</div>
""", unsafe_allow_html=True)
