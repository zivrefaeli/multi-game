import socket
from threading import Thread
from .data import *
from objects import App, Packet, Type


class HandleClient(Thread):
    VALID = 'valid'
    INVALID = 'invalid'

    SERVER_DATA = 'SERVER_DATA'
    CLIENTS = 'CLIENTS'
    DAMAGE = 'DAMAGE'

    def __init__(self, client: socket.socket, address: tuple[str, int], id: str) -> None:
        super().__init__()
        self.setName(f'{id}`s thread')
        self.client = client
        self.address = address
        self.id = id

    def run(self) -> None:
        status = self.INVALID if self.id in CONNECTED_USERS else self.VALID 
        App.send(self.client, Packet(Type.ID_STATUS, status))

        if status == self.INVALID:
            print('client joined with invalid id')
            self.client.close()
            return
        CONNECTED_USERS.add(self.id)

        while True:
            packet = App.receive(self.client)

            if packet.type == Type.ERROR:
                break # no response
            if packet.type == Type.DISCONNECT:
                print(f'{self.id} disconnected from the server')
                break # no response
            if packet.type == Type.SERVER_CLOSED:
                print(f'[{self.id}]: server closed - dissconnecting!')
                App.send(self.client, Packet(Type.SERVER_CLOSED))
                break

            # # TODO: calculate how match damage this client recevied - on client side !
            # damage = self.get_attack()

            DATABASE[self.id] = packet.data
            App.send(self.client, Packet(self.SERVER_DATA, {
                self.CLIENTS: DATABASE,
                self.DAMAGE: 1
            }))

        print(f'deleting {self.id} data: {DATABASE.pop(self.id)}')
        CONNECTED_USERS.remove(self.id)

        self.client.close()
        print('client thread ended')

    # def get_attack(self) -> int:
    #     attack = 0

    #     for id in DATABASE:
    #         if id == self.id:
    #             continue
    #         clone = Clone(DATABASE[id])

    #         i = 0
    #         while i < len(clone.bullets):
    #             bullet = clone.bullets[i]
    #             if self.hitbox(bullet, clone.position, clone.angle):
    #                 attack += 1
    #                 clone.bullets.pop(i)
    #             else:
    #                 i += 1

    #     return attack

    # def hitbox(self, bullet: Dot, clone: Dot, angle: int) -> bool:
    #     # relative dot (a, b) to clone position as origin
    #     a = bullet.x - clone.x
    #     b = bullet.y - clone.y
    #     r = sqrt(a ** 2 + b ** 2)

    #     try:
    #         alpha = degrees(atan(b / a))
    #     except ZeroDivisionError:
    #         alpha = 90 if b > 0 else 270
        
    #     beta = radians(alpha - angle)
    #     x, y = round(r * cos(beta)), round(r * sin(beta))
    #     d = Player.SIZE / 2

    #     return -d <= x <= d and -d <= y <= d