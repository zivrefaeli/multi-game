import socket
from threading import Thread
from objects import Player, Packet, Type, App


class ClientConnection(Thread):
    DATA = 'DATA'

    def __init__(self, client: socket.socket, id: str) -> None:
        super().__init__()
        self.setName(f'{id}`s Connection Thread')
        self.client = client
        self.id = id

        self.running = True
        self.player = Player(id)
        self.database = {}

        self.packet = Packet(f'{id}_{self.DATA}', self.player.json())

    def run(self) -> None:
        while self.running:
            # updates client data
            self.packet.data = self.player.json()

            App.send(self.client, self.packet)
            received_packet = App.receive(self.client)
            
            if received_packet.type == Type.ERROR:
                print('error occured on receive data')
                break
            if received_packet.type == Type.SERVER_CLOSED:
                print('server closed')
                break

            try:
                
                data = received_packet.data
                self.database = data['clients']
                damage = data['damage']
                self.player.health += damage
            except Exception as e:
                pass


            if self.player.health <= 0:
                self.player.health = Player.FULL_HEALTH

            # system('cls')
            # print(f'Database: {self.database}')
            print(f'Ammo: {self.player.ammo} | Damage: {damage}')

        try:
            if not self.running: # client left from pygame
                App.send(self.client, Packet(Type.DISCONNECT))
                print('left the server')
        except Exception as e:
            print(e)
        finally:
            self.running = False
            self.client.close()