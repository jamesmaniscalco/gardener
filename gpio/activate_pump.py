import board
import time
import digitalio

def activate_pump(pump_pin, pump_time):
    port = digitalio.DigitalInOut(getattr(board, 'D' + '{}'.format(pump_pin)))
    port.direction = digitalio.Direction.OUTPUT
    
    port.value = False
    time.sleep(pump_time)
    port.value = True


