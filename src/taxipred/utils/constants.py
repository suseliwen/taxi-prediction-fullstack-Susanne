
from importlib.resources import files

TAXI_CSV_PATH = files("taxipred").joinpath("data/cleaned_taxi_trip_pricing.csv") #absolute path to the csv-file in data


print(TAXI_CSV_PATH)