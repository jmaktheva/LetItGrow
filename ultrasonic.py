import time
import board
from adafruit_hcsr04 import HCSR04

# Initialize the ultrasonic sensor for plants
water = HCSR04(trigger_pin=board.IO11, echo_pin=board.IO12)
plant = HCSR04(trigger_pin=board.IO13, echo_pin=board.IO14)

heightOfTank = 9 #update

def get_plant_height():
    for attempt in range(5):
        try:
            return True if (plant.distance/2.54) < 3 else False #return boolean for if plant is within 3 inches of grow lights
        except RuntimeError:
            time.sleep(1)
            if attempt==4:
                return False

def get_water_level():
    for attempt in range(5):
        try:
            return heightOfTank - water.distance/2.54 #return water level in inches (greater distance = less water)
        except RuntimeError:
            time.sleep(1)
            if attempt==4:
                return 0 #fix        