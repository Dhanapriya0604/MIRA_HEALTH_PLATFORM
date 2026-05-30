import anthropic
import json

def predict_health_condition(full_name: str, date_of_birth: str, glucose: float, haemoglobin: float, cholesterol: float) -> str:
    """
    Uses Claude AI (via Anthropic API) to generate a health risk prediction
    based on patient blood test results.
    """
    import streamlit as st
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    prompt = f"""You are a medical AI assistant. Analyze the following patient blood test results and provide a structured health assessment.

Patient Information:
- Name: {full_name}
- Date of Birth: {date_of_birth}
- Glucose Level: {glucose} mg/dL
- Haemoglobin Level: {haemoglobin} g/dL
- Cholesterol Level: {cholesterol} mg/dL

Clinical Reference Ranges:
- Glucose: 70–99 mg/dL (Normal Fasting); 100–125 (Pre-diabetic); >126 (Diabetic risk)
- Haemoglobin: 12.0–17.5 g/dL (Normal varies by sex); <12 may indicate Anaemia
- Cholesterol: <200 mg/dL (Desirable); 200–239 (Borderline); >240 (High risk)

Please provide:
1. Risk Assessment: Identify any abnormal values and associated conditions
2. Health Status: Overall health status (Healthy / At Risk / Requires Medical Attention)
3. Key Findings: 2–3 bullet points of key observations
4. Recommendation: One concise clinical recommendation

Keep the response concise, professional, and clinically relevant. Format as a brief medical remark (max 80 words)."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text.strip()


def get_risk_level(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    """Quick rule-based risk classification for UI badge display."""
    risk_score = 0

    # Glucose risk
    if glucose > 126:
        risk_score += 3
    elif glucose > 99:
        risk_score += 1

    # Haemoglobin risk
    if haemoglobin < 8:
        risk_score += 3
    elif haemoglobin < 12:
        risk_score += 2

    # Cholesterol risk
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
