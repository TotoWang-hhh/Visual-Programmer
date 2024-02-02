import tkintertools as tkt
import tkinter as tk
from tkintertools.main import Tk, Toplevel

class Editor(tkt.Canvas):

    '''工作区Canvas'''

    def __init__(self, master: Tk | Toplevel, width: int, height: int, x: int | None = None, y: int | None = None, *, lock: bool = True, expand: bool = True, keep: bool = False, **kw) -> None:
        super().__init__(master, width, height, x, y, lock=lock, expand=expand, keep=keep, **kw)
        # self.create_line(176, 10, 176, 560)
        # self.create_line(176+176+10, 340, 176+176+10+200-10-10, 340)
        self.create_rectangle(176, 0, 176+176, 580, outline="#dddddd", fill="#dddddd")
        self.create_line(176+176, 0, 176+176, 580, fill="#000000")