
import tkinter as tk
from PIL import Image, ImageTk
from app import MainApp



HEIGHT = 650
WIDTH = 700

HEIGHT2 = 500
WIDTH2 = 500
text_window = "Digital Fingerprint Sweat-Pore Analysis"


class DefineFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        frame = GradientFrame(self, "#00B0F0", "#FFEFE5", borderwidth=1, relief="sunken", height=HEIGHT, width=WIDTH)
        frame.pack(fill="both", expand=True)


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


def quit():
    root.destroy()


root = tk.Tk()
root.title("Fingerprint")
DefineFrame(root).pack(fill="both", expand=True)

# code to add image of fingerprint to main window
img = Image.open("fingerprint_main_win.png")
w, h = int(4*WIDTH/5), int(2*HEIGHT/5)
image = img.resize((w, h), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
px, py = int((WIDTH - w)/2), int((HEIGHT - h)/2)

lab = tk.Label(root, image=photo)#.place(x=px, y=py)
lab.place(x=px, y=py)
lab.photo = photo

# code to add image of PolyGene logo to main window
img = Image.open("polygene_logo.png")
w, h = int(WIDTH/5), int(HEIGHT/11)
image = img.resize((w, h), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
px, py = WIDTH - w, HEIGHT - h
lab = tk.Label(root, image=photo)
lab.place(x=px, y=py)

root.after(5000, root.destroy)
root.mainloop()

MainApp()




