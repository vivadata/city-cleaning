#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Tuple, Dict, Any

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# If you later test a regressor variant (optional):
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# ---- Paths ----
DATA_PATH = Path("../data/dmr.csv")

# ------------------------------------------------------------
# 1) Load data
# ------------------------------------------------------------
def load_data(path: Path) -> pd.DataFrame:
    """
    Load the CSV and ensure the required columns exist.
    We parse the date column to datetime.
    """
    # Adjust encoding or sep if needed for your file
    df = pd.read_csv(path, parse_dates=["DATE DECLARATION"])

    required = [
        "ID DECLARATION",
        "DATE DECLARATION",
        "TYPE DECLARATION",
        "ARRONDISSEMENT",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df

# ------------------------------------------------------------
# 2) Time-aware preprocessing + window features
# ------------------------------------------------------------
def make_time_features(
    df: pd.DataFrame,
    window_size: int = 3,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Create a minimal time-aware feature set:
    - Sort by DATE DECLARATION (so 'past' rows come before 'future' rows)
    - Create DATE_ORD as numeric time (ordinal)
    - Build a rolling frequency feature over the last `window_size` rows.
      This acts like a small “window scaling/summary” that captures local repetitions.

    Returns:
      X: DataFrame with engineered features
      y: Series of the target labels as strings (classification)
    """
    df = df.copy()

    # Ensure datetime
    if not pd.api.types.is_datetime64_any_dtype(df["DATE DECLARATION"]):
        df["DATE DECLARATION"] = pd.to_datetime(df["DATE DECLARATION"], errors="coerce")

    # Sort by time (important for any rolling/window logic)
    df.sort_values("DATE DECLARATION", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Target as string labels (classification)
    y = df["ARRONDISSEMENT"].astype(str)

    # Base X with only the specified features
    X = df[["ID DECLARATION", "DATE DECLARATION", "TYPE DECLARATION"]].copy()

    # Numeric “time” feature from date
    X["DATE_ORD"] = X["DATE DECLARATION"].apply(lambda d: d.toordinal())

    # Rolling/window context:
    # We'll compute, for each row, the max frequency of any ARRONDISSEMENT in the last `window_size` rows.
    y_num = pd.factorize(y)[0]
    df["ARR_NUM"] = y_num

    roll_counts = (
        df["ARR_NUM"]
        .rolling(window=window_size, min_periods=1)
        .apply(lambda s: s.value_counts().max(), raw=False)
        .astype(float)
    )
    X["ROLL_MAX_ARR_DIS"] = roll_counts

    # We no longer need the raw date after extracting DATE_ORD
    X.drop(columns=["DATE DECLARATION"], inplace=True)

    # Ensure category-like columns are strings (safe for OHE)
    X["ID DECLARATION"] = X["ID DECLARATION"].astype(str)
    X["TYPE DECLARATION"] = X["TYPE DECLARATION"].astype(str)

    return X, y

# ------------------------------------------------------------
# 3) Build preprocessing pipelines (with scaling)
# ------------------------------------------------------------
def build_preprocessor(numeric_cols, categorical_cols) -> ColumnTransformer:
    """
    “Time series scaling / window scaling” idea implemented safely:
    - Fit imputer + StandardScaler ONLY on the training split (sklearn Pipeline handles this)
    - That means your means/medians/stds come from the past (train), not from the future (test)
    - For categories, we impute and one-hot encode.

    Note:
    - In Nixtla docs, you’ll see why scaling per series and careful treatment of exogenous features matters.
      Here we do a simple, global StandardScaler on numeric time/window features,
      which is the safest starting point for your dataset split.
    """
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    return preprocessor

# ------------------------------------------------------------
# 4) Train a CLASSIFIER (predict ARRONDISSEMENT)
# ------------------------------------------------------------
def train_classifier(
    X: pd.DataFrame, y: pd.Series, preprocessor: ColumnTransformer
) -> Tuple[Pipeline, Dict[str, Any]]:
    """
    Train a time-aware classifier using a pipeline:
    preprocessor -> classifier (LogisticRegression or RandomForest)
    """
    # Train/test split. Stratify to preserve class proportions.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Start with a simple linear model. You can swap to RandomForestClassifier easily.
    # clf_estimator = LogisticRegression(max_iter=1000)
    clf_estimator = RandomForestClassifier(
        n_estimators=300, random_state=42, n_jobs=-1, class_weight="balanced_subsample"
    )

    clf = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf_estimator),
        ]
    )

    clf.fit(X_train, y_train)

    # Predictions on both train and test
    train_pred = clf.predict(X_train)
    test_pred = clf.predict(X_test)

    # Simple metrics
    metrics = {
        "train_accuracy": float(accuracy_score(y_train, train_pred)),
        "test_accuracy": float(accuracy_score(y_test, test_pred)),
        "classification_report_test": classification_report(
            y_test, test_pred, zero_division=0
        ),
    }

    return clf, metrics

# ------------------------------------------------------------
# (Optional) 5) Train a REGRESSOR
# ------------------------------------------------------------
def train_regressor(
    X: pd.DataFrame, y_numeric: pd.Series, preprocessor: ColumnTransformer
) -> Tuple[Pipeline, Dict[str, float]]:
    """
    If you ever need a regression example (y must be numeric).
    For ARRONDISSEMENT, this only makes sense if you convert to numbers and treat them as ordinal,
    which is usually NOT recommended for arrondissement classification.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_numeric, test_size=0.2, random_state=42
    )

    reg = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)),
        ]
    )

    reg.fit(X_train, y_train)

    train_pred = reg.predict(X_train)
    test_pred = reg.predict(X_test)

    metrics = {
        "train_mae": float(mean_absolute_error(y_train, train_pred)),
        "test_mae": float(mean_absolute_error(y_test, test_pred)),
        "test_r2": float(r2_score(y_test, test_pred)),
    }
    return reg, metrics

# ------------------------------------------------------------
# 6) Main
# ------------------------------------------------------------
def main() -> None:
    # Load your data
    df = load_data(DATA_PATH)

    # Build time-aware features and target
    X, y = make_time_features(df, window_size=3)

    # Define which columns are numeric vs categorical for preprocessing
    categorical_cols = ["ID DECLARATION", "TYPE DECLARATION"]
    numeric_cols = ["DATE_ORD", "ROLL_MAX_ARR_DIS"]

    preprocessor = build_preprocessor(numeric_cols, categorical_cols)

    # ---- Classification path (recommended for ARRONDISSEMENT) ----
    model_cls, cls_metrics = train_classifier(X, y, preprocessor)

    print("=== CLASSIFICATION RESULTS (ARRONDISSEMENT) ===")
    print("Train Accuracy:", cls_metrics["train_accuracy"])
    print("Test  Accuracy:", cls_metrics["test_accuracy"])
    print("Test Classification Report:\n", cls_metrics["classification_report_test"])

    # Example of how to get predictions for the whole dataset (if needed)
    # y_all_pred = model_cls.predict(X)
    # df["PRED_ARRONDISSEMENT"] = y_all_pred

    # ---- Optional: regression path (only if you truly need a numeric target) ----
    # Not recommended for arrondissement categories, but shown for completeness.
    # y_num = pd.factorize(y)[0]  # convert categories to numeric codes
    # model_reg, reg_metrics = train_regressor(X, pd.Series(y_num), preprocessor)
    # print("\n=== REGRESSION RESULTS (NUMERIC-ENCODED ARR) ===")
    # print("Train MAE:", reg_metrics["train_mae"])
    # print("Test  MAE:", reg_metrics["test_mae"])
    # print("Test  R^2:", reg_metrics["test_r2"])

    # Save model (optional)
    # import joblib
    # joblib.dump(model_cls, "models/arrondissement_classifier.joblib")

if __name__ == "__main__":
    main()
