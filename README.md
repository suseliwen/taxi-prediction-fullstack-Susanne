
<h1 align="center">🚖 Resekollen Taxi</h1>
<h3 align= "center"> Backend | Frontend | ML </h3>

<p align="center">
  <i>Pris­prediktion av taxiresor med FastAPI, Streamlit och Maskininlärning</i><br>
  <sub>Skolprojekt – NBI/Handelsakademin 2024</sub>
</p>

<hr style="margin: 30px 0;">

### Syfte och projektbeskrivning
Resekollen Taxi är en applikation som predikterar priset för en taxiresa, baserat på användarens inmatningar.   
Projektet demonstrerar hur backend, frontend och maskininlärning kan integreras i en lösning. 
- Datan hämtas från en CSV-fil som innehåller historiska taxiresor.
- Backend och frontend kommunicerar via ett API. 
- En maskininlärningsmodell (Random Forest Regression) används för att prediktera kostnaden för resan baserat på tidpunkt, avstånd och andra faktorer.

---

### Teknisk översikt
| Komponent | Ramverk | Funktion |
|------------|----------|----------|
| Backend | FastAPI | Hanterar API och logik |
| Frontend | Streamlit | Interaktivt användargränssnitt |
| ML-modell | scikit-learn (Random Forest) | Predikterar pris |
| Kartor | Google Maps APIs | Hämtar avstånd och visar rutt |  

---

### Förutsättningar och viktigt att veta innan du kör applikationen

**API-nycklar behövs för att köra applikationen**
Appen behöver två API-nycklar.
- Distance Matrix API (för avståndsberäkning i backend)
- Maps Embed API (för kartvisning i frontend)

Skapa/hämta nycklar i Google Cloud Console och aktivera respektive API för dem.
*Rekommendation: begränsa nycklarna (HTTP-referers/domäner, IP, etc.).*

Lägg nycklarna i en secrets.toml. 
Skapa filen i frontendens Streamlit-katalog:
- mkdir -p src/taxipred/frontend/.streamlit
- touch src/taxipred/frontend/.streamlit/secrets.toml

Innehåll (exempel):
GOOGLE_MAPS_API_KEY = "din-distance-matrix-nyckel"      
GOOGLE_MAPS_EMBED_KEY = "din-maps-embed-nyckel"   

Filen checkas inte in i Git. Lägg gärna i .gitignore:   
src/taxipred/frontend/.streamlit/secrets.toml

**Api-et behöver vara igång för att preditionerna ska kunna hämtas till frontend**

---
### Kör appen
- #### 1) Klona repot
git clone https://github.com/<user>/resekollen-taxi.git   
cd resekollen-taxi   

- #### 2) Skapa och aktivera en virtuell miljö
    #### *Skapa virtuell miljö*:  
    python -m venv venv
    #### *Aktivera virtuell miljö*: 
    - Windows (bash) - source venv/Scripts/activate   
    - Mac/Linux - source venv/bin/activate  
    
  
- #### 3) Installera beroenden via requirements.txt
    - pip install -r requirements.txt   

- #### 4) Starta api:et/backend
*Viktigt: starta från projektroten och ange --app-dir src*
    - Öppna en ny terminal
    - *Aktivera* den virtuella miljön    
    - uvicorn taxipred.backend.api:app --reload --app-dir src 

- #### 5) Starta streamlit/frontend
    - Öppna en ny terminal
    - *Aktivera den* virtuella miljön
    -  streamlit run src/taxipred/frontend/dashboard.py
 
