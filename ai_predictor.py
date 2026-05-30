from groq import Groq
import streamlit as st
import re

def predict_health_condition(full_name, date_of_birth, glucose, haemoglobin, cholesterol):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"""You are a medical AI assistant. Analyze these patient blood test results.

Patient: {full_name}, DOB: {date_of_birth}
Glucose:     {glucose} mg/dL    (Normal: 70–99)
Haemoglobin: {haemoglobin} g/dL  (Normal: 12.0–17.5)
Cholesterol: {cholesterol} mg/dL (Normal: under 200)

Write a plain text clinical remark in exactly 3 sentences. No bullet points, no markdown, no asterisks, no special characters.
Sentence 1: Overall health status (Healthy / At Risk / Requires Medical Attention) and why.
Sentence 2: Key findings from the blood values.
Sentence 3: One clear recommendation."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    clean = re.sub(r'\*+', '', raw)
    clean = re.sub(r'#+\s*', '', clean)
    clean = re.sub(r'\?+\s*', '', clean)
    clean = clean.strip()
    return clean

def get_risk_level(glucose, haemoglobin, cholesterol):
    risk_score = 0
    if glucose > 126:
        risk_score += 3
    elif glucose > 99:
        risk_score += 1

    if haemoglobin < 8:
        risk_score += 3
    elif haemoglobin < 12:
        risk_score += 2

    if cholesterol > 240:
        risk_score += 3
    elif cholesterol > 200:
        risk_score += 1

    if risk_score >= 5:
        return "🔴 High Risk"
    elif risk_score >= 2:
        return "🟡 Moderate Risk"
    else:
        return "🟢 Healthy"
