import time
import board
import pulseio

flow_sensor_pin = board.IO4

flow_sensor = pulseio.PulseIn(flow_sensor_pin, 1)
total_water_passed = 0.0

while True:
    current_pulse_count = len(flow_sensor)
    current_water_passed = current_pulse_count * 2.25  # Amount of water passed in mL, assuming 2.25 mL per pulse
    total_water_passed += current_water_passed # / 1000.0  # Add to total water passed in L
    print("Total water passed: {:.3f} L".format(total_water_passed))
    flow_sensor.clear()
    time.sleep(1.0)