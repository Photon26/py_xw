import cv2
import numpy as np

def img_ini(frame, thres = 240, mode = "x", name = "l"):
    #   Rotate, Extract interest Area, Binarization
    if name == "a1":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_ = frame_[193: 268, 1413: 1835, :]
    elif name == "d":
        frame_ = frame[5: 44, 928:1158, :]
    elif name == "e":
        frame_ = frame[8: 59, 928:1230, :]
    elif name == "f":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame[191:268, 1417: 1834, :]
    elif name == "g":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)    #   for low resolution
        frame_ = frame_[128: 179, 945: 1224, :]
        # frame_ = frame[1386: 1839, 1172: 1242, :]
        # frame_ = cv2.rotate(frame_, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif name == "h":
        frame_ = frame[96: 145, 934: 1225, :]
    elif name == "j":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[7: 61, 1211: 1501, :]
    elif name == "k":
        frame_ = frame[6: 36, 690: 879, :]
    elif name == "l":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[188: 263, 1413: 1835, :]
    elif name == "m":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[94: 145, 927: 1222, :]
    elif name == "mz":         # mz_old
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)           # edited for single file xiashan_y
        frame_ = frame_[11: 59, 1224: 1505, :]
        # frame_ = frame_[11: 59, 1092: 1384, :]
        # frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # frame_ = frame[5: 53, 1224: 1505, :]
    elif name == "r":
        frame_ = frame[159: 590, 12: 88, :]
        frame_ = cv2.rotate(frame_, cv2.ROTATE_90_CLOCKWISE)
    elif name == "s":
        frame_ = frame[8: 52, 968: 1229, :]
    elif name == "q":
        frame_ = frame[5: 63, 924: 1227, :]
    elif name == "qx":
        # frame_ = frame[130: 179, 942: 1221, :]        #   low resolution
        frame_ = frame[83: 496, 194: 266, :]
        frame_ = cv2.rotate(frame_, cv2.ROTATE_90_CLOCKWISE)
    elif name == "x":
        frame_ = frame[72: 151, 1414: 1836, :]
    elif name == "y":
        frame_ = frame[8: 62, 949: 1223, :]
    elif name == "z":
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)          # edited for standup1
        frame_ = frame[194: 269, 1380: 1832, :]
    else:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)     #    edit for zc_d
        frame_ = frame[193: 268, 1413: 1835, :]
    frame0 = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
    _, frame0 = cv2.threshold(frame0, thres, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((8, 8), np.uint8)
    #
    # frame0 = cv2.erode(frame0, kernel, iterations=1)

    if mode == "d":
        # find all your connected components (white blobs in your image)
        if name == "d":
            min_size = 100
            min_height = 30
            max_height = 40
            ksize = 2
            ystart = 20
        elif name == "e":
            min_size = 100
            min_height = 35
            max_height = 48
            ksize = 2
            ystart = 20
        elif name == "f":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 1
            ystart = 20
        elif name == "g":
            min_size = 100        #   low resolution
            min_height = 35
            max_height = 48
            ksize = 2
            ystart = 20

            # min_size = 100
            # min_height = 50
            # max_height = 70
            # ksize = 4
            # ystart = 18
        elif name == "h":
            min_size = 100
            min_height = 35
            max_height = 48
            ksize = 2
            ystart = 20
        elif name == "j":
            min_size = 100
            min_height = 35
            max_height = 51
            ksize = 2
            ystart = 20
        elif name == "k":
            min_size = 0
            min_height = 0
            max_height = 30
            ksize = 1
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
        elif name =="mz":
            min_size = 100
            min_height = 35
            max_height = 51
            ksize = 2
            ystart = 20
        elif name == 'q':
            min_size = 100
            min_height = 30
            max_height = 50
            ksize = 3
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
        elif name == 'r':
            min_size = 100
            min_height = 50
            max_height = 75
            ksize = 2
            ystart = 20
        elif name == "s":
            min_size = 100
            min_height = 30
            max_height = 42
            ksize = 2
            ystart = 20
        elif name == "x":
            min_size = 500
            min_height = 50
            max_height = 75
            ksize = 2
            ystart = 20
        elif name == 'y':
            min_size = 100
            min_height = 30
            max_height = 50
            ksize = 2
            ystart = 20
        elif name == "z":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
            ystart = 20
        else:
            min_size = 100
            min_height = 50
            max_height = 70
            ksize = 4
            ystart = 18
        #
        # if name =="mz" or name == "q":
        #     kernel = np.ones((6,6), np.uint8)
        #     frame0 = cv2.dilate(frame0, kernel, iterations=1)
        #     frame0 = cv2.erode(frame0, kernel, iterations=1)
        if name == "k":
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
        # print(stats)
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] >= min_size and stats[i+1][3] > min_height and stats[i+1][3]<max_height and stats[i+1][0]>3 and stats[i+1][1]<ystart:
            # if sizes[i] >= min_size and stats[i + 1][3] > min_height and stats[i + 1][3] < max_height and stats[i + 1][0] > 20:
                if name == "s":
                    if stats[i + 1][1] > 0:
                        img2[output == i + 1] = 255
                else:
                    # print(stats[i+1])
                    # if sizes[i][0]+sizes[i][2] > sizes[i+1][0]
                    img2[output == i + 1] = 255
        img2 = cv2.dilate(img2, kernel, iterations=1)
        return img2

    return frame0

if __name__ == '__main__':
    pic = cv2.imread("./raw_img/600.jpg")
    pic_ = img_ini(pic, mode="d", name='e')
    cv2.imshow("ini_pic", pic_)
    cv2.waitKey(0)