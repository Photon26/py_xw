import cv2
import os
import numpy as np
import time

stime = time.time()
Inputfolder = "H:/data/a_d_myname_156"
os.chdir(Inputfolder)

a = os.listdir(Inputfolder)
for f in a:
    frame = cv2.imread(f)
    logger = open("tst.txt", "a")

    # height, width = frame.shape[:2]
    # size = (int(width * 0.5), int(height * 0.5))
    # img = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    interestarea = frame[1758:1918, 557:886, :]
    b = interestarea[:,:,0].astype(np.int16)
    r = interestarea[:,:,2].astype(np.int16)

    h,w = b.shape[:]
    # mask = np.zeros((h,w))
    # mask[:,:]=r[:,:]-b[:,:]
    mask = r-b

    # print(np.max(mask), np.min(mask))
    mask[mask<100]=0
    mask[mask>=100]=255

    logger.write(str(np.sum(mask)/255/(h*w))+"\n")

    # cv2.imshow("pic", mask.astype(np.uint8))
    # cv2.waitKey(0)
print(time.time()-stime)