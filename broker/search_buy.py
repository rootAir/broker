# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from threading import Thread
from time import sleep
from utils.util import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils.webselenium import *
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.select import Select
from broker.wallet_buy import *
from broker.trade_sell import *
import time, sys, threading, inspect, os
from settings import *


def get_list_trade(_driver, _active=None):
    """
    :param _active:
    :return:
    """
    # import ipdb; ipdb.set_trace()
    _active_trade = {}
    if _active is not None:
        _trade_base = Trade.objects.filter(cod_ativo= _active.upper())
        if _trade_base.exists():
            _num_grid = _trade_base.first().num_grid
            _active_trade = get_active_trade(_driver, _num_grid)
            if _active_trade.__len__() > 0 and _active == _active_trade['cod_ativo']:
                return _active_trade

    _list_trade = []
    _num_grid = 0
    _num_grid_max = 50
    while _num_grid < _num_grid_max:
        _trade_broker_list = get_active_trade(_driver, _num_grid)
        _num_grid += 1
        if _trade_broker_list.__len__() > 0:
            _list_trade.append( _trade_broker_list )
        else:
            _num_grid = _num_grid_max
    _trade = Trade()
    _trade.save_json(_list_trade)
    Trade.objects.exclude(hora__day=datetime.today().date().day).delete()
    return _list_trade

def upd_scroll(_driver, _num_grid=0):
    """
    :param _driver:
    :param _num_grid:
    :return:
    """
    _px_scroll = 6 * _num_grid
    _driver.execute_script(broker.get('BROKER_SCROL') %str(_px_scroll))
    _driver.find_elements_by_class_name('thumb')[1].click()

def get_active_trade(_driver, _num_grid=0):
    """
    :param _driver:
    :param _num_grid:
    :return:
    """
    try:
        # import ipdb; ipdb.set_trace()
        # upd_scroll(_driver, _num_grid)
        _list_trade = {}
        _element_id = broker.get('BROKER_GRID') + str(_num_grid)
        _active_broker = _driver.find_element_by_id(_element_id)
        _active_list = _active_broker.text.split('\n')
        if _active_list is not None and _active_list.__len__() in [20, 21]:
            _date = _active_list[11].replace('/','-')
            _year = _date.split('-')[2]
            _date = _date[:-2] + '20' + _year
            _list_trade.update({
                                    'cod_ativo': _active_list[0],
                                    'vl_ultimo': to_float(_active_list[1]),
                                    'variacao': fix_variacao(_active_list[2]),
                                    'q_compra': to_float(_active_list[3]),
                                    'compra': to_float(_active_list[4]),
                                    'venda': to_float(_active_list[5]),
                                    'q_venda': to_float(_active_list[6]),
                                    'minimo': to_float(_active_list[7]),
                                    'maximo': to_float(_active_list[8]),
                                    'abert': to_float(_active_list[9]),
                                    'fecham': to_float(_active_list[10]),
                                    'data': str_to_date(_active_list[11]),
                                    'hora': str_to_datetime(_date, _active_list[12]),
                                    'volume': _active_list[13],
                                    'perc_ano': _active_list[14],
                                    'perc_mes': _active_list[15],
                                    'pco_exerc': _active_list[16],
                                    'vencim': _active_list[17],
                                    'lot_neg': _active_list[18],
                                    'pco_medio': to_float(_active_list[19]),
                                    'num_grid': _num_grid,
                                    'n_net': 0
                            })
        return _list_trade
    except:
        return _list_trade

_minut_trend = broker.get('MINUTE_FIND_TREND')            # minut find trend in top trade now = 3
_qtd_act = broker.get('QUANT_FIND_ACTIVE')                # quantity find best active now in broker (send to wallet) = 4
_vl_max_purchase = broker.get('VALUE_MAX_PURCHASE')       # value maximize to intent buy = 10

def get_top_trade(_driver):
    """
    :param _driver:
    :param _active:
    :return: notes the trend and sends to wallet
    """
    # import ipdb; ipdb.set_trace()
    _trend_trade_minut = []
    _best_trend = None
    _trade = get_list_trade(_driver)
    if _trade.__len__() > 0:
        _trade_sorted = sorted(_trade, key=sort_by_variacao, reverse=True)

        while _trend_trade_minut.__len__() < _minut_trend:
            _list_minut = analysis_trend(_driver, _trade_sorted)
            if _list_minut.__len__() > 0:
                _trade_minut = max(_list_minut, key=itemgetter('trend_one_minut'))
                _trend_trade_minut.append({
                                                'active': _trade_minut['active'],
                                                'trend_one_minut': _trade_minut['trend_one_minut']
                                            })
        _best_trend = max(_trend_trade_minut, key=itemgetter('trend_one_minut'))['active']
    return _best_trend

def sort_by_variacao(d):
    """
    :param d:
    :return:
    """
    return d['variacao']

def analysis_trend(_driver, _trade_sorted):
    """
    :param _driver:
    :param _trade_sorted:
    :return: trend time search 1 minut
    """
    # import ipdb; ipdb.set_trace()
    _num_grid = None
    _top_trade = []
    _trend_trade = []
    _start_time = time.time()
    _line = 0
    _cont = 1
    _qtd_active = _trade_sorted.__len__()
    while timedelta(seconds=time.time() - _start_time).seconds < 60 and _line < _qtd_active:
        if _trade_sorted[_line]['vl_ultimo'] < _vl_max_purchase:
            _num_grid = _trade_sorted[_line]['num_grid']
            json_trade = get_active_trade(_driver, _num_grid)
            if json_trade.__len__() > 0:
                _top_trade.append(json_trade)
                if _cont < _qtd_act:
                    _cont += 1
                    _line += 1
                else:
                    _cont = 0
                    _line = 0
        else:
            _line += 1

    by_item = {}
    for d in _top_trade:
        _variacao = to_float(d['variacao'])
        by_item.setdefault(d['cod_ativo'], []).append(_variacao)

    _stats = dict((k, {'minValue': min(v), 'maxValue': max(v)}) for k, v in by_item.items())

    for key, value in _stats.items():
        _trend_one_minut = round((_stats[key]['maxValue'] + _stats[key]['minValue'])/2, 2)
        _trend_trade.append({
                                'active': key,
                                'trend_one_minut': _trend_one_minut
                            })
    return _trend_trade