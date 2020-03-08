#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import datetime
import pytz
from common import DataApi,Helper


#定义时区=东八区
tz = pytz.timezone('Asia/Shanghai')
#获取当前时间
now = datetime.datetime.now(tz)
#格式化日期时间
today = now.strftime('%Y%m%d')
#测试
#today = '20200306'

#仅在工作日执行后续操作
tradeDay = Helper.TradeDay()
if tradeDay.isHoliday(today) == False :
    print('今天不是交易日哟~')
else :
    #获取集思录数据
    jslData = DataApi.JslData()
    qdiiData = jslData.getQdiiData()
    stockLofData = jslData.getStockLofData()
    indexLofData = jslData.getIndexLofData()

    #将三张表合并在一起
    selected = pd.concat([qdiiData,stockLofData,indexLofData],axis=0,join='outer')

    #若有符合条件的基金则发送消息
    if selected.empty == True:
        print('当前没有符合套利条件的基金~')
    else :
        title = '当前可进行套利操作！'
        desp = '基金代码 | 基金名称 | 溢价率 | 场内现价 | 场外估值 ' +'\n\n'
        #编辑消息详情
        for index,fund in selected.iterrows():
            desp = desp + fund['fund_id'] + ' | ' + fund['fund_nm'] + ' | ' + str(fund['discount_rt'])+'% | ' + fund['price'] +' | '+fund['estimate_value'] + '\n\n'
        
        wxPusher = Helper.WxPusher()
        wxPusher.sendMessage(title = title , text = desp)
        #print('消息内容：\n' + text)