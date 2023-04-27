#import gc
import time
import board
import digitalio
import asyncio
import server as sv
import SPI_display as spid
import i2cSensors as i2cs
import pumps
import lights as lts
import ultrasonic as us
import npk


class Touch():
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

async def touch_input(touch):
    #TOUCHSCREEN SETUP
    i2c = busio.I2C(sda=board.IO6, scl=board.IO7)
    #ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)
    irq = digitalio.DigitalInOut(board.IO15)
    irq.direction = digitalio.Direction.INPUT
    ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False, irq_pin=irq)
    
    while True:
        point = ft.touches #list(dict) (True) if touched, empty list (False) otherwise
        if point != []:
            print(point)
            touch.y = point[0]['x']
            touch.x = 320 - point[0]['y']
        await asyncio.sleep(0) #let another task run

async def da_loop(touch):
    #VARIABLES SETUP
    server = False #False=display only, True=server+display
 
    #SEND POWER TO LIGHTS TO AVOID LED FLICKERING
    lts.power_on()

    #DRAW MAIN SCREEN
    index_water, index_temp, index_soilMoist, index_ambLight, index_eco2, water_x, water_y, water_width, water_height, light_x, light_y, light_width, light_height = spid.draw_screen0()

    ip = '172.20.10.6'
    ssid = 'TheBeast'
    password = 'lolsquare'

    if server:
        sv.InitializeWifi(ssid, password)
        socket = sv.InitializeClientSocket(ip)

    #print(gc.mem_free)

    variable_dict = {'led_switch': 0, 'led_color': 0, 'led_brightness': 0, 'water_tank': 0, 'sensor_moisture': 0,
                     'sensor_temperature': 0, 'sensor_airquality': 0, 'sensor_light': 0, 'change': 0,
                     'moisture_upper': 1000000, 'moisture_lower': -1000000, 'temperature_upper': 1000000,
                     'temperature_lower': -1000000, 'airquality_upper': 1000000, 'airquality_lower': -1000000,
                     'light_upper': 1000000, 'light_lower': -1000000, 'water_switch': 0, 'water_input': 0}

    #GET INITIAL VALUES
    print('GETTING INITIAL VALUES')
    '''
    for variable in variable_dict.keys():
        variable_dict[variable] = sv.getData(ip, variable)
        time.sleep(.4) #.4 is the limit
    '''
    variable_dict['change'] = 1

    postVarList1 = ['water_tank', 'sensor_moisture', 'sensor_temperature', 'sensor_airquality', 'sensor_light']

    postVarList2 = ['led_switch', 'led_color', 'led_brightness', 'change']

    getVarList1 = ['led_switch', 'led_color', 'led_brightness', 'water_switch', 'water_input']

    getVarList2 = ['moisture_upper', 'moisture_lower', 'temperature_upper', 'temperature_lower',
                   'airquality_upper', 'airquality_lower', 'light_upper', 'light_lower']

    #print(gc.mem_free)
    print(variable_dict)

    old_led_switch = 0
    old_led_color = 0
    old_led_brightness = 0

    tvoc = 0
    lightHeight = False

    pump_through_tube = .5

    notifStartTime = 0
    firstNotif = 0
    notifInterval = 300
    notifsCount = 0
    notifsMax = 5
    #notifs clear button
    #notifs count reset
    countLoop = False

    screen = 0 #0 = main screen; 1 = light on/off, color, brightness; 2 = mix/white/purple; 3 = 25/50/75/100%; 4 = water plant + amount buttons; 5 = warning indicators
    oldScreen = 0
    waterAmountSet = 0

    back_x = 0
    back_y = 210
    back_width = 40
    back_height = 30
    back_xbound = back_x+back_width
    back_ybound = back_y+back_height
    
    
    #DA ACTUAL LOOP
    while True:
        #GET SENSOR VALUES
        soilMoist = int(i2cs.get_moisture())
        ssTemp = int(i2cs.get_temp())
        #NPK = npk.get_npk()
        waterLevel = int(us.get_water_level()) #int
        lightHeight = int(us.get_plant_height()) #bool: True = bad, False = okay (probably)
        eco2, tvoc = i2cs.get_eco2_tvoc() #can take 4 seconds
        ambLight = int(i2cs.get_light())
        print('GATHERED SENSOR DATA')

        if (screen == 0):
            if (oldScreen != 0):
                #DRAW SCREEN
                index_water, index_temp, index_soilMoist, index_ambLight, index_eco2, water_x, water_y, water_width, water_height, light_x, light_y, light_width, light_height = spid.draw_screen0()

                #DRAW ERROR INDICATOR
                temp1 = soilMoist > variable_dict['moisture_upper']
                temp2 = soilMoist < variable_dict['moisture_lower']
                temp3 = ssTemp > variable_dict['temperature_upper']
                temp4 = ssTemp < variable_dict['temperature_lower']
                #temp5 = NPK > variable_dict['npk_upper']
                #temp6 = NPK < variable_dict['npk_lower']
                temp7 = eco2 > variable_dict['airquality_upper']
                temp8 = eco2 < variable_dict['airquality_lower']
                temp9 = ambLight > variable_dict['light_upper']
                temp10 = ambLight < variable_dict['light_lower']
                if temp1 or temp2 or temp3 or temp4 or temp7 or temp8 or temp9 or temp10 or lightHeight:
                    spid.draw_circle(300, 20, 8, 0xFF0000, 0)

            oldScreen = 0

            #CHECK TOUCHSCREEN
            if (touch.x >= water_x) and (touch.x <= (water_x+water_width)) and (touch.y >= water_y) and (touch.y <= (water_y+water_height)):
                print('water button touched')
                screen = 4
            elif (touch.x >= light_x) and (touch.x <= (light_x+light_width)) and (touch.y >= light_y) and (touch.y <= (light_y+light_height)):
                print('light button touched')
                screen = 1

        elif screen == 1:
            if oldScreen != 1:
                #DRAW SCREEN
                light_on_off_x, light_on_off_y, light_on_off_width, light_on_off_height, light_color_x, light_color_y, light_color_width, light_color_height, light_brightness_x, light_brightness_y, light_brightness_width, light_brightness_height = spid.draw_screen1()
            
            oldScreen = 1
            
            #CHECK TOUCHSCREEN
            if (touch.x >= light_on_off_x) and (touch.x <= (light_on_off_x+light_on_off_width)) and (touch.y >= light_on_off_y) and (touch.y <= (light_on_off_y+light_on_off_height)):
                print('On/Off button touched - toggle on/off')
                variable_dict['led_switch'] = 1
                variable_dict['change'] = 1
            elif (touch.x >= light_color_x) and (touch.x <= (light_color_x+light_color_width)) and (touch.y >= light_color_y) and (touch.y <= (light_color_y+light_color_height)):
                print('Color button touched')
                screen = 2
            elif (touch.x >= light_brightness_x) and (touch.x <= (light_brightness_x+light_brightness_width)) and (touch.y >= light_brightness_y) and (touch.y <= (light_brightness_y+light_brightness_height)):
                print('Brightness button touched')
                screen = 3
            elif (touch.x >= back_x) and (touch.x <= (back_xbound)) and (touch.y >= back_y) and (touch.y <= (back_ybound)):
                screen = 0

        elif screen == 2:
            if oldScreen != 2:
                #DRAW SCREEN
                mix_x, mix_y, mix_width, mix_height, white_x, white_y, white_width, white_height, purple_x, purple_y, purple_width, purple_height = spid.draw_screen2()

            oldScreen = 2

            #CHECK TOUCHSCREEN
            if (touch.x >= mix_x) and (touch.x <= (mix_x+mix_width)) and (touch.y >= mix_y) and (touch.y <= (mix_y+mix_height)):
                print('Mix button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_color'] = 0
                variable_dict['change'] = 1
            elif (touch.x >= white_x) and (touch.x <= (white_x+white_width)) and (touch.y >= white_y) and (touch.y <= (white_y+white_height)):
                print('White button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_color'] = 1
                variable_dict['change'] = 1
            elif (touch.x >= purple_x) and (touch.x <= (purple_x+purple_width)) and (touch.y >= purple_y) and (touch.y <= (purple_y+purple_height)):
                print('Purple button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_color'] = 2
                variable_dict['change'] = 1
            elif (touch.x >= back_x) and (touch.x <= (back_xbound)) and (touch.y >= back_y) and (touch.y <= (back_ybound)):
                screen = 1

        elif screen == 3:
            if oldScreen != 3:
                #DRAW SCREEN
                x_25, y_25, width_25, height_25, x_50, y_50, width_50, height_50, x_75, y_75, width_75, height_75, x_100, y_100, width_100, height_100 = spid.draw_screen3()

            oldScreen = 3

            #CHECK TOUCHSCREEN
            if (touch.x >= x_25) and (touch.x <= (x_25+width_25)) and (touch.y >= y_25) and (touch.y <= (y_25+height_25)):
                print('25% button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_brightness'] = 25
                variable_dict['change'] = 1
            elif (touch.x >= x_50) and (touch.x <= (x_50+width_50)) and (touch.y >= y_50) and (touch.y <= (y_50+height_50)):
                print('50% button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_brightness'] = 50
                variable_dict['change'] = 1
            elif (touch.x >= x_75) and (touch.x <= (x_75+width_75)) and (touch.y >= y_75) and (touch.y <= (y_75+height_75)):
                print('75% button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_brightness'] = 75
                variable_dict['change'] = 1
            elif (touch.x >= x_100) and (touch.x <= (x_100+width_100)) and (touch.y >= y_100) and (touch.y <= (y_100+height_100)):
                print('100% button touched')
                variable_dict['led_switch'] = 1
                variable_dict['led_brightness'] = 100
                variable_dict['change'] = 1
            elif (touch.x >= back_x) and (touch.x <= (back_xbound)) and (touch.y >= back_y) and (touch.y <= (back_ybound)):
                screen = 1

        elif screen == 4:
            if oldScreen != 4:
                #DRAW WATER BUTTONS
                x_25mL, y_25mL, width_25mL, height_25mL, x_50mL, y_50mL, width_50mL, height_50mL, x_75mL, y_75mL, width_75mL, height_75mL, x_100mL, y_100mL, width_100mL, height_100mL, water_plant_x, water_plant_y, water_plant_width, water_plant_height = spid.draw_screen4()

            oldScreen = 4

            #CHECK TOUCHSCREEN
            if (touch.x >= x_25mL) and (touch.x <= (x_25mL+width_25mL)) and (touch.y >= y_25mL) and (touch.y <= (y_25mL+height_25mL)):
                print('25mL button touched')
                waterAmountSet = 25
            elif (touch.x >= x_50mL) and (touch.x <= (x_50mL+width_50mL)) and (touch.y >= y_50mL) and (touch.y <= (y_50mL+height_50mL)):
                print('50mL button touched')
                waterAmountSet = 50
            elif (touch.x >= x_75mL) and (touch.x <= (x_75mL+width_75mL)) and (touch.y >= y_75mL) and (touch.y <= (y_75mL+height_75mL)):
                print('75mL button touched')
                waterAmountSet = 75
            elif (touch.x >= x_100mL) and (touch.x <= (x_100mL+width_100mL)) and (touch.y >= y_100mL) and (touch.y <= (y_100mL+height_100mL)):
                print('100mL button touched')
                waterAmountSet = 100
            elif (touch.x >= water_plant_x) and (touch.x <= (water_plant_x+water_plant_width)) and (touch.y >= water_plant_y) and (touch.y <= (water_plant_y+water_plant_height)) and waterAmountSet:
                print('Water Plant button touched')
                variable_dict['water_input'] = waterAmountSet
                variable_dict['water_switch'] = 1
                variable_dict['change'] = 1
                waterAmountSet = 0
            elif (touch.x >= back_x) and (touch.x <= (back_xbound)) and (touch.y >= back_y) and (touch.y <= (back_ybound)):
                screen = 0

        elif screen == 5:
            if oldScreen != 5:
                #DRAW ERROR CIRCLES AND LABELS
                spid.draw_screen5(lightHeight, water, ssTemp, soilMoist)

            oldScreen = 5

            #CHECK TOUCHSCREEN
            if (touch.x >= back_x) and (touch.x <= (back_xbound)) and (touch.y >= back_y) and (touch.y <= (back_ybound)):
                screen = 0

        #update globalDict
        variable_dict['sensor_moisture'] = soilMoist
        variable_dict['sensor_temperature'] = ssTemp
        #variable_dict['sensor_npk'] = NPK
        variable_dict['water_tank'] = waterLevel
        variable_dict['sensor_light'] = ambLight
        variable_dict['sensor_airquality'] = eco2

        if server:
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

        #LIGHT/WATER ACTIONS
        if variable_dict['change'] == 1:
            if variable_dict['led_switch'] != old_led_switch:
                lts.on_off_toggle()
                old_led_switch = variable_dict['led_switch']

            if (variable_dict['led_color'] != old_led_color) and (variable_dict['led_switch'] == 1):
                lts.color_change(variable_dict['led_color'])
                old_led_color = variable_dict['led_color']
            if (variable_dict['led_brightness'] != old_led_brightness) and (variable_dict['led_switch'] == 1):
                lts.brtness_change(variable_dict['led_brightness'])
                old_led_brightness = variable_dict['led_brightness']
            if variable_dict['water_switch'] == 1:
                pumps.pump_water(pump_through_tube + float(variable_dict['water_input'] / 30))
                variable_dict['water_switch'] = 0
                variable_dict['water_input'] = 0
            #get rest of server data
            if server:
                for key in getVarList2:
                    variable_dict[key] = sv.getData(ip, key)
                    time.sleep(.4) #.4 is the limit
                sv.postData(ip, 'change', 0)
            #CHANGE HAS BEEN TAKEN CARE OF
            variable_dict['change'] = 0

        #SEND PLANT CONDITION NOTIFICATIONS
        temp1 = soilMoist > variable_dict['moisture_upper']
        temp2 = soilMoist < variable_dict['moisture_lower']
        temp3 = ssTemp > variable_dict['temperature_upper']
        temp4 = ssTemp < variable_dict['temperature_lower']
        #temp5 = NPK > variable_dict['npk_upper']
        #temp6 = NPK < variable_dict['npk_lower']
        temp7 = eco2 > variable_dict['airquality_upper']
        temp8 = eco2 < variable_dict['airquality_lower']
        temp9 = ambLight > variable_dict['light_upper']
        temp10 = ambLight < variable_dict['light_lower']


        #if (soilMoist > variable_dict['moisture_upper']) or (soilMoist < variable_dict['moisture_lower']) or (ssTemp > variable_dict['temperature_upper']) or (ssTemp < variable_dict['temperature_lower']) or (NPK > variable_dict['ssTemp_upper']) or (NPK < variable_dict['ssTemp_lower']) or (eco2 > variable_dict['airquality_upper']) or (eco2 < variable_dict['airquality_lower']) or (ambLight > variable_dict['light_upper']) or (ambLight < variable_dict['light_lower']) or (lightHeight == True):
        if server:
            if temp1 or temp2 or temp3 or temp4 or temp7 or temp8 or temp9 or temp10 or lightHeight:
                if (notifsCount < notifsMax):
                    if (firstNotif == 0):
                        notifStartTime = time.time()
                        firstNotif = 1
                        notifsCount += 1
                        print('sent notif')
                        sv.sendNotification()
                    elif ((time.time() - notifStartTime) > notifInterval):
                        print('sent notif')
                        sv.sendNotification()
                        notifsCount += 1


        #update display
        spid.overwrite_text('{}%'.format(waterLevel), index_water)
        #spid.overwrite_text('{}%'.format(NPK), index_npk)
        spid.overwrite_text('{} F'.format(ssTemp), index_temp)
        spid.overwrite_text('{}%'.format(soilMoist), index_soilMoist)
        spid.overwrite_text('{}%'.format(ambLight), index_ambLight)
        spid.overwrite_text('{}'.format(eco2), index_eco2)

        print('LOOPED')
        await asyncio.sleep(0)

async def main():
    touch = Touch()
    touchscreenTask = asyncio.create_task(touch_input(touch))
    daLoopTask = asyncio.create_task(da_loop(touch))
    await asyncio.gather(daLoopTask, touchscreenTask)

asyncio.run(main(temp, water, index_water, color, NPK, index_npk, ss_temp, index_temp, soilMoist, index_soilMoist, ambLight, index_ambLight, ft))
