import board
import digitalio
import time

#DO NOT DEINIT. Find way to save state after reset (or just determine from lux sensor)
power = digitalio.DigitalInOut(board.IO48)
power.direction = digitalio.Direction.OUTPUT
power.value = False
clr = digitalio.DigitalInOut(board.IO47)
clr.direction = digitalio.Direction.OUTPUT
clr.value = False
brtness = digitalio.DigitalInOut(board.IO21)
brtness.direction = digitalio.Direction.OUTPUT
brtness.value = False

clrState = 0 #0 = both, 1 = white, 2 = purple

def gate_toggle(gate):
    gate.value = True
    time.sleep(1)
    gate.value - False
    return

def power_toggle():
    gate_toggle(power)
    return

def color_change(color):
    if color == 1: #want white
        if clrState == 0:
            gate_toggle(clr)
        elif clrState == 2:
            gate_toggle(clr)
            gate_toggle(clr)
    elif color == 2: #want purple
        if clrState == 0:
            gate_toggle(clr)
            gate_toggle(clr)
        elif clrState = 1:
            gate_toggle(clr)
    elif color == 0:
        if clrState == 1:
            gate_toggle(clr)
            gate_toggle(clr)
        elif clrState == 2:
            gate_toggle(clr)
    elif color == purple:
        gate_toggle(clr)
        gate_toggle(clr)
    return

def brtness_change(level):
    #level = 20, 40, 60, 80
    if level == 80:
        gate_toggle(brtness)
    elif level == 60:
        gate_toggle(brtness)
        gate_toggle(brtness)
    elif level == 40:
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
    elif level == 20:
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
        gate_toggle(brtness)
    return