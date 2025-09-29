import pandas as pd
import joblib
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


def main():
    
    df = pd.read_csv(DATA_PATH / "cleaned_taxi_trip_pricing.csv")       #Läser in datan
   
    target = "Trip_Price"                                               #Väljer feature_target => det som senare prediktas

    numeric_features = [
        "Trip_Distance_km", "Passenger_Count", "Base_Fare",             #Numeriska kolumner
        "Per_Km_Rate", "Per_Minute_Rate", "Trip_Duration_Minutes"
    ]
    categorical_features = [
        "Time_of_Day", "Day_of_Week", "Traffic_Conditions", "Weather"   #Kategoriska kolumner
    ]

    X = df[numeric_features + categorical_features].copy()             #Dela upp kolumnerna i X och y
    y = df[target].copy()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features), #Omvandlar kategoriska kolumner till numeriska värden
            ("num", "passthrough", numeric_features),
        ]
    )

    model = LinearRegression()

    pipe = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
    pipe.fit(X_train, y_train)

 
    MODELS_PATH.mkdir(parents=True, exist_ok=True)                      #Sparar pipeline + feature-ordning (så API:t skickar i rätt ordning)
    joblib.dump(
        {
            "pipeline": pipe,
            "feature_order": numeric_features + categorical_features,
            "target": target,
        },
        MODELS_PATH / "taxi_price_pipeline.joblib"
    )
    print(f"Saved: {MODELS_PATH / 'taxi_price_pipeline.joblib'}")

if __name__ == "__main__":
    main()