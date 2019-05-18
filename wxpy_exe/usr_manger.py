import wx

class managerPage(wx.Frame):
    def __init__(self, parent, title):
        super(managerPage, self).__init__(parent, title=title,size=(1350,700))

        self.InitMenu()
        self.InitUI()
        self.Centre()
        self.Show()

    #原始菜单生成-------------------------------------------------------------------
    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(7, 7)
        #垂直gap,水平gap


        #account输入栏控件-------------------
        text = wx.StaticText(panel, label="Account:")
        sizer.Add(text, pos=(3, 3),flag= wx.EXPAND|wx.TOP , border=10)
        text = wx.StaticText(panel, label="    ")
        sizer.Add(text, pos=(3, 4), flag=wx.TOP,border=10)
        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(3,5),span=(1, 3), flag=wx.TOP|wx.RIGHT| wx.EXPAND, border=10)

        #password输入栏控件------------------
        text1 = wx.StaticText(panel, label="password:",style=wx.TE_PASSWORD)
        sizer.Add(text1, pos=(4, 3), flag=wx.TOP, border=10)
        text = wx.StaticText(panel, label="    ")
        sizer.Add(text, pos=(4, 4), flag=wx.TOP, border=10)
        self.pwd = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        sizer.Add(self.pwd, pos=(4, 5),span=(1, 3), flag=wx.TOP| wx.RIGHT| wx.EXPAND, border=10)

        #按钮行控件--------------------------
        self.buttonOk = wx.Button(panel, label="验证")
        self.buttonClose = wx.Button(panel, label="注册")
        self.Bind(wx.EVT_BUTTON, None, self.buttonOk)
        # self.Bind(wx.EVT_BUTTON, None, close_button)

        #-----------------footer----------
        nm = wx.StaticBox(panel, -1, '制作')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)
        # 要生成staticBox和它自己的sizer

        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        fn1 = wx.StaticText(panel, -1, "@吞日月里洗澡")
        nmbox.Add(nm, 0, wx.ALL | wx.CENTER)
        nmbox.Add(fn1, 0, wx.ALL | wx.CENTER)
        nmSizer.Add(nmbox ,flag=wx.ALL | wx.CENTER, border=10)
        #-----------------footer End---------

        #sizer嵌入组件------------------------
        sizer.Add(self.buttonOk, pos=(6, 5), flag=wx.TOP, border=5)
        sizer.Add(self.buttonClose, pos=(6,7), flag=wx.TOP, border=5)
        sizer.Add(nmSizer, pos=(11, 1), flag=wx.ALL, border=20)
        panel.SetSizerAndFit(sizer)




#生成菜单Bar-----------------------------------------------------------------------------
    def InitMenu(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        newitem = wx.MenuItem(fileMenu, wx.ID_NEW, text="New", kind=wx.ITEM_NORMAL)
        # newitem.SetBitmap(wx.Bitmap("./img/new.bmp"))
        fileMenu.AppendItem(newitem)

        fileMenu.AppendSeparator()

        editMenu = wx.Menu()
        copyItem = wx.MenuItem(editMenu, 100, text="copy", kind=wx.ITEM_NORMAL)
        # copyItem.SetBitmap(wx.Bitmap("copy.bmp"))

        editMenu.AppendItem(copyItem)
        cutItem = wx.MenuItem(editMenu, 101, text="cut", kind=wx.ITEM_NORMAL)
        # cutItem.SetBitmap(wx.Bitmap("cut.bmp"))

        editMenu.AppendItem(cutItem)
        pasteItem = wx.MenuItem(editMenu, 102, text="paste", kind=wx.ITEM_NORMAL)
        # pasteItem.SetBitmap(wx.Bitmap("paste.bmp"))

        editMenu.AppendItem(pasteItem)
        fileMenu.AppendMenu(wx.ID_ANY, "Edit", editMenu)
        fileMenu.AppendSeparator()

        radio1 = wx.MenuItem(fileMenu, 200, text="Radio1", kind=wx.ITEM_RADIO)
        radio2 = wx.MenuItem(fileMenu, 300, text="radio2", kind=wx.ITEM_RADIO)

        fileMenu.AppendItem(radio1)
        fileMenu.AppendItem(radio2)
        fileMenu.AppendSeparator()

        fileMenu.AppendCheckItem(103, "Checkable")
        quit = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')

        fileMenu.AppendItem(quit)
        menubar.Append(fileMenu, '&File')

        self.SetMenuBar(menubar)
        # self.text = wx.TextCtrl(self, -1, style=wx.EXPAND | wx.TE_MULTILINE)
        # self.Bind(wx.EVT_MENU, self.menuhandler)
        # self.SetSize((350, 250))
        # self.Centre()
        # self.Show(True)

    # def menuhandler(self, event):
    #     id = event.GetId()
    #     if id == wx.ID_NEW:
    #         self.text.AppendText("new" + "\n")

def begin():
    app = wx.App()
    managerPage(None, title='2019毕设-人员管理页面')
    app.MainLoop()

if __name__=='__main__':
    begin()