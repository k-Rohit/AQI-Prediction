import os
import json
import pandas as pd
from datetime import datetime

data_list = []
raw_folder = "/Users/kumarrohit/Desktop/AQI - Prediction/data/raw"


for json_file in os.listdir(raw_folder):
    with open(os.path.join(raw_folder, json_file), 'r') as f:
        data = json.load(f)
        hourly_list = data['list']
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

raw_dataframe = pd.DataFrame(data_list, columns=['datetime', 'nh3', 'pm10', 'pm2_5', 'so2', 'o3', 'no2', 'co', 'aqi'])

raw_dataframe.to_csv("raw_dataframe.csv")
