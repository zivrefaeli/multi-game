import socket
from threading import Thread

from tkinter import messagebox

from objects.packet import *
from objects.methods import App

from server_user import HandleClient

class VerifyConnection(Thread):
    def __init__(self, client: socket.socket, result: tuple[str, int, str]) -> None:
        super().__init__()
        self.setName('Verify Connection Thread')
        self.client = client
        self.ip, self.port, self.id = result
        self.verified = False

    def run(self) -> None:
        try:
            self.client.connect((self.ip, self.port))
        except Exception as e:
            self.on_error('Connectivity Error', str(e))
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

        self.verified = True

    def on_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)
        self.client.close()
