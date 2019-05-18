

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from multiprocessing import Process, Queue

import os, time, random
import login

import wx
import cv2
from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import copy
import argparse
import facenet
import align.detect_face
import random

from os.path import join as pjoin
import matplotlib.pyplot as plt

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import joblib


# 读数据进程执行的代码:
def tfModelBuild():
    # 创建load_and_align_data网络
    print('Creating networks and loading parameters')
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)

    with tf.Graph().as_default():
        with tf.Session() as sess:
            # Load the model
            # 这里要改为自己的模型位置
            # model='/home/wind/facenet-master/src/models/20170512-110547/'
            model = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\20170512-110547'

            facenet.load_model(model)

            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            image = []
            nrof_images = 0

            # 这里要改为自己emb_img文件夹的位置
            # emb_dir='/home/wind/facenet-master/src/emb_img'
            emb_dir = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img'
            all_obj = []
            for i in os.listdir(emb_dir):
                all_obj.append(i)
                img = misc.imread(os.path.join(emb_dir, i), mode='RGB')
                prewhitened = facenet.prewhiten(img)
                image.append(prewhitened)
                nrof_images = nrof_images + 1

            images = np.stack(image)
            feed_dict = {images_placeholder: images, phase_train_placeholder: False}
            compare_emb = sess.run(embeddings, feed_dict=feed_dict)
            compare_num = len(compare_emb)

            # 开启ip摄像头
            # video="http://admin:admin@192.168.0.107:8081/"   #此处@后的ipv4 地址需要修改为自己的地址
            # 参数为0表示打开内置摄像头，参数是视频文件路径则打开视频
            # capture =cv2.VideoCapture(video)
            capture = cv2.VideoCapture(0)
            cv2.namedWindow("camera", 1)
            timer = 0
            while True:
                ret, frame = capture.read()

                # rgb frame np.ndarray 480*640*3
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 获取 判断标识 bounding_box crop_image
                mark, bounding_box, crop_image = load_and_align_data(rgb_frame, 160, 44, pnet, rnet, onet)
                timer += 1
                if (1):

                    print(timer)
                    if (mark):
                        feed_dict = {images_placeholder: crop_image, phase_train_placeholder: False}
                        emb = sess.run(embeddings, feed_dict=feed_dict)
                        temp_num = len(emb)

                        fin_obj = []
                        print(all_obj)

                        # 为bounding_box 匹配标签
                        for i in range(temp_num):
                            dist_list = []
                            for j in range(compare_num):
                                dist = np.sqrt(np.sum(np.square(np.subtract(emb[i, :], compare_emb[j, :]))))
                                dist_list.append(dist)
                            min_value = min(dist_list)
                            if (min_value > 0.65):
                                fin_obj.append('unknow')
                            else:
                                fin_obj.append(all_obj[dist_list.index(min_value)])

                                # 在frame上绘制边框和文字
                        for rec_position in range(temp_num):
                            cv2.rectangle(frame, (bounding_box[rec_position, 0], bounding_box[rec_position, 1]),
                                          (bounding_box[rec_position, 2], bounding_box[rec_position, 3]), (0, 255, 0),
                                          2, 8, 0)

                            cv2.putText(
                                frame,
                                fin_obj[rec_position],
                                (bounding_box[rec_position, 0], bounding_box[rec_position, 1]),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                0.8,
                                (0, 0, 255),
                                thickness=2,
                                lineType=2)
                        if(1):
                            cv2.imshow('camera', frame)

                # cv2.imshow('camera',frame)
                key = cv2.waitKey(3)
                if key == 27:
                    # esc键退出
                    print("esc break...")
                    break

            # if key == ord(' '):
            #     # 保存一张图像
            #     num = num+1
            #     filename = "frames_%s.jpg" % num
            #     cv2.imwrite(filename,frame)

            # When everything is done, release the capture
            capture.release()
            cv2.destroyWindow("camera")

        # When everything is done, release the capture


# # 创建load_and_align_data网络
# print('Creating networks and loading parameters')
# with tf.Graph().as_default():
#     gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
#     sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
#     with sess.as_default():
#         pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)


# 修改版load_and_align_data
# 传入rgb np.ndarray
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

#---------------------------------------------------------界面可以封装成类
class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,size=(1350,700))

        # self.InitMenu()
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
    # def InitMenu(self):
#     #     menubar = wx.MenuBar()
#     #
#     #     fileMenu = wx.Menu()
#     #     newitem = wx.MenuItem(fileMenu, wx.ID_NEW, text="New", kind=wx.ITEM_NORMAL)
#     #     # newitem.SetBitmap(wx.Bitmap("./img/new.bmp"))
#     #     fileMenu.AppendItem(newitem)
#     #
#     #     fileMenu.AppendSeparator()
#     #
#     #     editMenu = wx.Menu()
#     #     copyItem = wx.MenuItem(editMenu, 100, text="copy", kind=wx.ITEM_NORMAL)
#     #     # copyItem.SetBitmap(wx.Bitmap("copy.bmp"))
#     #
#     #     editMenu.AppendItem(copyItem)
#     #     cutItem = wx.MenuItem(editMenu, 101, text="cut", kind=wx.ITEM_NORMAL)
#     #     # cutItem.SetBitmap(wx.Bitmap("cut.bmp"))
#     #
#     #     editMenu.AppendItem(cutItem)
#     #     pasteItem = wx.MenuItem(editMenu, 102, text="paste", kind=wx.ITEM_NORMAL)
#     #     # pasteItem.SetBitmap(wx.Bitmap("paste.bmp"))
#     #
#     #     editMenu.AppendItem(pasteItem)
#     #     fileMenu.AppendMenu(wx.ID_ANY, "Edit", editMenu)
#     #     fileMenu.AppendSeparator()
#     #
#     #     radio1 = wx.MenuItem(fileMenu, 200, text="Radio1", kind=wx.ITEM_RADIO)
#     #     radio2 = wx.MenuItem(fileMenu, 300, text="radio2", kind=wx.ITEM_RADIO)
#     #
#     #     fileMenu.AppendItem(radio1)
#     #     fileMenu.AppendItem(radio2)
#     #     fileMenu.AppendSeparator()
#     #
#     #     fileMenu.AppendCheckItem(103, "Checkable")
#     #     quit = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
#     #
#     #     fileMenu.AppendItem(quit)
#     #     menubar.Append(fileMenu, '&File')
#     #
#     #     self.SetMenuBar(menubar)
#     #     # self.text = wx.TextCtrl(self, -1, style=wx.EXPAND | wx.TE_MULTILINE)
#     #     # self.Bind(wx.EVT_MENU, self.menuhandler)
#     #     # self.SetSize((350, 250))
#     #     # self.Centre()
#     #     # self.Show(True)
#     #
#     # # def menuhandler(self, event):
#     # #     id = event.GetId()
#     # #     if id == wx.ID_NEW:
#     # #         self.text.AppendText("new" + "\n")

def begin():
    app = wx.App()
    Example(None, title='2019毕设-人员管理页面')
    app.MainLoop()

# if __name__=='__main__':
#     begin()




if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：, args=()
    q = Queue()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pw = Process(target=begin)
    pr = Process(target=tfModelBuild)
    # 启动子进程pw，写入:, args=(q,)
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    # pr.terminate()