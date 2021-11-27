import cv2
import numpy as np
import os

name = "m"
dir = "./model_m"
if not os.path.exists(dir):
    os.makedirs(dir)

if name == "y":
    # area = (63, 40)
    area = (88, 55)
elif name == "d":
    area = (85, 55)
# elif name == "m":
#     area = (55, 35)
elif name == "q":
    area = (60, 40)
elif name =="z":
    area = (75, 55)
elif name == "s":
    area = (45, 42)
elif name == "mj":
    area = (90, 55)
elif name == "m":
    area = (60, 45)
elif name == "j":
    area = (55, 45)
elif name == "k":
    area = (30, 25)
elif name == "c":
    area = (90, 55)
elif name == "d":
    area = (40, 30)
elif name == "e":
    area = (55, 35)
elif name == "g":
    area = (55, 35)    #   low resolution
    # area = (75, 55)
elif name == "f":
    area = (80, 50)
# elif name == "x":
#     area = (80, 55)
elif name == "h":
    area = (55, 35)
elif name == "r":
    area = (80, 55)
elif name == "t":
    area = (90, 55)
elif name == "t1":
    area = (90, 55)
elif name == "x":
    area = (70, 35)
elif name == "y1":
    area = (50, 35)
elif name == "w":
    area = (70, 55)
elif name == "w":
    area = (60, 45)
elif name == "qx":
    # area = (55, 45)       #   low resolution
    area = (75, 55)
else:
    area = (70, 55)

for i in range(0,10):

    InputFolder = "./"+str(i)
    a = os.listdir(InputFolder)
    imlist = []
    for f in a:
        img_ = np.zeros(area).astype('int')
        frame = cv2.imread(InputFolder + "/" + f)
        s1, s2, _ = np.shape(frame)
        img_[:s1, :s2] = frame[:, :, 0]
        imlist.append(img_)

    imlist = np.array(imlist)
    imlist_ = np.mean(imlist, 0)
    imlist_ = np.round(imlist_).astype("int")
    imlist_[imlist_<150]=0
    imlist_[imlist_>150]=255

    cv2.imwrite(dir+'/'+str(i)+".jpg", imlist_)
