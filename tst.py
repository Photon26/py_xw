a = ['aas','ddaddas',3]
b =a.copy()
b[2] = 10
print(a,b)

def change(lst):
    llst = []
    for i in range(0,3):
        k =lst.copy()
        k[0]='9'
        llst.append(k)
    return llst

b = change(a)
print(a,b)