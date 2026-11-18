
# Credigo — AI-Powered Credit Risk Investigation System

Credigo is an AI-powered credit risk investigation system designed to help financial institutions analyze customer information, assess credit risk, and generate structured investigation reports.

The system combines Machine Learning, Large Language Models (LLMs), and rule-based validation to support credit risk investigations and assist bank officers in making more informed decisions.

> **Important:** Credigo is a decision-support system. AI and ML outputs are recommendations only. Final lending decisions must be made by authorized human reviewers.

---

## Key Features

### 1. Customer Information Management
- Search customers using their National ID.
- Retrieve customer profiles and financial information.
- Manage customer accounts, employment records, and credit history.
- Manage loan applications and repayment records.

### 2. Credit Risk Assessment
- Analyze customer financial information.
- Predict potential credit default risk using Machine Learning.
- Evaluate relevant financial indicators.
- Generate risk assessment results.

### 3. AI-Powered Credit Investigation
- Use LLM-based analysis to interpret verified customer information.
- Orchestrate investigation workflows using LangGraph.
- Generate structured credit risk investigation reports.
- Provide recommendations with supporting evidence.

### 4. Data Validation and Credit Policy Checks
- Validate customer and financial information.
- Apply deterministic business rules.
- Identify missing, inconsistent, or potentially problematic information.
- Flag cases that require further investigation.

### 5. Human-in-the-Loop Review
- Support human review of AI-generated recommendations.
- Keep final credit decisions separate from automated predictions.
- Allow authorized staff to review investigation findings.

---

## System Architecture

```text
                 Bank Officer
                      |
                      v
             Streamlit Frontend
                      |
                      v
                FastAPI Backend
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
   PostgreSQL     ML Model      LangGraph
   Database       Prediction    AI Workflow
        |             |             |
        +-------------+-------------+
                      |
                      v
             Credit Risk Report
                      |
                      v
               Human Review
                      |
                      v
                Final Decision
```

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.11 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Machine Learning | Scikit-learn, XGBoost |
| LLM Integration | LangChain |
| AI Agent Workflow | LangGraph |
| Vector Database | ChromaDB, Pinecone |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |
| API Communication | REST API, Requests |
| Environment Management | uv |

---

## Project Structure

```text
Credigo/
│
├── backend/
│   ├── routers/
│   ├── services/
│   ├── schemas/
│   ├── dependence/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── app/
│   └── model/
│
├── models/
│
├── database/
│
├── api/
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

*The directory structure may evolve as the project develops.*

---

## Getting Started

### Prerequisites

- Python 3.11
- PostgreSQL 16
- uv
- Git

### 1. Clone the repository

```bash
git clone https://github.com/IttikornMafaka/Credigo.git
cd Credigo
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root.

Configure the required environment variables for:

- PostgreSQL connection
- LLM API credentials
- Other external services used by the application

Refer to `.env.example` for the required variable names.

**Never commit `.env` or API credentials to GitHub.**

### 4. Start the Backend

```bash
uv run uvicorn backend.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the Frontend

Open another terminal:

```bash
uv run streamlit run frontend/app.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

---

## Credit Risk Investigation Workflow

The system follows a structured investigation process:

1. Customer Identification
2. Customer Financial Data Retrieval
3. Data Validation
4. Machine Learning Risk Prediction
5. Credit Policy Evaluation
6. AI-Assisted Investigation
7. Credit Risk Report Generation
8. Human Review and Final Decision

The workflow separates predictive modeling, deterministic business rules, and LLM-based analysis to improve transparency and control.

---

## Responsible AI and Limitations

Credigo is developed as an educational and portfolio project.

- ML predictions are not guaranteed to represent actual default probabilities without proper calibration and validation.
- LLM-generated recommendations may contain errors and must be reviewed.
- Credit policy rules must be configured and validated against applicable institutional requirements.
- Sensitive customer information must be protected.
- The system is not intended for autonomous lending decisions or direct production use without additional security, compliance, fairness, and reliability testing.

---

## Future Improvements

- Docker and Docker Compose deployment.
- Automated backend and frontend testing.
- Improved ML model evaluation and calibration.
- Human review and decision audit trail.
- Enhanced monitoring and investigation history.
- Production-grade authentication and authorization.

---

## Project Purpose

Credigo demonstrates the integration of Backend Engineering, Database Management, Machine Learning, and LLM-based Agent Workflows to solve a practical financial technology problem.

The goal is to build an explainable and structured AI-assisted credit investigation system that helps human decision-makers work more efficiently.

---

## Author

**IttikornMafaka**

GitHub: https://github.com/IttikornMafaka
