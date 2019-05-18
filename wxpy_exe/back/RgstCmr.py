import cv2
import os
from PIL import Image,ImageDraw,ImageFont
from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import copy
import argparse
import facenet
import align.detect_face
import detect_face
from scipy import misc

import time
import wx
from threading import Thread
from wx.lib.pubsub import pub
#找不到Publisher():出现这个错误是正常的
#现在版本已经将这个类私有化，
#将Publisher的subscribe与sendMessage复制给了subscribe与sendMessage变量。
# 所以我们这样引入头：from wx.lib.pubsub import pub，同时将所有的Publisher()改为pub。

#wxpython是通过wx.CallAfter给主程序推入事件，通过PubSub与主程序传递数据。

########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()  # start the thread

    # ----------------------------------------------------------------------
    def run(self):  #run是硬核Thread的函数。。
        """Run Worker Thread."""
        # This is the code executing in the new thread.
#===============================================================================
# 加入摄像头计算
#===============================================================================
        capture = cv2.VideoCapture(0)
        timer = 0
        num = 0
        imgCount = 0
        # 框参数

        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor
        gpu_memory_fraction = 1.0

        print('Creating networks and loading parameters')
        # align_folder = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\align'
        align_folder=r'..\..\core_Rgnz\align'
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            # sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            sess = tf.Session(config=tf.ConfigProto(device_count={'GPU': 0}, log_device_placement=False))
            with sess.as_default():
                pnet, rnet, onet = detect_face.create_mtcnn(sess, align_folder)

        while True:
            ret, frame = capture.read()
            # rgb frame np.ndarray 480*640*3
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 获取 判断标识 bounding_box crop_image
            timer += 1

            print(timer)

            frame = Image.fromarray(rgb_frame)

            draw = ImageDraw.Draw(frame)  # 图片上打印
            font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            draw.text((0, 0), "请在保证识别到人脸的情况下，按下's'键进行照片注册", (255, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

            # PIL图片转cv2 图片
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            frame = np.array(frame)
            image_path = frame
            img = image_path
            bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
            nrof_faces = bounding_boxes.shape[0]  # 存下人脸数
            print('找到人脸数目为：{}'.format(nrof_faces))

            print(bounding_boxes)

            # 加入一个人脸ID，提取feature map

            crop_faces = []
            for face_position in bounding_boxes:
                face_position = face_position.astype(int)
                print(face_position[0:4])
                cv2.rectangle(img, (face_position[0], face_position[1]), (face_position[2], face_position[3]),
                              (0, 255, 0), 2)

            cv2.namedWindow("camera", 1)
            cv2.imshow('camera', img)

            key = cv2.waitKey(3)

            if key == 27:
                # esc键退出/隐藏
                print("esc break...")
                break

            if key == ord('s'):
                # 保存一张图像
                num = num + 1

                # 确保路径存在
                # savePath = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\test'
                savePath=r'..\..\core_Rgnz\train_dir\test'
                folder = os.path.exists(savePath)
                if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(savePath)  # makedirs 创建文件时如果路径不存在会创建这个路径
                    print("---  new folder...  ---")
                    print("---  OK  ---")
                else:
                    print("---  There is this folder!  ---")

                # 写入图像
                filename = r"\test_%s.jpg" % (num)
                fileFullname = savePath + r"\test_%s.jpg" % (num)
                cv2.imwrite(fileFullname, frame)
                clipTips='写入了test_%s.jpg!!' %num
                wx.CallAfter(self.postTime, clipTips)

        # When everything is done, release the capture
        wx.CallAfter(pub.sendMessage, "update", msg=3)
        capture.release()
        cv2.destroyWindow("camera")


#====================================================================================
#计算结束
#====================================================================================

        # for i in range(6):
        #     time.sleep(10)
        #     wx.CallAfter(self.postTime, i) #CallAfter给主程序推入事件,i为信息。
        # time.sleep(5)
        # # wx.CallAfter(pub.sendMessage, "update", "Thread finished!")
        # wx.CallAfter(pub.sendMessage, "update", msg="Thread finished!")

        # ----------------------------------------------------------------------

    def postTime(self, tips):
        """
        Send time to GUI
        """
        # amtOfTime = (amt + 1) * 10
        # pub.sendMessage("update", amtOfTime)
        pub.sendMessage("update", msg=tips)

    ########################################################################


class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="开一个新的摄像头线程~")
        self.btn = btn = wx.Button(panel, label="点这里开摄像头。")

        btn.Bind(wx.EVT_BUTTON, self.onButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

        # create a pubsub receiver
        pub.subscribe(self.updateDisplay, "update")
        #pub是和主程序传递数据的，执行函数，这个函数的暗号名字是什么。

        # ----------------------------------------------------------------------

    def onButton(self, event):
        """
        Runs the thread
        """
        TestThread()    #这里开了一个线程
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        btn.Disable()   #然后让按钮变得不可以点

        # ----------------------------------------------------------------------

    def updateDisplay(self, msg):
        #然后主线程的数据就放在msg里。
        """
        Receives data from thread and updates the display
        """
        # t = msg.data
        t = msg
        if isinstance(t, str):
            self.displayLbl.SetLabel("%s" % t)
        else:
            self.displayLbl.SetLabel("多多多你是个大佬呀！！" )
            self.btn.Enable()

        # ----------------------------------------------------------------------


# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()