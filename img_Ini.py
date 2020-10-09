import cv2
import numpy as np

def img_ini(frame, thres = 240, mode = "x", name = "l"):
    #   Rotate, Extract interest Area, Binarization
    if name == "y":
        frame_ = frame[8: 62, 949: 1223, :]
    elif name =="m":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[194: 267, 1413: 1835, :]
        # frame_ = frame_[187: 260, 1413: 1835, :]
    elif name == "d":
        frame_ = frame[5: 44, 928:1158, :]
    elif name == "z":
        # frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)          # edited for standup1
        frame_ = frame_[194: 269, 1380: 1832, :]
    elif name == "s":
        frame_ = frame[8: 52, 968: 1229, :]
    elif name == "mz":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)           # edited for single file xiashan_y
        frame_ = frame_[11: 59, 1224: 1505, :]
        # frame_ = frame_[11: 59, 1092: 1384, :]
    elif name == "l":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[188: 263, 1413: 1835, :]
    elif name == "k":
        frame_ = frame[6: 36, 690: 879, :]
    elif name == "a1":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_ = frame_[193: 268, 1413: 1835, :]
    elif name == "g":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[128: 179, 945: 1224, :]
    elif name == "m1":
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_ = frame_[194: 267, 1413: 1835, :]
    elif name == "f":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame[191:268, 1417: 1834, :]
    else:
        frame_ = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_ = frame_[193: 268, 1413: 1835, :]
    frame0 = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
    _, frame0 = cv2.threshold(frame0, thres, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((8, 8), np.uint8)
    #
    # frame0 = cv2.erode(frame0, kernel, iterations=1)

    if mode == "d":
        # find all your connected components (white blobs in your image)
        if name == 'y':
            min_size = 100
            min_height = 30
            max_height = 50
            ksize = 2
        elif name == "m" or name == "m1":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
        elif name == "z":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 3
        elif name == "s":
            min_size = 100
            min_height = 30
            max_height = 42
            ksize = 2
        elif name =="mz":
            min_size = 100
            min_height = 35
            max_height = 51
            ksize = 2
        elif name == "l":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 4
        elif name == "d":
            min_size = 100
            min_height = 30
            max_height = 40
            ksize = 2
        elif name == "k":
            min_size = 0
            min_height = 0
            max_height = 30
            ksize = 1
        elif name == "g":
            min_size = 100
            min_height = 35
            max_height = 48
            ksize = 2
        elif name == "f":
            min_size = 300
            min_height = 50
            max_height = 70
            ksize = 1
        else:
            min_size = 100
            min_height = 50
            max_height = 70
            ksize = 4

        if name =="mz":
            kernel = np.ones((2,2), np.uint8)
            frame0 = cv2.dilate(frame0, kernel, iterations=1)
            frame0 = cv2.erode(frame0, kernel, iterations=1)
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
            if sizes[i] >= min_size and stats[i+1][3] > min_height and stats[i+1][3]<max_height and stats[i+1][0]>3:
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
    pic = cv2.imread("./raw_img/3216.jpg")
    pic_ = img_ini(pic, mode = "d", name='f')
    cv2.imshow("ini_pic", pic_)
    cv2.waitKey(0)