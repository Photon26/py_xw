import openpyxl
import os

Inputfolder = "C:/Users/gao/Desktop/S4-2022"
a = os.listdir(Inputfolder)
# print(a)
for mode in a:
    path = Inputfolder + "/" + mode
    lst = os.listdir(path)
    # print(lst)
    for num in lst:
        path_file = path + "/" + num
        bookname = os.listdir(path_file)
        book = path_file + "/" + bookname[0]
        try:
            wb = openpyxl.load_workbook(book)
            print("-----" ,num,"-----")
        except:
            # print("permission denied: ", num)
            pass
