import cv2
import time
import os
from img_Ini import img_ini
from num_Recog import num_Recog
import numpy as np
import heapq
import xlrd

# Inputfolder = '/media/hlabbunri/GAO/vid/s10/tst'
# Outputfolder = '/media/hlabbunri/GAO/data/s10/tst'

Inputfolder = 'H:/data/s10/ay'
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
    filen = f
    bpm = filen[-3:]
    if bpm[0] == "_":
        bpm = bpm[1:]
    bpm = int(bpm)
    song = filen

    # Opens the Video file
    st = time.time()
    # print("Calculation of " + song + ":\n")
    count = 0
    same = 0

    data = xlrd.open_workbook(Inputfolder + "/" + f + "/score_data.xls")
    table = data.sheets()[0]  # 通过索引顺序获取
    result = table.col_values(1)
    timestamp = table.col_values(2)
    result = result[:-2]
    result[0] = 0
    timestamp = timestamp[:-2]
    timestamp[0] = 0

    length = len(result)
    for i in range(1, length):
        # print(i)
        result[i] = int(result[i])
        timestamp[i] = float(timestamp[i])
        if result[i] < result[i - 1]:
            if i >= 2 and result[i] == result[i - 2]:
                result[i - 1] = result[i - 2]
            else:
                result[i] = result[i - 1]
        # if result[i] - result[i - 1] > 10000:
        #     result[i] = result[i - 1]
        count = count + 1
        if same != -1 and result[i] > 100000:
            if result[i] == result[i - 1]:
                same = same + 1
            else:
                same = 0
            if same == stmax:
                showtime = result[i]
                same = -1

    result = np.array(result)
    timestamp = np.array(timestamp)

    fins = result[-1]
    res_list = list(filter(lambda x: result[x] == showtime, range(len(result))))
    res_list1 = list(filter(lambda x: result[x] == fins, range(len(result))))

    #   Figure out the peak point(together)
    timelength = timestamp[-1]
    timea = 20 * 60 * 1000 / bpm
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
    # print(
    #     "\nThe peak score for together/ssp is: " + str(result[dif_id]) + ", score is " + str(dif[dif_id].T) +
    #     "the time is:" + str(timestamp[dif_id[0]] / 1000) + " to " + str((timestamp[dif_id[0]] + timea2) / 1000))
    togs = dif[dif_id].T[0][0]

  #   Figure out the skill

    bqscore_ssp = fins + togs * 2.323
    jxscore_ssp = fins * 1.11 + togs * (2.067 - 1.11)
    print("jx:",jxscore_ssp, "bq:", bqscore_ssp)
    if bqscore_ssp < jxscore_ssp:
        print("\n\nSkill for ssp is PERFECT!!!")

    print(f)

