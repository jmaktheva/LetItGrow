''
plant_height = 4
if water<20:
    spid.draw_circle(15, 145, 8, 0xFF0000)
    spid.draw_text('Tank water too low!', 2, 35, 145, 0xFF0000)
if NPK != 'okay':
    spid.draw_circle(15, 165, 8, 0xFF0000)
    spid.draw_text('NPK out of spec!', 2, 35, 165, 0xFF0000)
if ssTemp>86 or ssTemp<59:
    spid.draw_circle(15, 185, 8, 0xFF0000)
    spid.draw_text('Ambient temp too high!', 2, 35, 185, 0xFF0000)
if plant_height<3:
    spid.draw_circle(15, 205, 8, 0xFF0000)
    spid.draw_text('Raise lights!', 2, 35, 205, 0xFF0000)
if soilMoist<20:
    spid.draw_circle(15, 225, 8, 0xFF0000)
    spid.draw_text('Plant may need watered!', 2, 35, 225, 0xFF0000)
'''


import gc
import time
import board
import digitalio
import server as sv
import SPI_display as spid
import i2cSensors as i2cs
import pumps
import lights as lts
import ultrasonic as us
import npk

lts.power_on()

labelColor = 0xFF0000
valueColor = 0xFF0000

spid.draw_background(0x00FF00)
spid.draw_text('Let It Grow', 3, 30, 20, 0xD80621)

waterLevel = 0
spid.draw_text('Tank level:', 2, 35, 60, labelColor)
index_water = spid.draw_text('{}%'.format(waterLevel), 2, 179, 60, valueColor)

NPK = 0
spid.draw_text('NPK:', 2, 35, 80, labelColor)
index_npk = spid.draw_text('{}%'.format(NPK), 2, 95, 80, valueColor)

ssTemp = 0
spid.draw_text('Temp:', 2, 35, 100, labelColor)
index_temp = spid.draw_text('{} F'.format(ssTemp), 2, 110, 100, valueColor)

soilMoist = 0
spid.draw_text('Soil moisture:', 2, 35, 120, labelColor)
index_soilMoist = spid.draw_text('{}%'.format(soilMoist), 2, 215, 120, valueColor)

ambLight = 0
spid.draw_text('Ambient light:', 2, 35, 140, labelColor)
index_ambLight = spid.draw_text('{}%'.format(ambLight), 2, 215, 140, valueColor)


ip = '172.20.10.6'
ssid = 'TheBeast'
password = 'lolsquare'
sv.InitializeWifi(ssid, password)
#socket = sv.InitializeClientSocket(ip)
#print(gc.mem_free)
#before loop, ask server for values of variables

variable_dict = {'led_switch': 0, 'led_color': 0, 'led_brightness': 0, 'water_tank': 0,
                 'sensor_moisture': 0, 'sensor_temperature': 0, 'sensor_airquality': 0,
                 'sensor_light': 0, 'change': 0, 'led_schedule': 0, 'water_schedule': 0, 'moisture_upper': 1000000,
                 'moisture_lower': -1000000, 'temperature_upper': 1000000, 'temperature_lower': -1000000, 'npk_upper': 1000000,
                 'npk_lower': -1000000, 'airquality_upper': 1000000,
                 'airquality_lower': -1000000, 'light_upper': 1000000, 'light_lower': -1000000, 'water_switch': 0, 'water_input': 0}
#water input: how much water to water
#water switch: pump or no
postVarList1 = ['water_tank', 'sensor_moisture', 'sensor_temperature', 'sensor_npk', 'sensor_airquality', 'sensor_light']

postVarList2 = ['led_switch', 'led_color', 'led_brightness', 'change']

getVarList1 = ['led_switch', 'led_color', 'led_brightness', 'led_schedule', 'water_schedule', 'water_switch', 'water_input']

getVarList2 = ['moisture_upper', 'moisture_lower', 'temperature_upper', 'temperature_lower',
               'airquality_upper', 'airquality_lower', 'light_upper', 'light_lower']

#print(gc.mem_free)
print(variable_dict)

#put and ask for change variable. if change==1, get certain new data because things have changed
#get initially, but in loop, only get certain things if they've updated
#after getting changed data, POST change=0
'''
for variable in variable_dict.keys():
    variable_dict[variable] = sv.getData(ip, variable)
    time.sleep(.4) #.4 is the limit
'''
#old_variable_dict = copy.deepcopy(variable_dict)
old_led_switch = 0
old_led_color = 0
old_led_brightness = 0

#after watering, set water switch/pump switch to 0
#send updated data every 3 or 5 seconds

#print(variable_dict)

eco2, tvoc = 0, 0
lightHeight = False

pump_through_tube = .5

notifStartTime = 0
firstNotif = 0
notifInterval = 300
notifsCount = 0
notifsMax = 5
#notifs clear button
#notifs count reset

while True:
    #GET SENSOR VALUES
    soilMoist = int(i2cs.get_moisture())
    ssTemp = int(i2cs.get_temp())
    NPK = npk.get_npk()
    waterLevel = int(us.get_water_level()) #int
    lightHeight = int(us.get_plant_height()) #bool: True = bad, False = okay (probably)
    eco2, tvoc = i2cs.get_eco2_tvoc() #can take 4 seconds
    ambLight = int(i2cs.get_light())
    print('GATHERED SENSOR DATA')

    #update globalDict
    variable_dict['sensor_moisture'] = soilMoist
    variable_dict['sensor_temperature'] = ssTemp
    variable_dict['sensor_npk'] = NPK
    variable_dict['water_tank'] = waterLevel
    variable_dict['sensor_light'] = ambLight
    variable_dict['sensor_airquality'] = eco2

    #SEND SENSOR DATA TO SERVER
    for key in postVarList1:
        sv.postData(ip, key, variable_dict[key])
        time.sleep(.4) #.4 is the lower bound

    #GET VALUES FROM SERVER (if anything has changed)
    if sv.getData(ip, 'change'):
        variable_dict['change'] = 1
        for key in getVarList1:
            variable_dict[key] = sv.getData(ip, key)
            time.sleep(.4) #.4 is the limit

    #LIGHT/WATER ACTIONS - Server
    print('water switch')
    print(variable_dict['water_switch'])
    if variable_dict['change'] == 1:
        if variable_dict['led_switch'] != old_led_switch:
            lts.on_off_toggle()
            old_led_switch = variable_dict['led_switch']
        if variable_dict['led_color'] != old_led_color:
            lts.color_change(variable_dict['led_color'])
            old_led_color = variable_dict['led_color']
        if variable_dict['led_brightness'] != old_led_brightness:
            lts.brtness_change(variable_dict['led_brightness'])
            old_led_brightness = variable_dict['led_brightness']
        if variable_dict['water_switch'] == 1:
            print('water_input')
            print(variable_dict['water_input'])
            pumps.pump_water(pump_through_tube + float(variable_dict['water_input'] / 30))
            variable_dict['water_switch'] = 0
            variable_dict['water_input'] = 0
        #get rest of server data
        for key in getVarList2:
            variable_dict[key] = sv.getData(ip, key)
            time.sleep(.4) #.4 is the limit
        #CHANGE HAS BEEN TAKEN CARE OF
        variable_dict['change'] = 0
        sv.postData(ip, 'change', 0)

    #LIGHT/WATER ACTIONS - Touchscreen (later)
    '''
    #don't do list, do individual to cut down time
    for key in postVarList2:
        sv.postData(ip, key, variable_dict[key])
        time.sleep(.4) #.4 is the lower bound
    '''

    #SEND PLANT CONDITION NOTIFICATIONS
    temp1 = soilMoist > variable_dict['moisture_upper']
    temp2 = soilMoist < variable_dict['moisture_lower']
    temp3 = ssTemp > variable_dict['temperature_upper']
    temp4 = ssTemp < variable_dict['temperature_lower']
    temp5 = NPK > variable_dict['npk_upper']
    temp6 = NPK < variable_dict['npk_lower']
    temp7 = eco2 > variable_dict['airquality_upper']
    temp8 = eco2 < variable_dict['airquality_lower']
    temp9 = ambLight > variable_dict['light_upper']
    temp10 = ambLight < variable_dict['light_lower']

    #if (soilMoist > variable_dict['moisture_upper']) or (soilMoist < variable_dict['moisture_lower']) or (ssTemp > variable_dict['temperature_upper']) or (ssTemp < variable_dict['temperature_lower']) or (NPK > variable_dict['ssTemp_upper']) or (NPK < variable_dict['ssTemp_lower']) or (eco2 > variable_dict['airquality_upper']) or (eco2 < variable_dict['airquality_lower']) or (ambLight > variable_dict['light_upper']) or (ambLight < variable_dict['light_lower']) or (lightHeight == True):
    if temp1 or temp2 or temp3 or temp4 or temp5 or temp6 or temp7 or temp8 or temp9 or temp10 or lightHeight:
        if (notifsCount < notifsMax):
            if (firstNotif == 0):
                notifStartTime = time.time()
                firstNotif = 1
                notifsCount += 1
                print('sent notif')
                #sv.sendNotification()
            elif ((time.time() - notifStartTime) > notifInterval):
                print('sent notif')
                #sv.sendNotification()
                notifsCount += 1

    #update display
    spid.overwrite_text('{}%'.format(waterLevel), index_water)
    spid.overwrite_text('{}%'.format(NPK), index_npk)
    spid.overwrite_text('{} F'.format(ssTemp), index_temp)
    spid.overwrite_text('{}%'.format(soilMoist), index_soilMoist)
    spid.overwrite_text('{}%'.format(ambLight), index_ambLight)
    #eco2
    #tvoc (probably 0 tho)

    print('LOOPED')
    time.sleep(5) #delete later

'''
#Global Variables
led_switch = 0
led_color = 0 # 0 = White 1 = Purple
led_brightness = 0
led_schedule = 0
water_switch = 0
water_input = 0
water_tank = 0
water_schedule = 0
sensor_moisture = 0
sensor_temperature = 0
sensor_ssTemp = 0
sensor_airquality = 0
sensor_light = 0
 #Settings Values (Notifications)
moisture_upper = 0
moisture_lower = 0
temperature_upper = 0
temperature_lower = 0
ssTemp_upper = 0
ssTemp_lower = 0
airquality_upper = 0
airquality_lower = 0
light_upper = 0
light_lower = 0
'''

'''
while True:
    #connect to web server
    #call functions to pass and get values
    #send post request when sensors update
    #look into interrupts but prob not
    pass
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
while True:
    touch_coords = spid.touch_input()
    if touch_coords != None:
        if ((touch_coords['x'] >= 200) and (touch_coords['y'] <= 80)):
            print('start the watering sequence')
    time.sleep(1)
'''