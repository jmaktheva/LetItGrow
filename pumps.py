import board
import digitalio
import time

#DO NOT DEINIT. If the pumps turned on randomly (default values for chip?), that would be bad
waterGate = digitalio.DigitalInOut(board.IO35)
waterGate.direction = digitalio.Direction.OUTPUT
waterGate.value = False
nutGate = digitalio.DigitalInOut(board.IO36)
nutGate.direction = digitalio.Direction.OUTPUT
nutGate.value = False

def pump_water(seconds):
    waterGate.value = True #turn pump on
    time.sleep(seconds)
    waterGate.value = False #turn pump off

def pump_nutrients(seconds):
    nutGate.value = True #turn pump on
    time.sleep(seconds)
    nutGate.value = False #turn pump off
