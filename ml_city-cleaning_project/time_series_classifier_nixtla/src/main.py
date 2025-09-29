'''main script to run training/prediction for time series classification using Nixtla library'''

#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report

# Correct import for Nixtla's time series classifier
from nixtla import TimeSeriesClassifier  # <-- This is the correct import for the latest nixtla package

DATA_PATH = Path("../data/dmr.csv")

def load_data(path: Path):
    # Read the CSV. Adjust encoding if needed.
    df = pd.read_csv(path, parse_dates=["DATE DECLARATION"])
    # Basic sanity check for required columns
    required_cols = ["ID DECLARATION", "DATE DECLARATION", "TYPE DECLARATION", "ARRONDISSEMENT"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df

def preprocess_for_nixtla(df: pd.DataFrame):
    # Nixtla expects a long-format dataframe with columns: unique_id, ds, y, and optional exogenous variables
    # We'll use "ID DECLARATION" as unique_id, "DATE DECLARATION" as ds, "ARRONDISSEMENT" as y, and "TYPE DECLARATION" as an exogenous variable
    df = df.copy()
    df.rename(columns={
        "ID DECLARATION": "unique_id",
        "DATE DECLARATION": "ds",
        "ARRONDISSEMENT": "y",
        "TYPE DECLARATION": "type_decl"
    }, inplace=True)
    # Ensure correct types
    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    df["unique_id"] = df["unique_id"].astype(str)
    df["y"] = df["y"].astype(str)
    return df

def train_nixtla_classifier(df: pd.DataFrame):
    # Split into train/test by time (last 20% as test)
    df = df.sort_values("ds")
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    # Fit Nixtla's TimeSeriesClassifier
    clf = TimeSeriesClassifier()
    # If you have exogenous variables, pass them as X_df
    clf.fit(train_df[["unique_id", "ds", "y", "type_decl"]], freq="D")

    # Predict on test set
    preds = clf.predict(test_df[["unique_id", "ds", "type_decl"]])
    # preds is a DataFrame with columns: unique_id, ds, y_hat
    # Merge predictions with true values for evaluation
    merged = test_df.merge(preds, on=["unique_id", "ds"], how="left")
    acc = accuracy_score(merged["y"], merged["y_hat"])
    report = classification_report(merged["y"], merged["y_hat"], zero_division=0)
    return clf, acc, report, merged

def main():
    # Load data
    df = load_data(DATA_PATH)

    # Preprocess for Nixtla
    df_nixtla = preprocess_for_nixtla(df)

    # Train and evaluate Nixtla classifier
    model, acc, report, merged = train_nixtla_classifier(df_nixtla)

    print("Accuracy on hold-out test set:", acc)
    print("Classification report:\n", report)

if __name__ == "__main__":
    main()