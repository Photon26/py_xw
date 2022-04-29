import pickle

dst = pickle.load(open("2022-s4.pkl", "rb"))
num = 741781  # enter the number
lst = list(dst)
thief_num = lst.index(num)
print(thief_num)