import hcsr04
import ssd1306
import time
from machine import I2C, Pin, Timer
import uos, sh1106
import freesans20
import writer

def detect_esp32_variant():
    global NEOPIXEL_PIN, US_TRIGGER_PIN, US_ECHO_PIN, SCL_PIN, SDA_PIN, LED_PIN
    machine_info = uos.uname().machine
    print(machine_info)
    if "ESP32C3" in machine_info:
        print("Detected ESP32-C3")
        # Set GPIOs for ESP32-C3
        NEOPIXEL_PIN = 8
        US_TRIGGER_PIN = 2
        US_ECHO_PIN = 3
        SCL_PIN = 6
        SDA_PIN = 7
        LED_PIN = 10
    elif "ESP32S3" in machine_info:
        print("Detected ESP32-S3")
        # Set GPIOs for ESP32-S3
        NEOPIXEL_PIN = 48
        US_TRIGGER_PIN = 11
        US_ECHO_PIN = 10
        SCL_PIN = 12
        SDA_PIN = 13
        LED_PIN = 18
    else:
        print("Unknown ESP32 variant")
        # Handle other cases if needed
        # Your code here...

detect_esp32_variant()
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

sensor = hcsr04.HCSR04(trigger_pin=US_TRIGGER_PIN, echo_pin=US_ECHO_PIN,echo_timeout_us=1000000)
i2c = I2C(0,scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
font_writer = writer.Writer(display, freesans20)
display.flip()
display.contrast(255)
display.sleep(False)
# oled_width = 132
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

led = Pin(LED_PIN,Pin.OUT)
led.off()

# Configure the ESP32 wifi as Access Point mode
tim1 = Timer(2)
def read_us_callback(timer_us):
   # Get the Ultrasound sensor readings
   global distance
   distance = sensor.distance_cm()
   distance = round(distance,1)
   print(distance)
#    oled.fill(0)
#     
#    oled.text("Distance is:",20,1) 
#    # with method 2 with the modified ssd1306.py library, look at folder 'SSD1306_I2C_OLED_Display_Method2_Large_Fonts'
#    oled.write_text(str(round(distance,1)), x=1, y=14, size=1)
#    oled.write_text("cm",85,14,1)
#    oled.show()
   display.fill(0)
   font_writer.set_textpos(15, 15)
   font_writer.printstring('Distance is:')
   #display.text('Distance is:', 5, 5, 1)
   #display.text(str(distance), 5, 25, 1)
   font_writer.set_textpos(25, 35)
   font_writer.printstring(str(distance))
   font_writer.set_textpos(80, 35)
   font_writer.printstring("cm")
   
   display.show()
             
tim1.init(period=200, mode=Timer.PERIODIC, callback=read_us_callback)

ssid = 'Yonatan'
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
