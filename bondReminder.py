#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import datetime
import pytz
from common import Helper,DataApi


#定义时区=东八区
tz = pytz.timezone('Asia/Shanghai')
#获取当前时间
now = datetime.datetime.now(tz)
#格式化日期时间
today = now.strftime('%Y-%m-%d')

#测试
#today = '20200228'

#仅在工作日执行后续操作
tradeDay = Helper.TradeDay()
if tradeDay.isWorkday(today) == False :
    print('今天不是交易日哟~')
else :
    #获取集思录数据
    jslData = DataApi.JslData()
    stocks = jslData.getBondData()

    selected = stocks[stocks['apply_date']==today]

    #若有符合条件的基金则发送消息
    if selected.empty == True:
        print('今天没有可申购的可转债~')
    else :
        title = '今日有可申购的可转债！'
        desp = '申购代码 | 可转债名称 | 正股名称 | 类型 | 评级 \n\n'
        #编辑消息详情
        for index,bond in selected.iterrows():
            desp = desp + bond['apply_cd'] + ' | ' + bond['bond_nm'] + ' | ' + bond['stock_nm']+' | ' + bond['cb_type'] +' | '+bond['rating_cd'] + '\n\n'

        wxPusher = Helper.WxPusher()
        wxPusher.sendMessage(title = title , text = desp)
        #print('消息内容：\n' + desp)