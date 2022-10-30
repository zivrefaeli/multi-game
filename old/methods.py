import socket
from pickle import loads, dumps

class App:
    PORT = 3001
    BUFFER = 1024 # 1KB

    @staticmethod
    def send(socket: socket.socket, data: object) -> None:
        socket.send(dumps(data))

    @staticmethod
    def receive(socket: socket.socket) -> object:
        try:
            message = b''
        
            while True:
                data = socket.recv(App.BUFFER)
                message += data
                if len(data) < App.BUFFER:
                    break

            return loads(message)
        except EOFError as e:
            print(e)
            return dict()

class Packet:
    def __init__(self, type, data) -> None:
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return f'{self.type} | {self.data}'

if __name__ == '__main__':
    file_name = __file__.split('\\')[-1]
    print(f'{file_name} is a source file')