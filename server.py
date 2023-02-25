import wifi
import socketpool
import io
import re
import errno
import os
import sys

#User Libraries
import server

#Global Variables
Gled_switch = 0 
Gled_color = 0 # 0 = White 1 = Purple
Gled_brightness = 0
Gled_schedule = 0

Gwater_switch = 0
Gwater_input = 0
Gwater_tank = 0
Gwater_schedule = 0

Gsensor_moisture = 0
Gsensor_temperature = 0
Gsensor_nitrogen = 0
Gsensor_potassium = 0
Gsensor_phosphorous = 0

 #Settings Values (Notifications)
moisture_upper = 0
moisture_lower = 0
temperature_upper = 0
temperature_lower = 0
nitrogen_upper = 0
nitrogen_lower = 0
potassium_upper = 0
potassium_lower = 0
phosphorous_upper = 0
phosphorous_lower = 0


'''
Function Declarations

'''


def MessageData(Filename):
    
    global Gsensor_temperature
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
    global Gsensor_nitrogen
    global Gsensor_potassium
    global Gsensor_phosphorous
    
    global moisture_upper
    global moisture_lower
    global temperature_upper
    global temperature_lower
    global nitrogen_upper
    global nitrogen_lower
    global potassium_upper
    global potassium_lower
    global phosphorous_upper
    global phosphorous_lower
        
    headers = {}
    
    if Filename == "sensor_temperature":
        variable = str(Gsensor_temperature)
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
    elif Filename == "sensor_nitrogen":
        variable = str(Gsensor_nitrogen)
    elif Filename == "sensor_potassium":
        variable = str(Gsensor_potassium)
    elif Filename == "sensor_phosphorous":
        variable = str(Gsensor_phosphorous)
    elif Filename == "moisture_upper":
        variable = str(moisture_upper)
    elif Filename == "moisture_lower":
        variable = str(moisture_lower)
    elif Filename == "temperature_upper":
        variable = str(temperature_upper)
    elif Filename == "temperature_lower":
        variable = str(temperature_lower)
    elif Filename == "nitrogen_upper":
        variable = str(nitrogen_upper)
    elif Filename == "nitrogen_lower":
        variable = str(nitrogen_lower)
    elif Filename == "phosphorous_upper":
        variable = str(phosphorous_upper)
    elif Filename == "phosphorous_lower":
        variable = str(phosphorous_lower)
    elif Filename == "potassium_upper":
        variable = str(potassium_upper)
    elif Filename == "potassium_lower":
        variable = str(potassium_lower)
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
        global nitrogen_upper
        global nitrogen_lower
        global potassium_upper
        global potassium_lower
        global phosphorous_upper
        global phosphorous_lower
        
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
            elif(temp[0] == "nitrogen_upper"):
                nitrogen_upper = int(temp[1])
            elif(temp[0] == "nitrogen_lower"):
                nitrogen_lower = int(temp[1])
            elif(temp[0] == "potassium_upper"):
                potassium_upper = int(temp[1])
            elif(temp[0] == "potassium_lower"):
                potassium_lower = int(temp[1])
            elif(temp[0] == "phosphorous_upper"):
                phosporous_upper = int(temp[1])
            elif(temp[0] == "phosphorous_lower"):
                phosphorous_lower = int(temp[1])     

    return
    

def InitializeWifi(ssid,password):
    #Wifi Connectivity
    #ssid = 'TheCrib'
    #password = 'daddymitch'

    #Returns IP Address
    for network in wifi.radio.start_scanning_networks():
        print(network, network.ssid, network.channel)
    wifi.radio.stop_scanning_networks()

    print("joining network...")
    print("joining network...")
    print(wifi.radio.connect(ssid=ssid,password=password))

    print("my IP addr:", wifi.radio.ipv4_address)
    
    return str(wifi.radio.ipv4_address)

def IntializeSocket(ip):
    pool = socketpool.SocketPool(wifi.radio)
    socket = pool.socket()
    socket.bind([ip,80])
    socket.listen(5)
    socket.setblocking(True)
    socket.settimeout(None)
    
    return socket
    
def serverSend(response_buffer,conn):
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

    return


def sendNotification():
    #Create Socket
    pool = socketpool.SocketPool(wifi.radio)
    socket = pool.socket()

    #Connect Socket
    temp = pool.getaddrinfo("maker.ifttt.com", 80)
    ifttt = temp[0][4]

    socket.connect(ifttt)

    #Set Headers
    headers ={}
    #api_key = "api_key=XQOBNA59WMROOC0U\r\n"


    headers["Host"]= "maker.ifttt.com"
    headers["Connection"] = "close"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    #headers["Content-Length"] = len(api_key.encode('utf-8') ) + len(field_message.encode('utf-8'))
    headers["Content-Length"] = 0


    with io.BytesIO() as response:
        response.write(("POST /trigger/NotificationAlert/with/key/cbYpss66MlC9TGuRcUazbq HTTP/1.1\r\n").encode())
        for k, v in headers.items():
            response.write(("%s: %s\r\n" % (k, v)).encode())

        response.write(b"\r\n")

        response.write(b"\r\n")
        
        response.flush()
        response.seek(0)
        response_buffer = response.read()
        print(response_buffer)
        response_length = len(response_buffer)
        
    bytes_sent_total = 0 
    while True:
        try:
            bytes_sent = socket.send(response_buffer)
            bytes_sent_total += bytes_sent
            
            
            if bytes_sent_total >= response_length:
                break
            else:
                response_buffer = response_buffer[bytes_sent:]
                continue
        
        except OSError as e:
            if (e.errno == 11):       
                continue

    message = bytearray()
    buffer = bytearray(1024)
    socket_recv = True
    socket.recv_into(buffer)

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
    header = str(reader.getvalue(), "utf-8")
    print(header)


    socket.close()


#ip = InitializeWifi('TheBeast','lolsquare')
#socket = IntializeSocket(ip)

def webserver(socket):
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
            #continue
            return
        
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
                        #continue
                        return
                except OSError as e:
                    if (e.errno == 11):       
                        #continue
                        return
            conn.close()
            
            #continue
            return
            print("Trouble")
            
        #Case Statement
        if content == "led_switch":
            
            Gled_switch = int(value)
            
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
                        #continue
                        return
                
                except OSError as e:
                    if (e.errno == 11):       
                        #continue
                        return
            print("Sent Back HTTP200 LED STATE")
            conn.close()
            
            
        elif content == "led_color":
            Gled_color = int(value)
            
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
                        #continue
                        return
                
                except OSError as e:
                    if (e.errno == 11):       
                        #continue
                        return
                    
            print("Sent Back HTTP200 LED COLOR")
            conn.close()
        elif content == "led_brightness":
            Gled_brightness = int(value)
            
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
                        #continue
                        return
                
                except OSError as e:
                    if (e.errno == 11):       
                        #continue
                        return
                    
            print("Sent Back HTTP200 LED BRIGHTNESS")
            conn.close()
        elif content == "led_schedule":
            Gled_schedule = int(value)
        elif content == "water_switch":
            Gwater_switch = int(value)
        elif content == "water_input":
            Gwater_input = 1
            Gwater_inputValue = int(value)
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
                        #continue
                        return
                
                except OSError as e:
                    if (e.errno == 11):       
                        #continue
                        return
                    
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
        elif content == "sensor_nitrogen":
            Gsensor_nitrogen = int(value)
        elif content == "sensor_potassium":
            Gsensor_nitrogen = int(value)
        elif content == "sensor_phosphorous":
            Gsensor_phosphorous = int(value)
        
    elif method == "GET":
        
        #Figure Out What File To Retrieve
        if(full_path == "/"):
            Filename = "index.html"
        else:
            Filename = full_path.rstrip("/").split("/")[1]
        
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
                    #continue
                    return
            
            except OSError as e:
                if (e.errno == 11):       
                    #continue
                    return
                    
        
        conn.close()
        print("END OF CONNECTION")



