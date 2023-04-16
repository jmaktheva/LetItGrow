import wifi
import socketpool
import io
import re
import errno
import os
import sys

import random
#User Libraries
import server
import iftt

#Global Variables
Gled_switch = 0 
Gled_color = 0 # = White 1 = Purple
Gled_brightness = 0
Gled_schedule = 0

Gwater_switch = 0
Gwater_input = 0
Gwater_tank = 0
Gwater_schedule = 0

Gsensor_moisture = 0
Gsensor_temperature = 0
Gsensor_npk = 0
Gsensor_airquality = 0
Gsensor_light = 0

 #Settings Values (Notifications)
moisture_upper = 0
moisture_lower = 0
temperature_upper = 0
temperature_lower = 0
npk_upper = 0
npk_lower = 0
airquality_upper = 0
airquality_lower = 0
light_upper = 0
light_lower = 0




ip = server.InitializeWifi('TheCrib','daddymitch')
socket = server.IntializeSocket(ip)


def MessageData(Filename):
    
    global Gled_switch
    global Gled_color
    global Gled_brightness
    global Gled_schedule

    global Gwater_switch
    global Gwater_input
    global Gwater_inputValue
    global Gwater_tank
    global Gwater_schedule

    global Gsensor_moisture
    global Gsensor_temperature
    global Gsensor_npk
    global Gsensor_airquality
    global Gsensor_light
    
    global moisture_upper
    global moisture_lower
    global temperature_upper
    global temperature_lower
    global npk_upper
    global npk_lower
    global airquality_upper
    global airquality_lower
    global light_upper
    global light_lower
    
    
        
    headers = {}
    
    if Filename == "sensor_temperature":
        variable = str(Gsensor_temperature)
    elif Filename == "sensor_npk":
        variable = str(Gsensor_npk)
    elif Filename == "sensor_airquality":
        variable = str(Gsensor_airquality)
    elif Filename == "sensor_light":
        variable = str(Gsensor_light)
    elif Filename == "led_switch":
        variable = str(Gled_switch)
    elif Filename == "led_color":
        variable = str(Gled_color)
    elif Filename == "led_brightness":
        variable = str(Gled_brightness)
    elif Filename == "led_schedule":
        variable = str(Gled_schedule)
    elif Filename == "water_switch":
        variable = str(Gwater_switch)
    elif Filename == "water_input":
        variable = str(Gwater_input)   
    elif Filename == "water_tank":
        variable = str(Gwater_tank)        
    elif Filename == "water_schedule":
        variable = str(Gwater_schedule)       
    elif Filename == "sensor_moisture":
        variable = str(Gsensor_moisture)   
    elif Filename == "moisture_upper":
        variable = str(moisture_upper)
    elif Filename == "moisture_lower":
        variable = str(moisture_lower)
    elif Filename == "temperature_upper":
        variable = str(temperature_upper)
    elif Filename == "temperature_lower":
        variable = str(temperature_lower)
    elif Filename == "npk_upper":
        variable = str(npk_upper)
    elif Filename == "npk_lower":
        variable = str(npk_lower)
    elif Filename == "airquality_upper":
        variable = str(airquality_upper)
    elif Filename == "airquality_lower":
        variable = str(airquality_lower)
    elif Filename == "light_upper":
        variable = str(light_upper)
    elif Filename == "light_lower":
        variable = str(light_lower)
    elif Filename == "feedback":
        variable = ""
    else:
        return -1; 
        
    
    with io.BytesIO() as response:
        
        response.write(("HTTP/1.1 200 OK\r\n").encode())
        headers["Content-Length"] = 4;

        response.write(b"\r\n")
        response.write(variable.encode())
    
        response.write(b"\r\n")
        
        response.flush()
        response.seek(0)
        response_buffer = response.read()
        
        return response_buffer
    
    

def MessagePage(Filename):
    
    response_buffer = MessageData(Filename)   
     
    if response_buffer != -1: #Didn't Need to Parse
        return response_buffer
        
    #Filename = "water.svg"
    myfile = open(Filename, "rb")
    headers = {}

    if(".svg" in Filename):
        headers["Content-Type"] = "image/svg+xml"
    
    headers["Content-Length"] = os.stat(Filename)[6]
    
    
    with io.BytesIO() as response:
        response.write(("HTTP/1.1 200 OK\r\n").encode())
        for k, v in headers.items():
            response.write(("%s: %s\r\n" % (k, v)).encode())

        response.write(b"\r\n")
        response.write(myfile.read())
    
        response.write(b"\r\n")
        
        response.flush()
        response.seek(0)
        response_buffer = response.read()
            
        
        return response_buffer

def parseForm(value):
    
    message = value.split("&")
    #print(message)
    
    if(message[0] == 'settingsID=settingsID'):
         #Settings Values (Notifications)
        global moisture_upper
        global moisture_lower
        global temperature_upper
        global temperature_lower
        global npk_upper
        global npk_lower
        global airquality_upper
        global airquality_lower
        global light_upper
        global light_lower
        
        for x in message:
            temp = x.split("=")
            if(temp[1] == ''):
                continue
            
            if(temp[0] == "moisture_upper"):
                moisture_upper = int(temp[1])
            elif(temp[0] == "moisture_lower"):
                moisture_lower = int(temp[1])
            elif(temp[0] == "temperature_upper"):
                temperature_upper = int(temp[1])
            elif(temp[0] == "temperature_lower"):
                temperature_lower = int(temp[1])
            elif(temp[0] == "npk_upper"):
                npk_upper = int(temp[1])
            elif(temp[0] == "npk_lower"):
                npk_lower = int(temp[1])
            elif(temp[0] == "airquality_upper"):
                airquality_upper = int(temp[1])
            elif(temp[0] == "airquality_lower"):
                airquality_lower = int(temp[1])
            elif(temp[0] == "light_upper"):
                light_upper = int(temp[1])
            elif(temp[0] == "light_lower"):
                light_lower = int(temp[1])     

    return
    

while True: 
    message = bytearray()
    buffer = bytearray(1024)
    
    try:
        conn, addr = socket.accept()
        client = conn.recv_into(buffer)
        print('Got a connection from %s' % str(addr))
        
    except OSError as e:
        print("Errno Socket.Accept()")
        if e.errno == errno.EAGAIN:
            conn.close()
            continue
    
    socket_recv = True
    while socket_recv:
        for byte in buffer:
            if byte == 0x00:
                socket_recv = False
                break
            else:
                message.append(byte)

    #Read Message
    reader = io.BytesIO(message)
    line = str(reader.readline(), "utf-8")
    (method, full_path, _) = line.rstrip("\r\n").split(None, 2)
    
    
    #Message Parsing
    if method == "POST":
        header = str(reader.getvalue(), "utf-8")
        content = header.split("Content-Type: ")[1].split("\r\n")[0]
        value = header.split("\r\n\r\n",2)[1]
        #print(value)
        print("POST REQUEST CONTENT == " + content)
        print("POST REQUEST VALUE == " + value + "\n")
        
        if(content == "application/x-www-form-urlencoded"):
            parseForm(value)
            
            response_buffer = MessagePage("settings.html")    
            response_length = len(response_buffer)
            
            bytes_sent_total = 0 
            while True:
                try:
                    bytes_sent = conn.send(response_buffer)
                    bytes_sent_total += bytes_sent
                    
                    
                    if bytes_sent_total >= response_length:
                        break
                    else:
                        response_buffer = response_buffer[bytes_sent:]
                        continue
                
                except OSError as e:
                    if (e.errno == 11):       
                        continue
                    
            conn.close()
            
            continue
            print("Trouble")
            
        #Case Statement
        if content == "led_switch":
            
            Gled_switch = int(value)
            print("Demo Video LED_SWITCH OUTPUT =" + str(Gled_switch))
            
            response_buffer = MessageData("feedback")
            response_length = len(response_buffer)
            
            bytes_sent_total = 0 
            while True:
                try:
                    bytes_sent = conn.send(response_buffer)
                    bytes_sent_total += bytes_sent
                    
                    
                    if bytes_sent_total >= response_length:
                        break
                    else:
                        response_buffer = response_buffer[bytes_sent:]
                        continue
                
                except OSError as e:
                    if (e.errno == 11):       
                        continue
                    
            print("Sent Back HTTP200 LED STATE")
            conn.close()
            
            
        elif content == "led_color":
            Gled_color = int(value)
            
            print("Demo Video LED_COLOR OUTPUT =" + str(Gled_color))
            
            response_buffer = MessageData("feedback")
            response_length = len(response_buffer)
            
            bytes_sent_total = 0 
            while True:
                try:
                    bytes_sent = conn.send(response_buffer)
                    bytes_sent_total += bytes_sent
                    
                    
                    if bytes_sent_total >= response_length:
                        break
                    else:
                        response_buffer = response_buffer[bytes_sent:]
                        continue
                
                except OSError as e:
                    if (e.errno == 11):       
                        continue
                    
            print("Sent Back HTTP200 LED COLOR")
            conn.close()
        elif content == "led_brightness":
            Gled_brightness = int(value)
            
            print("Demo Video LED_Brightness OUTPUT =" + str(Gled_brightness))
            response_buffer = MessageData("feedback")
            response_length = len(response_buffer)
            
            bytes_sent_total = 0 
            while True:
                try:
                    bytes_sent = conn.send(response_buffer)
                    bytes_sent_total += bytes_sent
                    
                    
                    if bytes_sent_total >= response_length:
                        break
                    else:
                        response_buffer = response_buffer[bytes_sent:]
                        continue
                
                except OSError as e:
                    if (e.errno == 11):       
                        continue
                    
            print("Sent Back HTTP200 LED BRIGHTNESS")
            conn.close()
        elif content == "led_schedule":
            Gled_schedule = int(value)
        elif content == "water_switch":
            Gwater_switch = int(value)
        elif content == "water_input":
            Gwater_input = 1 #Microcontroller Turns Off
            Gwater_inputValue = int(value)
            print("Demo Video WATER INPUT Value =" + str(Gwater_input))
            print("Demo Video WATER AMOUNT Value =" + str(Gwater_inputValue))
            
            response_buffer = MessageData("feedback")
            response_length = len(response_buffer)
            
            bytes_sent_total = 0 
            while True:
                try:
                    bytes_sent = conn.send(response_buffer)
                    bytes_sent_total += bytes_sent
                    
                    
                    if bytes_sent_total >= response_length:
                        break
                    else:
                        response_buffer = response_buffer[bytes_sent:]
                        continue
                
                except OSError as e:
                    if (e.errno == 11):       
                        continue
                    
            print("Sent Back HTTP200 Water Input")
            conn.close()
        elif content == "water_tank":
            Gwater_tank = int(value)
        elif content == "water_schedule":
            Gwater_schedule = int(value)
        elif content == "sensor_moisture":
            Gsensor_moisture = int(value)
        elif content == "sensor_temperature":
            Gsensor_temperature = int(value)
        elif content == "sensor_npk":
            Gsensor_npk = int(value)
        elif content == "sensor_airquality":
            Gsensor_airquality = int(value)
        elif content == "sensor_light":
            Gsensor_light = int(value)
        
    elif method == "GET":
        
        #Figure Out What File To Retrieve
        if(full_path == "/"):
            Filename = "index.html"
        else:
            Filename = full_path.rstrip("/").split("/")[1]
        
        #Checks if LED is ON
        if(((Filename == "brightness.html") and (Gled_switch == 0)) or ((Filename == "color.html") and (Gled_switch == 0))):
            Filename = "warning_light.html"
        
        
        #Send File as Response
        print("NAME OF FILE == " + Filename)
        
        response_buffer = MessagePage(Filename)    
        response_length = len(response_buffer)
       
       #Send Function
        bytes_sent_total = 0 
        while True:
            try:
                bytes_sent = conn.send(response_buffer)
                bytes_sent_total += bytes_sent
                
                
                if bytes_sent_total >= response_length:
                    break
                else:
                    response_buffer = response_buffer[bytes_sent:]
                    continue
            
            except OSError as e:
                if (e.errno == 11):       
                    continue
                    
        
    conn.close()
    print("END OF CONNECTION")


