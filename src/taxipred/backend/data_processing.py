import pandas as pd
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
import json
from fastapi.responses import  JSONResponse
from pprint import pprint

df = pd.read_csv(DATA_PATH / "taxi_clean.csv")

class DataExplorer:
    def __init__(self, df: pd.DataFrame, limit:int | None = 100):
        self.df_full = df.copy()
        self._df = df.head(limit) if limit else df   

    @property
    def df(self) -> pd.DataFrame:
        return self._df
    
    def head(self, n: int = 100):
        self._df = self.df_full.head(n)
        return self

    def summary(self):
        self._df = self.df_full.describe(include= "all").T.reset_index()
        return self
    
    def kpis(self):
        df = self.df_full

        return {
            "n_trips": int(len(df)),
            "total_km": float(df["Trip_Distance_km"].sum()),
            "avg_km_per_trip": float(df["Trip_Distance_km"].mean()),
            "total_revenue": float(df["Trip_Price"].sum())
        }
    

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