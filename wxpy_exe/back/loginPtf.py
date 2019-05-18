from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx                       # 构造显示界面的GUI

COVER='./img/login.png'
from back import cameraGUI
from multiprocessing import Process


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,size=(750,400))

        self.InitUI()
        self.Centre()
        self.Show()





    def InitUI(self):
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 0)
        #垂直gap,水平gap


        #account输入栏控件----------------------------------------------------
        text = wx.StaticText(self.panel, label="Account:")
        sizer.Add(text, pos=(3, 3),flag= wx.EXPAND|wx.TOP , border=10)
        text = wx.StaticText(self.panel, label="    ")
        sizer.Add(text, pos=(3, 4), flag=wx.TOP,border=10)
        tc = wx.TextCtrl(self.panel)
        sizer.Add(tc, pos=(3,5),span=(1, 3), flag=wx.TOP|wx.RIGHT| wx.EXPAND, border=10)

        #password输入栏控件---------------------------------------------------
        text1 = wx.StaticText(self.panel, label="password:",style=wx.TE_PASSWORD)
        sizer.Add(text1, pos=(4, 3), flag=wx.TOP, border=10)
        text = wx.StaticText(self.panel, label="    ")
        sizer.Add(text, pos=(4, 4), flag=wx.TOP, border=10)
        tc1 = wx.TextCtrl(self.panel)
        sizer.Add(tc1, pos=(4, 5), span=(1, 3), flag=wx.TOP| wx.RIGHT| wx.EXPAND, border=10)

        #按钮行控件------------------------------------------------------------
        buttonOk = wx.Button(self.panel, label="验证")
        buttonClose = wx.Button(self.panel, label="注册")

#-----------------footer------------------------------------
        nm = wx.StaticBox(self.panel, -1, '制作')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)
        # 要生成staticBox和它自己的sizer

        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        fn1 = wx.StaticText(self.panel, -1, "@吞日月里洗澡")
        nmbox.Add(nm, 0, wx.ALL | wx.CENTER)
        nmbox.Add(fn1, 0, wx.ALL | wx.CENTER)
        nmSizer.Add(nmbox ,flag=wx.ALL | wx.CENTER, border=10)
# #-----------------footer End--------------------------------------

        #关于按钮响应事件self.subFrame,
        self.Bind(wx.EVT_BUTTON,self.subFrame, buttonOk)


        #sizer嵌入组件----------------------------------------------------
        sizer.Add(buttonOk, pos=(6, 5), flag=wx.TOP, border=5)
        sizer.Add(buttonClose, pos=(6,7), flag=wx.TOP, border=5)
        sizer.Add(nmSizer, pos=(11, 1), flag=wx.ALL, border=20)
        self.panel.SetSizerAndFit(sizer)

    def subFrame(self,holder):
        pass
        # dialog = wx.Dialog(self.panel,title='CameraOpen~')
        # rec = dialog.ShowWindowModal()
        # subpnl = wx.Panel(self)self.camObj.GUIshow


#========================================================================
#tf部分
#=======================================================================





#生成登陆框
def loginFrame():
    app = wx.App()
    Example(None, title='2019毕设演示')
    app.MainLoop()

# def cameraPrepare():
#     camObj.Show()
#     camObj.show=1



if __name__=='__main__':
    # q = Queue()
    pw = Process(target=loginFrame)
    # camObj=cameraGUI.cameraInit()
    # pr = Process(target=cameraGUI.cameraInit)
    # 启动子进程pw，写入:, args=(q,)
    pr = Process(target=cameraGUI.cameraInit)
    pr.start()
    pr.join()
    pw.start()
    # 启动子进程pr，读取:
    # pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    # pr.terminate()
