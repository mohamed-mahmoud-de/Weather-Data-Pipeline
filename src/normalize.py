import pandas as pd
import json
import os

def normalize_weather_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Location Info
    location_data = {
        'city': os.path.basename(file_path).split('_')[0].capitalize(),
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'timezone': data['timezone'],
        'elevation_m': data.get('elevation', 0)
    }
    
    # 2. Hourly Weather Info
    hourly_raw = data.get('hourly', {})
    times = hourly_raw.get('time', [])
    
    hourly_records = []
    for i in range(len(times)):
        record = {
            'city': location_data['city'],
            'observed_at': times[i],
            'temperature_c': hourly_raw.get('temperature_2m', [])[i],
            'humidity_pct': hourly_raw.get('relative_humidity_2m', [])[i],
            'wind_speed_kmh': hourly_raw.get('wind_speed_10m', [])[i],
            'weather_code': hourly_raw.get('weather_code', [])[i]
        }
        hourly_records.append(record)
    
    return location_data, pd.DataFrame(hourly_records)

if __name__ == "__main__":
    raw_dir = 'data/raw'
    files = [f for f in os.listdir(raw_dir) if f.endswith('.json')]
    
    if files:
        test_file = os.path.join(raw_dir, files[0])
        loc, df = normalize_weather_file(test_file)
        
        print(f"\n--- Success! Normalized City: {loc['city']} ---")
        print(f"Total Hours Processed: {len(df)}")
        print("\nTable Preview (First 5 Rows):")
        print(df.head())
