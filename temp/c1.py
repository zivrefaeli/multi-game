import socket, sys
from threading import Thread
from time import sleep
from methods import App, Packet
from os import system

from tkinter import Tk
from tkinter import ttk

HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, App.PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
left = False

class UI(Thread):
    # def __init__(self, username) -> None:
    #     Thread.__init__(self)
    #     self.root = Tk()
    #     self.username = username

    def close(self):
        global left
        left = True

        self.root.destroy()

    def run(self) -> None:
        self.root = Tk()
        self.root.title(f'das`s UI')

        button = ttk.Button(self.root, text='Left Server', command=self.close)
        button.pack()

        self.root.mainloop()

def exit_server_ui(usernme: str) -> None:
    root = Tk()

    def close():
        global left
        left = True

        root.destroy()

    root.title(f'{usernme}`s UI')

    button = ttk.Button(root, text='Left Server', command=close)
    button.pack()

    root.mainloop()

    print('ui closed')

def main() -> None:
    if len(sys.argv) != 2:
        file_name = __file__.split('\\')[-1]
        print('enter username as parameter')
        print(f'Usage: python {file_name} <username>')
        client.close()
        return
    else:
        username = sys.argv[1]

    try:
        client.connect(ADDR)
    except ConnectionRefusedError:
        print('server is closed')
        client.close()
        return

    data = Packet('client-data', [
        username, len(username)
    ])
    
    # Thread(target=exit_server_ui, args=(username,)).start()
    ui = UI()
    ui.start()

    App.send(client, 'SYN')
    if App.receive(client) == 'SYN-ACK':
        App.send(client, 'ACK')
        App.send(client, username)
        if App.receive(client) == username:
            print('signed to server')

            while True:
                if left:
                    App.send(client, Packet('client-left', 'LEFT'))
                    break
                else:
                    App.send(client, data)
                
                print('data from server:')
                packet = App.receive(client)

                print(packet.data)
                if packet.type == 'close-server':
                    # close ui
                    ui.close()
                    break

                sleep(1)
                # system('cls')

    client.close()

if __name__ == '__main__':
    main()