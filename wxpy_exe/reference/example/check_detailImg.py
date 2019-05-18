import wx
import os
import firstPage

class detailImg():

    def __init__(self,usr_acc,usr_name):

        self.frame=wx.Frame(None, -1, title="%s的详细图片" %usr_name,size=(750,710))
        # self.path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_yueqingming'
        # self.minipath = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img\usr_yueqingming'

        # self.path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_%s' %usr_acc
        # self.minipath=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img\usr_%s' %usr_acc

        self.path = r'..\..\..\core_Rgnz\train_dir\usr_%s' %usr_acc
        self.minipath=r'..\..\..\core_Rgnz\emb_img\usr_%s' %usr_acc

        self.usr_acc=usr_acc
        self.usr_name=usr_name

        # self.Center()
        splitter = wx.SplitterWindow(self.frame, size=(500,700))
        self.leftpanel = wx.Panel(splitter)
        self.rightpanel = wx.Panel(splitter)
        splitter.SplitVertically(self.leftpanel, self.rightpanel, 200)
        splitter.SetMinimumPaneSize(80)

        list2 = []
        for i in os.listdir(self.path):
            list2.append(i)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        # self.vbox3=wx.BoxSizer(wx.VERTICAL)
        lb2 = wx.ListBox(self.leftpanel, -1, choices=list2, style=wx.LB_SINGLE,size=(700,700))
        self.frame.Bind(wx.EVT_LISTBOX, self.on_listbox, lb2)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(lb2, 1, flag=wx.ALL | wx.EXPAND, border=5)
        self.leftpanel.SetSizer(vbox1)

        self.content = wx.StaticText(self.rightpanel, label='选择左侧图片预览')
        self.bigImg=wx.StaticBitmap(self.rightpanel,1)
        self.miniImg=wx.StaticBitmap(self.rightpanel,1)
        vbox2.Add(self.content, 0, flag=wx.ALL | wx.EXPAND, border=5)
        vbox2.Add(self.bigImg, proportion=0, flag=wx.TOP, border=5)
        self.content2 = wx.StaticText(self.rightpanel, label='小图: ')

        vbox2.Add(self.content2, 1, flag=wx.TOP, border=380)
        vbox2.Add(self.miniImg, proportion=1, flag=wx.TOP, border=5)
        # self.content2.Hide()

        delBtn = wx.Button(self.rightpanel, label="删除照片")
        # delBtn.Bind(wx.EVT_BUTTON, self.delImg)
        self.rightpanel.Bind(wx.EVT_BUTTON, self.delImg, delBtn)
        # hButtomBox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2.Add(delBtn, proportion=0, flag=wx.EXPAND|wx.TOP|wx.RIGHT, border=10)

        addBtn = wx.Button(self.rightpanel, label="开启摄像头添加照片")
        # addBtn.Bind(wx.EVT_BUTTON, self.delImg)
        self.rightpanel.Bind(wx.EVT_BUTTON, None, addBtn)
        # hButtomBox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2.Add(addBtn, proportion=0, flag=wx.EXPAND | wx.TOP|wx.RIGHT|wx.BOTTOM, border=10)

        self.rightpanel.SetSizer(vbox2)
        self.frame.Show()


    def singleImgAcs(self):
        pass

    def on_listbox(self, event):
        self.imgName=event.GetString()
        s = '图片:  ' + self.imgName
        minis='小图：  emb_'+self.imgName
        # self.content2.Show()
        mypic=self.picProcess(event, self.imgName, self.path)
        miniMypic = self.picProcess(event, 'emb_'+self.imgName, self.minipath)
        self.bigImg.SetBitmap(mypic)
        self.miniImg.SetBitmap(miniMypic)
        self.content.SetLabel(s)
        self.content2.SetLabel(minis)

        # self.frame.Show()

    def picProcess(self,event,name,path):
        print("read:%s" % name)
        path = path + r'\%s' % name
        image = wx.Image(path, wx.BITMAP_TYPE_ANY)
        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))
        portion = 0.8
        w = image.GetWidth() * portion
        h = image.GetHeight() * portion
        image.Rescale(w, h)
        mypic = image.ConvertToBitmap()
        return mypic

    # def OnExit(self):  # 退出
    #     print("退出")
    #     return 0

    def delImg(self,event):
        #移除文件.
        name=self.imgName
        print('移除前test目录下有文件：%s' % os.listdir(self.path))
        # 判断文件是否存在 + "\%s" %self.imgName+"\%s" %self.imgName
        if (os.path.exists(self.path)):
            os.remove(self.path + "\%s" %self.imgName)
            os.remove(self.minipath + "\emb_%s" % self.imgName)
            print('移除后test 目录下有文件：%s' % os.listdir(self.path))
            # self.reFreshImgDetail()
            self.frame.Close()
        else:
            print("要删除的文件不存在！")


        # pass



#测试
app=wx.App()
#usr_acc,usr_name
detailImg('yueqingming','岳清明')
app.MainLoop()