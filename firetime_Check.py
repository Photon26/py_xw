"""
    Input: frame is rgb img from video
    Output: 1 while the icon exists. otherwise 0.
"""

import cv2
import numpy as np

def firetime_Check(frame, name="a"):
    if name == "a":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)      #   edit for zc_d
        roi = frame[1758:1918, 557:886, :]
    elif name == "a1":
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        roi = frame[1758:1918, 557:886, :]
    elif name == "g":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # roi = frame[369:594, 1176:1279, :]
        roi = frame[1761: 1918, 548: 883, :]
    elif name == "y":
        roi = frame[251: 471, 1172: 1279, :]
    elif name == "m":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[555: 887, 1762: 1920, :]
    elif name == "m1":
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[555: 887, 1762: 1920, :]
    elif name == "mz":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[250: 472, 1454: 1559, :]
    elif name == "s":
        roi = frame[222: 420, 1185: 1280, :]
    elif name == "z":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[555: 887, 1762: 1920, :]
    elif name == "f":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[558: 885, 1759: 1919, :]
    elif name == "q":
        roi = frame[205: 401, 1185: 1279, :]
    elif name == "h":
        roi = frame[338: 561, 1173: 1281, :]
    elif name == "x":
        roi = frame[435: 766, 1762: 1920, :]
    elif name == "r":
        roi = frame[70: 234, 375: 707, :]
    elif name == "qx":
        # roi = frame[367: 591, 1173: 1279, :]
        roi = frame[4: 158, 552: 886, :]
    else:
        return 0

    b = roi[:, :, 0].astype(np.int16)
    r = roi[:, :, 2].astype(np.int16)
    # cv2.imshow("t",roi)
    # cv2.waitKey(0)

    h, w = b.shape[:]
    # mask = np.zeros((h,w))
    # mask[:,:]=r[:,:]-b[:,:]
    mask = r - b

    # print(np.max(mask), np.min(mask))
    mask[mask < 100] = 0
    mask[mask >= 100] = 255

    flag = np.sum(mask) / 255 / (h * w)
    # return flag
    if flag > 0.2 and flag < 0.55:
        return 1
    else:
        return 0


if __name__ == "__main__":
    import cv2
    import os
    import numpy as np

    Inputfolder = "H:/data/f_y_invader_180"
    os.chdir(Inputfolder)

    a = os.listdir(Inputfolder)
    a.sort(key=lambda x: int(x.split('.')[0]))

    flag = []
    for f in a:
        # f = "1420.jpg"
        frame = cv2.imread(f)
        print(firetime_Check(frame, "f"))
        flag.append(firetime_Check(frame, "f"))
    flag = np.array(flag)
    length = np.shape(flag)[0]
    aendflag = 0
    anti_aendflag = 0
    showtime0 = 0

    for i in range(1, length):
        #   aend time method 1
        if anti_aendflag == 0:
            if flag[i] == 0 and flag[i - 1] == 1:
                showtime0 = i
                aendflag = 1
            elif flag[i] == 0 and flag[i - 1] == 0:
                if aendflag == 10:
                    anti_aendflag = 1
                elif showtime0 != 0:
                    aendflag = aendflag + 1
            elif flag[i] == 1 and flag[i - 1] == 0:
                aendflag = 0
                showtime0 = 0
    print(showtime0)
