

ai_predictor.py
Python

requirements(3).txt
Document

app(2).py
Python

mira_patients.db
File

.gitignore
File

database(1).py
Python

README(2).md
File

validators(1).py
Python
i want to wrk this on github

Yes. Your project can be hosted on GitHub, but you must fix a few things first.

1. Fix ai_predictor.py
Your file contains Git merge conflict markers, which will cause errors: 


<<<<<<< HEAD
=======
>>>>>>> 13844e0
Delete all conflict markers and keep only one version of the code.

2. Rename files
GitHub project should use these names:

app.py
database.py
ai_predictor.py
validators.py
requirements.txt
README.md
.gitignore
Currently your uploaded files have names like:

app(2).py
database(1).py
validators(1).py
requirements(3).txt
README(2).md
Rename them before uploading.

3. Do NOT upload
Your .gitignore already excludes the database file. 


Do not upload:

mira_patients.db
.streamlit/secrets.toml
4. Create GitHub repository structure
mira-health-platform/
│
├── app.py
├── ai_predictor.py
├── database.py
├── validators.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml   (local only, not uploaded)
5. Initialize Git locally
Open terminal inside project folder:

git init
git add .
git commit -m "Initial commit"
6. Create repository on GitHub
Create a new repository named:

mira-health-platform
Do NOT add README or .gitignore during creation since you already have them.

7. Push to GitHub
Replace YOUR_USERNAME:

git remote add origin https://github.com/YOUR_USERNAME/mira-health-platform.git

git branch -M main

git push -u origin main
8. One more important fix
Your README says the project uses Anthropic Claude AI, but your code uses the Groq API and Llama model. These do not match. 

 


Update the README to mention:

Groq API
Llama 3.3 70B
instead of Claude AI.

After that, the repository will be ready for GitHub.


bc4292a6-0f17-4eb7-ba14-98aafc8115d5.png

e938fa3d-4fb4-486c-b81a-940b55f82a22.db
File

c5c3724b-672c-4831-b5d8-8c106fe80057.gitignore
File

17d523bd-19b1-41a2-a2f1-4a688ad8808e.py
Python

aa7a3bb9-387f-4339-ad81-f09660fdd5c3.py
Python

d7df448b-0336-43d1-ae3e-41f4320693e0.md
File

35a1efef-5447-4c57-abe3-8c2230a1c82f.py
Python

00bedd27-cbc2-4061-8afb-7503bbcbdaff.txt
Document

0b132c70-6479-4954-9a43-990f134c71e0.py
Python

29d0d6e0-e5a0-4261-80b1-536f1fe63a6a.pyc
File

b5d0fc1c-e104-4777-bd4b-d026fd31db64.pyc
File

fe063ddd-0b51-409c-b471-e3c97406667d.pyc
File

e2cc3e34-a807-4ae9-ba94-b31bd23523f9.toml
File
these are ;local files and github files ,while streamlit app does not runs similar to ps streamlit

I found the main issue.

Your GitHub version still contains Git merge conflict markers in ai_predictor.py: 


<<<<<<< HEAD
=======
>>>>>>> 13844e0
If Streamlit Cloud pulls this file, the app will fail immediately with a syntax error.

Also check this carefully
Your code uses:

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
So on Streamlit Cloud you must add:

GROQ_API_KEY="your_key"
inside App Settings → Secrets.

Most likely causes
Merge conflict still present in GitHub repo ❌

GROQ_API_KEY not added in Streamlit secrets ❌

Wrong main file selected during deployment ❌

Deployment using an older commit ❌

I need one screenshot
Open your Streamlit deployment.

Copy the exact error message from:

Manage app → Logs
or take a screenshot of the error page.

The logs will tell us exactly whether it is:

SyntaxError from merge conflicts

Missing GROQ_API_KEY

Missing package

Database issue

Without the log, we would only be guessing. Send the Streamlit error log screenshot and I'll pinpoint the exact fix.


but api key will be visible to all

No. If you use Streamlit Secrets, visitors cannot see your API key.

Correct way
In Streamlit Cloud:

App → Settings → Secrets

Add:

GROQ_API_KEY = "your_actual_key"
Then save.

Your code:

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
will read the key securely from Streamlit Secrets. The key is not shown in your GitHub repository, not visible in your app, and not accessible to users.

Dangerous way ❌
Never do this:

client = Groq(api_key="gsk_xxxxxxxxx")
or commit a file containing:

GROQ_API_KEY = "gsk_xxxxxxxxx"
to GitHub.

Anyone viewing your repository could steal the key.

Important
I can see that one of the uploaded files contains a Groq API key. 


You should:

Delete that key from all project files.

Generate a new Groq API key from your account.

Put the new key only in Streamlit Secrets.

Also, if that key was ever pushed to GitHub, revoke it immediately and create a new one.

Now send the Streamlit deployment error log, because the API key visibility issue is separate from the reason your app is failing to run.


what sendgridgrid will do

SendGrid is an email delivery service.

In your MIRA health app, SendGrid would be used if you want features like:

Sending patient registration confirmation emails

Sending AI health reports to patients

Password reset emails

Appointment reminders

Notifications to doctors/admins

Example workflow:

Patient added
      ↓
MIRA generates AI report
      ↓
SendGrid sends email
      ↓
Patient receives report in inbox
Without SendGrid:

Your app works normally.

No emails are sent.

With SendGrid:

Your app can automatically email reports and notifications.

For your current MIRA project, I don't see any SendGrid code in the files you uploaded. Your app currently uses:

Streamlit

SQLite

Groq API

Plotly

and does not require SendGrid to run.

If Streamlit Cloud is asking for a SendGrid key, send a screenshot of that page. It may be coming from a template or deployment setting rather than your actual code.


ok is email registered for patent needed

No, an email field is not required for a patient health prediction application unless you actually use email-related features.

For your MIRA project, ask yourself:

Keep Email if:
You want to send health reports later.

You want a unique identifier for each patient.

You want patient notifications/reminders.

You want the project to look more like a real healthcare system.

Remove Email if:
You only need CRUD operations.

You are not sending emails.

This is mainly a portfolio/project demonstration.

Currently, your database makes email mandatory and unique: 


email TEXT NOT NULL UNIQUE
For a fresher-level portfolio project, I would keep the email field because:

It demonstrates form validation.

It demonstrates duplicate-record prevention.

It makes the project look more complete to recruiters.

You do not need SendGrid or email sending just because you store an email address. Storing an email and sending emails are two different things.

If your goal is to showcase this project for Data Analyst/Data Science/AI job applications, keeping the email field is a good choice.


ok ,then registered confirmation mail no newed ah

No, for your current MIRA project, a registration confirmation email is not necessary.

When a recruiter tests your project, they usually look for:

✅ CRUD operations
✅ Database integration
✅ Input validation
✅ AI integration (Groq/Llama)
✅ Dashboard and visualizations
✅ Clean UI
✅ GitHub repository
✅ Deployment

They usually do not expect email notifications in a health prediction CRUD project.

In fact, adding email can create extra complications:

Need SendGrid/Mailtrap/Gmail SMTP

Need API keys

Email delivery failures

Spam folder issues

Additional deployment configuration

For your portfolio project, the success message you already show is sufficient:

st.success("Patient registered successfully!")
You can mention in your resume or README:

Future Enhancements:

Email notifications

PDF health report generation

Doctor dashboard

Appointment reminders

That shows you know how the project can be extended without making the current version more complex.

So my recommendation: Don't add registration confirmation emails now. Focus on getting the Streamlit deployment working correctly first.


ok

Good.

Next, focus on these items in order:

Fix ai_predictor.py merge conflicts (<<<<<<< HEAD, =======, >>>>>>>) because the app will not run until those are removed.

Remove the exposed Groq API key from files and generate a new key. The uploaded secret should be treated as compromised.

Add the new key to Streamlit Secrets, not GitHub.

Redeploy the app on Streamlit Cloud.

If it still fails, open Manage App → Logs and send the exact error message or screenshot.

Once you send the deployment log, I can identify the precise issue instead of guessing.



Pasted text(18).txt
Document
i need css,effects,cards,hovers,floating,style,etc...

Your current UI is already better than a basic Streamlit app, but for a portfolio project I would add more modern effects.

Add this CSS below your existing CSS block. 


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
Also add a floating hero section at the top:

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
For recruiter impact, the highest-value additions are:

Animated metric cards

Glassmorphism panels

Hover effects

Gradient buttons

Glow effects

Custom loading spinner

Lottie animation on dashboard

Particle background

KPI cards with icons

Those changes make the app look much closer to a premium SaaS dashboard than a standard Streamlit project.


remove gridlines

To remove the gridlines from your Plotly charts, change this section:

Current code:

fig.update_layout(
    paper_bgcolor='#1e293b',
    plot_bgcolor='#162032',
    xaxis=dict(gridcolor='#334155', showgrid=True),
    yaxis=dict(gridcolor='#334155', showgrid=True),
)
Replace with:

fig.update_layout(
    paper_bgcolor='#1e293b',
    plot_bgcolor='#162032',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
)
Or, if you want an even cleaner modern dashboard look:

fig.update_xaxes(
    showgrid=False,
    zeroline=False,
    showline=False
)

fig.update_yaxes(
    showgrid=False,
    zeroline=False,
    showline=False
)
This will:

✅ Remove horizontal gridlines

✅ Remove vertical gridlines

✅ Remove the zero line

✅ Make the chart look cleaner and more premium

For your MIRA dashboard, I would also keep:

showticklabels=True
so users can still read the values while enjoying a clean, minimalist appearance.


deledted permanantly crt for  st.warning("⚠️ This action cannot be restored.")?

Your sentence is understandable, but these are better options:

st.warning("⚠️ This action is permanent and cannot be undone.")
or

st.warning("⚠️ Once deleted, this record cannot be restored.")
or

st.warning("⚠️ This patient record will be permanently deleted.")
For a professional application, I recommend:

st.warning("⚠️ This action is permanent and cannot be undone.")
It is the most common wording used in production applications.



Pasted text(19).txt
Document
all need css,cards ,effects,hovers,styles,floating,etc,..

Your current design is already around 7.5/10 visually. 


To make it look like a premium SaaS dashboard (9.5/10), add these improvements:

1. Hide Streamlit Header/Footer
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
2. Floating Sidebar
[data-testid="stSidebar"] {
    border-radius: 0 20px 20px 0;
    box-shadow: 5px 0 30px rgba(0,0,0,.4);
}
3. Animated Gradient Border Cards
.mira-card {
    position: relative;
    overflow: hidden;
}

.mira-card::before {
    content: "";
    position: absolute;
    inset: 0;
    padding: 1px;
    background: linear-gradient(
        45deg,
        #0ea5e9,
        #06b6d4,
        #38bdf8,
        #0ea5e9
    );
    border-radius: 16px;
    opacity: 0;
    transition: .4s;
}

.mira-card:hover::before {
    opacity: 1;
}
4. Floating Animation
@keyframes floating {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-8px);}
    100% {transform: translateY(0px);}
}

.metric-box {
    animation: floating 4s ease-in-out infinite;
}
5. Premium Data Table
[data-testid="stDataFrame"] {
    border: 1px solid #0ea5e9;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(14,165,233,.15);
}
6. Glass Sidebar Info Card
Replace your sidebar information box with:

<div style="
background:rgba(255,255,255,.05);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,.08);
border-radius:18px;
padding:18px;">
7. Dashboard KPI Glow
.metric-value {
    text-shadow:
        0 0 10px rgba(14,165,233,.5),
        0 0 20px rgba(14,165,233,.3);
}
8. Modern Scrollbar
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #162032;
}

::-webkit-scrollbar-thumb {
    background: #0ea5e9;
    border-radius: 20px;
}
9. Animated Hero Section
Add below your MIRA title:

<div style="
font-size:1rem;
color:#94a3b8;
animation: pulse 3s infinite;">
AI-Powered Healthcare Intelligence
</div>
@keyframes pulse {
    0% {opacity:.5;}
    50% {opacity:1;}
    100% {opacity:.5;}
}
10. Better Empty State
Instead of:

No patient records yet
Use:

<div style='font-size:5rem;'>🩺</div>
<h2>No Patient Records</h2>
<p>Start by registering your first patient.</p>
The biggest visual upgrades will come from:

Glassmorphism

Floating cards

Animated borders

Sidebar shadow

KPI glow

Cleaner charts without gridlines

Those five changes alone will make the app feel significantly more polished.


50158007-4b09-4214-96e0-59d0271a5ba8.png
add patient shows nothing

The screenshot shows only the two header sections. There are no metric cards, sidebar content, or forms visible.

This usually means one of these is happening:

Most likely cause
You changed:

nav = st.radio(
    "Navigation",
    ["Home", " Add Patient", "View Records", "Update Record", "Delete Record"]
)
Notice " Add Patient" has a leading space. 


But your condition is:

elif nav == "Add Patient":
without the leading space.

Therefore:

nav == " Add Patient"   # True
nav == "Add Patient"    # False
The Add Patient block never executes.

Fix
Change:

" Add Patient"
to:

"Add Patient"
or change the condition to:

elif nav.strip() == "Add Patient":
Another issue
Your screenshot does not show the sidebar at all. Check whether you accidentally hid it with custom CSS.

Try temporarily removing:

[data-testid="stSidebar"]
customizations and redeploy.

Verify
Add this temporarily near the top:

st.write("Current page:", nav)
Then click Add Patient.

If it displays:

Current page:  Add Patient
(with a space before Add), then that is exactly the bug.

Send a screenshot of the sidebar menu or the value printed by st.write(nav) and I can confirm.


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime

from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from ai_predictor import predict_health_condition, get_risk_level
from validators import validate_patient_form

─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
page_title="MIRA – Medical Intelligence",
page_icon="🏥",
layout="wide",
initial_sidebar_state="expanded"
)

─── INIT DB ────────────────────────────────────────────────────────────────────
init_db()

─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""

""", unsafe_allow_html=True)

─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
st.markdown("""

MIRA
MEDICAL INTELLIGENCE


""", unsafe_allow_html=True)

nav = st.radio(
    "Navigation",
    ["🏠 Dashboard", "➕ Add Patient", "📋 View Records", "✏️ Update Record", "🗑️ Delete Record"],
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='background:#162032; border:1px solid #1e3a5f; border-radius:10px; padding:14px; font-size:0.78rem; color:#64748b;'>
    <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>⚕️ AI Engine</div>
    Powered by Claude AI (Anthropic)<br><br>
    <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>🗄️ Storage</div>
    SQLite — Persistent Local DB<br><br>
    <div style='color:#0ea5e9; font-weight:600; margin-bottom:8px;'>🔬 Parameters</div>
    Glucose · Haemoglobin · Cholesterol
</div>
""", unsafe_allow_html=True)
─── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""

════════════════════════════════════════════════════════════════════════════════
🏠 DASHBOARD
════════════════════════════════════════════════════════════════════════════════
if nav == "🏠 Dashboard":
patients = read_all_patients()
total = len(patients)
high_risk = sum(1 for p in patients if "🔴" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
moderate = sum(1 for p in patients if "🟡" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))
healthy = sum(1 for p in patients if "🟢" in get_risk_level(p['glucose'], p['haemoglobin'], p['cholesterol']))

# Metrics
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
            paper_bgcolor='#1e293b', plot_bgcolor='#162032',
            font=dict(color='#94a3b8', size=11),
            legend=dict(bgcolor='#1e293b', bordercolor='#334155'),
            xaxis=dict(gridcolor='#334155', showgrid=True),
            yaxis=dict(gridcolor='#334155', showgrid=True),
            margin=dict(l=0, r=0, t=10, b=0), height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("<div class='section-title'>🎯 Risk Distribution</div>", unsafe_allow_html=True)
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
════════════════════════════════════════════════════════════════════════════════
➕ ADD PATIENT
════════════════════════════════════════════════════════════════════════════════
elif nav == "➕ Add Patient":
st.markdown("➕ Register New Patient", unsafe_allow_html=True)

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
        with st.spinner("🤖 MIRA AI is analyzing patient data..."):
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
════════════════════════════════════════════════════════════════════════════════
📋 VIEW RECORDS
════════════════════════════════════════════════════════════════════════════════
elif nav == "📋 View Records":
st.markdown("📋 Patient Records", unsafe_allow_html=True)

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
            c1.markdown(f"**📧 Email:** {p['email']}")
            c1.markdown(f"**🎂 DOB:** {p['date_of_birth']}")
            c2.markdown(f"**🩸 Glucose:** {p['glucose']} mg/dL")
            c2.markdown(f"**💉 Haemoglobin:** {p['haemoglobin']} g/dL")
            c3.markdown(f"**🫀 Cholesterol:** {p['cholesterol']} mg/dL")
            c3.markdown(f"**📅 Added:** {p['created_at'][:10]}")
            if p.get('remarks'):
                st.markdown(f"""<div class='remarks-box' style='margin-top:10px;'>
                    <strong style='color:#0ea5e9;'>🤖 AI Remarks:</strong><br>{p['remarks'].replace('**','').replace('*','').replace('??','').strip()}</div>""",
                    unsafe_allow_html=True)
════════════════════════════════════════════════════════════════════════════════
✏️ UPDATE RECORD
════════════════════════════════════════════════════════════════════════════════
elif nav == "✏️ Update Record":
st.markdown("✏️ Update Patient Record", unsafe_allow_html=True)

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

            regen_ai = st.checkbox("🤖 Re-run AI Analysis", value=True, help="Regenerate AI health prediction with updated values")

            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                update_btn = st.form_submit_button("💾 Update Patient", use_container_width=True)

        if update_btn:
            errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
            if errors:
                for e in errors:
                    st.error(f"⚠️ {e}")
            else:
                remarks = patient.get('remarks', '')
                if regen_ai:
                    with st.spinner("🤖 Re-analyzing with updated data..."):
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
════════════════════════════════════════════════════════════════════════════════
🗑️ DELETE RECORD
════════════════════════════════════════════════════════════════════════════════
elif nav == "🗑️ Delete Record":
st.markdown("🗑️ Delete Patient Record", unsafe_allow_html=True)

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
                <tr><td style='padding:4px 0; width:50%;'>📋 <strong>Name:</strong> {patient['full_name']}</td>
                    <td>📧 <strong>Email:</strong> {patient['email']}</td></tr>
                <tr><td>🎂 <strong>DOB:</strong> {patient['date_of_birth']}</td>
                    <td>🎯 <strong>Risk:</strong> {risk}</td></tr>
                <tr><td>🩸 <strong>Glucose:</strong> {patient['glucose']} mg/dL</td>
                    <td>💉 <strong>Haemoglobin:</strong> {patient['haemoglobin']} g/dL</td></tr>
                <tr><td>🫀 <strong>Cholesterol:</strong> {patient['cholesterol']} mg/dL</td><td></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

        st.warning("⚠️ This action is permanent and cannot be undone.")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Confirm Delete", type="primary"):
                if delete_patient(pid):
                    st.success(f"✅ Patient #{pid} — **{patient['full_name']}** has been deleted.")
                    st.rerun()
                else:
                    st.error("❌ Deletion failed.")
        with col2:
            if st.button("❌ Cancel"):
                st.info("Deletion cancelled.")

Close
