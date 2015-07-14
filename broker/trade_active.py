# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from utils.util import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils.webselenium import *
from broker.sync_broker import *
import os
import time



# def trade_look(self, _act_now, _avg_minut=None):
#     _trade_actives = []
#     _trade_actives.append({
#                         'ativo': _act_now['cod_ativo'],
#                         'vl_ultimo': _act_now['vl_ultimo'],
#                         'variacao': _act_now['variacao'],
#                         'q_compra': _act_now['q_compra'],
#                         'compra': _act_now['compra'],
#                         'venda': _act_now['venda'],
#                         'q_venda': _act_now['q_venda'],
#                         'minimo': _act_now['minimo'],
#                         'maximo': _act_now['maximo'],
#                         'abert': _act_now['abert'],
#                         'fecham': _act_now['fecham'],
#                         'data': _act_now['data'],
#                         'hora': _act_now['hora'],
#                         'value_one_minut': _avg_minut
#                     })
