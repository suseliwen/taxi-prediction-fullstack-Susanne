from fastapi import FastAPI, Query, APIRouter
from fastapi.responses import RedirectResponse          #Används för att omdirigera root ("/") till docs
from taxipred.backend.data_processing import TaxiData
from pydantic import BaseModel, Field
from typing import Literal
from contextlib import asynccontextmanager
import pandas as pd
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
from taxipred.backend.data_processing import DataExplorer
import joblib

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv(DATA_PATH /"cleaned_taxi_trip_pricing.csv").round(2)

    bundle = joblib.load(MODELS_PATH / "taxi_price_pipeline.joblib")
    app.state.pipe = bundle["pipeline"]
    app.state.feature_order = bundle["feature_order"]
    yield
   
    del app.state.df
    del app.state.pipe
    del app.state.feature_order

router = APIRouter(prefix = "/api")
app = FastAPI(lifespan= lifespan)           #Skapar en FastAPI-applikation
taxi_data = TaxiData()                      #En instans av TaxiData-klassen, som hanterar taxidatan


#requst schema
class UserInput(BaseModel):    
    Trip_Distance_km: float = Field(gt= 1, lt= 150)
    Time_of_Day:  str
    Day_of_Week:  str
    Passenger_Count:  int = Field(gt= 0, lt= 5)
    Traffic_Conditions:  str
    Weather: str
    Base_Fare:  float = Field(gt= 0, lt= 5)
    Per_Km_Rate:  float = Field(gt= 0.5, lt= 2)
    Per_Minute_Rate:  float = Field(gt= 0.1, lt= 0.5)
    Trip_Duration_Minutes:  float = Field(gt= 2, lt= 120)

#response schema
class PredictionResponse(BaseModel):
    predicted_price: float
 


@router.get("/", include_in_schema=False)
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

@router.get("")
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

#prediction endpoint
@router.post("/predict", response_model= PredictionResponse)
def predict_price(payload: UserInput):
    row = {k: getattr(payload, k) for k in app.state.feature_order}
    X = pd.DataFrame([row])
    y_hat = app.state.pipe.predict(X)[0]
    return {"predicted_price": float(y_hat)}

             

@router.get("/taxi")
async def read_taxi_data(): 
    """
    Hämtar taxidatan och returnerar den som JSON.
    """            
    return taxi_data.to_json()




app.include_router(router = router)

