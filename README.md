
### Resekollen Taxi – Pris­prediktion (Backend | Frontend | ML)


 - Projektet syftar till att implementera backend och frontend för att lösa ett verklighetsnära problem.   
 - Backenden och frontenden kommunicerar via ett API-lager för att göra komponenterna decoupled från   
 varandra.   
 - Applikationen kommer servea en machine learning modell för att göra relevanta predictions.


# Stå i src/taxipred/data med sweden-YYYYMM.osm.pbf
docker run -t -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend \
  osrm-extract -p /opt/car.lua /data/sweden-YYYYMM.osm.pbf
docker run -t -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend \
  osrm-partition /data/sweden-YYYYMM.osrm
docker run -t -p 5000:5000 -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend \
  osrm-routed --algorithm mld /data/sweden-YYYYMM.osrm

 
