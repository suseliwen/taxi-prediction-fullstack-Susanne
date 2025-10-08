from fastapi import FastAPI, Query, APIRouter, HTTPException
from fastapi.responses import RedirectResponse          #Används för att omdirigera root ("/") till docs
from taxipred.backend.data_processing import TaxiData
from pydantic import BaseModel, Field, field_validator
from contextlib import asynccontextmanager
import pandas as pd
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
from taxipred.utils.helpers import FX_USDSEK
from taxipred.backend.data_processing import DataExplorer
from taxipred.utils.time_features import traffic_condition, day_of_week_label, time_of_day
import datetime
from dateutil import parser
from zoneinfo import ZoneInfo
import joblib
import googlemaps
import toml
from pathlib import Path
# from geopy.geocoders import Nominatim
# from geopy import distance


SECRETS_FILE_PATH = Path(__file__).parent.parent.parent.parent / 'src' / 'taxipred' / 'frontend' / '.streamlit' / 'secrets.toml'


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    if SECRETS_FILE_PATH.exists():
        secrets = toml.loads(SECRETS_FILE_PATH.read_text())     #Hämtar api-nyckel från secrets
       
        google_api_key = secrets.get('GOOGLE_API_KEY')          #skapar en variabel av api-nyckeln
        
        if google_api_key:
            app.state.gmaps = googlemaps.Client(key=google_api_key)
            print("INFO: === Google Maps klient initialiserad ===")
        else:
            app.state.gmaps = None
            print("VARNING: NÅGOT GICK FEL! 'google_api_key' saknas i secrets.toml.")
    else:
        app.state.gmaps = None
        print(f"VARNING: secrets.toml hittades inte på sökväg: {SECRETS_FILE_PATH}. Avståndsberäkning kommer att misslyckas.")

    app.state.df = pd.read_csv(DATA_PATH / "taxi_clean.csv").round(2)
    app.state.model = joblib.load(MODELS_PATH / "taxi_price_regressor_new.joblib")

    yield
    del app.state.df
    del app.state.model

router = APIRouter(prefix = "/api")
app = FastAPI(lifespan= lifespan)           #Skapar en FastAPI-applikation
taxi_data = TaxiData()                      #En instans av TaxiData-klassen, som hanterar taxidatan
TZ = ZoneInfo("Europe/Stockholm")


#request schema som hanterar adresser från google maps
class PredictUserRoute(BaseModel):
    origin_address: str
    destination_address: str
    passenger_count: int = Field(gt= 0, lt= 5)
    departure_iso: str  # => ISO8601-datetime, som hämtas från frontend (Streamlit)


#requst schema - prisprediktion baserat på alla variabler
class PricePrediction(BaseModel):    
    Trip_Distance_km: float = Field(gt=1, lt=200)
    Time_of_Day: str
    Day_of_Week: str
    Passenger_Count: int = Field(gt=0, lt=5)
    Traffic_Conditions: str = "Medium"
    Weather: str = "Clear"
    Base_Fare: float = Field(default=2.5, gt=0, lt=5)
    Per_Km_Rate: float = Field(default=1.2, gt=0.5, lt=2)
    Per_Minute_Rate: float = Field(default=0.3, gt=0.1, lt=0.5)
    Trip_Duration_Minutes: float = Field(default=15.0, gt=2, lt=300)

#response schema - prisprediktion baserat på alla variabler
class PredictionResponse(BaseModel):
    predicted_price: float

#request schema - prediktion baserat på användarens input
class PredictUserInput(BaseModel):
    trip_distance_km: float = Field( gt= 1, lt= 200)
    passenger_count: int = Field(gt= 0, lt= 5)
    departure_iso: str  # => ISO8601-datetime, som hämtas från frontend (Streamlit)

   
#response schema - prisprediktion baserat på användarens input
class PredictionAuditResponse(BaseModel):
    predicted_price: float
    traffic_used: str
    time_of_day_used: str
    day_of_week_used: str
    distance_km_calc: float
    duration_min_calc: float

def calc_distance(gmaps_client, origin_address, destination_address):
    if not gmaps_client:
        raise HTTPException(status_code= 503, detail="Google Maps-klient är inte initialiserad. Kontrollera API-nyckeln!")
    
    try:
         result = gmaps_client.distance_matrix(
            origins=[origin_address],
            destinations=[destination_address],
            mode="driving",
            language="sv"
        )
         
         element = result['rows'][0]['elements'][0]

         if element['status'] == "OK":
            distance_km = element['distance']['value'] / 1000.0
            duration_minutes = element['duration']['value'] / 60.0

            return distance_km, duration_minutes
         else:
            raise HTTPException(status_code=404, detail=f"Kunde inte hitta en giltig rutt. Kontrollera adresser. Status: {element['status']}")
    
    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Internt API-fel vid ruttberäkning: {e}")
             

@app.get("/", include_in_schema=False)
async def root():
    """ 
    Root-endpoint==> omdirigerar automatiskt till /docs  
    Bra för att slippa 404 när man öppnar http://127.0.0.1:8000                        
    """
    return RedirectResponse("/docs")
    

@router.get("/summary") 
async def summary():
    """
    Skriver ut översikt av den laddade datan"""
    data = DataExplorer(app.state.df)

    return data.summary().json_response()

@router.get("/rows")
async def read_limited_taxi_data(limit: int = Query(25, gt= 1, lt = 100)): #Query => Använd frågetecken för att skriva in antal rader man vill se
    data = DataExplorer(app.state.df, limit)
    return data.json_response()

@router.get("/kpis")
async def get_kpis():
    """
    Visar kpi:er
    """
    data = DataExplorer(app.state.df)
    return data.kpis()


# Endpoint som gör prediktion baserat på alla variabler
@router.post("/predict_raw", response_model=PredictionResponse)
async def predict_raw(payload: PricePrediction):
    row = payload.model_dump()   
    X = pd.DataFrame([row])
    try:
        y_hat = float(app.state.model.predict(X)[0])
    except Exception as e:
        raise HTTPException(400, f"Feature mismatch: {e}")
    return {"predicted_price": y_hat}

# Endpoint som gör prediktion baserat på användarens inmatning - nu med avståndsberäkning med google maps API (löst med hjälp av gemini...)
@router.post("/predict_route", response_model=PredictionAuditResponse)
async def predict_from_route(payload: PredictUserRoute):
    """ Tar in uppgifter adress, passagerare och tidpunkt från användaren för prisprediktion. 
    OBS! Använd följande format för inmatning av tid: 2025-10-07T07:30:00
    """
    gmaps_client = app.state.gmaps

    MAX_KM = 200.0
    MIN_KM = 1.0

    distance_km, duration_minutes = calc_distance(
        gmaps_client,
        payload.origin_address,
        payload.destination_address
    )

    # Fel till klienten (kod: 400) om sträckan är utanför gränserna
    if distance_km >= MAX_KM:
        raise HTTPException(
            status_code=400,
            detail=f"Resan är {distance_km:.1f} km, vilket överstiger maxlängden {MAX_KM:.0f} km. Ange en annan destination."
        )
    
    if distance_km <= MIN_KM:
        raise HTTPException(
            status_code=400,
            detail=f"Resan är för kort ({distance_km:.1f} km). Minimilängd är {MIN_KM:.0f} km. Ange en annan destination"
        )

    dt = parser.isoparse(payload.departure_iso).replace(tzinfo=TZ)
    tod = time_of_day(dt)
    dow = day_of_week_label(dt)
    traffic = traffic_condition(dt)

    # Bygg en PricePrediction – använd defaults för det som inte anges
    price_input = PricePrediction(
        Trip_Distance_km=distance_km,
        Trip_Duration_Minutes=duration_minutes,        
        Passenger_Count=payload.passenger_count,
        Time_of_Day=tod,
        Day_of_Week=dow,
        Traffic_Conditions=traffic,
    )

    row = price_input.model_dump()
    X = pd.DataFrame([row])
    y_usd = float(app.state.model.predict(X)[0])
    y_sek = y_usd * FX_USDSEK

    return {
        "predicted_price": y_sek,
        "traffic_used": traffic,
        "time_of_day_used": tod,
        "day_of_week_used": dow,
        "distance_km_calc": distance_km,
        "duration_min_calc": duration_minutes
    }
           

@router.get("/taxi")
async def read_taxi_data(): 
    """
    Hämtar taxidatan och returnerar den som JSON.
    """            
    return taxi_data.to_json()



app.include_router(router = router)

