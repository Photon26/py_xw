import cv2
from img_Ini import img_ini
from num_Recog import num_Recog
import os
import numpy as np
import heapq
import xlwt
import time
import sys
import shutil

folder = 'H:/data'
m = os.listdir(folder)
# for n in m:
#     if n.startswith("l_"):
#         name = "l"
#     elif n.startswith("a_"):
#         name = "a"
#     elif n.startswith("mz_"):
#         name = "mz"
#     elif n.startswith("m_"):
#         name = "m"
#     elif n.startswith("k_"):
#         name = "k"
#     elif n.startswith("s_"):
#         name = "s"
#     elif n.startswith("y_"):
#         name = "y"
#     elif n.startswith("z_"):
#         name = "z"
#     else:
#         continue
#     # stoptime = 9540

mode = "d"
name = "d"
n = "d_d_gt_126"
Inputfolder = folder+'/'+n   # The foldername: name + _mode(x, d, y, p) + _song + _bpm e.g.  s_x_happy_162
bpm = int(Inputfolder[-3:])
song = n

#   Create a logger file
logger = open("backup/" + n + ".txt", "w")
sys.stdout = logger
print("Calculation of "+song+":")

st = time.time()
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('raw')
count = 0

#   Read in models
if name == "y":
    modeldir = "./model_y"
    stmax = 50
elif name =="m":
    modeldir = "./model_m"
    stmax = 100
elif name == "z":
    modeldir = "./model_z"
    stmax = 150
elif name == "s":
    modeldir = "./model_s"
    stmax = 150
elif name == "mz":
    modeldir = "./model_mz"
    stmax = 150
elif name == "k":
    modeldir = "./model_k"
    stmax = 100
elif name == "d":
    modeldir = "./model_d_sidou"
    stmax = 100
else:
    modeldir = "./model"
    stmax = 150
model = []
for i in range(0, 10):
    img = cv2.imread(modeldir+'/'+str(i)+".jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #   Binarization
    img[img < 240] = 0
    img[img >= 240] = 1
    model.append(img)
model = np.array(model)

#   Read in img
a = os.listdir(Inputfolder)
a.sort(key=lambda x: int(x.split('.')[0]))

result = []
for f in a:
    img = cv2.imread(Inputfolder+"/"+f)
    img0 = img_ini(img, mode=mode, name=name)
    num = num_Recog(img0, model, name=name)
    worksheet.write(count, 0, label=str(num))
    count = count+1
    # print(f, num)
    result.append(num)
    # #   End point
    # if f == str(stoptime)+".jpg":
    #     break

# print(time.time()-st)

#   Smooth and figure out the showtime
count = 0
same = 0
result = np.array(result)
result[0] = 0
length = np.shape(result)[0]
for i in range(1, length):
    if result[i]<result[i-1]:
        if i >=2 and result[i]==result[i-2]:
            result[i-1]=result[i-2]
        else:
            result[i] = result[i-1]
    if result[i]-result[i-1]>30000:
        result[i] = result[i-1]
    worksheet.write(count, 1, label=str(result[i]))
    count = count + 1
    if same != -1 and result[i]>100000:
        if result[i] == result[i-1]:
            same = same+1
        else:
            same = 0
        if same == stmax:
            showtime = result[i]
            same = -1

workbook.save("backup/"+ song + '.xls')
fins = result[-1]
res_list = list(filter(lambda x: result[x] == showtime, range(len(result))))
res_list1 = list(filter(lambda x: result[x] == fins, range(len(result))))

# #   show img
# frame = cv2.imread(Inputfolder+"/"+a[res_list[0]])
# height, width = frame.shape[:2]
# size = (int(width * 0.5), int(height * 0.5))
# img = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
# cv2.imshow("pic", img)
# cv2.waitKey(0)
#
# frame = cv2.imread(Inputfolder+"/"+a[res_list1[0]])
# height, width = frame.shape[:2]
# size = (int(width * 0.5), int(height * 0.5))
# img = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
# cv2.imshow("pic", img)
# cv2.waitKey(0)

print("Showtime pic is:", a[res_list[0]])
stpic = a[res_list[0]]
print("Final pic is:", a[res_list1[0]])

#   Figure out the peak point(seperate)
if name == "y":
    timea = int(20/bpm*60*24)
elif name == "s":
    timea = int(20/bpm*60*49)
elif name == "k":
    timea = int(20/bpm*60*30)
elif name == "d":
    timea = int(20/bpm*55*30)
else:
    timea = int(20/bpm*60*59)

dif = np.zeros((length, 1))
for i in range(timea, length):
    dif[i-timea] = result[i]-result[i-timea]

dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
xs = dif[dif_id]
print("The peak score is: ", result[dif_id], "the filename is:", a[dif_id[0]], "to", a[dif_id[0]+timea])
pscore = xs[0][0]
picp1 = a[dif_id[0]]
picp2 = a[dif_id[0]+timea]

head = max(0, dif_id[0]-timea)
end = min(np.shape(dif)[0], dif_id[0]+timea)
dif[head: end] = 0
dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
ys = dif[dif_id]
score = result[dif_id]

print("The second peak score is: ", result[dif_id], ", score is ", (xs+ys).T, "the filename is:", a[dif_id[0]], "to", a[dif_id[0]+timea])
seps = (xs+ys).T[0][0]
picp3 = a[dif_id[0]]
picp4 = a[dif_id[0]+timea]

#   Figure out the peak point(together)
timea2 = timea*2
dif = np.zeros((length, 1))
for i in range(timea2, length):
    dif[i-timea2] = result[i]-result[i-timea2]

dif_id = heapq.nlargest(5, range(len(dif)), key=dif.__getitem__)
print("The peak score for together/ssp is: ", result[dif_id], ", score is ", dif[dif_id].T, "the filename is:", a[dif_id[0]], "to", a[dif_id[0]+timea2])
togs = dif[dif_id].T[0][0]
pict1 = a[dif_id[0]]
pict2 = a[dif_id[0]+timea2]

#   Figure out the peak point(save)
alength = res_list[0]
apara = result[0:alength+1]
bpara = result[res_list[-1]:]
blength = np.shape(bpara)[0]
savescore = 0
blankt = res_list[-1]-res_list[0]
xsave = 0
ysave = 0
for x in range(alength-timea, alength):
    ascore = showtime - apara[x]
    for y in range(0, blength-timea):
        b_end = 2*timea-(alength-x)+y
        try:
            bscore = bpara[b_end]-bpara[y]
            if ascore+bscore > savescore:
                savescore = ascore+bscore
                xs = apara[x]
                ys = bpara[y]
                xsave = x
                ysave = y
                ends = bpara[b_end]
        except:
            break
print("The peak score for saving is: ", xs, ys, ", score is ", savescore, "the filename is:", a[xsave], a[ysave+alength+blankt])
print("Ending time for saving is:", ends)
print("Btime is:", timea)
pics1 = a[xsave]
pics2 = a[ysave + alength + blankt]
pics3id = list(filter(lambda x: result[x] == ends, range(len(result))))[0]
pics3 = a[pics3id]

#   Figure out the skill
baoscore = pscore
jxscore = fins*1.11+baoscore*0.5*1.11
bqscore = fins+baoscore*1.7
print("PERFECT score is:", jxscore,", FIRE score is:", bqscore)

baoscore = max(seps, savescore, togs)
jxtscore = fins*1.11+baoscore*0.5*1.11
bqtscore = fins+baoscore*1.7
print("Team: PERFECT score is:", jxscore,", FIRE score is:", bqscore)

print("\n\nConclusion:\n")
teammaxscore = max(seps, savescore, togs)
if seps == teammaxscore:
    print("SEPERATE!\nThe pic is ", picp1, "to", picp2, "\t",picp3, "to", picp4)
elif savescore == teammaxscore:
    print("SAVE!\nThe pic is ", pics1, "to", stpic, "\t", pics2, "to", pics3)
elif savescore == togs:
    print("TOGETHER!\nThe pic is ", pict1, "to", pict2)

print("\nSolo peak: ", picp1, "to", picp2)

if jxscore>= bqscore:
    print("\nThe skill is PERFECT!")
else:
    print("\nThe skill is FIRE!")

if jxtscore>bqtscore:
    print("\nTeam skill is FIRE!!!\n")

print("Overall time:", time.time()-st,"\n")
shutil.move(folder+'/'+n, folder+'/done/'+n)

logger.close()