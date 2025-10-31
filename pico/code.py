import time
import board
import wifi
import socketpool
import usb_hid
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#WiFi Details
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# Reset WiFi radio
print("Resetting WiFi radio...")
wifi.radio.enabled = False
time.sleep(1)
wifi.radio.enabled = True
time.sleep(2)

print("Connecting to WiFi...")
try:
    wifi.radio.connect(SSID, PASSWORD, timeout=10)
    print("Connected to", SSID)
    print("IP address:", wifi.radio.ipv4_address)
except Exception as e:
    print("WiFi connection failed:", type(e).__name__, str(e))
    print("Performing hard reset in 3 seconds...")
    time.sleep(3)
    microcontroller.reset()  # Hard reset the board

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()

try:
    server.bind(("0.0.0.0", 5000))
    server.listen(1)
    server.settimeout(None)
except OSError as e:
    print("Socket binding failed:", e)
    print("Port 5000 already in use. Performing hard reset in 3 seconds...")
    time.sleep(3)
    microcontroller.reset()

keyboard = Keyboard(usb_hid.devices)

print("Waiting for command on port 5000...")

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
#        keyboard.press(Keycode.CAPS_LOCK)         - Caps lock key for testing since you can see the indicator light on your keyboard
        time.sleep(0.1)
        keyboard.release_all()
    
    conn.close()
