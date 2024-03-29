import wx


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(300, 200))

        self.InitUI()

    def InitUI(self):
        self.count = 0
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.text = wx.TextCtrl(pnl, size=(250, 25), style=wx.TE_READONLY)
        self.btn1 = wx.Button(pnl, label="Enter Text")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn1)

        hbox1.Add(self.text, proportion=1, flag=wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)

        vbox.Add((0, 30))# 距离上方组件30px
        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
        vbox.Add((0, 20))# margin-top:20px
        vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def OnClick(self, e):
        dlg = wx.TextEntryDialog(self, 'Enter Your Name', 'Text Entry Dialog')
        #'Enter ur name'是输入栏上方标签的字，然后Text Entry Dialog是模态框的框名字
        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue("Name entered:" + dlg.GetValue())
        dlg.Destroy()


ex = wx.App()
Mywin(None, 'TextEntry Demo - www.yiibai.com')
ex.MainLoop()