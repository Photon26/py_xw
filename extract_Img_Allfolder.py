import cv2
import time
import os
import shutil

Inputfolder = 'H:/vid/s10'
# Inputfolder = '/media/hlabbunri/GAO/vid/s10/tst'
a = os.listdir(Inputfolder)

for f in a:
    if f.startswith("x"):
        # Opens the Video file
        filen = f[:-4]
        cap = cv2.VideoCapture(Inputfolder+'/'+f)
        i = 0
        st = time.time()
        dir = "H:/data/"+filen
        # dir = "/media/hlabbunri/GAO/data/" + filen
        if not os.path.exists(dir):
            os.makedirs(dir)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            # frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(dir+'/'+str(i)+'.jpg',frame)
            i += 1
            # if i == 10:
            #     break

        cap.release()
        cv2.destroyAllWindows()
        print(time.time()-st)
        print(filen)
        # shutil.move(Inputfolder + '/' + f, Inputfolder + '/done/' + f)