# -*- coding: utf-8 -*-
from django.http import HttpResponse
import pickle

from django.shortcuts import render
from datetime import  datetime
import per.mod.models as models

def day(request):
    processDateT = datetime.strptime('20171015', '%Y%m%d')
    ArtiInfo = models.performance.objects(date__gte=processDateT)
    arrayList = []
    for arti in ArtiInfo:
        per=models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,arti.initMoney,arti.totalMargin,arti.marginRatio,arti.notional,arti.leverage,arti.netNotional,arti.netLeverage,arti.netPosDirection)
        arrayList.append(per)
    context = {}
    context['ArtiInfo'] = arrayList
    # return render(request, 'per.html', context)
    return render(request, 'day.html', context)

def index(request):
    processDateT = datetime.strptime('20171015', '%Y%m%d')
    ArtiInfo = models.performance.objects(date__gte=processDateT)
    arrayList = []
    for arti in ArtiInfo:
        per=models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,arti.initMoney,arti.totalMargin,arti.marginRatio,arti.notional,arti.leverage,arti.netNotional,arti.netLeverage,arti.netPosDirection)
        arrayList.append(per)
    context = {}
    context['ArtiInfo'] = arrayList
    # return render(request, 'per.html', context)
    return render(request, 'index.html', context)

def cycle(request):
    processDateT = datetime.strptime('20171015', '%Y%m%d')
    ArtiInfo = models.performance.objects(date__gte=processDateT)
    arrayList = []
    for arti in ArtiInfo:
        per=models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,arti.initMoney,arti.totalMargin,arti.marginRatio,arti.notional,arti.leverage,arti.netNotional,arti.netLeverage,arti.netPosDirection)
        arrayList.append(per)
    context = {}
    context['ArtiInfo'] = arrayList
    # return render(request, 'per.html', context)
    return render(request, 'cycle.html', context)
