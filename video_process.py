from moviepy.editor import VideoFileClip, clips_array

clip1 = VideoFileClip('D:\Files\PDF\english\EF\MOB_11.2.3.1.1.mp4')  # 读入视频
clip2 = VideoFileClip('D:\Files\PDF\english\EF\MOB_11.2.4.1.1.mp4')
clip1 = clip1.subclip(0, 55)
clip2 = clip2.subclip(0, 55)
# final_clip = clips_array([[clip1],[clip2]])#上下拼接
final_clip = clips_array([[clip1, clip2]])  # 左右拼接

final_clip.write_videofile('c.mp4')  # 保存视频
