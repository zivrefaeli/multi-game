from socket import gethostbyname, gethostname
from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import Label, Entry, Frame, Button 
from objects import Validate


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