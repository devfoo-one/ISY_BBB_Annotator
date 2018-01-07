# http://effbot.org/tkinterbook/tkinter-application-windows.htm
import glob
from enum import Enum
from random import randint
from tkinter import *
from PIL import Image, ImageTk
import img_rotate

IMAGE_DIMENSIONS = (1000, 750)  # SET TARGET DIMENSIONS HERE
PATHS = {
    'incoming': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/INCOMING/',
    'processed': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/INCOMING/PROCESSED',
    'final': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL'
}


def getRandomPicturePathFromPath(path):
    image_paths = list(glob.glob(path + '/*.jpg'))
    if len(image_paths) != 0:
        return image_paths[randint(0, len(image_paths))]  # TODO implement random
    else:
        return None
    # return PATHS['incoming'] + '17-12-20 17-57-02 0100.jpg'  #TODO IMPLEMENT ME


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
        self.imgViewCanvas = Canvas(frame, cnf={"width": IMAGE_DIMENSIONS[0], "height": IMAGE_DIMENSIONS[1]})
        self.imgViewCanvas.pack(side=LEFT)
        self.imgViewCanvas.bind('<Motion>', self.imgViewCanvasMouseMove)
        self.imgViewCanvas.bind('<ButtonRelease-1>', self.imgViewCanvasMouseClick)
        master.bind('<KeyPress-n>', self.next)
        master.bind('<KeyPress-N>', self.next)
        self.loadPicture(getRandomPicturePathFromPath(PATHS['incoming']))
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

    def next(self, event):
        # finalize current progress and load next pic
        self.loadPicture(getRandomPicturePathFromPath(PATHS['incoming']))
        # TODO IMPLEMENT ME
        return

    def loadPicture(self, path):
        im = Image.open(path)
        im, _ = img_rotate.fix_orientation(im)
        im = im.resize(IMAGE_DIMENSIONS, resample=Image.LANCZOS)
        self.imgViewCanvas.image = ImageTk.PhotoImage(im)
        self.imgViewCanvas.create_image(0, 0, anchor='nw', image=self.imgViewCanvas.image)


root = Tk()
app = App(root)
root.mainloop()
root.destroy()
