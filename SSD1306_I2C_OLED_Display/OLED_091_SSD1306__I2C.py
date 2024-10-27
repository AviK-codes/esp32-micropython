from machine import Pin, I2C
import ssd1306

# ESP32 Pin assignment 
i2c = I2C(0,scl=Pin(12), sda=Pin(13))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
 
oled.text('Hello world 1',0, 0)
oled.text('Hello world 2',0, 12)
oled.text('Hello world 3',0, 24)
# oled.invert(True)
oled.show()