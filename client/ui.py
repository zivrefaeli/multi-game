import socket
from tkinter import StringVar, Tk, messagebox
from tkinter.ttk import Button, Entry, Frame, Label
from tkinter.constants import DISABLED, NORMAL, W
from .verify import VerifyConnection
from objects import Validate


class ClientUI(Tk):
    WIDTH = 350 # px
    HEIGHT = 350 # px
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    ENTRY_FONT = ('Consolas', 11)

    def __init__(self) -> None:
        super().__init__()
        self.verified = False

        self.ip = StringVar()
        self.port = StringVar()
        self.id = StringVar()

        self.title('Join Server')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.iconbitmap(default='./assets/icon.ico')
        
        self.set_titles()
        self.set_entries()
        self.set_join_button()

    def set_titles(self) -> None:
        title_label = Label(self, text='Multi:Game', font=self.TITLE_FONT)
        title_label.pack(pady=(40, 0))

        sub_title_label = Label(self, text='Join a Mulit:Game server', font=self.LABEL_FONT)
        sub_title_label.pack()

    def set_entries(self) -> None:
        address_frame = Frame(self)
        address_frame.pack(pady=30)

        ip_label = Label(address_frame, text='IP Address: ', font=self.LABEL_FONT)
        ip_label.grid(row=0, column=0, sticky=W)

        ip_entry = Entry(address_frame, font=self.ENTRY_FONT, textvariable=self.ip)
        ip_entry.grid(row=0, column=1)

        port_label = Label(address_frame, text='Port: ', font=self.LABEL_FONT)
        port_label.grid(row=1, column=0, sticky=W)

        port_entry = Entry(address_frame, font=self.ENTRY_FONT, textvariable=self.port)
        port_entry.grid(row=1, column=1)

        id_frame = Frame(self)
        id_frame.pack(pady=(0, 30))

        id_label = Label(id_frame, text='ID: ', font=self.LABEL_FONT)
        id_label.grid(row=1, column=0, sticky=W)

        id_entry = Entry(id_frame, font=self.ENTRY_FONT, textvariable=self.id)
        id_entry.grid(row=1, column=1)

    def set_join_button(self) -> None:
        self.join_button = Button(self, text='Join Server',command=self.join_server)
        self.join_button.pack(ipadx=12, ipady=4)

    def validate_inputs(self) -> tuple[str, int, str]:
        ip = self.ip.get()
        port = self.port.get()
        id = self.id.get()

        result = Validate.ip(ip)
        if not result[Validate.VALID]:
            messagebox.showwarning(title='IP validation', message=result[Validate.MESSAGE])
            return tuple()

        result = Validate.port(port)
        if not result[Validate.VALID]:
            messagebox.showwarning(title='Port validation', message=result[Validate.MESSAGE])
            return tuple()

        result = Validate.id(id)
        if not result[Validate.VALID]:
            messagebox.showwarning(title='Id validation', message=result[Validate.MESSAGE])
            return tuple()

        return ip, int(port), id

    def join_server(self) -> None:
        result = self.validate_inputs()
        if len(result) == 0:
            return
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.join_button.config(state=DISABLED)
        
        self.verify_conn = VerifyConnection(self.client, result)
        self.verify_conn.start()
        self.monitor()

    def monitor(self) -> None:
        if self.verify_conn.is_alive():
            self.after(500, self.monitor)
        elif self.verify_conn.verified:
            self.verified = True
            self.destroy()
        else:
            self.join_button.config(state=NORMAL)