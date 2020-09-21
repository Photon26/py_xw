# import cv2
#
# start = 6914
# end = 7784
#
# vid = "E:/vid/test/a_d_sona2_165.MP4"
# cap = cv2.VideoCapture(vid)
# i = 0
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret == False:
#         break
#
#     if i == start:
#         time1 = cap.get(cv2.CAP_PROP_POS_MSEC)
#     if i == end:
#         time2 = cap.get(cv2.CAP_PROP_POS_MSEC)
#     i = i + 1
#
# print(time2-time1)
#
# cap.release()
# cv2.destroyAllWindows()

import numpy as np

