import time
import board
import busio
import adafruit_ccs811
import adafruit_apds9960.apds9960
from adafruit_seesaw.seesaw import Seesaw

i2c = busio.I2C(scl=board.IO5,sda=board.IO4)
airSensor = adafruit_ccs811.CCS811(i2c)
ss = Seesaw(i2c, addr=0x36)
lightSensor = adafruit_apds9960.apds9960.APDS9960(i2c)
lightSensor.enable_color = True
lightSensor.enable_proximity = True
lightSensor.enable_gesture = True

#max 5s sensor updates: FIX

def get_eco2():
    count=0
    eco2=0
    while((eco2 == 0) and (count<10)):
        eco2 = max(eco2, airSensor.eco2)
        count += 1
        time.sleep(.15)
    return eco2

def get_tvoc():
    count=0
    tvoc=0
    while((tvoc == 0) and (count<10)):
        tvoc = max(tvoc, airSensor.tvoc)
        count += 1
        time.sleep(.15)
    return tvoc

#FIX
def get_moisture():
    if ss.moisture_read() > 1000:
        return 100
    return (ss.moisture_read() - 300) / 7

def get_temp():
    offset = -8
    return ss.get_temp()*(9/5)+32 + offset
    
def get_light():
    #count=0
    #c=0
    #while((c == 0) and (count<10)):
    _, _, _, c = lightSensor.color_data #4 Tuple Want Clear for Light Intensity    
    #count += 1
    #time.sleep(.15)
    return c / 65535 * 100

def get_eco2_tvoc():
    count=0
    eco2=0
    tvoc=0
    tempEco2 = 0
    tempTvoc = 0
    while(((eco2 == 0) or (tvoc==0)) and (count<10)):
        tempEco2 = airSensor.eco2
        tempTvoc = airSensor.tvoc
        if tempEco2 is None:
            tempEco2 = 0
        if tempTvoc is None:
            tempTvoc = 0
        eco2 = max(eco2, tempEco2)
        tvoc = max(tvoc, tempTvoc)
        count += 1
        time.sleep(.4)
    return int(eco2), int(tvoc)

#FIXED
'''
Traceback (most recent call last):
  File "code.py", line 81, in <module>
  File "i2csensors.py", line 57, in get_eco2_tvoc
TypeError: unsupported types for __gt__: 'NoneType', 'int'

Might be an issue with the sensor not returning data (for some reason),
and max() can't deal with NoneType. if none, set to 0?
'''

'''
Traceback (most recent call last):
  File "code.py", line 270, in <module>
  File "i2cSensors.py", line 59, in get_eco2_tvoc
  File "adafruit_ccs811.py", line 221, in eco2
  File "adafruit_ccs811.py", line 174, in _update_data
  File "adafruit_register/i2c_bit.py", line 59, in __get__
OSError: [Errno 116] ETIMEDOUT
'''