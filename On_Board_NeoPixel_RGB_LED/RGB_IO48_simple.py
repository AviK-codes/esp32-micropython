from machine import Pin
from neopixel import NeoPixel
import time
import uos


def detect_esp32_variant():
    global NEOPIXEL_GPIO
    machine_info = uos.uname().machine
    print(machine_info)
    if "ESP32C3" in machine_info:
        print("Detected ESP32-C3")
        # Set GPIOs for ESP32-C3
        NEOPIXEL_GPIO = 8 
    elif "ESP32S3" in machine_info:
        print("Detected ESP32-S3")
        # Set GPIOs for ESP32-S3
        NEOPIXEL_GPIO = 48
    else:
        print("Unknown ESP32 variant")
        # Handle other cases if needed
        # Your code here...

detect_esp32_variant()

pin = Pin(NEOPIXEL_GPIO, Pin.OUT)   # set GPIO48  to output to drive NeoPixel
neo = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO48 for 1 pixel
neo[0] = (25, 10, 50) # set the first pixel to white
neo.write()              # write data to all pixels
r, g, b = neo[0]         # get first pixel colour
print(r,g,b)
