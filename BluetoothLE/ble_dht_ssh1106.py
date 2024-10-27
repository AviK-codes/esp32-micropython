# Rui Santos & Sara Santos - Random Nerd Tutorials
# Refference from project details at https://RandomNerdTutorials.com/micropython-esp32-bluetooth-low-energy-ble/

from micropython import const
import uasyncio as asyncio
import aioble
import bluetooth
import struct
from machine import Pin, I2C
from random import randint
import uos, sh1106
import freesans20
import writer
import dht

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

i2c = I2C(0,scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
font_writer = writer.Writer(display, freesans20)
display.flip()
display.contrast(255)
display.sleep(False)

# Init LED
led = Pin(LED_PIN, Pin.OUT)
led.value(0)
sensor = dht.DHT22(Pin(US_TRIGGER_PIN))

# Constants for the device information Service
_SVC_DEVICE_INFO = bluetooth.UUID(0x180A)
svc_dev_info = aioble.Service(_SVC_DEVICE_INFO)

# Constants for the UUID for device information characteristics
_CHAR_MANUFACTURER_NAME_STR = bluetooth.UUID(0x2A29)
_CHAR_MODEL_NUMBER_STR = bluetooth.UUID(0x2A24)
_CHAR_SERIAL_NUMBER_STR = bluetooth.UUID(0x2A25)
_CHAR_FIRMWARE_REV_STR = bluetooth.UUID(0x2A26)
_CHAR_HARDWARE_REV_STR = bluetooth.UUID(0x2A27)

# Adding characteristics to the service
aioble.Characteristic(svc_dev_info, _CHAR_MANUFACTURER_NAME_STR, read=True, initial='AviK')
aioble.Characteristic(svc_dev_info, _CHAR_MODEL_NUMBER_STR, read=True, initial='AviK-0001')
aioble.Characteristic(svc_dev_info, _CHAR_SERIAL_NUMBER_STR, read=True, initial='AviK-0001-0000')
aioble.Characteristic(svc_dev_info, _CHAR_FIRMWARE_REV_STR, read=True, initial='0.1')
aioble.Characteristic(svc_dev_info, _CHAR_HARDWARE_REV_STR, read=True, initial='0.1')

# Constants for the Environmental Sensing Service used for temperature and humidity
_SVC_ENVIRONM_SENSING = bluetooth.UUID(0x181A)
svc_env_sensing = aioble.Service(_SVC_ENVIRONM_SENSING)

# Constant for standard UUID characteristic for temperature and humidity measurment
_CHAR_TEMP_MEASUREMENT = bluetooth.UUID(0x2A6E) #0x2A1C
_CHAR_HUMIDITY_MEASURMENT = bluetooth.UUID(0x2A6F)

# Adding characteristics to the service
temperature_char = aioble.Characteristic(svc_env_sensing, _CHAR_TEMP_MEASUREMENT, read=True, notify=True, capture=True)
humidity_char = aioble.Characteristic(svc_env_sensing, _CHAR_HUMIDITY_MEASURMENT, read=True, notify=True, capture=True)

# Constants for the led button control Service
# from: https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/libraries/bluetooth_services/services/lbs.html
_SVC_LED_BUTTON_CONTROL = bluetooth.UUID('00001523-1212-EFDE-1523-785FEABCD123')
# Adding characteristics to the service
svc_lebbutton_cntl = aioble.Service(_SVC_LED_BUTTON_CONTROL)

#constant for characteristic of LED button control
_CHAR_LED_BUTTON_UUID = bluetooth.UUID('00001525-1212-EFDE-1523-785FEABCD123')
led_button_char = aioble.Characteristic(svc_lebbutton_cntl, _CHAR_LED_BUTTON_UUID, read=True, write=True, notify=True, capture=True)

# Registering all the services
aioble.register_services(svc_dev_info, svc_env_sensing, svc_lebbutton_cntl)

_ADVERTISING_INTERVAL_MS = const(200_000)
_APPEARANCE = const(0x0556) # Multi-sensor
      
connected=False
led_off = False

def get_temp_humidity():
   sensor.measure()
   temperature = sensor.temperature()
   humidity = sensor.humidity()
   temperature = round(temperature,2)
   humidity = round(humidity,2)
   print(f"temperature is: {temperature}c humidity is: {humidity}%")
   
   # display on the oled
   display.fill(0)
   display.text('Temperature', 15, 0)
   font_writer.set_textpos(35, 10)
   font_writer.printstring(str(temperature))
   font_writer.set_textpos(75, 10)
   font_writer.printstring("c")
   display.text('Humidity', 30, 32, 1)
   font_writer.set_textpos(40, 42)
   font_writer.printstring(str(humidity))
   font_writer.set_textpos(80, 42)
   font_writer.printstring("%")
   display.show()
   
   return temperature, humidity

async def task_peripheral():
  """ Task to handle advertising and connections """
  global connected
  while True:
      try:
            connected = False
            print("advertizing")
            async with await aioble.advertise(
                _ADVERTISING_INTERVAL_MS,
                appearance=_APPEARANCE,
                name='AVIK_ESP32',
                services=[_SVC_DEVICE_INFO, _SVC_ENVIRONM_SENSING, _SVC_LED_BUTTON_CONTROL]
            ) as connection:
              print("Connected from ", connection.device)
              connected = True
              await connection.disconnected()   

      except Exception as e:
            print("Error in peripheral_task:", e)
      finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)

async def wait_for_write():
    global led_off
    while True:
        try:
            connection, data = await led_button_char.written()
            print(data)
            print(type)
            data = _decode_data(data)
            print('Connection: ', connection)
            print('Data: ', data)
            if data == 1:
                print('Turning LED ON')
                led_off = False
            elif data == 0:
                print('Turning LED OFF')
                led_off = True
            else:
                print('Unknown command')
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)

# Helper to encode the data characteristic UTF-8
def _encode_data(data):
    return str(data).encode('utf-8')

# Helper to decode the LED characteristic encoding (bytes).
def _decode_data(data):
    try:
        if data is not None:
            # Decode the UTF-8 data
            number = int.from_bytes(data, 'big')
            return number
    except Exception as e:
        print("Error decoding data:", e)
        return None

async def task_flash_led():
     """ Blink the on-board LED, faster if disconnected and slower if connected  """
     global led_off
     BLINK_DELAY_MS_FAST = const(100)
     BLINK_DELAY_MS_SLOW = const(1000)
     while True:
       if not led_off: # if led_off is False than toogle the LED
           led.value(not led.value()) # toggle LED
       else:
           led.value(0) # if led_off is True turn the LED off
           
       if connected:
         await asyncio.sleep_ms(BLINK_DELAY_MS_SLOW)
       else:
         await asyncio.sleep_ms(BLINK_DELAY_MS_FAST)

def convert_temperature_to_bytes(temp_celsius):
    # Temperature in Celsius to characteristic (2 bytes, little-endian)
    temp_bytes = struct.pack('<h', int(temp_celsius * 100))
    return temp_bytes

def convert_humidity_to_bytes(humidity_percent):
    # Humidity in percentage to characteristic (2 bytes, little-endian)
    humidity_bytes = struct.pack('<H', int(humidity_percent * 100))
    return humidity_bytes


async def task_sensor():
     """ Task to handle sensor measures """
     while True:
       temperature, humidity = get_temp_humidity() 
       #temperature =  27.0 #- ((adc.read_u16() * 3.3 / 65535) - 0.706) / 0.001721
       #print("T: {}°C".format(temperature))
       #humidity = 50.0
       temperature_char.write(convert_temperature_to_bytes(temperature), send_update=True)
       humidity_char.write(convert_humidity_to_bytes(humidity), send_update=True)
       _TEMP_MEASUREMENT_INTERVAL_MS = const(15_000)
       await asyncio.sleep_ms(_TEMP_MEASUREMENT_INTERVAL_MS)

async def main():
     """ Create all the tasks """
     tasks = [
       asyncio.create_task(task_peripheral()),
       asyncio.create_task(task_flash_led()),
       asyncio.create_task(task_sensor()),
       asyncio.create_task(wait_for_write())
     ]
     await asyncio.gather(*tasks)
  
asyncio.run(main())