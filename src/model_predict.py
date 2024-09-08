import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

def load_data(filename):
    return pd.read_csv(filename)

def preprocess_data(data):
    data = data.drop("date", axis=1)
    X = data.drop("aqi", axis=1)
    return X

def scale_data(X, scaler):
    return scaler.transform(X)

def load_model_and_scaler(model_filename, scaler_filename):
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    with open(scaler_filename, 'rb') as file:
        scaler = pickle.load(file)
    return model, scaler

def make_prediction(model, scaler, data_path):
    data = load_data(data_path)
    X = preprocess_data(data)
    X_scaled = scale_data(X, scaler)
    predictions = model.predict(X_scaled)
    return predictions

model_path = "/Users/kumarrohit/Desktop/AQI - Prediction/models/random_forest_model.pkl"
scaler_path = "/Users/kumarrohit/Desktop/AQI - Prediction/models/scaler.pkl"
new_data_path = "/Users/kumarrohit/Desktop/AQI - Prediction/data/processed/new_data.csv"

model, scaler = load_model_and_scaler(model_path, scaler_path)

predictions = make_prediction(model, scaler, new_data_path)

print(predictions)
