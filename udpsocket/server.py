import asyncio
from udpsocket import UDPSignals, ServerEnviroment

class AsyncUDPServer:
    
    def __init__(self, signals: UDPSignals):
        self.HOST = ServerEnviroment().HOST
        self.PORT = ServerEnviroment().PORT
        self.signals = signals

    class UDPProtocol(asyncio.DatagramProtocol):
        def __init__(self, signals: UDPSignals):
            self.signals = signals

        def datagram_received(self, data, addr):
            print(f"Señal recibida de {addr}")
            self.signals.update_ui.emit()

    async def run_server(self):
        loop = asyncio.get_running_loop()

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