###  **Projekt taxi prediction**

##### **Uppgift 0 - Sätta upp repots struktur och läsa in data**
- [X] Sätt upp mappstrukturen enligt videon a2_packaging
- [X] Lägg till datan i foldern 'data'
- [X] Skapa ett par endpoints (docs, taxi)
- [X] Sätt upp så att datan kan visualiseras i Streamlit

##### **Uppgift 1 - EDA och data cleaning**
- [X] Gör explorativa dataanalyser
- [X] Gå igenom nullvärden i datasetet, och hitta sätt att hantera dem
- [X] Undersök om och hur ev. outliers påverkar datan och hantera dem. 
- [X] Exportera den städade datan till en ny csv-fil, och använd den fortsatt i applikationen
 
##### **Uppgift 2 -  ML modell**
Ta fram en ML modell för att prediktera taxipriser. Gå igenom data science workflow, med att testa olika modeller och evaluera. Välj därefter en modell och träna på all data. Exportera därefter datan med hjälp av
joblib 
- [X] Testat olika modeller i Jupyter NoteBook och bestämt mig för en modell
- [X] Träna datan på den bestämda modellen
- [X] Exportera datan med hjälp av joblib

##### **Uppgift 3 -  Backend och API-lager**
Skapa en backend och ett API-lager i FastAPI som ska serva datan. Det innebär att det ska finnas olika
endpoints för att kunna läsa delar av datan. Det ska också finnas möjlighet att göra prediktion genom att
låta användaren mata in olika parametrar.
- Vilka endpoints ska jag ha? CRUD - Create, Read, Update, Delete
- [X] GET-enpoints (summary, limited taxi-data, all taxi-data)
- [X] POST-endpoints (predict price - en med inmatning från användare och en med alla variabler)
- [ ] PUT-endpoints
- [ ] DELETED-endpoints


##### **Uppgift 4 -   Bygg en frontend**
Bygg en snygg frontend och konsumera API:et.
- [X] En prediktion, baserat på användarens inmatning ()
- [X] fritextfält för att fylla i varifrån man vill åka, och destination
- [X] Räknare som räknar ut antal kilometer
- [X] En karta för snyggare visualiseringen (borde gå att få med google maps...) 

- [ ] Felmeddelande när användaren lägger in avstånd över 120 alt 150 mil

- [-] Koppling till väderleks app, som talar om vilket väder det är de närmaste 10 dagarna? - Kommer inte göra
- [-] Metrics som visar vilket tid eller datum som det är billigast respektive dyrast att åka. - Kommer inte göra
- [-] Nice to have - spara info om användare - Kommer inte göra



##### **Uppgift 5 - Videopitch**
Spela in dig och själv och skärmen - ex mha teams, obs eller liknande verktyg. Du ska visa upp
applikationen och presentera övergripande hur din kod fungerar. Videon ska vara 5-10 min lång och skickas
in till lärplattformen.
- [ ] .



##### **=============== TEST =============**
***Teststrategi***  
Jag har klonat repot från GitHub och testat att köra programmet utifrån beskrivningen i ReadMe.   
Om jag har fått något problem i det klonade repot har jag identifierat och åtgärdat problemet.    
Jag har därefter uppdaterat ReadMe, slängt det klonade repot och börjat om på nytt.   
När ett steg får godkänt resultat bockar jag i kryssrutan och skriver in vad som inte funkat och hur det åtgärdats.  

---------------

- [X] Klona repot => Inga problem

- [X] Skapa virtuell miljö

- [X]  Installera requirements
    - Måste stå i rätt folder i terminalen...
    - Uppdterar ReadMen eftersom det är lätt att glömma bort.   

- [X] Skapa secerets.toml och lägg in API-nycklar 
    - Ändrar i ReadMe, så instruktioner för att skapa folder & fil kommer i rätt ordning. 

- [X] Starta upp backend och testa API via uvicorn
    - Funkar inte att köra från src/taxipred/backend som jag är van!
    - Behöver köras från projektroten pga src-layouten - hittar inte texipred. 
    - Efter felsökning med hjälp av chatGPT förstår jag att jag behöver köra uvicorn taxipred.backend.api:app --reload --app-dir src för att det ska funka.
    - Uppdaterar ReadMe med informationen. 
    - Betonar i ReadMe att api:et behöver vara igång för att frontend ska funka. 
    - Lägger också till hur man ska avsluta programmet. 

- [X] Starta upp frontend/Streamlit och testa att appen ger ett resultat
    - Kan lägga in olika adresser, och får en prediktion samt vägbeskrivning i kartan. 
    - Prediktionerna stämmer dock inte så jättebra - tid på dygn gör väldigt lite både för pris och tidsåtgång. 
  



