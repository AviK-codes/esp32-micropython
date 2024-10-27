# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, SoftI2C
import ssd1306
from time import sleep

import framebuf
import utime
import freesans20
import writer

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(12), sda=Pin(13))

# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

font_writer = writer.Writer(oled, freesans20)
font_writer.set_textpos(5, 40)
font_writer.printstring("Hellow World!")
oled.show() 