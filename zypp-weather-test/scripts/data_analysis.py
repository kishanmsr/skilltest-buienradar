import sqlite3
import pandas as pd

DB_PATH = "data/buienradar.db"

conn = sqlite3.connect(DB_PATH)
stations = pd.read_sql("SELECT * FROM stations", conn)
measurements = pd.read_sql("SELECT * FROM measurements", conn)

# Merge databases
df = measurements.merge(stations, on="stationid", how="left")

# Q5: Station with highest temperature
max_temp_row = df.loc[df["temperature"].idxmax()]
print(f"Q5: Highest temperature recorded by: {max_temp_row['stationname']} ({max_temp_row['temperature']}°C)")

# Q6: Average temperature
avg_temp = df["temperature"].mean()
print(f"Q6: Average temperature across all stations: {avg_temp:.2f}°C")

# Q7: Station with largest difference between feel and actual temperature
df["temp_diff"] = abs(df["feeltemperature"] - df["temperature"])
max_diff_row = df.loc[df["temp_diff"].idxmax()]
print(f"Q7: Largest feel vs actual difference at: {max_diff_row['stationname']} ({max_diff_row['temp_diff']:.2f}°C difference)")

# Q8: Station located in the North Sea
north_sea = df[df["regio"].str.lower().str.contains("noordzee", na=False)]
if not north_sea.empty:
    print(f"Q8: Station(s) located in the North Sea:\n{north_sea[['stationid','stationname','regio']]}")
else:
    print("Q8: No station found explicitly named 'Noordzee'. Check regio manually.")
