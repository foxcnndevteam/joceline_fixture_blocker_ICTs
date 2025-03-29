import socket
from udpsocket import ServerEnviroment

'''
#   Function: send_update_signal
#   Desc: Sends signal to server to update Panel and get new yield, status and latest N tests.
'''
def send_update_signal():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("a".encode('utf-8'), (ServerEnviroment().HOST, ServerEnviroment().PORT))