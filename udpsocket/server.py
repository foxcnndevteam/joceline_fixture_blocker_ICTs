import asyncio
from udpsocket import UDPSignals, ServerEnviroment

'''
#   Class: AsyncUDPServer
#   Desc: Creates an async server to execute in in another thread and communicate Panel.
'''
class AsyncUDPServer:

    '''
    #   Function: __init__
    #   Desc: AsyncUDPServer constructor.
    #   Arguments:
    #       signals      | type:UDPSignals | Siganals & Events to comunicate the Panel and UDP Server
    '''
    def __init__(self, signals: UDPSignals):
        self.HOST = ServerEnviroment().HOST
        self.PORT = ServerEnviroment().PORT
        self.signals = signals

    '''
    #   Class: UDPProtocol
    #   Desc: Defines the server in UDP protocol, this because TCP is slowler than UDP.
    '''
    class UDPProtocol(asyncio.DatagramProtocol):
        
        '''
        #   Function: __init__
        #   Desc: UDPProtocol constructor.
        #   Arguments:
        #       signals      | type:UDPSignals | Siganals & Events to comunicate the Panel and UDP Server
        '''
        def __init__(self, signals: UDPSignals):
            self.signals = signals

        '''
        #   Function: datagram_received
        #   Desc: Function executed when datagram is received.
        #   Arguments:
        #       data      | type:undefined | Data received in datagram (Not used)
        #       addr      | type:undefined | Addr who sends the datagram
        '''
        def datagram_received(self, data, addr):
            print(f"Señal recibida de {addr}")
            # ~ Receives an signal about test was finished and the server sends update signal to Panel.
            self.signals.update_ui.emit()

    '''
    #   Function: run_server
    #   Desc: Excutes server and waits for stop signal.
    '''
    async def run_server(self):
        # ~ Creates an loop
        loop = asyncio.get_running_loop()

        # ~ Starts an datagram endpoint to expose server
        transport, _ = await loop.create_datagram_endpoint(
            lambda: self.UDPProtocol(self.signals),
            local_addr=(self.HOST, self.PORT))
        print(f'Servidor UDP escuchando en {self.HOST}:{self.PORT}...')

        try:
            while not self.signals.stop_server.is_set():
                await asyncio.sleep(1)
        finally:
            transport.close()
            print("Servidor UDP detenido.")