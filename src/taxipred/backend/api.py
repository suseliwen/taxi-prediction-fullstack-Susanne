from fastapi import FastAPI, Query, APIRouter, HTTPException
from fastapi.responses import RedirectResponse          #Används för att omdirigera root ("/") till docs
from taxipred.backend.data_processing import TaxiData
from pydantic import BaseModel, Field
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
from geopy.geocoders import Nominatim
from geopy import distance

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv(DATA_PATH / "taxi_clean.csv").round(2)
    app.state.model = joblib.load(MODELS_PATH / "taxi_price_regressor_new.joblib")
    yield
    del app.state.df
    del app.state.model

router = APIRouter(prefix = "/api")
app = FastAPI(lifespan= lifespan)           #Skapar en FastAPI-applikation
taxi_data = TaxiData()                      #En instans av TaxiData-klassen, som hanterar taxidatan
TZ = ZoneInfo("Europe/Stockholm")

#requst schema - prisprediktion baserat på alla variabler
class PricePrediction(BaseModel):    
    Trip_Distance_km: float = Field(gt=1, lt=150)
    Time_of_Day: str
    Day_of_Week: str
    Passenger_Count: int = Field(gt=0, lt=5)
    Traffic_Conditions: str = "Medium"
    Weather: str = "Clear"
    Base_Fare: float = Field(default=2.5, gt=0, lt=5)
    Per_Km_Rate: float = Field(default=1.2, gt=0.5, lt=2)
    Per_Minute_Rate: float = Field(default=0.3, gt=0.1, lt=0.5)
    Trip_Duration_Minutes: float = Field(default=15.0, gt=2, lt=120)

#response schema - prisprediktion baserat på alla variabler
class PredictionResponse(BaseModel):
    predicted_price: float



#request schema - prediktion baserat på användarens input
class PredictUserInput(BaseModel):
    trip_distance_km: float = Field( gt= 1, lt= 150)
    passenger_count: int = Field(gt= 0, lt= 5)
    departure_iso: str  # => ISO8601-datetime, som hämtas från frontend (Streamlit)


#response schema - prisprediktion baserat på användarens input
class PredictionAuditResponse(BaseModel):
    predicted_price: float
    traffic_used: str
    time_of_day_used: str
    day_of_week_used: str


 


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

# Endpoint som gör prediktion baserat på användarens inmatning 
@router.post("/predict", response_model=PredictionAuditResponse)
async def predict_from_user(payload: PredictUserInput):
    """ Tar in uppgifter från användern vid prediktion. 
    Använd följande datumformat vid test: 2025-10-07T07:30:00
    """

    dt = parser.isoparse(payload.departure_iso).replace(tzinfo=TZ)

    tod = time_of_day(dt)
    dow = day_of_week_label(dt)
    traffic = traffic_condition(dt)

    # Bygg en PricePrediction – använd defaults för det som inte anges
    price_input = PricePrediction(
        Trip_Distance_km=payload.trip_distance_km,
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
    }
 
           

@router.get("/taxi")
async def read_taxi_data(): 
    """
    Hämtar taxidatan och returnerar den som JSON.
    """            
    return taxi_data.to_json()



app.include_router(router = router)

