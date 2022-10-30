import socket
from methods import App, Packet
from threading import Thread

from tkinter import Tk
from tkinter import ttk

HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, App.PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running = True

server_data = dict()

def print_message(username: str, message: str) -> None:
    print(f'[{username}]: {message}')

def client_loop(client: socket.socket, addr: tuple, username: str) -> None:
    left = False

    while running:
        packet = App.receive(client)
        print_message(username, packet)

        if packet.type == 'client-left':
            left = True
            del server_data[username]
            break

        server_data[username] = packet.data
        App.send(client, Packet('server-data', server_data))
    
    if not left:
        App.receive(client)
        App.send(client, Packet('server-closed', 'END'))
        del server_data[username]

    print(f'{username}`s loop closed')

def handle_client(client: socket.socket, addr: tuple) -> None:
    print(f'connection with {addr} started!')
    username = App.receive(client)

    while username in server_data.keys():
        App.send(client, 'bad-username')
        username = App.receive(client)

    print_message(username, 'connected')
    App.send(client, username)

    client_loop(client, addr, username)

    client.close()

def close_server_ui() -> None:
    def close():
        global running
        running = False

        root.destroy()

        close_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_client.connect(ADDR)
        close_client.close()

    root = Tk()
    root.title('Server UI')
    root.protocol('WM_DELETE_WINDOW', close)

    button = ttk.Button(root, text='Close Server', command=close)
    button.pack()

    root.mainloop()

    print('ui closed')

def main() -> None:
    server.bind(ADDR)
    server.listen(10)

    print(f'server listening on {ADDR}')

    Thread(target=close_server_ui).start()

    while running:
        client, addr = server.accept()

        if not running:
            break

        client_thread = Thread(target=handle_client, args=(client, addr))
        client_thread.start()

    print('server closed')

if __name__ == '__main__':
    main()