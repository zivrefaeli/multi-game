from tkinter import Tk, StringVar
from tkinter.ttk import Button, Label, Frame, Entry
from tkinter.constants import W


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
        func = lambda: print(self.ip.get(), self.port.get(), self.id.get())

        join_button = Button(self, text='Join Server',command=func)
        join_button.pack(ipadx=12, ipady=4)


def main() -> None:
    client_ui = ClientUI()
    client_ui.mainloop()


if __name__ == '__main__':
    main()