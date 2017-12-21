# http://effbot.org/tkinterbook/tkinter-application-windows.htm

from tkinter import *
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.imgViewCanvas = Canvas(frame, cnf={"width": 1000, "height": 750})
        self.imgViewCanvas.pack(side=LEFT)
        self.imgViewCanvas.bind('<Motion>', self.updateCrosshair)
        self.loadPicture('/home/devfoo/Nextcloud/ISY_BBB/images/INCOMING/test.jpg')
        # TODO: Add Status Bar
        # TODO: Add input for brand
        # TODO: Add checkbox for openstate

    def updateCrosshair(self, event):
        self.imgViewCanvas.delete('crosshair')
        self.imgViewCanvas.create_line(event.x, 0, event.x, 750, fill='red', width=1, tag='crosshair')
        self.imgViewCanvas.create_line(0, event.y, 1000, event.y, fill='red', width=1, tag='crosshair')

    def loadPicture(self, path):
        im = Image.open(path)
        # TODO: rotate image according to exif data
        im = im.resize((1000,750), resample=Image.LANCZOS)
        self.imgViewCanvas.image = ImageTk.PhotoImage(im)
        self.imgViewCanvas.create_image(0, 0, anchor='nw', image=self.imgViewCanvas.image)


root = Tk()
app = App(root)
root.mainloop()
root.destroy()
