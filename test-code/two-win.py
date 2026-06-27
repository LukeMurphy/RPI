import tkinter as tk
from tkinter import ttk
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import Text
from tkinter import Button
from tkinter import END
from tkinter import OUTSIDE
from tkinter import RIGHT
from tkinter import BOTH
from tkinter import font

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x100")
        self.title("Toplevel Window")

        self.Txt = Text(self, height=1, width=32, bg="white", fg="black", bd=False, padx=4, pady=4)
        self.Txt.place(bordermode=OUTSIDE, x=2, y=2)


        ttk.Button(self, text="Close", command=self.destroy).pack(expand=True)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("Main Window")

        # place a button on the root window
        ttk.Button(self, text="Open a window", command=self.open_window).pack(expand=True)
        ttk.Button(self, text="SEND", command=self.msg_window).pack(expand=True)

    def msg_window(self):
        self.window.Txt.insert(1.0,"foo")

    def open_window(self):
        self.window = Window(self)
        self.window2 = Window(self)
        self.window.grab_release()
        self.window2.grab_release()
        # window.grab_set()
        # window2.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
