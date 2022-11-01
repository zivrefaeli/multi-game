from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import Button, Label, Frame, Entry
from tkinter.constants import W, DISABLED, NORMAL
import socket
from threading import Thread
from time import sleep

from objects.methods import Validate, App
from objects.packet import Packet, ID_TYPE, ID_STATUS_TYPE, ERROR_TYPE, DISCONNECT_TYPE
from server import HandleClient


class ClientUI(Tk):
    WIDTH = 350
    HEIGHT = 350
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    ENTRY_FONT = ('Consolas', 11)

    def __init__(self) -> None:
        super().__init__()

        self.ip = StringVar()
        self.port = StringVar()
        self.id = StringVar()

        # UI settings
        self.title('Join Server')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.iconbitmap(default='./assets/icon.ico')
        
        # TODO: TEMP
        self.protocol('WM_DELETE_WINDOW', self.close)

        self.set_titles()
        self.set_entries()
        self.set_join_button()

    # TEMP method
    def close(self) -> None:
        self.destroy()
        self.connection.disconnect()

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
            return None

        result = Validate.port(port)
        if not result[Validate.VALID]:
            messagebox.showwarning(title='Port validation', message=result[Validate.MESSAGE])
            return None

        result = Validate.id(id)
        if not result[Validate.VALID]:
            messagebox.showwarning(title='Id validation', message=result[Validate.MESSAGE])
            return None

        return ip, int(port), id

    def join_server(self) -> None:
        result = self.validate_inputs()
        if not result:
            return
        self.join_button.config(state=DISABLED)
        self.connection = ClientConnection(result, self.join_button)
        self.connection.start()


class ClientConnection(Thread):
    def __init__(self, result: tuple[str, int, str], button: Button) -> None:
        super().__init__()
        self.ip, self.port, self.id = result
        self.button = button

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def run(self) -> None:
        try:
            self.client.connect((self.ip, self.port))
        except Exception as e:
            self.on_error('Connectivity  Error', str(e))
            return
        
        App.send(self.client, Packet(ID_TYPE, self.id))
        response = App.receive(self.client)
        
        if response.type != ID_STATUS_TYPE:
            self.on_error(response.type, 'An error occurred')
            return
        
        status = response.data
        if status == HandleClient.INVALID:
            self.on_error('Invalid Id', 'This id already exists on the server')
            return

        self.loop()

    def loop(self) -> None:
        count = 0
        
        while self.running:
            count += 1

            App.send(self.client, Packet('DATA', {'id': self.id, 'value': count}))
            packet = App.receive(self.client)
            if packet.type == ERROR_TYPE:
                print('error occured on receive data')
                break
            print(f'DATABASE: {packet.data}')

            sleep(1)

        # TODO: TEMP
        if self.running:
            self.disconnect()
        self.client.close()

    def on_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)
        self.client.close()
        self.button.config(state=NORMAL)

    def disconnect(self) -> None:
        self.running = False
        App.send(self.client, Packet(DISCONNECT_TYPE))


def main() -> None:
    client_ui = ClientUI()
    client_ui.mainloop()


if __name__ == '__main__':
    main()