import os
import json
import pandas as pd
from datetime import datetime

# Define file paths
historical_data_file = "/Users/kumarrohit/Desktop/AQI - Prediction/data/raw/raw_dataframe.csv"
current_data_file = "/Users/kumarrohit/Desktop/AQI - Prediction/data/raw/current_data.json"

# Load the historical data if it exists, otherwise create an empty DataFrame
if os.path.exists(historical_data_file):
    historical_df = pd.read_csv(historical_data_file)
else:
    historical_df = pd.DataFrame(columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])

# Process the current data from the current_data.json file
def process_current_data(file_path):
    data_list = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        hourly_list = data['list']
        
        # Loop through the hourly data in the current data file
        for hourly_data in hourly_list:
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
    
    # Return the processed current data as a DataFrame
    return pd.DataFrame(data_list, columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])

# Check if current data exists, and if it does, process it
if os.path.exists(current_data_file):
    current_df = process_current_data(current_data_file)
else:
    current_df = pd.DataFrame(columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])

# Concatenate the historical data with the current data, remove duplicates based on 'datetime'
combined_df = pd.concat([historical_df, current_df]).drop_duplicates(subset=['datetime']).reset_index(drop=True)

# Save the updated data back to the historical data file
combined_df.to_csv(historical_data_file, index=False)

print(f"Data successfully updated. New shape: {combined_df.shape}")
