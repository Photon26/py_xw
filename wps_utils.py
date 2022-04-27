import xlrd
import xlwt
import requests
import json
import xlsxwriter
from xlutils.copy import copy
import shutil
import os

def copy(num, filename, root, mode):
    """
    input:
    · root->file1, file2, ...
    output:
    · root->mode->0,1,2,...->file
    """
    dir = root+"/"+mode
    if not os.path.exists(dir):
        os.makedirs(dir)
    for i in range(0, num):
        if not os.path.exists(dir+"/"+str(i+1)):
            os.makedirs(dir+"/"+str(i+1))
            shutil.copyfile(root+"/"+filename, dir+"/"+str(i+1)+"/"+filename)


if __name__ == "__main__":
    copy(10, "工作簿1.xls", "C:/Users/gao/Desktop/x", "星弹")