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
    out_music.export(out_f="./Lemon_Tree01.mp3", format='mp3')   # 可以指定bitrate为64k比特率 None为源文件

    print('done')
    pass
'''
@Time    : 2020/2/12 14:48
@FileName: joinVoice.py
@Author  : Yoakam
@Email   : yuwang@nilfisk.com
'''

def joinVoice():
    file1_name = r"../data/sound1.mp3"
    file2_name = r"../data/sound2.mp3"
    # 加载需要拼接的两个文件
    sound1 = AudioSegment.from_mp3(file1_name)
    sound2 = AudioSegment.from_mp3(file2_name)
    # 取得两个文件的声音分贝
    db1 = sound1.dBFS
    db2 = sound2.dBFS
    dbplus = db1 - db2
    # 声音大小
    if dbplus < 0:
        sound1 += abs(dbplus)
    else:
        sound2 += abs(dbplus)
    # 拼接两个音频文件
    finSound = sound1 + sound2
    save_name = r"../data/" + "finSound" + file1_name[-4:]
    print("save_path:", save_name)

    finSound.export(save_name, format="mp3", tags={'artist': 'AppLeU0', 'album': save_name[:-4]})
    return True


if __name__ == '__main__':
    src_path = r'./Lemon_Tree.mp3'   # seconds: 30 -> 3'49(229)
    cut_mp3(filepath=src_path)

