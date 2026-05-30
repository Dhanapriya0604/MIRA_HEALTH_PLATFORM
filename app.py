import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from ai_predictor import predict_health_condition, get_risk_level
from validators import validate_patient_form

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MIRA — Medical Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --border:    #1e2d40;
    --accent:    #00d4aa;
    --accent2:   #3b82f6;
    --warn:      #f59e0b;
    --danger:    #ef4444;
    --text:      #e2e8f0;
    --muted:     #64748b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: #0a0e1a;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.5rem 1.2rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Section header */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

/* Risk badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-yellow { background: #1c1400; color: #facc15; border: 1px solid #854d0e; }
.badge-red    { background: #1c0a0a; color: #f87171; border: 1px solid #991b1b; }

/* Cards */
.patient-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.patient-card:hover { border-color: var(--accent); }

/* Logo */
.logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.02em;
}
.logo-sub {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-transform: uppercase;
}

/* Divider */
hr { border-color: var(--border); }

/* Success / error */
.stSuccess { background: #052e16 !important; color: #4ade80 !important; }
.stError   { background: #1c0a0a !important; color: #f87171 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 8px; }

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-text">🏥 MIRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Medical Intelligence Robotic Automation</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "➕ Add Patient", "📋 View Records", "✏️ Edit Patient", "🗑️ Delete Patient"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    patients = read_all_patients()
    st.markdown(f'<p class="section-header">System Stats</p>', unsafe_allow_html=True)
    st.markdown(f"**{len(patients)}** total patients")

    risks = [get_risk_level(p["glucose"], p["haemoglobin"], p["cholesterol"]) for p in patients]
    high   = sum(1 for r in risks if "High" in r)
    mod    = sum(1 for r in risks if "Moderate" in r)
    healthy = sum(1 for r in risks if "Healthy" in r)
    st.markdown(f"🔴 High Risk: **{high}** &nbsp; 🟡 Moderate: **{mod}** &nbsp; 🟢 Healthy: **{healthy}**", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="logo-sub">v1.0.0 · Groq + Llama 3.3</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown("## 📊 Dashboard")
    st.markdown("Real-time overview of patient health analytics.")
    st.markdown("---")

    patients = read_all_patients()

    if not patients:
        st.info("No patient records yet. Add your first patient using **➕ Add Patient**.")
    else:
        df = pd.DataFrame(patients)

        # KPI Row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Patients", len(df))
        c2.metric("Avg Glucose", f"{df['glucose'].mean():.1f} mg/dL")
        c3.metric("Avg Haemoglobin", f"{df['haemoglobin'].mean():.1f} g/dL")
        c4.metric("Avg Cholesterol", f"{df['cholesterol'].mean():.1f} mg/dL")

        st.markdown("---")

        col_left, col_right = st.columns(2)

        # Line chart — blood values per patient
        with col_left:
            st.markdown('<p class="section-header">Blood Parameter Trends</p>', unsafe_allow_html=True)
            fig_line = go.Figure()
            names = df["full_name"].str.split().str[0]  # first names
            fig_line.add_trace(go.Scatter(x=names, y=df["glucose"],      mode="lines+markers", name="Glucose",      line=dict(color="#00d4aa", width=2)))
            fig_line.add_trace(go.Scatter(x=names, y=df["haemoglobin"],  mode="lines+markers", name="Haemoglobin",  line=dict(color="#3b82f6", width=2)))
            fig_line.add_trace(go.Scatter(x=names, y=df["cholesterol"],  mode="lines+markers", name="Cholesterol",  line=dict(color="#f59e0b", width=2)))
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=11),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="#1e2d40"), yaxis=dict(gridcolor="#1e2d40"),
                margin=dict(l=10, r=10, t=10, b=10), height=300,
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # Donut — risk distribution
        with col_right:
            st.markdown('<p class="section-header">Risk Distribution</p>', unsafe_allow_html=True)
            risk_labels = [get_risk_level(p["glucose"], p["haemoglobin"], p["cholesterol"]) for p in patients]
            risk_counts = pd.Series(risk_labels).value_counts()
            fig_donut = go.Figure(go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                hole=0.6,
                marker_colors=["#00d4aa", "#f59e0b", "#ef4444"],
            ))
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=11),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10, r=10, t=10, b=10), height=300,
                showlegend=True,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Recent records table
        st.markdown("---")
        st.markdown('<p class="section-header">Recent Records</p>', unsafe_allow_html=True)
        display_df = df[["full_name", "date_of_birth", "email", "glucose", "haemoglobin", "cholesterol", "remarks"]].head(10)
        display_df.columns = ["Name", "DOB", "Email", "Glucose", "Haemoglobin", "Cholesterol", "AI Remarks"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ADD PATIENT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Patient":
    st.markdown("## ➕ Add New Patient")
    st.markdown("Enter patient details. AI will generate a health remark automatically.")
    st.markdown("---")

    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full Name *", placeholder="e.g. Priya Sharma")
            email     = st.text_input("Email Address *", placeholder="priya@example.com")
            glucose   = st.number_input("Glucose (mg/dL) *", min_value=0.1, max_value=600.0, value=90.0, step=0.1)
        with c2:
            dob         = st.date_input("Date of Birth *", value=date(1990, 1, 1), max_value=date.today())
            haemoglobin = st.number_input("Haemoglobin (g/dL) *", min_value=0.1, max_value=25.0, value=13.5, step=0.1)
            cholesterol = st.number_input("Cholesterol (mg/dL) *", min_value=0.1, max_value=700.0, value=180.0, step=0.1)

        st.markdown("")
        submitted = st.form_submit_button("🤖 Analyse & Save Patient", use_container_width=True)

    if submitted:
        errors = validate_patient_form(full_name, str(dob), email, glucose, haemoglobin, cholesterol)
        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            with st.spinner("🧠 AI is analysing blood test results..."):
                remarks = predict_health_condition(full_name, str(dob), glucose, haemoglobin, cholesterol)

            patient_id = create_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
            if patient_id:
                st.success(f"✅ Patient **{full_name}** saved successfully (ID: {patient_id})")
                risk = get_risk_level(glucose, haemoglobin, cholesterol)
                st.markdown(f"**Risk Level:** {risk}")
                st.info(f"**AI Remark:** {remarks}")
            else:
                st.error("❌ Email already exists. Please use a unique email address.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: VIEW RECORDS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 View Records":
    st.markdown("## 📋 Patient Records")
    st.markdown("---")

    search_q = st.text_input("🔍 Search by name or email", placeholder="Type to search...")
    st.markdown("")

    patients = search_patients(search_q) if search_q else read_all_patients()

    if not patients:
        st.info("No records found.")
    else:
        st.markdown(f'<p class="section-header">{len(patients)} record(s) found</p>', unsafe_allow_html=True)

        for p in patients:
            risk = get_risk_level(p["glucose"], p["haemoglobin"], p["cholesterol"])
            badge_cls = "badge-red" if "High" in risk else ("badge-yellow" if "Moderate" in risk else "badge-green")

            with st.expander(f"🧑‍⚕️ {p['full_name']}  ·  {p['email']}  ·  {risk}", expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**DOB:** {p['date_of_birth']}")
                c2.markdown(f"**ID:** {p['id']}")
                c3.markdown(f"**Added:** {p['created_at'][:10]}")

                c4, c5, c6 = st.columns(3)
                c4.metric("Glucose", f"{p['glucose']} mg/dL")
                c5.metric("Haemoglobin", f"{p['haemoglobin']} g/dL")
                c6.metric("Cholesterol", f"{p['cholesterol']} mg/dL")

                st.markdown(f"**🤖 AI Remarks:** {p['remarks'] or '_No remark generated_'}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EDIT PATIENT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Edit Patient":
    st.markdown("## ✏️ Edit Patient Record")
    st.markdown("---")

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"[{p['id']}] {p['full_name']} — {p['email']}": p["id"] for p in patients}
        selected = st.selectbox("Select patient to edit", list(options.keys()))
        pid = options[selected]
        p = read_patient_by_id(pid)

        if p:
            with st.form("edit_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_name  = st.text_input("Full Name", value=p["full_name"])
                    new_email = st.text_input("Email", value=p["email"])
                    new_gluc  = st.number_input("Glucose (mg/dL)", value=float(p["glucose"]), min_value=0.1, max_value=600.0, step=0.1)
                with c2:
                    new_dob   = st.date_input("Date of Birth", value=datetime.strptime(p["date_of_birth"], "%Y-%m-%d").date())
                    new_haem  = st.number_input("Haemoglobin (g/dL)", value=float(p["haemoglobin"]), min_value=0.1, max_value=25.0, step=0.1)
                    new_chol  = st.number_input("Cholesterol (mg/dL)", value=float(p["cholesterol"]), min_value=0.1, max_value=700.0, step=0.1)

                regenerate = st.checkbox("🤖 Re-generate AI Remarks", value=False)
                save_btn   = st.form_submit_button("💾 Save Changes", use_container_width=True)

            if save_btn:
                errors = validate_patient_form(new_name, str(new_dob), new_email, new_gluc, new_haem, new_chol)
                if errors:
                    for e in errors:
                        st.error(f"⚠️ {e}")
                else:
                    remarks = p["remarks"]
                    if regenerate:
                        with st.spinner("🧠 Re-generating AI remarks..."):
                            remarks = predict_health_condition(new_name, str(new_dob), new_gluc, new_haem, new_chol)

                    success = update_patient(pid, new_name, str(new_dob), new_email, new_gluc, new_haem, new_chol, remarks)
                    if success:
                        st.success(f"✅ Patient **{new_name}** updated successfully.")
                        if regenerate:
                            st.info(f"**New AI Remark:** {remarks}")
                    else:
                        st.error("❌ Update failed. Email may already be in use.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DELETE PATIENT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Delete Patient":
    st.markdown("## 🗑️ Delete Patient Record")
    st.markdown("---")

    patients = read_all_patients()
    if not patients:
        st.info("No patient records found.")
    else:
        options = {f"[{p['id']}] {p['full_name']} — {p['email']}": p["id"] for p in patients}
        selected = st.selectbox("Select patient to delete", list(options.keys()))
        pid = options[selected]
        p   = read_patient_by_id(pid)

        if p:
            st.markdown("### ⚠️ You are about to delete:")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Name:** {p['full_name']}")
            c2.markdown(f"**Email:** {p['email']}")
            c3.markdown(f"**DOB:** {p['date_of_birth']}")

            c4, c5, c6 = st.columns(3)
            c4.metric("Glucose", f"{p['glucose']} mg/dL")
            c5.metric("Haemoglobin", f"{p['haemoglobin']} g/dL")
            c6.metric("Cholesterol", f"{p['cholesterol']} mg/dL")

            st.markdown("")
            confirm = st.checkbox("✅ I confirm I want to permanently delete this record")

            if st.button("🗑️ Delete Patient", disabled=not confirm):
                if delete_patient(pid):
                    st.success(f"✅ Patient **{p['full_name']}** has been deleted.")
                    st.rerun()
                else:
                    st.error("❌ Deletion failed.")
