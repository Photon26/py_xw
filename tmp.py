# # # # import wps_utils as wu
# # # # import openpyxl
# # # #
# # # # #  for test
# # # # wu.make_watermark(699865, "tst", x_step=250, y_step=200, size=70)
# # # # wb = openpyxl.load_workbook('S3-星弹.xlsx')
# # # # wu.add_pic(wb, "tst.png")
# # # # wb.save('out.xlsx')

# import asposecells
# import jpype
# jpype.startJVM()
# from asposecells.api import *
#
# # Load the Excel file
# workbook = Workbook("test.xlsx")
#
# # Get the first default sheet
# sheet = workbook.getWorksheets().get(3)
#
# # Add watermark
# wordart = sheet.getShapes().addTextEffect(MsoPresetTextEffect.TEXT_EFFECT_2, "658795",
#     "Arial Black", 50, False, False, 8, 100, 1, 1, 250, 378)
# # Get the fill format of the word art
# wordArtFormat = wordart.getFill()
#
# print(type(sheet.getShapes()))
# # wordArtFormat.RotationAngle = 45
# # # Set the color
# wordArtFormat.setOneColorGradient(Color.getBlack(), 1, GradientStyleType.UNKNOWN, 2);
# # wordArtFormat.Forecolor = (255, 0, 0)
#
# # Set the transparency
# wordArtFormat.setTransparency(0.7)
#
# # Make the line invisible
# wordart.setHasLine(False)
#
# # Lock shape aspects
# wordart.setLocked(False)
# # wordart.setLockedProperty(ShapeLockType.SELECTION, True)
# # wordart.setLockedProperty(ShapeLockType.SHAPE_TYPE, True)
# # wordart.setLockedProperty(ShapeLockType.MOVE, True)
# # wordart.setLockedProperty(ShapeLockType.RESIZE, True)
# # wordart.setLockedProperty(ShapeLockType.TEXT, True)
#
# # Save the watermarked Excel file
# workbook.save("watermarked.xlsx")

# # # import xlsxwriter
# # #
# # # workbook = xlsxwriter.Workbook("tst.xlsx")
# # # worksheet = workbook.add_worksheet()
# # # worksheet.set_landscape()
# # #
# # # bold_format = workbook.add_format({'bold': True})
# # # bold_format.set_rotation(45)
# # #
# # # worksheet.insert_textbox('B2', 'Text rotated up',
# # #                          {'text_rotation': 45})
# # #
# # # worksheet.write('A1', "something", bold_format)
# # #
# # # workbook.close()
# #
# # import xlsxwriter
# # import xlrd
# # import openpyxl
# # from os.path import expanduser
# #
# # xlrd.xlsx.ensure_elementtree_imported(False, None)
# # xlrd.xlsx.Element_has_iter = True
# #
# # wbRD = xlrd.open_workbook("test.xlsx")
# # sheets = wbRD.sheets()
# #
# # wb = xlsxwriter.Workbook("tst.xlsx")
# # for sheet in sheets: # write data from old file
# #     newSheet = wb.add_worksheet(sheet.name)
# #     for row in range(sheet.nrows):
# #         for col in range(sheet.ncols):
# #             newSheet.write(row, col, sheet.cell(row, col).value)
# #
# # # wb = openpyxl.load_workbook('tst.xlsx')
# # # workbook = xlsxwriter.Workbook('test.xlsx')
# # worksheet = wb.add_worksheet()
# # # worksheet = wb.worksheets[0]
# #
# # text = 'Formatted textbox'
# #
# # options = {
# #     'width': 378,
# #     'height': 150,
# #     'x_offset': 10,
# #     'y_offset': 10,
# #     'font': {'bold': True,
# #              'name': 'Arial',
# #              'color': 'black',
# #              'size': 77},
# #     'align': {'vertical': 'middle',
# #               'horizontal': 'center'
# #               },
# #     'gradient': {'colors': ['#DDEBCF',
# #                             '#9CB86E',
# #                             '#156B13']},
# #     'fill': {'none': True}
# # }
# #
# # worksheet.insert_textbox('B2', text, options)
# #
# # wb.close()
#
import wps_utils as wu
import openpyxl
import asposecells
import jpype
from asposecells.api import *

# jpype.startJVM()
wb1 = openpyxl.load_workbook("test.xlsx")
ws_num = len(wb1.sheetnames)
# print(ws_num)
num = 877672
wb = Workbook("test.xlsx")
# wb = wu.add_watermark_wordart(wb, num, ws_num)
# # make_watermark(num, "tst", x_step=250, y_step=200, size=70)
# # add_pic(wb, "tst.png")
# # wb.save(filepath)


row = 1
ws = wb1.worksheets[1]
while (ws['B'+str(row)].value) is not None:
    row = row + 1
wb = wu.add_watermark_wordart(wb, num, 1, row)
wb.save("ttst.xlsx")

import win32com.client as win32
import os
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False
wb = excel.Workbooks.Open("F:/py_xw/ttst.xlsx")
i = wb.Worksheets.Count
wb.Worksheets(i).Delete()
wb.Save()
excel.DisplayAlerts = True
excel.Application.Quit()
# print(i)
# print(ws['B98'].value)