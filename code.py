'''
import wifi
import socketpool
import io
import re
import errno
import os

#Wifi Connectivity
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

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind([ip,80])
socket.listen(5)
socket.setblocking(True)
socket.settimeout(None)


buffer = bytearray(1024)
message = bytearray()

while True:

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


    reader = io.BytesIO(message)
    line = str(reader.readline(), "utf-8")
    (method, full_path, _) = line.rstrip("\r\n").split(None, 2)


    #Parse Request
    if(full_path == "/"):
        Filename = "index.html"
    else:
        Filename = full_path.rstrip("/").split("/")[1]


    #Send Response
    print(Filename)
    #Filename = "water.svg"
    myfile = open(Filename, "rb")
    headers = {}

    #headers["Server"] = "Ampule/0.0.1-alpha (CircuitPython)"
    #headers["Connection"] = "close"
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


    conn.close();
    print("end")
'''

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT





#SPI display test
#TODO: convert to module
import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_ili9341
import SPIdisplay as spid

display = spid.startup()
splash = spid.splash(display)
splash = spid.draw_background(splash, 0x00FF00)
splash = spid.draw_text(splash, 'Let It Grow', 4, 35, 60, 0xD80621)
splash = spid.draw_text(splash, 'Harsh, Jackson,', 2, 60, 120, 0xD80621)
splash = spid.draw_text(splash, 'Logan, Marcus,', 2, 60, 140, 0xD80621)
#splash = spid.draw_image(splash, '/water_resized.png', 40, 170)
#splash = spid.draw_image(splash, '/light_resized.png', 120, 170)
#splash = spid.draw_image(splash, '/health_resized.png', 200, 170)


'''
#import board
import digitalio
import time
gate = digitalio.DigitalInOut(board.IO47)
gate.direction = digitalio.Direction.OUTPUT
'''

while True:
    #gate.value = True
    #time.sleep(2)
    #gate.value = False
    #time.sleep(2)
    pass
