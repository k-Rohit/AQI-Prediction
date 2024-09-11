import requests
import json
import os
from datetime import datetime, timedelta
import time

# Historical data from OpenWeather API
def fetch_openweather_historical_data(lat, lon, start_date, end_date, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start_date}&end={end_date}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from OpenWeather API (historical): {response.status_code}")
        return None
# Save data to a folder
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
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Fetch historical data day by day for the past year
    for single_date in (start_date + timedelta(n) for n in range(365)):
        start_timestamp = int(single_date.timestamp())
        end_timestamp = int((single_date + timedelta(days=1)).timestamp())
        
        # Fetch data for a single day
        weather_data = fetch_openweather_historical_data(lat, lon, start_timestamp, end_timestamp, weather_api_key)
        
        if weather_data:
            # Save data only if fetched successfully
            save_data(weather_data, f"weather_{single_date.strftime('%Y-%m-%d')}.json")
        else:
            print(f"Failed to fetch data for {single_date.strftime('%Y-%m-%d')}")

        # Optional: Wait between requests to avoid hitting rate limits
        time.sleep(1)
