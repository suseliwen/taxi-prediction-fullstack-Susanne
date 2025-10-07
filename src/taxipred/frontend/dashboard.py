import streamlit as st
import requests
import pandas as pd
import requests
from datetime import date, time as dtime, datetime
from zoneinfo import ZoneInfo
import urllib.parse, streamlit as st

API_BASE = "http://127.0.0.1:8000"
TZ = ZoneInfo("Europe/Stockholm")


st.title("Taxipriset - Vad kostar din resa?")

st.divider()


def predict_price_user(origin_address: str, destination_address: str, passengers: int, departure_dt: datetime):
    
    if departure_dt.tzinfo is None or departure_dt.tzinfo.utcoffset(departure_dt) is None:
        departure_dt = departure_dt.replace(tzinfo=TZ)

    payload = {
        "origin_address": origin_address,
        "destination_address": destination_address,
        "passenger_count": int(passengers),
        "departure_iso": departure_dt.isoformat(),  # t.ex. "2025-10-07T07:30:00"
    }  
      
    url = f"{API_BASE}/api/predict_route"
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
        
    except requests.RequestException as e:
        st.error(f"Kunde inte anropa API:t: {e}")        
        return None

def main():

    default_origin = "Göteborgs Centralstation"
    default_destination = "Landvetter Flygplats"
            
    with st.sidebar:        
        st.subheader("Beräkna priset för din resa här!")

        with st.form("sidebar_prediction_form"):
                
                origin_address = st.text_input("Skriv in adressen du vill åka **från**:", value = default_origin)
            
                destination_address = st.text_input("Skriv in adressen du vill åka **till**:", value = default_destination)     

                departure_date =st.date_input("Avresedag: ", value = date.today())

                departure_time = st.time_input("Avresetid: ", value=dtime(hour= 8, minute= 0))

                passengers = st.slider("Antal Passagerare:", 1, 4, 1, step=1, help="Du kan beräkna pris för upp till 4 passagerare")

                submitted = st.form_submit_button("Beräkna pris för resan")         
      
        st.divider()     


   
    if submitted:

        departure_dt = datetime.combine(departure_date, departure_time)        
        result = predict_price_user(origin_address, destination_address, passengers, departure_dt)

        if result:
            price_sek = result['predicted_price']
            distance_km = result['distance_km_calc']
            duration_minutes = result['duration_min_calc']
            
            st.success("Priset beräknat!")
           
            st.subheader(f"Din resa beräknas att kosta {price_sek:,.2f} kr")       
           
            st.subheader("Utökad information om beräkningen")
            
            
            col_1, col_2, col_3 = st.columns(3)
            
            with col_1:
                st.metric("Beräknat Avstånd", f"{distance_km:.2f} km")
                
            with col_2:
                st.metric("Beräknad Restid", f"{duration_minutes:.0f} min")

            with col_3:
                st.markdown(f"""
                **Tidpunkt:** {result['time_of_day_used']}
                
                **Veckodag:** {result['day_of_week_used']}
                
                **Trafiksituation:** {result['traffic_used']}
                """)   

    origin = urllib.parse.quote_plus(origin_address)
    dest   = urllib.parse.quote_plus(destination_address)
    key    = st.secrets["GMAPS_EMBED_KEY"]

    url = f"https://www.google.com/maps/embed/v1/directions?key={key}&origin={origin}&destination={dest}&mode=driving"
    st.components.v1.iframe(url, width=800, height=520)     
        

 #st.dataframe(df.head())

if __name__ == '__main__':
    main()