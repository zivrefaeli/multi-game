import socket
from threading import Thread
from tkinter import messagebox
from objects import App, Packet, Type, INVALID


class VerifyConnection(Thread):
    def __init__(self, client: socket.socket, result: tuple[str, int, str]) -> None:
        super().__init__(name='Verify Connection Thread', daemon=True)
        self.client = client
        *self.address, self.id = result
        self.verified = False

    def run(self) -> None:
        try:
            self.client.connect(tuple(self.address))
        except Exception as e:
            self.on_error('Connectivity Error', str(e))
            return
        
        App.send(self.client, Packet(Type.SEND_ID, self.id))
        response = App.receive(self.client)
        
        if response.type == Type.FULL_SERVER:
            self.on_error('Server Message', 'The server is currently full')
            return

        if response.type != Type.ID_STATUS:
            self.on_error(response.type, 'An error occurred')
            return
        
        if response.data == INVALID:
            self.on_error('Invalid Id', 'This id already exists on the server')
            return

        self.verified = True

    def on_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)
        self.client.close()