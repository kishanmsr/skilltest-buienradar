import schedule
import time
from etl_buienradar import main

schedule.every(20).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(60)


# I would use a code like this to automate the population of the database with all measurements for a specific day.