import pandas as pd
import joblib
from taxipred.utils.constants import DATA_PATH, MODELS_PATH
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

def main():
    df = pd.read_csv(DATA_PATH / "taxi_clean.csv")
    target = "Trip_Price"
    
    X = df.drop(columns=[target]).copy()
    y = df[target].copy()

   
    num_cols = X.select_dtypes(include="number").columns
    cat_cols = X.select_dtypes(exclude="number").columns
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

   
    pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    pipe.fit(X, y)

    
    MODELS_PATH.mkdir(parents=True, exist_ok=True)
    out_path = MODELS_PATH / "taxi_price_regressor_new.joblib"
    joblib.dump(pipe, out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
