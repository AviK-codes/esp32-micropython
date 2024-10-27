from machine import Pin, I2C
import ssd1306
from time import sleep
 
# ESP32 Pin assignment 
i2c = I2C(-1, scl=Pin(6), sda=Pin(7))
 
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
 
oled.text('Welcome', 0, 0)
oled.text('OLED Display', 0, 10)
oled.text('how2electronics', 0, 20)
oled.text('Makerfabs', 0, 30)
        
oled.show()