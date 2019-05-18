from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import tensorflow as tf
import os
import facenet
import align.detect_face

import numpy as np              # 数据处理的库numpy
import cv2                      # 图像处理的库OpenCv
import wx                       # 构造显示界面的GUI

COVER='./img/login.png'
from multiprocessing import Process

#登陆框---------------------------------------------------------------------
class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,size=(750,400))

        self.InitUI()
        self.Centre()
        self.Show()
        subProcess()

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
        self.Bind(wx.EVT_BUTTON,None, buttonOk)
        # self.Bind(wx.EVT_BUTTON, self.picCTest, buttonClose)


        #sizer嵌入组件----------------------------------------------------
        sizer.Add(buttonOk, pos=(6, 5), flag=wx.TOP, border=5)
        sizer.Add(buttonClose, pos=(6,7), flag=wx.TOP, border=5)
        sizer.Add(nmSizer, pos=(11, 1), flag=wx.ALL, border=20)
        self.panel.SetSizerAndFit(sizer)






#========================================================================
#camera 框
#=======================================================================
class subFrame(wx.Frame):
    def __init__(self):
        super(subFrame, self).__init__(parent=None, title='摄像头展示', size=(850, 400))

        self.panel = wx.Panel(self)
        image_cover = wx.Image(COVER, wx.BITMAP_TYPE_ANY).Scale(350, 300)
        # 显示图片在panel上
        self.bmp = wx.StaticBitmap(self.panel, -1, wx.Bitmap(image_cover))

        start_button = wx.Button(self.panel, label='Start')
        # close_button = wx.Button(self.panel, label='Close')
        text = wx.StaticText(self.panel, label="  ")

        self.Bind(wx.EVT_BUTTON, None, self.panel)
        # self.Bind(wx.EVT_BUTTON, None, close_button)
        # 这里两个None是触发事件函数

        # 基于GridBagSizer的界面布局
        # 先实例一个对象
        self.grid_bag_sizer = wx.GridBagSizer(hgap=6, vgap=5)
        # # 注意pos里面是先纵坐标后横坐标| wx.ALIGN_CENTER_VERTICAL
        self.grid_bag_sizer.Add(self.bmp, pos=(0, 0), flag=wx.ALL | wx.EXPAND, span=(4, 4), border=5)
        self.grid_bag_sizer.Add(start_button, pos=(4, 1), flag=wx.LEFT, span=(1, 1), border=45)
        self.grid_bag_sizer.Add(text, pos=(5, 1), flag=wx.EXPAND | wx.TOP, border=10)
        # self.grid_bag_sizer.Add(close_button, pos=(4, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)

        self.grid_bag_sizer.AddGrowableCol(0, 1)
        # grid_bag_sizer.AddGrowableCol(0,2)

        self.grid_bag_sizer.AddGrowableRow(0, 1)
        # grid_bag_sizer.AddGrowableRow(0,2)

        self.panel.SetSizer(self.grid_bag_sizer)
        # 界面自动调整窗口适应内容
        self.grid_bag_sizer.Fit(self)
        # rec = dialog.ShowWindowModal()
        # subapp.MainLoop()
    def subFrameShow(self):
        self.Show()

    def cameraOpen(self):
        # self.bmp = bmp
        # self.grid_bag_sizer = grid_bag_sizer
        self.cnt = 0
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
                # cv2.namedWindow("camera", 1)
                timer = 0
                self.show = 0
                while True:
                    ret, frame = capture.read()
                    self.key= cv2.waitKey(3)
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
                                              (bounding_box[rec_position, 2], bounding_box[rec_position, 3]),
                                              (0, 255, 0),
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
                            cv2.imshow('camera',frame)
                            # if(self.show):
                            #     #读取图片显示到GUI上
                            #     height, width = frame.shape[:2]
                            #     # image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            #     pic = wx.Bitmap.FromBuffer(width, height, frame)
                            #     # 显示图片在panel上
                            #     self.bmp.SetBitmap(pic)
                            #     self.grid_bag_sizer.Fit(self)
                            #
                            #     if self.key == 27:
                            #         # esc键退出
                            #         print("esc break...")
                            #         break


                # if key == ord(' '):
                #     # 保存一张图像
                #     num = num+1
                #     filename = "frames_%s.jpg" % num
                #     cv2.imwrite(filename,frame)

                # When everything is done, release the capture
                capture.release()
                cv2.destroyWindow("camera")


    # def showEveryImg(self):




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


#生成登陆框
def loginFrame():
    app = wx.App()
    Example(None, title='2019毕设演示')
    app.MainLoop()

# def cameraPrepare():
#     camObj.Show()
#     camObj.show=1


def mainFrame():
    app=wx.App()
    Example(None, '2019毕设演示')
    app.MainLoop()

#第二个框------------------------------------------
def subProcess():
    pa=Process(target=subFrameInit)
    pa.start()
    # pa.join()

def subFrameInit():
    app=wx.App()
    subFrame()
    app.MainLoop()




if __name__=='__main__':
    # # q = Queue()
    # pw = Process(target=loginFrame)
    # # camObj=cameraGUI.cameraOpt()
    #
    # # pr = Process(target=cameraGUI.cameraInit)
    # # 启动子进程pw，写入:, args=(q,)
    #
    # # pr = Process(target=camObj.cameraPrepare)
    # # pr.start()
    # pw.start()
    # # 启动子进程pr，读取:
    # # pr.start()
    # # 等待pw结束:
    # pw.join()
    sf=subFrameInit()
    # app=wx.App()
    pa = Process(target=mainFrame)
    # frame2 = subFrame()

    # myframe =
    # app.SetTopWindow(myframe)
    # myframe.Show(True)
    # pr = Process(target=subFrame)
    # pr = Process(target=frame2.cameraOpen)
    # pr.start()
    pa.start()
    # pr.start()

    # 等待pw结束:
    # pa.join()
    # app.MainLoop()
