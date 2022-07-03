import pickle
import numpy as np
import heapq

season = 'S6'

dst = pickle.load(open("2022-s6_add.pkl", "rb"))
num = 145240  # enter the number
lst = list(dst)
try:
    thief_num = lst.index(num)
    print(thief_num)
except:
    print("No found.")


dst = pickle.load(open(season+'-'+"songlst.pkl", "rb"))
print(dst[0])
slist = []
anti_slist = []
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
score = sim[max_id]
print(max_id, score)