# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from utils.util import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils.webselenium import *
from broker.sync_broker import *
from operator import itemgetter
import os
import time


def send_sale(_element, _ativo, _qtde, _preco):
    """
    :param _ativo:
    :param _qtde:
    :param _preco:
    :return:
    """
    # _element = self.driver.find_element_by_id
    _element(broker.get('BROKER_TAB_SELL')).click()
    value_now = str(float(_preco) - 0.1).replace('.',',')
    _value_sell = _element(broker.get('BROKER_VAL_SELL'))
    _value_sell.clear()
    _value_sell.send_keys(value_now, Keys.RETURN)
    # self.execute_orde(_ativo, _qtde)
    os.system('say active sale sale %s price %s' %(_ativo, str(_preco)))


_max_value = {}
def can_sell(self, _act_now):
    """
    :param _act_now:
    :param _stop_loss:
    :return:
    """
    # import ipdb; ipdb.set_trace()
    _trade = Trade()
    _active = _act_now['cod_ativo']
    _value_now = _act_now['vl_ultimo']

    if self._max_value.get(_active) is None:
        self._max_value.update({_active: 0})
    if self._max_value.get(_active) < _value_now:
        self._max_value.update({ _active: _value_now})

    # _inv = Investment()
    # _value_purchase = _inv.get_value_purchase(_active) - 0.01
    _stop_loss = self._max_value.get(_active) - get_stop_loss(_value_now)
    print('_value_now => %s _stop_loss => %s' %(_value_now, _stop_loss))
    if (_value_now <= _stop_loss) or self.penny_stocks(_act_now):
        self._max_value.update({_active: 0})
        return True

    return False

def penny_stocks(self, _act_now):
    """
    :param _act_now:
    :return:
    """
    if (_act_now['compra'] < _act_now['vl_ultimo']) and (_act_now['q_compra'] < (_act_now['q_venda'] / 3)):
        return True

    return False