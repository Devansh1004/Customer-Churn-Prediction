import requests
import streamlit as st

API_URL = "https://127.0.0.1:8000"

st.set_page_config(page_title = "Credit Card Customer Churn Prediction",
                   layout = "wide")

st.title("Credit Card Customer Churn Prediction")

st.write("Enter customer information to estimate churn probability")

st.header("Customer Information")