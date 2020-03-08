#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import common.Helper as Helper


#从集思录获取数据源
class JslData():
    def __init__(self):
        #集思录网址可转债查询接口（测试中）
        self.bondUrl = 'https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t'
        #集思录网址QDII基金查询接口（测试中）
        self.qdiiUrl = 'https://www.jisilu.cn/data/qdii/qdii_list/?___jsl=LST___t'

    #从集思录获取可转债的数据
    def getBondData(self):
        try :
            jsl = requests.get(url=self.bondUrl)
        except :
            wxPusher = Helper.WxPusher()
            wxPusher.sendMessage(title = '发生未知错误！' , text = '访问集思录网站获取数据失败，请检查代码接口！')
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
    

    #从集思录获取QDII基金数据
    def getQdiiData(self):
        try :
            jsl = requests.get(url=self.qdiiUrl)
        except :
            wxPusher = Helper.WxPusher()
            wxPusher.sendMessage(title = '发生未知错误！' , text = '访问集思录网站获取数据失败，请检查代码接口！')
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
        stocks = stocks.loc[:,['fund_id','fund_nm','discount_rt','price','price_dt','fund_nav','nav_dt','estimate_value','est_val_dt','amount_incr','apply_status','apply_fee','redeem_status','redeem_fee','last_est_datetime']]

        #去除百分比%字符
        stocks['discount_rt'] = stocks['discount_rt'].str.replace('%','')
        #将字符串转化为数字格式
        stocks['discount_rt'] = pd.to_numeric(stocks['discount_rt'],errors='ignore')
        stocks['amount_incr'] = pd.to_numeric(stocks['amount_incr'],errors='ignore')

        return stocks