import time
import sensor_helpers
from activate_pump import activate_pump
import datetime as dt
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from numpy import *

sensor_read_delay = 20  # seconds between consecutive readings

# get all sensors listed in the database
cmd = 'SELECT * FROM sensors'
sensor_helpers.c.execute(cmd)
response = sensor_helpers.c.fetchall()

# make a list of the sensor objects
sensors = []
for row in response:
    sensors.append(sensor_helpers.MoistureSensor(row[0]))

# keep track of what is currently being watered
currently_watering = zeros(shape(sensors), dtype=bool)

# perform the loop
while True:
    for i in range(len(sensors)):
        s = sensors[i]
        # read the voltage
        v = s.voltage()
        s.write_to_db(v)
        # check if it's time to water the plant
        # first check if the last watering was more than a day ago (or has never been recorded):
        if parse(s.last_watering) < dt.datetime.now()-relativedelta(days=1) or s.last_watering == '':
            # check if we are currently watering:
            if not currently_watering[i]:
                # check if the moisture level is too low:
                if s.moisture() < s.low_m_pct:
                    # activate the pump for 0.5 seconds:
                    activate_pump(s.pump_pin, 0.5)
                    # mark that we are actively watering this plant:
                    currently_watering[i] = True
            else: # if indeed we are watering currently,
                # check whether the moisture is above the upper threshold:
                if s.moisture() < s.high_m_pct:
                    # activate the pump if we are still below
                    activate_pump(s.pump_pin, 0.5)
                else: # if we are now above the upper limit,
                    # stop the watering procedure and mark the time.
                    currently_watering[i] = False
                    s.mark_watering_time() 



    time.sleep(sensor_read_delay)

