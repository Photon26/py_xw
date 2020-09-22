import cv2
import time
import os
import shutil
from img_Ini import img_ini
from num_Recog import num_Recog
import numpy as np
import heapq
import xlwt
import sys
from get_Gif import get_gif

Inputfolder = '/media/hlabbunri/GAO/vid/s10/tst'
Outputfolder = '/media/hlabbunri/GAO/data/s10/tst'

# Inputfolder = 'H:/vid/s10'
# Outputfolder = 'H:/data/s10'
a = os.listdir(Inputfolder)

for f in a:
    #   Define name
    if f.startswith("a_"):
        name = "a"
        modeldir = "./model"
        stmax = 150
    elif f.startswith("a1_"):
        name = "a1"
        modeldir = "./model"
        stmax = 150
    elif f.startswith("mz_"):
        name = "mz"
        modeldir = "./model_mz"
        stmax = 150
    elif f.startswith("m_"):
        name = "m"
        modeldir = "./model_m"
        stmax = 100
    elif f.startswith("m1_"):
        name = "m1"
        modeldir = "./model_m"
        stmax = 100
    elif f.startswith("y_"):
        name = "y"
        modeldir = "./model_y"
        stmax = 50
    elif f.startswith("s_"):
        name = "s"
        modeldir = "./model_s"
        stmax = 150
    elif f.startswith("g_"):
        name = "g"
        modeldir = "./model_g"
        stmax = 150
    elif f.startswith("z_"):
        name = "z"
        modeldir = "./model_z"
        stmax = 150
    elif f.startswith("k_"):
        name = "k"
        modeldir = "./model_k"
        stmax = 100
    else:
        continue

    mode = "d"
    filen = f[:-4]
    bpm = filen[-3:]
    if bpm[0] == "_":
        bpm = bpm[1:]
    bpm = int(bpm)
    song = filen

    try:
        # Opens the Video file
        cap = cv2.VideoCapture(Inputfolder+'/'+f)

        st = time.time()
        dir = Outputfolder+'/'+filen
        if not os.path.exists(dir):
            os.makedirs(dir)
        logger = open(dir + "/backup.txt", "a")
        logger.write("Calculation of "+song+":\n")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('raw')
        count = 0

        #   Read in models
        model = []
        for i in range(0, 10):
            img = cv2.imread(modeldir + '/' + str(i) + ".jpg")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #   Binarization
            img[img < 240] = 0
            img[img >= 240] = 1
            model.append(img)
        model = np.array(model)

        result = []
        timestamp = []
        while(cap.isOpened()):
            #   Read in img
            ret, frame = cap.read()
            if ret == False:
                break
            # img0 = img_ini(frame, thres=120, mode=mode, name=name)      # edited for y
            img0 = img_ini(frame, mode=mode, name=name)
            num = num_Recog(img0, model, name=name)
            worksheet.write(count, 0, label=str(num))
            count = count + 1
            result.append(num)
            ttmp = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp.append(ttmp)
            worksheet.write(count, 2, label=str(ttmp))
        cap.release()
        cv2.destroyAllWindows()
        timestamp = np.array(timestamp)

        #   Smooth and figure out the showtime
        count = 0
        same = 0
        result = np.array(result)
        result[0] = 0
        length = np.shape(result)[0]
        for i in range(1, length):
            if result[i] < result[i - 1]:
                if i >= 2 and result[i] == result[i - 2]:
                    result[i - 1] = result[i - 2]
                else:
                    result[i] = result[i - 1]
            if result[i] - result[i - 1] > 10000:
                result[i] = result[i - 1]
            worksheet.write(count, 1, label=str(result[i]))
            count = count + 1
            if same != -1 and result[i] > 100000:
                if result[i] == result[i - 1]:
                    same = same + 1
                else:
                    same = 0
                if same == stmax:
                    showtime = result[i]
                    same = -1

        workbook.save(dir + '/score_data.xls')
        fins = result[-1]
        res_list = list(filter(lambda x: result[x] == showtime, range(len(result))))
        res_list1 = list(filter(lambda x: result[x] == fins, range(len(result))))
        logger.write("Showtime pic is:" + str(res_list[0]+1))
        logger.write("\nFinal pic is:" + str(res_list1[0]+1))

        #   Figure out the peak point(seperate)
        if name == "y":
            timea = int(20.33 / bpm * 60 * 24)
        elif name == "s":
            timea = int(20.33 / bpm * 60 * 49)
        elif name == "k":
            timea = int(20.33 / bpm * 60 * 30)
        elif name == "z":
            timea = int(20.33 / bpm * 60 * 30)
        else:
            timea = int(20.33 / bpm * 60 * 59)

        dif = np.zeros((length, 1))
        for i in range(timea, length):
            dif[i - timea] = result[i] - result[i - timea]

        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        xs = dif[dif_id]
        logger.write("\nThe peak score is:  " + str(result[dif_id]) + ". The filename is:  " + str(dif_id[0]) + " to " +
                     str(dif_id[0] + timea))
        pscore = xs[0][0]
        pic1 = dif_id[0]
        pic2 = dif_id[0] + timea

        head = max(0, dif_id[0] - timea)
        end = min(np.shape(dif)[0], dif_id[0] + timea)
        dif[head: end] = 0
        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        ys = dif[dif_id]
        score = result[dif_id]

        logger.write("\nThe second peak score is: " + str(result[dif_id]) + ", score is " + str((xs + ys).T) +
                     "the filename is:" + str(dif_id[0]) + "to" + str(dif_id[0] + timea))
        seps = (xs + ys).T[0][0]
        pic3 = dif_id[0]
        pic4 = dif_id[0] + timea

        #   Figure out the peak point(together)
        timea2 = timea * 2
        dif = np.zeros((length, 1))
        for i in range(timea2, length):
            dif[i - timea2] = result[i] - result[i - timea2]

        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        logger.write("\nThe peak score for together/ssp is: "+ str(result[dif_id]) + ", score is " + str(dif[dif_id].T) +
                     "the filename is:" + str(dif_id[0]) + " to " + str(dif_id[0] + timea2))
        pic5 = dif_id[0]
        pic6 = dif_id[0] + timea2
        togs = dif[dif_id].T[0][0]

        #   Figure out the peak point(save)
        alength = res_list[0]
        apara = result[0:alength + 1]
        bpara = result[res_list[-1]:]
        blength = np.shape(bpara)[0]
        savescore = 0
        blankt = res_list[-1] - res_list[0]
        for x in range(alength - timea, alength):
            ascore = showtime - apara[x]
            for y in range(0, blength - timea):
                b_end = 2 * timea - (alength - x) + y
                try:
                    bscore = bpara[b_end] - bpara[y]
                    if ascore + bscore > savescore:
                        savescore = ascore + bscore
                        xs = apara[x]
                        ys = bpara[y]
                        xsave = x
                        ysave = y
                        ends = bpara[b_end]
                except:
                    break
        logger.write("\nThe peak score for saving is: " + str(xs) + str(ys) + ", score is " +str(savescore) +
                     "the filename is:" + str(xsave) + " and " + str(ysave + alength + blankt))
        logger.write("\nEnding time for saving is:" + str(ends))
        endframe = list(filter(lambda x: result[x] == ends, range(len(result))))[0]
        logger.write("\nBtime is:" + str(timea))

        #   Figure out the skill
        baoscore = pscore
        jxscore = fins * 1.11 + baoscore * 0.5 * 1.11
        bqscore = fins + baoscore * 1.7
        logger.write("\nPERFECT score is:" + str(jxscore) + ", FIRE score is:" + str(bqscore))

        baoscore = max(seps, savescore, togs)
        jxscore2 = fins * 1.11 + baoscore * 0.5 * 1.11
        bqscore2 = fins + baoscore * 1.7
        logger.write("\nTeam: PERFECT score is:" + str(jxscore2) + ", FIRE score is:" + str(bqscore2))

        logger.write("\nOverall time:" + str(time.time() - st))


        if jxscore >= bqscore:
            logger.write("\n\nThe skill is PERFECT!")
        else:
            logger.write("\n\nThe skill is FIRE!")
        if jxscore2 > bqscore2:
            logger.write("\n\nSkill for team is PERFECT!!!")

        cap = cv2.VideoCapture(Inputfolder + '/' + f)
        sttime = timestamp[res_list[0]]
        cap.set(0, sttime)
        ret, frame = cap.read()
        cv2.imwrite(dir+"/"+"showtime.jpg",frame)
        cap.release()
        cv2.destroyAllWindows()

    except IndexError or NameError:

        cv2.destroyAllWindows()
        shutil.move(Inputfolder + '/' + f, Inputfolder + '/bug/' + f)

    else:
        logger.write("\n\n\nCONCULSION:\n")

        teams = max(savescore, seps, togs)

        if teams == seps:
            logger.write("SEPERATE! \nThe picture is from" + str(pic1) + " to " + str(pic2) + "\tThe second is from "
                         + str(pic3) + " to " + str(pic4))
            time1 = timestamp[pic1]
            get_gif(Inputfolder + '/' + f, time1, "sep1_begin", dir)
            time2 = timestamp[pic2]
            get_gif(Inputfolder + '/' + f, time2, "sep1_end", dir)
            time3 = timestamp[pic3]
            get_gif(Inputfolder + '/' + f, time3, "sep2_begin", dir)
            time4 = timestamp[pic4]
            get_gif(Inputfolder + '/' + f, time4, "sep2_end", dir)


        elif teams == savescore:
            logger.write("SAVE! \nThe picture is from" + str(xsave) + " to " + str(res_list[0]) + "\tand" +
                         str(ysave + alength + blankt) + " to " + str(endframe))
            time1 = timestamp[xsave]
            get_gif(Inputfolder + '/' + f, time1, "save1_begin", dir)
            time2 = timestamp[res_list[0]]
            get_gif(Inputfolder + '/' + f, time2, "save1_end", dir)
            time3 = timestamp[ysave + alength + blankt]
            get_gif(Inputfolder + '/' + f, time3, "save2_begin", dir)
            time4 = timestamp[endframe]
            get_gif(Inputfolder + '/' + f, time4, "save2_end", dir)

        elif teams == togs:
            logger.write("TOGETHER!\n The picture is from" + str(pic5) + " to " + str(pic6))
            time1 = timestamp[pic5]
            get_gif(Inputfolder + '/' + f, time1, "tog_begin", dir)
            time2 = timestamp[pic6]
            get_gif(Inputfolder + '/' + f, time2, "tog_end", dir)

        logger.write("\n\nThe solo peak is from" + str(pic1) + " to " + str(pic2))
        time1 = timestamp[pic1]
        get_gif(Inputfolder + '/' + f, time1, "solo_begin", dir)
        time2 = timestamp[pic2]
        get_gif(Inputfolder + '/' + f, time2, "solo_end", dir)

        print(f)
        logger.write("\n\nOverall runtime is:" + str(time.time() - st))
        logger.close()
        shutil.move(Inputfolder + '/' + f, Inputfolder + '/done/' + f)
