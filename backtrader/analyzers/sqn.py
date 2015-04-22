#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from backtrader import Analyzer
from backtrader.mathsupport import average, standarddev
from backtrader.utils import AutoOrderedDict


class SQN(Analyzer):
    alias = ('SystemQualityNumber',)

    def start(self):
        self.ret = AutoOrderedDict()
        self.pnl = list()
        self.count = 0

    def notify_trade(self, trade):
        if trade.status == trade.Closed:
            self.pnl.append(trade.pnlcomm)
            self.count += 1

    def stop(self):
        pnl_av = average(self.pnl)
        pnl_stddev = standarddev(self.pnl)

        trades_sqr = pow(len(self.pnl), 0.5)

        sqn = trades_sqr * pnl_av / pnl_stddev

        self.ret.sqn = sqn
        self.ret.trades = self.count

    def get_analysis(self):
        return self.ret
