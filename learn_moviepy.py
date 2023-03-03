from moviepy.editor import *

"""
MoviePy可以实现视频的剪辑、提取音频等强大的功能。
"""


def get_audio_mp4(path_1, base, name):
    video = VideoFileClip(path_1)
    audio = video.audio
    audio_path = os.path.join(base, name + '.mp3')
    print(audio_path)
    audio.write_audiofile(audio_path)


def get_path():
    if len(sys.argv) < 2:
        print("Please try again")
        sys.exit()
    path = sys.argv[1]
    rel_path = os.path.split(path)
    basepath = rel_path[0]
    filename = rel_path[1]
    exe_name = os.path.splitext(filename)
    rel_filename = exe_name[0]
    return path, basepath, rel_filename


if __name__ == "__main__":
    mp4_path, base_path, file_name = get_path()
    get_audio_mp4(mp4_path, base_path, file_name)

    # print(mp4_path)
    # print(base_path)
    # print(file_name)
    # get_audio_mp4()
# video = VideoFileClip("./movie/lake.mp4").subclip(50, 60)
# audio_path = "./movie/audio.mp3"
# print(video.size)
# print(video.duration)
# # Make the text. Many more options are available.
# txt_clip = (TextClip("YJ Holidays 2013", fontsize=70, color='white')
#             .set_position('center')
#             .set_duration(10))
# audio = video.audio
# result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
# result.write_videofile("./movie/myHolidays_edited.mp4", fps=40)
# audio.write_audiofile(audio_path)

"""
另一个强大的工具spleeter可以实现人声与伴奏的分离。
安装spleeter: pip install spleeter
运行 Python -m spleeter separate -i E:/movies/1s.mp3 -p spleeter:2stems -o E:/movies/output
1. 如果报错 Error: Missing argument 'FILES...'. 就去掉参数-i
2. 如果报错 AttributeError: module 'tensorflow.tools.docs.doc_controls' has no attribute 'inheritable_header'
就降低tensorflow和keras的版本，运行 pip install -U tensorflow-estimator==2.6.0 pip install --upgrade keras==2.6.0
-m: python的写法，表示指定模块，在此处表示使用spleeter模块
-p: 指定预测模型
-i: 要进行分离的音频数据（建议使用绝对地址，否则可能出现WinErr2）
-o: 分离出的音轨数据wav文件所在文件夹

直接使用官方预测模型。目前spleeter提供三种音轨分离方式，其中：

Vocals (singing voice) / accompaniment separation (2 stems) —两个音轨：背景和人声
Vocals /drums / bass / other separation (4 stems) —四个音轨
Vocals / drums / bass /piano / other separation (5 stems)—五个音轨

"""

# import asyncio
#
# from ffmpeg import FFmpeg
#
#
# async def main():
#     ffmpeg = (
#         FFmpeg()
#         .option("y")
#         .input(
#             "rtsp://example.com/cam",
#             # Specify file options using kwargs
#             rtsp_transport="tcp",
#             rtsp_flags="prefer_tcp",
#         )
#         .output(
#             "output.ts",
#             # Use a dictionary when an option name contains special characters
#             {"codec:v": "copy"},
#             f="mpegts",
#         )
#     )
#
#     @ffmpeg.on("start")
#     def on_start(arguments):
#         print("Arguments:", arguments)
#
#     @ffmpeg.on("stderr")
#     def on_stderr(line):
#         print("stderr:", line)
#
#     @ffmpeg.on("progress")
#     def on_progress(progress):
#         print(progress)
#
#     @ffmpeg.on("progress")
#     def time_to_terminate(progress):
#         # Gracefully terminate when more than 200 frames are processed
#         if progress.frame > 200:
#             ffmpeg.terminate()
#
#     @ffmpeg.on("completed")
#     def on_completed():
#         print("Completed")
#
#     @ffmpeg.on("terminated")
#     def on_terminated():
#         print("Terminated")
#
#     @ffmpeg.on("error")
#     def on_error(code):
#         print("Error:", code)
#
#     await ffmpeg.execute()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
