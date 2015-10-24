# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from utils.util import *
from utils.webselenium import *
from broker.trade_sell import *
from broker.wallet_buy import *
from broker.find_options import *
from broker.search_buy import *
from broker.find_options import findOptions, findOptionsLoop
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *
import time, sys, threading, inspect, os


# os.environ["webdriver.chrome.driver"] = directory.get('CHROME_DRIVER')
"""
    That defines who wins the market or is on the way
         => Conscious wealth = (gain - spending) * interest
         => Maturity, power reaction
         => Coldness to handle loss
         => Stop loss or gain of conscious way

     Recovery in the short term and continuation of the main trend of high
     Analysis of the re-entry of the buying pressure
     Analysis of congestion or accumulated force fight between (buy / sell)
     Trade bull with great volatility, positions in rumor and in fact correct

     To-Do => Analise da movimentacao
     => Tendencia principal de alta
     => Topos e fundos acendentes
     => Medias moveis possitivamente inclinadas
     => Forte processo de acumulo de capital nos ultimos meses
"""

class syncBroker(threading.Thread):
    """Thread that executes a task every N seconds"""
    robot_broker = None
    def __init__(self):
        if self.robot_broker is None:
            threading.Thread.__init__(self)
            self._finished = threading.Event()
            self.robot_broker = robotBroker()
        self._interval = 0

    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        """
        :return: sleep for interval or until shutdown
        if self._finished.isSet(): return self._finished.wait(self._interval)
        """
        while True:
            self.robot_broker._intent_sell()
            # self._robot_broker._intent_buy(_search_buy())

    def __hash__(self):
        """
        :return:
        """
        return 0


class robotBroker(RobotRemoteChrome):
# class robotBroker(RobotRemoteFirefox):
    """
        Go to Sync Broker and if is not logged make login
        java -jar selenium-server-standalone-2.45.0.jar
        https://selenium-release.storage.googleapis.com/index.html?path=2.45/
    """
    _usr = broker.get('BROKER_USERNAME') or 'BROKER_USERNAME'
    _pwd = broker.get('BROKER_PASSWORD') or 'BROKER_PASSWORD'

    def __init__(self, debug=False, proxy=False, *args, **kwargs):
        """
        :param debug:
        :param proxy:
        :param args:
        :param kwargs:
        :return:
        """
        super(robotBroker, self).__init__(*args, **kwargs)
        # self.driver.manage().window().setSize(windowMinSize)
        self.switch_to_window_broker()
        self.do_login(self._usr, password=None)
        self.is_logged()
        if not debug:
            self.switch_to_window_advfn()
            # find_options = findOptions()
            # options = find_options.list_options()
            # if op
            #
            # if bool(_options):
            #     self.send_active_broker(_options)

        self.switch_to_window_broke()
        self.send_report_invest(True)

    def switch_to_window_broker(self):
        """
        :return:
        """
        try:
            # self.driver.find_element_by_tag_name('body').send_keys(Keys.LEFT_CONTROL + Keys.COMMAND + 'f')
            _url_broker = broker.get('URL_BROKER') or 'URL_BROKER'
            self.driver.switch_to_window(self.driver.window_handles[0])
            self.driver.get(_url_broker)
        except:
            self.switch_to_window_broker()

    def do_login(self, username, password=None):
        """
        :param username:
        :param password:
        :return:
        """
        try:
            _caption =  self.driver.find_element_by_id(broker.get('BROKER_TXT_LOGIN'))
            _caption.clear()
            _caption.send_keys(username)
            self.driver.find_element_by_id(broker.get('BROKER_BTN_OK')).click()
            self.driver.find_element_by_class_name('login').click()
        except:
            self.do_login(username)

    def is_logged(self):
        """
        :return: Check if user name is on html content
        """
        try:
            while self.driver.window_handles.__len__() == 1:
                time.sleep(5)
                self.is_logged()
        except:
            self.is_logged()

    def switch_to_window_broke(self):
        """
        :return:
        """
        try:
            while self.driver.window_handles.__len__() > 2:
                self.driver.switch_to_window(self.driver.window_handles[-1])
                self.driver.close()
            _url_broker = broker.get('URL_TRADE') or 'URL_TRADE'
            self.driver.switch_to_window(self.driver.window_handles[1])
            self.driver.get(_url_broker)
        except:
            self.switch_to_window_broke()

    def switch_to_window_advfn(self):
        """
        :return:
        """
        try:
            self.driver.execute_script("window.open('','_blank');")
            self.driver.switch_to_window(self.driver.window_handles[2])
        except:
            self.switch_to_window_advfn()

    def send_active_broker(self, _active=[]):
        """
        :param _active:
        :return:
        """
        try:
            for _active in _options.keys():
                for _type_option in ['compra', 'venda']:
                    _cod_option = _options.get(_active).get(_type_option)
                    # _list_trade += self.get_list_trade(_cod_option)
                    _caption = _driver.find_element_by_id(broker.get('BROKER_CAPTION_GRID'))
                    _caption.clear()
                    _caption.send_keys(_cod_option, Keys.RETURN)
        except:
            self.send_active_broker(_active)

    def execute_ordem(self, _type_exec, _ativo, _qtde, _preco):
        """
        :param _ativo:
        :param _qtde:
        :param _pwd:
        :return:
        """
        _element = self.driver.find_element_by_id
        if _type_exec == 'sale':
            send_sale(_element, _ativo, _qtde, _preco)
        elif _type_exec == 'buy':
            send_buy(_element, _ativo, _qtde, _preco)

        _active = _element(broker.get('BROKER_ACTIVE'))
        _active.clear()
        _active.send_keys(_ativo, Keys.RETURN)
        _quant = _element(broker.get('BROKER_QUANT'))
        _quant.clear()
        _quant.send_keys(str(_qtde), Keys.RETURN)
        _signat = _element(broker.get('BROKER_SIGNAT'))
        _signat.clear()
        _signat.send_keys(self._pwd, Keys.RETURN)
        _element(broker.get('BROKER_BTN_CONF')).click()

    def _intent_buy(self):
        """
        :return: make an actual purchase with intention_buy is True
        """
        # import ipdb; ipdb.set_trace()
        # try:
        _wallet = Wallet()
        _intent_buy = Wallet.objects.filter(intention_buy=True, purchased=False)
        for _buy in _intent_buy:
            if hour_broker() and _wallet.can_buy(self.driver.find_element_by_id, _buy):
                _ativo = _buy.active.cod_ativo
                _qtde = _buy.quantity
                _preco = float(_buy.active.vl_ultimo)
                self.execute_ordem('buy', _ativo, _qtde, _preco)
                print('Active %s purchase quantity = %s price = %s' %(_ativo, _qtde, _preco))
                self.send_report_invest()

    def _intent_sell(self):
        """
        :return:
        """
        # import ipdb; ipdb.set_trace()
        _qtd_to_sell = 1
        _trade = Trade()

        while _qtd_to_sell != 0:
            self._intent_buy()
            _qtd_to_sell = 0
            for _wallet_item in self.get_wallet_broker():
                _active = _wallet_item['ativo']
                _num_grid = _wallet_item['num_grid']
                _act_now = self.get_list_trade(_active, _num_grid)
                _qtd_to_sell += int(_wallet_item['qtd_negoc'])

                if _trade.can_sell(_act_now):
                    _ativo = _wallet_item['ativo']
                    _qtde = _wallet_item['qtd_negoc']
                    _preco = float(_act_now['vl_ultimo'])
                    self.execute_ordem('buy', _ativo, _qtde, _preco)
                    print('Active %s sale sale price %s' %(_ativo, _preco))
                    self.send_report_invest()

    def send_report_invest(self, _first_time=False):
        """
        :param _element: driver selenium, time send call to extract
        :return: extract broker moviment last 7 days, palet ordens and click in export xls
        :param _element: _items_month.__len__() == 15  filter month to get extract Últimos 7 dias
        :param _element: _items_status.__len__() == 09 filter status e click search Executadas
        """
        try:
            _suas_ordens = self.driver.find_element_by_id(broker.get('BROKER_ORD_MENU'))
            _suas_ordens.click()
            # Select(self.driver.find_element_by_id(broker.get('BROKER_ORD_COMB')).find_elements_by_tag_name('li')).select_by_visible_text(u"Últimos 7 dias")

            _items_month = self.driver.find_element_by_id(broker.get('BROKER_ORD_COMB')).find_elements_by_tag_name('li')
            _items_month[0].click()
            _items_month[2].click()

            _items_status = self.driver.find_element_by_id(broker.get('BROKER_ORD_STAT')).find_elements_by_tag_name('li')
            _items_status[0].click()
            _items_status[5].click()

            if _items_month[0].text != u"Últimos 7 dias" or _items_status[0].text != u"Executadas":
                self.send_report_invest(_first_time)
            else:
                self.driver.find_element_by_id(broker.get('BROKER_ORD_INPT')).click()
                self.driver.find_element_by_id(broker.get('BROKER_ORD_EXPT')).click()
                if _first_time:
                    time.sleep(10)
                _wn = WeekNumber()
                _wn.send_file_to_dropbox()
        except:
            self.send_report_invest(_first_time)

    def get_wallet_broker(self):
        """
        :param _element: driver selenium find to go erro element not exists
        :return: search active purchase in wallet to sell
        """
        # import ipdb; ipdb.set_trace()
        _num_grid = -1
        _wallet = []
        try:
            while True:
                _num_grid += 1
                _num_grid_trade = 0
                _element = self.driver.find_element_by_id
                _carteira = _element(broker.get('BROKER_MEN_WALT'))
                _carteira.click()
                self.take_screenshot()
                if _element(broker.get('BROKER_LIN_WALT') + str(_num_grid)).text != None:
                    _ativo = _element(broker.get('BROKER_ACT_POST') + str(_num_grid)).text
                    _qtd_negoc = int(_element(broker.get('BROKER_ACT_QTDI') + str(_num_grid)).text.replace('.',''))
                    _trade_base = Trade.objects.filter(cod_ativo= _ativo)
                    if _trade_base.exists():
                        _num_grid_trade = _trade_base.first().num_grid

                    if _qtd_negoc > 0:
                        _wallet.append({
                                            'ativo': _ativo,
                                            'qtd_negoc': _qtd_negoc,
                                            'num_grid': _num_grid_trade
                                        })
        except:
            return _wallet

    def get_value_action_available_broker(self):
        """
        :param _element:
        :return: value available in the brokerage
        """
        try:
            _value_available = 0
            while _value_available == 0:
                _element(broker.get('BROKER_MEN_FINA')).click()
                _value_available = str_to_float(_element(broker.get('BROKER_VAL_ACTI')).text.split('\n')[1])
        except:
            self.get_value_action_available_broker()
        return _value_available

    def get_value_option_available_broker(self):
        """
        :param _element:
        :return: value available in the brokerage
        """
        try:
            _value_available = 0
            while _value_available == 0:
                _element(broker.get('BROKER_MEN_FINA')).click()
                _value_available = str_to_float(_element(broker.get('BROKER_VAL_OPTI')).text.split('\n')[1])
        except:
            self.get_value_option_available_broker()
        return _value_available