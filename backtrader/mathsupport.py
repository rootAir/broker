#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math
import operator


def average(x):
    return math.fsum(x) / len(x)


def variance(x):
    return list(map(lambda y: (y - average(x)) ** 2, x))


def standarddev(x):
    return math.sqrt(average(variance(x)))
