
<h1 align="center">🚖 Resekollen Taxi</h1>
<h3 align= "center"> Backend | Frontend | ML </h3>

<p align="center">
  <i>Pris­prediktion av taxiresor med FastAPI, Streamlit och Maskininlärning</i><br>
  <sub>Skolprojekt – NBI/Handelsakademin 2024</sub>
</p>

<hr style="margin: 30px 0;">

---

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
Du behöver två API-nycklar för att kunna köra applikationen: 
- Skapa eller hämta nycklar via Google Cloud Console. 
- Aktivera "Distance Matrix API" för den ena nyckeln. 
- Aktivera "Maps Embed API" för den andra nyckeln. 
- Spara dina api-nycklar i .streamlit/sercrets.toml

Api-et behöver vara igång för att preditionerna ska kunna hämtas till frontend

---
### Kör appen
- #### Klona repot   

- #### Skapa och aktivera en virtuell miljö
    1. python -m venv venv
    2. source venv/Scripts/activate  (Windows (Bash)) | source venv/bin/activate (Mac/Linux)   
  
- #### Installera beroenden via requirements.txt
    - uv pip install -r requirements.txt   

- #### Starta api:et/backend
    - Öppna en ny terminal
    - Aktivera den vituella miljön
    - cd src/taxipred/backend
    - uvicorn api:app --reload   

- #### Starta streamlit/frontend
    - Öppna en ny terminal
    - Aktivera den vituella miljön
    - cd src/taxipred/frontend
    - streamlit run dashboard.py
 
