import os
import sys
import asyncio
import threading

from gui.views import MainWindow

from PyQt5.QtWidgets import QApplication

from udpsocket import UDPSignals
from udpsocket.server import AsyncUDPServer

# --- UDP Server set up --- #
'''
#   Function: run_udp_server
#   Desc: Instances UDPServer an run it. 
#       signals      | type:UDPSignals | Siganals & Events to comunicate the Panel and UDP Server
'''
async def run_udp_server(signals):
    try:
        server = AsyncUDPServer(signals)
        await server.run_server()
    except OSError:
        print("error iniating UI.")
        print("Exitting")
        os._exit(1)

# --- GUI & UDP Server execution --- #
'''
#   Function: exec_
#   Desc: Executes and starts Panel & UDPServer with threads and async. 
'''
def exec_():
    
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
    
    # ~ Return app exit code
    return exit_code
