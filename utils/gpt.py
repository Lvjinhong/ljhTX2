import random

import openai
import yaml

from utils.tts import TTS


class GPT:
    def __init__(self):
        with open("../config.yml", 'r', encoding='utf-8') as f:
            self.config = yaml.full_load(f.read())
        openai.api_key = self.config['OPENAI']['API_KEY']
        openai.organization = self.config['OPENAI']['ORG']
        # os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33210'
        # os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33210'
        self.initPrompt= self.config['OPENAI']['INIT_PROMPT']
        self.tts=TTS()
        self.msg=[{"role": "user", "content": f"{self.initPrompt}"}]
    def createChat(self):
        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.msg
        )
        return ans

    def clearChat(self):
        self.msg=[]
        self.tts.speakNoremove('voice/vChatClear.mp3')

    def chat(self, text):
        self.msg.append({"role": "user", "content": f"{text}"})
        if len(self.msg) > 10:
            self.msg = [{"role": "user", "content": f"{self.initPrompt}"}]
            self.tts.speakNoremove('voice/vmaxClearChat.mp3')
            self.msg.append({"role": "user", "content": f"{text}"})
        ans = self.createChat()
        res = ans['choices'][0]['message']['content']
        print(self.msg)
        self.tts.start(res,str(random.randint(10,99)))
        self.msg.append({"role": "assistant", "content": f"{res}"})
        return res
    def chatNoHistory(self,text):
        self.msg[0]={"role": "user", "content": f"{text}"}
        ans = self.createChat()
        res = ans['choices'][0]['message']['content']
        print(res)
        return res

if __name__ == '__main__':
    rebot = GPT()
    rebot.msg=[]
    rebot.chat('天行健，君子以自强不息这句话出自哪里')







