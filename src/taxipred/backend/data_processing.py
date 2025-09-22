import pandas as pd
from taxipred.utils.constants import TAXI_CSV_PATH
import json
from pprint import pprint

df = pd.read_csv(TAXI_CSV_PATH)

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(TAXI_CSV_PATH)

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))
    

print(df.info())

# taxi = TaxiData().to_json()

# pprint(taxi)