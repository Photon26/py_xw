import wps_utils as wu
import openpyxl

#  for test
wu.make_watermark(699865, "tst", x_step=250, y_step=200, size=70)
wb = openpyxl.load_workbook('S3-星弹.xlsx')
wu.add_pic(wb, "tst.png")
wb.save('out.xlsx')