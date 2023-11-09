
# Imports:
import tkinter as tk
from Constants import *

class GradientFrame(tk.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

        px, py = int(WIDTH / 17), int(HEIGHT/6)
        text_canvas = self.create_text(px, py, anchor="nw")
        self.itemconfig(text_canvas, text=text_window, font=("Arial", 28))

    '''Draw the gradient'''
    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = WIDTH
        height = HEIGHT

        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / height
        g_ratio = float(g2-g1) / height
        b_ratio = float(b2-b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)

        self.lower("gradient")

