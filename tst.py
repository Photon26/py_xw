# a = ['aas',[3,2,1],[7,4,5]]
# b =a.copy()
# b[2][0] = 1
# print(a,b)
# print(id(a[2]), id(b[2]))
#
#
# def change(lst):
#     llst = []
#     for i in range(0,3):
#         k =lst.copy()
#         k[0]='9'
#         llst.append(k)
#     return llst
#
# b = change(a)
# print(a,b)
def foo():
    a = []
    a.append(5)
    print(a)
    return a
foo()
foo()
foo()
