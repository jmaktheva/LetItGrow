#code not for demo:

#spid.draw_text('Harsh, Jackson,', 2, 70, 70, 0xD80621)
#spid.draw_text('Logan, Marcus,', 2, 70, 90, 0xD80621)
#spid.draw_image('/water_resized.png', 40, 180)
#spid.draw_image('/light_resized.png', 120, 180)
#spid.draw_image('/health_resized.png', 200, 180)

#water = 25
#spid.overwrite_text(str(water), 2, 179, 60, 0xFF0000, index_water)
#nitro, phos, potass = 6, 2, 2
#spid.overwrite_text(str(nitro)+':'+str(phos)+':'+str(potass), 2, 95, 80, 0xFF0000, index_npk)
#ss_temp = 76
#spid.overwrite_text(str(ss_temp), 2, 110, 100, 0xFF0000, index_temp)
#soil_moist = 25
#spid.overwrite_text(str(soil_moist), 2, 215, 120, 0xFF0000, index_soil_moist)
'''
lts.cycle_power()
print('cycle power')
time.sleep(3)

lts.cycle_power()
print('cycle power')
time.sleep(3)

lts.cycle_color()
print('cycle color')
time.sleep(3)

lts.cycle_color()
print('cycle color')
time.sleep(3)

lts.cycle_color()
print('cycle color')
time.sleep(3)

lts.cycle_brightness()
print('cycle brightness 1')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 2')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 3')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 4')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 5')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 6')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 7')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 8')
time.sleep(3)
lts.cycle_brightness()
print('cycle brightness 9')
time.sleep(3)
'''



import SPI_display as spid
import time
import board
import digitalio
import lights as lts
#import soil_sensor as ss
#import server as sv
#import Ultrasonic as us

'''
gate = digitalio.DigitalInOut(board.IO8)
gate.direction = digitalio.Direction.OUTPUT
gate.value = False
'''
'''
water_flow = 0

while water_flow<5:
    gate.value = True
    time.sleep(3)
    gate.value=False
    time.sleep(1.5)
    water_flow += 1

'''
spid.draw_background(0x00FF00)
spid.draw_text('Let It Grow', 3, 30, 20, 0xD80621)

water = 69
spid.draw_text('Tank level:   ' + '%', 2, 35, 60, 0xFF0000)
index_water = spid.draw_text(str(water), 2, 179, 60, 0xFF0000)

nitro, phos, potass = 4, 2, 1
spid.draw_text('NPK: ', 2, 35, 80, 0xFF0000)
index_npk = spid.draw_text(str(nitro)+':'+str(phos)+':'+str(potass), 2, 95, 80, 0xFF0000)

ss_temp = 74
spid.draw_text('Temp:   ' + ' ' + 'F', 2, 35, 100, 0xFF0000)
index_temp = spid.draw_text(str(ss_temp), 2, 110, 100, 0xFF0000)

soil_moist = 42
spid.draw_text('Soil moisture:   '+'%', 2, 35, 120, 0xFF0000)
index_soil_moist = spid.draw_text(str(soil_moist), 2, 215, 120, 0xFF0000)

plant_height = 4

if water<20:
    spid.draw_circle(15, 145, 8, 0xFF0000)
    spid.draw_text('Tank water too low!', 2, 35, 145, 0xFF0000)
if nitro<3.2 or nitro>4.8 or phos<1.6 or phos>2.4 or potass<0.8 or potass>1.2:
    spid.draw_circle(15, 165, 8, 0xFF0000)
    spid.draw_text('NPK out of spec!', 2, 35, 165, 0xFF0000)
if ss_temp>86 or ss_temp<59:
    spid.draw_circle(15, 185, 8, 0xFF0000)
    spid.draw_text('Ambient temp too high!', 2, 35, 185, 0xFF0000)
if plant_height<3:
    spid.draw_circle(15, 205, 8, 0xFF0000)
    spid.draw_text('Raise lights!', 2, 35, 205, 0xFF0000)
if soil_moist<20:
    spid.draw_circle(15, 225, 8, 0xFF0000)
    spid.draw_text('Plant may need watered!', 2, 35, 225, 0xFF0000)


#18 13
import busio
import binascii
uart = busio.UART(tx=board.IO18, rx=board.IO13, baudrate=9600, timeout=3)
testList = [0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xB5, 0xCC]
bigB = bytearray(testList)
print(type(bigB))
print(bigB)
while True:
    sentBytes = uart.write(bigB)
    print('bytes sent: '+str(sentBytes))
    print('################')
    data = uart.read()
    if data is not None:
        print(bytearray(data))
    else:
        print('No data received')
    time.sleep(1)


'''
ip = sv.InitializeWifi('TheBeast', 'lolsquare')
socket = sv.InitializeSocket(ip)

light_pwr_state = 0
light_clr_state = 0 #both


while True:
    moisture = ss.get_moisture()
    ss_temp = int(ss.get_temp())
    #water_level = int(us.get_water_level())
    #print('water: '+str(water_level))
    print(str(moisture))
    print(str(ss_temp))
    sv.Gsensor_moisture = moisture
    sv.Gsensor_temperature = ss_temp
    if moisture > 400:
        sv.sendNotification()
    sv.Gsensor_temperature = ss_temp
    print(sv.Gsensor_temperature)
    sv.webserver(socket)
    print('Gled_switch: '+str(sv.Gled_switch))
    print('Gled_color: '+str(sv.Gled_color))
    if sv.Gled_switch == 1 and light_pwr_state == 0:
        lts.cycle_power()
        light_pwr_state = 1
    if sv.Gled_switch == 0 and light_pwr_state == 1:
        lts.cycle_power()
        light_pwr_state = 0
    if light_pwr_state == 1:
        if sv.Gled_color == 0: #white
            if light_clr_state == 2: #my purple
                lts.cycle_color()
                lts.cycle_color()
                light_clr_state = 1 #my white
            elif light_clr_state == 0: #my both
                lts.cycle_color()
                light_clr_state = 1 #my white

        if sv.Gled_color == 1: #purple
            if light_clr_state == 0:
                lts.cycle_color()
                lts.cycle_color()
                light_clr_state = 2
            elif light_clr_state == 1:
                lts.cycle_color()
                light_clr_state = 2
    print(str(light_clr_state))

    pass
'''
'''
while True:
    #connect to web server
    #call functions to pass and get values
    #send post request when sensors update
    #look into interrupts but prob not
    pass
'''

#moisture = ss.get_moisture()
#temp = ss.get_temp()
#print(str(moisture)+', '+str(temp))


#import Ultrasonic as us
#plant_height = us.get_plant_height()
#water_level = us.get_water_level()
#print(plant_height)
#print(water_level)


#print(spid.touch_input())
#time.sleep(1)

#spid.draw_button(240, 210, 80, 30, 'Water Plant')
#spid.draw_button(240, 0, 80, 30, 'Light Power')
#spid.draw_button(240, 30, 80, 30, 'Color Adj')
#spid.draw_button(240, 60, 80, 30, 'Brtness Adj')

#import alarm

#pin_alarm = alarm.pin.PinAlarm(pin=board.IO6, value=False)
#alarm.light_sleep_until_alarms(pin_alarm)
#print('got here')

#NOTE: IRQ as input raises an error when double pressing screen. Not sure why. So no interrupts for now

'''
while True:
    touch_coords = spid.touch_input()
    if touch_coords != None:
        if ((touch_coords['x'] >= 200) and (touch_coords['y'] <= 80)):
            print('start the watering sequence')
    time.sleep(1)
'''




'''
while True:
    gate.value = True #on True cycle, switches on or off
    time.sleep(1) #should be set much shorter, but really doesn't matter. BJT can handle it
    gate.value = False
    time.sleep(1)
    pass


'''
