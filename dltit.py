import cv2

time = 5000

while(1):
    vid = "D:/Photon/Videos/QOGW3025.MP4"
    cap = cv2.VideoCapture(vid)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        i = i+1
        if i == 100:
            print(cap.get(cv2.CAP_PROP_POS_MSEC))
            break

    # cap.set(0, time)
    # ret, frame = cap.read()
    # cv2.imshow("tst",frame)
    # cv2.waitKey(0)
