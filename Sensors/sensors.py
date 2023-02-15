import time
import board #low level control for ESP32 hardware
from adafruit_hcsr04 import HCSR04 #importing code for the Ultrasonic Sensor

# Initialize the ultrasonic sensor
# Trigger is initialised to pin 4 and Echo is initialised to pin 5
sonar = HCSR04(board.IO4, board.IO5)

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
        return distance