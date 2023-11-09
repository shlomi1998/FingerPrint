
# Imports:
import tkinter as tk
from Constants import *
from GradientFrame import GradientFrame

class DefineFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        frame = GradientFrame(self, "#00B0F0", "#FFEFE5", borderwidth=1, relief="sunken", height=HEIGHT, width=WIDTH)
        frame.pack(fill="both", expand=True)