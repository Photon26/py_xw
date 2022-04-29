import openpyxl
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil
import os
import random as r
import pickle

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

def copy_single(filename, root, target):
    """
    input:
    · root->file1, file2, ...
    · target: folder name to save the file, usually "mode/" + str(num)
    output:
    · root->mode->target->file
    """
    dir = root+"/"+target
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    shutil.copyfile(root+"/"+filename, dir+"/"+filename)
    return dir+"/"+filename

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

def make_watermark(num, img_name, width = 1375, height = 8000, x_step = 500, y_step = 400, size = 100):
    font = ImageFont.truetype("simhei.ttf", size)
    img = Image.new('RGBA', (x_step, y_step), (0, 0, 0, 0))  # make transparent background
    draw = ImageDraw.Draw(img)
    # for i in range(0, height, y_step):
    #     for j in range(0, width, x_step):
    #         pos = (j, i)
    #         draw.text(pos, str(num), (0, 0, 0, 40), font=font)
    # # img = img.rotate(30)
    # img.save(img_name + '.png')

    # make rotated watermark
    draw.text((size/2, size), str(num), (0, 0, 0, 40), font=font)   # Transparency
    img = img.rotate(30)
    # paste the watermark together
    new_image = Image.new('RGBA',(width, height), (0, 0, 0, 0))
    for j in range(0, height, y_step):
        for i in range(0, width, x_step):
            next_pos = (i, j)
            # print(next_pos)
            new_image.paste(img, next_pos)
    new_image.save(img_name + ".png")


def code_dst_gen(count, num_digit, name, save_path=""):
    list=set("")
    while len(list)<count:
        x=r.randint(pow(10, num_digit-1),pow(10, num_digit))
        list.add(x)
    pickle.dump(list, open(save_path + name + ".pkl", 'wb'))


if __name__ == "__main__":
    # copy(10, "工作簿1.xls", "C:/Users/gao/Desktop/x", "星弹")
    # import openpyxl
    #
    # wb = openpyxl.load_workbook('out.xlsx')
    # ws = wb.worksheets[0]
    # add_pic(wb, 'test.jpg')
    # wb.save('out.xlsx')
    # from PIL import Image
    #
    # from PIL import ImageFont
    # from PIL import ImageDraw
    #
    # font = ImageFont.truetype("simhei.ttf", 100)

    # plot digit numbers (from 0 to 9):

    # i = 988762
    # img = Image.new('RGBA', (400, 300), (0, 0, 0, 0))
    # draw = ImageDraw.Draw(img)
    # # draw.text((0,0), str(i), (0, 0, 0, 30), font=font)
    # draw.text((50, 100), str(855564), (0, 0, 0, 40), font=font)
    # # img = Image.open("tst_988762.png")
    # img = img.rotate(30)
    # img.save("test1.png")

    # img.save('tst_' + str(i) + '.png')

    # #  for test
    # make_watermark(699865, "tst", x_step=250, y_step=200, size=70)
    # wb = openpyxl.load_workbook('test.xlsx')
    # add_pic(wb, "tst.png")
    # wb.save('out.xlsx')

    #  set mode number and root folder
    # num_xd = 130
    # num_xx = 20
    # num_xp = 20
    # num_dx = 30
    # num_dp = 20
    # num_px = 40
    # num_4 = 60
    # num_p = 40

    #  small num set for test
    num_xd = 5
    num_xx = 5
    num_xp = 5
    num_dx = 5
    num_dp = 5
    num_px = 5
    num_4 = 5
    num_p = 5

    root_folder = "D:/Photon/Desktop/S4-2022"
    season = "S4-"
    num_sum = num_xd+num_xx+num_xp+num_dx+num_dp+num_px+num_4

    #  generate dst
    code_dst_gen(num_sum, 6, "2022-s4")  # TODO: delete it when once generated the dst

    mode = ""
    dst = pickle.load(open("2022-s4.pkl", "rb"))
    dst = list(dst)
    for i in range(0, num_sum):
        #  classify mode and copy files
        if i < num_xd:
            mode = "xd"
            filepath = copy_single(season+"星弹.xlsx", root_folder, season+"星弹/"+str(i))
        elif i < num_xd+num_xx:
            mode = "xx"
            filepath = copy_single(season+"星弦.xlsx", root_folder, season+"星弦/"+str(i))
        elif i < num_xd+num_xx+num_xp:
            mode = "xp"
            filepath = copy_single(season+"星泡.xlsx", root_folder, season+"星泡/"+str(i))
        elif i < num_xd+num_xx+num_xp+num_dx:
            mode = "dx"
            filepath = copy_single(season+"弹弦.xlsx", root_folder, season+"弹弦/"+str(i))
        elif i < num_xd+num_xx+num_xp+num_dx+num_dp:
            mode = "dp"
            filepath = copy_single(season+"弹泡.xlsx", root_folder, season+"弹泡/"+str(i))
        elif i < num_xd+num_xx+num_xp+num_dx+num_dp+num_px:
            mode = "px"
            filepath = copy_single(season+"泡弦.xlsx", root_folder, season+"泡弦/"+str(i))
        elif i < num_xd+num_xx+num_xp+num_dx+num_dp+num_px+num_4:
            mode = "4"
            filepath = copy_single(season+"四模.xlsx", root_folder, season+"四模/"+str(i))
        else:
            mode = "p"
            filepath = copy_single(season+"泡泡.xlsx", root_folder, season+"泡泡/"+str(i))

        #  add watermark
        wb = openpyxl.load_workbook(filepath)
        num = dst[i]
        make_watermark(num, "tst", x_step=250, y_step=200, size=70)
        add_pic(wb, "tst.png")
        wb.save(filepath)