import pickle
import numpy as np
import heapq

season = 'S8'

dst = pickle.load(open("2022-s8.pkl", "rb"))
num = 398548  # enter the number
lst = list(dst)
try:
    thief_num = lst.index(num)
    print(thief_num)
except:
    print("No found.")


dst = pickle.load(open(season+'-'+"songlst.pkl", "rb"))
# print(dst[577-370])
# print(dst[578-370])
# print(dst[559-370])
# print(dst[563-370])
slist = ['无疾而终的暗恋2','许你2','兰陵香2']
anti_slist = ['欠你的婚礼2','沦陷与心动2','后来我们2','东南西北中2','情意结2','Dream Girl1','Break Down1','The Drum1','兰陵香1','沦陷与心动1']
while True:
    print("Please enter the song name that has changed(e.g. song1): ")
    name = input()
    if name == '0':
        break
    slist.append(name)

while True:
    print("Please enter the song name that has NOT changed(e.g. song1): ")
    name = input()
    if name == '0':
        break
    anti_slist.append(name)

sim = []

print("---------------------")
for i in range(0, len(dst)):
    sum = 0
    for song in slist:
        if song in dst[i]:
            sum = sum + 1
    for song in anti_slist:
        if not(song in dst[i]):
            sum = sum + 1
    sim.append(sum)

sim = np.array(sim)
max_id = heapq.nlargest(5, range(len(sim)), key=sim.__getitem__)
new_list = [x+205 for x in max_id]
score = sim[max_id]
print(new_list, score)