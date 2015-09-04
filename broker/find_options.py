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
from settings import *
import time, sys, threading, inspect, os


class findOptionsLoop(threading.Thread):
    """Thread that executes a task every N seconds"""
    robot_options = None
    def __init__(self):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 1

    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        """
        :return: sleep for interval or until shutdown
        """
        while not self._finished.wait(self._interval):
            self._interval = broker.get('INTERVAL_FIND_OPTION')
            self.robot_options = findOptions()
            print(self.robot_options.list_options())
            self.robot_options.driver.close()

    def __hash__(self):
        """
        :return: __hash__
        """
        return 0


class findOptions(RobotRemoteChrome):
# class robotOptions(RobotRemoteFirefox):

    def __init__(self, debug=False, proxy=False, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        super(self.__class__, self).__init__(*args, **kwargs)

    def list_options(self):
        """
        :param:  driver selenium connect
        :return: contract vigent to month in bovesp with max business ATM
        """
        try:
            _list_options = {}
            # import ipdb; ipdb.set_trace()
            for _option in listOptions:
                _best_type = {}
                for _type_option in ['compra', 'venda']:
                    url_option = url.get('URL_OPTION') %(_option, _type_option)
                    _cod_option = self.find_best_options(url_option)
                    if bool(_cod_option):
                        _best_type.update({ _type_option: _cod_option })

                if _best_type.__len__() > 0:
                    _list_options.update({ _option: _best_type })

            return _list_options
        except:
            return self.list_options()

    def find_best_options(self, url_option):
        """
        :param _option:
        :param _type:
        :return:
        """
        try:
            self.driver.get(url_option)
            time.sleep(2)
            _begin_day = True
            _table_options = self.driver.find_element_by_id('options-table').text
            _max_business = 0
            _best_option = ''
            for _row_option in _table_options.split('\n'):
                _list_option = _row_option.split(' ')
                if _list_option.__len__() == 10:
                    _option = _list_option[0]
                    _stile = _list_option[1]
                    _classif = _list_option[2]
                    _cotacao = _list_option[3]
                    _variation = _list_option[4]
                    _buy = _list_option[5]
                    _sell = _list_option[6]
                    _intrins = _list_option[7]
                    _extrins = _list_option[8]
                    _qtd_business = int(_list_option[9].replace('-','0').replace('.',''))

                    if _max_business < _qtd_business:
                        _max_business = _qtd_business
                        _best_option = _option
                    if _list_option[9] != '-':
                        _begin_day = False

            # import ipdb; ipdb.set_trace()
            if _begin_day and _table_options != '':
                return False
            if _table_options == '' or _best_option == '':
                return self.find_best_options(self.driver)

            return _best_option
        except:
            self.driver.get(url_option)
            time.sleep(2)
            self.find_best_options(self.driver)
            # print('erro sync contract vigent option in advfn.')

    # def get_cpo_status(self, search_period=u"Mês anterior"):
    #     """
    #     :param search_period:
    #     :return:
    #     """
    #     try:
    #         self.driver.switch_to_alert().accept()
    #     except NoAlertPresentException:
    #         pass
    #
    #     self.driver.switch_to_default_content()
    #     self.driver.switch_to_frame("pb_1053011930")
    #     frames = self.driver.find_elements_by_tag_name('frame')
    #     self.driver.switch_to_frame(frames[0].get_attribute('name'))
    #     self.driver.find_element_by_id("menu_SUS30MENU0000000018-cnt-start").click()
    #     Select(self.driver.find_element_by_id("search_searchPeriodDropdownListBox")).select_by_visible_text(search_period)
    #     self.driver.find_element_by_css_selector("span.urBtnPadding").click()
    #
    #     # Ler informações das tabelas
    #     self.wait_by_element_id("order.list_list_pager-btn-4")
    #     next_page_bt = self.driver.find_element_by_id("order.list_list_pager-btn-4")
    #     while True:
    #         status_from_page = self.get_cpo_status_from_page_source()
    #         result = result + status_from_page
    #         if next_page_bt.get_attribute('class') == u'urBtnIco urPagVBtnNxtPage':
    #             self.driver.find_element_by_id("order.list_list_pager-btn-4").click()
    #             self.wait_by_element_id("order.list_list_pager-btn-4")
    #             next_page_bt = self.driver.find_element_by_id("order.list_list_pager-btn-4")
    #         else:
    #             break
    #     return result
