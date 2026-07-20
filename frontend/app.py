import streamlit as st
import requests

st.set_page_config(page_title="House Price Predictor", layout="centered")

st.title(" House Price Prediction System")
st.write("Enter the property details below to estimate the market price.")

API_URL = "http://127.0.0.1:8000"

# Fetch locations dynamically from Backend
try:
    response = requests.get(f"{API_URL}/locations")
    if response.status_code == 200:
        locations = response.json().get("locations", [])
    else:
        locations = ["Thane", "Navi Mumbai", "Mumbai"]
except Exception:
    locations = ["Thane", "Navi Mumbai", "Mumbai"]

# Form Layout
st.subheader("Property Specifications")

col1, col2 = st.columns(2)

with col1:
    carpet_area = st.number_input("Carpet Area (sqft)", min_value=100.0, max_value=10000.0, value=1200.0, step=50.0)
    floor_num = st.number_input("Floor Number", min_value=0, max_value=100, value=3, step=1)
    bathroom = st.selectbox("Number of Bathrooms", [1, 2, 3, 4, 5], index=1)
    balcony = st.selectbox("Number of Balconies", [0, 1, 2, 3, 4], index=1)
    location = st.selectbox("Location / Area", locations)

with col2:
    furnishing = st.selectbox("Furnishing Status", ["Unfurnished", "Semi-Furnished", "Furnished"], index=1)
    transaction = st.selectbox("Transaction Type", ["Resale", "New Property"], index=0)
    ownership = st.selectbox("Ownership Type", ["Freehold", "Leasehold", "Power of Attorney"], index=0)
    facing = st.selectbox("Facing Direction", ["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"], index=0)

st.markdown("---")

if st.button(" Estimate House Price", use_container_width=True):
    payload = {
        "carpet_area_sqft": float(carpet_area),
        "floor_num": int(floor_num),
        "bathroom": int(bathroom),
        "balcony": int(balcony),
        "location_grouped": str(location),
        "Furnishing": str(furnishing),
        "Transaction": str(transaction),
        "Ownership": str(ownership),
        "facing": str(facing)
    }

    with st.spinner("Calculating estimate... Please wait."):
        try:
            res = requests.post(f"{API_URL}/predict", json=payload)
            if res.status_code == 200:
                predicted_price = res.json().get("predicted_price", 0)
                st.success(f" Estimated Property Price: ₹ {predicted_price:,.2f}")
            else:
                st.error(f"Error from server: {res.status_code}")
        except Exception as e:
            st.error("Could not connect to the Backend server. Make sure the API is running.")
