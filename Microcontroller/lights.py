import board
import digitalio
import time

#DO NOT DEINIT()

#setup power button gate pin
gate_power = digitalio.DigitalInOut(board.IO15)
gate_power.direction = digitalio.Direction.OUTPUT

#setup color button gate pin
gate_color = digitalio.DigitalInOut(board.IO16)
gate_color.direction = digitalio.Direction.OUTPUT

#setup brightness button gate pin
gate_brightness = digitalio.DigitalInOut(board.IO17)
gate_brightness.direction = digitalio.Direction.OUTPUT

def cycle_power():
    gate_power.value = True
    time.sleep(.5)
    gate_power.value = False

def cycle_color():
    gate_color.value = True
    time.sleep(.5)
    gate_color.value = False

def cycle_brightness():
    gate_brightness.value = True
    time.sleep(.5)
    gate_brightness.value = False