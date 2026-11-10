# Customer Churn Prediction

An end-to-end credit card customer churn prediction system: an XGBoost model served through a FastAPI backend, with prediction logging to a PostgreSQL database, SHAP-based explanations, and a Streamlit dashboard.

## Features

- **XGBoost churn model** (scikit-learn pipeline) with a tuned decision threshold (0.22).
- **Display probability**: the raw model probability is rescaled into a more business-friendly score, since the optimal threshold (0.22) is too low to be intuitive for flagging customers.
- **SHAP explanations** for each prediction, showing which features drove the result.
- **FastAPI REST API** with async SQLAlchemy persistence of every prediction.
- **Streamlit dashboard** with a prediction form and prediction statistics/history.
- **Docker / Docker Compose** setup for the API and dashboard.

## Project Structure

```
├── main.py                  # App entry point (uvicorn main:app)
├── create_tables.py         # Creates the database tables
├── api/                     # FastAPI app and request/response schemas
├── src/inference.py         # Prediction + SHAP logic
├── database/                # SQLAlchemy models, session, CRUD
├── dashboard/               # Streamlit dashboard (Dashboard.py, pages/)
├── models/                  # Trained pipeline, SHAP explainer, model config
├── Dockerfile               # API image
├── Dockerfile.streamlit     # Dashboard image
└── docker-compose.yml
```

## API Endpoints

| Method | Path                  | Description                                  |
|--------|-----------------------|----------------------------------------------|
| GET    | `/`                   | Welcome message                              |
| GET    | `/health`             | Model/config/explainer load status, version  |
| POST   | `/predict`            | Predict churn, returns SHAP values, logs to DB |
| GET    | `/predictions`        | Recent prediction logs (`limit`, 1–500)      |
| GET    | `/predictions/stats`  | Aggregate prediction statistics              |

Interactive docs are available at `http://localhost:8000/docs`.

## Getting Started

### Prerequisites

- Python 3.12
- A PostgreSQL database (async driver `asyncpg`)

### Configuration

Create a `.env` file in the project root (it is git-ignored):

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
```

The dashboard reads `API_URL` (defaults are set in Docker Compose to `http://api:8000`).

### Run locally

```bash
python -m venv churn_pred_env
source churn_pred_env/bin/activate      # Windows: churn_pred_env\Scripts\activate
pip install -r requirements.txt

python create_tables.py                 # one-time table creation
uvicorn main:app --reload               # API on :8000

# in a second terminal
export API_URL=http://localhost:8000    # Windows PowerShell: $env:API_URL="http://localhost:8000"
streamlit run dashboard/Dashboard.py    # Dashboard on :8501
```

### Run with Docker

```bash
docker compose up --build
```

- API: http://localhost:8000
- Dashboard: http://localhost:8501

## Tech Stack

Python, XGBoost, scikit-learn, SHAP, FastAPI, SQLAlchemy (async), PostgreSQL, Streamlit, Docker.

## Notes

- Model artifacts (`models/*.pkl`) must be loaded with the same `xgboost` and `scikit-learn` versions used for training (see `requirements.txt`); mismatches cause the model to fail to load.
