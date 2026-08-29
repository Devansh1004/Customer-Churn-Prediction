from fastapi import FastAPI
from api.schemas import Response, Request
import joblib
import json
from src.inference import prediction

app = FastAPI()

model = None
try:
    model = joblib.load("models/churn_pipeline.pkl")
except Exception as e:
    print("Exception : ", e)

config = None
with open("models/model_config.json", 'r') as f:
    config = json.load(f)

@app.get("/")
def home_page():
    return {
        'message' : 'Credit Card Churn Prediction Model'
    }
    
@app.get("/health")
def get_health():
    model_load = False if model is None else True
    config_load = False if config is None else True
    return {
        'message' : 'OK',
        'model_loaded' : model_load,
        'config_loaded' : config_load
    }
    
@app.post("/predict", response_model=Response)
def predict(request : Request):
    return prediction(request.model_dump(), model, config)