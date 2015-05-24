#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .. import Observer


class DrawDown(Observer):
    lines = ('drawdown', 'maxdrawdown',)

    plotinfo = dict(plot=True, subplot=True)

    plotlines = dict(maxdrawdown=dict(_plotskip='True',))

    def __init__(self):
        super(DrawDown, self).__init__()

        self.maxdd = 0.0
        self.peak = float('-inf')

    def next(self):
        value = self._owner.stats.broker.value[0]

        # update the maximum seen peak
        if value > self.peak:
            self.peak = value

        # calculate the current drawdown
        self.lines.drawdown[0] = dd = 100.0 * (self.peak - value) / self.peak

        # update the maxdrawdown if needed
        self.lines.maxdrawdown[0] = self.maxdd = max(self.maxdd, dd)
