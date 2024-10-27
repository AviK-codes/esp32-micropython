import machine, time
from micropython import const
import time
import framebuf
import sys
from machine import Pin, I2C, Timer
from time import sleep
import ssd1306
import hcsr04
#import freesans20
#import writer
    
sensor = hcsr04.HCSR04(trigger_pin=11, echo_pin=10,echo_timeout_us=1000000)

i2c = I2C(0,scl=Pin(12), sda=Pin(13))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

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

# try:
#   while True:
#     distance = sensor.distance_cm()
#     print(round(distance,2))
# 
#     oled.fill(0)
#     
#     #with the regular method
#     oled.text("Distance is:",20,1) 
#     #oled.text(str(round(distance,2)),30,24)
#     # with method 2 with the modified ssd1306.py library, look at folder 'SSD1306_I2C_OLED_Display_Method2_Large_Fonts'
#     oled.write_text(str(round(distance,1)), x=1, y=14, size=2)
#     oled.write_text("cm",85,14,2)
#     #oled.text("cm",100,20)
#     
#     # Enlarging font size with method 1, look at folder 'SSD1306_I2C_OLED_Display_Method1_Large_Fonts'
#     # for the required libraries that should be imported, freesans20 and writer
#     # with the larger charachters by using freesans20 and writer libraries
#     #font_writer = writer.Writer(oled, freesans20)
#     #oled.text("Distance:",30,1)
#     #font_writer.set_textpos(5, 10)
#     #font_writer.printstring('Dist')
#     #font_writer.set_textpos(40, 10)
#     #font_writer.printstring(str(round(distance,2)))
#     oled.show()
#     
# except KeyboardInterrupt:
#        pass
