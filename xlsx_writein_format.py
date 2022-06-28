# 函数默认值不能给lst
import os.path

import openpyxl
import numpy as np
import xlsxwriter
import copy
import random as r

def readin(fileroot, sheetn, colnum = 21, f_season = 's7'):
    # colnum = 19 when mode is y or p (season included)
    # colnum = 21 when mode is x or d (season included)
    wb = openpyxl.load_workbook(fileroot)
    ws = wb.worksheets[sheetn]
    song_count = 0
    songlst = []
    for row in range(ws.max_row):
        song_count = song_count + 1
        if song_count == 1:
            continue
        rowlst = []
        for col in range(1, colnum):
            value = ws.cell(row + 1, col).value
            if ws.cell(row + 1, col).value is None:
                value = ''
            rowlst.append(value)
        if not rowlst[16] == '无' or rowlst[16] == f_season:
            songlst.append(rowlst)
    songlst = np.array(songlst)
    song_count = song_count - 1
    return songlst, song_count

def readin_all(fileroot, colnum = 21, f_season = '7'):
    # colnum = 19 when mode is y or p (season included)
    # colnum = 21 when mode is x or d (season included)
    # Note that in openpyxl, col num is from 1
    wb = openpyxl.load_workbook(fileroot)
    song_count = 0
    songlst = []
    for i in range(1, 5):
        # 1 is x, 2 is d, 3 is y, 4 is p
        ws = wb.worksheets[i]
        for row in range(ws.max_row):
            song_count = song_count + 1
            if ws.cell(row + 1, 3).value == "歌名":
                continue
            rowlst = []
            for col in range(1, colnum):
                value = ws.cell(row + 1, col).value
                if ws.cell(row + 1, col).value is None:
                    value = ''
                rowlst.append(value)
            if i in [3, 4]:
                rowlst[17] = ''
                rowlst[18] = ''
                rowlst[19] = ''
            rowlst.append(i)    # rowlst[20] = mode
            if not rowlst[16] == '无' and not rowlst[16] == 'S'+f_season and not rowlst[16] == 's'+f_season:
                songlst.append(rowlst)
        song_count = song_count - 1
    return songlst

def writein_format(songlst, workbook, mode, name, sspflag = 0):
    """
    lst[0]: alpha
    lst[1]: level
    lst[2]: name
    lst[3]: cb1
    lst[4]: disc1
    lst[5]: cb2
    lst[6]: disc2
    lst[7]: indexd
    lst[8]: cb
    lst[9]: skill
    lst[10]: disc
    lst[11]: indexs
    lst[12]: sspcb
    lst[13]: discssp
    lst[14]: indexssp
    lst[15]: halfcb
    lst[16]: season
    """
    color_first = 'black'
    color_conditional = 'white'
    if mode == "星":
        color_first = '#d0d0d0'
        color_conditional = '#f0f0f0'
    if mode == "弹":
        color_first = '#c4a8ee'
        color_conditional = '#f6efff'
    if mode == "弦":
        color_first = '#f4b183'
        color_conditional = '#fdf1e9'
    if mode == "泡":
        color_first = '#6eaaf2'
        color_conditional = '#e5f1ff'

    cell_format_a = workbook.add_format({  # 首列
        'font_size': 14,
        'text_wrap': True,
        'bg_color': color_first,
        'valign': 'vcenter',
        'bold': True,
        'align': 'center',
        'border': 1,
        'border_color': '#7c7c7c',
    })

    cell_format_bdfhlmop = workbook.add_format({  # D F H L M O P (I J 无爆气)
        'font_size': 14,
        'text_wrap': True,
        'valign': 'vcenter',
        'bold': True,
        'align': 'center',
        'border': 1,
        'border_color': '#7c7c7c',
    })


    cell_format_c1 = workbook.add_format({  # 歌名
        'text_wrap': True,
        'font_size': 14,
        'bold': True,
        'valign': 'vcenter',
        'align': 'left',
        'border': 1,
        'color': 'black',
        'border_color': '#7c7c7c'
    })

    cell_format_c2 = workbook.add_format({  # 歌名-爆气
        'text_wrap': True,
        'font_size': 14,
        'bold': True,
        'color': 'red',
        'valign': 'vcenter',
        'align': 'left',
        'border': 1,
        'border_color': '#7c7c7c'
    })

    cell_format_egkn = workbook.add_format({  # 描述
        'font_size': 12,
        'valign': 'vcenter',
        'align': 'left',
        'text_wrap': True,
        'border': 1,
        'border_color': '#7c7c7c'
    })

    cell_format_ij = workbook.add_format({  # I J 爆气
        'font_size': 14,
        'text_wrap': True,
        'valign': 'vcenter',
        'color': 'red',
        'bold': True,
        'align': 'center',
        'border': 1,
        'border_color': '#7c7c7c'
    })

    cell_format_head = workbook.add_format({  # 首行
        'font_size': 16,
        'text_wrap': True,
        'bg_color': color_first,
        'valign': 'vcenter',
        'bold': True,
        'align': 'center',
        'border': 1,
        'border_color': '#7c7c7c',
    })

    format_bgc = workbook.add_format({'bg_color': color_conditional})
    if sspflag == 0:
        head = ['音序', '星级', '歌名', 'cb1', '描述1', 'cb2', '描述2', '指数', '单排cb', '单排技能', '单排描述', '指数', '半cb']
    else:
        head = ['音序', '星级', '歌名', 'SSPcb', 'SSP描述', '指数', '半cb']

    worksheet = workbook.add_worksheet(name)
    count = 0
    for item in head:
        worksheet.write(0, count, item, cell_format_head)
        count = count+1
    for format_ in workbook.formats:
        format_.set_font_name('DengXian')
    if sspflag == 0:
        worksheet.set_column("C:C", 20)
        worksheet.set_column("E:E", 23.33)
        worksheet.set_column("G:G", 23.33)
        worksheet.set_column("K:K", 23.33)
    else:
        worksheet.set_column("C:C", 35)
        worksheet.set_column("D:D", 26)
        worksheet.set_column("E:E", 44)
    row = 0
    start_v = 'sdfdf'   # TODO: change it to ''
    start = 0
    for song in songlst:  # 处理 row+1 行的数据
        if not song[0] == start_v:
            cell1 = 'A' + str(start + 2)
            cell2 = 'A' + str(row + 1)
            if start < row-1:
                worksheet.merge_range(cell1 + ':' + cell2, start_v, cell_format_a)
            start = row
            start_v = song[0]
            # print(cell1, cell2)
        if sspflag == 0:
            #   单双排
            if song[9] == "爆气":
                flag = 1
            else:
                flag = 0
            for col in [1, 3, 5, 7, 11, 15]:
                if col == 15:
                    wcol = 12
                else:
                    wcol = col
                if isinstance(song[col], int) or isinstance(song[col], float):
                    worksheet.write_number(row + 1, wcol, int(song[col]), cell_format_bdfhlmop)
                elif song[col].isdigit():
                    worksheet.write_number(row + 1, wcol, int(song[col]), cell_format_bdfhlmop)
                else:
                    try:
                        worksheet.write_number(row + 1, wcol, float(song[col]), cell_format_bdfhlmop)
                    except:
                        worksheet.write(row + 1, wcol, song[col], cell_format_bdfhlmop)
            worksheet.write(row + 1, 0, song[0], cell_format_a)   # 音序
            if flag == 1:   # 歌名
                worksheet.write(row + 1, 2, song[2], cell_format_c2)
            else:
                worksheet.write(row + 1, 2, song[2], cell_format_c1)
            for col in [4, 6, 10]:  # 描述
                worksheet.write(row + 1, col, song[col], cell_format_egkn)
            for col in [8, 9]:  # 技能、cb
                if flag == 1:
                    worksheet.write(row + 1, col, song[col], cell_format_ij)
                else:
                    worksheet.write(row + 1, col, song[col], cell_format_bdfhlmop)
            str_long, str_len = str_maxlen(song[4], song[6])
            rowlen = int((str_long.count('\n')+(str_len-str_long.count('\n'))//22+1)/3*50)
        else:
            #   SSP
            for col in [1, 14, 15]:
                if col == 1:
                    wcol = 1    # 星级
                elif col == 14:
                    wcol = 5    # 指数
                elif col == 15:
                    wcol = 6    # 半cb
                if song[col].isdigit():
                    worksheet.write_number(row + 1, wcol, int(song[col]), cell_format_bdfhlmop)
                else:
                    try:
                        worksheet.write_number(row + 1, wcol, float(song[col]), cell_format_bdfhlmop)
                    except:
                        worksheet.write(row + 1, wcol, song[col], cell_format_bdfhlmop)
            worksheet.write(row + 1, 0, song[0], cell_format_a)     # 音序
            worksheet.write(row + 1, 2, song[2], cell_format_c2)    # 歌名
            worksheet.write(row + 1, 4, song[13], cell_format_egkn)     # 描述
            worksheet.write(row + 1, 3, song[12], cell_format_ij)       # cb

            str_long, str_len = str_maxlen('', song[13])
            rowlen = int((str_long.count('\n')+(str_len-str_long.count('\n'))//40+1)/3*48)

        worksheet.set_row(row+1, rowlen)
        row = row + 1
    cell1 = 'A' + str(start + 2)
    cell2 = 'A' + str(row + 1)
    if start < row - 1:
        worksheet.merge_range(cell1 + ':' + cell2, start_v, cell_format_a)

    if sspflag ==0:
        cond_str = 'B2:M'
    else:
        cond_str = 'B2:G'
    worksheet.conditional_format(cond_str+str(row+1),
    {'type':     'formula',
     'criteria': '=MOD(ROW(),2)=0',
     'format':   format_bgc
    })
    worksheet.freeze_panes(1, 1)
    worksheet.protect()

def str_maxlen(str1, str2):
    len1 = int((len(str1.encode('utf-8'))-len(str1))/2+len(str1))
    len2 = int((len(str2.encode('utf-8'))-len(str2))/2+len(str2))
    if len1 > len2:
        return str1, len1
    else:
        return str2, len2

def separate(lst):
    lst_67 = []
    lst_810 = []
    for item in lst:
        try:
            level = int(item[1])
            if level in [6, 7]:
                lst_67.append(item)
            elif level in [8, 9, 10]:
                lst_810.append(item)
        except:
            pass
    return lst_67, lst_810


def gen_all_songlst_modified(lst_ini, num_required):
    # TODO: make sure num_required is smaller than power(2, spare_num)
    # song_spare_lst = []
    spare_id = []
    count = 0
    num_spare = 0
    for song in lst_ini:
        if not song[17] == '':   # make sure all None has been converted to ''
            # song_spare_lst.append(song)
            spare_id.append(count)
            num_spare = num_spare + 1
            # print(song[17], song[2])
        count = count + 1
    # num_spare = len(song_spare_lst)
    # print(num_spare)

    dst = []

    str_b = '{0:0' + str(num_spare) + 'b}'
    # point_select_matrix = []
    modified_songllst = []

    list = set("")
    while len(list) < num_required:
        x = r.randint(0, pow(2, num_spare)-1)
        list.add(x)
    for i in list:
        modified_songlst = copy.deepcopy(lst_ini)
        point_select_array = np.zeros(num_spare)
        point_select_str = str_b.format(i)
        songnamelst = []
        for j in range(len(point_select_str)):
            point_select_array[j] = int(point_select_str[j])
            if point_select_array[j] == 1:
                modified_songlst[spare_id[j]][8] = lst_ini[spare_id[j]][17]
                modified_songlst[spare_id[j]][10] = lst_ini[spare_id[j]][18]
                modified_songlst[spare_id[j]][11] = lst_ini[spare_id[j]][19]
                songnamelst.append(lst_ini[spare_id[j]][2] + str(lst_ini[spare_id[j]][20]))
            else:
                songnamelst.append('')
        # point_select_array = np.array(point_select_array)
        # point_select_matrix.append(point_select_array)
        modified_songllst.append(modified_songlst)
        dst.append(songnamelst)
    return modified_songllst, dst

def gen_file_with_fulllst(cata, full_lst, output_root, sspflag, season = ''):
    # Given a songlst with all mode and all level,
    # Generate file with name.
    xl = []
    dl = []
    yl = []
    pl = []
    for item in full_lst:
        mode = item[20]
        if mode == 1:
            xl.append(item)
        elif mode == 2:
            dl.append(item)
        elif mode == 3:
            yl.append(item)
        elif mode == 4:
            pl.append(item)
    lst_4 = [xl, dl, yl, pl]

    if cata == "星弹":
        q = [0, 1]
    elif cata == "星弦":
        q = [0, 2]
    elif cata == "星泡":
        q = [0, 3]
    elif cata == "弹弦":
        q = [1, 2]
    elif cata == "弹泡":
        q = [1, 3]
    elif cata == "弦泡":
        q = [2, 3]
    elif cata == "泡泡":
        q = [3]
    elif cata == "四模":
        q = [0, 1, 2, 3]

    name = ["星", "弹", "弦", "泡"]
    if not (os.path.exists(output_root)):
        os.makedirs(output_root)
    if sspflag == 1:
        output_file = output_root + '/' + season + cata + 'SSP' + '.xlsx'
    else:
        output_file = output_root + '/' + season + cata + '.xlsx'
    workbook = xlsxwriter.Workbook(output_file)
    for m in q:
        lst_m = lst_4[m]
        lst_m = np.array(lst_m)
        lst_m = lst_m[lst_m[:, 2].argsort()]
        lst_m = lst_m[lst_m[:, 0].argsort()]
        lst67, lst810 = separate(lst_m)
        writein_format(lst67, workbook, name[m], name[m]+"6-7", sspflag)
        writein_format(lst810, workbook, name[m], name[m] + "8-10", sspflag)

    workbook.close()


if __name__ == "__main__":
    # from win32com.client import Dispatch
    import win32com.client as win32

    # xl = Dispatch("Excel.Application")
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = False  # You can remove this line if you don't want the Excel application to be visible

    songlst_all = readin_all("test.xlsx")

    songdst, dst = gen_all_songlst_modified(songlst_all, 10)

    songlst = songdst[0]
    # print(dst[0])
    # print(songdst[0]==songlst_all)
    root = 'F:/py_xw/'
    # print(dst)

    for name in ['星弹', '星弦', '星泡', '弹弦', '弹泡', '弦泡', '四模', '泡泡']:

        gen_file_with_fulllst(name, songlst, name + ".xlsx", 0)
        gen_file_with_fulllst(name, songlst, name + "SSP.xlsx", 1)
        wb1 = xl.Workbooks.Open(root + "test.xlsx")
        wb2 = xl.Workbooks.Open(root+name + ".xlsx")
        wb3 = xl.Workbooks.Open(root+name + "SSP.xlsx")
        ws1 = wb1.Worksheets(1)
        ws1.Copy(Before=wb2.Worksheets(1))
        ws1.Copy(Before=wb3.Worksheets(1))
        wb2.Close(SaveChanges=True)
        wb3.Close(SaveChanges=True)

        title1 = '2022年S5赛季' + name + '爆气表说明'
        title2 = '2022年S5赛季' + name + 'SSP爆气表说明'

        wb2 = openpyxl.load_workbook(root+name + ".xlsx")
        wb2.worksheets[0].cell(1, 1).value = title1
        wb2.save(root+name + ".xlsx")
        wb3 = openpyxl.load_workbook(root + name + "SSP.xlsx")
        wb3.worksheets[0].cell(1, 1).value = title2
        wb3.save(root + name + "SSP.xlsx")

    xl.Quit()