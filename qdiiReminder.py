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
    stocks = jslData.getQdiiData()

    #选取出溢价率大于4%且开放申赎且有新增场内份额的基金
    selected = stocks[(abs(stocks['discount_rt']) >= 4) & (stocks['apply_status'].str.contains('开放')) & (stocks['redeem_status'].str.contains('开放')) & (stocks['amount_incr'] > 0 )]

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