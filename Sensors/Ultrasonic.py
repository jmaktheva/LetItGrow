import time
import board
import pulseio
from adafruit_hcsr04 import HCSR04

# Initialize trigger and echo pins
#trigger = pulseio.PulseOut(board.IO4)
#echo = pulseio.PulseIn(board.IO5, maxlen=500)

# Initialize the ultrasonic sensor
sonar = HCSR04(board.IO4, board.IO5)

# Read the distance from the ultrasonic sensor
while True:
    try:
        # Measure the distance to the nearest object
        distance = sonar.distance/2.54
        if distance <= 3:
            print("Object detected within 3 inches!")
        else:
            print("No object detected within 3 inches.")
        time.sleep(0.5)
    except:
        print("Error")
        time.sleep(0.5)