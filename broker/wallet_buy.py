# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from utils.util import *
from utils.webselenium import *
from broker.trade_sell import *
from selenium.webdriver.support.select import Select
from broker.trade_sell import *
import os, time


def send_buy(_element, _ativo, _qtde, _preco):
    """
    :param _ativo:
    :param _qtde:
    :param _preco:
    :return:
    """
    # _element = self.driver.find_element_by_id
    _element(broker.get('BROKER_TAB_BUY')).click()
    value_now = str(float(_preco) + 0.1).replace('.',',')
    _value_buy = _element(broker.get('BROKER_VAL_BUY'))
    _value_buy.clear()
    _value_buy.send_keys(value_now, Keys.RETURN)
    # self.execute_orde(_ativo, _qtde)
    os.system('say buy active %s price %s' %(_ativo, str(_preco)))


    def can_buy(self, _element, _intent_buy):
        """
        :param _element:
        :param _intent_buy:
        :return:
        """
        try:
            # import ipdb; ipdb.set_trace()
            _active_intent = _intent_buy.active.cod_ativo
            _qtd_intent = _intent_buy.quantity #* _intent_buy.times
            _wallet_activs = self.get_wallet_broker(_element)
            for _wallet in _wallet_activs:
                _active_negoc = _wallet['ativo']
                _qtd_negoc = _wallet['qtd_negoc']
                if _active_intent == _active_negoc and _qtd_intent <= _qtd_negoc:
                    self.set_purchased(_intent_buy.active_id, True)
                    return False

            if _qtd_intent > 0:
                return True
        except:
            return False

    def get_stop_wallet(self, _wallet):
        """
        :param _active:
        :return:
        """
        _active = _wallet['ativo']
        _wallet_stop = Wallet.objects.filter(active__cod_ativo= _active)
        if _wallet_stop.exists():
            return _wallet_stop.first().stop_loss, _wallet_stop.first().stop_gain

    def set_top_trade_wallet(self, _cod_active, _type_option=None, _qtd_purchase=0):
        """
        :param _top_act: list with top active in broker
        :param _qtd_purchase: quantity available to purchase
        :return: takes the value available in the brokerage, notes the trend and sends to wallet
        """
        try:
            # import ipdb; ipdb.set_trace()
            _list_wallet = []
            _trade = Trade.objects.filter(cod_ativo= _cod_active)
            if _trade.exists():
                _vl_ultimo = _trade.first().vl_ultimo
                _variacao = _trade.first().variacao
                _time_purchase = _trade.first().hora
                _list_wallet.append({
                                        'active_id': _trade.first().id,
                                        'type_option': _type_option,
                                        'vl_ultimo': _vl_ultimo,
                                        'variacao': _variacao,
                                        'time_purchase': _time_purchase,
                                        'intention_buy': False,
                                        'stop_loss': get_stop_loss(_vl_ultimo),
                                        'stop_gain': get_stop_loss(_vl_ultimo),
                                        'quantity': _qtd_purchase,
                                        'times': 2,  # with auxiliary value of brokerage
                                        'observation': 'Purchase intent made by automation...'
                                    })
                self.save_json(_list_wallet)
                # print('Update contract options with more business.')
                # print('Positive trend in asset option %s => %s - %s - (%s)'
                #       %(_type_option, _cod_active, str(_vl_ultimo), str(_variacao)))
            else:
                print('There is not active in trade mycap and can not be included in the portfolio %s %s.'
                      %(_type_option, _cod_active))
        except:
            print('erro function set_top_trade_wallet')

    def get_qtd_purchase(self, _value_active, _finan_mycap):
        """
        :param _value_activ: value active now to purchase
        :param _finan_mycap: value available at no brokerage fees
        :return: looking for purchasing lot 100 according to asset value
        """
        _qtd_purchase = int(int(_finan_mycap / _value_active) / 100)* 100
        return _qtd_purchase
