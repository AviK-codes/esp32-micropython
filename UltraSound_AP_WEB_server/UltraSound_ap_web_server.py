import hcsr04
import ssd1306
import time
from machine import I2C, Pin

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

sensor = hcsr04.HCSR04(trigger_pin=11, echo_pin=10,echo_timeout_us=1000000)
i2c = I2C(0,scl=Pin(12), sda=Pin(13))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Configure the ESP32 wifi as Access Point mode

ssid = 'USserver'
password = '01234567'

ap = network.WLAN(network.AP_IF)
ap.active(True)
time.sleep(5)

ap.config(essid=ssid, password=password, authmode=3)

while not ap.active():
    pass
    
print('network config:', ap.ifconfig())
print("ssid:",ssid, "password:",password)

# Function for creating the web page to be displayed
def web_page():
   # Get the Ultrasound sensor readings
   distance = sensor.distance_cm()
   distance = round(distance,2)
   print(distance)

   oled.fill(0)
    
   oled.text("Distance is:",20,1) 
   # with method 2 with the modified ssd1306.py library, look at folder 'SSD1306_I2C_OLED_Display_Method2_Large_Fonts'
   oled.write_text(str(round(distance,1)), x=1, y=14, size=2)
   oled.write_text("cm",85,14,2)
   oled.show()

   html_page = """ 
     <html>   
     <head>   
      <meta name="viewport" content="width=device-width, initial-scale=1">   
      <meta http-equiv="refresh" content="2">
     </head>   
     <body>   
       <center><h2>ESP32 Web Server in MicroPython </h2></center>   
       <center><p>Distance is <strong>""" + str(distance) + """ CM</strong>.</p></center> 
       <center><p>Distance is <strong>""" + str(distance/100) + """ M</strong>.</p></center>   
     </body>   
     </html>"""
   return html_page
   
# Configure the socket connection over TCP/IP
# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

try:
  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()

except KeyboardInterrupt:
       pass
