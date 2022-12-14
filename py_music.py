from pydub import AudioSegment


def cut_mp3(filepath):
    """
    # 程序流程
    1. 读取一个mp3文件,指定文件路径即可
    2. 根据用户选择设置截取片段，使用切片, 单位为ms
    3. 导出文件并保存, 指定导出文件名以及路径，最后指定导出的格式
    （其他编码格式，参考ffmpeg上的专业知识）

    :param filepath: 音乐文件路径, path
    :return: None
    """
    music = AudioSegment.from_mp3(file=filepath)
    sound_time = music.duration_seconds
    print(f"music duration time: {sound_time}")

    # 使用切片截取, 单位毫秒， 1s -> 1000ms
    out_music = music[30000: 229000]

    # 导出
    out_music.export(out_f="./蜗牛-周杰伦.mp3", format='mp3')   # 可以指定bitrate为64k比特率 None为源文件

    print('done')
    pass


if __name__ == '__main__':
    src_path = r'./周杰伦-蜗牛_need_cut.mp3'   # seconds: 30 -> 3'49(229)
    cut_mp3(filepath=src_path)

