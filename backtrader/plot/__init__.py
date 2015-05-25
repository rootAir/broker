#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

try:
    import matplotlib
except ImportError:
    raise ImportError(
        'Matplotlib seems to be missing. Needed for plotting support')


from .plot import Plot
from .scheme import PlotScheme
