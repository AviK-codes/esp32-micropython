# Complete project details at https://RandomNerdTutorials.com
import time

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'microp'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
time.sleep(5)
#ap.config(essid=ssid,authmode=network.AUTH_WPA_WPA2_PSK, password=password, channel = 5)
ap.config(essid=ssid,authmode=3, password=password, channel = 5)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Hello, World!</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()