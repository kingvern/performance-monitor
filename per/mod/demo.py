#-*- conding;utf-8 -*-

"""
@auther: Mark
@file:demo.py
@time:2018/3/1 13:59
"""
from django.http import HttpResponse, JsonResponse
import pickle

from django.shortcuts import render
from datetime import datetime,timedelta
import models as models


context = {}
end = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
start = end + timedelta(days=-80)
ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")

arrayList = []
symbolNameList=[]
symbolList=[]

for arti in ArtiInfo:
    per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                     arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                     arti.netNotional, arti.netLeverage, arti.netPosDirection)
    arrayList.append(per)
    # print(per.perDe)
    for Symbol in per.perDe:
        if Symbol['contractIndex'] in symbolNameList:
            continue
        else:
            symbolNameList.append(Symbol['contractIndex'])
        print(Symbol['contractIndex'] in symbolNameList)


for SymbolName in symbolNameList:
    # symbolList[Symbol['contractIndex']].append(Symbol)
    Symbol=[]
    print(SymbolName)
    for per in arrayList:
        for perr in per.perDe:
            if perr['contractIndex'] == SymbolName:
                perr['date']=per.date
                Symbol.append(perr)
    print(sorted(Symbol, key=lambda perContract: perContract["date"]))


# print(symbolNameList)
context['ArtiInfo'] = arrayList
