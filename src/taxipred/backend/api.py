from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse          #Används för att omdirigera root ("/") till docs
from taxipred.backend.data_processing import TaxiData
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import pandas as pd
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
from taxipred.backend.data_processing import DataExplorer

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv(DATA_PATH / "cleaned_taxi_trip_pricing.csv" )
    app.state.df = app.state.df.round(2)

    yield
    del app.state.df

app = FastAPI(lifespan= lifespan)         #Skapar en FastAPI-applikation
taxi_data = TaxiData()  #En instans av TaxiData-klassen, som hanterar taxidatan


# class TaxiItem(BaseModel):    
#     Trip_Distance_km = float
#     Time_of_Day = str
#     Day_of_Week = str
#     Passenger_Count = int
#     Traffic_Conditions = str
#     Weather = str
#     Base_Fare = float
#     Per_Km_Rate = float
#     Per_Minute_Rate = float
#     Trip_Duration_Minutes = float
#     Trip_Price = float
  


@app.get("/", include_in_schema=False)
async def root():
    """ 
    Root-endpoint==> omdirigerar automatiskt till /docs  
    Bra för att slippa 404 när man öppnar http://127.0.0.1:8000                        
    """
    return RedirectResponse("/docs")

@app.get("/api/summary") 
async def summary():
    """
    Skriver ut översikt av den laddade datan"""
    data = DataExplorer(app.state.df)

    return data.summary().json_response()

@app.get("/api")
async def read_limited_taxi_data(limit: int = Query(25, gt= 1, lt = 100)): #Query => Använd frågetecken för att skriva in antal rader man vill se
    data = DataExplorer(app.state.df, limit)
    return data.json_response()

@app.get("/api/kpis")
async def get_kpis():
    """
    Visar kpi:er
    """
    data = DataExplorer(app.state.df)
    return data.kpis()
   

@app.get("/taxi")
async def read_taxi_data(): 
    """
    Hämtar taxidatan och returnerar den som JSON.
    """            
    return taxi_data.to_json()


