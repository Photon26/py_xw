# # # # # import xlsxwriter
# # # # #
# # # # # workbook = xlsxwriter.Workbook("tst.xlsx")
# # # # # worksheet = workbook.add_worksheet()
# # # # # worksheet.set_landscape()
# # # # #
# # # # # bold_format = workbook.add_format({'bold': True})
# # # # # bold_format.set_rotation(45)
# # # # #
# # # # # worksheet.insert_textbox('B2', 'Text rotated up',
# # # # #                          {'text_rotation': 45})
# # # # #
# # # # # worksheet.write('A1', "something", bold_format)
# # # # #
# # # # # workbook.close()
# # # #
# # # # import xlsxwriter
# # # # import xlrd
# # # # import openpyxl
# # # # from os.path import expanduser
# # # #
# # # # xlrd.xlsx.ensure_elementtree_imported(False, None)
# # # # xlrd.xlsx.Element_has_iter = True
# # # #
# # # # wbRD = xlrd.open_workbook("test.xlsx")
# # # # sheets = wbRD.sheets()
# # # #
# # # # wb = xlsxwriter.Workbook("tst.xlsx")
# # # # for sheet in sheets: # write data from old file
# # # #     newSheet = wb.add_worksheet(sheet.name)
# # # #     for row in range(sheet.nrows):
# # # #         for col in range(sheet.ncols):
# # # #             newSheet.write(row, col, sheet.cell(row, col).value)
# # # #
# # # # # wb = openpyxl.load_workbook('tst.xlsx')
# # # # # workbook = xlsxwriter.Workbook('test.xlsx')
# # # # worksheet = wb.add_worksheet()
# # # # # worksheet = wb.worksheets[0]
# # # #
# # # # text = 'Formatted textbox'
# # # #
# # # # options = {
# # # #     'width': 378,
# # # #     'height': 150,
# # # #     'x_offset': 10,
# # # #     'y_offset': 10,
# # # #     'font': {'bold': True,
# # # #              'name': 'Arial',
# # # #              'color': 'black',
# # # #              'size': 77},
# # # #     'align': {'vertical': 'middle',
# # # #               'horizontal': 'center'
# # # #               },
# # # #     'gradient': {'colors': ['#DDEBCF',
# # # #                             '#9CB86E',
# # # #                             '#156B13']},
# # # #     'fill': {'none': True}
# # # # }
# # # #
# # # # worksheet.insert_textbox('B2', text, options)
# # # #
# # # # wb.close()
#
#
# import xlsxwriter
# import openpyxl
# import numpy as np
#
# wb = openpyxl.load_workbook("test.xlsx")
# ws = wb.worksheets[1]
# data = ws.cell(2, 5).value
# # print(data)
#
# song_count = 0
# songlst = []
# for row in range(ws.max_row):
#     song_count = song_count+1
#     if song_count == 1:
#         continue
#     # print(song_count)
#     rowlst = []
#     for col in range(1, 21):
#        rowlst.append(ws.cell(row+1, col).value)
#     songlst.append(rowlst)
# songlst = np.array(songlst)
# song_count = song_count - 1
# # songlst = songlst[songlst[:, 2].argsort()]
# # songlst = songlst[songlst[:, 0].argsort()]
# print(songlst)
# print(len(songlst[0]))
# #
# #
# #
# # import xlsxwriter
# # workbook = xlsxwriter.Workbook('demo.xlsx')
# #
# # # default cell format to size 10
# # workbook.formats[0].set_font_size(12)
# # workbook.formats[0].set_font_name('DengXian')
# #
# # worksheet = workbook.add_worksheet()
# #
# # # Write some simple text.
# # cell_format1 = workbook.add_format({   # 描述
# #     'font_size': 12,
# #     'text_wrap': True,
# #     'valign': 'vcenter',
# #     'align': 'left'
# # })
# #
# #
# # cell_format2 = workbook.add_format({   # A B D F H L M O P
# #     'text_wrap': True,
# #     'font_size': 14,
# #     'bold': True,
# #     'valign': 'vcenter',
# #     'align': 'center'
# # })
# #
# # cell_format3 = workbook.add_format({   # 歌名
# #     'font_size': 14,
# #     'bold': True,
# #     'color': 'red',
# #     'text_wrap': True,
# #     'valign': 'vcenter',
# #     'align': 'left'
# # })
# #
# # row = 0
# # for song in songlst:
# #     for col in range(0, 17):
# #         if col in [0,1,3,5,7,8,9,11,12,14,15]:
# #             worksheet.write(row+1, col, song[col], cell_format2)
# #         if col == 2:
# #             worksheet.write(row+1, col, song[col], cell_format3)
# #         if col in [4,6,10,13]:
# #             worksheet.write(row+1, col, song[col], cell_format1)
# #     row = row+1
# #
# #
# # # worksheet.conditional_format('A2:C9' ,
# # #     {'type':     'formula',
# # #      'criteria': '=MOD(ROW(),2)=0',
# # #      'format':   format1
# # #     })
# #
# #
# # worksheet = workbook.add_worksheet()
# #
# # # Write some simple text.
# # worksheet.write('A1', 'Hello')
# #
# # worksheet.write('A2', 'World')
# #
# # workbook.close()
# # for col in range(1, 21):
# #     value = ws.cell(row + 1, col).value
# #     if ws.cell(row + 1, col).value is None:
# #         value = ''
# #
# # song_spare_lst = []
# # for song in songlst:
# #     if not song[17] == '':
# #         song_spare_lst.append(song)
# # print()
# # num = len(song_spare_lst)
# # str_b = '{0:0'+ str(num) + 'b}'
# # for i in range(0, 200):
# #     point_select_array = np.zeros(num)
# #     point_select_str = str_b.format(i)
# #     for j in range(len(point_select_str)):
# #         m = point_select_str[j]
# #         point_select_array[j] = int(point_select_str[j])
# #     point_select_array = np.array(point_select_array)
# #     print(point_select_array)
#
#
# # # 作废
# # x6lst = []
# # d6lst = []
# # y6lst = []
# # p6lst = []
# # x8lst = []
# # d8lst = []
# # y8lst = []
# # p8lst = []
# # for item in full_lst:
# #     try:
# #         level = int(item[1])
# #         mode = int(item[20])
# #         if level in [6, 7]:
# #             if mode == 1:
# #                 x6lst.append(item)
# #             elif mode == 2:
# #                 d6lst.append(item)
# #             elif mode == 3:
# #                 y6lst.append(item)
# #             elif mode == 4:
# #                 p6lst.append(item)
# #         elif level in [8, 9, 10]:
# #             if mode == 1:
# #                 x8lst.append(item)
# #             elif mode == 2:
# #                 d8lst.append(item)
# #             elif mode == 3:
# #                 y8lst.append(item)
# #             elif mode == 4:
# #                 p8lst.append(item)
# #     except:
# #         pass



for i in range(0, num_required):
    modified_songlst = lst_ini[:]
    point_select_array = np.zeros(num_spare)
    point_select_str = str_b.format(i)
    songnamelst = []
    for j in range(len(point_select_str)):
        point_select_array[j] = int(point_select_str[j])
        if point_select_array[j] == 1:
            modified_songlst[spare_id[j]][8] = lst_ini[spare_id[j]][17]
            modified_songlst[spare_id[j]][10] = lst_ini[spare_id[j]][18]
            modified_songlst[spare_id[j]][11] = lst_ini[spare_id[j]][19]
            songnamelst.append(lst_ini[spare_id[j]][2])
        else:
            songnamelst.append('')
    # point_select_array = np.array(point_select_array)
    # point_select_matrix.append(point_select_array)
    modified_songllst.append(modified_songlst)
    dst.append(songnamelst)