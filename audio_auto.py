from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from pydub.silence import detect_silence
from aip import AipSpeech
import os
import time
import re
import requests
import js2py


class baidu_Translate():
    def __init__(self):
        self.js = js2py.eval_js('''
            var i = null;

            function n(r, o) {
                for (var t = 0; t < o.length - 2; t += 3) {
                    var a = o.charAt(t + 2);
                    a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                    a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
                    r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
                }
                return r
            }
            var hash = function e(r,gtk) {
                var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
                if (null === o) {
                    var t = r.length;
                    t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr( - 10, 10))
                } else {
                    for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)"" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                    C !== h - 1 && f.push(o[C]);
                    var g = f.length;
                    g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice( - 10).join(""))
                }
                var u = void 0,
                u = null !== i ? i: (i = gtk || "") || "";
                for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                    var A = r.charCodeAt(v);
                    128 > A ? S[c++] = A: (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
                }

                for (
                var p = m,F = "+-a^+6", D = "+-3^+b+-f", b = 0;
                b < S.length; b++) p += S[b],p = n(p, F);

                return p = n(p, D),
                p ^= s,
                0 > p && (p = (2147483647 & p) + 2147483648),
                p %= 1e6,
                p.toString() + "." + (p ^ m)
            }
        ''')
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36', }
        self.session = requests.Session()
        self.session.get('https://fanyi.baidu.com', headers=headers)
        response = self.session.get('https://fanyi.baidu.com', headers=headers)
        self.token = re.findall("token: '(.*?)',", response.text)[0]
        self.gtk = '320305.131321201'  # re.findall("window.gtk = '(.*?)';", response.text, re.S)[0]

    def translate(self, query, from_lang='en', to_lang='zh'):
        # langdetect
        self.session.post('https://fanyi.baidu.com/langdetect', data={'query': query})
        # clickEvent
        self.session.get('https://click.fanyi.baidu.com/?src=1&locate=zh&action=query&type=1&page=1')
        # translate
        data = {
            'from': from_lang,
            'to': to_lang,
            'query': query,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': self.js(query, self.gtk),
            'token': self.token
        }
        response = self.session.post('https://fanyi.baidu.com/v2transapi', data=data)
        json = response.json()
        if 'error' in json:
            pass
            # return 'error: {}'.format(json['error'])
        else:
            return response.json()['trans_result']['data'][0]['dst']


class baidu_SpeechRecognition():
    def __init__(self, dev_pid):
        # ??????????????????API
        Speech_APP_ID = '?????????'
        Speech_API_KEY = '?????????'
        Speech_SECRET_KEY = '?????????'
        self.dev_pid = dev_pid
        self.SpeechClient = AipSpeech(Speech_APP_ID, Speech_API_KEY, Speech_SECRET_KEY)
        self.TranslClient = baidu_Translate()

    def load_audio(self, audio_file):
        self.source = AudioSegment.from_wav(audio_file)

    def speech_recognition(self, offset, duration, fanyi):
        data = self.source[offset * 1000:duration * 1000].raw_data
        result = self.SpeechClient.asr(data, 'wav', 16000, {'dev_pid': self.dev_pid, })
        fanyi_text = ''
        if fanyi:
            try:
                fanyi_text = self.TranslClient.translate(result['result'][0])
            except:
                pass
        try:
            return [result['result'][0], fanyi_text]
        except:
            # print('??????:',result)
            return ['', '']


def cut_point(path, dbfs=1.25):
    sound = AudioSegment.from_file(path, format="wav")
    tstamp_list = detect_silence(sound, 600, sound.dBFS * dbfs, 1)

    timelist = []
    for i in range(len(tstamp_list)):
        if i == 0:
            back = 0
        else:
            back = tstamp_list[i - 1][1] / 1000
        timelist.append([back, tstamp_list[i][1] / 1000])

    min_len = 0.5
    max_len = 5
    result = []
    add = 0
    total = len(timelist)
    for x in range(total):
        if x + add < total:
            into, out = timelist[x + add]
            if out - into > min_len and out - into < max_len and x + add + 1 < total:
                add += 1
                out = timelist[x + add][1]
                result.append([into, out])
            elif out - into > max_len:
                result.append([into, out])
        else:
            break

    return result


def cut_text(text, length=38):
    newtext = ''
    if len(text) > length:
        while True:
            cutA = text[:length]
            cutB = text[length:]
            newtext += cutA + '\n'
            if len(cutB) < 4:
                newtext = cutA + cutB
                break
            elif len(cutB) > length:
                text = cutB
            else:
                newtext += cutB
                break
        return newtext
    return text


def progressbar(total, temp, text='&&', lenght=40):
    content = '\r' + text.strip().replace('&&', '[{0}{1}]{2}%')
    percentage = round(temp / total * 100, 2)
    a = round(temp / total * lenght)
    b = lenght - a
    print(content.format('???' * a, '???' * b, percentage), end='')


def format_time(seconds):
    sec = int(seconds)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    fm = int(str(round(seconds, 3)).split('.')[-1])
    return "%02d:%02d:%02d,%03d" % (h, m, s, fm)


def separate_audio(file_path, save_path):
    audio_file = save_path + '\\tmp.wav'
    audio = AudioFileClip(file_path)
    audio.write_audiofile(audio_file, ffmpeg_params=['-ar', '16000', '-ac', '1'], logger=None)
    return audio_file


def file_filter(path, alldir=False):
    key = ['mp4', 'mov']
    if alldir:
        dic_list = os.walk(path)
    else:
        dic_list = os.listdir(path)
    find_list = []
    for i in dic_list:
        if os.path.isdir(i[0]):
            header = i[0]
            file = i[2]
            for f in file:
                for k in key:
                    if f.rfind(k) != -1:
                        find_list.append([header, f])
        else:
            for k in key:
                if i.rfind(k) != -1:
                    find_list.append([path, i])
    if find_list:
        find_list.sort(key=lambda txt: re.findall(r'\d+', txt[1])[0])
    return find_list


def countTime(s_time, now=True):
    if now: s_time = (time.time() - s_time)
    m, s = divmod(int(s_time), 60)
    return '{}???{}???'.format('%02d' % (m), '%02d' % (s))


def __line__print__(txt='-' * 10):
    print('\n' + '-' * 10 + ' ' + txt + ' ' + '-' * 10 + '\n')


if __name__ == '__main__':
    def StartHandle(timeList, save_path, srt_mode=2, result_print=False):
        index = 0
        total = len(timeList)
        a_font = r'{\fn????????????\fs14}'
        b_font = r'{\fn????????????\fs10}'
        fanyi = False if srt_mode == 1 else True
        file_write = open(save_path, 'a', encoding='utf-8')

        for x in range(total):
            into, out = timelist[x]
            timeStamp = format_time(into - 0.2) + ' --> ' + format_time(out - 0.2)
            result = baidufanyi.speech_recognition(into + 0.1, out - 0.1, fanyi)

            if result_print:
                if srt_mode == 0:
                    print(timeStamp, result[0])
                else:
                    print(timeStamp, result)
            else:
                progressbar(total, x, '?????????...&& - {0}/{1}'.format('%03d' % (total), '%03d' % (x)), 44)

            if len(result[0]) > 1:
                index += 1
                text = str(index) + '\n' + timeStamp + '\n'
                if srt_mode == 0:  # ?????????
                    text += a_font + cut_text(result[1])
                elif srt_mode == 1:  # ?????????
                    text += b_font + cut_text(result[0])
                else:  # ??????+??????
                    text += a_font + cut_text(result[1]) + '\n' + b_font + result[0]

                text = text.replace('\u200b', '') + '\n\n'
                file_write.write(text)

        file_write.close()
        if not result_print:
            progressbar(total, total, '?????????...&& - {0}/{1}'.format('%03d' % (total), '%03d' % (total)), 44)


    os.system('cls')
    wav_path = os.environ.get('TEMP')

    # ????????????
    pid_list = 1536, 1537, 1737, 1637, 1837, 1936

    # ????????????
    print('[ ????????????????????????????????? - by Teri ]\n')
    __line__print__('1 ????????????')
    input_dev_pid = input('?????????????????????:\n'
                          '\n  (1)?????????,'
                          '\n  (2)?????????+????????????,'
                          '\n  (3)??????,'
                          '\n  (4)??????,'
                          '\n  (5)?????????,'
                          '\n  (6)?????????-??????'
                          '\n\n?????????????????????(??????3):')

    __line__print__('2 ????????????')
    input_srt_mode = input('?????????????????????:\n'
                           '\n  (1)??????,'
                           '\n  (2)??????,'
                           '\n  (3)??????+?????????'
                           '\n\n?????????????????????(??????3):')

    __line__print__('3 ????????????')
    input_print = input('?????????????????????????????????? (??????:???/y:??????):').upper()

    # ????????????
    dev_pid = int(input_dev_pid) - 1 if input_dev_pid else 3
    dev_pid -= 1
    srt_mode = int(input_srt_mode) if input_srt_mode else 3
    srt_mode -= 1
    re_print = True if input_print == 'Y' else False

    # ????????????
    __line__print__('4 ????????????')
    input_file = input('?????????????????????????????????????????????:').strip('"')
    video_file = []
    if not os.path.isdir(input_file):
        video_file = [input_file]
    else:
        file_list = file_filter(input_file)
        for a, b in file_list:
            video_file.append(a + '\\' + b)

    # ????????????
    select_dev = ['?????????', '?????????+????????????', '??????', '??????', '?????????', '?????????-??????']
    select_mode = ['??????', '??????', '??????+??????']
    __line__print__('5 ????????????')
    input('???????????????:\n????????????: {0}, ????????????: {1}, ????????????: {2}\n????????????????????? {3} ???\n???????????????????????????...'.format(
        select_dev[dev_pid],
        select_mode[srt_mode],
        '???' if re_print else '???',
        len(video_file)
    ))

    # ????????????
    total_file = len(video_file)
    total_time = time.time()
    baidufanyi = baidu_SpeechRecognition(pid_list[dev_pid])
    for i in range(total_file):
        item_time = time.time()
        file_name = video_file[i].split('\\')[-1]
        print('\n>>>>>>>> ...??????????????????... <<<<<<<<', end='')
        audio_file = separate_audio(video_file[i], wav_path)
        timelist = cut_point(audio_file, dbfs=1.15)
        if timelist:
            print('\r>>>>>>>> ??????:{} ??????:{} <<<<<<<<'.format(
                '%03d' % (i),
                countTime(len(timelist) * 5, now=False)
            ))
            srt_name = video_file[i][:video_file[i].rfind('.')] + '.srt'
            baidufanyi.load_audio(audio_file)
            StartHandle(timelist, srt_name, srt_mode, re_print)
            print('\n{} ????????????, ????????????{}'.format(file_name, countTime(item_time)))
        else:
            print('??????????????????')

    # ????????????
    input('????????????, ?????????{}?????????, ????????????{}'.format(total_file, countTime(total_time)))



"""
import requests
import json
import base64
import os
import logging
import speech_recognition as sr
import wx
import threading
#?????????

def get_token():  # ???????????????????????????API?????????????????????????????????
    logging.info('Retrieving token...') #???print?????????
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    client_id = "EUON57v2pcpk5CDQnet6AN6s" #??????ID
    client_secret = "oHb0INPt5MGSC4LfoQ9hd7W2oSR6GLmV" #??????
    url = f"{baidu_server}grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    res = requests.post(url)
    token = json.loads(res.text)["access_token"] #???json??????????????????
    return token


def audio_baidu(filename):  # ??????????????????????????????????????????????????????????????????
    if not os.path.exists('record'):
        os.makedirs('record') #????????????
    filename = 'record/' + filename
    logging.info('Analysing audio file...')
    with open(filename, "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf-8')
    size = os.path.getsize(filename)
    token = get_token()
    headers = {'Content-Type': 'application/json'}
    url = "https://vop.baidu.com/server_api"
    data = {
        "format": "wav",
        "rate": "16000",
        "dev_pid": 1737,  #???????????????1737=english, 17372=enhanced english, 15372=enhanced chinese, ??????????????????????????????
        "speech": speech,
        "cuid": "3.141592653589793238462643383279502884197169399375105820", #??????????????????
        "len": size,
        "channel": 1,
        "token": token,
    }

    req = requests.post(url, json.dumps(data), headers)
    result = json.loads(req.text)

    if result["err_msg"] == "success.":
        message = ''.join(result['result'])
        print('RETURNED: ' + message)
        return result['result']
    else:
        print("RETURNED: Recognition failure")
        return -1


def main():  # ??????2: ????????????
    logging.basicConfig(level=logging.INFO)

    wav_num = 0
    while True:
        r = sr.Recognizer() #???????????????
        mic = sr.Microphone() #?????????????????????
        logging.info('Recording...')
        with mic as source:
            r.adjust_for_ambient_noise(source) #??????????????????
            audio = r.listen(source, timeout=1000) #?????????1000ms??????
        with open('record/' + f"00{wav_num}.wav", "wb") as f:
            f.write(audio.get_wav_data(convert_rate=16000)) #?????????
        message = ''.join(audio_baidu(f"00{wav_num}.wav"))
        history = open('record/' + f"history.txt", "a")
        history.write(message + '\n')
        history.close()

        wav_num += 1


def update_content(win, height=200, width=800): #??????????????????????????????
    f = open('record/' + f"history.txt", "r") #????????????
    try:
        last_line = f.readlines()[-1] #?????????????????????
    except IndexError:
        last_line = ''
    if last_line.strip('\n') in ['key point']:  #???????????????????????????????????????
        logging.info('Emphasized')
        ft = wx.Font(80, wx.MODERN, wx.NORMAL, wx.BOLD, False, '') #????????????
    else:
        ft = wx.Font(50, wx.MODERN, wx.NORMAL, wx.NORMAL, False, '')
    richText = wx.TextCtrl(win, value='', pos=(0, 0), size=(width, height))
    richText.SetInsertionPoint(0) #?????????????????????????????????????????????
    richText.SetFont(ft)
    richText.SetValue(last_line)
    f.close()
    return last_line


def show_win(x=320, y=550, height=200, width=800):  #??????????????????
    win = wx.Frame(None, title="TRAS v1.0.0", pos=(x, y), size=(width, height), style=wx.STAY_ON_TOP) #??????Frame??????
    win.SetTransparent(1000) #?????????
    win.Show()

    return win


#?????????
if __name__ == "__main__":
    history = open('record/' + f"history.txt", "w+")
    history.close()

    thread = threading.Thread(target=main) #???????????????thread???????????????
    thread.start()

    global app #???????????????????????????????????????
    app = wx.App() #????????????
    while True:
        win = show_win() #??????????????????
        v = update_content(win) #??????????????????
        wx.CallLater(2000, win.Destroy) #?????????????????????????????????
        app.MainLoop()

"""