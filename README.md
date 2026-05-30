# 🏥 MIRA — Medical Intelligence Robotic Automation

> **Health Prediction Platform** | AI-Powered Patient Analytics | Built with Python & Streamlit

---

## 📌 Overview

**MIRA** is a full-stack health prediction application that collects patient blood test data, performs intelligent AI-based health risk assessment using the **Anthropic Claude API**, and stores all records persistently in **SQLite**. It supports complete **CRUD operations** with a polished, production-grade UI.

Built as part of a technical assessment for the **Junior AI/ML Developer** position.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Health Prediction** | Claude AI analyzes Glucose, Haemoglobin & Cholesterol values |
| 📊 **Interactive Dashboard** | Plotly charts — line trends + risk distribution donut chart |
| 🗄️ **Persistent Storage** | SQLite database with full CRUD operations |
| 🔍 **Patient Search** | Search records by name or email |
| ✅ **Data Validation** | Email format, future DOB guard, numeric range checks |
| 🎨 **Medical-grade UI** | Dark healthcare theme, Space Mono + Inter typography |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Backend** | Python 3.11+ |
| **AI/ML API** | Anthropic Claude (`claude-sonnet-4-20250514`) |
| **Database** | SQLite3 (via Python standard library) |
| **Deployment** | Streamlit Community Cloud / Local |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mira-health-platform.git
cd mira-health-platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
# Linux / macOS
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows
set ANTHROPIC_API_KEY=your-api-key-here
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
mira-health-platform/
├── app.py              # Main Streamlit application (UI + navigation)
├── database.py         # SQLite CRUD operations layer
├── ai_predictor.py     # Claude AI health prediction module
├── validators.py       # Input validation utilities
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🔬 Blood Parameter Reference Ranges

| Parameter | Normal | At Risk | High Risk |
|---|---|---|---|
| **Glucose** | 70–99 mg/dL | 100–125 mg/dL | >126 mg/dL |
| **Haemoglobin** | 12.0–17.5 g/dL | 8–12 g/dL | <8 g/dL |
| **Cholesterol** | <200 mg/dL | 200–239 mg/dL | >240 mg/dL |

---

## 🧠 AI Integration

The app uses the **Anthropic Claude API** (`claude-sonnet-4-20250514`) to:
- Evaluate blood test values against clinical reference ranges
- Identify potential health conditions (diabetes risk, anaemia, cardiovascular risk)
- Generate a concise clinical remark stored in the `Remarks` field

```python
# ai_predictor.py — core function
remarks = predict_health_condition(full_name, dob, glucose, haemoglobin, cholesterol)
```

---

## 📸 Application Screenshots

| Dashboard | Add Patient | Records View |
|---|---|---|
| Metrics + Charts | AI-powered form | Searchable table |

---

## 👩‍💻 Developer

**Dhanapriya D**  
M.Sc. Data Science — Bharathidasan University  
📧 [your-email@example.com]  
🔗 [linkedin.com/in/dhanapriya-d2004](https://linkedin.com/in/dhanapriya-d2004)

---

## ⚠️ Security Note

All API keys and sensitive configuration values have been **removed** from this repository.  
Use environment variables to configure your `ANTHROPIC_API_KEY`.

---

*Built with ❤️ using Python, Streamlit, and Anthropic Claude AI*
