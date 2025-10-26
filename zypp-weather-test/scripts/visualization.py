import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Setup
os.makedirs("plots", exist_ok=True)
DB_PATH = "data/buienradar.db"
conn = sqlite3.connect(DB_PATH)

# Load tables
stations = pd.read_sql("SELECT * FROM stations", conn)
measurements = pd.read_sql("SELECT * FROM measurements", conn)
conn.close()

# Merge for joined analysis
df = measurements.merge(stations, on="stationid", how="left")

# Q5: Highest temperature per station
max_temp = df.groupby("stationname")["temperature"].max().sort_values(ascending=False)
plt.figure(figsize=(10,5))
max_temp.head(10).plot(kind="bar", color="tomato")
plt.title("Top 10 Stations by Highest Recorded Temperature")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/max_temperature.png")
plt.close()

# Q6: Average temperature
plt.figure(figsize=(10,5))
max_temp.plot(kind="box", color="skyblue")
plt.title("Distribution of Recorded Temperatures")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig("plots/avg_temperature.png")
plt.close()

# Q7: Difference between feel and actual temperature
df["temp_diff"] = (df["feeltemperature"] - df["temperature"]).abs()
avg_diff = df.groupby("stationname")["temp_diff"].mean().sort_values(ascending=False)
plt.figure(figsize=(10,5))
avg_diff.head(10).plot(kind="bar", color="steelblue")
plt.title("Average Feel vs Actual Temperature Difference")
plt.ylabel("Difference (°C)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/temp_difference.png")
plt.close()

# Q8: Station map (interactive)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/buienradar.db")
stations = pd.read_sql("SELECT * FROM stations", conn)
conn.close()

plt.figure(figsize=(8,6))
plt.scatter(stations["lon"], stations["lat"], color="teal", s=60)

# Label stations
for _, row in stations.iterrows():
    plt.text(row["lon"]+0.02, row["lat"], row["stationname"], fontsize=8)

plt.title("Buienradar Weather Stations (Latitude vs Longitude)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/station_scatter.png")
plt.show()

north_sea = stations[stations["regio"].str.lower().str.contains("noordzee", na=False)]
plt.scatter(north_sea["lon"], north_sea["lat"], color="red", s=120, marker="*", label="North Sea Station")
plt.legend()


