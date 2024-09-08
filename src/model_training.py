# train_and_save_model.py

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_data(filename):
    return pd.read_csv(filename)

def preprocess_data(data):
    data = data.drop("date", axis=1)
    X = data.drop("aqi", axis=1)
    y = data['aqi']
    return X, y

def scale_data(X_train, X_test):
    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train)
    X_test_scaled = sc.transform(X_test)
    return X_train_scaled, X_test_scaled, sc

def train_model(X_train_scaled, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    return model

def save_model(model, scaler, model_filename, scaler_filename):
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
    with open(scaler_filename, 'wb') as file:
        pickle.dump(scaler, file)

# File paths
data_path = "/Users/kumarrohit/Desktop/AQI - Prediction/data/processed/averaged.csv"
model_path = "/Users/kumarrohit/Desktop/AQI - Prediction/models/random_forest_model.pkl"
scaler_path = "/Users/kumarrohit/Desktop/AQI - Prediction/models/scaler.pkl"

data = load_data(data_path)
X, y = preprocess_data(data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
model = train_model(X_train_scaled, y_train)

save_model(model, scaler, model_path, scaler_path)