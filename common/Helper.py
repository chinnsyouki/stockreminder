#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from random import randint

class WxPusher():
    def __init__(self):
        #wxPusher消息发送接口
        self.serverUrl = 'http://wxpusher.zjiecode.com/api/send/message'
        #证券交易提醒的token
        self.appToken = "AT_awCxNJvY4xqWek40uB7xXUvbS8X0hUtk"
        #发送目标的UID，是一个数组！！！(目前仅发送给关注我的人)
        self.uids = [ "UID_4KEgQdVFBw7ciEX4u0A9HTmuHoEL","UID_2gaVeBmrkw9zeqSi4ouZdKWBgi2B" ]


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
    def isWorkday(self,date):
        #常用的浏览器headers
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
            ]
        #随机获取headers
        random_agent = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
        headers = {'User-Agent':random_agent}

        #节假日接口(工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2 )
        server_url = "http://timor.tech/api/holiday/info/" + date
        req = requests.get(url = server_url,headers = headers)
        result = req.json()

        #"type": enum(0, 1, 2, 3), // 节假日类型，分别表示 工作日、周末、节日、调休。
        if result['type']['type'] == 0:
            return True
        else:
            return False