import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from ai_predictor import predict_health_condition, get_risk_level
from validators import validate_patient_form

st.set_page_config(
    page_title="MIRA – Medical Intelligence",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()
THRESHOLDS = {
    "glucose":     {"low": 70,   "high": 99,   "max": 300,  "unit": "mg/dL"},
    "haemoglobin": {"low": 12.0, "high": 17.5, "max": 20.0, "unit": "g/dL"},
    "cholesterol": {"low": 0,    "high": 200,  "max": 300,  "unit": "mg/dL"},
}

def param_status(key, value):
    t = THRESHOLDS[key]
    if value < t["low"]:
        return "Low",    "#d97706", "#fffbeb"
    elif value <= t["high"]:
        return "Normal", "#059669", "#ecfdf5"
    else:
        return "High",   "#dc2626", "#fef2f2"

def bar_color_for_patient(p):
    out = {}
    for key in ("glucose", "haemoglobin", "cholesterol"):
        _, color, _ = param_status(key, p[key])
        out[key] = color
    return out

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --primary:        #1847c2;
    --primary-light:  #eef2fd;
    --primary-mid:    #c0cef8;
    --success:        #059669;
    --success-light:  #ecfdf5;
    --warning:        #d97706;
    --warning-light:  #fffbeb;
    --danger:         #dc2626;
    --danger-light:   #fef2f2;
    --normal-bar:     #059669;
    --low-bar:        #d97706;
    --high-bar:       #dc2626;
    --bg:             #f0f4f8;
    --bg-white:       #ffffff;
    --surface:        #f7f9fc;
    --border:         #dde3ed;
    --border-strong:  #c4cdd9;
    --text-primary:   #0c1629;
    --text-secondary: #4a5568;
    --text-muted:     #8a97aa;
    --shadow-sm:      0 1px 4px rgba(12,22,41,0.07);
    --shadow-md:      0 4px 18px rgba(12,22,41,0.10);
    --shadow-lg:      0 10px 40px rgba(12,22,41,0.13);
    --glow:           0 0 0 3px rgba(24,71,194,0.13);
    --radius:         12px;
    --radius-sm:      8px;
    --radius-lg:      18px;
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: var(--bg);
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background: var(--bg-white);
    border-right: 1px solid var(--border);
    box-shadow: 3px 0 16px rgba(12,22,41,0.06);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

.sidebar-logo {
    padding: 28px 20px 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 18px;
}
.sidebar-logo-mark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.sidebar-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1847c2, #3b6ff0);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 2px 8px rgba(24,71,194,0.25);
}
.sidebar-logo-name {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    letter-spacing: 3px;
}
.sidebar-logo-sub {
    font-size: 0.62rem;
    color: var(--text-muted) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding-left: 46px;
}

.nav-section-label {
    font-size: 0.6rem;
    font-weight: 700;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 0 14px 6px;
}

.sidebar-meta {
    margin: 16px 0 0;
    border-top: 1px solid var(--border);
    padding: 16px 14px 0;
}
.sidebar-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    font-size: 0.73rem;
    color: var(--text-secondary) !important;
    border-bottom: 1px solid var(--border);
}
.sidebar-meta-row:last-child { border-bottom: none; }
.sidebar-meta-label {
    font-weight: 600;
    color: var(--text-muted) !important;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.sidebar-meta-val {
    color: var(--primary) !important;
    font-weight: 600;
    font-size: 0.72rem;
}
.mira-header {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 0;
    margin-bottom: 28px;
    overflow: hidden;
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: stretch;
    min-height: 100px;
}
.mira-header-stripe {
    width: 7px;
    background: linear-gradient(180deg, #1847c2 0%, #3b6ff0 50%, #0891b2 100%);
    flex-shrink: 0;
}
.mira-header-body {
    flex: 1;
    padding: 28px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.mira-header-left {}
.mira-header-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 5px;
    line-height: 1;
}
.mira-header-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 5px;
    font-weight: 400;
}
.mira-header-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
}
.mira-header-badge {
    background: var(--primary-light);
    border: 1px solid var(--primary-mid);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--primary);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.mira-header-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    color: var(--success);
    font-weight: 500;
}
.mira-header-status-dot {
    width: 7px; height: 7px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.45; }
}
.section-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::before {
    content: '';
    width: 3px; height: 14px;
    background: linear-gradient(180deg, var(--primary), #3b6ff0);
    border-radius: 2px;
    flex-shrink: 0;
}
.metric-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 20px 18px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--card-color, #1847c2);
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
.metric-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.2rem;
    font-weight: 500;
    color: var(--card-color, #1847c2);
    line-height: 1;
    margin-bottom: 6px;
}
.metric-title {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.metric-bg-icon {
    position: absolute;
    right: 14px; top: 12px;
    font-size: 2.2rem;
    opacity: 0.06;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    color: var(--card-color, #1847c2);
    letter-spacing: -2px;
}
.chart-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 20px 12px;
    box-shadow: var(--shadow-sm);
}
.legend-row {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 8px;
    justify-content: center;
}
.legend-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: 0.5px;
}
.legend-dot {
    width: 9px; height: 9px;
    border-radius: 3px;
    flex-shrink: 0;
}
.pt-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.83rem;
}
.pt-table thead th {
    background: var(--surface);
    border-bottom: 2px solid var(--border);
    padding: 10px 14px;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    text-align: left;
}
.pt-table tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
}
.pt-table tbody tr:hover {
    background: var(--surface);
}
.pt-table tbody td {
    padding: 11px 14px;
    color: var(--text-secondary);
    vertical-align: middle;
}
.pt-table tbody td.name-cell {
    font-weight: 600;
    color: var(--text-primary);
}
.val-cell {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
}
.pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.pill-healthy  { background: #ecfdf5; color: #059669; }
.pill-moderate { background: #fffbeb; color: #d97706; }
.pill-high     { background: #fef2f2; color: #dc2626; }
.pill-normal   { background: #ecfdf5; color: #059669; }
.pill-low      { background: #fffbeb; color: #d97706; }
.mira-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.mira-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-mid);
}
.remarks-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--primary);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    font-size: 0.86rem;
    color: var(--text-secondary);
    line-height: 1.78;
}
.remarks-label {
    font-size: 0.62rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
[data-testid="stExpander"] {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
    margin-bottom: 8px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
}
[data-testid="stExpander"]:hover { box-shadow: var(--shadow-md); }
.stButton > button {
    background: linear-gradient(135deg, #1847c2, #2558e0);
    color: #fff !important;
    border: none;
    border-radius: var(--radius-sm);
    padding: 10px 28px;
    font-weight: 600;
    font-size: 0.86rem;
    letter-spacing: 0.3px;
    transition: all 0.2s;
    width: 100%;
    box-shadow: 0 2px 10px rgba(24,71,194,0.28);
    font-family: 'Sora', sans-serif;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #133ba3, #1847c2);
    box-shadow: 0 6px 20px rgba(24,71,194,0.38);
    transform: translateY(-1px);
}
.stButton > button:active { transform: none; }
.stTextInput > div > div input,
.stNumberInput > div > div input,
.stDateInput > div > div input,
.stTextArea > div > div textarea {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.88rem !important;
    transition: border-color 0.18s, box-shadow 0.18s;
}
.stTextInput > div > div input:focus,
.stNumberInput > div > div input:focus,
.stDateInput > div > div input:focus,
.stTextArea > div > div textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: var(--glow) !important;
}
.stSelectbox > div > div {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
}
label, .stTextInput label, .stNumberInput label,
.stDateInput label, .stTextArea label, .stSelectbox label {
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

div[data-testid="stDataFrame"] {
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}

.stAlert { border-radius: var(--radius-sm) !important; }
hr { border-color: var(--border); margin: 10px 0 18px; }
[data-testid="stRadio"] label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--text-secondary) !important;
    padding: 7px 10px;
    border-radius: 7px;
    transition: background 0.15s;
}
[data-testid="stRadio"] label:hover { background: var(--surface); }

.stCheckbox label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.86rem !important;
    color: var(--text-primary) !important;
    font-weight: 400 !important;
}

.empty-state {
    background: var(--bg-white);
    border: 2px dashed var(--border-strong);
    border-radius: var(--radius-lg);
    padding: 60px 40px;
    text-align: center;
}
.empty-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.empty-sub { font-size: 0.83rem; color: var(--text-muted); }
.mira-divider { height: 1px; background: var(--border); margin: 18px 0; }

.delete-card {
    background: #fff9f9;
    border: 1px solid #fecaca;
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow-sm);
}
.delete-card-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--danger);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}
.delete-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.delete-table td {
    padding: 12px 16px;
    width: 50%;
    color: var(--text-secondary);
    border-bottom: 1px solid #fde8e8;
    vertical-align: middle;
    line-height: 1.6;
}
.delete-table tr:last-child td { border-bottom: none; }
.delete-table td strong { color: var(--text-primary); font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def risk_pill(g, h, c):
    raw = get_risk_level(g, h, c)
    if "🔴" in raw:
        return "<span class='pill pill-high'>High Risk</span>"
    elif "🟡" in raw:
        return "<span class='pill pill-moderate'>Moderate</span>"
    return "<span class='pill pill-healthy'>Healthy</span>"

def clean_md(text):
    return text.replace("**","").replace("*","").replace("??","").replace("##","").strip()

with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <div class='sidebar-logo-mark'>
            <div class='sidebar-logo-icon'>+</div>
            <div class='sidebar-logo-name'>MIRA</div>
        </div>
        <div class='sidebar-logo-sub'>Medical Intelligence Platform</div>
    </div>
    <div class='nav-section-label'>Navigation</div>
    """, unsafe_allow_html=True)

    nav = st.radio("", ["Home", "Add Patient", "View Records",
                        "Update Record", "Delete Record"],
                   label_visibility="collapsed")

st.markdown("""
<div class='mira-header'>
    <div class='mira-header-stripe'></div>
    <div class='mira-header-body'>
        <div class='mira-header-left'>
            <div class='mira-header-title'>MIRA</div>
            <div class='mira-header-sub'>Medical Intelligence &amp; Robotic Automation</div>
        </div>
        <div class='mira-header-right'>
            <div class='mira-header-badge'>Health Prediction Platform</div>
            <div class='mira-header-status'>
                <div class='mira-header-status-dot'></div>
                System Active
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if nav == "Home":
    patients  = read_all_patients()
    total     = len(patients)
    high_risk = sum(1 for p in patients if "🔴" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    moderate  = sum(1 for p in patients if "🟡" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    healthy   = sum(1 for p in patients if "🟢" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (total,     "Total Patients", "#1847c2", "T"),
        (healthy,   "Healthy",        "#059669", "H"),
        (moderate,  "Moderate Risk",  "#d97706", "M"),
        (high_risk, "High Risk",      "#dc2626", "!"),
    ]
    for col, (val, label, color, icon) in zip([c1, c2, c3, c4], kpis):
        col.markdown(f"""
        <div class='metric-card' style='--card-color:{color};'>
            <div class='metric-bg-icon'>{icon}</div>
            <div class='metric-number'>{val}</div>
            <div class='metric-title'>{label}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not patients:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-title'>No patient records yet</div>
            <div class='empty-sub'>Use "Add Patient" to register your first patient.</div>
        </div>""", unsafe_allow_html=True)
    else:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown("<div class='section-title'>Blood Parameter Overview</div>", unsafe_allow_html=True)
            df = pd.DataFrame(patients)
            names = df['full_name'].tolist()
            G_MAX, C_MAX, H_MAX = 300.0, 300.0, 20.0

            params = [
                ("glucose",     "Glucose",     G_MAX, "mg/dL"),
                ("cholesterol", "Cholesterol", C_MAX, "mg/dL"),
                ("haemoglobin", "Haemoglobin", H_MAX, "g/dL"),
            ]
            fig = go.Figure()
            for key, label, max_val, unit in params:
                raw_vals = df[key].tolist()
                pct_vals = [v / max_val * 100 for v in raw_vals]
                colors = [param_status(key, v)[1] for v in raw_vals]

                fig.add_trace(go.Bar(
                    name=label,
                    x=names,
                    y=pct_vals,
                    text=[f"{v} {unit}" for v in raw_vals],
                    textposition='outside',
                    textfont=dict(size=9.5, color='#4a5568', family='IBM Plex Mono'),
                    marker=dict(
                        color=colors,
                        opacity=0.90,
                        line=dict(color='white', width=1.5),
                        cornerradius=4,
                    ),
                    hovertemplate=(
                        f"<b>%{{x}}</b><br>"
                        f"{label}: <b>%{{customdata}} {unit}</b><br>"
                        f"% of range: %{{y:.1f}}%<extra></extra>"
                    ),
                    customdata=raw_vals,
                    legendgroup=label,
                    showlegend=False,  
                ))

            fig.update_layout(
                barmode='group',
                paper_bgcolor='white', plot_bgcolor='white',
                font=dict(color='#4a5568', family='Sora', size=11),
                xaxis=dict(showgrid=False, linecolor='#dde3ed',
                           tickfont=dict(size=11, color='#0c1629')),
                yaxis=dict(showgrid=False, showticklabels=False, range=[0, 135]),
                bargap=0.22, bargroupgap=0.06,
                margin=dict(l=0, r=0, t=12, b=0),
                height=310,
                legend=dict(visible=False),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        padding:0 4px;margin-top:-6px;'>
                <div class='legend-row'>
                    <span class='legend-pill'><span class='legend-dot' style='background:#1847c2'></span>Glucose</span>
                    <span class='legend-pill'><span class='legend-dot' style='background:#d97706'></span>Cholesterol</span>
                    <span class='legend-pill'><span class='legend-dot' style='background:#0891b2'></span>Haemoglobin</span>
                </div>
                <div class='legend-row'>
                    <span class='legend-pill'><span class='legend-dot' style='background:#059669'></span>Normal</span>
                    <span class='legend-pill'><span class='legend-dot' style='background:#d97706'></span>Low</span>
                    <span class='legend-pill'><span class='legend-dot' style='background:#dc2626'></span>High</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='section-title'>Risk Distribution</div>", unsafe_allow_html=True)
            fig2 = go.Figure(data=[go.Pie(
                labels=['Healthy', 'Moderate', 'High Risk'],
                values=[healthy if healthy else 0.001,
                        moderate if moderate else 0.001,
                        high_risk if high_risk else 0.001],
                hole=0.65,
                marker=dict(
                    colors=['#059669', '#d97706', '#dc2626'],
                    line=dict(color='white', width=3)
                ),
                textfont=dict(size=11, family='Sora'),
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>%{value} patients<extra></extra>',
            )])
            fig2.update_layout(
                paper_bgcolor='white', plot_bgcolor='white',
                font=dict(color='#4a5568', family='Sora'),
                legend=dict(
                    orientation='v',
                    bgcolor='white',
                    font=dict(size=11),
                    x=0.75, y=0.5,
                    xanchor='left', yanchor='middle'
                ),
                margin=dict(l=0, r=60, t=10, b=10),
                height=265,
                annotations=[dict(
                    text=f'<b>{total}</b><br><span style="font-size:10px">patients</span>',
                    x=0.37, y=0.5,
                    font=dict(size=18, color='#0c1629', family='IBM Plex Mono'),
                    showarrow=False
                )]
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Recent Patients</div>", unsafe_allow_html=True)
        recent = patients[:6]
        rows = ""
        for p in recent:
            g_st, g_col, _ = param_status("glucose",     p['glucose'])
            h_st, h_col, _ = param_status("haemoglobin", p['haemoglobin'])
            c_st, c_col, _ = param_status("cholesterol", p['cholesterol'])
            rp = risk_pill(p['glucose'], p['haemoglobin'], p['cholesterol'])
            rows += f"""
            <tr>
                <td class='name-cell'>{p['full_name']}</td>
                <td>{p['email']}</td>
                <td class='val-cell'><span style='color:{g_col};font-weight:600;'>{p['glucose']}</span>
                    <span style='font-size:0.7rem;color:#8a97aa;'> mg/dL</span></td>
                <td class='val-cell'><span style='color:{h_col};font-weight:600;'>{p['haemoglobin']}</span>
                    <span style='font-size:0.7rem;color:#8a97aa;'> g/dL</span></td>
                <td class='val-cell'><span style='color:{c_col};font-weight:600;'>{p['cholesterol']}</span>
                    <span style='font-size:0.7rem;color:#8a97aa;'> mg/dL</span></td>
                <td>{rp}</td>
                <td style='color:#8a97aa;font-size:0.78rem;'>{p['created_at'][:10]}</td>
            </tr>"""

        st.markdown(f"""
        <div style='background:white;border:1px solid var(--border);border-radius:12px;
                    overflow:hidden;box-shadow:var(--shadow-sm);'>
        <table class='pt-table'>
            <thead>
                <tr>
                    <th>Patient</th><th>Email</th>
                    <th>Glucose</th><th>Haemoglobin</th><th>Cholesterol</th>
                    <th>Risk</th><th>Added</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        </div>""", unsafe_allow_html=True)

elif nav == "Add Patient":
    st.markdown("<div class='section-title'>Register New Patient</div>", unsafe_allow_html=True)
    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name   = st.text_input("Full Name", placeholder="Enter your name")
            email       = st.text_input("Email Address", placeholder="xxxxxxx@gmail.com")
            glucose     = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=600.0,
                                           value=90.0, step=0.1, help="Normal fasting: 70–99 mg/dL")
        with col2:
            dob         = st.date_input("Date of Birth", max_value=date.today(), value=date(1990, 1, 1))
            haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=0.0, max_value=25.0,
                                           value=13.5, step=0.1, help="Normal: 12.0–17.5 g/dL")
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, max_value=700.0,
                                           value=180.0, step=0.1, help="Desirable: <200 mg/dL")
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            submitted = st.form_submit_button("Analyze and Save Patient", use_container_width=True)

    if submitted:
        errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
        if errors:
            for e in errors:
                st.error(e)
        else:
            with st.spinner("MIRA AI is analyzing patient data..."):
                try:
                    remarks    = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                    patient_id = create_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
                    if patient_id:
                        risk = risk_pill(glucose, haemoglobin, cholesterol)
                        st.success(f"Patient {full_name} registered successfully.")
                        st.markdown(f"""
                        <div class='mira-card'>
                            <div style='display:flex;justify-content:space-between;
                                        align-items:center;margin-bottom:14px;'>
                                <div style='font-size:0.65rem;font-weight:700;color:#8a97aa;
                                            text-transform:uppercase;letter-spacing:1.5px;'>
                                    AI Health Assessment
                                </div>
                                {risk}
                            </div>
                            <div class='remarks-box'>{clean_md(remarks)}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.error("A patient with this email already exists.")
                except Exception as ex:
                    st.error(f"AI Analysis failed: {ex}")

elif nav == "View Records":
    st.markdown("<div class='section-title'>Patient Records</div>", unsafe_allow_html=True)

    search_query = st.text_input("Search by name or email", placeholder="Type to search...")
    patients     = search_patients(search_query) if search_query else read_all_patients()

    if not patients:
        st.info("No records found.")
    else:
        st.markdown(f"""<div style='font-size:0.72rem;color:#8a97aa;font-weight:600;
                        text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;'>
            {len(patients)} record(s) found</div>""", unsafe_allow_html=True)

        def make_gauge(value, label, unit, low_ok, high_ok, max_val, pid_key):
            status, color, _ = param_status(
                {"Glucose":"glucose","Haemoglobin":"haemoglobin","Cholesterol":"cholesterol"}[label],
                value
            )
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number=dict(suffix=f" {unit}",
                            font=dict(size=19, family='IBM Plex Mono', color='#0c1629')),
                title=dict(
                    text=f"<b>{label}</b><br><span style='font-size:10px;color:{color};font-weight:700;'>{status}</span>",
                    font=dict(size=12, family='Sora', color='#4a5568')
                ),
                gauge=dict(
                    axis=dict(range=[0, max_val],
                              tickfont=dict(size=8, color='#8a97aa'),
                              tickcolor='#dde3ed'),
                    bar=dict(color=color, thickness=0.55),
                    bgcolor='#f0f4f8',
                    borderwidth=0,
                    steps=[
                        dict(range=[0, low_ok],        color='#fffbeb'),
                        dict(range=[low_ok, high_ok],  color='#ecfdf5'),
                        dict(range=[high_ok, max_val], color='#fef2f2'),
                    ],
                    threshold=dict(line=dict(color=color, width=2),
                                   thickness=0.75, value=value)
                )
            ))
            fig_g.update_layout(
                paper_bgcolor='white',
                margin=dict(l=14, r=14, t=52, b=10),
                height=195
            )
            return fig_g

        for p in patients:
            rp = risk_pill(p['glucose'], p['haemoglobin'], p['cholesterol'])
            label_str = p['full_name'] + " — " + ("High Risk" if "🔴" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']) else ("Moderate" if "🟡" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']) else "Healthy"))

            with st.expander(p['full_name']):
                # meta row
                m1, m2, m3, m4 = st.columns(4)
                m1.markdown(f"**Email**\n\n{p['email']}")
                m2.markdown(f"**Date of Birth**\n\n{p['date_of_birth']}")
                m3.markdown(f"**Added**\n\n{p['created_at'][:10]}")
                m4.markdown(f"**Risk**")
                m4.markdown(rp, unsafe_allow_html=True)
                st.markdown("<div class='mira-divider'></div>", unsafe_allow_html=True)

                gc1, gc2, gc3 = st.columns(3)
                with gc1:
                    st.plotly_chart(make_gauge(p['glucose'], "Glucose", "mg/dL",
                                               70, 99, 300, f"g{p['id']}"),
                                    use_container_width=True, key=f"gauge_g_{p['id']}")
                with gc2:
                    st.plotly_chart(make_gauge(p['haemoglobin'], "Haemoglobin", "g/dL",
                                               12.0, 17.5, 20.0, f"h{p['id']}"),
                                    use_container_width=True, key=f"gauge_h_{p['id']}")
                with gc3:
                    st.plotly_chart(make_gauge(p['cholesterol'], "Cholesterol", "mg/dL",
                                               0, 200, 300, f"c{p['id']}"),
                                    use_container_width=True, key=f"gauge_c_{p['id']}")

                if p.get('remarks'):
                    st.markdown(f"""
                    <div class='remarks-box' style='margin-top:4px;'>
                        <div class='remarks-label'>AI Clinical Remarks</div>
                        {clean_md(p['remarks'])}
                    </div>""", unsafe_allow_html=True)

elif nav == "Update Record":
    st.markdown("<div class='section-title'>Update Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"{p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to update", list(options.keys()))
        pid      = options[selected]
        patient  = read_patient_by_id(pid)

        if patient:
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                with col1:
                    full_name   = st.text_input("Full Name",    value=patient['full_name'])
                    email       = st.text_input("Email Address",value=patient['email'])
                    glucose     = st.number_input("Glucose (mg/dL)",    value=float(patient['glucose']),
                                                   min_value=0.0, max_value=600.0, step=0.1)
                with col2:
                    dob_val     = datetime.strptime(patient['date_of_birth'], "%Y-%m-%d").date()
                    dob         = st.date_input("Date of Birth", value=dob_val, max_value=date.today())
                    haemoglobin = st.number_input("Haemoglobin (g/dL)", value=float(patient['haemoglobin']),
                                                   min_value=0.0, max_value=25.0, step=0.1)
                    cholesterol = st.number_input("Cholesterol (mg/dL)",value=float(patient['cholesterol']),
                                                   min_value=0.0, max_value=700.0, step=0.1)
                regen_ai = st.checkbox("Re-run AI Analysis with updated values", value=True)
                _, col_btn, _ = st.columns([1, 2, 1])
                with col_btn:
                    update_btn = st.form_submit_button("Save Changes", use_container_width=True)

            if update_btn:
                errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
                if errors:
                    for e in errors: st.error(e)
                else:
                    remarks = patient.get('remarks', '')
                    if regen_ai:
                        with st.spinner("Re-analyzing..."):
                            try:
                                remarks = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                            except Exception as ex:
                                st.warning(f"AI analysis failed — keeping previous remarks. ({ex})")
                    success = update_patient(pid, full_name, str(dob), email,
                                             glucose, haemoglobin, cholesterol, remarks)
                    if success:
                        st.success(f"Patient record updated successfully.")
                        if remarks:
                            st.markdown(f"""
                            <div class='mira-card'>
                                <div style='font-size:0.65rem;font-weight:700;color:#8a97aa;
                                            text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;'>
                                    Updated AI Remarks
                                </div>
                                <div class='remarks-box'>{clean_md(remarks)}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.error("Update failed. Email may belong to another patient.")

elif nav == "Delete Record":
    st.markdown("<div class='section-title'>Delete Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"{p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to delete", list(options.keys()))
        pid      = options[selected]
        patient  = read_patient_by_id(pid)

        if patient:
            rp = risk_pill(patient['glucose'], patient['haemoglobin'], patient['cholesterol'])
            g_st, g_col, _ = param_status("glucose",     patient['glucose'])
            h_st, h_col, _ = param_status("haemoglobin", patient['haemoglobin'])
            c_st, c_col, _ = param_status("cholesterol", patient['cholesterol'])

            st.markdown(f"""
            <div class='delete-card'>
                <div class='delete-card-title'>Patient to be Deleted</div>
                <table class='delete-table'>
                    <tr>
                        <td><strong>Name:</strong> {patient['full_name']}</td>
                        <td><strong>Email:</strong> {patient['email']}</td>
                    </tr>
                    <tr>
                        <td><strong>Date of Birth:</strong> {patient['date_of_birth']}</td>
                        <td><strong>Risk Level:</strong> {rp}</td>
                    </tr>
                    <tr>
                        <td><strong>Glucose:</strong>
                            <span style='color:{g_col};font-weight:600;'>{patient['glucose']} mg/dL</span>
                            &nbsp;<span style='font-size:0.7rem;color:{g_col};'>{g_st}</span></td>
                        <td><strong>Haemoglobin:</strong>
                            <span style='color:{h_col};font-weight:600;'>{patient['haemoglobin']} g/dL</span>
                            &nbsp;<span style='font-size:0.7rem;color:{h_col};'>{h_st}</span></td>
                    </tr>
                    <tr>
                        <td><strong>Cholesterol:</strong>
                            <span style='color:{c_col};font-weight:600;'>{patient['cholesterol']} mg/dL</span>
                            &nbsp;<span style='font-size:0.7rem;color:{c_col};'>{c_st}</span></td>
                        <td></td>
                    </tr>
                </table>
            </div>""", unsafe_allow_html=True)

            st.warning("This action is permanent and cannot be undone.")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Confirm Delete", type="primary"):
                    if delete_patient(pid):
                        st.success(f"{patient['full_name']} has been deleted.")
                        st.rerun()
                    else:
                        st.error("Deletion failed.")
            with col2:
                if st.button("Cancel"):
                    st.info("Deletion cancelled.")
