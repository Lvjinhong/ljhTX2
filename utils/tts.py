import os
import random
import time
import threading
import sys
from time import sleep
from playsound import playsound
import nls
import yaml

with open("./config.yml", 'r', encoding='utf-8') as f:
    config = yaml.full_load(f.read())

URL = "wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
TOKEN = config['Aliyun']['TOKEN']  # 参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = config['Aliyun']['APPKEY']  # 获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist


# 以下代码会根据上述TEXT文本反复进行语音合成
class TTS:
    def start(self, text, id=''):
        self.__text = text
        self.__id = id
        self.voiceFilePath = './voice//v' + self.__id + '.mp3'
        self.voiceFile = open(self.voiceFilePath, 'wb')
        # self.__remove = remove
        self.run()

    def on_metainfo(self, message, *args):
        # print("如果start方法中通过ex参数传递enable_subtitle，则会返回对应字幕信息:{}".format(message))
        pass

    def on_error(self, message, *args):
        print("TTS合成出错 {}".format(args))

    def on_close(self, *args):
        try:
            self.voiceFile.close()
        except Exception as e:
            print("关闭音源失败或播放失败", e)

    def on_data(self, data):
        try:
            self.voiceFile.write(data)
        except Exception as e:
            print("音频数据写入失败", e)

    def on_completed(self, message, *args):
        # print("status : {}".format(str(message['header']['status'])))
        print("语音合成完成")

    def run(self):
        tts = nls.NlsSpeechSynthesizer(
            url=URL,
            token=TOKEN,
            appkey=APPKEY,
            on_error=self.on_error,
            on_completed=self.on_completed,
            on_close=self.on_close,
            on_data=self.on_data
        )
        print("语音合成开始")
        tts.start(self.__text, voice="zhimiao_emo", speech_rate=-100, aformat='mp3')  # zhimiao_emo
        self.speak(self.voiceFilePath)
        # self.speakNoremove(self.voiceFilePath)

    def speak(self, path):
        if os.path.exists(path):
            playsound(path, True)
            sleep(0.1)
            os.remove(path)
        else:
            print('未找到音源')
        # speakFlag = 0
        # tim = 0
        # while tim < 100:
        #     if os.path.exists(path):
        #         playsound(path,True)
        #         sleep(0.1)
        #         speakFlag = 1
        #         break
        #     sleep(0.1)
        #     tim += 1
        # if speakFlag:
        #     # print('播放完毕')
        #     os.remove(path)
        # else:
        #     print('未找到音源')

    def speakNoremove(self, path):
        if os.path.exists(path):
            playsound(path, True)
            sleep(0.1)
        else:
            print('未找到音源')


if __name__ == "__main__":
    ts = TTS()
    TEXT = '好的，本次对话已重置'
    ts.start(TEXT, 'ChatClear', 0)
    ts.speakNoremove('../voice/vChatClear.mp3')
