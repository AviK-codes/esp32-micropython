from machine import Pin, I2C
import ssd1306
import freesans20
import writer

# ESP32 Pin assignment 
i2c = I2C(0,scl=Pin(6), sda=Pin(7))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

font_writer = writer.Writer(oled, freesans20)
font_writer.set_textpos(0, 0)
font_writer.printstring('Hello world 1')
#font_writer.set_textpos(95, 30)
#font_writer.printstring("C")
    
#oled.text('Hello world 1',0, 0)
#oled.text('Hello world 2',0, 12)
#oled.text('Hello world 3',0, 24)
# oled.invert(True)
oled.show()