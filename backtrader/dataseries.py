#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from six.moves import xrange

from .lineseries import LineSeries
from .import num2date
from .utils import OrderedDict


class TimeFrame(object):
    Minutes, Days, Weeks, Months, Years = range(5)
    names = ['Minutes', 'Days', 'Weeks', 'Months', 'Years']

    @classmethod
    def getname(cls, tframe, compression):
        if compression == 1:
            # return singular if compression is 1
            return cls.names[tframe][:-1]
        return cls.names[tframe]


class DataSeries(LineSeries):
    _name = ''
    _compression = 1
    _timeframe = TimeFrame.Days

    Close, Low, High, Open, Volume, OpenInterest, DateTime = range(7)

    LineOrder = [DateTime, Open, High, Low, Close, Volume, OpenInterest]

    def getwriterheaders(self):
        headers = [self._name, 'len']

        for lo in self.LineOrder:
            headers.append(self._getlinealias(lo))

        morelines = self.getlinealiases()[len(self.LineOrder):]
        headers.extend(morelines)

        return headers

    def getwritervalues(self):
        values = [self._name, len(self)]

        dtstr = num2date(self.datetime[0])
        values.append(dtstr)

        for line in self.LineOrder[1:]:
            values.append(self.lines[line][0])

        for i in xrange(len(self.LineOrder), self.lines.size()):
            values.append(self.lines[i][0])

        return values

    def getwriterinfo(self):
        # returns dictionary with information
        info = OrderedDict()
        info['Name'] = self._name
        info['Timeframe'] = TimeFrame.names[self._timeframe]
        info['Compression'] = self._compression

        return info


class OHLC(DataSeries):
    lines = ('close', 'low', 'high', 'open', 'volume', 'openinterest',)


class OHLCDateTime(OHLC):
    lines = (('datetime'),)
