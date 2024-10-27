from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

# Initialize I2C
i2c = I2C(0, scl=Pin(12), sda=Pin(13), freq=400000)

# Initialize SSD1306 with width, height, I2C interface, and optional parameters
oled = SSD1306_I2C(128, 32, i2c)

# Display text with different sizes
oled.write_text("Hello", x=25, y=0, size=1)
oled.write_text("MicroPython!", x=0, y=20, size=1)
oled.show()