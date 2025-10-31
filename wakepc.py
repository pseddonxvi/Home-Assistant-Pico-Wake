import socket

#enter the static IP address of your Pico W
HOST = "YOUR PICO IP HERE"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"wake")
