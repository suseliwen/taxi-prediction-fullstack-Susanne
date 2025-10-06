
### Resekollen Taxi – Pris­prediktion 
Backend | Frontend | ML

#### Skolprojekt i kursen *'Objektorienterad programmering avancerad 1"* (OPA24GB) 
*NBI/Handelsakademin* 

#### Syfte och projektbeskrivning
Resekollen Taxi är en applikation som predikterar priset för en taxiresa, baserat på användarens inmatningar.   
Projektet demonstrerar hur backend, frontend och maskininlärning kan integreras i en lösning. 
- Datan hämtas från en CSV-fil som innehåller historiska taxiresor.
- Backend och frontend kommunicerar via ett API. 
- En maskininlärningsmodell (Random Forest Regression) används för att prediktera kostnaden för resan baserat på tidpunkt, avstånd och andra faktorer.

#### Teknisk översikt
Backend - FastAPI – tar emot användardata och anropar ML-modellen   
Frontend - Streamlit – användargränssnitt för inmatning och resultat   
ML-modell - Random Forest Regressor, tränad på historiska taxiresor   
Karttjänster - Google Distance Matrix API (avstånd) + Maps Embed API (visualisering)  
Data - CSV-fil med fält som avstånd, restid, tidpunkt, pris m.m.   

#### Förutsättningar och viktigt att veta innan du kör applikationen
Du behöver två API-nycklar för att kunna köra applikationen: 
- Skapa eller hämta nycklar via Google Cloud Console. 
- Aktivera "Distance Matrix API" för den ena nyckeln. 
- Aktivera "Maps Embed API" för den andra nyckeln. 
- Spara dina api-nycklar i .streamlit/sercrets.toml

Api-et behöver vara igång för att preditionerna ska kunna hämtas till frontend

#### Kör appen
- ##### Klona repot   

- ##### Skapa och aktivera en virtuell miljö
    1. python -m venv venv
    2. source venv/Scripts/activate  (Windows (Bash)) | source venv/bin/activate (Mac/Linux)   
  
- ##### Installera beroenden via requirements.txt
    - uv pip install -r requirements.txt   

- ##### Starta api:et/backend
    - Öppna en ny terminal
    - cd src/taxipred/backend
    - uvicorn api:app --reload   

- ##### Starta streamlit/frontend
    - Öppna en ny terminal
    - cd src/taxipred/frontend
    - streamlit run dashboard.py
 
