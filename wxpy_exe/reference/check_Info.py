import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,size=(470,320))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 0)

        text = wx.StaticText(panel, label="用户名:")
        sizer.Add(text, pos=(0, 0), flag=wx.ALL, border=5)
        #如果想要只读:在TextCtrl后边加上 style = wx.TE_READONLY
        tc = wx.TextCtrl(panel,value="只读测试",style=wx.TE_CENTER)
        sizer.Add(tc, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        text1 = wx.StaticText(panel,label="用户账号")
        sizer.Add(text1, pos=(1, 0), flag=wx.ALL, border=5)

        tc1 = wx.TextCtrl(panel,value="只读测试",style=wx.TE_CENTER)
        sizer.Add(tc1, pos=(1, 1), span=(1,2), flag=wx.EXPAND | wx.ALL, border=5)
        #span=(1, 3),, style=wx.TE_MULTILINE
        text2 = wx.StaticText(panel, label="登陆密码")
        sizer.Add(text2, pos=(2, 0), flag=wx.ALL, border=5)

        tc2 = wx.TextCtrl(panel,value="只读测试",style=wx.TE_CENTER)
        sizer.Add(tc2, pos=(2, 1), span=(1,2), flag=wx.EXPAND |wx.ALL, border=5)

        #这个是所在班级栏====================================================
        text3 = wx.StaticText(panel, label="所在班级")
        sizer.Add(text3, pos=(3, 0), flag= wx.ALL, border=5)

        tc3 = wx.TextCtrl(panel,value="只读测试",style=wx.TE_CENTER)
        sizer.Add(tc3, pos=(3, 1), flag= wx.ALL, border=5)
        #================================================================= wx.EXPAND|wx.ALIGN_CENTER |

        text4 = wx.StaticText(panel, label="备注")
        sizer.Add(text4, pos=(4, 0), flag=wx.ALL, border=5)

        tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE,value="只读测试")
        sizer.Add(tc4, pos=(4, 1), span=(2, 3), flag=wx.EXPAND | wx.ALL, border=5)
        # sizer.AddGrowableRow(3)#表示空三行的意思。

        ImgChange = wx.Button(panel, label="用户图像")
        buttonOk = wx.Button(panel, label="保存修改")
        buttonClose = wx.Button(panel, label="关闭")
        buttonClose.Bind(wx.EVT_BUTTON, self.closeWin)


        sizer.Add(ImgChange, pos=(6, 1), flag=wx.ALL, border=5)
        sizer.Add(buttonOk, pos=(6, 2), flag=wx.ALL, border=5)
        sizer.Add(buttonClose, pos=(6, 3), flag=wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)

    def updateImg(self,event):
        pass

    def saveNew(self,event):
        pass

    def closeWin(self,event):
        self.Close()

app = wx.App()
Example(None, title='GridBag Demo - www.yiibai.com')
app.MainLoop()
