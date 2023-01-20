import socket
import time

HOST = "161.35.162.53"
# HOST = "127.0.0.1"
PORT = 31664

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

