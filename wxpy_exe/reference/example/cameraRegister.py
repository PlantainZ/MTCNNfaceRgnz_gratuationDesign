import register_cropFace
import os
import core_Rgnz.detect_face as detect_face
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image,ImageFont,ImageDraw
import wx
from threading import Thread
from pubsub import pub as Publisher

#../../../core_Rgnz/align

#====================以下是注册操作的框实现部分====================================
class cameraRgst(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()  # start the thread

    def run(self):
        capture = cv2.VideoCapture(0)
        timer = 0
        num = 0

        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor
        gpu_memory_fraction = 1.0

        self.cameraShow = 0

        # if self.breakSet=='no':
        print('Creating networks and loading parameters')
        # align_folder = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\align'
        align_folder=r'..\..\..\core_Rgnz\align'
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
            draw.text((0, 0), "请在保证识别到人脸的情况下，按下's'键进行照片注册", (0, 255, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

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

            for face_position in bounding_boxes:
                face_position = face_position.astype(int)
                print(face_position[0:4])
                cv2.rectangle(img, (face_position[0], face_position[1]), (face_position[2], face_position[3]),
                              (0, 255, 0), 2)

            if(self.cameraShow==1):
                cv2.namedWindow("camera", 1)
                cv2.imshow('camera', img)

                self.key = cv2.waitKey(3)

                if self.key == 27 :
                    # esc键退出/隐藏
                    print("esc break...")
                    # self.add_affirm.SetLabel('注册')#这里，点注册就裁小图片。
                    register_cropFace.cropFace('usr_%s' % self.usr_acc)
                    # wx.CallAfter(pub.sendMessage, "rgst", msg="rgst_end")
                    wx.CallAfter(Publisher.sendMessage, "rgst", msg="rgst_end")
                    #这句是专门为修改资料的时候补录图片（图片展示界面）准备的，
                    #当摄像头关闭的时候能够刷新一下图片详细界面，显示新录入的图片
                    break

                if self.key == ord('s'):
                    # 保存一张图像
                    self.trainNum=self.trainNum+1
                    # 确保路径存在


                    # 写入图像
                    fileFullname = self.savePath + r"\%s_%s.jpg" % (self.usr_acc,self.trainNum)
                    cv2.imwrite(fileFullname, frame)

                    wx.CallAfter(self.postMsg, r"\%s_%s.jpg in!" % (self.usr_acc,self.trainNum))
            # When everything is done, release the capture
            #     if self.key == 27:
            #         break
        capture.release()
        cv2.destroyWindow("camera")
        print('Thread End!==============================================')

#
    def getRegisterParams(self,usr_acc,cameraShow):
        # self.user_name = user_name
        self.cameraShow = cameraShow
        # self.now_usr_name = now_usr_name
        self.usr_acc = usr_acc
        # self.savePath = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_%s' % self.usr_acc
        self.savePath=r'..\..\..\core_Rgnz\train_dir\usr_%s' % self.usr_acc
        self.trainNum = 0

        folder = os.path.exists(self.savePath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.savePath)  # makedirs 创建文件时如果路径不存在会创建这个路径
        for i in os.listdir(self.savePath):
            self.trainNum += 1

    def breakSet(self):
        self.key=27

    def postMsg(self, tips):
        """
        Send time to GUI
        """
        # pub.sendMessage("rgst", msg=tips)
        Publisher.sendMessage("rgst", msg=tips)




#测试
if __name__=='__main__':
    obj=cameraRgst()
    obj.getRegisterParams('test',cameraShow=1)