#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .. import Observer


class Cash(Observer):
    lines = ('cash',)

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        self.lines[0][0] = self._owner.broker.getcash()


class Value(Observer):
    lines = ('value',)

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        self.lines[0][0] = self._owner.broker.getvalue()


class Broker(Observer):
    alias = ('CashValue',)
    lines = ('cash', 'value')

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        self.lines.cash[0] = self._owner.broker.getcash()
        self.lines.value[0] = value = self._owner.broker.getvalue()
