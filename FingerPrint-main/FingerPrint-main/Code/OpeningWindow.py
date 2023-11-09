
# Imports:
from app import MainApp
from DefineFrame import DefineFrame
from Constants import *


def quit(root):
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Fingerprint")
    DefineFrame(root).pack(fill="both", expand=True)

    # code to add image of fingerprint to main window
    img = Image.open("fingerprint_main_win.png")
    w, h = int(4 * WIDTH / 5), int(2 * HEIGHT / 5)
    image = img.resize((w, h), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    px, py = int((WIDTH - w) / 2), int((HEIGHT - h) / 2)

    lab = tk.Label(root, image=photo)  # .place(x=px, y=py)
    lab.place(x=px, y=py)
    lab.photo = photo

    # code to add image of PolyGene logo to main window
    img = Image.open("polygene_logo.png")
    w, h = int(WIDTH / 5), int(HEIGHT / 11)
    image = img.resize((w, h), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    px, py = WIDTH - w, HEIGHT - h
    lab = tk.Label(root, image=photo)
    lab.place(x=px, y=py)

    root.iconbitmap("icon.ico")

    root.after(5000, root.destroy)
    root.mainloop()

    MainApp()


if __name__ == "__main__":
    main()
