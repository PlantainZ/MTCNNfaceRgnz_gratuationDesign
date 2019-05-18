import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 0)
        #垂直gap,水平gap

        text = wx.StaticText(panel, label="Name:")
        sizer.Add(text, pos=(0, 0), flag=wx.ALL, border=5)
        #flag参数与border参数结合指定边距宽度
        #wx.LEFT ，左边距
        # wx.RIGHT，右边距
        # wx.BOTTOM，底边距
        # wx.TOP，上边距
        # wx.ALL，上下左右四个边距
        # 可以结合  | 来联合使用

        #此外，flag参数还可以与proportion参数结合，指定控件本身的对齐（排列）方式，包括以下选项：
        # wx.ALIGN_LEFT 左边固定，右边扩展（当proportion >0 时，下同)
        # wx.ALIGN_RIGHT 右边不动
        # wx.ALIGN_TOP
        # wx.ALIGN_BOTTOM
        # wx.ALIGN_CENTER_VERTICAL
        # wx.ALIGN_CENTER_HORIZONTAL
        # wx.ALIGN_CENTER
        # 此外，flag参数可以使用wx.EXPAND标志，那么所添加控件将占有sizer定位方向的方向上所有可用的空间。

        tc = wx.TextCtrl(panel)
        sizer.Add(tc, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)


        text1 = wx.StaticText(panel, label="address")
        sizer.Add(text1, pos=(1, 0), flag=wx.ALL, border=5)
        tc1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(tc1, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)

        text2 = wx.StaticText(panel, label="age")
        sizer.Add(text2, pos=(2, 0), flag=wx.ALL, border=5)

        tc2 = wx.TextCtrl(panel)
        sizer.Add(tc2, pos=(2, 1), flag=wx.ALL, border=5)

        text3 = wx.StaticText(panel, label="Mob.No")
        sizer.Add(text3, pos=(2, 2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        tc3 = wx.TextCtrl(panel)
        sizer.Add(tc3, pos=(2, 3), flag=wx.EXPAND | wx.ALL, border=5)

        text4 = wx.StaticText(panel, label="Description")
        sizer.Add(text4, pos=(3, 0), flag=wx.ALL, border=5)

        tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(tc4, pos=(3, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)
        sizer.AddGrowableRow(3)
        #注意这个pos和span的使用方式

        buttonOk = wx.Button(panel, label="Ok")
        buttonClose = wx.Button(panel, label="Close")

        sizer.Add(buttonOk, pos=(4, 2), flag=wx.ALL, border=5)
        sizer.Add(buttonClose, pos=(4, 3), flag=wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)


app = wx.App()
Example(None, title='GridBag Demo - www.yiibai.com')
app.MainLoop()
