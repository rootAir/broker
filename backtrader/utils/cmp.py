#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

if six.PY3:
    def cmp(a, b):
        return (a > b) - (a < b)

else:
    cmp = cmp
