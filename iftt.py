import wifi
import socketpool
import io

'''
#Wifi Connectivity
ssid = 'TheBeast'
password = 'lolsquare'


for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")
print("joining network...")
print(wifi.radio.connect(ssid=ssid,password=password))

print("my IP addr:", wifi.radio.ipv4_address)
ip = str(wifi.radio.ipv4_address)
'''
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


