import time
import board
import busio
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = busio.I2C(board.IO5, board.IO4)
ss = Seesaw(i2c_bus, addr = 0x36)

while True:
    #read moisture level in Raw Capacitance Units
    moist = ss.moisture_read()
    print("Moisture: " + str(moist))

    #read temperature in C
    temp = ss.get_temp()
    print("Temperature: " + str(temp))

    time.sleep(1)
