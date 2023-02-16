import wifi
import socketpool
import io 
import re
import errno
import os

'''
#Global Variables 
#Below are placeholder variables to store POST request data values so that
#these values can be added to an HTML request sent to the database. 

'''
Gled_switch = 0
Gled_color = "white"
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

#Buffers for Parsing Data
buffer = bytearray(1024)
message = bytearray()

'''
#Wifi Connectivity
#Below is the code to connect to a specified SSID and Password for a Wifi Network
#Code scans for all local networks and then joins based on the specified SSID. 
#Prints out IP address once connected. 

'''

ssid = 'TheCrib'
password = 'daddymitch'

for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")
print("joining network...")
print(wifi.radio.connect(ssid=ssid,password=password))

print("my IP addr:", wifi.radio.ipv4_address)
ip = str(wifi.radio.ipv4_address)

'''
#TCP Connection Setup
#Below is the code to create a TCP socketpool and listen for 5 connection requests. 
#Socket is set to blocking and No Timeout so that all connections are required to have data. 

'''

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind([ip,80])
socket.listen(5)
socket.setblocking(True)
socket.settimeout(None)

#############
# MAIN LOOP #
#############

while True:
    
    '''
    #Check for Connection Requests
    #Below is code to check for requests and store message into buffer
    '''
    
    try:
        conn, addr = socket.accept()
        client = conn.recv_into(buffer)
        message = bytearray()
        
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

    #Read Message and Parse Out Header Line
    reader = io.BytesIO(message)
    line = str(reader.readline(), "utf-8")
    (method, full_path, _) = line.rstrip("\r\n").split(None, 2)
    
    '''
    #Message Parsing
    #Below is code to parse the header line for GET and POST Requests
    #POST request will print value and update global variable
    #Get Request will look for valid file and send back HTML page as response
    
    '''
    if method == "POST":
        header = str(reader.getvalue(), "utf-8")
        content = header.split("Content-Type: ")[1].split("\r\n")[0]
        value = header.split("\r\n\r\n",2)[1]
        print(content)
        print(value)
        
        #Case Statement
        if content == "led_switch":
            Gled_switch = int(value)
        else if content == "led_color":
            Gled_color = value 
        else if content == "led_brightness":
            Gled_brightness = int(value)
        else if content == "led_schedule":
            Gled_schedule = int(value)
        else if content == "water_switch":
            Gwater_switch = int(value)
        else if content == "water_input":
            Gwater_input = int(value)
        else if content == "water_tank":
            Gwater_tank = int(value)
        else if content == "water_schedule":
            Gwater_schedule = int(value)
        else if content == "sensor_moisture":
            Gsensor_moisture = int(value)
        else if content == "sensor_temperature":
            Gsensor_temperature = int(value)
        else if content == "sensor_nitrogen":
            Gsensor_nitrogen = int(value)
        else if content == "sensor_potassium":
            Gsensor_nitrogen = int(value)
        else if content == "sensor_phosphorous":
            Gsensor_phosphorous = int(value)
    
    else if method == "GET":
        
        #Figure Out What File To Retrieve
        if(full_path == "/"):
            Filename = "index.html"
        else:
            Filename = full_path.rstrip("/").split("/")[1]
        
    
        #Send File as Response
        #print(Filename)
        #Filename = "water.svg"
        myfile = open(Filename, "rb")
        headers = {}
        
        #Set HTML response Headers
        #headers["Server"] = "Ampule/0.0.1-alpha (CircuitPython)"
        #headers["Connection"] = "close"
        if(".svg" in Filename):
            headers["Content-Type"] = "image/svg+xml"
        headers["Content-Length"] = os.stat(Filename)[6]

        #Build HTML Response Message
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
            
            response_length = len(response_buffer)
            bytes_sent_total = 0
            
            #Send HTML Response to Client
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
        print("end")

