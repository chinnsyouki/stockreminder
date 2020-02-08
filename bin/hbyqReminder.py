#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd

#发送微信消息提醒
def sendMessage(text,desp):
    #server酱消息发送接口
    severUrl = 'https://sc.ftqq.com/SCU80469T3f7f6cd2cc99acb1eace952a841df5835e3da00e0cc93.send'
    paramaters = {'text':text,'desp':desp}

    response = requests.get(url=severUrl,params=paramaters)
    result = response.json()
    
    if result['errno'] == 0 :
        print('消息发送成功~~')
    else :
        print('消息发送失败！错误信息：' + result['errmsg'])



#集思录网址QDII基金查询接口（测试中）
jslUrl = 'https://www.jisilu.cn/data/qdii/qdii_list/?___jsl=LST___t'

jsl = requests.get(url=jslUrl)

data = jsl.json()

#格式化获取到的数据
qdiiInfo = pd.DataFrame(data['rows'])

#查找华宝油气（代码=162411）
hbyq = qdiiInfo[qdiiInfo['id']=='162411']

info = hbyq['cell'][1]

if abs(float(info['discount_rt'][:-1])) > 2 :
    text = '当前可进行套利操作！'
    desp = '华宝油气溢价率：' + info['discount_rt'] + '\n\n' + info['price_dt'] + ' | 场内现价：' + info['price'] + '(' + info['increase_rt'] + ')' + '\n\n' + info['nav_dt'] + ' | 场外净值：' + info['fund_nav'] + '\n\n'  + info['est_val_dt'] + ' | 场外估值：' + info['estimate_value'] + '(' + info['est_val_increase_rt'] + ')'
    sendMessage(text = text , desp = desp)