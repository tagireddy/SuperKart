import os
import requests
import streamlit as st
import pandas as pd

API_URL = os.getenv("MODEL_API_URL", "http://localhost:7860")

st.title("SuperKart Sales Forecast")

with st.form("prediction_form"):
    product_weight = st.number_input("Product Weight", value=12.66)
    product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    product_area = st.number_input("Product Allocated Area", value=0.027)
    product_mrp = st.number_input("Product MRP", value=117.08)
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
    product_id_char = st.selectbox("Product Id Prefix", ["FD", "NC", "DR"])
    store_age_years = st.number_input("Store Age (Years)", value=16)
    product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
    submitted = st.form_submit_button("Predict Sales")

if submitted:
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": product_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category,
    }
    response = requests.post(f"{API_URL}/v1/predict", json=payload, timeout=30)
    if response.status_code == 200:
        st.success(f"Predicted Sales: ${response.json()['prediction']:.2f}")
    else:
        st.error(f"Prediction failed: {response.text}")

uploaded_file = st.file_uploader("Upload batch CSV", type=["csv"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    response = requests.post(f"{API_URL}/v1/predictbatch", files=files, timeout=60)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Batch prediction failed: {response.text}")
