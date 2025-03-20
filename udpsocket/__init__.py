import threading
from PyQt5.QtCore import pyqtSignal, QObject

class UDPSignals(QObject):
    update_ui = pyqtSignal()
    stop_server = threading.Event()

class ServerEnviroment():
    HOST = '127.0.0.1'
    PORT = 65432