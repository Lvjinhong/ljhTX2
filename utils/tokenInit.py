#! /usr/bin/env python
# coding=utf-8
import os
import time
import json

import yaml
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
configPath="config.yml"

with open(configPath, 'r', encoding='utf-8') as f:
    config = yaml.full_load(f.read())

# 创建AcsClient实例
client = AcsClient(
    config['Aliyun']['AccessKey ID'],
    config['Aliyun']['AccessKey Secret'],
    "cn-shanghai"
);

def init():
    # 创建request，并设置参数。
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request)
        # print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token 已获取 ")
            print("expireTime = " + str(expireTime))
    except Exception as e:
        print('token获取失败')
        print(e)
    config['Aliyun']['TOKEN']=token
    with open(configPath,'w') as f:
        f.write(yaml.dump(config))
    print('初始化完成，配置文件已同步')
