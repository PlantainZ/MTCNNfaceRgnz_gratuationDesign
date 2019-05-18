from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
import calculate_dection_single_face as cdf

def cameraOpen():
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
            #model='/home/wind/facenet-master/src/models/20170512-110547/'
            model = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\20170512-110547'
            savePath=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\pic_others'
            facenet.load_model(model)
    
            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")


            image=[]
            nrof_images=0

            # 这里要改为自己emb_img文件夹的位置
            #emb_dir='/home/wind/facenet-master/src/emb_img'
            emb_dir=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img'
            all_obj=[]
            for i in os.listdir(emb_dir):
                all_obj.append(i)
                img = misc.imread(os.path.join(emb_dir,i), mode='RGB')
                prewhitened = facenet.prewhiten(img)
                image.append(prewhitened)
                nrof_images=nrof_images+1

            images=np.stack(image)
            feed_dict = { images_placeholder: images, phase_train_placeholder:False }
            compare_emb = sess.run(embeddings, feed_dict=feed_dict) 
            compare_num=len(compare_emb)

            #开启ip摄像头
            # video="http://admin:admin@192.168.0.107:8081/"   #此处@后的ipv4 地址需要修改为自己的地址
            # 参数为0表示打开内置摄像头，参数是视频文件路径则打开视频
            #capture =cv2.VideoCapture(video)
            capture =cv2.VideoCapture(0)
            cv2.namedWindow("camera",1)
            timer=0
            num=16
            while True:
                ret, frame = capture.read() 

                # rgb frame np.ndarray 480*640*3
                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                
                # 获取 判断标识 bounding_box crop_image
                mark,bounding_box,crop_image=load_and_align_data(rgb_frame,160,44,pnet, rnet, onet)
                timer+=1
                if(1):
                    
                    print(timer)
                    if(mark):
                        feed_dict = { images_placeholder: crop_image, phase_train_placeholder:False }
                        emb = sess.run(embeddings, feed_dict=feed_dict)
                        temp_num=len(emb)

                        fin_obj=[]
                        print(all_obj)

                        # 为bounding_box 匹配标签
                        for i in range(temp_num):
                            dist_list=[]
                            for j in range(compare_num):
                                dist = np.sqrt(np.sum(np.square(np.subtract(emb[i,:], compare_emb[j,:]))))
                                dist_list.append(dist)
                            min_value=min(dist_list)
                            if(min_value>0.65):
                                fin_obj.append('unknow')
                            else:
                                fin_obj.append(all_obj[dist_list.index(min_value)])    


                        # 在frame上绘制边框和文字
                        for rec_position in range(temp_num):                        
                            cv2.rectangle(frame,(bounding_box[rec_position,0],bounding_box[rec_position,1]),(bounding_box[rec_position,2],bounding_box[rec_position,3]),(0, 255, 0), 2, 8, 0)

                            cv2.putText(
                                frame,
                            fin_obj[rec_position], 
                            (bounding_box[rec_position,0],bounding_box[rec_position,1]),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                            0.8, 
                            (0, 0 ,255), 
                            thickness = 2, 
                            lineType = 2)

                        cv2.imshow('camera',frame)


                # cv2.imshow('camera',frame)
                key = cv2.waitKey(3)
                if key == 27:
                    #esc键退出
                    print("esc break...")
                    break

                if key == ord(' '):
                    # 保存一张图像
                    num = num+1
                    filename = savePath+"frames_%s.jpg" % num
                    cv2.imwrite(filename,frame)
                    cdf.dection()
                    #保存它的切割形态


            
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
def load_and_align_data(img, image_size, margin,pnet, rnet, onet):

    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor

    img_size = np.asarray(img.shape)[0:2]

    # bounding_boxes shape:(1,5)  type:np.ndarray
    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)

    # 如果未发现目标 直接返回
    if len(bounding_boxes) < 1:
        return 0,0,0

    # 从数组的形状中删除单维度条目，即把shape中为1的维度去掉
    # det = np.squeeze(bounding_boxes[:,0:4])
    det=bounding_boxes

    print('det shape type')
    print(det.shape)
    print(type(det))

    det[:,0] = np.maximum(det[:,0]-margin/2, 0)
    det[:,1] = np.maximum(det[:,1]-margin/2, 0)
    det[:,2] = np.minimum(det[:,2]+margin/2, img_size[1]-1)
    det[:,3] = np.minimum(det[:,3]+margin/2, img_size[0]-1)

    det=det.astype(int)
    crop=[]
    for i in range(len(bounding_boxes)):
        temp_crop=img[det[i,1]:det[i,3],det[i,0]:det[i,2],:]
        aligned=misc.imresize(temp_crop, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        crop.append(prewhitened)

    # np.stack 将crop由一维list变为二维
    crop_image=np.stack(crop)  

    return 1,det,crop_image



# #传入切割图片！
# def dection():
#     # 将目标图片文件夹下的图片地址append进list,传入load_and_align_data(),对图片进行切割（因为其图片参数为list）
#     # 这里的位置改为test_img文件夹的绝对路径
#     img_dir = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_yueqingming'
#     img_path_set = []
#     for file in os.listdir(img_dir):
#         single_img = os.path.join(img_dir, file)
#         print(single_img)
#         print('loading...... :', file)
#         img_path_set.append(single_img)
#
#     images = cropped160img(img_path_set, 160, 44, 1.0)
#
#     # 改为emb_img文件夹的绝对路径
#     emb_dir = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\emb_img'
#
#     if (os.path.exists(emb_dir) == False):
#         os.mkdir(emb_dir)
#
#     count = 0
#     for file in os.listdir(img_dir):
#         misc.imsave(os.path.join(emb_dir, file), images[count])
#         count = count + 1
#
#
# #对图片的切割操作
# def cropped160img(image_paths, image_size, margin, gpu_memory_fraction):
#     minsize = 20  # minimum size of face
#     threshold = [0.6, 0.7, 0.7]  # three steps's threshold
#     factor = 0.709  # scale factor
#
#     print('Creating networks and loading parameters')
#     with tf.Graph().as_default():
#         gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
#         sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
#         with sess.as_default():
#             pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
#
#     tmp_image_paths = copy.copy(image_paths)
#     img_list = []
#     for image in tmp_image_paths:
#         print(image)
#         img = misc.imread(os.path.expanduser(image), mode='RGB')
#         # img = misc.imread(image, mode='RGB')
#         img_size = np.asarray(img.shape)[0:2]
#         bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
#         if len(bounding_boxes) < 1:
#             image_paths.remove(image)
#             print("can't detect face, remove ", image)
#             continue
#         det = np.squeeze(bounding_boxes[0, 0:4])
#         bb = np.zeros(4, dtype=np.int32)
#         bb[0] = np.maximum(det[0] - margin / 2, 0)
#         bb[1] = np.maximum(det[1] - margin / 2, 0)
#         bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
#         bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
#         cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
#
#         # 根据cropped位置对原图resize，并对新得的aligned进行白化预处理
#         aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
#         prewhitened = facenet.prewhiten(aligned)
#         img_list.append(prewhitened)
#     images = np.stack(img_list)
#     return images



if __name__=='__main__':
    cameraOpen()