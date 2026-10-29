import json
import joblib

from fastapi import FastAPI, Depends, Query
from api.schemas import Response, Request, DBResponse, PredictionStatsresponse

from src.inference import prediction

from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from database.crud import create_prediction_log, get_prediction_logs, get_prediction_stats

app = FastAPI()


model = None
try:
    model = joblib.load("models/churn_pipeline.pkl")
except Exception as e:
    print("Exception : ", e)



explainer = None
try:
    explainer = joblib.load("models/shap_explainer.pkl")
except Exception as e:
    print("Exception : ", e)



config = None
with open("models/model_config.json", 'r') as f:
    config = json.load(f)
    


model_version = None
if config is not None:
    model_version = config['model_version']



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
        'config_loaded' : config_load,
        'explainer_loaded' : explainer is not None,
        'model_version' : model_version
    }
    
@app.get("/predictions/stats", response_model=PredictionStatsresponse)
async def get_stats(db : AsyncSession = Depends(get_db)):
    stats = await get_prediction_stats(db)
    
    return {
        "total_predictions" : stats.total_predictions or 0,
        "churn_predictions" : stats.churn_predictions or 0,
        "non_churn_predictions" : stats.non_churn_predictions or 0,
        "mean_churn_probability" : (float(stats.mean_churn_probability) if stats.mean_churn_probability is not None else 0.0)
    }    
    
@app.get("/predictions", response_model=list[DBResponse])
async def get_predictions(limit : int = Query(default=20, ge=1, le=500), db : AsyncSession = Depends(get_db)):
    logs = await get_prediction_logs(db = db, limit = limit)
    return logs
    
@app.post("/predict", response_model=Response)
async def predict(request : Request, db : AsyncSession = Depends(get_db)):
    
    result = prediction(request.model_dump(), model, config, explainer)
    
    model_ver = model_version or "Unknown"
    
    await create_prediction_log(db, result['prediction'], result['churn_probability'], 
                                result['display_probability'], model_ver,
                                result.get('shap_values'))
    
    return result


