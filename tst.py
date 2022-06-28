from xlsx_writein_format import *
from wps_utils import *
import pickle as pkl
import asposecells
import jpype
from asposecells.api import *
import win32com.client as win32

root_folder = "C:/Users/gao/Desktop/S6-2022"
season = "S6"
origin_file = "C:/Users/gao/Desktop/总表v4.16.xlsx"

# get the full songlst
songlst_all = readin_all(origin_file, 21, '7')

# copy the files
st_num = 0
mode = '星弹'
gen_file_with_fulllst(mode, songlst_all, root_folder, 0, season + '-')