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

    #获取haoETF原油数据
    haoEtfData = DataApi.HaoEtfData()
    oilLofData = haoEtfData.getOilFundData()

    #若有符合条件的基金则发送消息
    if selected.empty == True & oilLofData.empty == True:
        print('当前没有符合套利条件的基金~')
    else :        
        #编辑集思录消息详情
        #jsl_desp = ''
        if selected.empty == False:
            jsl_desp = '基金代码 | 基金名称 | 溢价率 | 场内现价 | 场外估值 ' +'\n\n'
            for index,fund in selected.iterrows():
                jsl_desp = jsl_desp + fund['fund_id'] + ' | ' + fund['fund_nm'] + ' | ' + str(fund['discount_rt'])+'% | ' + fund['price'] +' | '+fund['estimate_value'] + '\n\n'
            
            jsl_desp = jsl_desp + '数据来源：[集思录]('+ jslData.url +') \n\n'

        #编辑haoETF原油基金估值详情
        #oil_desp = ''
        if oilLofData.empty == False :
            oil_desp = '基金代码 | 基金名称 | 溢价率 | 场内现价 | T-1估值 ' +'\n\n'
            for index,oil in oilLofData.iterrows():
                oil_desp = oil_desp + oil['代码'] + ' | ' + oil['名称'] + ' | ' + str(oil['实时溢价'])+'% | ' + oil['现价'] +' | '+oil['T-1估值'] + '\n\n'
            
            oil_desp = oil_desp + '数据来源：[HaoETF]('+ haoEtfData.url +') \n\n'

        #发送消息通知
        title = '当前可进行套利操作！'
        #判断变量是否存在
        jsl_desp_exist = 'jsl_desp' in locals() or 'jsl_desp' in globals()
        oil_desp_exist = 'oil_desp' in locals() or 'oil_desp' in globals()

        if jsl_desp_exist == False:
            text = oil_desp
        if oil_desp_exist == False :
            text = jsl_desp
        if jsl_desp_exist == True & oil_desp_exist == True:
            text = jsl_desp + oil_desp

        wxPusher = Helper.WxPusher()
        wxPusher.sendMessage(title = title , text = text)
        #print('消息内容：\n' + text)