# MicroPython SH1106 OLED driver
#
# Pin Map I2C for ESP8266
#   - 3v - xxxxxx   - Vcc
#   - G  - xxxxxx   - Gnd
#   - D2 - GPIO 5   - SCK / SCL
#   - D1 - GPIO 4   - DIN / SDA
#   - D0 - GPIO 16  - Res (required, unless a Hardware reset circuit is connected)
#   - G  - xxxxxx     CS
#   - G  - xxxxxx     D/C
#
# Pin's for I2C can be set almost arbitrary
#
from machine import Pin, I2C
import sh1106

i2c = I2C(0,scl=Pin(6), sda=Pin(7), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
display.sleep(False)
display.fill(0)
display.flip()
display.contrast(255)
display.text('Testing 1', 5, 5, 1)
display.text('Testing 2', 15, 15, 1)
display.text('Testing 3', 25, 25, 1)
display.text('Testing 4', 35, 35, 1)
display.text('Testing 4', 45, 45, 1)
display.text('Testing 5', 55, 55, 1)
display.show()