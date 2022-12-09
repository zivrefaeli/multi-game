import socket
from threading import Thread
from objects import Player, Packet, Type, App, ClientData, ServerData, Json


class ClientConnection(Thread):
    def __init__(self, client: socket.socket, id: str) -> None:
        super().__init__(name=f'{id} Connection Thread', daemon=True)
        self.client = client
        self.id = id
        self.running = True

        self.player = Player(id)
        self.clones = {}
        self.client_packet = Packet(f'{id}_DATA')

    def run(self) -> None:
        while self.running:
            self.client_packet.data = {
                ClientData.JSON: self.player.json(),
                ClientData.DAMAGE_TO: self.get_damages()
            }
            App.send(self.client, self.client_packet)

            server_packet = App.receive(self.client)
            if server_packet.type == Type.ERROR:
                print('error occurred on receive data')
                break
            if server_packet.type == Type.SERVER_CLOSED:
                print('server closed')
                break

            self.clones = server_packet.data[ServerData.CLIENTS]
            self.player.health = server_packet.data[ServerData.HEALTH]

        try:
            if not self.running: # client left from pygame
                App.send(self.client, Packet(Type.DISCONNECT))
                print('left the server')
        except Exception as e:
            print(e)
        finally:
            self.running = False
            self.client.close()

    def get_damages(self) -> dict:
        damages = {}
        for clone_id in self.clones:
            if clone_id == self.player.id:
                continue
            clone_json = self.clones[clone_id]
            damages[clone_id] = self.player.hit(clone_json[Json.POS], clone_json[Json.ANGLE])
        return damages