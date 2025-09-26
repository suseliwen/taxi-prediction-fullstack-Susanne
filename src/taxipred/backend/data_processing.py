import pandas as pd
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
import json
from fastapi.responses import  JSONResponse
from pprint import pprint

df = pd.read_csv(DATA_PATH / "cleaned_taxi_trip_pricing.csv")

class DataExplorer:
    def __init__(self, df, limit=100):
        self.df_full = df
        self._df = df.head(limit)

    def summary(self):
        self._df = self.df_full.describe().T.reset_index()
        return self

    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))

class TaxiData:
    def __init__(self, filename="cleaned_taxi_trip_pricing.csv"):
        self.df = pd.read_csv(DATA_PATH / filename)

        self.df = self.df.round(2) #avrundar till två decimaler

    def to_json(self):
        return json.loads(self.df.to_json(orient="records", double_precision=2))
    

print(df.info())


if __name__ == "__main__":
    taxi = TaxiData()
    print(taxi.to_json())