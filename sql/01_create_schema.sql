-- Table 1: locations
CREATE TABLE IF NOT EXISTS locations (
    location_id   SERIAL PRIMARY KEY,
    city          VARCHAR(100),
    country_code  CHAR(2),
    latitude      FLOAT,
    longitude     FLOAT,
    timezone      VARCHAR(50),
    elevation_m   FLOAT
);

-- Table 2: weather_observations
CREATE TABLE IF NOT EXISTS weather_observations (
    observation_id       SERIAL PRIMARY KEY,
    location_id          INT REFERENCES locations(location_id), 
    observed_at          TIMESTAMPTZ,
    temperature_c        FLOAT,
    humidity_pct         FLOAT,
    wind_speed_kmh       FLOAT,
    wind_direction_deg   FLOAT,
    precipitation_mm     FLOAT,
    surface_pressure_hpa FLOAT,
    weather_code         INT,

    CONSTRAINT unique_location_observation UNIQUE(location_id, observed_at)
);