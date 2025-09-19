from fastapi import FastAPI
from fastapi.responses import RedirectResponse          #Används för att omdirigera root ("/") till docs
from taxipred.backend.data_processing import TaxiData

app = FastAPI()         #Skapar en FastAPI-applikation
taxi_data = TaxiData()  #En instans av TaxiData-klassen, som hanterar taxidatan

@app.get("/", include_in_schema=False)
def root():
    """ 
    Root-endpoint==> omdirigerar automatiskt till /docs  
    Bra för att slippa 404 när man öppnar http://127.0.0.1:8000                        
    """
    return RedirectResponse("/docs")    

@app.get("/taxi")

async def read_taxi_data(): 
    """
    Hämtar taxidatan och returnerar den som JSON.
    """            
    return taxi_data.to_json()