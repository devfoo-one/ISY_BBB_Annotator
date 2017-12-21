# http://effbot.org/tkinterbook/tkinter-application-windows.htm
from enum import Enum
from tkinter import *
from PIL import Image, ImageTk


class OperationMode(Enum):  # ENUM FOR APPSTATE
    SETPOINT1 = 1
    SETPOINT2 = 2


class App:
    CURRENT_EDITMODE = OperationMode.SETPOINT1
    CURRENT_CROSSHAIR_COLOR = 'red'
    CURRENT_FINAL_QUADS = []
    CURRENT_LASTPOINT = None

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.imgViewCanvas = Canvas(frame, cnf={"width": 1000, "height": 750})
        self.imgViewCanvas.pack(side=LEFT)
        self.imgViewCanvas.bind('<Motion>', self.imgViewCanvasMouseMove)
        self.imgViewCanvas.bind('<ButtonRelease-1>', self.imgViewCanvasMouseClick)
        self.loadPicture('/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/INCOMING/17-12-20 17-57-02 0100.jpg')
        # TODO: Add Status Bar
        # TODO: Add input for brand
        # TODO: Add checkbox for openstate

    def imgViewCanvasMouseMove(self, event):
        self.redrawCrosshair(event.x, event.y)
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT2:
            self.imgViewCanvas.delete('bb_preview')
            self.imgViewCanvas.create_rectangle(self.CURRENT_LASTPOINT[0], self.CURRENT_LASTPOINT[1], event.x, event.y,
                                                outline='green yellow', width=1, tag='bb_preview')

    def imgViewCanvasMouseClick(self, event):
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT1:
            self.CURRENT_CROSSHAIR_COLOR = 'green yellow'
            self.CURRENT_EDITMODE = OperationMode.SETPOINT2
            self.addNewPoint(event.x, event.y)
            self.redrawCrosshair(event.x, event.y)
            return
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT2:
            self.CURRENT_CROSSHAIR_COLOR = 'red'
            self.CURRENT_EDITMODE = OperationMode.SETPOINT1
            self.addNewPoint(event.x, event.y)
            self.redrawCrosshair(event.x, event.y)
            return

    def redrawCrosshair(self, x, y):
        self.imgViewCanvas.delete('crosshair')
        self.imgViewCanvas.create_line(x, 0, x, self.imgViewCanvas.winfo_height(), fill=self.CURRENT_CROSSHAIR_COLOR,
                                       width=1, tag='crosshair')
        self.imgViewCanvas.create_line(0, y, self.imgViewCanvas.winfo_width(), y, fill=self.CURRENT_CROSSHAIR_COLOR,
                                       width=1, tag='crosshair')

    def addNewPoint(self, x, y):
        self.CURRENT_LASTPOINT = (x, y)
        self.imgViewCanvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='green yellow', width=0)

    def loadPicture(self, path):
        im = Image.open(path)
        # TODO: rotate image according to exif data
        im = im.resize((1000, 750), resample=Image.LANCZOS)
        self.imgViewCanvas.image = ImageTk.PhotoImage(im)
        self.imgViewCanvas.create_image(0, 0, anchor='nw', image=self.imgViewCanvas.image)


root = Tk()
app = App(root)
root.mainloop()
root.destroy()
