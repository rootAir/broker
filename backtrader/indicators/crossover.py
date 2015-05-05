#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, And


class _CrossBase(Indicator):
    lines = ('cross',)

    plotinfo = dict(plotymargin=0.05, plotyhlines=[0.0, 1.0])

    def __init__(self):
        if self._crossup:
            before = self.data0(-1) < self.data1(-1)
            after = self.data0 > self.data1
        else:
            before = self.data0(-1) > self.data1(-1)
            after = self.data0 < self.data1

        self.lines.cross = And(before, after)


class CrossUp(_CrossBase):
    '''
    This indicator gives a signal if the 1st provided data crosses over the 2nd
    indicator upwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1t and 2nd data

    This indicator is not automatically plotted

    Formula:
      - upcross = data0(-1) < data1(-1) and data0(0) > data1(0)
    '''
    _crossup = True


class CrossDown(_CrossBase):
    '''
    This indicator gives a signal if the 1st provided data crosses over the 2nd
    indicator upwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1t and 2nd data

    This indicator is not automatically plotted

    Formula:
      - upcross = data0(-1) < data1(-1) and data0(0) > data1(0)
    '''
    _crossup = False


class CrossOver(Indicator):
    '''
    This indicator gives a signal if the provided datas (2) cross up or down.

      - 1.0 if the 1st data crosses the 2nd data upwards
      - -1.0 if the 1st data crosses the 2nd data downwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1t and 2nd data

    This indicator is not automatically plotted

    Formula:
      - upcross = data0(-1) < data1(-1) and data0(0) > data1(0)
      - downcross = data0(-1) > data1(-1) and data0(0) < data1(0)
      - crossover = upcross - downcross
    '''
    lines = ('crossover',)

    plotinfo = dict(plot=False, plotymargin=0.05, plotyhlines=[-1.0, 1.0])

    def __init__(self):
        upcross = CrossUp(self.data, self.data1)
        downcross = CrossDown(self.data, self.data1)

        self.lines.crossover = upcross - downcross
