import cv2
import numpy as np

def img_ini(frame, thres = 240, mode = "x", name = "l"):
    #   Rotate, Extract interest Area, Binarization
    if name == "d":
        frame_ = frame[132: 212, 1350: 1846, :]
        # frame_ = frame[502: 840, 1760: 1919, :]
    elif name == "b":
        frame_ = frame[132: 214, 1351: 1831, :]
    elif name == "g":
        frame_ = frame[123: 174, 945: 1224, :]
    elif name == "h":
        frame_ = frame[91: 140, 934: 1225, :]
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # roi = frame[558: 885, 1759: 1919, :]
    elif name == "l":
        # frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame[188: 263, 1413: 1835, :]
    elif name == "m":
        frame_ = frame[86: 139, 920: 1220, :]
    elif name == "mj":         # mz_old
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_ = frame[1391: 1839, 1176: 1253, :]
        frame_ = cv2.rotate(frame_, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif name == "t":
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame_ = frame[1115: 1203, 77: 531, :]
        frame_ = cv2.rotate(frame_, cv2.ROTATE_180)
    elif name == "t1":
        frame_ = frame[186: 271, 1306: 1842, :]
    elif name == "qx":
        # frame_ = frame[130: 179, 942: 1221, :]        #   low resolution
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame[83: 526, 187: 261, :]
        frame_ = cv2.rotate(frame_, cv2.ROTATE_90_CLOCKWISE)
    elif name == "w":
        # frame_ = frame[122: 183, 910: 1228, :]
        # frame_ = frame[70: 119, 733: 1009, :]
        frame_ = frame[207: 265, 1017: 1341, :]
    # elif name == "x":     #   七夜
    #     # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)    #   for low resolution
    #     frame_ = frame[128: 179, 945: 1224, :]
    frame0 = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
    _, frame0 = cv2.threshold(frame0, thres, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((8, 8), np.uint8)
    #
    # frame0 = cv2.erode(frame0, kernel, iterations=1)
    if name == "y1"  or name == "t1" or name == "w":
        kernel = np.ones((2, 2), np.uint8)
        frame0 = cv2.dilate(frame0, kernel, iterations=1)
    if name == "g":
        kernel = np.ones((3, 3), np.uint8)
        frame0 = cv2.dilate(frame0, kernel, iterations=1)
        kernel = np.ones((2, 2), np.uint8)
        frame0 = cv2.erode(frame0, kernel, iterations=1)
    if mode == "d":
        # find all your connected components (white blobs in your image)
        if name == "b":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
            ystart = 20
        elif name == "d":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
            ystart = 20
        elif name == "g":
            min_size = 100        #   low resolution
            min_height = 30
            max_height = 48
            ksize = 3
            ystart = 25
        elif name == "h":
            min_size = 100
            min_height = 35
            max_height = 48
            ksize = 2
            ystart = 20
        elif name == "l":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 4
            ystart = 20
        elif name =="m":
            min_size = 100
            min_height = 35
            max_height = 51
            ksize = 2
            ystart = 20
        elif name == "mj":
            min_size = 100
            min_height = 53
            max_height = 78
            ksize = 2
            ystart = 20
        elif name == 'qx':
            # min_size = 100    #   low resolution
            # min_height = 30
            # max_height = 55
            # ksize = 2
            # ystart = 20

            min_size = 100
            min_height = 50
            max_height = 70
            ksize = 4
            ystart = 18
        elif name == "t":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
            ystart = 20
        elif name == "t1":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 2
            ystart = 20
        elif name == 'w':
            min_size = 100
            min_height = 30
            max_height = 50
            ksize = 2
            ystart = 20
        # elif name == "x":
        #     min_size = 500
        #     min_height = 50
        #     max_height = 75
        #     ksize = 2
        #     ystart = 20
        else:
            min_size = 100
            min_height = 50
            max_height = 70
            ksize = 4
            ystart = 18
        #
        if name =="g" or name == "m":
            kernel = np.ones((2,2), np.uint8)
            frame0 = cv2.dilate(frame0, kernel, iterations=1)
            frame0 = cv2.erode(frame0, kernel, iterations=1)
        if name == "q" or name == "w":
            kernel = np.ones((2, 2), np.uint8)
            frame0 = cv2.dilate(frame0, kernel, iterations=1)
            frame0 = cv2.erode(frame0, kernel, iterations=1)
        kernel = np.ones((ksize, ksize), np.uint8)
        frame0 = cv2.erode(frame0, kernel, iterations=1)
        # cv2.imshow("tst", frame0)

        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(frame0, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1]
        nb_components = nb_components - 1

        # minimum size of particles we want to keep (number of pixels)
        # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
        # your answer image
        img2 = np.zeros((output.shape))
        border = 1
        imgh = output.shape[0]
        # print(stats)
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] >= min_size and stats[i+1][3] > min_height and stats[i+1][3]<max_height and stats[i+1][0]>3 and stats[i+1][1]<ystart:  # and stats[i+1][1]+stats[i+1][3]<imgh-border:
            # if sizes[i] >= min_size and stats[i + 1][3] > min_height and stats[i + 1][3] < max_height and stats[i + 1][0] > 20:
                if name == "s":
                    if stats[i + 1][1] > 0:
                        img2[output == i + 1] = 255
                elif name == "m":
                    if stats[i+1][2]<35:
                        img2[output == i + 1] = 255
                else:
                    # print(stats[i+1])
                    # if sizes[i][0]+sizes[i][2] > sizes[i+1][0]
                    img2[output == i + 1] = 255
            # else:
            #     print(sizes[i], min_size)
            #     print(stats[i+1][3] , min_height)
            #     print(stats[i+1][3], max_height)
            #     print(stats[i+1][0])
            #     print(stats[i+1][1], ystart)


        img2 = cv2.dilate(img2, kernel, iterations=1)
        return img2

    return frame0

if __name__ == '__main__':
    pic = cv2.imread("./raw_img/8913.jpg")
    pic_ = img_ini(pic, mode="d", name='b')
    cv2.imshow("ini_pic", pic_)
    cv2.waitKey(0)