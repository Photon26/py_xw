import cv2
import numpy as np
from img_Ini import img_ini
import os

count = 0
Inputfolder = "./raw_img"
a = os.listdir(Inputfolder)
for f in a:

    raw = cv2.imread(Inputfolder+'/'+f)
    raw_ = img_ini(raw, mode="d", name="mz")

    #   Segmentation
    colsum = np.sum(raw_, 0)
    colsum[colsum<2] = 0
    colsum[colsum>2] = 1

    flag = 0
    m = []
    n = []

    for i in range(0, len(colsum)):
        if colsum[i] == 1 and flag != 1:
            flag = 1
            m.append(i)
        elif colsum[i] == 0 and flag == 1:
            flag = 0
            n.append(i)

    img = []

    for j in range(0, len(m)):
        begin = m[j]
        end = n[j]
        tmp = raw_[:, begin : end]
        cv2.imwrite(str(count)+".jpg", tmp)
        count = count+1


import shutil
for i in range(0,10):
    shutil.rmtree(str(i))
    os.mkdir(str(i))