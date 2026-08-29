import pandas as pd
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def prediction(transaction: dict, model, config):
    
    THRESHOLD = config["optimal_threshold"]
    
    df = pd.DataFrame([transaction])
    
    proba = model.predict_proba(df)[0, 1]
    
    display_prob = sigmoid(10 * (proba - THRESHOLD))
    
    pred = int(proba >= THRESHOLD)
    
    return {
        "prediction" : pred,
        "churn_probability" : proba,
        "display_probability" : display_prob      
    }
