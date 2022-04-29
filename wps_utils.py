import openpyxl
from xlutils.copy import copy
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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

def add_pic(workbook, img_path, place_lst = ['A1']):
    res = len(workbook.sheetnames)
    # print(res)
    # res = 1
    for i in range(0, res):
        img = openpyxl.drawing.image.Image(img_path)
        ws = workbook.worksheets[i]
        for pos in place_lst:
            img.anchor = pos
            # print(pos)
            ws.add_image(img)

def make_watermark(num, img_name, width = 1375, height = 8000, x_step = 500, y_step = 400):
    font = ImageFont.truetype("simhei.ttf", 100)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # make transparent background
    draw = ImageDraw.Draw(img)
    # for i in range(0, height, y_step):
    #     for j in range(0, width, x_step):
    #         pos = (j, i)
    #         draw.text(pos, str(num), (0, 0, 0, 40), font=font)
    # # img = img.rotate(30)
    # img.save(img_name + '.png')

    # make rotated watermark
    draw.text((50, 100), str(num), (0, 0, 0, 40), font=font)



if __name__ == "__main__":
    # copy(10, "工作簿1.xls", "C:/Users/gao/Desktop/x", "星弹")
    import openpyxl
    #
    # wb = openpyxl.load_workbook('out.xlsx')
    # ws = wb.worksheets[0]
    # add_pic(wb, 'test.jpg')
    # wb.save('out.xlsx')
    from PIL import Image

    from PIL import ImageFont
    from PIL import ImageDraw

    font = ImageFont.truetype("simhei.ttf", 100)

    # plot digit numbers (from 0 to 9):

    i = 988762
    img = Image.new('RGBA', (400, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # draw.text((0,0), str(i), (0, 0, 0, 30), font=font)
    draw.text((50, 100), str(855564), (0, 0, 0, 40), font=font)
    # img = Image.open("tst_988762.png")
    img = img.rotate(30)
    img.save("test1.png")

    # img.save('tst_' + str(i) + '.png')
    # make_watermark(699865, "tst")
    # wb = openpyxl.load_workbook('test.xlsx')
    # add_pic(wb, "tst.png")
    # wb.save('out.xlsx')
    #

