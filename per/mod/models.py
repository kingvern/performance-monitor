# -*- coding: utf-8 -*-
import pickle

from datetime import datetime, time
from django.db import models

# Create your models here.
from mongoengine import *

connect('StrategyPerformance', port=27017)


class performanceDetail(EmbeddedDocument):
    contractIndex = StringField()
    posYes = IntField()
    posToday = IntField()
    holdPnl = FloatField()
    tradePnl = FloatField()
    totalPnl = FloatField()
    margin = FloatField()
    commission = FloatField()

class huataiPerformance(Document):

    _id = ObjectIdField()
    netValue=FloatField()
    pnl=FloatField()
    pctChg=FloatField()
    date=DateTimeField()
    equity=FloatField()
    performanceDetails=BinaryField()
    initMoney=IntField()
    totalMargin=FloatField()
    marginRatio=FloatField()
    notional=FloatField()
    leverage=FloatField()
    netPosDirection=IntField()
    netNotional=FloatField()
    netLeverage=FloatField()
    performanceDetail = ListField()
    meta = {'collection': 'NetValue_huatai_1000w'}  # 指明连接数据库的哪张表

class xinhuPerformance(Document):

    _id = ObjectIdField()
    netValue=FloatField()
    pnl=FloatField()
    pctChg=FloatField()
    date=DateTimeField()
    equity=FloatField()
    performanceDetails=BinaryField()
    initMoney=IntField()
    totalMargin=FloatField()
    marginRatio=FloatField()
    notional=FloatField()
    leverage=FloatField()
    netPosDirection=IntField()
    netNotional=FloatField()
    netLeverage=FloatField()
    performanceDetail = ListField()
    meta = {'collection': 'NetValue_xinhu_300w'}  # 指明连接数据库的哪张表



class per():
    def __init__(self, netValue,pnl, equity,pctChg,date,perDestr,initMoney,totalMargin,marginRatio,notional,leverage,netNotional,netLeverage,netPosDirection):
        self.netValue = netValue
        self.pnl = pnl
        self.equity = equity
        self.pctChg=pctChg
        self.initMoney=initMoney
        self.totalMargin=totalMargin
        self.marginRatio=marginRatio
        self.notional=notional
        self.leverage=leverage
        self.netNotional=netNotional
        self.netLeverage=netLeverage
        self.netPosDirection=netPosDirection
        self.date = date.strftime("%Y-%m-%d")
        self.perDestr=perDestr

        if self.perDestr is not None:
            perDetails = pickle.loads(self.perDestr)
            self.perDe = sorted(perDetails, key=lambda perContract: perContract["contractIndex"])
    def getDetail(self):
        if self.perDestr is not None:
            perDetails = pickle.loads(self.perDestr)
            perDe = sorted(perDetails, key=lambda perContract: perContract["contractIndex"])
        return [perDe]
    def getRank(self):
        if self.perDestr is not None:
            perDetails = pickle.loads(self.perDestr)
            perDe = sorted(perDetails, key=lambda perContract: perContract["contractIndex"])
            posToday = sorted(perDetails, key=lambda perContract: perContract["posToday"])
            tradePnl = sorted(perDetails, key=lambda perContract: perContract["tradePnl"])
            margin = sorted(perDetails, key=lambda perContract: perContract["margin"])
            commission = sorted(perDetails, key=lambda perContract: perContract["commission"])
            totalPnl = sorted(perDetails, key=lambda perContract: perContract["totalPnl"])
            pp=[perDe,posToday,tradePnl,margin,commission,totalPnl]
        return pp


# for i in performance.objects[10:]:  # 测试是否连接成功
#     print(i.performanceDetails)