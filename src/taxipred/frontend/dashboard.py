import streamlit as st
import requests
from taxipred.utils.helpers import read_api_endpoint
import pandas as pd

API_BASE = "http://127.0.0.1:8000"




def predict_price(payload: dict):
    url = f"{API_BASE}/api/predict"
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["predicted_price"]
    except requests.RequestException as e:
        st.error(f"Kunde inte anropa API:t: {e}")
        return None



def main():
    st.markdown("# Taxi Prediction Dashboard")
    data = read_api_endpoint("/api")
    df = pd.DataFrame(data.json())
    #st.dataframe(df)

    st.subheader("Testa en prediktion!")

    with st.form("taxi_form"):
        distance = st.number_input("Trip Distance (km)", min_value=1.0, max_value=150.0, step=0.1)
        time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
        day_of_week = st.selectbox("Day of Week", ["Weekday", "Weekend"])
        passengers = st.number_input("Passenger Count", min_value=1, max_value=4, step=1)
        traffic = st.selectbox("Traffic Conditions", ["High", "Medium", "Low", "Unknown"])
        weather = st.selectbox("Weather", ["Clear", "Rain", "Snow", "Unknown"])
        base_fare = st.number_input("Base Fare", min_value=0.1, max_value=5.0, step=0.1)
        per_km = st.number_input("Per Km Rate", min_value=0.5, max_value=2.0, step=0.1)
        per_minute = st.number_input("Per Minute Rate", min_value=0.1, max_value=0.5, step=0.1)
        duration = st.number_input("Trip Duration (min)", min_value=2.0, max_value=120.0, step=1.0)

        submitted = st.form_submit_button("Predict price")

        if submitted:
            payload = {
                "Trip_Distance_km": distance,
                "Time_of_Day": time_of_day,  
                "Day_of_Week": day_of_week,            
                "Passenger_Count": passengers,
                "Traffic_Conditions": traffic,
                "Weather": weather,
                "Base_Fare": base_fare,
                "Per_Km_Rate": per_km,
                "Per_Minute_Rate": per_minute,
                "Trip_Duration_Minutes": duration,
            }

            y_hat = predict_price(payload)
            st.success(f"Predikterat pris: {y_hat:.2f} kr")    


if __name__ == '__main__':
    main()