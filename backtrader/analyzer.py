#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pprint as pp

import six

from backtrader import MetaParams, Strategy
import backtrader.metabase as metabase


class MetaAnalyzer(MetaParams):
    def donew(cls, *args, **kwargs):
        '''
        Intercept the strategy parameter
        '''
        # Create the object and set the params in place
        _obj, args, kwargs = super(MetaAnalyzer, cls).donew(*args, **kwargs)

        _obj._children = list()

        _obj.strategy = strategy = metabase.findowner(_obj, Strategy)
        _obj._parent = metabase.findowner(_obj, Analyzer)

        _obj.datas = strategy.datas

        # For each data add aliases: for first data: data and data0
        if _obj.datas:
            _obj.data = data = _obj.datas[0]

            for l, line in enumerate(data.lines):
                linealias = data._getlinealias(l)
                if linealias:
                    setattr(_obj, 'data_%s' % linealias, line)
                setattr(_obj, 'data_%d' % l, line)

            for d, data in enumerate(_obj.datas):
                setattr(_obj, 'data%d' % d, data)

                for l, line in enumerate(data.lines):
                    linealias = data._getlinealias(l)
                    if linealias:
                        setattr(_obj, 'data%d_%s' % (d, linealias), line)
                    setattr(_obj, 'data%d_%d' % (d, l), line)

        # Return to the normal chain
        return _obj, args, kwargs

    def dopostinit(cls, _obj, *args, **kwargs):
        _obj, args, kwargs = \
            super(MetaAnalyzer, cls).dopostinit(_obj, *args, **kwargs)

        if _obj._parent is not None:
            _obj._parent._register(_obj)

        # Return to the normal chain
        return _obj, args, kwargs


class Analyzer(six.with_metaclass(MetaAnalyzer, object)):
    csv = True

    def __len__(self):
        return len(self.strategy)

    def _register(self, child):
        self._children.append(child)

    def _prenext(self):
        for child in self._children:
            child._prenext()

        self.prenext()

    def _nextstart(self):
        for child in self._children:
            child._nextstart()

        self.nextstart()

    def _next(self):
        for child in self._children:
            child._next()

        self.next()

    def _start(self):
        for child in self._children:
            child._start()

        self.start()

    def _stop(self):
        for child in self._children:
            child._stop()

        self.stop()

    def notify_order(self, order):
        pass

    def notify_trade(self, trade):
        pass

    def next(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        self.next()

    def start(self):
        pass

    def stop(self):
        pass

    def get_analysis(self):
        return dict()

    def print(self, *args, **kwargs):
        self.pprint(*args, **kwargs)

    def pprint(self, *args, **kwargs):
        pp.pprint(self.get_analysis(), *args, **kwargs)
