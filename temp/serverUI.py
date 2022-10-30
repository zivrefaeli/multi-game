from threading import Thread
from time import sleep
from tkinter import Tk, ttk

class UI(Thread):
    def __init__(self, title: str = 'UI', size: int = 300) -> None:
        super().__init__()
        self.title = title
        self.size = size

    def close(self) -> None:
        self.root.quit()

    def run(self) -> None:
        self.root = Tk()
        self.root.title(self.title)
        self.root.geometry(f'{self.size}x{self.size}')

        label = ttk.Label(self.root, text='Server UI', font=('Times', 20))
        label.pack(pady=16)

        button = ttk.Button(self.root, text='start server', command=self.close)
        button.pack()

        self.root.mainloop()

def main() -> None:
    ui = UI(title='Server UI')
    ui.start()

if __name__ == '__main__':
    main()