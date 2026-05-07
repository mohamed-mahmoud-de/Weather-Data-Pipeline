import pandas as pd

def clean_weather_data(df):
    df = df.drop_duplicates(subset=['city', 'observed_at'])
    
    df['observed_at'] = pd.to_datetime(df['observed_at'])
    
    numeric_cols = ['temperature_c', 'humidity_pct', 'wind_speed_kmh']
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())
            
    return df

if __name__ == "__main__":
    from normalize import normalize_weather_file
    import os
    
    raw_file = 'data/raw/alexandria_20260504T135020Z.json'
    if os.path.exists(raw_file):
        _, raw_df = normalize_weather_file(raw_file)
        cleaned_df = clean_weather_data(raw_df)
        print(" Data Cleaning Logic Applied Successfully!")
        print(f"Rows after cleaning: {len(cleaned_df)}")