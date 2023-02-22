import time
import board #low level control for ESP32 hardware
import busio
from adafruit_seesaw.seesaw import Seesaw #needed for moisture / temperature reading
from adafruit_hcsr04 import HCSR04 #importing code for the Ultrasonic Sensor

#####Defining Constants#####
heightoftank = 3 ##Needs to be updated
airmoisture = 3 ##Needs to be updated
watermoisture = 3 ##Needs to be updated

# Initialize the ultrasonic sensor
# Trigger is initialised to pin 4 and Echo is initialised to pin 5
sonar = HCSR04(board.IO4, board.IO5)

# Initialize the Moisture & Temp sensor
# SCL is initialised to pin 5 and SDA is initialised to pin 4
i2c_bus = busio.I2C(board.IO5, board.IO4)
ss = Seesaw(i2c_bus, addr = 0x36)

#function to check if plant is within 3 inches of grow lights
def plantheight():
    try:
        #Measure distance and convert to inches
        distance = sonar.distance/2.54
        #Check if within 3 inches
        if (distance <= 3):
            return True
        else:
            return False

    except:
        print("Error Measuring Plant Height")
        return -1

#function to check water level of tank
def waterlevel():
    try:
        #Measure distance and convert to inches
        distance = sonar.distance/2.54
        #Subtracting distance of water from distance to tank to calculate water level
        level = heightoftank - distance
        return level
    
    except:
        print("Error Measuring Water Level")
        return -1

#function to check soil moisture level
def soilmoisturelevel():
    try:
        #read moisture level in Raw Capacitance Units
        moist = ss.moisture_read()
        #Convert moisture to Volumetric Water Content
        moisture = ((airmoisture - moist) / (airmoisture - watermoisture)) * 100
        return moisture
    
    except:
        print("Error Measuring Soil Moisture Level")
        return -1

#function to check air temperature
def airtemperature():
    try:
        ##read temperature in Celsius
        temp = ss.get_temp()
        #converting to Fahrenheit
        airtemp = (temp * (9/5)) + 32
        return airtemp
    
    except:
        print("Error Measuring Air Temperature")
        return -1