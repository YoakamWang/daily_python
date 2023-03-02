from pdf2docx import Converter

pdf_file = r'D:\Files\OEM&ASP\robot navigation test.pdf'
docx_file = r'D:\Files\OEM&ASP\robot.docx'
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()



#https://www.latexlive.com/home,识别pdf里面的数学公式，然后复制MathML到word里面，，，，搞定！！！   牛牛牛牛！！！


# from PyPDF2 import PdfFileReader
# with open(pdf_file,'r',encoding='symbol') as f:
#     pdf=PdfFileReader(f)
#     page=pdf.getPage(10)
#     print(page)
#     text=page.extractText()
#     print(text)


# from pdfreader import SimplePDFViewer, PageDoesNotExist
#
# fd = open(pdf_file, "rb")
# viewer = SimplePDFViewer(fd)
#
# plain_text = ""
# pdf_markdown = ""
# images = []
# try:
#     while True:
#         viewer.render()
#         pdf_markdown += viewer.canvas.text_content
#         plain_text += "".join(viewer.canvas.strings)
#         images.extend(viewer.canvas.inline_images)
#         images.extend(viewer.canvas.images.values())
#         viewer.next()
#         print(plain_text)
# except PageDoesNotExist:
#     pass
