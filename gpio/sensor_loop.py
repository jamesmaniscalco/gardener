import time
import sensor_helpers

sensor_read_delay = 20  # seconds between consecutive readings

# get all sensors listed in the database
cmd = 'SELECT * FROM sensors'
sensor_helpers.c.execute(cmd)
response = sensor_helpers.c.fetchall()

# make a list of the sensor objects
sensors = []
for row in response:
    sensors.append(sensor_helpers.MoistureSensor(row[0]))

# perform the loop
while True:
    for s in sensors:
        s.write_to_db(s.voltage())
    time.sleep(sensor_read_delay)

