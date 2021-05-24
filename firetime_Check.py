"""
    Input: frame is rgb img from video
    Output: 1 while the icon exists. otherwise 0.
"""

import cv2
import numpy as np

def firetime_Check(frame, name="a"):
    if name == "a":
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)      #   edit for zc_d
        roi = frame[1758:1918, 557:886, :]
    elif name == "a1":
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        roi = frame[1758:1918, 557:886, :]
    elif name == "c":
        roi = frame[503: 839, 1760: 1915, :]
    elif name == "e":
        roi = frame[247: 472, 1172: 1281, :]
    elif name == "g":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[369:594, 1176:1279, :]
        # roi = frame[1761: 1918, 548: 883, :]
    elif name == "j":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[248: 474, 1453: 1560, :]
    elif name == "y":
        roi = frame[373: 702, 2148: 2311, :]
        #   old model
        # roi = frame[251: 471, 1172: 1279, :]
    elif name == "y1":
        roi = frame[270: 450, 1144: 1234, :]
    elif name == "m":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[334: 553, 1170: 1279, :]
    elif name == "mj":
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        roi = frame[1752: 1918, 503: 925, :]
    elif name == "mz":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[250: 472, 1454: 1559, :]
    elif name == "s":
        roi = frame[222: 420, 1185: 1280, :]
    elif name == "t":
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        roi = frame[493: 840, 1: 155, :]
    elif name == "t1":
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        roi = frame[548: 889, 1758: 1921, :]
    elif name == "z":
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[555: 887, 1762: 1920, :]
    elif name == "f":
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[558: 885, 1759: 1919, :]
    elif name == "h":
        roi = frame[338: 561, 1173: 1281, :]
    elif name == "x":
        roi = frame[435: 766, 1762: 1920, :]
    elif name == "r":
        roi = frame[70: 234, 375: 707, :]
    elif name == "q":
        roi = frame[249: 475, 1174: 1278, :]
    elif name == "qx":
        # roi = frame[367: 591, 1173: 1279, :]    # low resolution
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = frame[4: 158, 552: 886, :]
    elif name == "w":
        roi = frame[365: 597, 1172: 1278, :]
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
