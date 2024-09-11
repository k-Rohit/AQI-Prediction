import requests
import json
import os
from datetime import datetime

# Fetch current AQI data from OpenWeather API
def fetch_openweather_current_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from OpenWeather API (current): {response.status_code}")
        return None

# Save current data as a temporary JSON file
def save_data(data, filename):
    if data:
        os.makedirs('/Users/kumarrohit/Desktop/AQI - Prediction/data/raw', exist_ok=True)
        with open(f'/Users/kumarrohit/Desktop/AQI - Prediction/data/raw/{filename}', 'w') as f:
            json.dump(data, f)
    else:
        print(f"No data to save for {filename}")

if __name__ == "__main__":
    city = "Patna"
    weather_api_key = "e8775684fb652e1382fcaf077305e749"
    lat, lon = 25.5941, 85.1376
    
    # Fetch current data
    current_data = fetch_openweather_current_data(lat, lon, weather_api_key)
    save_data(current_data, 'current_data.json')
