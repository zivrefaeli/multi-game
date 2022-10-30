# app server

# server: bind -> listen -> accept ->        SYN-ACK ->        recv -> send
# client:                   connect -> SYN ->           ACK -> send -> recv

# Connection three-way Handshake
# SYN: client sends to server
# SYN-ACK: server replies to client
# ACK: client sends to server, and starts a full-duplex communication

import socket
from methods import App
from threading import Thread

from tkinter import *
from tkinter import ttk

HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, App.PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running = True 

def handleClient(client: socket.socket, addr: tuple):
    if App.receive(client) == 'SYN':
        App.send(client, 'SYN-ACK')
        
        if App.receive(client) == 'ACK':
            print(f'connection with {addr} started!')
            print(f'[{addr}]: {App.receive(client)}')

    client.close()
    print('thread done')

def ui():
    x = Tk()
    x.title('abc')
    x.mainloop()

    global running
    running = False
    print('stop running')
    # on close send a 'closing client' to stop it! 

def main() -> None:
    server.bind(ADDR)
    server.listen(10)

    print(f'server listening on {ADDR}')
    print('waiting for a client')

    ui_thread = Thread(target=ui)
    ui_thread.start()

    while running:
        client, addr = server.accept()

        client_thread = Thread(target=handleClient, args=(client, addr))
        client_thread.start()
    print('server stopped')

if __name__ == '__main__':
    main()