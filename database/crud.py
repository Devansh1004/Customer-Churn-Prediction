from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import PredictionLog

async def create_prediction_log(
    db : AsyncSession,
    prediction : int,
    churn_probability : float,
    display_probability : float,
    model_version : str,
    shap_values : list | None = None
):

    log = PredictionLog(
        shap_values = shap_values,
        churn_probability = churn_probability,
        prediction = prediction,
        display_probability = display_probability,
        model_version = model_version
    )
    
    db.add(log)
    
    await db.commit()
    
    await db.refresh(log)
    
    return log

async def get_prediction_logs(
    db : AsyncSession,
    limit: int = 20
):
    result = await db.execute(select(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(limit))
    
    return result.scalars().all()

async def get_prediction_stats(
    db : AsyncSession
):
    result = await db.execute(
        select(
            func.count(PredictionLog.id).label("total_predictions"),
            
            func.sum(PredictionLog.prediction).label("churn_predictions"),
            
            func.count(PredictionLog.id).filter(PredictionLog.prediction == 0).label("non_churn_predictions"),
            
            func.avg(PredictionLog.display_probability).label("mean_churn_probability")
        )
    )
    
    return result.one()