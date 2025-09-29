import joblib
import pandas as pd

def load_model(model_path: str):
    return joblib.load(model_path)

def predict(model, df: pd.DataFrame):
    preds = model.predict(df)
    return preds

def main():
    model_path = "models/rf_model.joblib"
    df_new = pd.read_csv("data/input_new.csv")  #new data for prediction
    model = load_model(model_path)
    preds = predict(model, df_new)
    print("Predictions:", preds)

if __name__ == "__main__":
    main()