import time
from machine import I2C, Pin, Timer

led = Pin(18,Pin.OUT)
ir_prox = Pin(16,Pin.IN)
led.off()

# # Configure the ESP32 wifi as Access Point mode
# tim1 = Timer(1)
# def read_us_callback(timer_us):
   # # Get the Ultrasound sensor readings
   # global distance
   # distance = sensor.distance_cm()
   # distance = round(distance,2)
   # print(distance)
   # oled.fill(0)
    
   # oled.text("Distance is:",20,1) 
   # # with method 2 with the modified ssd1306.py library, look at folder 'SSD1306_I2C_OLED_Display_Method2_Large_Fonts'
   # oled.write_text(str(round(distance,1)), x=1, y=14, size=2)
   # oled.write_text("cm",85,14,2)
   # oled.show()
pin = 0
proximity = False
# tim1.init(period=200, mode=Timer.PERIODIC, callback=read_us_callback)
def handle_ir_int(pin):
    global proximity
    proximity = True

ir_prox.irq(trigger=Pin.IRQ_RISING,handler=handle_ir_int)

i=0
while True:
    if proximity:
        proximity = False
        led.value(True)
        print(f"interrupt: {ir_prox.value()}")
        time.sleep(1)
        led.value(False)
#    i = i + 1
#    level=ir_prox.value()
#    print(level, i)
#    led.value(level)
#p0.irq(lambda p:print(p))
   