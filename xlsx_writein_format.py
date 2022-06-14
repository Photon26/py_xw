import openpyxl
import numpy as np
import xlsxwriter

def readin(fileroot, sheetn, colnum = 18):
    # colnum = 18 when mode is y or p
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
        songlst.append(rowlst)
    songlst = np.array(songlst)
    song_count = song_count - 1
    return songlst, song_count

def writein_format(songlst, workbook, mode, name):
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
    if mode == "x":
        color_first = '#d0d0d0'
        color_conditional = '#f0f0f0'
    if mode == "d":
        color_first = '#c4a8ee'
        color_conditional = '#f6efff'
    if mode == "y":
        color_first = '#f4b183'
        color_conditional = '#fdf1e9'
    if mode == "p":
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
    head = ['音序', '星级', '歌名', 'cb1', '描述1', 'cb2', '描述2', '指数', '单排cb', '单排技能', '单排描述', '指数', 'SSPcb', 'SSP描述', '指数', '半cb']

    worksheet = workbook.add_worksheet(name)
    count = 0
    for item in head:
        worksheet.write(0, count, item, cell_format_head)
        count = count+1
    for format in workbook.formats:
        format.set_font_name('DengXian')
    worksheet.set_column("C:C", 20)
    worksheet.set_column("E:E", 23.33)
    worksheet.set_column("G:G", 23.33)
    worksheet.set_column("K:K", 23.33)
    worksheet.set_column("N:N", 23.33)
    row = 0
    start_v = 'faferwefwq'
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

        if song[9] == "爆气":
            flag = 1
        else:
            flag = 0
        for col in range(0, 17):
            if col in [1, 3, 5, 7, 11, 12, 14, 15]:
                if song[col].isdigit():
                    worksheet.write_number(row + 1, col, int(song[col]), cell_format_bdfhlmop)
                else:
                    try:
                        worksheet.write_number(row + 1, col, float(song[col]), cell_format_bdfhlmop)
                    except:
                        worksheet.write(row + 1, col, song[col], cell_format_bdfhlmop)
            if col == 0:
                worksheet.write(row + 1, col, song[col], cell_format_a)
            if col == 2:
                if flag == 1:
                    worksheet.write(row + 1, col, song[col], cell_format_c2)
                else:
                    worksheet.write(row + 1, col, song[col], cell_format_c1)
            if col in [4, 6, 10, 13]:
                worksheet.write(row + 1, col, song[col], cell_format_egkn)
            if col in [8, 9]:
                if flag == 1:
                    worksheet.write(row + 1, col, song[col], cell_format_ij)
                else:
                    worksheet.write(row + 1, col, song[col], cell_format_bdfhlmop)
        str_long, str_len = str_maxlen(song[4], song[6])
        rowlen = int((str_long.count('\n')+(str_len-str_long.count('\n'))//22+1)/3*50)
        worksheet.set_row(row+1, rowlen)
        row = row + 1
    cell1 = 'A' + str(start + 2)
    cell2 = 'A' + str(row + 1)
    if start < row - 1:
        worksheet.merge_range(cell1 + ':' + cell2, start_v, cell_format_a)

    worksheet.conditional_format('B2:P'+str(row+1),
        {'type':     'formula',
         'criteria': '=MOD(ROW(),2)=0',
         'format':   format_bgc
        })
    worksheet.freeze_panes(1, 1)
    worksheet.protect()

def str_maxlen(str1, str2):
    len1 = int((len(str1.encode('utf-8'))-len(str1))/2+len(str1))
    len2 = int((len(str2.encode('utf-8'))-len(str2))/2+len(str2))
    if len1>len2:
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


if __name__ == "__main__":
    workbook = xlsxwriter.Workbook("demo.xlsx")
    llst = []
    for i in range(1, 5):
        lst, _ = readin("test1.xlsx", i)
        lst = lst[lst[:, 2].argsort()]
        lst = lst[lst[:, 0].argsort()]
        lst_67, lst_810 = separate(lst)
        llst.append(lst_67)
        llst.append(lst_810)


    writein_format(llst[0], workbook, "x", "星6-7")
    writein_format(llst[1], workbook, "x", "星8-10")
    writein_format(llst[2], workbook, "d", "弹6-7")
    writein_format(llst[3], workbook, "d", "弹8-10")
    writein_format(llst[4], workbook, "y", "弦6-7")
    writein_format(llst[5], workbook, "y", "弦8-10")
    writein_format(llst[6], workbook, "p", "泡6-7")
    writein_format(llst[7], workbook, "p", "泡8-10")

    workbook.close()