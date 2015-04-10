#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from .lineiterator import LineIterator, ObserverBase, StrategyBase


class Observer(ObserverBase):
    _OwnerCls = StrategyBase
    _ltype = LineIterator.ObsType

    csv = True

    plotinfo = dict(plot=False, subplot=True)

    # An Observer is ideally always observing and that' why prenext calls
    # next. The behaviour can be overriden by subclasses
    def prenext(self):
        self.next()
