import socket
from threading import Thread
from .handle import HandleClient
from objects import App, Packet, Type


class ClientsListener(Thread):
    def __init__(self, server: socket.socket) -> None:
        super().__init__()
        self.setName('Clients Listener Thread')
        self.server = server
        self.address = self.server.getsockname()
        self.clients_threads: list[HandleClient] = []

    def run(self) -> None:
        while True:
            client, client_address = self.server.accept()
            print('client conected from', client_address)

            init_packet = App.receive(client)

            if init_packet.type == Type.CLOSE_SERVER:
                break
            
            elif init_packet.type == Type.SEND_ID:
                client_id = str(init_packet.data)

                client_thread = HandleClient(client, client_id)
                client_thread.start()

                self.clients_threads.append(client_thread)
                print('client thread started')
            
            else:
                print('client error')

        for thread in self.clients_threads:
            if thread.is_alive():
                App.send(thread.client, Packet(Type.SERVER_CLOSED))

        self.server.close()
        print('server closed')

    def stop(self) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(self.address)
            App.send(client, Packet(Type.CLOSE_SERVER))
        except Exception as e:
            print(e)
        finally:
            client.close()