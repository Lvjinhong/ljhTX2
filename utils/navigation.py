import json

import requests as rq
import yaml

from utils.tts import TTS
from utils.gpt import GPT



class Navigation:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        with open("./config.yml", 'r', encoding='utf-8') as f:
            self.ak = yaml.full_load(f.read())['BAIDU']['AK']
        self.tts = TTS()
        self.gpt = GPT()

    def get_public_ip(self):
        url = 'https://api.ipify.org?format=json'
        response = rq.get(url)
        ip_data = response.json()
        return ip_data['ip']

    # 请求，定位服务
    def getLoc(self):
        ip = nav.get_public_ip()
        url = f"https://api.map.baidu.com/location/ip?ak={self.ak}&ip={ip}&coor=bd09ll"
        res = rq.get(url, headers=self.header)
        self.loc = json.loads(res.content)
        return self.loc

    def getTarloc(self,posName):
        #这里城市 需要根据定位获取，如果是ip定位，根据响应，应该是content address_detail city
        url = f'https://api.map.baidu.com/place/v2/suggestion?query={posName}&region=太原&city_limit=true&output=json&ak={self.ak}'
        response = rq.get(url, headers=self.header)
        prompt = json.loads(response.content)
        self.results=prompt['result']
        if prompt['status']:
            print('查询失败，请稍后重试')
            self.tts.speakNoremove('./voice/vNav_getTarLocError.mp3')
            return
        names='! '.join([str(i+1)+' '+self.results[i]['name'] for i in range(len(self.results))])
        self.tts.start('好的，为您查询到以下地点，'+names+'，您想去第几个呢？','nav')
        return

    def dealInput(self,select):
        sel = self.gpt.chat(f"根据下面的输入，将输入语句的含义转为意思最为相近的一个下标数字，并输出这个数字。输入：{select}")
        # index=int(re.findall(r'(\d{1,})',select)[0])-1
        try:
            self.loc2=self.results[int(sel)]

        except Exception as e:
            print(e)
            print('路径导航文件中 dealInput error')


    def getPath(self):
        try:
            start = self.loc['content']['point']
            end = self.loc2['location']
            url = f'https://api.map.baidu.com/directionlite/v1/driving?origin=40.01116,116.339303&destination=39.936404,116.452562&ak={self.ak}'
            path= rq.get(url, headers=self.header)
            print(path)


        except Exception as e:
            print(e)
            print('路径导航文件中 getPath error')



if __name__ == '__main__':
    nav = Navigation()
    nav.getTarloc('医院')
