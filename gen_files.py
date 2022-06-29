from xlsx_writein_format import *
from wps_utils import *
import pickle as pkl
import asposecells
import jpype
from asposecells.api import *
import win32com.client as win32

#  set mode number and root folder
num_xd = 120
num_xx = 20
num_xp = 10
num_dx = 25
num_dp = 20
num_px = 50
num_4 = 80
num_p = 25

# #  small num set for test
# num_xd = 5
# num_xx = 5
# num_xp = 5
# num_dx = 5
# num_dp = 5
# num_px = 5
# num_4 = 5
# num_p = 5

root_folder = "C:/Users/gao/Desktop/S6-2022"
season = "S6"
origin_file = "C:/Users/gao/Desktop/总表v4.16.xlsx"
num_sum = num_xd+num_xx+num_xp+num_dx+num_dp+num_px+num_4+num_p

# # ---------------- Comment from this ----------------
# # get the full songlst
# songlst_all = readin_all(origin_file, 21, '7')
#
# # copy the files
# st_num = 0
# m = ['星弦', '星泡', '弹弦', '弹泡', '弦泡', '泡泡']
# n = [num_xx, num_xp, num_dx, num_dp, num_px, num_p]
# for i in range(0, len(m)):
#     mode = m[i]
#     num = n[i]
#     gen_file_with_fulllst(mode, songlst_all, root_folder, 0, season + '-')
#     copy_all(num, season + '-' + mode + '.xlsx', root_folder, mode, st_num)
#     st_num = st_num + num
#
# # generate songlst for xd and 4
# num_req = num_xd + num_4
# songlst, dst = gen_all_songlst_modified(songlst_all, num_req)
# pkl.dump(dst, open(season+'-'+"songlst.pkl", "wb"))
# for i in range(0, num_xd):
#     index = i + st_num
#     gen_file_with_fulllst('星弹', songlst[i], root_folder + '/星弹/'+str(index), 0, season+ '-')
# st_num = st_num+num_xd
# for i in range(0, num_4):
#     index = i + st_num
#     gen_file_with_fulllst('四模', songlst[i+num_xd], root_folder + '/四模/'+str(index), 0, season+ '-')
#
#
#
# #  generate dst
# code_dst_gen(num_sum, 6, "2022-s6")  # TODO: comment it when once generated the dst
#
# #  add watermark
# # jpype.startJVM()
# mode = ""
# # ---------------- Comment to this ----------------

dst = pickle.load(open("2022-s6.pkl", "rb"))
dst = list(dst)

#   TODO: change the start num and comment the above part
for i in range(300, num_sum):
    #  classify mode and copy files
    flst = os.listdir(root_folder)
    for folder in flst:
        if folder.endswith(".xlsx"):
            continue
        fflst = os.listdir(root_folder + '/' + folder)
        if str(i) in fflst:
            filepath = root_folder + '/' + folder + '/' + str(i) + '/' + os.listdir(root_folder + '/' + folder + '/' + str(i))[0]
            mode = folder
            break
    wb1 = openpyxl.load_workbook(filepath)
    ws_num = len(wb1.sheetnames)
    print(ws_num)
    num = dst[i]
    wb = Workbook(filepath)

    for ws_id in range(0, ws_num):
        row = 1
        ws = wb1.worksheets[ws_id]
        while (ws['B' + str(row)].value) is not None:
            row = row + 1
        wb = add_watermark_wordart(wb, num, ws_id, row)
    wb.save(filepath)
    del wb
    print(filepath)

    # change the title
    title = '2022年' + season + '赛季' + mode + '爆气表说明'
    wb = openpyxl.load_workbook(origin_file)
    wb.worksheets[0].cell(1, 1).value = title
    wb.save(origin_file)

    # delete the last sheet and add the first sheet
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = False
    xl.DisplayAlerts = False
    wb1 = xl.Workbooks.Open(origin_file)
    wb2 = xl.Workbooks.Open(filepath)
    i = wb2.Worksheets.Count
    wb2.Worksheets(i).Delete()
    ws1 = wb1.Worksheets(1)
    ws1.Copy(Before=wb2.Worksheets(1))
    wb1.Close(SaveChanges=False)
    wb2.Close(SaveChanges=True)
    xl.DisplayAlerts = True
    xl.Application.Quit()