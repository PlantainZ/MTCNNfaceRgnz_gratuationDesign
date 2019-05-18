import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(300, 250))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(3, 2, 10, 10)
        #三行、两列，横坐标方向的组件距离，纵坐标的组件距离

        title = wx.StaticText(panel, label="Title")
        author = wx.StaticText(panel, label="Name of the Author")
        review = wx.StaticText(panel, label="Review")

        tc1 = wx.TextCtrl(panel)
        tc2 = wx.TextCtrl(panel)
        tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs.AddMany([(title), (tc1, 1, wx.EXPAND), (author),
                     (tc2, 1, wx.EXPAND), (review, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])
        #小心它只能被压缩成一维数组

        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)
        #第二个参数是proportion增长。

        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)


app = wx.App()
Example(None, title='FlexiGrid Demo - www.yiibai.com')
app.MainLoop()