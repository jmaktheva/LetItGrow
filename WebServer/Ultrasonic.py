import time
import machine #low level control for ESP32
import pulseio

#Setting up Trigger
trigger = machine.Pin(4, machine.Pin.OUT)
trigger_pin = pulseio.PulseOut(trigger)

#Setting up Echo Pin
echo = machine.Pin(5, machine.Pin.IN)
echo_pin = pulseio.PulseIn(echo, maxlen = 500, idle_state = True)

def distance_mm():
    # Trigger the sensor by sending a 10us pulse
    trigger_pin.send(bytearray([1, 0] * 50))
    # Wait for the echo pin to go high
    while echo.value() == 0:
        pass
    # Start the timer
    start = time.monotonic()
    # Wait for the echo pin to go low
    while echo.value() == 1:
        pass
    # Stop the timer
    stop = time.monotonic()
    # Calculate the duration of the echo
    duration = stop - start
    # Calculate the distance to the object (in mm)
    distance = duration * 343 / 2
    return distance

while True:
    # Measure the distance to the object (in mm)
    distance = distance_mm()
    # Convert the distance to inches
    distance_inches = distance / 25.4
    #Printing Distance to check
    print("Distance in Inches: " + distance_inches)
    # Check if the distance is less than 3 inches
    if distance_inches < 3:
        print("Object detected within 3 inches!")
    else:
        print("No object detected within 3 inches.")
    # Wait before making another measurement
    time.sleep(1)
