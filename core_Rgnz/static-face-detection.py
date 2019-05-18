from scipy import misc
import tensorflow as tf
import detect_face
import cv2
import matplotlib.pyplot as plt
# %pylab inline     #jupter真难用不搞了先写完
# def draw_rectangle_in_camera(self,frame):
minsize = 20 # minimum size of face
threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
factor = 0.709 # scale factor
gpu_memory_fraction=1.0


print('Creating networks and loading parameters')

with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        #sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        sess = tf.Session(config=tf.ConfigProto(device_count = {'GPU': 0}, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess,r'./align')
# , None
image_path = r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_yueqingming\yueqingming_8.jpg'   #哈哈哈高级水印

img = misc.imread(image_path)#借用MIT大佬们的模块
bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
nrof_faces = bounding_boxes.shape[0]#存下人脸数
print('找到人脸数目为：{}'.format(nrof_faces))

print(bounding_boxes)

#加入一个人脸ID，提取feature map


crop_faces=[]
for face_position in bounding_boxes:
    face_position=face_position.astype(int)
    print(face_position[0:4])
    cv2.rectangle(img, (face_position[0], face_position[1]), (face_position[2], face_position[3]), (0, 255, 0), 2)

cv2.namedWindow("camera", 1)
cv2.imshow('camera', img)
