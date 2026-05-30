import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime
from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from ai_predictor import predict_health_condition, get_risk_level
from validators import validate_patient_form

st.set_page_config(
    page_title="MIRA – Medical Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --primary: #0ea5e9;
    --primary-dark: #0284c7;
    --accent: #06b6d4;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-card2: #162032;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-primary);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid var(--border);
}

/* Cards */
.mira-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.mira-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
}

/* Header */
.mira-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.mira-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at top center, rgba(14,165,233,0.12) 0%, transparent 70%);
}
.mira-logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #0ea5e9, #06b6d4, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
    position: relative;
}
.mira-subtitle {
    font-size: 0.95rem;
    color: var(--text-secondary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
    position: relative;
}

/* Metric cards */
.metric-box {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
}
.metric-label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Risk badges */
.badge-healthy { color: #10b981; font-weight: 600; }
.badge-moderate { color: #f59e0b; font-weight: 600; }
.badge-high { color: #ef4444; font-weight: 600; }

/* Section headers */
.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--primary);
    border-left: 3px solid var(--primary);
    padding-left: 12px;
    margin-bottom: 20px;
}

/* Remarks box */
.remarks-box {
    background: linear-gradient(135deg, #0c1a2e, #162032);
    border: 1px solid #0ea5e9;
    border-radius: 10px;
    padding: 16px;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.6;
}

/* Success/Error message */
.msg-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid #10b981;
    border-radius: 8px;
    padding: 12px 16px;
    color: #10b981;
}
.msg-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef4444;
    border-radius: 8px;
    padding: 12px 16px;
    color: #ef4444;
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.3);
    transform: translateY(-1px);
}
.stTextInput > div > div, .stNumberInput > div > div, .stDateInput > div > div, .stTextArea > div > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
.stSelectbox > div > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
}
/* Animated Background */
.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(14,165,233,0.15), transparent 25%),
        radial-gradient(circle at 80% 80%, rgba(6,182,212,0.15), transparent 25%),
        #0f172a;
}

/* Floating Cards */
.mira-card,
.metric-box {
    transition: all 0.35s ease;
}

.mira-card:hover,
.metric-box:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 40px rgba(14,165,233,0.25);
    border-color: #0ea5e9;
}

/* Glassmorphism */
.glass-card {
    background: rgba(30,41,59,0.7);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
}

/* Glow Animation */
@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(14,165,233,.2);}
    50% { box-shadow: 0 0 25px rgba(14,165,233,.5);}
    100% { box-shadow: 0 0 5px rgba(14,165,233,.2);}
}

.metric-box {
    animation: glow 4s infinite;
}

/* Neon Header */
.mira-logo-text {
    text-shadow:
        0 0 10px rgba(14,165,233,.5),
        0 0 20px rgba(14,165,233,.4),
        0 0 30px rgba(14,165,233,.3);
}

/* Input Focus Effect */
.stTextInput input:focus,
.stNumberInput input:focus {
    border: 1px solid #0ea5e9 !important;
    box-shadow: 0 0 15px rgba(14,165,233,.4) !important;
}

/* Button Shine */
.stButton button {
    position: relative;
    overflow: hidden;
}

.stButton button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -120%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,.3),
        transparent
    );
    transition: .6s;
}

.stButton button:hover::before {
    left: 120%;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
background:rgba(30,41,59,.7);
backdrop-filter:blur(15px);
padding:35px;
border-radius:25px;
border:1px solid rgba(255,255,255,.1);
text-align:center;
margin-bottom:20px;
">
<h1 style="font-size:3rem;">🏥 MIRA AI</h1>
<p style="color:#94a3b8;">
Medical Intelligence & Risk Prediction Platform
</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <div style='font-family: Space Mono, monospace; font-size:1.8rem; font-weight:700;
                    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    letter-spacing:3px;'>MIRA</div>
        <div style='font-size:0.7rem; color:#64748b; letter-spacing:2px; margin-top:4px;'>MEDICAL INTELLIGENCE</div>
    </div>
    <hr style='border-color:#334155; margin: 10px 0 20px 0;'>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["Home", " Add Patient", "View Records", "Update Record", "Delete Record"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#162032; border:1px solid #1e3a5f; border-radius:10px; padding:14px; font-size:0.78rem; color:#64748b;'>
        <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>AI Engine</div>
        Powered by Claude AI (Anthropic)<br><br>
        <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>Storage</div>
        SQLite — Persistent Local DB<br><br>
        <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>Parameters</div>
        Glucose · Haemoglobin · Cholesterol
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='mira-header'>
    <div class='mira-logo-text'>MIRA</div>
    <div class='mira-subtitle'>Medical Intelligence Robotic Automation · Health Prediction Platform</div>
</div>
""", unsafe_allow_html=True)

if nav == "Home":
    patients = read_all_patients()
    total = len(patients)
    high_risk = sum(1 for p in patients if "🔴" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    moderate = sum(1 for p in patients if "🟡" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
    healthy = sum(1 for p in patients if "🟢" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in zip(
        [c1, c2, c3, c4],
        [total, healthy, moderate, high_risk],
        ["Total Patients", "Healthy", "Moderate Risk", "High Risk"],
        ["#0ea5e9", "#10b981", "#f59e0b", "#ef4444"]
    ):
        col.markdown(f"""
        <div class='metric-box'>
            <div class='metric-value' style='color:{color};'>{val}</div>
            <div class='metric-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if patients:
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("<div class='section-title'>📊 Blood Parameter Overview</div>", unsafe_allow_html=True)
            df = pd.DataFrame(patients)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['full_name'], y=df['glucose'],
                name='Glucose (mg/dL)', mode='lines+markers',
                line=dict(color='#0ea5e9', width=2),
                marker=dict(size=8, color='#0ea5e9')
            ))
            fig.add_trace(go.Scatter(
                x=df['full_name'], y=df['cholesterol'],
                name='Cholesterol (mg/dL)', mode='lines+markers',
                line=dict(color='#f59e0b', width=2),
                marker=dict(size=8, color='#f59e0b')
            ))
            fig.add_trace(go.Scatter(
                x=df['full_name'], y=df['haemoglobin'],
                name='Haemoglobin (g/dL)', mode='lines+markers',
                line=dict(color='#10b981', width=2),
                marker=dict(size=8, color='#10b981')
            ))
            fig.update_layout(
                paper_bgcolor='#1e293b',
                plot_bgcolor='#162032',
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("<div class='section-title'>Risk Distribution</div>", unsafe_allow_html=True)
            labels = ['Healthy', 'Moderate Risk', 'High Risk']
            values = [healthy, moderate, high_risk]
            colors = ['#10b981', '#f59e0b', '#ef4444']

            fig2 = go.Figure(data=[go.Pie(
                labels=labels, values=values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color='#1e293b', width=2)),
                textfont=dict(color='white', size=12)
            )])
            fig2.update_layout(
                paper_bgcolor='#1e293b', plot_bgcolor='#1e293b',
                font=dict(color='#94a3b8'),
                showlegend=True,
                legend=dict(bgcolor='#1e293b', bordercolor='#334155', font=dict(color='#94a3b8')),
                margin=dict(l=0, r=0, t=10, b=0), height=280,
                annotations=[dict(text=f"<b>{total}</b><br>Total", x=0.5, y=0.5,
                                  font=dict(size=16, color='#f1f5f9'), showarrow=False)]
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Recent patients table
        st.markdown("<div class='section-title'>🕐 Recent Patients</div>", unsafe_allow_html=True)
        recent = patients[:5]
        df_display = pd.DataFrame(recent)[['full_name', 'email', 'glucose', 'haemoglobin', 'cholesterol', 'created_at']]
        df_display['created_at'] = df_display['created_at'].apply(lambda x: x[:10])
        df_display.columns = ['Name', 'Email', 'Glucose', 'Haemoglobin', 'Cholesterol', 'Added On']
        df_display['Risk'] = [get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']) for p in recent]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class='mira-card' style='text-align:center; padding:40px;'>
            <div style='font-size:3rem;'>🏥</div>
            <div style='font-size:1.1rem; color:#0ea5e9; margin-top:12px;'>No patient records yet</div>
            <div style='color:#64748b; margin-top:8px;'>Use "Add Patient" to register your first patient</div>
        </div>""", unsafe_allow_html=True)

elif nav == "Add Patient":
    st.markdown("<div class='section-title'>Register New Patient</div>", unsafe_allow_html=True)

    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g., Dhanapriya D")
            email = st.text_input("Email Address *", placeholder="e.g., patient@email.com")
            glucose = st.number_input("Glucose (mg/dL) *", min_value=0.0, max_value=600.0, value=90.0, step=0.1,
                                       help="Normal fasting: 70–99 mg/dL")
        with col2:
            dob = st.date_input("Date of Birth *", max_value=date.today(),
                                 value=date(1990, 1, 1), help="Must not be a future date")
            haemoglobin = st.number_input("Haemoglobin (g/dL) *", min_value=0.0, max_value=25.0, value=13.5, step=0.1,
                                           help="Normal: 12.0–17.5 g/dL")
            cholesterol = st.number_input("Cholesterol (mg/dL) *", min_value=0.0, max_value=700.0, value=180.0, step=0.1,
                                           help="Desirable: <200 mg/dL")

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submitted = st.form_submit_button("🤖 Analyze & Save Patient", use_container_width=True)

    if submitted:
        errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            with st.spinner("MIRA AI is analyzing patient data..."):
                try:
                    remarks = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                    patient_id = create_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)

                    if patient_id:
                        risk = get_risk_level(glucose, haemoglobin, cholesterol)
                        # Clean markdown characters from AI response
                        clean_remarks = remarks.replace("**", "").replace("*", "").replace("??", "").replace("##", "").strip()
                        st.success(f"✅ Patient {full_name} registered successfully! ID: #{patient_id}")
                        st.markdown(f"""
                        <div class='mira-card'>
                            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                                <div style='font-size:1rem; font-weight:600; color:#0ea5e9;'>🤖 AI Health Assessment</div>
                                <div style='font-size:0.95rem; font-weight:600;'>{risk}</div>
                            </div>
                            <div class='remarks-box'>{clean_remarks}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.error("❌ A patient with this email already exists.")
                except Exception as ex:
                    st.error(f"❌ AI Analysis failed: {str(ex)}")

elif nav == "View Records":
    st.markdown("<div class='section-title'>📋 Patient Records</div>", unsafe_allow_html=True)

    search_query = st.text_input("🔍 Search by name or email", placeholder="Type to search...")

    patients = search_patients(search_query) if search_query else read_all_patients()

    if not patients:
        st.info("No records found.")
    else:
        st.markdown(f"<div style='color:#64748b; font-size:0.85rem; margin-bottom:12px;'>Showing {len(patients)} record(s)</div>", unsafe_allow_html=True)
        for p in patients:
            risk = get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol'])
            with st.expander(f"#{p['id']} · {p['full_name']} · {risk}"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Email:** {p['email']}")
                c1.markdown(f"**DOB:** {p['date_of_birth']}")
                c2.markdown(f"**Glucose:** {p['glucose']} mg/dL")
                c2.markdown(f"**Haemoglobin:** {p['haemoglobin']} g/dL")
                c3.markdown(f"**Cholesterol:** {p['cholesterol']} mg/dL")
                c3.markdown(f"**Added:** {p['created_at'][:10]}")
                if p.get('remarks'):
                    st.markdown(f"""<div class='remarks-box' style='margin-top:10px;'>
                        <strong style='color:#0ea5e9;'>AI Remarks:</strong><br>{p['remarks'].replace('**','').replace('*','').replace('??','').strip()}</div>""",
                        unsafe_allow_html=True)

elif nav == "Update Record":
    st.markdown("<div class='section-title'>Update Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"#{p['id']} · {p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to update", list(options.keys()))
        pid = options[selected]
        patient = read_patient_by_id(pid)

        if patient:
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("Full Name *", value=patient['full_name'])
                    email = st.text_input("Email Address *", value=patient['email'])
                    glucose = st.number_input("Glucose (mg/dL) *", value=float(patient['glucose']), min_value=0.0, max_value=600.0, step=0.1)
                with col2:
                    dob_val = datetime.strptime(patient['date_of_birth'], "%Y-%m-%d").date()
                    dob = st.date_input("Date of Birth *", value=dob_val, max_value=date.today())
                    haemoglobin = st.number_input("Haemoglobin (g/dL) *", value=float(patient['haemoglobin']), min_value=0.0, max_value=25.0, step=0.1)
                    cholesterol = st.number_input("Cholesterol (mg/dL) *", value=float(patient['cholesterol']), min_value=0.0, max_value=700.0, step=0.1)

                regen_ai = st.checkbox("Re-run AI Analysis", value=True, help="Regenerate AI health prediction with updated values")

                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    update_btn = st.form_submit_button("Update Patient", use_container_width=True)

            if update_btn:
                errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
                if errors:
                    for e in errors:
                        st.error(f"⚠️ {e}")
                else:
                    remarks = patient.get('remarks', '')
                    if regen_ai:
                        with st.spinner("Re-analyzing with updated data..."):
                            try:
                                remarks = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)
                            except Exception as ex:
                                st.warning(f"AI analysis failed, keeping old remarks: {ex}")

                    success = update_patient(pid, full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
                    if success:
                        st.success(f"✅ Patient #{pid} updated successfully!")
                        if remarks:
                            st.markdown(f"""<div class='mira-card'>
                                <div style='color:#0ea5e9; font-weight:600; margin-bottom:10px;'>🤖 Updated AI Remarks</div>
                                <div class='remarks-box'>{remarks}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.error("❌ Update failed. Email may already exist for another patient.")

elif nav == "Delete Record":
    st.markdown("<div class='section-title'>Delete Patient Record</div>", unsafe_allow_html=True)

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"#{p['id']} · {p['full_name']} ({p['email']})": p['id'] for p in patients}
        selected = st.selectbox("Select patient to delete", list(options.keys()))
        pid = options[selected]
        patient = read_patient_by_id(pid)

        if patient:
            risk = get_risk_level(patient['glucose'], patient['haemoglobin'], patient['cholesterol'])
            st.markdown(f"""
            <div class='mira-card' style='border-color:#ef444444;'>
                <div style='font-size:1rem; font-weight:600; color:#f1f5f9; margin-bottom:12px;'>Patient Details</div>
                <table style='width:100%; font-size:0.88rem; color:#94a3b8;'>
                    <tr><td style='padding:4px 0; width:50%;'><strong>Name:</strong> {patient['full_name']}</td>
                        <td><strong>Email:</strong> {patient['email']}</td></tr>
                    <tr><td><strong>DOB:</strong> {patient['date_of_birth']}</td>
                        <td><strong>Risk:</strong> {risk}</td></tr>
                    <tr><td><strong>Glucose:</strong> {patient['glucose']} mg/dL</td>
                        <td><strong>Haemoglobin:</strong> {patient['haemoglobin']} g/dL</td></tr>
                    <tr><td><strong>Cholesterol:</strong> {patient['cholesterol']} mg/dL</td><td></td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

            st.warning("⚠️ This action is permanent and cannot be undone.")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Confirm Delete", type="primary"):
                    if delete_patient(pid):
                        st.success(f"✅ Patient #{pid} — **{patient['full_name']}** has been deleted.")
                        st.rerun()
                    else:
                        st.error("❌ Deletion failed.")
            with col2:
                if st.button("❌ Cancel"):
                    st.info("Deletion cancelled.")
