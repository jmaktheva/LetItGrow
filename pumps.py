import board
import digitalio
import time

#DO NOT DEINIT. If the pumps turned on randomly (default values for chip?), that would be bad
gate = digitalio.DigitalInOut(board.IO35)
gate.direction = digitalio.Direction.OUTPUT
gate.value = False

def pump_water(seconds):
    print('pumping water for '+str(seconds)+' seconds')
    gate.value = True #turn pump on
    print('on')
    time.sleep(seconds)
    gate.value = False #turn pump off
    print('off')

