import xlwt
import cv2
from img_Ini import img_ini
from num_Recog import num_Recog
import os
import numpy as np
import time

st = time.time()
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('raw')

#   Read in models
modeldir = "./model"
model = []
for i in range(0, 10):
    img = cv2.imread(modeldir+'/'+str(i)+".jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #   Binarization
    img[img < 240] = 0
    img[img >= 240] = 1
    model.append(img)
model = np.array(model)

# Inputfolder = "D:/Photon/Documents/MATLAB/video3sup"
Inputfolder = "./raw_img/0829"

#   Read in img
a = os.listdir(Inputfolder)
a.sort(key=lambda x: int(x.split('.')[0]))

count = 0

for f in a:
    img = cv2.imread(Inputfolder+"/"+f)
    img0 = img_ini(img, mode="d")
    num = num_Recog(img0, model)
    worksheet.write(count,0, label = str(num))
    # print(f, num)
    count = count+1
    if f == "12905.jpg":
        break

print(time.time()-st)
workbook.save('tst.xls')
print(time.time()-st)