from tkinter import Tk, StringVar, messagebox, Text
from tkinter.ttk import Label, Entry, Frame, Button, Scrollbar
from tkinter.constants import RIGHT, BOTTOM, HORIZONTAL, VERTICAL, Y, X, NONE, NORMAL,DISABLED, INSERT, END
import socket
from socket import gethostbyname, gethostname
from threading import Thread
from math import sqrt, degrees, radians, cos, sin, atan, floor

from objects.methods import App, Validate
from objects.packet import *
from objects.constants import Data
from objects.dot import Dot
from objects.player import Player
from objects.clone import Clone

# when client joins the server, he should send is ID
# the server should check if the ID exists, and send a response

CONNECTED_USERS = set() # list of conncted users' ids
DATABASE = dict()       # map of [id] = user data

# TODO: split server.py and client.py to seperate flies


class CreateServerUI(Tk):
    WIDTH = 350
    HEIGHT = 310
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    IP_FONT = ('Consolas', 11, 'bold')
    PORT_FONT = ('Consolas', 11)

    def __init__(self) -> None:
        super().__init__()
        # variables
        self.IP = gethostbyname(gethostname())
        self.port = StringVar()
        self.address = None

        # UI settings
        self.title('Create Server')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.iconbitmap(default='./assets/icon.ico')

        self.set_titles()
        self.set_port_input()
        self.set_create_button()

    def set_titles(self) -> None:
        title_label = Label(self, text='Multi:Game', font=self.TITLE_FONT)
        title_label.pack(pady=40)

        sub_title_label = Label(self, text='Run a server on your machine', font=self.LABEL_FONT)
        sub_title_label.pack()

        ip_frame = Frame(self)
        ip_frame.pack()

        ip_title_label = Label(ip_frame, text='Your machine IP address is', font=self.LABEL_FONT)
        ip_title_label.grid(row=0, column=0)

        ip_label = Label(ip_frame, text=self.IP, font=self.IP_FONT, background='lightblue')
        ip_label.grid(row=0, column=1)

    def set_port_input(self) -> None:
        port_frame = Frame(self)
        port_frame.pack(pady=30)

        port_label = Label(port_frame, text='Port: ', font=self.LABEL_FONT)
        port_label.grid(row=0, column=0)

        port_entry = Entry(port_frame, font=self.PORT_FONT, textvariable=self.port)
        port_entry.grid(row=0, column=1)

    def set_create_button(self) -> None:
        create_button = Button(self, text='Create Server', command=self.create_server)
        create_button.pack(ipadx=12, ipady=4)

    def create_server(self) -> None:
        result = Validate.port(self.port.get())

        if result[Validate.VALID]:
            HOST, PORT = self.IP, int(self.port.get())
            print(f'creating server on {HOST}:{PORT}')

            self.address = (HOST, PORT)
            self.destroy()
        else:
            messagebox.showwarning(title='Port validation', message=result[Validate.MESSAGE])


class ServerUI(Tk):
    WIDTH = 400 # px
    HEIGHT = 400 # px
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    IP_FONT = ('Consolas', 11, 'bold')
    USERS_CAPACITY = 10
    UI_DELAY = 300 # ms

    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__()
        self.running = True
        self.address = address

        # UI settings
        self.title('Multi:Game Server')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.iconbitmap(default='./assets/icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.set_title()
        self.set_users_frame()

        self.open_server()

    def close(self):
        self.running = False
        self.listener.stop()        
        self.destroy()

    def set_title(self) -> None:
        title_label = Label(self, text=f'The Server Is Running', font=self.TITLE_FONT)
        title_label.pack(pady=(30, 10))

        address_label = Label(self, text=f'{self.address[0]}:{self.address[1]}', font=self.IP_FONT, background='lightblue')
        address_label.pack()

    def set_users_frame(self) -> None:
        users_frame = Frame(self)
        users_frame.pack(padx=10, pady=10)

        scroll_vertical = Scrollbar(users_frame, orient=VERTICAL)
        scroll_vertical.pack(side=RIGHT, fill=Y)
        scroll_horizontal = Scrollbar(users_frame, orient=HORIZONTAL)
        scroll_horizontal.pack(side=BOTTOM, fill=X)

        self.textarea = Text(users_frame, state=DISABLED, wrap=NONE)
        self.textarea.pack()

        scroll_vertical.config(command=self.textarea.yview)
        scroll_horizontal.config(command=self.textarea.xview)
        self.textarea.configure(yscrollcommand=scroll_vertical.set)
        self.textarea.configure(xscrollcommand=scroll_horizontal.set)

    def update_textarea(self) -> None:
        self.textarea.config(state=NORMAL)
        self.textarea.delete('1.0', END)

        text = []
        for user in CONNECTED_USERS:
            if not user in DATABASE:
                continue
            user_data = DATABASE[user]
            text.append(f'{user}: {{')
            text.append(f'    position: {user_data[Data.POS]},')
            text.append(f'    angle: {user_data[Data.ANGLE]}')
            text.append('}\n')

        if len(text) == 0:
            text.append('There are no connected users')

        self.textarea.insert(INSERT, '\n'.join(text))
        self.textarea.config(state=DISABLED)

    def open_server(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(self.USERS_CAPACITY)

        self.listener = ClientsListener(self)
        self.listener.start()

        self.update_ui()

    def update_ui(self) -> None:
        if not self.running:
            return
        self.update_textarea()
        self.after(self.UI_DELAY, self.update_ui)


class ClientsListener(Thread):
    def __init__(self, ui: ServerUI) -> None:
        super().__init__()
        self.setName('Clients Listener Thread')
        self.ui = ui
        self.threads = []

    def run(self) -> None:
        server = self.ui.server

        while True:
            client, client_address = server.accept()
            print('client conected from', client_address)

            init_packet = App.receive(client)

            if init_packet.type == CLOSE_SERVER_TYPE:
                break
            
            elif init_packet.type == ID_TYPE:
                client_id = init_packet.data

                client_thread = HandleClient(client, client_address, client_id)
                client_thread.start()

                self.threads.append(client_thread)
                print('client thread started')
            else:
                print('client error')

        for thread in self.threads:
            if thread.is_alive():
                App.send(thread.client, Packet(SERVER_CLOSED_TYPE))

        server.close()
        print('server closed')

    def stop(self) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(self.ui.address)
            App.send(client, Packet(CLOSE_SERVER_TYPE))
        except Exception as e:
            print(e)
        finally:
            client.close()


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
        App.send(self.client, Packet(ID_STATUS_TYPE, status))

        if status == self.INVALID:
            print('client joined with invalid id')
            self.client.close()
            return
        CONNECTED_USERS.add(self.id)

        while True:
            packet = App.receive(self.client)

            if packet.type == ERROR_TYPE:
                break # no response
            if packet.type == DISCONNECT_TYPE:
                print(f'{self.id} disconnected from the server')
                break # no response
            if packet.type == SERVER_CLOSED_TYPE:
                print(f'[{self.id}]: server closed - dissconnecting!')
                App.send(self.client, Packet(SERVER_CLOSED_TYPE))
                break

            # TODO: calculate how match damage this client recevied - on client side !
            damage = self.get_attack()

            DATABASE[self.id] = packet.data
            App.send(self.client, Packet(self.SERVER_DATA, {
                self.CLIENTS: DATABASE,
                self.DAMAGE: damage
            }))

        print(f'deleting {self.id} data: {DATABASE.pop(self.id)}')
        CONNECTED_USERS.remove(self.id)

        self.client.close()
        print('client thread ended')

    def get_attack(self) -> int:
        attack = 0

        for id in DATABASE:
            if id == self.id:
                continue
            clone = Clone(DATABASE[id])

            i = 0
            while i < len(clone.bullets):
                bullet = clone.bullets[i]
                if self.hitbox(bullet, clone.position, clone.angle):
                    attack += 1
                    clone.bullets.pop(i)
                else:
                    i += 1

        return attack

    def hitbox(self, bullet: Dot, clone: Dot, angle: int) -> bool:
        # relative dot (a, b) to clone position as origin
        a = bullet.x - clone.x
        b = bullet.y - clone.y
        r = sqrt(a ** 2 + b ** 2)

        try:
            alpha = degrees(atan(b / a))
        except ZeroDivisionError:
            alpha = 90 if b > 0 else 270
        
        beta = radians(alpha - angle)
        x, y = round(r * cos(beta)), round(r * sin(beta))
        d = Player.SIZE / 2

        return -d <= x <= d and -d <= y <= d


def main() -> None:
    create_server_ui = CreateServerUI()
    create_server_ui.mainloop()

    if create_server_ui.address:
        server_ui = ServerUI(create_server_ui.address)
        server_ui.mainloop()


if __name__ == '__main__':
    main()