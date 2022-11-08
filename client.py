from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import Button, Label, Frame, Entry
from tkinter.constants import W, DISABLED, NORMAL
import socket
from threading import Thread
from os import system

from objects.methods import Validate, App
from objects.packet import *
from server import HandleClient

import pygame
from pygame import display, time, mouse, event
from objects.constants import WIDTH, HEIGHT, WHITE, FPS
from objects.player import Player
from objects.clone import Clone


class ClientUI(Tk):
    WIDTH = 350
    HEIGHT = 350
    TITLE_FONT = ('Times', 20)
    LABEL_FONT = ('Calibri', 11)
    ENTRY_FONT = ('Consolas', 11)

    def __init__(self) -> None:
        super().__init__()
        self.verified = False

        self.ip = StringVar()
        self.port = StringVar()
        self.id = StringVar()

        # UI settings
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
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.join_button.config(state=DISABLED)
        
        verify_conn = VerifyConnection(self.client, result, self)
        verify_conn.start()
        self.monitor(verify_conn)

    def monitor(self, thread: Thread) -> None:
        if thread.is_alive():
            self.after(200, lambda: self.monitor(thread))
        else:
            if self.verified:
                self.destroy()


class VerifyConnection(Thread):
    def __init__(self, client: socket.socket, result: tuple[str, int, str], ui: ClientUI) -> None:
        super().__init__()
        self.client = client
        self.ip, self.port, self.id = result
        self.ui = ui

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

        self.ui.verified = True

    def on_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)
        self.ui.join_button.config(state=NORMAL)
        self.client.close()


class ClientConnection(Thread):
    DATA = 'DATA'

    def __init__(self, client: socket.socket, id: str) -> None:
        super().__init__()
        self.client = client
        self.id = id

        self.running = True
        self.player = Player(id)
        self.database = {}

        self.packet = Packet(f'{id}_{self.DATA}', self.player.json())

    def run(self) -> None:
        while self.running:
            # updates client data
            self.packet.data = self.player.json()

            App.send(self.client, self.packet)
            received_packet = App.receive(self.client)
            
            if received_packet.type == ERROR_TYPE:
                print('error occured on receive data')
                break
            if received_packet.type == SERVER_CLOSED_TYPE:
                print('server closed')
                break

            self.database = received_packet.data
            system('cls')
            print(f'Database: {self.database}')
            print(f'Ammo: {self.player.ammo}')

        try:
            if not self.running:
                App.send(self.client, Packet(DISCONNECT_TYPE))
                print('left the server')
        except Exception as e:
            print(e)
        finally:
            self.running = False
            self.client.close()


def main() -> None:
    pygame.init()
    display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)

    client_ui = ClientUI()
    client_ui.mainloop()
    if not client_ui.verified:
        pygame.quit()
        return

    connection = ClientConnection(client_ui.client, client_ui.id.get())
    connection.start()
    
    player = connection.player

    # UI settings
    display.set_caption(f'{player.id}`s screen')
    display.set_icon(player.body)
    window = display.set_mode((WIDTH, HEIGHT), flags=pygame.SHOWN)
    clock = time.Clock()

    while connection.running:
        clock.tick(FPS)
        window.fill(WHITE)

        mx, my = mouse.get_pos()

        for e in event.get():
            if e.type == pygame.QUIT:
                connection.running = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    player.accelerating = True
                    player.moving = True
                
                elif e.key == pygame.K_LSHIFT:
                    player.crouching = True
            
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    player.accelerating = False
                
                elif e.key == pygame.K_LSHIFT:
                    player.crouching = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    player.shooting = True
                elif e.button == 3:
                    player.shoot()
            
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    player.shooting = False
        
        if player.shooting:
            player.shoot()

        for clone_id in connection.database:
            if clone_id == connection.id:
                continue
            clone_json = connection.database[clone_id]
            clone = Clone(clone_json)
            clone.display(window)

        player.rotate_to((mx, my))
        player.display(window)

        display.update()

    pygame.quit()

if __name__ == '__main__':
    main()