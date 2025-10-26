# Dutch Weather Analysis — Zypp Skill Test

This project is part of the Zypp skill test and demonstrates skills in:

- Data integration (ETL)
- Data modeling with SQL
- Data analysis and visualization
- Automation (scheduling & logging)

All data comes from the Buienradar API, which provides current weather measurements for all stations in the Netherlands.

## Requirements

Python 3.10 or higher

Required libraries: requests, pandas, schedule, matplotlib, plotly

## Part 1 — Data Integration

The ETL script fetches live weather data from Buienradar every 20 minutes and stores it in a local SQLite database.
The database contains two tables:

- stations — information about each weather station (ID, name, coordinates, region)
- measurements — recorded measurements such as temperature, humidity, wind speed, and sunpower

The database schema is represented in erd/weather_erd.png with a one-to-many relationship from stations to measurements.

## Part 2 — Data Analysis

After collecting a full day of measurements, the analysis script answers:

- Which station recorded the highest temperature
- The average temperature across all stations
- Which station had the largest difference between feel temperature and actual temperature
- Which station is located in the North Sea

## Part 3 — Data Visualization and Automation

### Visualization
Visualizations are generated using Matplotlib and Plotly, including:

- Top 10 stations by maximum temperature
- Distribution of temperatures
- Average difference between feel and actual temperature
- Station locations plotted as a scatter map, highlighting the North Sea station

All plots are saved in the /plots/ folder.

### Automation

The ETL process can be automated to run every 20 minutes for a full day using automate_etl.py.
