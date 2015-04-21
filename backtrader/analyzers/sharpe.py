#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import operator

from six.moves import map

from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn


class SharpeRatio(Analyzer):
    '''
    This analyzer calculates the SharpRatio of a strategy using a risk free
    asset which is simply an interest rate

    Params:

      - riskfreerate: (default: 0.01 -> 1%)

    Member Attributes:

      - ``anret``: list of annual returns used for the final calculation

    **get_analysis**:

      - Returns a dictionary with key "sharperatio" holding the ratio
    '''
    params = (('timeframe', TimeFrame.Years), ('riskfreerate', 0.01),)

    def __init__(self):
        super(SharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)

        self.ratio = retavg / retdev

    def get_analysis(self):
        return dict(sharperatio=self.ratio)
