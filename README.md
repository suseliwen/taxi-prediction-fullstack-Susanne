
### Resekollen Taxi – Pris­prediktion 
(Backend | Frontend | ML)

#### Skollab i kursen 'Objektorienterad programmering avancerad 1" (OPA24GB) 
NBI/Handelsakademin. 

##### Syfte och projektbeskrivning
Resekollen Taxi är en applikation som predikterar priset för en taxiresa, baserat på användarens inmatningar.   
Projektet demonstrerar hur backend, frontend och maskininlärning kan integreras i en lösning. 
- Datan hämtas från en CSV-fil som innehåller historiska taxiresor.
- Backend och frontend kommunicerar via ett FAST API. 
- En maskininlärningsmodell (Random Forest Regression) används för att prediktera kostnaden för resan baserat på tidpunkt, avstånd och andra faktorer.


##### Förutsättningar och viktigt att veta innan du kör applikationen
Du behöver en API-nyckel för att kunna köra applikationen. 
- Skapa eller hämta en nyckel via Google Clod Console. 
- Aktivera "Distance Matrix API". 
- Spara din api-nyckel i .streamlit/sercrets.toml.

Api-et behöver vara igång för att preditionerna ska kunna hämtas till frontend

##### Kör appen
- Klona repot   

- Skapa och aktivera en virtuell miljö
    1. python -m venv venv
    2. source venv/Scripts/activate  (Windows (Bash)) | source venv/bin/activate (Mac/Linux)   
  
- Installera beroenden via requirements.txt
    - uv pip install -r requirements.txt   

- Starta api:et
    - Öppna en ny terminal
    - cd src/taxipred/backend
    - uvicorn api:app --reload   

- Starta streamlit
    - Öppna en ny terminal
    - cd src/taxipred/frontend
    - streamlit run dashboard.py
 
