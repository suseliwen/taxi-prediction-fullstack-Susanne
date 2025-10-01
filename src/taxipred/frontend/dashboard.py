import streamlit as st
import requests
from taxipred.utils.helpers import read_api_endpoint
import pandas as pd
import requests
from datetime import date, time as dtime, datetime

API_BASE = "http://127.0.0.1:8000"


def predict_price_user(distance_km: float, passengers: int, departure_dt: datetime):
    payload = {
        "trip_distance_km": float(distance_km),
        "passenger_count": int(passengers),
        "departure_iso": departure_dt.isoformat(),  # t.ex. "2025-10-07T07:30:00"
    }  
      
    url = f"{API_BASE}/api/predict"
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"Kunde inte anropa API:t: {e}")
        return None



def main():
    with st.sidebar:
        st.radio("Select one:", [1, 2])

    st.markdown("# Taxi Prediction Dashboard")
    data = read_api_endpoint("/api/rows")
    df = pd.DataFrame(data.json())

    col1, col2, col3 = st.columns(3)

    col1.metric("My metric", 42, 2)
    col2.metric("My metric", 42, -5)
    col3.metric("My metric", 42, +10)

    
  

    st.subheader("Testa en prediktion!")

    with st.form("taxi_form"):
        distance = st.number_input("Trip Distance (km)", min_value=1.5, max_value=150.0, step=0.1)
        passengers = st.number_input("Passenger Count", min_value=1, max_value=4, step=1)

        dep_date = st.date_input("Departure date", value=date.today())
        dep_time = st.time_input("Departure time", value=dtime(hour=8, minute=0))

        submitted = st.form_submit_button("Predict price")

    if submitted:
        try:
            departure_dt = datetime.combine(dep_date, dep_time)  # naiv → backend sätter Europe/Stockholm
            result = predict_price_user(distance, passengers, departure_dt)

            # Visa resultat
            st.success(f"Predikterat pris: {result['predicted_price']:.2f} kr")
            st.caption(
                f"Antaganden: Traffic={result['traffic_used']} • "
                f"TimeOfDay={result['time_of_day_used']} • "
                f"DayOfWeek={result['day_of_week_used']}"
)

        except requests.RequestException as e:
            st.error(f"Kunde inte anropa API:t: {e}")
        except KeyError:
            st.error("Oväntat svar från API:t. Kontrollera backend-loggen.") 


    #st.dataframe(df.head())

if __name__ == '__main__':
    main()