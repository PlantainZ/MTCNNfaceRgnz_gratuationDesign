import wx
import wx.aui

#在顶层框架投入浮动窗口
class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(300, 300))

        self.mgr = wx.aui.AuiManager(self)

        pnl = wx.Panel(self)
        pbox = wx.BoxSizer(wx.HORIZONTAL)
        text1 = wx.TextCtrl(pnl, -1, "Dockable", style=wx.NO_BORDER | wx.TE_MULTILINE)
        pbox.Add(text1, 1, flag=wx.EXPAND)
        pnl.SetSizer(pbox)

        info1 = wx.aui.AuiPaneInfo().Bottom()
        self.mgr.AddPane(pnl, info1)
        #使用这种PanelInfo，所设计的面板添加到管理器对象。
        #这个pnl是放到了下边的

        panel = wx.Panel(self)
        #这里是顶层窗口的其它部件
        text2 = wx.TextCtrl(panel, size=(300, 200), style=wx.NO_BORDER | wx.TE_MULTILINE)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(text2, 1, flag=wx.EXPAND)

        panel.SetSizerAndFit(box)
        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Show(True)

    def OnClose(self, event):
        self.mgr.UnInit()
        self.Destroy()


app = wx.App()
Mywin(None, "Dock Demo - www.yiibai.com")
app.MainLoop()
