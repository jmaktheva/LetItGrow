import board
import digitalio
import time

#DO NOT DEINIT. Find way to save state after reset (or just determine from lux sensor)
power = digitalio.DigitalInOut(board.IO36)
power.direction = digitalio.Direction.OUTPUT
power.value = False
onOff = digitalio.DigitalInOut(board.IO38)
onOff.direction = digitalio.Direction.OUTPUT
onOff.value = False
clr = digitalio.DigitalInOut(board.IO47)
clr.direction = digitalio.Direction.OUTPUT
clr.value = False
brtness = digitalio.DigitalInOut(board.IO21)
brtness.direction = digitalio.Direction.OUTPUT
brtness.value = False

delay = .1 #.1 is limit
oldColor = 0
oldBrightness = 0

def power_on():
    power.value = True
    time.sleep(delay)
    return

def power_off():
    power.value = False
    time.sleep(delay)
    return

def power_cycle():
    power_off()
    power_on()
    return

def gate_toggle(gate):
    gate.value = True
    time.sleep(delay)
    gate.value = False
    time.sleep(delay)
    return

def turn_off():
    onOff.value = False
    time.sleep(delay)
    return

def turn_on():
    onOff.value = True
    time.sleep(.5)
    onOff.value = False
    return

def on_off_toggle():
    gate_toggle(onOff)
    return

def color_change(color):
    oldColor = color
    power_cycle()
    turn_on()
    print(color)
    if color == 1: #white
        gate_toggle(clr)
    elif color == 2: #purple
        gate_toggle(clr)
        gate_toggle(clr)
    if oldBrightness == 80:
        gate_toggle(brtness)
    elif oldBrightness == 60:
        gate_toggle(brtness)
        gate_toggle(brtness)
    elif oldBrightness == 40:
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
    elif oldBrightness == 20:
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
    return

def brtness_change(level):
    oldBrightness = level
    #level = desired level: 25 (20%), 50 (60%), 75 (80%), 100
    power_cycle()
    on_off_toggle() #turn lights on
    if level == 75:
        gate_toggle(brtness)
    elif level == 50:
        gate_toggle(brtness)
        gate_toggle(brtness)
    elif level == 25:
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
    if oldColor == 1:
        gate_toggle(clr)
    elif oldColor == 2:
        gate_toggle(clr)
        gate_toggle(clr)
    return
