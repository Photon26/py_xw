import pickle

dst = pickle.load(open("2022-s5.pkl", "rb"))
num = 761415  # enter the number
lst = list(dst)
thief_num = lst.index(num)
print(thief_num)