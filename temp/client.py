# app client

# server: bind -> listen -> accept ->        SYN-ACK ->        recv -> send
# client:                   connect -> SYN ->           ACK -> send -> recv

# Connection three-way Handshake
# SYN: client sends to server
# SYN-ACK: server replies to client
# ACK: client sends to server, and starts a full-duplex communication

import socket
from methods import App

HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, App.PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main() -> None:
    try:
        client.connect(ADDR)
    except ConnectionRefusedError:
        print('server is closed')
        client.close()
        return

    App.send(client, 'SYN')
    if App.receive(client) == 'SYN-ACK':
        App.send(client, 'ACK')

        print('signed to server')
        App.send(client, 'abcdefg')

    client.close()

if __name__ == '__main__':
    main()