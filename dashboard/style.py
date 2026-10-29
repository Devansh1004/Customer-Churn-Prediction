import altair as alt
import pandas as pd
import streamlit as st

CHURN_COLOR = "#f87171"
RETAIN_COLOR = "#38bdf8"
RISK_COLORS = {
    "low": "#34d399",
    "medium": "#fbbf24",
    "high": "#fb923c",
    "severe": "#f87171",
}

_CSS = """
<style>
.block-container { padding-top: 2rem; max-width: 1200px; }
h1, h2, h3 { letter-spacing: -0.01em; }
.hero {
    padding: 1.6rem 1.8rem; border-radius: 16px; margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
}
.hero h1 { color: #fff; margin: 0; font-size: 2rem; }
.hero p { color: rgba(255,255,255,0.85); margin: 0.3rem 0 0; }
[data-testid="stMetric"] {
    background: #131c2e; border: 1px solid #22304a; border-radius: 14px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: #94a3b8; }
[data-testid="stMetricValue"] { font-weight: 700; }
.pill {
    display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px;
    font-weight: 600; font-size: 0.95rem; color: #0b1220;
}
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    border-radius: 10px; font-weight: 600;
}
[data-testid="stForm"] {
    background: #131c2e; border: 1px solid #22304a; border-radius: 16px;
}
#MainMenu, footer { visibility: hidden; }
</style>
"""

def shap_chart(shap_values: list[dict]):
    st.caption(
        "Top factors behind the prediction. Red pushes the customer toward churn, "
        "blue pushes toward staying."
    )

    shap_df = pd.DataFrame(shap_values)
    shap_df["label"] = shap_df["feature"].str.replace("_", " ") + " = " + shap_df["value"]
    shap_df["effect"] = shap_df["shap_value"].map(
        lambda v: "Increases churn risk" if v > 0 else "Decreases churn risk"
    )

    st.altair_chart(
        alt.Chart(shap_df).mark_bar(cornerRadius=4).encode(
            x=alt.X("shap_value:Q", title="Impact on churn (SHAP value)"),
            y=alt.Y("label:N", sort=alt.EncodingSortField("shap_value", op="max", order="descending"),
                    title=None),
            color=alt.Color("effect:N", title=None,
                            scale=alt.Scale(domain=["Increases churn risk", "Decreases churn risk"],
                                            range=[CHURN_COLOR, RETAIN_COLOR])),
            tooltip=["label", alt.Tooltip("shap_value:Q", format=".3f"), "effect"],
        ).properties(height=320),
        width='stretch',
    )

def setup(title: str, subtitle: str, icon: str = "📉"):
    st.set_page_config(page_title="Churn Prediction", page_icon=icon, layout="wide")
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero"><h1>{icon} {title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )
