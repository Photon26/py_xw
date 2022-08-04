# from xlsx_writein_format import *
# from wps_utils import *
# import pickle as pkl
# import asposecells
# import jpype
# from asposecells.api import *
# import win32com.client as win32
#
# root_folder = "C:/Users/gao/Desktop/S7-2022"
# season = "S7"
# origin_file = "C:/Users/gao/Desktop/总表v4.16.xlsx"
#
# # get the full songlst
# songlst_all = readin_all(origin_file, 21, '8')
#
# m = ['星弹', '星弦', '星泡', '弹弦', '弹泡', '弦泡', '四模']
# for i in range(0, len(m)):
#     mode = m[i]
#     gen_file_with_fulllst(mode, songlst_all, root_folder, 1, season + '-')
#
#     # change the title
#     title = '2022年' + season + '赛季' + mode + 'SSP爆气表说明'
#     wb = openpyxl.load_workbook(origin_file)
#     wb.worksheets[0].cell(1, 1).value = title
#     wb.save(origin_file)
#     wb.close()
#
#     # delete the last sheet and add the first sheet
#     filepath = root_folder + '/' + season + '-' + mode + 'SSP.xlsx'
#     xl = win32.gencache.EnsureDispatch('Excel.Application')
#     xl.Visible = False
#     xl.DisplayAlerts = False
#     wb1 = xl.Workbooks.Open(origin_file)
#     wb2 = xl.Workbooks.Open(filepath)
#     ws1 = wb1.Worksheets(1)
#     ws1.Copy(Before=wb2.Worksheets(1))
#     wb1.Close(SaveChanges=False)
#     wb2.Close(SaveChanges=True)
#     xl.DisplayAlerts = True
#     xl.Application.Quit()

#  gen special
from xlsx_writein_format import *
from wps_utils import *
import pickle as pkl
import asposecells
import jpype
from asposecells.api import *
import win32com.client as win32

root_folder = "C:/Users/gao/Desktop/S7-2022"
season = "S7"
origin_file = "C:/Users/gao/Desktop/总表v4.16.xlsx"

# get the full songlst
songlst_all = readin_all(origin_file, 21, '8')

m = ['四模']
for i in range(0, len(m)):
    mode = m[i]
    gen_file_with_fulllst(mode, songlst_all, root_folder, 0, season + '-')

    # change the title
    title = '2022年' + season + '赛季' + mode + '爆气表说明'
    wb = openpyxl.load_workbook(origin_file)
    wb.worksheets[0].cell(1, 1).value = title
    wb.save(origin_file)
    wb.close()

    # delete the last sheet and add the first sheet
    filepath = root_folder + '/' + season + '-' + mode + '.xlsx'

    wb1 = openpyxl.load_workbook(filepath)
    ws_num = len(wb1.sheetnames)
    print(ws_num)
    num = 791048
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

    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = False
    xl.DisplayAlerts = False
    wb1 = xl.Workbooks.Open(origin_file)
    wb2 = xl.Workbooks.Open(filepath)
    ws1 = wb1.Worksheets(1)
    ws1.Copy(Before=wb2.Worksheets(1))
    wb1.Close(SaveChanges=False)
    wb2.Close(SaveChanges=True)
    xl.DisplayAlerts = True
    xl.Application.Quit()