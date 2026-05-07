import pandas as pd
from sqlalchemy import create_engine
from normalize import normalize_weather_file
from clean import clean_weather_data
import os

DB_URL = "postgresql://postgres:postgres@localhost:5432/weather_db"

def load_data_to_db(df):
    engine = create_engine(DB_URL)
    
    
    df.to_sql('weather_observations', engine, if_exists='append', index=False)
    print(f"✅ Successfully loaded {len(df)} rows to Database!")

if __name__ == "__main__":
    raw_dir = 'data/raw'
    files = [f for f in os.listdir(raw_dir) if f.endswith('.json')]
    
    if files:
        test_file = os.path.join(raw_dir, files[0])
        _, raw_df = normalize_weather_file(test_file)
        cleaned_df = clean_weather_data(raw_df)
        
        load_data_to_db(cleaned_df)