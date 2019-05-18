import wx
class MyFrame(wx.Frame):
    eve = 0

    def __init__(self):
        super().__init__(parent=None,title="vbox",size=(500,200),pos=(100,100))   #继承wx.Frame类
        self.Center()

        splitter = wx.SplitterWindow(self,-1)
        leftpanel = wx.Panel(splitter)
        rigntpanel = wx.Panel(splitter)
        splitter.SplitVertically(leftpanel,rigntpanel,100)
        splitter.SetMinimumPaneSize(80)

        list2 = ['shanghai','beijin']
        lb2=wx.ListBox(leftpanel,-1,choices = list2,style = wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX,self.on_listbox,lb2)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(lb2,1,flag=wx.ALL | wx.EXPAND,border=5)
        leftpanel.SetSizer(vbox1)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.content = wx.StaticText(rigntpanel,label='右侧面板')
        vbox2.Add(self.content, 1, flag=wx.ALL | wx.EXPAND, border=5)
        leftpanel.SetSizer(vbox2)

    def on_listbox(self,event):
        s = '选择'+event.GetString()
        self.content.SetLabel(s)



class App(wx.App):
    def OnInit(self):    #进入
        frame = MyFrame()
        frame.Show()
        return True
    def OnExit(self):   #退出
        print("tuichu")
        return 0

if __name__ == '__main__':
    app=App()
    app.MainLoop()