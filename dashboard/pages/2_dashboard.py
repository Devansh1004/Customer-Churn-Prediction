import streamlit as st
import pandas as pd

from api import get_pred_stats, get_predictions

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