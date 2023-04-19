import os
from time import sleep

import speech_recognition as sr
import yaml
import pickle as pk
import  re
from utils.gpt import GPT
from utils.tts import TTS
from utils.navigation import Navigation
import json
from utils import tokenInit as tI
# tI.init()

# with open('str.pkl','wb') as f:
#     pk.dump(str,f)
# with open("str.pkl", "rb") as f:
#     q = pk.load(f)
# with open("config.yml",'r',encoding='utf-8') as f:
#     config = yaml.full_load(f.read())
# print(q)

# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33210'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33210'
rebot = GPT()
tts = TTS()
def audioDeal(r):
    with sr.Microphone() as source:
        print("语音输入中")
        tts.speakNoremove('voice/startRec.mp3')
        audio = r.listen(source)
    try:
        print('语音识别中')
        # text = r.recognize_google(audio, language="zh-CN")
        text = r.recognize_whisper(audio, language="chinese")
        return text
    except sr.UnknownValueError:
        print("音源识别错误")
    except sr.RequestError as e:
        print("网络连接错误")
def myChat(r):
    while True:
        text=audioDeal(r)
        if not text or len(text) < 3:
            sleep(1)
            continue
        #清除对话
        sleep(1)
        print(text)
        if re.search('退出聊天模式',text):
            tts.speakNoremove('voice/vexitChat.mp3')
            print('已退出聊天模式')
            break
        if re.search('清空对话',text):
            rebot.clearChat()
            print('清除对话')
        rebot.chat(text)
def navigation(r):
    tts.speakNoremove('voice/vnavigationMode.mp3')
    nav = Navigation()
    sleep(0.5)
    tts.speakNoremove('voice/vNav_getPosName.mp3')
    posName=audioDeal(r)
    nav.getTarloc(posName)
    select=audioDeal(r)
    nav.dealInput(select)
if __name__ == '__main__':
    r = sr.Recognizer()
    myChat(r)
    # tts.speak('voice/vnav.mp3')
    # tts.start('请问您想前往哪些地点呢，说出关键词就可以哦！','Nav_getPosName')
    # r = sr.Recognizer()
    # navigation(r)
    # userText = ''
    # # while True:
    # myChat(r)

