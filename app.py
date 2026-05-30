import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime

from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from ai_predictor import predict_health_condition, get_risk_level
from validators import validate_patient_form

# PAGE CONFIG
st.set_page_config(
    page_title="MIRA – Medical Intelligence",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# CUSTOM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --primary:        #1a56db;
    --primary-light:  #eff6ff;
    --primary-mid:    #bfdbfe;
    --accent:         #0891b2;
    --success:        #059669;
    --success-light:  #ecfdf5;
    --warning:        #d97706;
    --warning-light:  #fffbeb;
    --danger:         #dc2626;
    --danger-light:   #fef2f2;
    --bg:             #f8fafc;
    --bg-white:       #ffffff;
    --surface:        #f1f5f9;
    --border:         #e2e8f0;
    --border-strong:  #cbd5e1;
    --text-primary:   #0f172a;
    --text-secondary: #475569;
    --text-muted:     #94a3b8;
    --shadow-sm:      0 1px 3px rgba(15,23,42,0.08), 0 1px 2px rgba(15,23,42,0.04);
    --shadow-md:      0 4px 16px rgba(15,23,42,0.10), 0 2px 6px rgba(15,23,42,0.06);
    --shadow-lg:      0 12px 40px rgba(15,23,42,0.12), 0 4px 12px rgba(15,23,42,0.06);
    --shadow-glow:    0 0 0 3px rgba(26,86,219,0.12);
    --radius:         14px;
    --radius-sm:      8px;
    --radius-lg:      20px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text-primary);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg-white);
    border-right: 1px solid var(--border);
    box-shadow: 2px 0 12px rgba(15,23,42,0.05);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── HEADER ── */
.mira-header {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 36px 48px;
    margin-bottom: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-md);
}
.mira-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,
        rgba(26,86,219,0.04) 0%,
        rgba(8,145,178,0.03) 50%,
        transparent 100%);
    pointer-events: none;
}
.mira-header::after {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 320px; height: 120px;
    background: radial-gradient(ellipse, rgba(26,86,219,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.mira-logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #1a56db 0%, #0891b2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 6px;
    position: relative;
}
.mira-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 8px;
    font-weight: 500;
    position: relative;
}
.mira-tagline-bar {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 16px;
    background: var(--primary-light);
    border: 1px solid var(--primary-mid);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--primary);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── METRIC CARDS ── */
.metric-box {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 20px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent-color, #1a56db);
    border-radius: var(--radius) var(--radius) 0 0;
}
.metric-box:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}
.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 2.4rem;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 2px solid var(--border);
    padding-bottom: 10px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 1.15rem;
    background: linear-gradient(180deg, #1a56db, #0891b2);
    border-radius: 2px;
    flex-shrink: 0;
}

/* ── CARDS ── */
.mira-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}
.mira-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-mid);
}

/* ── REMARKS / AI BOX ── */
.remarks-box {
    background: linear-gradient(135deg, #f8fafc, #eff6ff);
    border: 1px solid var(--primary-mid);
    border-left: 4px solid var(--primary);
    border-radius: var(--radius-sm);
    padding: 18px 20px;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.75;
    font-weight: 400;
}

/* ── SIDEBAR BRAND ── */
.sidebar-brand {
    text-align: center;
    padding: 24px 0 12px 0;
}
.sidebar-brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(135deg, #1a56db, #0891b2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
}
.sidebar-brand-sub {
    font-size: 0.6rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    margin-top: 3px;
    text-transform: uppercase;
}
.sidebar-info-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 16px;
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.8;
}
.sidebar-info-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 2px;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #1a56db 0%, #1d4ed8 100%);
    color: #ffffff !important;
    border: none;
    border-radius: var(--radius-sm);
    padding: 11px 28px;
    font-weight: 600;
    font-size: 0.88rem;
    letter-spacing: 0.3px;
    transition: all 0.22s ease;
    width: 100%;
    box-shadow: 0 2px 8px rgba(26,86,219,0.25);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1a56db 100%);
    box-shadow: 0 6px 20px rgba(26,86,219,0.35);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(26,86,219,0.2);
}

/* ── FORM INPUTS ── */
.stTextInput > div > div input,
.stNumberInput > div > div input,
.stDateInput > div > div input,
.stTextArea > div > div textarea {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.18s, box-shadow 0.18s;
}
.stTextInput > div > div input:focus,
.stNumberInput > div > div input:focus,
.stDateInput > div > div input:focus,
.stTextArea > div > div textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: var(--shadow-glow) !important;
}
.stSelectbox > div > div {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

/* ── LABELS ── */
label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTextArea label, .stSelectbox label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 4px !important;
}

/* ── DATAFRAME ── */
div[data-testid="stDataFrame"] {
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: var(--bg-white);
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
    margin-bottom: 8px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
}
[data-testid="stExpander"]:hover {
    box-shadow: var(--shadow-md);
}

/* ── ALERTS ── */
.stAlert {
    border-radius: var(--radius-sm) !important;
}

/* ── HORIZONTAL RULE ── */
hr {
    border-color: var(--border);
    margin: 12px 0 20px 0;
}

/* ── RADIO (NAV) ── */
[data-testid="stRadio"] label {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--text-secondary) !important;
    padding: 8px 10px;
    border-radius: 7px;
    transition: background 0.15s;
}
[data-testid="stRadio"] label:hover {
    background: var(--surface);
}

/* ── CHECKBOX ── */
.stCheckbox label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.88rem !important;
    color: var(--text-primary) !important;
}

/* ── STATUS BADGE ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-healthy  { background: var(--success-light); color: var(--success); }
.badge-moderate { background: var(--warning-light); color: var(--warning); }
.badge-high     { background: var(--danger-light);  color: var(--danger);  }

/* ── EMPTY STATE ── */
.empty-state {
    background: var(--bg-white);
    border: 2px dashed var(--border-strong);
    border-radius: var(--radius-lg);
    padding: 56px 40px;
    text-align: center;
}
.empty-icon {
    width: 56px; height: 56px;
    margin: 0 auto 16px;
    background: var(--primary-light);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
}
.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.empty-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
}

/* ── PATIENT DETAIL TABLE ── */
.patient-detail-table {
    width: 100%;
    font-size: 0.88rem;
    border-collapse: collapse;
    color: var(--text-secondary);
}
.patient-detail-table td {
    padding: 8px 12px 8px 0;
    vertical-align: top;
    width: 50%;
}
.patient-detail-table td strong {
    color: var(--text-primary);
    font-weight: 600;
}

/* ── DIVIDER LINE ── */
.mira-divider {
    height: 1px;
    background: var(--border);
    margin: 20px 0;
}

/* ── SUBTLE GRID BG ON HEADER ── */
.grid-bg {
    background-image:
        linear-gradient(rgba(26,86,219,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(26,86,219,0.04) 1px, transparent 1px);
    background-size: 28px 28px;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='sidebar-brand-name'>MIRA</div>
        <div class='sidebar-brand-sub'>Medical Intelligence</div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["Dashboard", "Add Patient", "View Records", "Update Record", "Delete Record"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sidebar-info-block'>
        <div class='sidebar-info-label'>AI Engine</div>
        Claude AI by Anthropic
        <br><br>
        <div class='sidebar-info-label'>Storage</div>
        SQLite — Persistent Local DB
        <br><br>
        <div class='sidebar-info-label'>Parameters</div>
        Glucose · Haemoglobin · Cholesterol
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='mira-header grid-bg'>
    <div class='mira-logo-text'>MIRA</div>
    <div class='mira-subtitle'>Medical Intelligence Robotic Automation</div>
    <div style='display:flex; justify-content:center; margin-top:14px;'>
        <div class='mira-tagline-bar'>Health Prediction Platform</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if nav == "Dashboard":
    patients = read_all_patients()
    total    = len(patients)
    high_risk = sum(1 for p in patients if "🔴" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    moderate  = sum(1 for p in patients if "🟡" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    healthy   = sum(1 for p in patients if "🟢" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (total,     "Total Patients", "#1a56db"),
        (healthy,   "Healthy",        "#059669"),
        (moderate,  "Moderate Risk",  "#d97706"),
        (high_risk, "High Risk",      "#dc2626"),
    ]
    for col, (val, label, color) in zip([c1, c2, c3, c4], metrics):
        col.markdown(f"""
        <div class='metric-box' style='--accent-color:{color};'>
            <div class='metric-value' style='color:{color};'>{val}</div>
            <div class='metric-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if patients:
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("<div class='section-title'>Blood Parameter Overview</div>", unsafe_allow_html=True)
            df = pd.DataFrame(patients)
            fig = go.Figure()
            palette = [
                ("#1a56db", "Glucose (mg/dL)"),
                ("#d97706", "Cholesterol (mg/dL)"),
                ("#059669", "Haemoglobin (g/dL)"),
            ]
            keys = ["glucose", "cholesterol", "haemoglobin"]
            for (color, name), key in zip(palette, keys):
                fig.add_trace(go.Scatter(
                    x=df['full_name'], y=df[key],
                    name=name, mode='lines+markers',
                    line=dict(color=color, width=2.5),
                    marker=dict(size=7, color=color,
                                line=dict(color='white', width=1.5))
                ))
            fig.update_layout(
                paper_bgcolor='white', plot_bgcolor='#f8fafc',
                font=dict(color='#475569', family='DM Sans', size=11),
                legend=dict(bgcolor='white', bordercolor='#e2e8f0',
                            borderwidth=1, font=dict(size=11)),
                xaxis=dict(gridcolor='#e2e8f0', showgrid=True,
                           linecolor='#e2e8f0', tickfont=dict(size=10)),
                yaxis=dict(gridcolor='#e2e8f0', showgrid=True,
                           linecolor='#e2e8f0'),
                margin=dict(l=0, r=0, t=10, b=0),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("<div class='section-title'>Risk Distribution</div>", unsafe_allow_html=True)
            fig2 = go.Figure(data=[go.Pie(
                labels=['Healthy', 'Moderate Risk', 'High Risk'],
                values=[healthy, moderate, high_risk],
                hole=0.62,
                marker=dict(
                    colors=['#059669', '#d97706', '#dc2626'],
                    line=dict(color='white', width=3)
                ),
                textfont=dict(size=12, family='DM Sans'),
                textinfo='percent+label'
            )])
            fig2.update_layout(
                paper_bgcolor='white', plot_bgcolor='white',
                font=dict(color='#475569', family='DM Sans'),
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                height=280,
                annotations=[dict(
                    text=f"<b>{total}</b>",
                    x=0.5, y=0.5,
                    font=dict(size=22, color='#0f172a', family='DM Mono'),
                    showarrow=False
                )]
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div class='section-title'>Recent Patients</div>", unsafe_allow_html=True)
        recent = patients[:5]
        df_display = pd.DataFrame(recent)[['full_name', 'email', 'glucose', 'haemoglobin', 'cholesterol', 'created_at']]
        df_display['created_at'] = df_display['created_at'].apply(lambda x: x[:10])
        df_display.columns = ['Name', 'Email', 'Glucose', 'Haemoglobin', 'Cholesterol', 'Added On']
        df_display['Risk'] = [get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']) for p in recent]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    else:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-title'>No patient records yet</div>
            <div class='empty-sub'>Navigate to "Add Patient" to register your first patient.</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ADD PATIENT
# ════════════════════════════════════════════════════════════════════════════
elif nav == "Add Patient":
    st.markdown("<div class='section-title'>Register New Patient</div>", unsafe_allow_html=True)

    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name  = st.text_input("Full Name", placeholder="e.g., Dhanapriya D")
            email      = st.text_input("Email Address", placeholder="e.g., patient@email.com")
            glucose    = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=600.0,
                                          value=90.0, step=0.1, help="Normal fasting: 70–99 mg/dL")
        with col2:
            dob         = st.date_input("Date of Birth", max_value=date.today(),
                                         value=date(1990, 1, 1))
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
                st.error(f"{e}")
        else:
            with st.spinner("MIRA is analyzing patient data..."):
                try:
                    remarks    = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                    patient_id = create_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
                    if patient_id:
                        risk = get_risk_level(glucose, haemoglobin, cholesterol)
                        clean = remarks.replace("**","").replace("*","").replace("??","").replace("##","").strip()
                        st.success(f"Patient {full_name} registered successfully — ID #{patient_id}")
                        st.markdown(f"""
                        <div class='mira-card'>
                            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>
                                <span style='font-family:Playfair Display,serif;font-size:1rem;font-weight:600;color:#0f172a;'>
                                    AI Health Assessment
                                </span>
                                <span style='font-size:0.85rem;'>{risk}</span>
                            </div>
                            <div class='remarks-box'>{clean}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.error("A patient with this email already exists.")
                except Exception as ex:
                    st.error(f"AI Analysis failed: {str(ex)}")

# ════════════════════════════════════════════════════════════════════════════
# VIEW RECORDS
# ════════════════════════════════════════════════════════════════════════════
elif nav == "View Records":
    st.markdown("<div class='section-title'>Patient Records</div>", unsafe_allow_html=True)

    search_query = st.text_input("Search by name or email", placeholder="Type to search...")
    patients = search_patients(search_query) if search_query else read_all_patients()

    if not patients:
        st.info("No records found.")
    else:
        st.markdown(f"""
        <div style='color:var(--text-muted);font-size:0.8rem;margin-bottom:14px;font-weight:500;'>
            {len(patients)} record(s) found
        </div>""", unsafe_allow_html=True)
        for p in patients:
            risk = get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol'])
            with st.expander(f"#{p['id']}  —  {p['full_name']}  |  {risk}"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Email:** {p['email']}")
                c1.markdown(f"**Date of Birth:** {p['date_of_birth']}")
                c2.markdown(f"**Glucose:** {p['glucose']} mg/dL")
                c2.markdown(f"**Haemoglobin:** {p['haemoglobin']} g/dL")
                c3.markdown(f"**Cholesterol:** {p['cholesterol']} mg/dL")
                c3.markdown(f"**Added:** {p['created_at'][:10]}")
                if p.get('remarks'):
                    clean = p['remarks'].replace('**','').replace('*','').replace('??','').strip()
                    st.markdown(f"""
                    <div class='remarks-box' style='margin-top:12px;'>
                        <strong style='color:#1a56db;font-size:0.75rem;letter-spacing:1px;
                                       text-transform:uppercase;'>AI Remarks</strong>
                        <div style='margin-top:8px;'>{clean}</div>
                    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# UPDATE RECORD
# ════════════════════════════════════════════════════════════════════════════
elif nav == "Update Record":
    st.markdown("<div class='section-title'>Update Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"#{p['id']} — {p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to update", list(options.keys()))
        pid      = options[selected]
        patient  = read_patient_by_id(pid)

        if patient:
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                with col1:
                    full_name  = st.text_input("Full Name", value=patient['full_name'])
                    email      = st.text_input("Email Address", value=patient['email'])
                    glucose    = st.number_input("Glucose (mg/dL)", value=float(patient['glucose']),
                                                  min_value=0.0, max_value=600.0, step=0.1)
                with col2:
                    dob_val     = datetime.strptime(patient['date_of_birth'], "%Y-%m-%d").date()
                    dob         = st.date_input("Date of Birth", value=dob_val, max_value=date.today())
                    haemoglobin = st.number_input("Haemoglobin (g/dL)", value=float(patient['haemoglobin']),
                                                   min_value=0.0, max_value=25.0, step=0.1)
                    cholesterol = st.number_input("Cholesterol (mg/dL)", value=float(patient['cholesterol']),
                                                   min_value=0.0, max_value=700.0, step=0.1)

                regen_ai = st.checkbox("Re-run AI Analysis with updated values", value=True)

                _, col_btn, _ = st.columns([1, 2, 1])
                with col_btn:
                    update_btn = st.form_submit_button("Save Changes", use_container_width=True)

            if update_btn:
                errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
                if errors:
                    for e in errors:
                        st.error(f"{e}")
                else:
                    remarks = patient.get('remarks', '')
                    if regen_ai:
                        with st.spinner("Re-analyzing with updated data..."):
                            try:
                                remarks = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                            except Exception as ex:
                                st.warning(f"AI analysis failed — keeping previous remarks. ({ex})")

                    success = update_patient(pid, full_name, str(dob), email,
                                             glucose, haemoglobin, cholesterol, remarks)
                    if success:
                        st.success(f"Patient #{pid} updated successfully.")
                        if remarks:
                            st.markdown(f"""
                            <div class='mira-card'>
                                <div style='font-family:Playfair Display,serif;font-size:1rem;
                                            font-weight:600;color:#0f172a;margin-bottom:12px;'>
                                    Updated AI Remarks
                                </div>
                                <div class='remarks-box'>{remarks}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.error("Update failed. The email may already belong to another patient.")

# ════════════════════════════════════════════════════════════════════════════
# DELETE RECORD
# ════════════════════════════════════════════════════════════════════════════
elif nav == "Delete Record":
    st.markdown("<div class='section-title'>Delete Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"#{p['id']} — {p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to delete", list(options.keys()))
        pid      = options[selected]
        patient  = read_patient_by_id(pid)

        if patient:
            risk = get_risk_level(patient['glucose'], patient['haemoglobin'], patient['cholesterol'])
            st.markdown(f"""
            <div class='mira-card' style='border-color:#fecaca;'>
                <div style='font-family:Playfair Display,serif;font-size:1rem;font-weight:600;
                            color:#0f172a;margin-bottom:16px;'>Patient Details</div>
                <table class='patient-detail-table'>
                    <tr>
                        <td><strong>Name:</strong> {patient['full_name']}</td>
                        <td><strong>Email:</strong> {patient['email']}</td>
                    </tr>
                    <tr>
                        <td><strong>Date of Birth:</strong> {patient['date_of_birth']}</td>
                        <td><strong>Risk Level:</strong> {risk}</td>
                    </tr>
                    <tr>
                        <td><strong>Glucose:</strong> {patient['glucose']} mg/dL</td>
                        <td><strong>Haemoglobin:</strong> {patient['haemoglobin']} g/dL</td>
                    </tr>
                    <tr>
                        <td><strong>Cholesterol:</strong> {patient['cholesterol']} mg/dL</td>
                        <td></td>
                    </tr>
                </table>
            </div>""", unsafe_allow_html=True)

            st.warning("This action is permanent and cannot be undone.")
            col1, col2, _ = st.columns([1, 1, 2])
            with col1:
                if st.button("Confirm Delete", type="primary"):
                    if delete_patient(pid):
                        st.success(f"Patient #{pid} — {patient['full_name']} has been deleted.")
                        st.rerun()
                    else:
                        st.error("Deletion failed.")
            with col2:
                if st.button("Cancel"):
                    st.info("Deletion cancelled.")
