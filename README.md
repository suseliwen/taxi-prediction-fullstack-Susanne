
<h1 align="center">🚖 Resekollen Taxi</h1>
<h3 align= "center"> Backend | Frontend | ML </h3>

<p align="center">
  <i>Pris­prediktion av taxiresor med FastAPI, Streamlit och Maskininlärning</i><br>
  <i>Skolprojekt – NBI/Handelsakademin 2025</i>
</p>

<hr style="margin: 30px 0;">

# Syfte och projektbeskrivning
Resekollen Taxi är en applikation som predikterar priset för en taxiresa, baserat på användarens inmatningar.   
Projektet demonstrerar hur backend, frontend och maskininlärning kan integreras i en lösning. 
- Datan hämtas från en CSV-fil som innehåller historiska taxiresor.
- Backend och frontend kommunicerar via ett API. 
- En maskininlärningsmodell (Random Forest Regression) används för att prediktera kostnaden för resan baserat på tidpunkt och avstånd.

---

# Teknisk översikt
| Komponent | Ramverk | Funktion |
|------------|----------|----------|
| Backend | FastAPI | Hanterar API och logik |
| Frontend | Streamlit | Interaktivt användargränssnitt |
| ML-modell | scikit-learn (Random Forest) | Predikterar pris |
| Kartor | Google Maps APIs | Hämtar avstånd och visar rutt |  

---

# Förutsättningar och viktigt att veta innan du kör applikationen

## **API-nycklar behövs för att köra applikationen**
#### Appen behöver två API-nycklar.
- Distance Matrix API (för avståndsberäkning i backend)
- Maps Embed API (för kartvisning i frontend)

Skapa/hämta nycklar i Google Cloud Console och aktivera respektive API för dem.   
Spara nycklarna i secrets.toml (se steg 4 nedan). 
*Rekommendation: begränsa nycklarna (HTTP-referers/domäner, IP, etc.).*

---
# Kör appen
### 1) Klona repot
    https://github.com/suseliwen/taxi-prediction-fullstack-Susanne.git 

### 2) Skapa och aktivera en virtuell miljö      
- **Skapa virtuell miljö**:
    ```bash
    python -m venv venv

- **Aktivera  virtuell miljö**:     
    ```bash    
    source venv/Scripts/activate      # Windows (bash)      
    source venv/bin/activate          # Mac/Linux      

  
### 3) Installera beroenden via requirements.txt 
*Viktigt: starta från projekt-roten (cd taxi-prediktion-fullstack-Susanne)*   
   
    pip install -r requirements.txt   

### 4) Skapa secrets.toml och spara API-nycklarna
Skapa filen i frontendens Streamlit-katalog:   
    
    mkdir -p src/taxipred/frontend/.streamlit
    touch src/taxipred/frontend/.streamlit/secrets.toml

  Lägg till följande i secrets:  
  - GOOGLE_MAPS_API_KEY = "din-distance-matrix-nyckel"      
  - GOOGLE_MAPS_EMBED_KEY = "din-maps-embed-nyckel"   

### 5) Starta api:et/backend
*Kontrollera att du står i projektroten: (cd taxi-prediktion-fullstack-Susanne)* 
  - Öppna en ny terminal   
  - Aktivera den virtuella miljön:   
     ```bash
    source venv/Scripts/activate   
  - starta backend/api:   
    ```bash   
    uvicorn taxipred.backend.api:app --reload --app-dir src   

### 6) Starta streamlit/frontend
*Kontrollera att du står i projektroten: (cd taxi-prediktion-fullstack-Susanne)* 
  - Öppna en ny terminal   
  - Aktivera den virtuella miljön:   
     ```bash
    source venv/Scripts/activate   
  - starta frontend/Streamlit:   
    ```bash   
    streamlit run src/taxipred/frontend/dashboard.py
 
   
