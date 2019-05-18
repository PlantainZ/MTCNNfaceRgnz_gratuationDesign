#有个bug存在：
#    关闭查看详细个人图片页面的时候，要记得切断cameraRegister线程

# 导入mx模块
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
from scipy import misc
import tensorflow as tf
import numpy as np
import os
import facenet
import align.detect_face

import wx
import wx.grid
from mydb import Sql_operation
import cameraRegister
import check_record
import MulProcessing_Camera
from wx.lib.pubsub import pub
import shutil
import edit_delImgDir

# 创建CSDN学生信息管理系统登录界面类
class UserLogin(wx.Frame):
    '''
    登录界面
    '''

    # 初始化登录界面
    def __init__(self):
        app = wx.App()
        super(UserLogin, self).__init__(None, title='2019毕设-人员管理系统',size=(1224, 750))
        # 设置窗口屏幕居中
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        # 调用登录界面函数
        self.LoginInterface()

        #开摄像头就开下边两行
        self.mulProCamera=MulProcessing_Camera.CameraThread('login')
        pub.subscribe(self.updateDisplay, "update")
        app.MainLoop()

    def LoginInterface(self):
        # 创建垂直方向box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="2019毕设-人员管理系统")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)

        text = wx.StaticText(self.pnl, label="    ")
        # 添加logo静态文本到vbox布局管理器
        vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=180)
        vbox.Add(text, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)
        #wx.FIXED_MINSIZE:不允许该项目变得比其最初的最小尺寸更小
        #################################################################################
        # 创建静态框
        sb_username = wx.StaticBox(self.pnl, label="用户名")
        sb_password = wx.StaticBox(self.pnl, label="密  码")
        # self.warnText = wx.StaticBox(self.pnl, label="用户名或密码错误！")
        # 创建水平方向box布局管理器
        hsbox_username = wx.StaticBoxSizer(sb_username, wx.HORIZONTAL)
        hsbox_password = wx.StaticBoxSizer(sb_password, wx.HORIZONTAL)
        # hsbox_warnText = wx.StaticBoxSizer(self.warnText, wx.HORIZONTAL)
        # 创建用户名、密码输入框
        self.user_name = wx.TextCtrl(self.pnl, size=(210, 25))
        self.user_password = wx.TextCtrl(self.pnl, size=(210, 25))
        # 添加用户名和密码输入框到hsbox布局管理器
        hsbox_username.Add(self.user_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_password.Add(self.user_password, 0, wx.EXPAND | wx.BOTTOM, 5)
        # hsbox_warnText.Add(self.warnText, 0, wx.EXPAND | wx.BOTTOM, 5)
        #错误提示的StaticText!

        # self.warnText.Hide()
        # 将水平box添加到垂直box
        # vbox.Add(hsbox_warnText,proportion=0,flag=wx.CENTER)
        vbox.Add(hsbox_username, proportion=0, flag=wx.CENTER)
        vbox.Add(hsbox_password, proportion=0, flag=wx.CENTER)
        #################################################################################
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()
        # 创建登录按钮、绑定事件处理
        self.login_button = wx.Button(self.pnl, label="摄像头验证", size=(80, 25))
        self.login_button.Bind(wx.EVT_BUTTON, self.LoginButton)
        # 添加登录按钮到hbox布局管理器
        hbox.Add(self.login_button, 0, flag=wx.EXPAND | wx.TOP, border=5)
        # 将水平box添加到垂直box
        vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        #################################################################################
        # 设置面板的布局管理器vbox
        self.pnl.SetSizer(vbox)
        self.Show()


    def LoginButton(self, event):
        # self.openCamera=self.user_name.GetValue()
        # self.login_button.Hide()
        # 连接login_users数据库
        op = Sql_operation()
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll("original_web_user")
        # 匹配标记
        self.login_sign = 0
        # 匹配用户名和密码
        for i in np:
            if (i[3] == self.user_name.GetValue()) and (i[4] == self.user_password.GetValue()):
                self.login_sign = 1
                self.now_usr_acc=i[3]
                self.now_usr_name=i[2]
                break
        if self.login_sign == 0:
            print("用户名或密码错误！")
            # self.warnText.Show()
        elif self.login_sign == 1:
            print("登录成功！")
            self.cameraShow = 1
            #开摄像头就开下边一行下下边全部不要开
            self.mulProCamera.getLoginParams(self.user_name.GetValue(),self.cameraShow,self.now_usr_name,self.now_usr_acc)

            # 测试模式切换部分
            # operation = UserOperation(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            # operation.Show()
            # self.Hide()
            # self.Close(True)

    def updateDisplay(self, msg):
        # 然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        t = msg
        # if isinstance(t, str):
        #     self.displayLbl.SetLabel("%s" % t)
        # else:
        #     self.displayLbl.SetLabel("多多多你是个大佬呀！！")
        #     self.btn.Enable()
        if(t =='Close_Login'):
            operation = UserOperation(self.now_usr_name, self.now_usr_acc, None, title="2019毕业设计演示",
                                                size=(1224, 750))
            operation.Show()
            self.Close(True)
        elif(t =='Close_Register'):
            print('已关闭注册摄像头')

class UserOperation(wx.Frame):
    '''
    操作界面
    '''

    def __init__(self,now_usr_name,now_usr_acc,*args, **kw):
        # ensure the parent's __init__ is called
        super(UserOperation, self).__init__(*args, **kw)
        # 设置窗口屏幕居中
        self.now_usr_name = now_usr_name
        self.now_usr_acc = now_usr_acc
        print("UserOperation----now_usr_name=%s" % self.now_usr_name)
        print("UserOperation----now_usr_acc=%s" % self.now_usr_acc)
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        # 调用操作界面函数
        self.OperationInterface()
        self.recordWriter=check_record.writeRecord()

    def OperationInterface(self):
        # 创建垂直方向box布局管理器
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="2019毕业设计演示")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)
        # 添加logo静态文本到vbox布局管理器
        self.vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=5)
        # accBox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=5)
        # accBox.Add(accTips,proportion=1,flag=wx.FIXED_MINSIZE | wx.BOTTOM | wx.RIGHT, border=5)
        # self.vbox.Add(accBox)
        #################################################################################
        # 创建静态框
        sb_button = wx.StaticBox(self.pnl, label="选择操作")
        # 创建垂直方向box布局管理器
        vsbox_button = wx.StaticBoxSizer(sb_button, wx.VERTICAL)
        # 创建操作按钮、绑定事件处理
        check_button = wx.Button(self.pnl, id=10, label="打开现有摄像头", size=(150, 50))
        add_button = wx.Button(self.pnl, id=11, label="添加人员信息", size=(150, 50))
        delete_button = wx.Button(self.pnl, id=12, label="查看/编辑信息", size=(150, 50))
        quit_button = wx.Button(self.pnl, id=13, label="退出系统", size=(150, 50))
        name_tips = wx.StaticText(self.pnl,label="用户:  %s"%self.now_usr_name)
        account_tips = wx.StaticText(self.pnl, label="账号:  %s" % self.now_usr_acc)
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=10, id2=13)
        # 添加操作按钮到vsbox布局管理器
        vsbox_button.Add(check_button, 0, wx.EXPAND | wx.BOTTOM, 40)
        vsbox_button.Add(add_button, 0, wx.EXPAND | wx.BOTTOM, 40)
        vsbox_button.Add(delete_button, 0, wx.EXPAND | wx.BOTTOM, 40)
        vsbox_button.Add(quit_button, 0, wx.EXPAND | wx.BOTTOM, 150)
        vsbox_button.Add(name_tips, 0, wx.EXPAND | wx.BOTTOM, 15)
        vsbox_button.Add(account_tips, 0, wx.EXPAND | wx.BOTTOM, 50)
        # 创建静态框
        sb_show_operation = wx.StaticBox(self.pnl, label="显示/操作窗口", size=(800, 500))
        # 创建垂直方向box布局管理器
        self.vsbox_show_operation = wx.StaticBoxSizer(sb_show_operation, wx.VERTICAL)
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()
        hbox.Add(vsbox_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        hbox.Add(self.vsbox_show_operation, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 将hbox添加到垂直box
        self.vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        #################################################################################
        self.pnl.SetSizer(self.vbox)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("摄像头激活！")
            inquire_button = InquireOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            # ul.show=1
            add_button = AddOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            add_button.Show()

            self.Close(True)
        elif source_id == 12:
            print("删除操作！")
            del_button = DelOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)

    def reFreshInfo(self):
        print("删除操作！")
        del_button = DelOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
        del_button.Show()
        self.Close()#测试


    def OnLabelleftClick(self, event):
        # 连接login_users数据库
        op = Sql_operation()
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll("original_web_user")
        print("RowIdx: {0}".format(event.GetRow()))
        # print("ColIdx: {0}".format(event.GetCol()))
        print(np[event.GetRow()])
        self.gridChoice=np[event.GetRow()]
        #[0]:id / [1]:usr_icon / [2]:usr_name / [3]:usr_acc
        #[4]:usr_pwd / [5]:rgst_time / [6]:class
        # print(self.gridChoice)
        event.Skip()

    def showDetail(self, event):
        self.detail = detailImg(self.gridChoice[3], self.gridChoice[2])

    def reFreshImgDetail(self, acc, name):
        detailImg(acc, name)

    # 用户信息更改=====================================================================
    def changeDetail(self, event):
        self.detailFrame = wx.Frame(self, title="修改页面", size=(470, 320))
        panel = wx.Panel(self.detailFrame)
        sizer = wx.GridBagSizer(0, 0)

        text = wx.StaticText(panel, label="用户名:")
        sizer.Add(text, pos=(0, 0), flag=wx.ALL, border=5)
        # 如果想要只读:在TextCtrl后边加上 style = wx.TE_READONLY
        self.tc = wx.TextCtrl(panel, value=self.gridChoice[2], style=wx.TE_CENTER)
        sizer.Add(self.tc, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        text1 = wx.StaticText(panel, label="用户账号")
        sizer.Add(text1, pos=(1, 0), flag=wx.ALL, border=5)

        self.tc1 = wx.TextCtrl(panel, value=self.gridChoice[3], style=wx.TE_CENTER | wx.TE_READONLY)
        sizer.Add(self.tc1, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        # span=(1, 3),, style=wx.TE_MULTILINE
        text2 = wx.StaticText(panel, label="登陆密码")
        sizer.Add(text2, pos=(2, 0), flag=wx.ALL, border=5)

        self.tc2 = wx.TextCtrl(panel, value=self.gridChoice[4], style=wx.TE_CENTER)
        sizer.Add(self.tc2, pos=(2, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        # 这个是所在班级栏====================================================
        text3 = wx.StaticText(panel, label="所在班级")
        sizer.Add(text3, pos=(3, 0), flag=wx.ALL, border=5)

        self.tc3 = wx.TextCtrl(panel, value=self.gridChoice[6], style=wx.TE_CENTER)
        sizer.Add(self.tc3, pos=(3, 1), flag=wx.ALL, border=5)
        # ================================================================= wx.EXPAND|wx.ALIGN_CENTER |

        text4 = wx.StaticText(panel, label="备注")
        sizer.Add(text4, pos=(4, 0), flag=wx.ALL, border=5)

        self.tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE, value="四大皆空")
        sizer.Add(self.tc4, pos=(4, 1), span=(2, 3), flag=wx.EXPAND | wx.ALL, border=5)
        # sizer.AddGrowableRow(3)#表示空三行的意思。

        ImgChange = wx.Button(panel, label="用户图像")
        buttonOk = wx.Button(panel, label="保存修改")
        buttonClose = wx.Button(panel, label="关闭")

        ImgChange.Bind(wx.EVT_BUTTON, self.showDetail)
        buttonOk.Bind(wx.EVT_BUTTON, self.saveNew)
        buttonClose.Bind(wx.EVT_BUTTON, self.closeWin)

        sizer.Add(ImgChange, pos=(6, 1), flag=wx.ALL, border=5)
        sizer.Add(buttonOk, pos=(6, 2), flag=wx.ALL, border=5)
        sizer.Add(buttonClose, pos=(6, 3), flag=wx.ALL, border=5)

        panel.SetSizer(sizer)
        self.detailFrame.Center()
        self.detailFrame.Show()

    def saveNew(self, event):
        dbObj = Sql_operation()
        dbObj.Update(self.tc.GetValue(),
                     self.tc1.GetValue(),
                     self.tc2.GetValue(),
                     self.tc3.GetValue())

    # , self.tc4

    def closeWin(self, event):
        self.detailFrame.Close()
        self.reFreshInfo()
        # self.delRgstCamera=int(0)#记得关闭注册摄像头后台线程
        # self.Close()
        # self.Hide()


# 继承UserOperation类，实现初始化操作界面
class InquireOp(UserOperation):

    def __init__(self,now_usr_name,now_usr_acc, *args, **kw):
        # ensure the parent's __init__ is called
        super(InquireOp, self).__init__(now_usr_name,now_usr_acc,*args, **kw)
        self.now_usr_name=now_usr_name
        self.now_usr_acc=now_usr_acc
        # # 创建学生信息网格
        # self.stu_grid = self.CreateGrid()
        # self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,self.OnLabelleftClick)
        # # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(self.stu_grid, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 30)


        #-----布局测试-------
        #第一行的提示
        vbox=wx.BoxSizer(wx.VERTICAL)

        tips=wx.StaticText(self.pnl, label="提示:若有人员变动，请先在开启监控前点击更新识别库按钮。")
        vbox.Add(tips, 0 ,flag=wx.ALL, border=5)




        #第二行的两个按钮
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # newRgnzBtn = wx.Button(self.pnl, label="更新识别库", pos=(325, 78), size=(100, 35))
        check_detail = wx.Button(self.pnl, label="开启管理监控", pos=(625, 78), size=(100, 35))
        show_grid = wx.Button(self.pnl, label="查看变更记录", pos=(625, 78), size=(100, 35))

        tips2 = wx.StaticText(self.pnl, label=" ")
        # newRgnzBtn.Bind(wx.EVT_BUTTON, self.newRgnzDb )
        check_detail.Bind(wx.EVT_BUTTON, self.newRgnzCmr)
        # show_grid.Bind(wx.EVT_BUTTON,self.changeDetail)
        show_grid.Bind(wx.EVT_BUTTON,None)

        # hbox.Add(newRgnzBtn, 0, wx.CENTER | wx.TOP |wx.LEFT| wx.FIXED_MINSIZE, 20)
        hbox.Add(check_detail, 0, wx.CENTER| wx.TOP|wx.LEFT| wx.FIXED_MINSIZE, 20)
        hbox.Add(show_grid, 0, wx.CENTER | wx.TOP | wx.LEFT | wx.FIXED_MINSIZE, 20)

        vbox.Add(hbox)
        vbox.Add(tips2, 0, flag=wx.ALL, border=5)
        self.vsbox_show_operation.Add(vbox)

        # self.ppl_now=self.genGrid()
        # self.ppl_now.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        # self.vsbox_show_operation.Add(self.ppl_now, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 10)

    def newRgnzCmr(self,event):
        self.tipDia=wx.Dialog(self.pnl, title="提示", size=(250, 120))
        panel = wx.Panel(self.tipDia)
        vbox=wx.BoxSizer(wx.HORIZONTAL)
        tips = wx.StaticText(panel, label="这将会耗费大约15秒的时间，请稍候...")
        vbox.Add(tips, 0, flag=wx.ALL|wx.CENTER, border=10)
        panel.SetSizer(vbox)
        self.tipDia.Show()

        # train_knn_emb.createKNN()

        multiCmr= MulProcessing_Camera.CameraThread('spy')
        multiCmr.getSpyParams(1,self.now_usr_name,self.now_usr_acc)
        pub.subscribe(self.updateDisplay, "closeDia")


        # msg2=wx.MessageBox("识别库更新完成", "提示", wx.OK)

    def updateDisplay(self, msg):
        #然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        tips = msg
        # if isinstance(t, str):
            # self.displayLbl.SetLabel("%s" % t)
        if msg=='Tips_Close':
            self.tipDia.Close()
        print(tips)
        # else:
        #     self.displayLbl.SetLabel("多多多你是个大佬呀！！" )
        #     self.btn.Enable()

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            pass
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("删除操作！")
            del_button = DelOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)

    def singleImgAcs(self,path):
        image = wx.Image(path, wx.BITMAP_TYPE_ANY)
        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))
        portion = 0.50
        w = image.GetWidth() * portion
        h = image.GetHeight() * portion
        image.Rescale(w, h)
        mypic = image.ConvertToBitmap()
        return mypic
#------------------------------------------------------------------------------
    #这里开始append数据库的资料。==========================================================

    # def genGrid(self):
    #     # 连接数据库
    #     op = Sql_operation()
    #     # 获取stu_information表中的学生信息，返回为二维元组
    #     np = op.FindAll("original_web_user")
    #
    #     # np=[]
    #     # for i in self.fin_obj:
    #     #     tmp=op.Search(i)
    #     #     np.append(tmp)
    #     # print("np 现在有的记录条数：%s" %np)
    #
    #     column_names = ("图像文件夹", "用户名", "账号", "密码", "注册时间", "所属班级","备注")
    #     stu_grid = wx.grid.Grid(self.pnl)
    #     stu_grid.CreateGrid(len(np), len(np[0]) - 1)#(记录的行数,记录的列数)
    #     for row in range(len(np)):
    #         stu_grid.SetRowLabelValue(row, str(np[row][0]))  # 确保网格序列号与数据库id保持一致
    #         for col in range(1, len(np[row])):
    #             stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
    #             stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
    #     self.detail = wx.Button(self.pnl, label="查看个人照片", pos=(625, 78), size=(80, 25))
    #
    #     # 为删除按钮组件绑定事件处理
    #     self.detail.Bind(wx.EVT_BUTTON,self.showDetail)
    #     stu_grid.AutoSize()
    #     return stu_grid






# 继承UserOperation类，实现初始化操作界面
class AddOp(UserOperation):
    def __init__(self,now_usr_name,now_usr_acc, *args, **kw):
        # ensure the parent's __init__ is called
        super(AddOp, self).__init__(now_usr_name,now_usr_acc,*args, **kw)
        # 创建添加学生信息输入框、添加按钮
        # self.stu_name = wx.TextCtrl(self.pnl, size=(210, 25))
        self.now_usr_name=now_usr_name
        self.now_usr_acc=now_usr_acc
        self.stu_gender = wx.TextCtrl(self.pnl, size=(210, 25))
        self.stu_age = wx.TextCtrl(self.pnl, size=(210, 25))
        self.stu_cid = wx.TextCtrl(self.pnl, size=(210, 25))
        self.stu_classid = wx.TextCtrl(self.pnl, size=(210, 25))
        # self.stu_phone = wx.TextCtrl(self.pnl, size=(210, 25))
        self.add_affirm = wx.Button(self.pnl, label="点击采集注册图像")
        # 为添加按钮组件绑定事件处理, size=(80, 25)
        self.add_affirm.Bind(wx.EVT_BUTTON, self.AddAffirm)
        #################################################################################
        # 创建静态框
        # sb_name = wx.StaticBox(self.pnl, label="识别图像位置")
        sb_gender = wx.StaticBox(self.pnl, label="姓名")
        sb_age = wx.StaticBox(self.pnl, label="账号")
        sb_cid = wx.StaticBox(self.pnl, label="密码")
        sb_classid = wx.StaticBox(self.pnl, label="所在班级")
        # sb_phone = wx.StaticBox(self.pnl, label="识别图像")
        # 创建水平方向box布局管理器
        # hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_gender = wx.StaticBoxSizer(sb_gender, wx.HORIZONTAL)
        hsbox_age = wx.StaticBoxSizer(sb_age, wx.HORIZONTAL)
        hsbox_cid = wx.StaticBoxSizer(sb_cid, wx.HORIZONTAL)
        hsbox_classid = wx.StaticBoxSizer(sb_classid, wx.HORIZONTAL)
        # hsbox_phone = wx.StaticBoxSizer(sb_phone, wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        # hsbox_name.Add(self.stu_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_gender.Add(self.stu_gender, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_age.Add(self.stu_age, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_cid.Add(self.stu_cid, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_classid.Add(self.stu_classid, 0, wx.EXPAND | wx.BOTTOM, 5)
        # hsbox_phone.Add(self.stu_phone, 0, wx.EXPAND | wx.BOTTOM, 5)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_name, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_gender, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_age, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_cid, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_classid, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_phone, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(self.add_affirm, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.rgstCmr=cameraRegister.cameraRgst()

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("查询操作！")
            self.rgstCmr.breakSet()
            inquire_button = InquireOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            pass
        elif source_id == 12:
            print("删除操作！")
            self.rgstCmr.breakSet()
            del_button = DelOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.rgstCmr.breakSet()
            self.Close(True)

    def AddAffirm(self, event):
        # 连接users数据库
        op = Sql_operation()
        # 向stu_information表添加学生信息
        # stu_name = self.stu_name.GetValue()
        self.stu_name = 'usr_%s' %self.stu_age.GetValue()#usr_icon
        print(self.stu_name)
        stu_gender = self.stu_gender.GetValue() #usr_name
        print(stu_gender)
        self.stu_acc = self.stu_age.GetValue()  #usr_acc
        print(self.stu_acc) #是usr_acc
        self.stu_pwd = self.stu_cid.GetValue()  #usr_pwd
        print(self.stu_pwd)
        self.stu_clsid = self.stu_classid.GetValue()  #usr_class
        print(self.stu_clsid)
        # stu_phone = self.stu_phone.GetValue()     #还没开的备注
        stu_phone = ''
        print(stu_phone)

        if (self.stu_acc == '' or self.stu_name=='' or self.stu_pwd=='' or self.stu_clsid==''):
            wx.MessageBox("请填写完整信息！", "警告", wx.OK | wx.ICON_INFORMATION)
        else:
            np = op.Insert(self.stu_name, stu_gender, self.stu_acc, self.stu_pwd, self.stu_clsid, stu_phone)
            # cameraRegister.cameraRgst(self.stu_acc)
            self.rgstCmr.getRegisterParams(self.stu_acc,1)


    def rgstDisplay(self, msg):
        #然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        tips = msg
        if(tips):
            print("注册完成！"+tips)
        # if isinstance(t, str):
        #     self.displayLbl.SetLabel("%s" % t)
        # else:
        #     self.displayLbl.SetLabel("多多多你是个大佬呀！！" )
        #     self.btn.Enable()




# 继承InquireOp类，实现初始化操作界面
class DelOp(UserOperation):

    def __init__(self,now_usr_name,now_usr_acc, *args, **kw):
        # ensure the parent's __init__ is called
        self.gridChoice = ('null')
        super(DelOp, self).__init__(now_usr_name,now_usr_acc,*args, **kw)
        self.now_usr_name=now_usr_name
        self.now_usr_acc=now_usr_acc
        # 迁移过来的学生网格
        self.stu_grid = self.CreateGrid()
        self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        # 添加到vsbox_show_operation布局管理器
        self.vsbox_show_operation.Add(self.stu_grid, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 30)

        # 创建删除学员信息输入框、删除按钮
        # self.del_id = wx.TextCtrl(self.pnl, pos=(407, 78), size=(210, 25))
        hbox=wx.BoxSizer(wx.HORIZONTAL)
        self.del_affirm = wx.Button(self.pnl, label="删除", pos=(625, 78), size=(80, 25))
        self.check_detail = wx.Button(self.pnl, label="修改信息", pos=(625, 78), size=(80, 25))
        # 为删除按钮组件绑定事件处理
        self.del_affirm.Bind(wx.EVT_BUTTON, self.DelAffirm)
        self.check_detail.Bind(wx.EVT_BUTTON, self.changeDetail)

        #################################################################################
        # 创建静态框
        # sb_del = wx.StaticBox(self.pnl, label="请选择需要删除的用户账户名：")
        # 创建水平方向box布局管理器
        # hsbox_del = wx.StaticBoxSizer(sb_del, wx.HORIZONTAL)
        # 添加到hsbox_name布局管理器
        # hsbox_del.Add(self.del_id, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_del, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        hbox.Add(self.del_affirm, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        hbox.Add(self.check_detail, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(self.del_affirm, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(self.check_detail, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 10)
        self.vsbox_show_operation.Add(hbox)




    def CreateGrid(self):
        # 连接数据库
        op = Sql_operation()
        # 获取stu_information表中的学生信息，返回为二维元组
        np = op.FindAll("original_web_user")
        column_names = ("图像文件夹", "用户名", "账号", "密码", "注册时间", "所属班级","备注")
        stu_grid = wx.grid.Grid(self.pnl)
        stu_grid.CreateGrid(len(np), len(np[0]) - 1)#(记录的行数,记录的列数)
        for row in range(len(np)):
            stu_grid.SetRowLabelValue(row, str(np[row][0]))  # 确保网格序列号与数据库id保持一致
            for col in range(1, len(np[row])):
                stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
        self.detail = wx.Button(self.pnl, label="查看个人照片", pos=(625, 78), size=(80, 25))

        # 为删除按钮组件绑定事件处理
        self.detail.Bind(wx.EVT_BUTTON,self.showDetail)
        stu_grid.AutoSize()
        return stu_grid



    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("查询操作！")
            inquire_button = InquireOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            pass
        elif source_id == 13:
            self.Close(True)

    def DelAffirm(self, event):

        op = Sql_operation()
        # 向stu_information表添加学生信息
        del_acc = self.gridChoice[3]
        print(del_acc)
        np = op.Del(del_acc)

        path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_%s' %del_acc
        minipath = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img\usr_%s' % del_acc
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(minipath):
            shutil.rmtree(minipath)

        del_button = DelOp(self.now_usr_name,self.now_usr_acc,None, title="2019毕业设计演示", size=(1224, 750))
        del_button.Show()
        self.Close(True)






#=============================================================================================
#用户图片编辑部分
#=============================================================================================
class detailImg(DelOp):

    def __init__(self,usr_acc,usr_name):
        self.frame=wx.Frame(None, -1, title="%s的详细图片" %usr_name,size=(750,710))
        # self.path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_yueqingming'
        # self.minipath = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img\usr_yueqingming'
        self.path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_%s' %usr_acc
        self.minipath=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img\usr_%s' %usr_acc
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
        self.lb2 = wx.ListBox(self.leftpanel, -1, choices=list2, style=wx.LB_SINGLE,size=(700,700))
        self.frame.Bind(wx.EVT_LISTBOX, self.on_listbox, self.lb2)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1.Add(self.lb2, 1, flag=wx.ALL | wx.EXPAND, border=5)
        self.leftpanel.SetSizer(self.vbox1)

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
        self.rightpanel.Bind(wx.EVT_BUTTON, self.delImg, delBtn)
        vbox2.Add(delBtn, proportion=0, flag=wx.EXPAND|wx.TOP|wx.RIGHT, border=10)

        addBtn = wx.Button(self.rightpanel, label="开启摄像头添加照片")
        self.rightpanel.Bind(wx.EVT_BUTTON, self.addUsrImg, addBtn)
        vbox2.Add(addBtn, proportion=0, flag=wx.EXPAND | wx.TOP|wx.RIGHT|wx.BOTTOM, border=10)

        self.rightpanel.SetSizer(vbox2)
        self.frame.Center()
        self.frame.Show()
        self.addCmr=cameraRegister.cameraRgst()

        pub.subscribe(self.imgListRefresh, "rgst")


    def imgListRefresh(self, msg):
        #然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        t = msg
        if t =='rgst_end':
            self.reFreshImgDetail(self.usr_acc, self.usr_name)
            self.frame.Close()


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
            self.reFreshImgDetail(self.usr_acc,self.usr_name)
            self.frame.Close()
        else:
            print("要删除的文件不存在！")

    def addUsrImg(self,event):
        # cameraRegister.cameraRgst(self.usr_acc)
        self.addCmr.getRegisterParams(self.usr_acc, cameraShow=1)
        #esc按钮之后。
        # self.reFreshImgDetail(self.usr_acc, self.usr_name)
        # self.frame.Close()



#----------------------------公共部分--------------------------------------------
def load_and_align_data(img, image_size, margin, pnet, rnet, onet):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    img_size = np.asarray(img.shape)[0:2]

    # bounding_boxes shape:(1,5)  type:np.ndarray
    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)

    # 如果未发现目标 直接返回
    if len(bounding_boxes) < 1:
        return 0, 0, 0

    # 从数组的形状中删除单维度条目，即把shape中为1的维度去掉
    # det = np.squeeze(bounding_boxes[:,0:4])
    det = bounding_boxes

    print('det shape type')
    print(det.shape)
    print(type(det))

    det[:, 0] = np.maximum(det[:, 0] - margin / 2, 0)
    det[:, 1] = np.maximum(det[:, 1] - margin / 2, 0)
    det[:, 2] = np.minimum(det[:, 2] + margin / 2, img_size[1] - 1)
    det[:, 3] = np.minimum(det[:, 3] + margin / 2, img_size[0] - 1)

    det = det.astype(int)
    crop = []
    for i in range(len(bounding_boxes)):
        temp_crop = img[det[i, 1]:det[i, 3], det[i, 0]:det[i, 2], :]
        aligned = misc.imresize(temp_crop, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        crop.append(prewhitened)

    # np.stack 将crop由一维list变为二维
    crop_image = np.stack(crop)

    return 1, det, crop_image


if __name__ == '__main__':
    ul=UserLogin()
