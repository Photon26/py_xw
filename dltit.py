# import cv2
# import os
# import numpy as np
# import time
#
# stime = time.time()
# Inputfolder = "H:/py_xw/raw_img"
# os.chdir(Inputfolder)
#
# a = os.listdir(Inputfolder)
# # a.sort(key=lambda x: int(x.split('.')[0]))
# # for f in a:
# f = "z.jpg"
# frame = cv2.imread(f)
# frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#
# # logger = open("tst.txt", "w")
#
# # height, width = frame.shape[:2]
# # size = (int(width * 0.5), int(height * 0.5))
# # img = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
# # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
#
# roi = frame[561: 884, 1763: 1920, :]
# b = roi[:,:,0].astype(np.int16)
# r = roi[:,:,2].astype(np.int16)
# cv2.imshow("t",roi)
# cv2.waitKey(0)
#
# h,w = b.shape[:]
# # mask = np.zeros((h,w))
# # mask[:,:]=r[:,:]-b[:,:]
# mask = r-b
#
# # print(np.max(mask), np.min(mask))
# mask[mask<100]=0
# mask[mask>=100]=255
#
# # logger.write(str(np.sum(mask)/255/(h*w))+"\n")
# print(str(np.sum(mask)/255/(h*w))+"\n")
#
# # cv2.imshow("pic", mask.astype(np.uint8))
# # cv2.waitKey(0)
# # print(time.time()-stime)

from firetime_Check import firetime_Check
import cv2
import os

Inputfolder = "H:/data/fortst/y_p_louder_128"
os.chdir(Inputfolder)

a = os.listdir(Inputfolder)
a.sort(key=lambda x: int(x.split('.')[0]))
for f in a:
# f = "1420.jpg"
    frame = cv2.imread(f)
    print(f, firetime_Check(frame, "y"))