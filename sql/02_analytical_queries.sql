SELECT l.city, COUNT(*) AS total_observations
FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city
ORDER BY total_observations DESC;

SELECT l.city, MAX(o.observed_at) AS latest_reading
FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city;

SELECT l.city, ROUND(AVG(o.temperature_c)::numeric, 2) AS avg_temp_c
FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city
ORDER BY avg_temp_c DESC;

SELECT l.city, o.observed_at, o.temperature_c
FROM weather_observations o
JOIN locations l USING(location_id)
ORDER BY o.temperature_c DESC
LIMIT 1;

SELECT l.city, COUNT(*) AS null_temp_count
FROM weather_observations o
JOIN locations l USING(location_id)
WHERE o.temperature_c IS NULL
GROUP BY l.city;

SELECT l.city, ROUND(AVG(o.humidity_pct)::numeric, 2) AS avg_humidity
FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city
ORDER BY avg_humidity DESC;

SELECT l.city, MAX(o.wind_speed_kmh) AS max_wind_kmh
FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city
ORDER BY max_wind_kmh DESC;
