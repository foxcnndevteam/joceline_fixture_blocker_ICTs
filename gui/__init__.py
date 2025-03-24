import sys
import asyncio
import threading

from gui.views import MainWindow

from PyQt5.QtWidgets import QApplication

from udpsocket import UDPSignals
from udpsocket.server import AsyncUDPServer

# --- UDP Server set up --- #
async def run_udp_server(signals):
    server = AsyncUDPServer(signals)
    await server.run_server()

# --- GUI & UDP Server execution --- #
def execute():
    
    # ~ Instance signals to comunicate GUI wiht UDP Server
    signals = UDPSignals()

    # ~ Configure main GUI view
    app = QApplication(sys.argv)
    window = MainWindow(signals)
    window.show()

    # ~ Starts UDP Server in another thread
    server_thread = threading.Thread(
        target=asyncio.run,
        args=(run_udp_server(signals),),
        daemon=True
    )

    server_thread.start()
    
    # ~ Prevents "sys.exit()" execution & get exit code
    exit_code = app.exec_()
    server_thread.join()
    app.aboutToQuit.connect(lambda: app.closeAllWindows())
    
    
    return exit_code
