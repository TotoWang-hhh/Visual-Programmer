import tkinter as tk
import tkintertools as tkt

class Editor(tkt.Canvas):

    '''工作区Canvas'''

    def __init__(self, master: tk.Tk | tk.Toplevel) -> None:
        super().__init__(master)
        # self.create_line(176, 10, 176, 560)
        # self.create_line(176+176+10, 340, 176+176+10+200-10-10, 340)
        self.create_rectangle(176, 0, 176+176, 580, outline="#dddddd", fill="#dddddd")
        self.create_line(176+176, 0, 176+176, 580, fill="#000000")