import time
import board
from adafruit_seesaw.seesaw import seesaw

i2c_bus = board.I2C()
ss = seesaw(i2c_bus, addr = 0x36)

while True:
    #read moisture level
    moist = ss.moisture_read()
    print("Moisture: " + str(moist))

    #read temperature
    temp = ss.get_temp()
    print("Temperature: " + str(temp))

    time.sleep(1)