import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd

from preprocess import build_preprocessor

def train_model(df: pd.DataFrame, target_col: str, model_path: str = "models/rf_model.joblib"):
    preprocessor, X_train, X_valid, y_train, y_valid = build_preprocessor(df, target_col)

    # Define the model
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    # Create full pipeline
    from sklearn.pipeline import Pipeline
    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # Train
    clf.fit(X_train, y_train)

    # Evaluate on validation set
    preds = clf.predict(X_valid)
    mae = mean_absolute_error(y_valid, preds)
    rmse = np.sqrt(np.mean((y_valid - preds) ** 2))
    print(f"Validation MAE: {mae}")
    print(f"Validation RMSE: {rmse}")

    # Save model
    import os
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")