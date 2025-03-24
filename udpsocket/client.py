import socket
from udpsocket import ServerEnviroment

def send_update_signal():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("a".encode('utf-8'), (ServerEnviroment().HOST, ServerEnviroment().PORT))