import streamlit as st

from api import predict_churn

st.title('Predict Customer Churn')

st.markdown("Enter the customer's information")

with st.form("churn_prediction_form"):

    st.subheader("Customer Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        customer_age = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=120,
            value=45,
            step=1
        )

        gender = st.selectbox(
            "Gender",
            ["M", "F"]
        )

        dependent_count = st.number_input(
            "Dependent Count",
            min_value=0,
            max_value=5,
            value=2,
            step=1
        )

    with col2:

        education_level = st.selectbox(
            "Education Level",
            [
                "Uneducated",
                "High School",
                "College",
                "Graduate",
                "Post-Graduate",
                "Doctorate",
                "Unknown"
            ]
        )

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Single",
                "Married",
                "Divorced",
                "Unknown"
            ]
        )

        income_category = st.selectbox(
            "Income Category",
            [
                "Less than $40K",
                "$40K - $60K",
                "$60K - $80K",
                "$80K - $120K",
                "$120K +",
                "Unknown"
            ]
        )

    with col3:

        card_category = st.selectbox(
            "Card Category",
            [
                "Blue",
                "Silver",
                "Gold",
                "Platinum"
            ]
        )

        months_on_book = st.number_input(
            "Months on Book",
            min_value=0,
            max_value=60,
            value=36,
            step=1
        )

        total_relationship_count = st.number_input(
            "Total Relationship Count",
            min_value=1,
            value=3,
            step=1
        )

    st.divider()

    st.subheader("Account Activity")

    col1, col2, col3 = st.columns(3)

    with col1:

        months_inactive = st.number_input(
            "Months Inactive (12 months)",
            min_value=0,
            max_value=12,
            value=2,
            step=1
        )

        contacts_count = st.number_input(
            "Contacts Count (12 months)",
            min_value=0,
            value=2,
            step=1
        )

    with col2:

        credit_limit = st.number_input(
            "Credit Limit",
            min_value=0.0,
            max_value=40000.0,
            value=5000.0,
            step=100.0
        )

        revolving_balance = st.number_input(
            "Total Revolving Balance",
            min_value=0.0,
            max_value=4000.0,
            value=1000.0,
            step=100.0
        )

    with col3:

        avg_open_to_buy = st.number_input(
            "Average Open To Buy",
            min_value=0.0,
            max_value=40000.0,
            value=4000.0,
            step=100.0
        )

    st.divider()

    st.subheader("Transaction Behaviour")

    col1, col2, col3 = st.columns(3)

    with col1:

        total_amt_change = st.number_input(
            "Total Amount Change Q4/Q1",
            min_value=0.0,
            max_value=5.0,
            value=0.75,
            step=0.05
        )

        total_trans_amt = st.number_input(
            "Total Transaction Amount",
            min_value=0.0,
            max_value=20000.0,
            value=4000.0,
            step=100.0
        )

    with col2:

        total_trans_ct = st.number_input(
            "Total Transaction Count",
            min_value=0.0,
            max_value=150.0,
            value=50.0,
            step=1.0
        )

        total_ct_change = st.number_input(
            "Total Count Change Q4/Q1",
            min_value=0.0,
            max_value=5.0,
            value=0.75,
            step=0.05
        )

    with col3:

        utilization_ratio = st.number_input(
            "Average Utilization Ratio",
            min_value=0.0,
            max_value=1.0,
            value=0.30,
            step=0.01
        )

    st.divider()

    submitted = st.form_submit_button(
        "Predict Churn",
        use_container_width=True
    )
    
if submitted:

    data = {
        "Customer_Age": customer_age,
        "Gender": gender,
        "Dependent_count": dependent_count,
        "Education_Level": education_level,
        "Marital_Status": marital_status,
        "Income_Category": income_category,
        "Card_Category": card_category,
        "Months_on_book": months_on_book,
        "Total_Relationship_Count": total_relationship_count,
        "Months_Inactive_12_mon": months_inactive,
        "Contacts_Count_12_mon": contacts_count,
        "Credit_Limit": credit_limit,
        "Total_Revolving_Bal": revolving_balance,
        "Avg_Open_To_Buy": avg_open_to_buy,
        "Total_Amt_Chng_Q4_Q1": total_amt_change,
        "Total_Trans_Amt": total_trans_amt,
        "Total_Trans_Ct": total_trans_ct,
        "Total_Ct_Chng_Q4_Q1": total_ct_change,
        "Avg_Utilization_Ratio": utilization_ratio
    }

    try:

        result = predict_churn(data)

        st.success("Prediction completed successfully.")

        probability = result["churn_probability"]
        prediction = result["prediction"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Churn Probability",
                f"{probability:.2%}"
            )

        with col2:
            st.metric(
                "Prediction",
                "Will Churn" if prediction else "Will Not Churn"
            )

    except Exception as e:

        st.error(
            f"Unable to obtain prediction: {e}"
        )