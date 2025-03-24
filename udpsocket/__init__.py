import threading

from core import config
from PyQt5.QtCore import pyqtSignal, QObject

class UDPSignals(QObject):
    update_ui = pyqtSignal()
    stop_server = threading.Event()

class ServerEnviroment():
    
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = config.get_udp_server_port()