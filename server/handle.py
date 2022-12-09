import socket
from threading import Thread
from .data import *
from objects import App, Packet, Type, Player, ServerData, ClientData, VALID, INVALID 


class HandleClient(Thread):
    def __init__(self, client: socket.socket, id: str) -> None:
        super().__init__(name=f'Handle {id} Thread', daemon=True)
        self.client = client
        self.id = id
        
        self.server_packet = Packet('SERVER_DATA')

    def run(self) -> None:
        status = INVALID if self.id in CONNECTED_CLIENTS else VALID
        App.send(self.client, Packet(Type.ID_STATUS, status))

        if status == INVALID:
            print('client joined with invalid id')
            self.client.close()
            return
        CONNECTED_CLIENTS.add(self.id)
        CLIENTS_HEALTH[self.id] = Player.FULL_HEALTH

        while True:
            client_packet = App.receive(self.client)
            if client_packet.type == Type.ERROR:
                break # no response
            if client_packet.type == Type.DISCONNECT:
                print(f'{self.id} disconnected from the server')
                break # no response
            if client_packet.type == Type.SERVER_CLOSED:
                print(f'[{self.id}]: server closed - disconnecting!')
                App.send(self.client, Packet(Type.SERVER_CLOSED))
                break

            CLIENTS_DATA[self.id] = client_packet.data[ClientData.JSON]
            damage_to = client_packet.data[ClientData.DAMAGE_TO]

            for id in damage_to:
                if id not in CLIENTS_HEALTH: # if client left, you can't shoot him
                    continue
                CLIENTS_HEALTH[id] -= damage_to[id]
                if CLIENTS_HEALTH[id] <= 0:
                    CLIENTS_HEALTH[id] = Player.FULL_HEALTH

            self.server_packet.data = {
                ServerData.CLIENTS: CLIENTS_DATA,
                ServerData.HEALTH: CLIENTS_HEALTH[self.id]
            }
            App.send(self.client, self.server_packet)

        if self.id in CLIENTS_DATA:
            print(f'deleting {self.id} data: {CLIENTS_DATA.pop(self.id)}')
        CLIENTS_HEALTH.pop(self.id)
        CONNECTED_CLIENTS.remove(self.id)

        self.client.close()
        print('client thread ended')