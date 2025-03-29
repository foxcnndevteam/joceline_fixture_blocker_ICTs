import threading

from core import config
from PyQt5.QtCore import pyqtSignal, QObject

'''
#   Class: UDPSignals
#   Desc: Defines the update_ui & stop_server signals to communicate between Panel & Server to update Panel and correctly stop Server.
'''
class UDPSignals(QObject):
    update_ui = pyqtSignal()
    stop_server = threading.Event()


'''
#   Class: ServerEnviroment
#   Desc: Defines the server eviroments vars like Host & Port.
'''
class ServerEnviroment():
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = config.get_udp_server_port()