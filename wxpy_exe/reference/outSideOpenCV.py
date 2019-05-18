import wx
import matplotlib as plt
import cv2

def __init__(self, parent, pathToImage=None):
    # Use English dialog
    self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

    # Initialise the parent
    wx.Panel.__init__(self, parent)

    # Intitialise the matplotlib figure
    # self.figure = plt.figure(facecolor='gray',figsize=(10.5, 8))
    self.figure = Figure(facecolor='gray', figsize=(10.5, 8))

    # Create an axes, turn off the labels and add them to the figure
    self.axes = plt.Axes(self.figure, [0, 0, 1, 1])

    self.axes.set_axis_off()
    self.figure.add_axes(self.axes)

    self.panel = wx.Panel(self, -1, pos=(10, 10), size=(1390, 940))

    # Add the figure to the wxFigureCanvas
    self.canvas = FigureCanvas(self.panel, -1, self.figure)

    # Height,width
    # self.picSize=wx.TextCtrl(self,-1,"",pos=(1100,800),size=(100,30),style=wx.TE_READONLY)

    # Check box
    self.check = wx.CheckBox(self.panel, -1, u"批量处理全部图片", pos=(1080, 50), size=(100, 20))
    self.check.Bind(wx.EVT_CHECKBOX, self.onCheck)

    # StaticText
    wx.StaticText(self.panel, -1, u"图像文件所在目录：", pos=(1080, 90))

    # Show dialog path
    self.pathText = wx.TextCtrl(self.panel, -1, "", pos=(1080, 130), size=(190, 30))

    # Add Button
    self.openBtn = wx.Button(self.panel, -1, u">>", pos=(1280, 130), size=(90, 30))
    self.frontBtn = wx.Button(self.panel, -1, u"上一张", pos=(1080, 830), size=(90, 50))
    self.saveBtn = wx.Button(self.panel, -1, u"保存本帧结果", pos=(1190, 830), size=(100, 50))
    self.nextBtn = wx.Button(self.panel, -1, u"下一张", pos=(1300, 830), size=(90, 50))
    self.workBtn = wx.Button(self.panel, -1, u"开始处理/暂停处理", pos=(1080, 760), size=(290, 40))
    # Progress Bar
    self.gauge = wx.Gauge(self.panel, -1, 1000, (10, 830), (1050, 50))
    # self.gauge.SetValue(2)

    # StaticText
    wx.StaticText(self.panel, -1, u"耗时：", pos=(1080, 723))
    # Show time
    self.timeText = wx.TextCtrl(self.panel, -1, "", pos=(1140, 720), size=(230, 30), style=wx.TE_READONLY)

    # Attach button with function
    self.Bind(wx.EVT_BUTTON, self.load, self.openBtn)
    self.Bind(wx.EVT_BUTTON, self.save, self.saveBtn)
    self.Bind(wx.EVT_BUTTON, self.front, self.frontBtn)
    self.Bind(wx.EVT_BUTTON, self.next, self.nextBtn)
    self.Bind(wx.EVT_BUTTON, self.work, self.workBtn)

    self.area_text = wx.TextCtrl(self, -1, u'小轿车', pos=(1080, 175), size=(290, 535), style=(wx.TE_MULTILINE))
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n大货车')
    self.area_text.AppendText('\n矩形:(1,10,10,10)')
    self.area_text.AppendText('\n矩形:(1,10,10,10)')
    self.area_text.AppendText('\n矩形:(1,10,10,10)')
    self.area_text.AppendText('\n矩形:(1,10,10,10)')
    self.area_text.AppendText('\n矩形:(1,10,10,10)')

    # Initialise the rectangle
    self.rect = Rectangle((0, 0), 0, 0, facecolor='None', edgecolor='red')
    self.x0 = None
    self.y0 = None
    self.x1 = None
    self.y1 = None
    self.axes.add_patch(self.rect)

    # The list of the picture(absolute path)
    self.fileList = []

    # Picture name
    self.picNameList = []

    # Picture index in list
    self.count = 0

    # Cut from the picture of the rectangle
    self.cut_img = None

    # Connect the mouse events to their relevant callbacks
    self.canvas.mpl_connect('button_press_event', self._onPress)
    self.canvas.mpl_connect('button_release_event', self._onRelease)
    self.canvas.mpl_connect('motion_notify_event', self._onMotion)

    # Lock to stop the motion event from behaving badly when the mouse isn't pressed
    self.pressed = False