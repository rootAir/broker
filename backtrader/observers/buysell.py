#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math

from ..observer import Observer


class BuySell(Observer):
    lines = ('buy', 'sell',)

    plotinfo = dict(plot=True, subplot=False, plotlinelabels=True)
    plotlines = dict(
        buy=dict(marker='^', markersize=8.0, color='lime', fillstyle='full'),
        sell=dict(marker='v', markersize=8.0, color='red', fillstyle='full')
    )

    def next(self):
        buy = list()
        sell = list()

        for order in self._owner._orderspending:
            if order.data is not self.data or not order.executed.size:
                continue

            if order.isbuy():
                buy.append(order.executed.price)
            else:
                sell.append(order.executed.price)

        # Write down the average buy/sell price
        self.lines.buy[0] = math.fsum(buy)/float(len(buy) or 'NaN')
        self.lines.sell[0] = math.fsum(sell)/float(len(sell) or 'NaN')
