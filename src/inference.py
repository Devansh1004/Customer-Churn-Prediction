import pandas as pd
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

TOP_N = 8

def explain(df: pd.DataFrame, model, explainer):
    """Per-feature SHAP contributions (log-odds) for a single-row input,
    with one-hot columns folded back into their original feature."""
    X = model.named_steps['preprocessor'].transform(df)
    names = model.named_steps['preprocessor'].get_feature_names_out()
    shap_values = explainer.shap_values(X)[0]

    contributions = {}
    for name, value in zip(names, shap_values):
        feature = name.split("__", 1)[1]
        if feature.startswith("Marital_Status_"):
            feature = "Marital_Status"
        elif feature.startswith("Gender_"):
            feature = "Gender"
        contributions[feature] = contributions.get(feature, 0.0) + float(value)

    ranked = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)[:TOP_N]

    return [
        {"feature": feature, "value": str(df.iloc[0][feature]), "shap_value": shap_value}
        for feature, shap_value in ranked
    ]

def prediction(transaction: dict, model, config, explainer=None):
    
    THRESHOLD = config["optimal_threshold"]
    
    df = pd.DataFrame([transaction])
    
    proba = model.predict_proba(df)[0, 1]
    
    display_prob = sigmoid(10 * (proba - THRESHOLD))
    
    pred = int(proba >= THRESHOLD)
    
    result = {
        "prediction" : pred,
        "churn_probability" : proba,
        "display_probability" : display_prob      
    }

    if explainer is not None:
        try:
            result["shap_values"] = explain(df, model, explainer)
        except Exception as e:
            print("SHAP Exception : ", e)

    return result
