# # from PIL import Image
# from PIL import Image, ImageDraw, ImageFont
# ##pip install pillow
# #
# # import datetime
# import time
#
#
# def pic_add(textin1, textin2, savename):  # 第一行文本，，第二行文本需要保存的图片名字
#     # pip install pillow
#     # 创建底图
#     target = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
#     # 打开头像
#     nike_image = Image.open("./image1.jpg")
#     # nike_image = nike_image.resize((300, 300))
#
#     # 打开装饰，水印图片，这里用固定值了，有需要的可以设置为变量
#     hnu_image = Image.open("./ll.jpg")
#     # 分离透明通道
#     r, g, b, a = hnu_image.split()
#     # 将头像贴到底图
#     nike_image.convert("RGBA")
#     target.paste(nike_image, (0, 0))
#     # 将装饰贴到底图
#     hnu_image.convert("RGBA")
#     target.paste(hnu_image, (0, 0), mask=a)
#
#     draw = ImageDraw.Draw(target)
#     # 显示图片
#     # target.show()
#     # rawsocket.sendto(imcp_packet,(dst_addr,80))
#     # OSError: [WinError 10049] 在其上下文中，该请求的地址无效。
#
#     # 选择文字字体和大小
#     setFont1 = ImageFont.truetype('C:/windows/Fonts/simsun.ttc', 30)
#     draw.text((40, 40), textin1, font=setFont1, fill='#0000ff', direction=None)
#     setFont2 = ImageFont.truetype('C:/windows/Fonts/msyh.ttc', 60)
#     draw.text((40, 100), textin2, font=setFont2, fill='#FF0000', direction=None)
#
#     setFont3 = ImageFont.truetype('C:/windows/Fonts/SIMYOU.TTF', 20)
#     # draw.text((40,200),str(datetime.datetime.now()),font=setFont3,fill='#FFFFFF',direction=None)
#     draw.text((40, 200), str(time.strftime("%d/%m/%Y")), font=setFont3, fill='#FFFFFF', direction=None)
#     # target.show()
#
#     # 保存图片，只能保存为png格式！
#     target.save(savename)
#
#
# ##########################
# #
# # python读取excel操作开始
# #
# ##########################
# import openpyxl
#
# # pip install openpyxl
# # pip install pymodel
#
# # 打开excel文件,获取工作簿对象
# wb = openpyxl.load_workbook('商品示例.xlsx')
#
# # 从工作薄中获取一个表单(sheet)对象
# # sheets = wb.sheetnames
# # print(sheets, type(sheets))
#
# # 创建一个表单  代码无效？？
# # mySheet = wb.create_sheet('Sheet1')
# # print(wb.sheetnames)
#
# # 获取指定的表单
# # sheet3 = wb.get_sheet_by_name('商品信息')
# # DeprecationWarning: Call to deprecated function get_sheet_by_name(Use wb[sheetname]).
#
# # sheet4 = wb['商品信息']
#
# # for sheet in wb:
# #    print(sheet.title)
#
# ws = wb.active  # 当前活跃的表单
# # print(ws) #<Worksheet "商品信息">
# # print(ws['A1']) # 获取A列的第一个对象   #<Cell '商品信息'.A1>
# # print(ws['A1'].value) #商品信息xxx
#
# # c = ws['B1']
# # print('Row {}, Column {} is {}'.format(c.row, c.column, c.value)) # 打印这个单元格对象所在的行列的数值和内容
# # print('Cell {} is {}\n'.format(c.coordinate, c.value)) # 获取单元格对象的所在列的行数和值
# # print(ws.cell(row=1, column=2)) # 获取第一行第二列的单元格
# # print(ws.cell(row=1, column=2).value)
# # print('{}行 {}列'.format(ws.max_row, ws.max_column)) #行和列的总数
#
# max_excel_row = int(format(ws.max_row)) + 1
# # print(max_excel_row)
#
# i = 1
# j = 0
# for i in range(1, max_excel_row):
#     # print(i)
#     name = str(ws.cell(i, 2).value)
#     guige_picname = str(ws.cell(i, 11).value)
#     gongying_name = str(ws.cell(i, 1).value)
#
#     if name != '' and guige_picname != 'None':
#         pic_name = guige_picname + '.png'
#         print('正在写入第(' + str(i) + '/' + str(max_excel_row - 1) + ')个商品：' + name + ' 的图片文件：' + pic_name)
#         write_text1 = gongying_name
#         write_text2 = '[' + name + ']'
#         pic_add(write_text1, write_text2, pic_name)
#         j = j + 1
#
# print('写入有效商品图片个数：' + str(j))

# coding=UTF-8
import xlrd
import xlwt
import requests
import json
import xlsxwriter
from xlutils.copy import copy
import glob
def  insert(workbook,sheet_name_xls,value_title,url,picturePath,):
    lengh=len(picturePath)
    sheet = workbook.add_worksheet(sheet_name_xls)  # 在工作簿中新建一个表格
    index = len(value_title)
    for i in range(0, index):
        for j in range(0, len(value_title[i])):
            sheet.write(i, j, value_title[i][j])  # 像表格中写入数据（对应的行和列）
            print("xls格式表格写入数据成功！")
    arrayList = []
    for t in range(0, lengh):  # 通过range()把行数生成一个可迭代对象
        files = {'photo': open(picturePath[t], 'rb')}
        # print(uploadpicture(url, files))
        list = []  ## 空列表
        list.append(url)  ## 使用 append() 添加元素
        print(picturePath[t])
        text = uploadpicture(url, files)
        list.append(text)
        list.append(picturePath[t])
        try:
            re = json.loads(text)
            if re['status']==200:
                list.append('成功')
            else:
                list.append('失败')
            data = re['data']
            list.append(str(data['score']))
            arrayList.append(list)
            print(list)
        except Exception as e:
            print(e)
            continue


    rows_old = 1  # 获取表格中已存在的数据的行数
    index1 = len(arrayList)  # 获取需要写入数据的行数
    for i in range(0, index1):
        for j in range(0, len(arrayList[i])):
            if j == 2:
                try:
                    sheet.insert_image(i + rows_old, j, arrayList[i][j], {'x_scale': 0.1, 'y_scale': 0.1})
                except IOError:
                    sheet.write(i + rows_old, j, arrayList[i][j])
            else:
                sheet.write(i + rows_old, j, arrayList[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入

                # new_workbook.save(path)  # 保存工作簿
                # print("xls格式表格【追加】写入数据成功！")
def  uploadpicture(url,files ):
    r = requests.post(url, files=files)
    return r.text
book_name_xls  = '身份证识别接口统计表耳环.xlsx'
sheet_name_xls = '身份证识图片识别是否有人脸，是否闭眼picture1'
value_title = [["url", "data", "图片", "机器识别结果","阈值"],]
workbook = xlsxwriter.Workbook(book_name_xls)  # 新建一个工作簿
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello world')

workbook.close()
