import cv2
from PIL import Image,ImageDraw,ImageFont
import tensorflow as tf
import numpy as np
import os
import core_Rgnz.facenet as facenet
import core_Rgnz.align.detect_face as ad
from scipy import misc

import wx
from threading import Thread

from pubsub import pub

#找不到Publisher():出现这个错误是正常的
#现在版本已经将这个类私有化，
#将Publisher的subscribe与sendMessage复制给了subscribe与sendMessage变量。
# 所以我们这样引入头：from wx.lib.pubsub import pub，同时将所有的Publisher()改为pub。

#wxpython是通过wx.CallAfter给主程序推入事件，通过PubSub与主程序传递数据。

########################################################################
class CameraThread(Thread):
    """Test Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self,mode):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()  # start the thread
        self.mode=mode
        self.cameraShow = 0

        #mode有: login \ spy \

    # ----------------------------------------------------------------------
    def run(self):  #run是硬核Thread的函数。。
        """Run Worker Thread."""
        # This is the code executing in the new thread.
#===============================================================================
# 加入摄像头计算
#===============================================================================
        # 创建load_and_align_data网络
        print('Creating networks and loading parameters')

        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                pnet, rnet, onet = ad.create_mtcnn(sess, None)

        with tf.Graph().as_default():
            with tf.Session() as sess:
                # model = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\20170512-110547'
                model=r'..\..\..\core_Rgnz\20170512-110547'
                facenet.load_model(model)

                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

                image = []
                nrof_images = 0

                # 这里要改为自己emb_img文件夹的位置
                # emb_dir='/home/wind/facenet-master/src/emb_img'\%s' %str(self.user_name)\usr_yueqingming
                # emb_dirs = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img'
                emb_dirs=r'..\..\..\core_Rgnz\emb_img'
                # spySavePath=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\spy_img'
                spySavePath=r'..\..\..\core_Rgnz\spy_img'
                all_obj = []
                for emb_dir in os.listdir(emb_dirs):
                    for i in os.listdir(emb_dirs + r'\%s' % emb_dir):
                        all_obj.append(i)
                        img = misc.imread(os.path.join(emb_dirs + r'\%s' % emb_dir, i), mode='RGB')
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

                timer = 0
                # num = 10
                spyNum=0
                for i in os.listdir(spySavePath):
                    spyNum +=1
                    #如果不重的话，得用文件夹记录最大数字。。。。。。。

                picRgnz = 0

                # cv2.namedWindow("camera", 1)
                if self.mode=='spy':
                    wx.CallAfter(pub.sendMessage, "closeDia", msg='Tips_Close')

                while True:
                    print("whileRecycle-cameraShow:%d" % self.cameraShow)
                    print('self-mode!!:%s' %self.mode)

                    ret, frame = capture.read()

                    # rgb frame np.ndarray 480*640*3
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # 获取 判断标识 bounding_box crop_image
                    mark, bounding_box, crop_image = load_and_align_data(rgb_frame, 160, 44, pnet, rnet, onet)
                    timer += 1

            #写上标注=============================================================
                    if(self.mode=='spy'):
                        frame = Image.fromarray(rgb_frame)

                        draw = ImageDraw.Draw(frame)  # 图片上打印
                        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
                        draw.text((0, 0), "请在保证识别到人脸的情况下，按下's'键进行照片记录", (0, 255, 0),
                                  font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

                        # PIL图片转cv2 图片
                        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                        frame = np.array(frame)
            #=====================================================================

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

                            usr_name = fin_obj[rec_position].split('_')
                            if (self.mode=='login' and usr_name[0] != 'unknow' and self.cameraShow==1):
                                if (self.user_name == usr_name[1] and self.cameraShow == 1):
                                    picRgnz += 1

                        if (self.cameraShow):
                            cv2.namedWindow("camera", 1)
                            cv2.imshow('camera', frame)

                    if (picRgnz == 15):     #15次验证通过，就返回~
                        wx.CallAfter(self.postMsg, 'Close_Login')
                        break


                    self.key = cv2.waitKey(3)
                    # # 如果是SPY，就允许写群体文件
                    if (self.key == ord('s') and self.mode == 'spy'):
                        # 保存一张图像
                        spyNum = spyNum + 1
                        # filename = "frames_%s.jpg" % num
                        # cv2.imwrite(filename,frame)
                        folder = os.path.exists(spySavePath)
                        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                            os.makedirs(spySavePath)  # makedirs 创建文件时如果路径不存在会创建这个路径
                            print("---  new folder...  ---")
                            print("---  OK  ---")
                        else:
                            print("---  There is this folder!  ---")

                        # 写入图像
                        fileFullname = spySavePath + r"\spyImg_%s.jpg" % spyNum
                        cv2.imwrite(fileFullname, frame)
                        wx.CallAfter(pub.sendMessage, "update", msg="群体文件写入！！\spyImg_%s.jpg" % spyNum)


                    if self.key == 27:
                        # esc键退出/隐藏
                        print("esc break...")
                        break
                        # cv2.destroyWindow('camera')
                        # self.cameraShow = 0

                capture.release()
                cv2.destroyWindow("camera")


#====================================================================================
#login的计算结束
#====================================================================================
        # for i in range(6):
        #     time.sleep(10)
        #     wx.CallAfter(self.postTime, i) #CallAfter给主程序推入事件,i为信息。
        # time.sleep(5)
        # # wx.CallAfter(pub.sendMessage, "update", "Thread finished!")
        # wx.CallAfter(pub.sendMessage, "update", msg="Thread finished!")

        # ----------------------------------------------------------------------

    def getLoginParams(self,user_name,cameraShow,now_usr_name,now_usr_acc):
        self.user_name = user_name
        self.cameraShow = cameraShow
        self.now_usr_name = now_usr_name
        self.now_usr_acc = now_usr_acc

    #, user_name
    def getSpyParams(self, cameraShow, now_usr_name, now_usr_acc):
        # self.user_name = user_name
        self.cameraShow = cameraShow
        self.now_usr_name = now_usr_name
        self.now_usr_acc = now_usr_acc
        print("getSpyParams-cameraShow:%d" %self.cameraShow)

        #user_name,cameraShow,now_usr_name,

    def postMsg(self, tips):
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
        ct=CameraThread('spy')    #这里开了一个线程
        ct.getSpyParams(1,'岳清明','yueqingming')
        # ct = CameraThread('login')  # 这里开了一个线程
        # ct.getLoginParams("岳清明",1,"岳清明",'yueqingming')
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
        # else:
        #     self.displayLbl.SetLabel("多多多你是个大佬呀！！" )
        #     self.btn.Enable()

        # ----------------------------------------------------------------------


#----------------------------公共部分--------------------------------------------
def load_and_align_data(img, image_size, margin, pnet, rnet, onet):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    img_size = np.asarray(img.shape)[0:2]

    # bounding_boxes shape:(1,5)  type:np.ndarray
    bounding_boxes, _ = ad.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)

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







# Run the program
if __name__ == "__main__":
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
    gpu_memory_fraction = 1.0


    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()