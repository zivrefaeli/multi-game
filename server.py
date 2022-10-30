from tkinter import Tk, StringVar, messagebox, Text
from tkinter.ttk import Label, Entry, Frame, Button, Scrollbar
from tkinter.constants import RIGHT, BOTTOM, HORIZONTAL, VERTICAL, Y, X, NONE, NORMAL, INSERT
import socket
from socket import gethostbyname, gethostname
from threading import Thread

from objects.methods import App, Validate
from objects.packet import *

# when client joins the server, he should send is ID
# the server should check if the ID exists, and send a response

CONNECTED_USERS = set() # list of conncted users' ids
DATABASE = dict()       # map of [id] = user data


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
    WIDTH = 400
    HEIGHT = 400
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    IP_FONT = ('Consolas', 11, 'bold')
    USERS_CAPACITY = 10

    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__()
        # variables
        self.address = address

        self.open_server()

        # UI settings
        self.title('Multi:Game Server')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.iconbitmap(default='./assets/icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.set_title()
        self.set_users_frame()

    def close(self):
        self.destroy()
        if self.running:
            self.running = False
            close_server = CloseSeverClient(self.address)
            close_server.start()

    def open_server(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(self.USERS_CAPACITY)

        self.running = True

        self.server_thread = Thread(target=self.listen_for_users)
        self.server_thread.start()

    def listen_for_users(self):
        while self.running:
            client, client_address = self.server.accept()
            print('client conected from', client_address)

            init_packet = App.receive(client)

            if init_packet.type == CLOSE_SERVER_TYPE:
                self.running = False
                App.send(client, Packet(SERVER_CLOSED_TYPE))
                print('server closed by client')
            elif init_packet.type == ID_TYPE:
                client_id = init_packet.data
                client_thread = HandleClient(client, client_address, client_id, self)
                client_thread.start()
                print('client thread started')
            else:
                print('client error')

        self.server.close()
        print('server closed')

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
        
        self.textarea = Text(users_frame, state=NORMAL, wrap=NONE)
        self.textarea.pack()

        scroll_vertical.config(command=self.textarea.yview)
        scroll_horizontal.config(command=self.textarea.xview)
        self.textarea.configure(yscrollcommand=scroll_vertical.set)
        self.textarea.configure(xscrollcommand=scroll_horizontal.set)


class CloseSeverClient(Thread):
    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__()
        self.address = address

    def run(self) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(self.address)
        except Exception as e:
            if type(e) == ConnectionRefusedError:
                print('server is closed')
            else:
                print(e)
        else:
            App.send(client, Packet(CLOSE_SERVER_TYPE))
        finally:
            client.close()


class HandleClient(Thread):
    VALID = 'valid'
    INVALID = 'invalid'

    def __init__(self, client: socket.socket, address: tuple[str, int], id: str, server_ui: ServerUI) -> None:
        super().__init__()
        self.client = client
        self.address = address
        self.id = id
        self.server_ui = server_ui

    def run(self) -> None:
        status = self.INVALID if self.id in CONNECTED_USERS else self.VALID 
        App.send(self.client, Packet(ID_STATUS_TYPE, status))
        if status == self.INVALID:
            return
        CONNECTED_USERS.add(self.id)
        
        self.server_ui.textarea.insert(INSERT, f'{self.id}\n')

        while self.server_ui.running:
            packet = App.receive(self.client)
            if packet.type == ERROR_TYPE:
                break

            DATABASE[self.id] = packet.data
            App.send(self.client, Packet('DATABASE', DATABASE))

        # remove client from server's data
        print(f'deleting {self.id} data: {DATABASE.pop(self.id)}')
        CONNECTED_USERS.remove(self.id)

        print('client thread ended')


def main() -> None:
    create_server_ui = CreateServerUI()
    create_server_ui.mainloop()

    if create_server_ui.address:
        server_ui = ServerUI(create_server_ui.address)
        server_ui.mainloop()


if __name__ == '__main__':
    main()