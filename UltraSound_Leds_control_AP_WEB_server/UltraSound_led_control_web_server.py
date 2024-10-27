import hcsr04
import ssd1306
import time
from machine import I2C, Pin, Timer

distance = 0

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

led = Pin(18,Pin.OUT)
led.off()

# Configure the ESP32 wifi as Access Point mode
tim1 = Timer(1)
def read_us_callback(timer_us):
   # Get the Ultrasound sensor readings
   global distance
   distance = sensor.distance_cm()
   distance = round(distance,2)
   print(distance)
   oled.fill(0)
    
   oled.text("Distance is:",20,1) 
   # with method 2 with the modified ssd1306.py library, look at folder 'SSD1306_I2C_OLED_Display_Method2_Large_Fonts'
   oled.write_text(str(round(distance,1)), x=1, y=14, size=2)
   oled.write_text("cm",85,14,2)
   oled.show()
    
tim1.init(period=200, mode=Timer.PERIODIC, callback=read_us_callback)

ssid = 'USserver'
password = '01234567'

ap = network.WLAN(network.AP_IF)
ap.active(True)
time.sleep(5)

ap.config(essid=ssid, password=password, authmode=3, txpower= 4)

while not ap.active():
    pass
    
print('network config:', ap.ifconfig())
print("ssid:",ssid, "password:",password)

# Function for creating the web page to be displayed
def web_page():
   
   if isLedBlinking==True:
       led_state = 'Blinking'
       print('led is Blinking')
   else:
       if led.value()==1:
           led_state = 'ON'
           print('led is ON')
       elif led.value()==0:
           led_state = 'OFF'
           print('led is OFF')

#    html_page = """ 
#      <html>   
#      <head>   
#       <meta name="viewport" content="width=device-width, initial-scale=1">   
#       <!--<meta http-equiv="refresh" content="2">-->
#      </head>   
#      <body>   
#        <center><h2>ESP32 Web Server in MicroPython </h2></center>   
#        <center><p>Distance is <strong>""" + str(distance) + """ CM</strong>.</p></center> 
#        <center><p>Distance is <strong>""" + str(distance/100) + """ M</strong>.</p></center>
#        <center>    
#           <form>    
#               <button name="LED" type="submit" value="1"> LED ON </button>    
#               <button name="LED" type="submit" value="0"> LED OFF </button>  
#               <button name="LED" type="submit" value="2"> LED BLINK </button>   
#           </form>    
#        </center>    
#        <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>
# 
#        <script>
#            // JavaScript function to highlight the clicked button
#            function highlightButton(button) {
#                const buttons = document.querySelectorAll('button[name="LED"]');
#                buttons.forEach(btn => btn.classList.remove('highlighted-button'));
#                button.classList.add('highlighted-button');
#            }
#            // JavaScript to Refresh the page every second
#            setInterval(function () {
#                window.location.reload();
#            }, 1000);
#        </script>
#      </body>   
#      </html>"""
#    return html_page
   html_page = """
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            /* Define the styling for the highlighted button */
            .highlighted-button {
                background-color: yellow; /* Change this to your desired highlight color */
            }
        </style>
    </head>
    <body>
        <center>
            <h2>ESP32 Web Server in MicroPython</h2>
        </center>
        <center>
            <p>Distance is <strong>""" + str(distance) + """ CM</strong>.</p>
            <p>Distance is <strong>""" + str(distance/100) + """ M</strong>.</p>
        </center>
        <center>
            <form>
                <button name="LED" type="submit" value="1" onclick="highlightButton(this)">LED ON</button>
                <button name="LED" type="submit" value="0" onclick="highlightButton(this)">LED OFF</button>
                <button name="LED" type="submit" value="2" onclick="highlightButton(this)">LED BLINK</button>
            </form>
        </center>
        <center>
            <p>LED is now <strong>""" + led_state + """</strong>.</p>
        </center>

        <script>
            // JavaScript function to highlight the clicked button
            function highlightButton(button) {
                // Remove the class from all buttons
                const buttons = document.querySelectorAll('button[name="LED"]');
                buttons.forEach(btn => btn.classList.remove('highlighted-button'));

                // Add the class to the clicked button
                button.classList.add('highlighted-button');
            }

            // Refresh the page every second
            setInterval(function () {
                window.location.reload();
            }, 1000);
        </script>
 
#         <script>
#             // JavaScript function to highlight the clicked button
#             function highlightButton(button) {
#                 const buttons = document.querySelectorAll('button[name="LED"]');
#                 buttons.forEach(btn => btn.classList.remove('highlighted-button'));
#                 button.classList.add('highlighted-button');
#             }
# 
#             // Refresh the page every second
#             setInterval(function () {
#                 window.location.reload();
#             }, 1000);
#         </script>

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

tim0 = Timer(0)
def handle_callback(timer_led):
    led.value( not led.value() )
isLedBlinking = False

try:
  
  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    
    request = str(request)
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    led_blink = request.find('/?LED=2')
    if led_on == 6:
        print('LED ON')
        print(str(led_on))
        led.value(1)
        if isLedBlinking==True:
            tim0.deinit()
            isLedBlinking = False
        
    elif led_off == 6:
        print('LED OFF')
        print(str(led_off))
        led.value(0)
        if isLedBlinking==True:
            tim0.deinit()
            isLedBlinking = False
        
    elif led_blink == 6:
        print('LED Blinking')
        print(str(led_blink))
        isLedBlinking = True
        tim0.init(period=1000, mode=Timer.PERIODIC, callback=handle_callback)
    
    
    response = web_page()
    conn.send(response)
    conn.close()

except KeyboardInterrupt:
       pass
