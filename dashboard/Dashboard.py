import requests
import pandas as pd
import streamlit as st

API_URL = "http://127.0.0.1:8000"

from api.api import get_pred_stats, get_predictions # pyright: ignore[reportAttributeAccessIssue]

st.set_page_config(page_title = "Credit Card Customer Churn Prediction",
                   layout = "wide")

st.title("Churn Monitoring Dashboard")

try:
    stats = get_pred_stats()
except Exception as e:
    st.error(f"Unable to connect to API: {e}")
    st.stop()
    
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Predictions", stats["total_predictions"])

with col2:
    st.metric("Churn Predictions", stats["churn_predictions"])

with col3:
    st.metric("Avg Churn Probability", f"{stats['mean_churn_probability']:.2%}")
    
predictions = get_predictions(limit=200)

df = pd.DataFrame(predictions)

st.divider()

st.subheader("Churn Risk Distribution")

if not df.empty:
    
    bins = [-float('inf'), 0.5, 0.75, 0.9, float('inf')]
    labels = ['low', 'medium', 'high', 'severe']
    
    df['risk'] = pd.cut(df['display_probability'], bins=bins, labels=labels, right=False)
    
    risk_counts = (df["risk"].value_counts())

    st.bar_chart(risk_counts)

else:
    st.info("No predictions available yet.")
    
st.divider()

st.subheader("Recent Predictions")

if not df.empty:
    display_df = df[
        [
            "id",
            "timestamp",
            "prediction",
            "churn_probability",
            "display_probability",
            "model_version"
        ]
    ].copy()
    
    display_df.drop(columns=['churn_probability'], inplace=True)

    display_df["probability"] = (
        display_df["display_probability"]
        .map(lambda x: f"{x:.2%}")
    )

    display_df["prediction"] = (
        display_df["prediction"]
        .map(
            {
                0: "No Churn",
                1: "Churn"
            }
        )
    )
    
    display_df.drop(columns=['display_probability'], inplace=True)

    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True
    )

else:
    st.info("No predictions available yet.")