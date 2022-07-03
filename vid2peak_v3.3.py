"""
    Try to figure out the exact time of fire using timestamp.
    Variable explanation:
        showtime: score of st
        alength: frame of st
        showtime_ms: time of st
        showtime0: frame of true end
        showtime_ms: ending time of A paragraph
        truest: The true ending time of A paragraph(excluding time lagging)
        xs: solo peak
        ys: second solo peak
        seps: seperate score
        savescore: save score
        togs: together score
        before Output: pic1: solo peak start(index)
                       pic2: solo peak end(index)
                       pic3: second peak start(index)
                       pic4: second peak end(index)
                       pic5: ssp/together peak start(index)
                       pic6: ssp/together peak end(index)
                       pic1_1: peak1 start for neighbouring
                       pic1_2: peak1 end for neighbouring
                       pic2_1: peak2 start for neighbouring
                       pic2_2: peak2 end for neighbouring
        xsave: save start(A index)
        ysave: save start(B index)
        endframe: save end(B index)
        pindex: solo peak fire index
        sepindex: seperate fire index
        togindex: together fire index
        saveindex: save fire index
        neigindex: neighbouring fire index
"""

import time
import os
import shutil
import cv2
import numpy as np
import heapq
import xlwt

from img_Ini import img_ini
from num_Recog import num_Recog
from get_Gif import get_gif
from save_Img import save_Img
from firetime_Check import firetime_Check

# Inputfolder = '/media/gao/GAO/vid/2021/s6'
# Outputfolder = '/media/gao/GAO/data/2021/s6'

Inputfolder = 'F:/vid/2022/s7'
Outputfolder = 'F:/data/2022/s7'

# Inputfolder = 'H:/vid/debug'
# Outputfolder = 'H:/data/debug'

a = os.listdir(Inputfolder)

lagging = 167   # for all ios devices
nolagging_test = 1

for f in a:
    #   Define name
    if f.startswith("a_"):
        name = "a"
        modeldir = "./model/model"
        stmax = 150
    if f.startswith("b_"):
        name = "b"
        modeldir = "./model/model_b"
        stmax = 150
    elif f.startswith("a1_"):
        name = "a1"
        modeldir = "./model/model"
        stmax = 150
    elif f.startswith("c_"):
        name = "c"
        modeldir = "./model/model_c"
        stmax = 150
    elif f.startswith("d_"):
        name = "d"
        modeldir = "./model/model_d"
        stmax = 150
    elif f.startswith("e_"):
        name = "e"
        modeldir = "./model/model_e"
        stmax = 100
    elif f.startswith("f_"):
        name = "f"
        modeldir = "./model/model_f"
        stmax = 150
    elif f.startswith("g_"):
        name = "g"
        modeldir = "./model/model_g_old"
        stmax = 150
    elif f.startswith("h_"):
        name = "h"
        modeldir = "./model/model_h"
        stmax = 150
    elif f.startswith("j_"):
        name = "j"
        modeldir = "./model/model_j"
        stmax = 150
    elif f.startswith("k_"):
        name = "k"
        modeldir = "./model/model_k"
        stmax = 100
    elif f.startswith("l_"):
        name = "l"
        modeldir = "./model/model_l"
        stmax = 150
    elif f.startswith("m_"):
        name = "m"
        modeldir = "./model/model_m"
        stmax = 150
    elif f.startswith("mj_"):
        name = "mj"
        modeldir = "./model/model_mj"
        stmax = 150
    elif f.startswith("mz_"):
        name = "mz"
        modeldir = "./model/model_mz"
        stmax = 150
        lagging = 164
    elif f.startswith("q_"):
        name = "q"
        modeldir = "./model/model_q"
        stmax = 150
        lagging = 166
    elif f.startswith("qx_"):
        name = "qx"
        # modeldir = "./model/model_qx_old"
        modeldir = "./model/model_qx"
        stmax = 150
    elif f.startswith("r_"):
        name = "r"
        modeldir = "./model/model_r"
        stmax = 150
    elif f.startswith("s_"):
        name = "s"
        modeldir = "./model/model_s"
        stmax = 150
        lagging = 240
    elif f.startswith("t_"):
        name = "t"
        modeldir = "./model/model_t"
        stmax = 150
        lagging = 166
    elif f.startswith("t1_"):
        name = "t1"
        modeldir = "./model/model_t1"
        stmax = 150
    elif f.startswith("x_"):
        name = "x"
        modeldir = "./model/model_x"
        stmax = 150
    elif f.startswith("w_"):
        name = "w"
        modeldir = "./model/model_w1"
        stmax = 50
        lagging = 166
    elif f.startswith("y_"):
        name = "y"
        modeldir = "./model/model_ym"
        stmax = 150
        lagging = 206
    elif f.startswith("y1_"):
        name = "y1"
        modeldir = "./model/model_y1"
        stmax = 50
        lagging = 206
    elif f.startswith("z_"):
        name = "z"
        modeldir = "./model/model_z"
        stmax = 150
    # elif f.startswith("RP_"):
    #     name = "mj"
    #     modeldir = "./model/model_mj"
    #     stmax = 150
    #     f = "mj_x_xxyy_152.MP4"
    else:
        continue

    if nolagging_test == 1:
        lagging = 0

    true_mode = f.replace(name+"_", "", 1)[0]
    if true_mode == "p" or true_mode == "d":
        mode = "d"
    else:
        mode = "x"

    lag = lagging  # ms
    filen = f[:-4]
    bpm = filen[-3:]
    if bpm[0] == "_":
        bpm = bpm[1:]
    bpm = int(bpm)
    if f.startswith("mz_") or f.startswith("qx_") or f.startswith("mj_") or f.startswith("t1_") or f.startswith("y1_"):
        song = filen[3:]
    else:
        song = filen[2:]

    try:
        # Opens the Video file
        cap = cv2.VideoCapture(Inputfolder + '/' + f)

        st = time.time()
        dir = Outputfolder + '/' + song
        if not os.path.exists(dir):
            os.makedirs(dir)
        logger = open(dir + "/backup.txt", "w", encoding="utf-8")
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

        print("Start reading video...\n")
        while (cap.isOpened()):
            #   Read in img
            ret, frame = cap.read()
            if ret == False:
                break
            # img0 = img_ini(frame, thres=120, mode=mode, name=name)      # edited for y
            fireflag = firetime_Check(frame, name)
            img0 = img_ini(frame, mode=mode, name=name)
            # cv2.imshow("img0", img0)
            # cv2.waitKey(0)
            num = num_Recog(img0, model, name=name)

            # ttmp = cap.get(cv2.CAP_PROP_POS_MSEC)     #   for restarted
            # if ttmp<108000:
            #     continue

            # if num == 68:
            #     cv2.imwrite("bug.jpg", frame)     #   for debug

            worksheet.write(count, 0, label=str(num))
            count = count + 1
            result.append(num)
            ttmp = cap.get(cv2.CAP_PROP_POS_MSEC)
            if count > 10 and ttmp <= 0:
                ttmp = timestamp[-1]+10
            timestamp.append(ttmp)
            worksheet.write(count, 2, label=str(ttmp))
            fireflaglist.append(fireflag)
            worksheet.write(count, 3, label=str(fireflag))
        cap.release()
        cv2.destroyAllWindows()
        timestamp = np.array(timestamp)
        fireflaglist = np.array(fireflaglist)

        #   Smooth and figure out the showtime
        print("Start calculating st...")
        aendflag = 0
        anti_aendflag = 0
        count = 0
        result = np.array(result)
        result[0] = 0
        length = np.shape(result)[0]
        showtime0 = 0
        same = 0
        for i in range(1, length):
            if result[i] < result[i - 1]:
                if i >= 2 and result[i] == result[i - 2]:
                    result[i - 1] = result[i - 2]
                else:
                    result[i] = result[i - 1]
            if result[i] - result[i - 1] > 23000:           #   edit for fanmade
                result[i] = result[i - 1]
            worksheet.write(count, 1, label=str(result[i]))

            if same != -1 and result[i] > 100000:
                if result[i] == result[i - 1]:
                    if same == 0:
                        showtime_score = result[i]
                        showtime_score_id = i
                        showtime_score_time = timestamp[i]
                    same = same + 1
                else:
                    same = 0
                if same == stmax:
                    same = -1

            count = count + 1

            # if i>1000:
            if result[i]>120000:
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

        truest = timestamp[showtime0]  # The true ending time of a paragraph(excluding time lagging).
        showtime_ms = truest + lag  # According to the time lagging we have to postpone the showtime when calculating.
        alength = (np.abs(timestamp - showtime_ms)).argmin()
        showtime = result[alength]
        # showtime_score_time = timestamp[(np.abs(result - showtime_score)).argmin()]

        # #   aend time method 2
        # count = 0
        # same = 0
        # result = np.array(result)
        # result[0] = 0
        # length = np.shape(result)[0]
        # for i in range(1, length):
        #     if result[i] < result[i - 1]:
        #         if i >= 2 and result[i] == result[i - 2]:
        #             result[i - 1] = result[i - 2]
        #         else:
        #             result[i] = result[i - 1]
        #     if result[i] - result[i - 1] > 10000:
        #         result[i] = result[i - 1]
        #     worksheet.write(count, 1, label=str(result[i]))
        #     count = count + 1
        #     if same != -1 and result[i] > 100000:
        #         if result[i] == result[i - 1]:
        #             same = same + 1
        #         else:
        #             same = 0
        #         if same == stmax:
        #             showtime = result[i]
        #             same = -1
        # showtime0 = list(filter(lambda x: result[x] == showtime, range(len(result))))[0]

        workbook.save(dir + '/score_data.xls')
        fins = result[-1]
        res_list = list(filter(lambda x: result[x] == showtime, range(len(result))))
        res_list1 = list(filter(lambda x: result[x] == fins, range(len(result))))
        logger.write("Showtime pic is:" + str(alength))
        logger.write("\nFinal pic is:" + str(res_list1[0] + 1))

        #   Figure out the peak point(seperate)
        print("Start calculating fire point...")
        timelength = timestamp[-1]
        i = 0
        bqtime = (20+3/16) * 60 * 1000 / bpm
        timea = bqtime + lagging     # edited for lagging
        dif = np.zeros((length, 1))

        while timestamp[i] + timea < timelength:
            endtime = timestamp[i] + timea
            frameid = (np.abs(timestamp - endtime)).argmin()     # A version for nearest value
            # frameid = -np.searchsorted(timestamp[::-1], endtime)       # A version for nearest smaller value
            # frameid = np.searchsorted(timestamp, [endtime, ], side='right')[0]      # A version for nearest greater value
            dif[i] = result[frameid] - result[i]
            i = i + 1

        #   Solo peak
        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        xs = dif[dif_id]
        pscore = xs[0][0]
        pic1 = dif_id[0]
        pic2 = (np.abs(timestamp - timestamp[pic1] - timea)).argmin()
        pindex = round(pscore / 3120, 1)
        logger.write("\nThe peak score is:  " + str(result[dif_id]) + " to "
                     + str(result[pic2]) + ". The time is:  " + str(
            timestamp[dif_id[0]] / 1000) + " to " +
                     str((timestamp[dif_id[0]] + timea) / 1000))

        alter_id = None
        if true_mode == "x" or true_mode == "d":
            dif_alter = dif.copy()
            # print(type(dif_alter))
            #   alternative peak
            max_id = np.argmax(dif_alter)
            alter_id = max_id
            while(abs(result[max_id]-result[alter_id])<6240):
                dif_alter[alter_id] = 0
                alter_id = np.argmax(dif_alter)
                pscore_alter = np.max(dif_alter)
            pic1_alter = alter_id
            pic2_alter = (np.abs(timestamp - timestamp[pic1_alter] - timea)).argmin()
            pindex_alter = round(pscore_alter / 3120, 1)
            logger.write(f'\nAn alternative peak score is: {result[pic1_alter]} to {result[pic2_alter]}. The time is: '
                         f'{timestamp[pic1_alter]/1000} to {timestamp[pic2_alter]/1000}.')

        #   Figure out the point for neighbouring fire(sep when solo peak is not one of the 2 points)
        neigs = 0
        neig_x = 0
        neig_y = 0
        neig_start_cal_time = (np.abs(timestamp - (timestamp[pic1] - timea))).argmin()  # index of peak-t
        neig_end_cal_time = pic2  # index of peak + t
        for i in range(neig_start_cal_time, pic1):
            second_neig_start_cal_time = (np.abs(timestamp - (timestamp[i] + timea))).argmin() + 2  # index of i+t
            for j in range(second_neig_start_cal_time, neig_end_cal_time):
                if dif[i][0] + dif[j][0] > neigs:
                    neigs = dif[i][0] + dif[j][0]
                    neig_x = i
                    neig_y = j
        pic1_1 = neig_x
        pic1_2 = (np.abs(timestamp - (timestamp[neig_x] + timea))).argmin()
        pic2_1 = neig_y
        pic2_2 = (np.abs(timestamp - (timestamp[neig_y] + timea))).argmin()
        neigindex = round(neigs/3120, 1)
        # neigs = 0

        #   Second peak
        head_time = max(0, timestamp[pic1] - timea)
        end = min(np.shape(dif)[0], pic2)
        head = (np.abs(timestamp - head_time)).argmin()
        dif[head: end] = 0
        dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
        ys = dif[dif_id]
        score = result[dif_id]

        pic3 = dif_id[0]
        pic4 = (np.abs(timestamp - timestamp[pic3] - timea)).argmin()

        logger.write(
            "\nThe second peak score is: " + str(result[dif_id]) +
            " to " + str(result[pic4]) + ", score is " + str((xs + ys).T) +
            ". The time is: " + str(timestamp[dif_id[0]] / 1000) + " to " + str(
                (timestamp[dif_id[0]] + timea) / 1000))
        seps = (xs + ys).T[0][0]
        sepindex = round(seps / 3120, 1)

        logger.write(
            "\nThe score for neighbouring is: " + str(result[pic1_1]) + " and "+ str(result[pic2_1]) +", score is " + str(neigs) +
            ". The time is: " + str(timestamp[pic1_1] / 1000) + " to " + str(timestamp[pic1_2] / 1000) + " and "+
        str(timestamp[pic2_1] / 1000) + "to" + str(timestamp[pic2_2] / 1000))

        #   Figure out the peak point(together)
        timea2 = bqtime*2+lagging
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
            "\nThe peak score for together/ssp is: " + str(result[dif_id]) +
            " to " + str(result[pic6]) + ", score is " + str(dif[dif_id].T) +
            ". The time is: " + str(timestamp[dif_id[0]] / 1000) + " to " + str((timestamp[dif_id[0]] + timea2) / 1000))
        togs = dif[dif_id].T[0][0]
        togindex = round(togs/3120, 1)

        #   Figure out the peak point(save)
        bpara_begin = res_list[-1]
        bpara_end = res_list1[0]
        savescore = 0
        blankt = res_list[-1] - alength
        save_start_cal_time = (np.abs(timestamp - (timestamp[alength] - timea))).argmin()
        save_end_cal_time = (np.abs(timestamp - (timestamp[bpara_end] - timea))).argmin()
        xsave = 0
        ysave = 0
        ends = 0
        for x in range(save_start_cal_time, alength):
            ascore = showtime - result[x]
            for y in range(bpara_begin, save_end_cal_time):
                b_end_time = timea2 - (truest - timestamp[x]) + timestamp[y]       # test for saving(edited for d_left)
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
                     ". The filename is: " + str(xsave) + " and " + str(ysave + alength + blankt))
        logger.write("\nEnding score for saving is:" + str(ends))
        endframe = list(filter(lambda x: result[x] == ends, range(len(result))))[0]
        logger.write("\nBtime is:" + str(timea))
        saveindex = round(savescore/3120, 1)

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


    except IndexError or NameError or ValueError:

        cv2.destroyAllWindows()
        movefolder = Inputfolder + '/bug'
        if not os.path.exists(movefolder):
            os.makedirs(movefolder)
        shutil.move(Inputfolder + '/' + f, movefolder + '/' + f)

    else:
        logger.write("\n\n\n结论：")

        if jxscore >= bqscore:
            logger.write("\n\n单排技能：极限")
        else:
            logger.write("\n\n单排技能：爆气")
        if jxscore2 > bqscore2:
            logger.write("\n\n双排技能：极限")

        if bqscore_ssp < jxscore_ssp:
            logger.write("\n\nSSP技能：极限")

        save_Img(Inputfolder + '/' + f, showtime_score_time / 1000, dir + "/" + "showtime.jpg")

        fintime = timestamp[res_list1[0]]
        save_Img(Inputfolder + '/' + f, fintime / 1000, dir + "/" + "final.jpg")

        teams = max(savescore, seps, togs, neigs)

        logger.write("\n单排爆点序列：" + str(pic1) + " 到 " + str(pic2))
        logger.write("\n单排指数： " + str(pindex))
        time1 = timestamp[pic1]
        # print(time1)
        get_gif(Inputfolder + '/' + f, time1, "solo_begin", dir)
        time2 = timestamp[pic2]
        get_gif(Inputfolder + '/' + f, time2, "solo_end", dir)

        if alter_id is not None:
            # logger.write(f'\n备用爆点序列：{pic1_alter} 到 {pic2_alter}')
            # logger.write(f'\n单排指数：{pindex_alter}')
            if pindex - pindex_alter <= 0.15:
                jxs_alter = fins * 1.11 + pscore_alter * 0.5 * 1.11
                bqscore = fins + pscore_alter * 1.7
                logger.write(f'\n备用爆点序列：{pic1_alter} 到 {pic2_alter}')
                logger.write(f'\n单排指数：{pindex_alter}')
                time1_alter = timestamp[pic1_alter]
                get_gif(Inputfolder + '/' + f, time1_alter, "备用_solo_begin", dir)
                time2_alter = timestamp[pic2_alter]
                get_gif(Inputfolder + '/' + f, time2_alter, "备用_solo_end", dir)

        if teams == seps:
            if pic1 > pic3:
                pic1, pic3 = pic3, pic1
                pic2, pic4 = pic4, pic2
            logger.write("\n\n爆法：分开！ \n双排爆点序列：一爆从 " + str(pic1) + " 到 " + str(pic2) + "。\t二爆从 "
                         + str(pic3) + " 到 " + str(pic4))
            time1 = timestamp[pic1]
            get_gif(Inputfolder + '/' + f, time1, "sep1_begin", dir)
            time2 = timestamp[pic2]
            get_gif(Inputfolder + '/' + f, time2, "sep1_end", dir)
            time3 = timestamp[pic3]
            get_gif(Inputfolder + '/' + f, time3, "sep2_begin", dir)
            time4 = timestamp[pic4]
            get_gif(Inputfolder + '/' + f, time4, "sep2_end", dir)
            logger.write("\n双排指数： " + str(sepindex)+"\n")


        elif teams == savescore:
            logger.write("\n\n爆法：存气！ \n双排爆点序列：一爆从 " + str(xsave) + " 到 " + str(alength) + "。\t二爆从 " +
                         str(ysave) + " 到 " + str(endframe))
            time1 = timestamp[xsave]
            get_gif(Inputfolder + '/' + f, time1, "save1_begin", dir)
            time2 = showtime_ms
            get_gif(Inputfolder + '/' + f, time2, "save1_end", dir)
            time3 = timestamp[ysave]
            get_gif(Inputfolder + '/' + f, time3, "save2_begin", dir)
            time4 = timestamp[endframe]
            get_gif(Inputfolder + '/' + f, time4, "save2_end", dir)
            logger.write("\n双排指数： " + str(saveindex)+"\n")

            if neigs > seps:
                logger.write("若分开爆气, \n双排爆点序列：一爆从 " + str(pic1_1) + " 到 " + str(pic1_2) + "。\t二爆从 "
                             + str(pic2_1) + " 到 " + str(pic2_2))
                time1 = timestamp[pic1_1]
                get_gif(Inputfolder + '/' + f, time1, "sep1_begin", dir)
                time2 = timestamp[pic1_2]
                get_gif(Inputfolder + '/' + f, time2, "sep1_end", dir)
                time3 = timestamp[pic2_1]
                get_gif(Inputfolder + '/' + f, time3, "sep2_begin", dir)
                time4 = timestamp[pic2_2]
                get_gif(Inputfolder + '/' + f, time4, "sep2_end", dir)
                logger.write("\n分开指数： " + str(neigindex))
                logger.write("\n存气分数-分开分数 = " + str(savescore - neigindex) + "\n")  # Check difference between Seps and Saves

            else:
                if pic1 > pic3:
                    pic1, pic3 = pic3, pic1
                    pic2, pic4 = pic4, pic2
                logger.write("若分开爆气, \n双排爆点序列：一爆从 " + str(pic1) + " 到 " + str(pic2) + "。\t二爆从 "
                             + str(pic3) + " 到 " + str(pic4))
                time1 = timestamp[pic1]
                get_gif(Inputfolder + '/' + f, time1, "sep1_begin", dir)
                time2 = timestamp[pic2]
                get_gif(Inputfolder + '/' + f, time2, "sep1_end", dir)
                time3 = timestamp[pic3]
                get_gif(Inputfolder + '/' + f, time3, "sep2_begin", dir)
                time4 = timestamp[pic4]
                get_gif(Inputfolder + '/' + f, time4, "sep2_end", dir)
                logger.write("\n分开指数： " + str(sepindex))
                logger.write("\n存气分数-分开分数 = " + str(savescore-seps)+"\n")      #   Check difference between Seps and Saves

        elif teams == togs:
            logger.write("\n\nTOGETHER!\n The picture is from " + str(pic5) + " to " + str(pic6))
            time1 = timestamp[pic5]
            get_gif(Inputfolder + '/' + f, time1, "tog_begin", dir)
            time2 = timestamp[pic6]
            get_gif(Inputfolder + '/' + f, time2, "tog_end", dir)
            logger.write("\nTogether index is " + str(togindex)+"\n")

        elif teams == neigs:
            logger.write("\n\n爆法：分开！ \n双排爆点序列：一爆从 " + str(pic1_1) + " 到 " + str(pic1_2) + "。\t二爆从 "
                         + str(pic2_1) + " 到 " + str(pic2_2))
            time1 = timestamp[pic1_1]
            get_gif(Inputfolder + '/' + f, time1, "sep1_begin", dir)
            time2 = timestamp[pic1_2]
            get_gif(Inputfolder + '/' + f, time2, "sep1_end", dir)
            time3 = timestamp[pic2_1]
            get_gif(Inputfolder + '/' + f, time3, "sep2_begin", dir)
            time4 = timestamp[pic2_2]
            get_gif(Inputfolder + '/' + f, time4, "sep2_end", dir)
            logger.write("\n双排指数： " + str(neigindex)+"\n")

        logger.write("\n\nSSP爆点序列：" + str(pic5) + " 到 " + str(pic6))
        time1 = timestamp[pic5]
        get_gif(Inputfolder + '/' + f, time1, "ssp_begin", dir)
        time2 = timestamp[pic6]
        get_gif(Inputfolder + '/' + f, time2, "ssp_end", dir)
        logger.write("\nSSP指数为： " + str(togindex))

        print(f)
        logger.write("\n\n总运行时间：" + str(time.time() - st))
        logger.close()
        movefolder = Inputfolder + '/done'
        if not os.path.exists(movefolder):
            os.makedirs(movefolder)
        shutil.move(Inputfolder + '/' + f, movefolder + '/'+f)