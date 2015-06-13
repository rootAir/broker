#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

from .dateintern import _num2date, _date2num

__all__ = ('num2date', 'date2num')

try:
    import matplotlib.dates as mdates

except ImportError:
    num2date = _num2date
    date2num = _date2num
else:
    num2date = mdates.num2date
    date2num = mdates.date2num
