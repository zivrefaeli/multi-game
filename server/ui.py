import socket
from tkinter import Tk, Text
from tkinter.ttk import Label, Frame, Scrollbar
from tkinter.constants import RIGHT, BOTTOM, HORIZONTAL, VERTICAL, Y, X, NONE, DISABLED, NORMAL, END, INSERT
from .listener import ClientsListener
from .data import *
from objects import Json


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
        self.textarea.delete('1.0', END) # clear text

        text = []
        for user in CONNECTED_USERS:
            if not user in DATABASE:
                continue
            user_data = DATABASE[user]
            text.append(f'{user}: {{')
            text.append(f'    position: {user_data[Json.POS]},')
            text.append(f'    angle: {user_data[Json.ANGLE]}')
            text.append('}\n')

        if len(text) == 0:
            text.append('There are no connected users')

        self.textarea.insert(INSERT, '\n'.join(text))
        self.textarea.config(state=DISABLED)

    def open_server(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(self.USERS_CAPACITY)

        self.listener = ClientsListener(self.server)
        self.listener.start()

        self.update_ui()

    def update_ui(self) -> None:
        if not self.running:
            return
        self.update_textarea()
        self.after(self.UI_DELAY, self.update_ui)