# MEDINSIGHT — AI-Powered Health Risk Assessment Platform

MedInsight is a health prediction web application built with Python and Streamlit. It collects patient blood test data, performs AI-based health risk assessment using the Groq API, and stores all records persistently in SQLite. The application supports complete CRUD operations with a clean, production-grade interface.

---

## Features

- AI Health Prediction: Groq API with Llama 3.3 70B analyses Glucose, Haemoglobin, and Cholesterol values and generates a clinical remark
- Interactive Dashboard: Plotly bar chart for blood parameter trends and donut chart for risk distribution
- Persistent Storage: SQLite database with full Create, Read, Update, and Delete operations
- Patient Search: Search records by name or email in real time
- Data Validation: Email format check, future date of birth guard, and numeric range validation for all blood values
- Risk Scoring: Rule-based scoring system categorises patients as Healthy, Moderate Risk, or High Risk

---

## Tech Stack

     | Layer                                       | Technology                                |
     |---------------------------------------------|-------------------------------------------|
     | Frontend                                    | Streamlit, Plotly, Custom CSS             | 
     | Backend                                     | Python 3.11+                              |
     | AI API                                      | Groq API — llama-3.3-70b-versatile        |
     | Database                                    | SQLite3 (Python standard library)         |

---

## Project Structure

```
medinsight/
├── app.py              # Main Streamlit application — UI and navigation
├── database.py         # SQLite CRUD operations
├── ai_predictor.py     # Groq API health prediction module
├── validators.py       # Input validation utilities
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MEDINSIGHT
cd MEDINSIGHT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.streamlit/secrets.toml` file in the project root:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

A free API key is available at [console.groq.com](https://console.groq.com).

### 4. Run the application

```bash
streamlit run app.py
```

---

## Blood Parameter Reference Ranges

                  | Parameter    | Normal          | At Risk         | High Risk    |
                  |--------------|-----------------|-----------------|--------------|
                  | Glucose      | 70-99 mg/dL     | 100-125 mg/dL   | >126 mg/dL   |
                  | Haemoglobin  | 12.0-17.5 g/dL  | 8.0-12.0 g/dL   | <8.0 g/dL    |
                  | Cholesterol  | <200 mg/dL      | 200-239 mg/dL   | >240 mg/dL   |

---

## AI Integration

The application uses the Groq API with the `llama-3.3-70b-versatile` model to evaluate a patient's blood test values against clinical reference ranges and generate a concise 3-sentence clinical remark. The remark is stored in the database and displayed alongside the patient record.

A secondary rule-based scoring function provides an instant risk category label as Healthy, Moderate Risk, or High Risk used across the dashboard and records view.

---

## Application Pages

        | Page           | Description                                                            |
        |----------------|------------------------------------------------------------------------|
        | Home           | KPI metrics, blood parameter bar chart, risk donut chart, recent table |
        | Add Patient    | Validated form with AI remark generated on save                        |
        | View Records   | Searchable list with gauge charts and AI remarks per patient           |
        | Update Record  | Pre-filled edit form with optional AI remark regeneration              |
        | Delete Record  | Patient summary with confirmation before permanent deletion            |

---

## Security

All API keys and sensitive configuration values have been removed from this repository. Use `.streamlit/secrets.toml` for local development or Streamlit Cloud secrets for deployment.
