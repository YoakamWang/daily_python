# tesseract-ocr
# pip install pytesseract
# pip install pillow

# （1）Tesseract的安装及配置
# Tesseract的安装我们可以移步到该网址 https://digi.bib.uni-mannheim.de/tesseract/，我们可以看到如下界面：
# 有很多版本供大家选择，大家可以根据自己的需求选择。其中w32表示32位系统，w64表示64位系统，大家选择合适的版本即可，可能下载速度比较慢，大家可以选择链接：https://pan.baidu.com/s/1YQCMnx-wCeNrJEE3wcEnQA 提取码：rbc6下载。安装时我们需要知道我们安装的位置，将安装目录配置到系统path变量当中，我们路径是D:\CodeField\Tesseract-OCR。
# 我们右击我的电脑/此电脑->属性->高级系统设置->环境变量->Path->编辑->新建然后将我们的路径复制进去即可。添加好系统变量后后我们还需要依次点确定，这样才算配置好了

import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = 'f:/tessert/tesseract.exe'
img = Image.open('test.png')
text = pytesseract.image_to_string(img, lang='chi_sim')
print(text)

import os
import pytesseract
# 文字图片的路径
path = 'text_img/'
# 获取图片路径列表
imgs = [path + i for i in os.listdir(path)]
# 打开文件
f = open('text.txt', 'w+', encoding='utf-8')
# 将各个图片的路径写入text.txt文件当中
for img in imgs:
  f.write(img + '\n')
# 关闭文件
f.close()
# 文字识别
string = pytesseract.image_to_string('text.txt', lang='chi_sim')
print(string)