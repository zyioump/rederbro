import time
import socket
import readline

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect(("127.0.0.1", 9876))

running = True

while running:
    msg = input("msg --> ")

    if msg is "":
        running = False
    else:
        socket.send(msg.encode())

socket.close()
