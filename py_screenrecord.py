# import tkinter
#
# import tkinter.filedialog
#
# import os
#
# from PIL import ImageGrab
#
# from time import sleep
#
# # 创建tkinter主窗口
#
# root = tkinter.Tk()
#
# # 指定主窗口位置与大小
#
# root.geometry('100x40+400+300')
#
# # 不允许改变窗口大小
#
# root.resizable(False, False)
#
#
# class MyCapture:
#
#     def __init__(self, png):
#
#         # 变量X和Y用来记录鼠标左键按下的位置
#
#         self.X = tkinter.IntVar(value=0)
#
#         self.Y = tkinter.IntVar(value=0)
#
#         # 屏幕尺寸
#
#         screenWidth = root.winfo_screenwidth()
#
#         screenHeight = root.winfo_screenheight()
#
#         # 创建顶级组件容器
#
#         self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
#
#         # 不显示最大化、最小化按钮
#
#         self.top.overrideredirect(True)
#
#         self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)
#
#         # 显示全屏截图，在全屏截图上进行区域截图
#
#         self.image = tkinter.PhotoImage(file=png)
#
#         self.canvas.create_image(screenWidth // 2, screenHeight // 2, image=self.image)
#
#     # 鼠标左键按下的位置
#
#     def onLeftButtonDown(self, event):
#
#         self.X.set(event.x)
#
#         self.Y.set(event.y)
#
#         # 开始截图
#
#         self.sel = True
#
#         self.canvas.bind('<Button-1>', self.onLeftButtonDown)
#
#     # 鼠标左键移动，显示选取的区域
#
#     def onLeftButtonMove(self, event):
#
#         if not self.sel:
#
#             return
#
#         global lastDraw
#
#         try:
#
#             # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
#
#             self.canvas.delete(lastDraw)
#
#         except Exception as e:
#
#             pass
#
#             lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')
#
#             self.canvas.bind('<B1-Motion>', self.onLeftButtonMove)
#
#         # 获取鼠标左键抬起的位置，保存区域截图
#
#     def onLeftButtonUp(self, event):
#         self.sel = False
#
#         try:
#
#             self.canvas.delete(lastDraw)
#
#         except Exception as e:
#
#             pass
#
#
#         sleep(0.1)
#
#         # 考虑鼠标左键从右下方按下而从左上方抬起的截图
#
#         left, right = sorted([self.X.get(), event.x])
#
#         top, bottom = sorted([self.Y.get(), event.y])
#
#         pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
#
#         # 弹出保存截图对话框
#
#         fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('JPG files', '*.jpg')])
#
#         if fileName:
#             pic.save(fileName + '.jpg')
#
# # 关闭当前窗口
#
#         self.top.destroy()
#
#         self.canvas.bind('<ButtonRelease-1>', self.onLeftButtonUp)
#
#         self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
#
#
# # 开始截图
#
# def buttonCaptureClick():
#     # 最小化主窗口
#
#     root.state('icon')
#
#     sleep(0.2)
#
#     filename = 'temp.png'
#
#     im = ImageGrab.grab()
#
#     im.save(filename)
#
#     im.close()
#
#     # 显示全屏幕截图
#
#     w = MyCapture(filename)
#
#     buttonCapture.wait_window(w.top)
#
#     # 截图结束，恢复主窗口，并删除临时的全屏幕截图文件
#
#     root.state('normal')
#
#     os.remove(filename)
#
#
# buttonCapture = tkinter.Button(root, text='截图', command=buttonCaptureClick)
#
# buttonCapture.place(x=10, y=10, width=80, height=20)
#
# # 启动消息主循环
#
# root.mainloop()

import time,threading
from datetime import datetime
from PIL import ImageGrab
from cv2 import *
import numpy as np
from cv2 import VideoWriter_fourcc, VideoWriter, cvtColor, COLOR_RGB2BGR, VideoCapture, CAP_PROP_FPS, \
  CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from pynput import keyboard
def video_record():   # 录入视频
  global name
  name = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # 当前的时间（当文件名）
  screen = ImageGrab.grab() # 获取当前屏幕
  width, high = screen.size # 获取当前屏幕的大小
  fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D') # MPEG-4编码,文件后缀可为.avi .asf .mov等
  video = VideoWriter('%s.avi' % name, fourcc, 15, (width, high)) # （文件名，编码器，帧率，视频宽高）
  #print('3秒后开始录制----')  # 可选
  #time.sleep(3)
  print('开始录制!')
  global start_time
  start_time = time.time()
  while True:
    if flag:
      print("录制结束！")
      global final_time
      final_time = time.time()
      video.release() #释放
      break
    im = ImageGrab.grab()  # 图片为RGB模式
    imm = cvtColor(np.array(im), COLOR_RGB2BGR) # 转为opencv的BGR模式
    video.write(imm)  #写入
    # time.sleep(5) # 等待5秒再次循环
def on_press(key):   # 监听按键
  global flag
  if key == keyboard.Key.home:
    flag = True # 改变
    return False # 返回False，键盘监听结束！
def video_info():   # 视频信息
  video = VideoCapture('%s.avi' % name)  # 记得文件名加格式不要错！
  fps = video.get(CAP_PROP_FPS)
  Count = video.get(CAP_PROP_FRAME_COUNT)
  size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
  print('帧率=%.1f'%fps)
  print('帧数=%.1f'%Count)
  print('分辨率',size)
  print('视频时间=%.3f秒'%(int(Count)/fps))
  print('录制时间=%.3f秒'%(final_time-start_time))
  print('推荐帧率=%.2f'%(fps*((int(Count)/fps)/(final_time-start_time))))
if __name__ == '__main__':
  flag = False
  th = threading.Thread(target=video_record)
  th.start()
  with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
  time.sleep(1)  # 等待视频释放过后
  video_info()
