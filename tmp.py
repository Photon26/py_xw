from img_Ini import img_ini
import os
import cv2
import numpy as np
import xlwt

Inputfolder = "./video3sup"

a = os.listdir(Inputfolder)
a.sort(key=lambda x: int(x.split('.')[0]))

workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('xy_')

#   Read in models
modeldir = "./model"
model = []
for i in range(0, 10):
    img = cv2.imread(modeldir+'/'+str(i)+".jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #   Binarization
    img[img < 240] = 0
    img[img >= 240] = 1

    # img_ = np.zeros((75,55)).astype('int')
    # s1, s2, _ = np.shape(img)
    # img_[:s1, :s2] = img[:, :, 0]

    model.append(img)

count = 0
for f in a:
    rawimg = cv2.imread(Inputfolder+'/'+f)
    frame0 = img_ini(rawimg)
    #   Binarization
    frame0[frame0<240] = 0
    frame0[frame0>=240] = 1

    #   Segmentation
    colsum = np.sum(frame0, 0)
    colsum[colsum < 2] = 0
    colsum[colsum >= 2] = 1

    flag = 0
    m = []
    n = []

    recog_num = 0

    for i in range(0, len(colsum)):
        if colsum[i] == 1 and flag != 1:
            flag = 1
            m.append(i)
        elif colsum[i] == 0 and flag == 1:
            flag = 0
            n.append(i)

    if m:
        #   Recognize
        for j in range(0, len(m)):
            begin = m[j]
            end = n[j]

            if end-begin >=55:
                recog_num = 0
                break
            else:
                tmp = frame0[:, begin: end]

                tmp_ = np.zeros((75, 55)).astype('int')
                s1, s2 = np.shape(tmp)
                tmp_[:s1, :s2] = tmp

                # mask = model[:] & tmp_
                mask = (model[:] == tmp_).astype('int')

                # print(np.shape(mask))
                sum1 = np.sum(mask, 1)
                sum2 = np.sum(sum1, 1)  # output 1xn
                index = np.argmax(sum2)
                # print(index)

                recog_num = 10*recog_num+index
                continue
            break

    worksheet.write(count, 0, label=str(recog_num))
    count = count+1

workbook.save('tst.xls')


