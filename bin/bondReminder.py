#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import datetime
import pytz
import json


#判断当前是否为工作日
def isHoliday(date):
    #节假日接口(工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2 )
    server_url = "http://www.easybots.cn/api/holiday.php?d="
    req = requests.get(server_url + date)
    result = req.json()[date]
    if result == '0':
        return True
    else:
        return False


#发送微信消息提醒
def sendMessage(title,text):
    #wxPusher消息发送接口
    severUrl = 'http://wxpusher.zjiecode.com/api/send/message'
    paramaters = {
        #证券交易提醒的token
        "appToken":"AT_awCxNJvY4xqWek40uB7xXUvbS8X0hUtk",
        #发送目标的UID，是一个数组！！！
        "uids":[ "UID_4KEgQdVFBw7ciEX4u0A9HTmuHoEL" ],
        #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
        "contentType":3,
        "content":"【"+ title +"】\n\n" + text
}

    response = requests.post(url=severUrl,json=paramaters)
    result = response.json()
    
    if result['success'] == True :
        print('消息发送成功~~')
    else :
        print('消息发送失败！错误信息：' + result['msg'])

#从集思录获取可转债的数据
def getJslData():
    #集思录网址可转债查询接口（测试中）
    jslUrl = 'https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t'

    try :
        jsl = requests.get(url=jslUrl)
    except :
        sendMessage(title = '发生未知错误！' , text = '访问集思录网站获取数据失败，请检查代码接口！')
        raise

    data = jsl.json()

    #将json数据转换成列表
    list = []
    for row in data['rows']:
        list.append(row['cell'])

    #创建DataFrame
    stocks = pd.DataFrame(data=list)

    #stocks = stocks.set_index('fund_id')
    #截取需要用到的字段
    stocks = stocks.loc[:,['apply_date','apply_cd','bond_nm','stock_nm','cb_type','rating_cd']]

    return stocks

#定义时区=东八区
tz = pytz.timezone('Asia/Shanghai')

#获取当前时间
now = datetime.datetime.now(tz)

#格式化日期时间
today = now.strftime('%Y%m%d')

#测试
#today = '20200228'

#仅在工作日执行后续操作
if isHoliday(today) == False :
    print('今天不是交易日哟~')
else :
    #获取集思录数据
    stocks = getJslData()

    #选取出溢价率大于2%且开放申赎且有新增场内份额的基金
    today2 = now.strftime('%Y-%m-%d')
    #today2 = '2020-02-28'
    selected = stocks[stocks['apply_date']==today2]

    #若有符合条件的基金则发送消息
    if selected.empty == False:
        title = '今日有可申购的可转债！'
        desp = '申购代码 | 可转债名称 | 正股名称 | 类型 | 评级 \n\n'
        #编辑消息详情
        for index,bond in selected.iterrows():
            desp = desp + bond['apply_cd'] + ' | ' + bond['bond_nm'] + ' | ' + bond['stock_nm']+' | ' + bond['cb_type'] +' | '+bond['rating_cd'] + '\n\n'

        sendMessage(title = title , text = desp)
        #print('消息内容：\n' + desp)