import wx
import pyautogui
from PIL import Image

global selectionOffset, selectionSize

selectionOffset = ""
selectionSize = ""

x1 = x2 = y1 = y2 = 0


class SelectableFrame(wx.Frame):

    c1 = None
    c2 = None

    def __init__(self, parent=None, id=wx.ID_ANY, title=""):
        wx.Frame.__init__(self, parent, id, title, size=wx.DisplaySize())
        print("Size: ", wx.DisplaySize())
        self.menubar = wx.MenuBar(wx.MB_DOCKABLE)
        self.filem = wx.Menu()
        self.filem.Append(wx.ID_EXIT, '&Transparency')
        self.menubar.Append(self.filem, '&File')
        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MENU, self.OnTrans)

        # flash occurs here
        self.ShowFullScreen(True)
        # self.Maximize(True)


        print("TEST")
        # flash occurs here
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.Show()
        self.transp = False
        wx.CallLater(250, self.OnTrans, None)
        count = wx.Display.GetCount()
        print("Count: ",count)
        d = wx.Display(1)
        size = d.GetGeometry()
        # Size:  (0, 0, 2560, 1440)
        # "Size:  (-864, 0, 864, 1536)"
        print("Size: ",size)

    def OnTrans(self, event):
        if self.transp == False:
            self.SetTransparent(20)
            self.transp = True
        else:
            self.SetTransparent(255)
            self.transp = False
    
    
    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.Refresh()

    def OnMouseDown(self, event):
        self.c1 = event.GetPosition()

    def OnMouseUp(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        self.Destroy()

    def OnPaint(self, event):
        global selectionOffset, selectionSize
        global x1,x2,y1,y2

        if self.c1 is None or self.c2 is None: return

        # dc stands for device context
        # https://wiki.wxpython.org/PenAndBrushStyles

        pdc = wx.PaintDC(self)

        dc = wx.GCDC(pdc)
        # dc.SetPen(wx.Pen('red', 5))
        # # https://wxpython.org/Phoenix/docs/html/wx.BrushStyle.enumeration.html#wx-brushstyle
        # dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255), wx.SOLID))
  
                    
        r, g, b = 255,255,255
        penclr   = wx.Colour(r, g, b, wx.ALPHA_OPAQUE)
        brushclr = wx.Colour(r, g, b, 255)   # half transparent
        dc.SetPen(wx.Pen(penclr))
        dc.SetBrush(wx.Brush(brushclr))

        # SOLIDE
        # print("Wx.Transparent: ", wx.TRANSPARENT) #106

        dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)
        selectionOffset = str(self.c1.x) + "x" + str(self.c1.y)
        selectionSize = str(abs(self.c2.x - self.c1.x)) + "x" + str(abs(self.c2.y - self.c1.y))

        x1 = self.c1.x
        y1 = self.c1.y
        x2 = abs(self.c2.x - self.c1.x)
        y2 = abs(self.c2.y - self.c1.y)

    def PrintPosition(self, pos):
        return str(pos.x) + "x" + str(pos.y)


class MyApp(wx.App):

    def OnInit(self):
        frame = SelectableFrame()

        return True


app = MyApp(redirect=False)
app.MainLoop()
print("offset: " + selectionOffset + ". Screen selection size: " + selectionSize)
# print(x1," ",y1, " ", x2, " ", y2)
print("x1: ",x1)
print("y1: ",y1)
print("x2: ",x2)
print("y2: ",y2)
im = pyautogui.screenshot(region=(x1,y1, x2, y2)) # + 100
im.save("my_screenshot.png")

im.save(r"C:\Users\vvarf\Desktop\screenshot1.png")

im = Image.open(r"C:\Users\vvarf\Desktop\screenshot1.png") 
  
im.show()


# from pynput import mouse

# class MyException(Exception):pass

# NumberOfMouseClicks = 0

# def on_click(x, y, button, pressed):
#     global NumberOfMouseClicks
#     print(x, y)
#     NumberOfMouseClicks = NumberOfMouseClicks + 1
#     if (NumberOfMouseClicks==25):
#         raise MyException(button)

# with mouse.Listener(on_click=on_click) as listener:
#     try:
#         listener.join()
#     except MyException as e:
#         pass