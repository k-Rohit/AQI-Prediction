import streamlit as st
import pandas as pd
import requests
import joblib
import os
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

# File paths
historical_data_file = "/Users/kumarrohit/Desktop/AQI - Prediction/data/processed/historical_data.csv"
current_data_file = "/Users/kumarrohit/Desktop/AQI - Prediction/data/processed/current_data.csv"
model_file = "/Users/kumarrohit/Desktop/AQI - Prediction/models/random_forest_model.pkl"

# Function to process current AQI data
def fetch_and_process_current_data(api_key, lat, lon):
    api_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()['list']
        data_list = []
        for hourly_data in data:
            aqi = hourly_data["main"]["aqi"]
            co = hourly_data["components"]["co"]
            no2 = hourly_data["components"]["no2"]
            o3 = hourly_data["components"]["o3"]
            so2 = hourly_data["components"]["so2"]
            pm2_5 = hourly_data["components"]["pm2_5"]
            pm10 = hourly_data["components"]["pm10"]
            nh3 = hourly_data["components"]["nh3"]
            dt = datetime.utcfromtimestamp(hourly_data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
            data_list.append([dt, nh3, pm10, pm2_5, so2, o3, no2, co, aqi])
        
        current_df = pd.DataFrame(data_list, columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])
        return current_df
    else:
        st.error("Error fetching data from the API")
        return pd.DataFrame()

# Function to load the model
def load_model():
    if os.path.exists(model_file):
        return joblib.load(model_file)
    else:
        st.error("Model not found!")
        return None

# Function to retrain the model
def retrain_model(data):
    X = data[['nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co']]
    y = data['aqi']
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, model_file)

# Function to generate features (daily averages)
def generate_features(data):
    data['date'] = pd.to_datetime(data['datetime']).dt.date
    daily_average = data.groupby('date').mean()[['aqi', 'pm2_5', 'pm10', 'co', 'no2', 'o3', 'so2', 'nh3']]
    daily_average = daily_average.reset_index()
    return daily_average

st.title("Real-time AQI Prediction and Model Update")

# API Key Input
api_key = st.text_input("Enter OpenWeather API Key", type="password")
latitude = st.text_input("Enter Latitude", value="25.5941")
longitude = st.text_input("Enter Longitude", value="85.1376")

# Fetch Current Data Button
if st.button("Fetch Current Data"):
    if api_key:
        current_df = fetch_and_process_current_data(api_key, latitude, longitude)
        st.dataframe(current_df)

        # Load historical data
        if os.path.exists(historical_data_file):
            historical_df = pd.read_csv(historical_data_file)
        else:
            historical_df = pd.DataFrame(columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])

        # Combine current data with historical data and drop duplicates
        combined_df = pd.concat([historical_df, current_df]).drop_duplicates(subset=['datetime']).reset_index(drop=True)

        # Save updated data
        combined_df.to_csv(historical_data_file, index=False)
        st.success("Data has been updated successfully!")

        # Load the model and make predictions
        model = load_model()
        if model:
            X_current = current_df[['nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co']]
            predictions = model.predict(X_current)
            current_df['predicted_aqi'] = predictions
            st.dataframe(current_df[['datetime', 'predicted_aqi']])

            # Retrain the model with the updated data
            retrain_model(combined_df)
            st.success("Model retrained successfully!")

            # Generate and display daily average features
            daily_avg_df = generate_features(combined_df)
            daily_avg_df.to_csv("./data/processed/average.csv", index=False)
            st.dataframe(daily_avg_df)
    else:
        st.warning("Please enter your API key!")
