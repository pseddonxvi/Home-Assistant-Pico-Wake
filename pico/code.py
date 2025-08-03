import time
import board
import wifi
import socketpool
import usb_hid
import adafruit_requests
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#WiFi Details
SSID = "WiFi NETWORK NAME HERE" 
PASSWORD = "WiFi PASSWORD HERE"

#WiFi connection status
print("Connecting to WiFi...")
try:
    wifi.radio.connect(SSID, PASSWORD)
    print("Connected to", SSID)
    print("IP adress:", wifi.radio.ipv4_address)
except Exception as e:
    print("WiFi connection failed", e)

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()
server.bind(("0.0.0.0", 5000))
server.listen(1)
server.settimeout(None)

keyboard = Keyboard(usb_hid.devices)

print("Waiting for command...")

while True:
    conn, addr = server.accept()
    print("Connection from", addr)
    buf = bytearray(64)
    num_bytes = conn.recv_into(buf)
    data = buf[:num_bytes]
    print("Received:", data)
    
    if b"wake" in data:
        print("Triggering key press...")
        keyboard.press(Keycode.LEFT_SHIFT) 
        time.sleep(0.1)
        keyboard.release_all()
        
#     conn.send(b"OK\n")
#     conn.close()