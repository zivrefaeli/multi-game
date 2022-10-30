# import socket
# from methods import App, Packet
from threading import Thread

from tkinter import ttk, Tk, StringVar

# HOST = socket.gethostbyname(socket.gethostname())
# ADDR = (HOST, App.PORT)

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# running = True

# server_data = dict()

# def print_message(username: str, message: str) -> None:
#     print(f'[{username}]: {message}')

# def client_loop(client: socket.socket, addr: tuple, username: str) -> None:
#     left = False

#     while running:
#         packet = App.receive(client)
#         print_message(username, packet)

#         if packet.type == 'client-left':
#             left = True
#             del server_data[username]
#             break

#         server_data[username] = packet.data
#         App.send(client, Packet('server-data', server_data))
    
#     if not left:
#         App.receive(client)
#         App.send(client, Packet('server-closed', 'END'))
#         del server_data[username]

#     print(f'{username}`s loop closed')

# def handle_client(client: socket.socket, addr: tuple) -> None:
#     print(f'connection with {addr} started!')
#     username = App.receive(client)

#     while username in server_data.keys():
#         App.send(client, 'bad-username')
#         username = App.receive(client)

#     print_message(username, 'connected')
#     App.send(client, username)

#     client_loop(client, addr, username)

#     client.close()

# def close_server_ui() -> None:
#     def close():
#         global running
#         running = False

#         root.destroy()

#         close_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         close_client.connect(ADDR)
#         close_client.close()

#     root = Tk()
#     root.title('Server UI')
#     root.protocol('WM_DELETE_WINDOW', close)

#     button = ttk.Button(root, text='Close Server', command=close)
#     button.pack()

#     root.mainloop()

#     print('ui closed')

# def main() -> None:
#     server.bind(ADDR)
#     server.listen(10)

#     print(f'server listening on {ADDR}')

#     Thread(target=close_server_ui).start()

#     while running:
#         client, addr = server.accept()

#         if not running:
#             break

#         client_thread = Thread(target=handle_client, args=(client, addr))
#         client_thread.start()

#     print('server closed')



CLIENTS = dict()
ADDRESSES = []

def get_clients_list() -> str:
    result = []
    index = 0
    for username in CLIENTS:
        result.append(f'{username} | {ADDRESSES[index]}')
        index += 1
    return '\n'.join(result)

class ServerUI(Thread):
    def __init__(self, title) -> None:
        Thread.__init__(self)
        self.title = title
        self.size = 300

    def add(self):
        CLIENTS[f'ziv{len(ADDRESSES)}'] = { 'name': 'ziv', 'age': 18 }
        ADDRESSES.append(('10.100.102.13', 65578))
        print('clicj')
        self.clients.set(get_clients_list())

    def run(self) -> None:
        self.root = Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.size}x{self.size}")
        # self.clients = StringVar()

        # clients_label = ttk.Label(self.root, textvariable=self.clients)
        # clients_label.pack()

        btn = ttk.Button(self.root, text='click')
        btn.pack()

        self.root.mainloop()

def main():
    ui = ServerUI('Multi:Game')
    ui.start()

if __name__ == '__main__':
    main()