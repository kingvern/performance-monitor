# -*- coding: utf-8 -*-
import json

import numpy as np
import pandas as pd
from django.contrib.sessions import serializers
from django.http import HttpResponse, JsonResponse
import pickle

from django.shortcuts import render
from datetime import datetime, timedelta
import per.mod.models as models
# import models as models


def day(request):
    context = {}

    end = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
    start = end + timedelta(days=-90)
    ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
    if 'd' in request.GET:
        end = datetime.strptime(request.GET['d'], '%Y-%m-%d')
        start = end + timedelta(days=-90)
        context['d'] = request.GET['d']

    if 'q' in request.GET:
        context['q'] = request.GET['q']
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.xinhuPerformance.objects(date__lte=end, date__gte=start).order_by("date")
    arrayList = []
    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList.append(per)
    context['ArtiInfo'] = arrayList
    return render(request, 'day.html', context)

def index_detail(request):
    d = datetime.strptime(request.GET['b'], '%Y-%m-%d')
    ArtiInfo = models.huataiPerformance.objects(date=d)

    if 'q' in request.GET:
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date=d)
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.xinhuPerformance.objects(date=d)

    arrayList = {}
    deList = {}
    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList = {'initMoney': per.initMoney, 'totalMargin': per.totalMargin, 'marginRatio': per.marginRatio,
                     'notional': per.notional, 'leverage': per.leverage, 'netNotional': per.netNotional,
                     'netLeverage': per.netLeverage, 'netPosDirection': per.netPosDirection}
        pp = [arrayList, per.getDetail()]
    pp = json.dumps(pp, cls=DateEncoder)
    perDe = json.loads(pp)

    return JsonResponse(perDe, safe=False)

def day_locate(request):
    d = datetime.strptime(request.GET['b'], '%Y-%m-%d')
    ArtiInfo = models.huataiPerformance.objects(date=d)

    if 'q' in request.GET:
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date=d)
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.xinhuPerformance.objects(date=d)

    arrayList = {}
    deList = {}
    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList = {'initMoney': per.initMoney, 'totalMargin': per.totalMargin, 'marginRatio': per.marginRatio,
                     'notional': per.notional, 'leverage': per.leverage, 'netNotional': per.netNotional,
                     'netLeverage': per.netLeverage, 'netPosDirection': per.netPosDirection}
        perDetails = pickle.loads(arti.performanceDetails)
        pp = [arrayList, per.getRank()]
    pp = json.dumps(pp, cls=DateEncoder)
    perDe = json.loads(pp)

    return JsonResponse(perDe, safe=False)


def cycle_check(request):
    end = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
    start = end + timedelta(days=-90)
    SymbolName = request.GET['sym']
    if 'end' in request.GET:
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d')
    if 'start' in request.GET:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
    else:
        start = end + timedelta(days=-90)
    ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")

    if 'q' in request.GET:
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")

    arrayList = []
    symbolNameList = []

    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList.append(per)

        if per.perDestr is not None:
            for Symbol in per.perDe:
                if Symbol['contractIndex'] in symbolNameList:
                    continue
                else:
                    symbolNameList.append(Symbol['contractIndex'])
    Symbol = []
    for per in arrayList:
        if per.perDestr is not None:
            for perr in per.perDe:
                if perr['contractIndex'] == SymbolName:
                    perr['date'] = per.date
                    Symbol.append(perr)
    Symbol = sorted(Symbol, key=lambda perContract: perContract["date"])
    deList = json.dumps(Symbol, cls=DateEncoder)
    perDe = json.loads(deList)
    return JsonResponse(perDe, safe=False)


def cycle(request):
    context = {}
    statistics = {}
    end = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
    start = end + timedelta(days=-90)
    if 'end' in request.GET:
        context['end'] = request.GET['end']
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d')

    if 'start' in request.GET:
        context['start'] = request.GET['start']
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
    else:
        start = end + timedelta(days=-90)
    ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")

    if 'q' in request.GET:
        context['q'] = request.GET['q']
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
            account = 'huatai'
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
            account = 'xinhu'
    else:
        account = 'huatai'

    arrayList = []
    symbolNameList = []
    SymbolList = []
    pnl = []

    i = 0
    pnl_total = 0

    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList.append(per)

        # 统计部分
        pnl.append(per.pnl)
        i += 1
        pnl_total += per.pnl

        if per.perDestr is not None:
            for Symbol in per.perDe:
                if Symbol['contractIndex'] in symbolNameList:
                    continue
                else:
                    symbolNameList.append(Symbol['contractIndex'])
                # print(Symbol['contractIndex'] in symbolNameList)

    for SymbolName in symbolNameList:
        # symbolList[Symbol['contractIndex']].append(Symbol)
        Symbol = []
        # print(SymbolName)
        for per in arrayList:
            if per.perDestr is not None:
                for perr in per.perDe:
                    if perr['contractIndex'] == SymbolName:
                        perr['date'] = per.date
                        Symbol.append(perr)
        Symbol = sorted(Symbol, key=lambda perContract: perContract["date"])
        SymbolList.append(Symbol)

    statistics['pnl_total'] = pnl_total
    statistics['pnl_ave'] = pnl_total / i
    statistics['sharp_ratio'] = getSharpeRadio(pnl)

    context['start'] = start
    context['end'] = end
    context['account'] = account
    context['ArtiInfo'] = arrayList
    context['SymbolList'] = SymbolList
    context['symbolNameList'] = symbolNameList
    context['statistics'] = statistics

    return render(request, 'cycle.html', context)


def index(request):
    context = {}
    end = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
    start = end + timedelta(days=-90)
    ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
    if 'd' in request.GET:
        end = datetime.strptime(request.GET['d'], '%Y-%m-%d')
        start = end + timedelta(days=-90)
        context['d'] = request.GET['d']

    if 'q' in request.GET:
        context['q'] = request.GET['q']
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date__lte=end, date__gte=start).order_by("date")
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.xinhuPerformance.objects(date__lte=end, date__gte=start).order_by("date")
    arrayList = []
    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList.append(per)
    context['ArtiInfo'] = arrayList

    return render(request, 'index.html', context)


def ajax_detail(request):
    processDateT = datetime.strptime(request.GET['d'], '%Y-%m-%d')
    if 'q' in request.GET:
        if request.GET['q'] == 'huatai':
            per = models.huataiPerformance.objects(date=processDateT)
        if request.GET['q'] == 'xinhu':
            per = models.xinhuPerformance.objects(date=processDateT)
    # for pe in per:
    #     if pe.performanceDetails is not None:
    #         detail= pickle.loads(pe.performanceDetails)
    # de={}
    # de['detail']=detail

    for arti in per:
        perr = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                          arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                          arti.netNotional, arti.netLeverage, arti.netPosDirection)
        detail = pickle.loads(arti.performanceDetails)
    de = {}
    de['perr'] = perr
    de['detail'] = detail
    return HttpResponse(de)


def demo(request):
    context = {}
    return render(request, 'demo.html', context)


def test(request):
    context = {}
    return render(request, 'test.html', context)


def add(request):
    q = request.GET['a']
    b = request.GET['b']
    d = datetime.strptime(request.GET['b'], '%Y-%m-%d')
    ArtiInfo = models.huataiPerformance.objects(date=d)

    if 'q' in request.GET:
        if request.GET['q'] == 'huatai':
            ArtiInfo = models.huataiPerformance.objects(date=d)
        if request.GET['q'] == 'xinhu':
            ArtiInfo = models.xinhuPerformance.objects(date=d)

    arrayList = {}
    deList = {}
    for arti in ArtiInfo:
        per = models.per(arti.netValue, arti.pnl, arti.equity, arti.pctChg, arti.date, arti.performanceDetails,
                         arti.initMoney, arti.totalMargin, arti.marginRatio, arti.notional, arti.leverage,
                         arti.netNotional, arti.netLeverage, arti.netPosDirection)
        arrayList = {'netValue': per.netValue, 'pnl': per.pnl, 'equity': per.equity, 'pctChg': per.pctChg,
                     'initMoney': per.initMoney}
        perDetails = pickle.loads(arti.performanceDetails)
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    # deList=json.dumps(deList)
    # response_data = {}
    # try:
    #     response_data['result'] = 'Success'
    #     response_data['message'] = serializers.serialize('json', ArtiInfo)
    # except:
    #     response_data['result'] = 'Ouch!'
    #     response_data['message'] = 'Script has not ran correctly'
    ll = perDetails[2]
    deList = json.dumps(perDetails, cls=DateEncoder)
    perDe = json.loads(deList)
    print(type(perDe))
    return JsonResponse(perDe, safe=False)
    # return HttpResponse(deList)


def ajax_list(request):
    a = range(100)
    return JsonResponse(a, safe=False)


def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)


def getSharpeRadio(listData):
    s1_c = pd.Series(data=listData)
    # 计算对数收益率序列
    s1_rets = np.log(s1_c / s1_c.shift(1))
    # print(s1_rets)
    # 计算平均收益率
    s1_rets_mean = s1_rets.mean()
    # print('平均收益率:', s1_rets_mean)
    # 计算夏普比率
    s1_sharp_ratio = s1_rets_mean / s1_rets.std()
    # print('夏普比率:', s1_sharp_ratio)
    return round(s1_sharp_ratio, 3)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, float):
        #     # print(obj)
        #     obj = round(obj,2)
        if obj < 0:
            # print(obj.__str__())
            # print(type(obj.__str__()))

            return obj.__int__()
            return json.JSONEncoder.default(self, obj)
        if obj >= 0:
            # print(obj.__str__())
            # print(type(obj.__str__()))
            return obj.__int__()
            return json.JSONEncoder.default(self, obj)

