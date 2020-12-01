import numpy as np

def num_Recog(frame0, model, name = "l"):
    """

    ·   Input:
    ·    img: initialized img (Area filting done)
    ·    model: [y, x ,10] nparray
    ·   Output:
    ·    num: recognized number
    ·       (If no number detected/number block is too long, return 0.)

    """

    #   Binarization
    frame0[frame0<240] = 0
    frame0[frame0>=240] = 1

    #   Segmentation
    colsum = np.sum(frame0, 0)
    colsum[colsum < 1] = 0
    colsum[colsum >= 1] = 1

    flag = 0
    m = []
    n = []

    recog_num = 0

    if name == "y":
        area = (54, 40)
    elif name =="z":
        area = (75, 55)
    elif name == "s":
        area = (45, 42)
    elif name == "j":
        area = (55, 45)
    elif name == "m":
        area = (55, 35)
    elif name == "mz":
        area = (50, 45)
    elif name == "k":
        area = (30, 25)
    elif name =="d":
        area = (40, 30)
    elif name =="g":
        area = (55, 35)     #   low resolution
        # area = (75, 55)
    elif name == "f":
        area = (80, 50)
    elif name == "x":
        area = (80, 55)
    elif name == "h":
        area = (55, 35)
    elif name == "r":
        area = (80, 55)
    elif name == "q":
        area = (60, 40)
    elif name == "qx":
        # area = (55, 45)       #   low resolution
        area = (75, 55)
    else:
        area = (75, 55)
    for i in range(0, len(colsum)):
        if colsum[i] == 1 and flag != 1:
            if i == len(colsum):
                continue
            else:
                flag = 1
                m.append(i)
        elif colsum[i] == 0 and flag == 1:
            flag = 0
            n.append(i)

    if m:
        #   Recognize
        if len(m) != len(n):
            recog_num = 0
            return recog_num
        else:
            for j in range(0, len(m)):
                begin = m[j]
                end = n[j]

                if end-begin >area[1]:  #   The num block is too large.
                    # recog_num = 0
                    # return recog_num
                    continue

                else:
                    tmp = frame0[:, begin: end]
                    tmp_ = np.zeros(area).astype('int')
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
    return recog_num

if __name__ == '__main__':
    import cv2
    from img_Ini import img_ini
    import os

    modeldir = "./model_j"
    model = []
    for i in range(0, 10):
        img = cv2.imread(modeldir + '/' + str(i) + ".jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #   Binarization
        img[img < 240] = 0
        img[img >= 240] = 1
        model.append(img)
    model = np.array(model)
    a = os.listdir("raw_img")
    a.sort(key=lambda x: int(x.split('.')[0]))
    for f in a:
    # f = "7241.jpg"
        img = cv2.imread("./raw_img/"+f)
        img_ = img_ini(img, mode="d", name="j")
        num = num_Recog(img_, model, name="j")
        print(num)