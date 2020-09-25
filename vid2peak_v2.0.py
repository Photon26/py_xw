"""
    Try to figure out the exact time of fire using timestamp.
    Variable explanation:
        showtime: score of st, alength: frame of st, showtime_ms: time of st
        showtime0: frame of true end
        truest: The true ending time of a paragraph(excluding time lagging).

"""

import cv2
import time
import os
import shutil
from img_Ini import img_ini
from num_Recog import num_Recog
import numpy as np
import heapq
import xlwt
from get_Gif import get_gif
from save_Img import save_Img
from firetime_Check import firetime_Check

# Inputfolder = '/media/hlabbunri/GAO/vid/s10/tst'
# Outputfolder = '/media/hlabbunri/GAO/data/s10/tst'

Inputfolder = 'H:/vid/s10'
Outputfolder = 'H:/data/s10'
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
    lag = 180  # ms
    filen = f[:-4]
    bpm = filen[-3:]
    if bpm[0] == "_":
        bpm = bpm[1:]
    bpm = int(bpm)
    song = filen

    try:
        # Opens the Video file
        cap = cv2.VideoCapture(Inputfolder + '/' + f)

        st = time.time()
        dir = Outputfolder + '/' + filen
        if not os.path.exists(dir):
            os.makedirs(dir)
        logger = open(dir + "/backup.txt", "a")
        logger.write("Calculation of " + song + ":\n")
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
        fireflaglist = []
        while (cap.isOpened()):
            #   Read in img
            ret, frame = cap.read()
            if ret == False:
                break
            # img0 = img_ini(frame, thres=120, mode=mode, name=name)      # edited for y
            fireflag = firetime_Check(frame, name)
            img0 = img_ini(frame, mode=mode, name=name)
            num = num_Recog(img0, model, name=name)
            worksheet.write(count, 0, label=str(num))
            count = count + 1
            result.append(num)
            ttmp = cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp.append(ttmp)
            worksheet.write(count, 2, label=str(ttmp))
            fireflaglist.append(fireflag)
            worksheet.write(count, 3, label=str(fireflag))
        cap.release()
        cv2.destroyAllWindows()
        timestamp = np.array(timestamp)
        fireflaglist = np.array(fireflaglist)

        #   Smooth and figure out the showtime
        aendflag = 0
        anti_aendflag = 0
        count = 0
        result = np.array(result)
        result[0] = 0
        length = np.shape(result)[0]
        showtime0 = 0
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

            #   aend time method 1
            if anti_aendflag == 0:
                if fireflaglist[i] == 0 and fireflaglist[i - 1] == 1:
                    showtime0 = i
                    aendflag = 1
                elif fireflaglist[i] == 0 and fireflaglist[i - 1] == 0:
                    if aendflag == stmax:
                        anti_aendflag = 1
                    elif showtime0 != 0:
                        aendflag = aendflag + 1
                elif fireflaglist[i] == 1 and fireflaglist[i - 1] == 0:
                    aendflag = 0
                    showtime0 = 0

        truest = timestamp[showtime0 - 1]  # The true ending time of a paragraph(excluding time lagging).
        showtime_ms = truest + lag  # According to the time lagging we have to postpone the showtime when calculating.
        alength = (np.abs(timestamp - showtime_ms)).argmin()
        showtime = result[alength]

        workbook.save(dir + '/score_data.xls')
        fins = result[-1]
        res_list = list(filter(lambda x: result[x] == showtime, range(len(result))))
        res_list1 = list(filter(lambda x: result[x] == fins, range(len(result))))
        logger.write("Showtime pic is:" + str(alength))
        logger.write("\nFinal pic is:" + str(res_list1[0] + 1))

        #   Figure out the peak point(seperate)
        timelength = timestamp[-1]
        i = 0
        timea = 20 * 60 * 1000 / bpm
        dif = np.zeros((length, 1))

        while timestamp[i] + timea < timelength:
            endtime = timestamp[i] + timea
            frameid = (np.abs(timestamp - endtime)).argmin()
            # frameid = -np.searchsorted(timestamp[::-1], endtime)       # A version for nearest smaller value
            dif[i] = result[frameid] - result[i]
            i = i + 1

        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        xs = dif[dif_id]
        logger.write("\nThe peak score is:  " + str(result[dif_id]) + ". The time is:  " + str(
            timestamp[dif_id[0]] / 1000) + " to " +
                     str((timestamp[dif_id[0]] + timea) / 1000))
        pscore = xs[0][0]
        pic1 = dif_id[0]
        pic2 = (np.abs(timestamp - timestamp[pic1] - timea)).argmin()

        head_time = max(0, timestamp[pic1] - timea)
        end = min(np.shape(dif)[0], pic2)
        head = (np.abs(timestamp - head_time)).argmin()
        dif[head: end] = 0
        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        ys = dif[dif_id]
        score = result[dif_id]

        pic3 = dif_id[0]
        pic4 = (np.abs(timestamp - timestamp[pic3] - timea)).argmin()

        logger.write("\nThe second peak score is: " + str(result[dif_id]) + ", score is " + str((xs + ys).T) +
                     "the time is: " + str(timestamp[dif_id[0]] / 1000) + "to" + str(
            (timestamp[dif_id[0]] + timea) / 1000))
        seps = (xs + ys).T[0][0]

        #   Figure out the peak point(together)
        timea2 = timea * 2
        dif = np.zeros((length, 1))
        i = 0

        while timestamp[i] + timea2 < timelength:
            endtime = timestamp[i] + timea2
            frameid = (np.abs(timestamp - endtime)).argmin()
            # frameid = -np.searchsorted(timestamp[::-1], endtime)       # A version for nearest smaller value
            dif[i] = result[frameid] - result[i]
            i = i + 1

        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        pic5 = dif_id[0]
        pic6 = (np.abs(timestamp - timestamp[pic5] - timea2)).argmin()
        logger.write(
            "\nThe peak score for together/ssp is: " + str(result[dif_id]) + ", score is " + str(dif[dif_id].T) +
            "the time is:" + str(timestamp[dif_id[0]] / 1000) + " to " + str((timestamp[dif_id[0]] + timea2) / 1000))
        togs = dif[dif_id].T[0][0]

        #   Figure out the peak point(save)
        bpara_begin = res_list[-1]
        bpara_end = res_list1[0]
        savescore = 0
        blankt = res_list[-1] - alength
        save_start_cal_time = (np.abs(timestamp - (timestamp[alength] - timea))).argmin()
        save_end_cal_time = (np.abs(timestamp - (timestamp[bpara_end] - timea))).argmin()
        for x in range(save_start_cal_time, alength):
            ascore = showtime - result[x]
            for y in range(bpara_begin, save_end_cal_time):
                b_end_time = 2 * timea - (showtime_ms - timestamp[x]) + timestamp[y]
                try:
                    b_end = (np.abs(timestamp - b_end_time)).argmin()
                    bscore = result[b_end] - result[y]
                    if ascore + bscore > savescore:
                        savescore = ascore + bscore
                        xs = result[x]
                        ys = result[y]
                        xsave = x
                        ysave = y
                        ends = result[b_end]
                except:
                    break
        logger.write("\nThe peak score for saving is: " + str(xs) + " " + str(ys) + ", score is " + str(savescore) +
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

        bqscore_ssp = fins + togs * 2.323
        jxscore_ssp = fins * 1.11 + togs * (2.067 - 1.11)

        logger.write("\nTeam: PERFECT score is:" + str(jxscore2) + ", FIRE score is:" + str(bqscore2))

        logger.write("\nSsp: PERFECT score is:" + str(jxscore_ssp) + ", FIRE score is:" + str(bqscore_ssp))

        logger.write("\nOverall time:" + str(time.time() - st))

        if jxscore >= bqscore:
            logger.write("\n\nThe skill is PERFECT!")
        else:
            logger.write("\n\nThe skill is FIRE!")
        if jxscore2 > bqscore2:
            logger.write("\n\nSkill for team is PERFECT!!!")

        if bqscore_ssp < jxscore_ssp:
            logger.write("\n\nSkill for ssp is PERFECT!!!")

        save_Img(Inputfolder + '/' + f, showtime_ms / 1000, dir + "/" + "showtime.jpg")

        fintime = timestamp[res_list1[0]]
        save_Img(Inputfolder + '/' + f, fintime / 1000, dir + "/" + "final.jpg")

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
            logger.write("SAVE! \nThe picture is from" + str(xsave) + " to " + str(alength) + "\tand" +
                         str(ysave + alength + blankt) + " to " + str(endframe))
            time1 = timestamp[xsave]
            get_gif(Inputfolder + '/' + f, time1, "save1_begin", dir)
            time2 = showtime_ms
            get_gif(Inputfolder + '/' + f, time2, "save1_end", dir)
            time3 = timestamp[ysave]
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

        logger.write("\n\nThe ssp peak is from" + str(pic5) + " to " + str(pic6))
        time1 = timestamp[pic5]
        get_gif(Inputfolder + '/' + f, time1, "ssp_begin", dir)
        time2 = timestamp[pic6]
        get_gif(Inputfolder + '/' + f, time2, "ssp_end", dir)

        print(f)
        logger.write("\n\nOverall runtime is:" + str(time.time() - st))
        logger.close()
        shutil.move(Inputfolder + '/' + f, Inputfolder + '/done/' + f)
