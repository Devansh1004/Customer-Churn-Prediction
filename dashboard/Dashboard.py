import altair as alt
import pandas as pd
import streamlit as st

from api.api import get_pred_stats, get_predictions # pyright: ignore[reportAttributeAccessIssue]
from dashboard.style import setup, shap_chart, RISK_COLORS, CHURN_COLOR, RETAIN_COLOR

setup("Churn Monitoring Dashboard",
      "Live view of credit card customer churn predictions")

try:
    stats = get_pred_stats()
except Exception as e:
    st.error(f"Unable to connect to API: {e}")
    st.stop()

total = stats["total_predictions"]
churn_rate = stats["churn_predictions"] / total if total else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Predictions", f"{total:,}")
col2.metric("Predicted Churners", f"{stats['churn_predictions']:,}")
col3.metric("Churn Rate", f"{churn_rate:.1%}")
col4.metric("Avg Churn Probability", f"{stats['mean_churn_probability']:.2%}")

df = pd.DataFrame(get_predictions(limit=200))

st.write("")

if df.empty:
    st.info("No predictions available yet. Make one on the Predict Churn page.")
    st.stop()

bins = [-float('inf'), 0.5, 0.75, 0.9, float('inf')]
labels = ['low', 'medium', 'high', 'severe']
df['risk'] = pd.cut(df['display_probability'], bins=bins, labels=labels, right=False)
df['timestamp'] = pd.to_datetime(df['timestamp'])

left, right = st.columns(2)

with left:
    st.subheader("Churn Risk Distribution")
    risk_counts = (
        df['risk'].value_counts().reindex(labels).fillna(0)
        .rename_axis('risk').reset_index(name='count')
    )
    st.altair_chart(
        alt.Chart(risk_counts).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X('risk:N', sort=labels, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('count:Q', title=None),
            color=alt.Color('risk:N', legend=None,
                            scale=alt.Scale(domain=labels, range=[RISK_COLORS[l] for l in labels])),
            tooltip=['risk', 'count'],
        ).properties(height=300),
        width='stretch',
    )

with right:
    st.subheader("Predicted Outcome")
    outcome = (
        df['prediction'].map({0: 'No Churn', 1: 'Churn'})
        .value_counts().rename_axis('outcome').reset_index(name='count')
    )
    st.altair_chart(
        alt.Chart(outcome).mark_arc(innerRadius=70).encode(
            theta='count:Q',
            color=alt.Color('outcome:N', title=None,
                            scale=alt.Scale(domain=['No Churn', 'Churn'],
                                            range=[RETAIN_COLOR, CHURN_COLOR])),
            tooltip=['outcome', 'count'],
        ).properties(height=300),
        width='stretch',
    )

st.subheader("Churn Probability Over Time")
st.altair_chart(
    alt.Chart(df.sort_values('timestamp')).mark_area(
        line={'color': RETAIN_COLOR}, color=RETAIN_COLOR, opacity=0.25,
    ).encode(
        x=alt.X('timestamp:T', title=None),
        y=alt.Y('display_probability:Q', title='Probability', axis=alt.Axis(format='%'),
                scale=alt.Scale(domain=[0, 1])),
        tooltip=['timestamp:T', alt.Tooltip('display_probability:Q', format='.1%')],
    ).properties(height=250),
    width='stretch',
)

st.subheader("Recent Predictions")

table = df[["id", "timestamp", "prediction", "display_probability", "risk", "model_version"]].copy()
table["prediction"] = table["prediction"].map({0: "No Churn", 1: "Churn"})
table["risk"] = table["risk"].astype(str)

st.caption("Click a row to see why the model made that prediction.")

event = st.dataframe(
    table,
    hide_index=True,
    width='stretch',
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "id": st.column_config.NumberColumn("ID", width="small"),
        "timestamp": st.column_config.DatetimeColumn("Time", format="DD MMM YYYY, HH:mm"),
        "prediction": "Prediction",
        "display_probability": st.column_config.ProgressColumn(
            "Churn Probability", format="percent", min_value=0, max_value=1),
        "risk": "Risk",
        "model_version": "Model",
    },
)

selected = event.selection.rows

if selected:
    row = df.iloc[selected[0]]
    st.subheader(f"Why prediction #{row['id']}?")

    c1, c2, c3 = st.columns(3)
    c1.metric("Churn Probability", f"{row['display_probability']:.2%}")
    c2.metric("Prediction", "Churn" if row['prediction'] else "No Churn")
    c3.metric("Risk Level", str(row['risk']).upper())

    shap_values = row.get('shap_values')

    if isinstance(shap_values, list) and shap_values:
        shap_chart(shap_values)
    else:
        st.info("No SHAP explanation was stored for this prediction (made before SHAP was enabled).")
