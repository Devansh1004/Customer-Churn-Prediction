import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_URL = os.getenv("API_URL")

if not API_URL:
    raise RuntimeError("API_URL is not set")

def predict_churn(data : dict):
    response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
    response.raise_for_status()
    return response.json()

def get_pred_stats():
    response = requests.get(f"{API_URL}/predictions/stats", timeout=10)
    response.raise_for_status()
    return response.json()

def get_predictions(limit: int = 20):
    response = requests.get(f"{API_URL}/predictions", timeout=10)
    response.raise_for_status()
    return response.json()