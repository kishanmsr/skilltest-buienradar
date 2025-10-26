# Import libraries

import requests
import sqlite3
from datetime import datetime
import pandas as pd
import os
import time

# API connection
DB_PATH = "data/buienradar.db"
API_URL = "https://data.buienradar.nl/2.0/feed/json"

def fetch_weather_data():
    """Get JSON data from Buienradar API."""
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

# Extract station and measurement data
def extract_station_data(data):
    """Extract station info."""
    stations = []
    for s in data["actual"]["stationmeasurements"]:
        stations.append({
            "stationid": s.get("stationid"),
            "stationname": s.get("stationname"),
            "lat": s.get("lat"),
            "lon": s.get("lon"),
            "regio": s.get("regio")
        })
    return pd.DataFrame(stations).drop_duplicates("stationid")

def extract_measurements(data):
    """Extract measurement info."""
    measurements = []
    now = datetime.utcnow().isoformat()
    for s in data["actual"]["stationmeasurements"]:
        measurements.append({
            "measurementid": f"{s.get('stationid')}_{now}",
            "timestamp": now,
            "temperature": s.get("temperature"),
            "groundtemperature": s.get("groundtemperature"),
            "feeltemperature": s.get("feeltemperature"),
            "windgusts": s.get("windgusts"),
            "windspeedBft": s.get("windspeedBft"),
            "humidity": s.get("humidity"),
            "precipitation": s.get("precipitation"),
            "sunpower": s.get("sunpower"),
            "stationid": s.get("stationid")
        })
    return pd.DataFrame(measurements)

# Create database
def init_db():
    """Create database."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        stationid INTEGER PRIMARY KEY,
        stationname TEXT,
        lat REAL,
        lon REAL,
        regio TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        measurementid TEXT PRIMARY KEY,
        timestamp TEXT,
        temperature REAL,
        groundtemperature REAL,
        feeltemperature REAL,
        windgusts REAL,
        windspeedBft INTEGER,
        humidity REAL,
        precipitation REAL,
        sunpower REAL,
        stationid INTEGER,
        FOREIGN KEY (stationid) REFERENCES stations(stationid)
    );
    """)

    conn.commit()
    conn.close()

# Store data
def store_data(stations_df, measurements_df):
    """Store data in database."""
    conn = sqlite3.connect(DB_PATH)
    stations_df.to_sql("stations", conn, if_exists="append", index=False)
    measurements_df.to_sql("measurements", conn, if_exists="append", index=False)
    conn.close()

# Execute code
def main():
    print("Fetching weather data from Buienradar...")
    data = fetch_weather_data()

    print("Extracting data...")
    stations_df = extract_station_data(data)
    measurements_df = extract_measurements(data)

    print("Initializing database...")
    init_db()

    print("Storing data...")
    store_data(stations_df, measurements_df)
    print("Data successfully stored!")

if __name__ == "__main__":
    main()