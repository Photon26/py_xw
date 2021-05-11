import cv2
import numpy as np

frame = cv2.imread("raw_img/4429.jpg")
# frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
# frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
m,n =np.shape(frame)[:2]
a = np.zeros((m, n)).astype(int)
a[:, :] = frame[:, :, 0]
center = np.array([100,1000])
a1 = 100
b1 = 100
kstep = 1

disIm = np.zeros((m,n,3)).astype('uint8')
disIm[:,:,:] = frame[:,:,:]

a[int(center[0]-a1/2) : int(center[0]+a1/2), int(center[1]-b1/2): int(center[1]+b1/2)] = a[int(center[0]-a1/2) : int(center[0]+a1/2), int(center[1]-b1/2): int(center[1]+b1/2)] -100
disIm[:, :, 0] = a

while True:
    height, width = disIm.shape[:2]
    size = (int(width * 0.5), int(height * 0.5))
    img = cv2.resize(disIm, size, interpolation=cv2.INTER_AREA)
    cv2.imshow("pic", img)
    # cv2.imshow("pic", disIm)

    print("Press 'a' 'd' 'w' 's' to adjust the rectangle.\nPress SPACE to exit.")
    key = cv2.waitKey(0)
    if key & 0xFF == 32:
        print("Got the mask.")
        break
    elif key & 0xFF == ord('w'):
        center[1] = center[1] - kstep
    elif key & 0xFF == ord('s'):
        center[1] = center[1] + kstep
    elif key & 0xFF == ord('a'):
        center[0] = center[0] - kstep
    elif key & 0xFF == ord('d'):
        center[0] = center[0] + kstep
    elif key & 0xFF == ord('-'):
        a1 = a1 - kstep
    elif key & 0xFF == ord('='):
        a1 = a1 + kstep
    elif key & 0xFF == ord('o'):
        b1 = b1 - kstep
    elif key & 0xFF == ord('p'):
        b1 = b1 + kstep

    # BallBord = [center[0] - Radius1, center[0] + Radius1, center[1] - Radius1, center[1] + Radius1]

    #   redraw the circle
    #   unit8?
    a[:, :] = frame[:, :, 0]
    a[int(center[0] - a1 / 2): int(center[0] + a1 / 2), int(center[1] - b1 / 2): int(center[1] + b1 / 2)] = a[int(
        center[0] - a1 / 2): int(center[0] + a1 / 2), int(center[1] - b1 / 2): int(center[1] + b1 / 2)] - 100
    disIm[:, :, 0] = a


print(int(center[0] - a1 / 2), int(center[0] + a1 / 2), int(center[1] - b1 / 2), int(center[1] + b1 / 2))
print(np.shape(frame))
# 446 94 [1620 1206]
# [1397:1843, 1159:1253]