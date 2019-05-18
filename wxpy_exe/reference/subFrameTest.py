import wx




class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(parent=None, title='摄像头展示', size=(850, 400))
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 0)
        buttonOk = wx.Button(self.panel, label="验证")
        self.Bind(wx.EVT_BUTTON, self.subFrame, buttonOk)
        sizer.Add(buttonOk, pos=(6, 5), flag=wx.TOP, border=5)
        self.panel.SetSizerAndFit(sizer)

    def subFrame(self,placeholder):
        myframe2 = MyFrame2()
        myframe2.Show(True)

class MyFrame2(wx.Frame):
    def __init__(self):
        super(MyFrame2, self).__init__(parent=None, title='摄像头展示2', size=(850, 400))

class MyApp(wx.App):
    def OnInit(self):
        self.myframe = MyFrame()

        self.SetTopWindow(self.myframe)
        self.myframe.Show(True)
        return True

if __name__=='__main__':
      app = MyApp(0)
      app.MainLoop()