"""
title:识别验证码图片
author：zhangyi
利用pytesseract，其精度不是很高
后期有待进行改进(进行训练)
"""


# -*-encoding:utf-8-*-
import pytesseract
from PIL import Image

# 测试的是pytesseract自带的图片，效果十分理想，完全没毛病
for i in range(1,7):
    image = Image.open("%d.jpg"%i)
    string = pytesseract.image_to_string(image)

    print(string)
