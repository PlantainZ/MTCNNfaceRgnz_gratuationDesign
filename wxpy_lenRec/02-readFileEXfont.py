import wx
import os


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title)

        self.InitUI()

    def InitUI(self):
        self.count = 0
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.text = wx.TextCtrl(pnl, size=(-1, 200), style=wx.TE_MULTILINE)
        self.btn1 = wx.Button(pnl, label="Open a File")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn1)

        #文本字体选择的框
        self.btn2 = wx.Button(pnl, label="Choose Font")
        self.Bind(wx.EVT_BUTTON, self.fontOnClick, self.btn2)

        hbox1.Add(self.text, proportion=1, flag=wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
        hbox3.Add(self.btn2, proportion=1, flag=wx.ALIGN_CENTER)

        vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
        vbox.Add(hbox3,proportion=1, flag=wx.ALIGN_CENTRE)

        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND | wx.ALIGN_CENTRE)
        #这里注意一个EXPAND，它表示占据整个窗口的宽度

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def OnClick(self, e):
        wildcard = "Text Files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, wx.FC_OPEN)
        #注意它要是FC_OPEN才能打开文件


        if dlg.ShowModal() == wx.ID_OK:
            f = open(dlg.GetPath(), 'r')

            with f:
                data = f.read()
                self.text.SetValue(data)
        dlg.Destroy()

    def fontOnClick(self,e):
        dlg = wx.FontDialog(self, wx.FontData())
        #弹出选字体的框
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            #data是那些选字体的数据
            font = data.GetChosenFont()
            #然后得到选择的字体数据
            self.text.SetFont(font)
            #把text的字体都设置为选的字体数据

        dlg.Destroy()

ex = wx.App()
Mywin(None, 'FileDialog Demo - www.yiibai.com')
ex.MainLoop()
