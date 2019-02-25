import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import sqlite3
import os
import runpy

# import configuration (to get the DB path)
APP_INSTANCE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../var/app-instance/config.py' ))
CONFIG = runpy.run_path(APP_INSTANCE_PATH)

# connect to the database
db = sqlite3.connect(CONFIG['DATABASE'])
c = db.cursor()

# i2c/ADC setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)  # this may have to change later if we have multiple ADCs

class MoistureSensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        # get the port and voltage limits from the db
        cmd = 'SELECT * FROM sensors WHERE id = {:d}'.format(sensor_id)
        c.execute(cmd)
        db_row = c.fetchone()
        self.db_id = db_row[0]
        self.port = db_row[1]
        self.V_high = db_row[2]
        self.V_low = db_row[3]
        self.pump_pin = db_row[4]
        self.low_m_pct = db_row[5]
        self.high_m_pct = db_row[6]
        self.last_watering = db_row[7]
        self.auto_watering_on = db_row[8]
        # get the port object
        port_dict = {0:ADS.P0, 1:ADS.P1, 2:ADS.P2, 3:ADS.P3}
        self.chan = AnalogIn(ads, port_dict[self.port])

    def info(self):
        # print info about the sensor
        print('id = {}'.format(self.sensor_id))
        print('port = {}'.format(self.port))
        print('V_high = {}'.format(self.V_high))
        print('V_low = {}'.format(self.V_low))
 
    def voltage(self):
        return self.chan.voltage

    def moisture(self):
        # moisture percentage
        return (self.chan.voltage - self.V_low) / (self.V_high - self.V_low) * 100

    def write_to_db(self, voltage):
        cmd = 'INSERT INTO readings (sensor_id, voltage) VALUES ({:d}, {:f});'.format(self.sensor_id, voltage)
        #print(cmd)
        c.execute(cmd)
        db.commit()

    def mark_watering_time(self):
        cmd = 'UPDATE readings SET last_watering = date("now") WHERE id = {:d}'.format(self.db_id)
        c.execute(cmd)
        db.commit()


