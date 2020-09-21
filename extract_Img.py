import cv2
import time
import os

# Opens the Video file
filen = "k_x_need_165"
cap= cv2.VideoCapture('C:/Users/GAO/Videos/vid/'+filen+'.MP4')
i=0
st = time.time()
dir = "./"+filen
if not os.path.exists(dir):
    os.makedirs(dir)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite(dir+'/'+str(i)+'.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()
print(time.time()-st)