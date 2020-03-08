#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

class WxPusher():
    def __init__(self):
        #wxPusher消息发送接口
        self.serverUrl = 'http://wxpusher.zjiecode.com/api/send/message'
        #证券交易提醒的token
        self.appToken = "AT_awCxNJvY4xqWek40uB7xXUvbS8X0hUtk"
        #发送目标的UID，是一个数组！！！(目前仅发送给我一个人)
        self.uids = [ "UID_4KEgQdVFBw7ciEX4u0A9HTmuHoEL" ]


    #发送微信消息提醒
    def sendMessage(self,title,text):
        #编辑发送消息的参数        
        paramaters = {
            "appToken":self.appToken,
            "uids":self.uids,
            #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
            "contentType":3,
            "content":"【"+ title +"】\n\n" + text
    }

        response = requests.post(url=self.serverUrl,json=paramaters)
        result = response.json()
        
        if result['success'] == True :
            print('消息发送成功~~')
        else :
            print('消息发送失败！错误信息：' + result['msg'])
    
class TradeDay():
    #判断当前是否为工作日
    def isHoliday(self,date):
        #节假日接口(工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2 )
        server_url = "http://www.easybots.cn/api/holiday.php?d="
        req = requests.get(server_url + date)
        result = req.json()[date]
        if result == '0':
            return True
        else:
            return False