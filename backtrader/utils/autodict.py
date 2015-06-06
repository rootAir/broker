#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import OrderedDict


class AutoDict(dict):
    _closed = False

    def _close(self):
        self._closed = True
        for key, val in self.items():
            if isinstance(val, (AutoDict, AutoOrderedDict)):
                val._close()

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def __getattr__(self, key):
        if False and key.startswith('_'):
            raise AttributeError

        return self[key]

    def __setattr__(self, key, value):
        if False and key.startswith('_'):
            self.__dict__[key] = value
            return

        self[key] = value


class AutoOrderedDict(OrderedDict):
    _closed = False

    def _close(self):
        self._closed = True
        for key, val in self.items():
            if isinstance(val, (AutoDict, AutoOrderedDict)):
                val._close()

    def _open(self):
        self._closed = False

    def __missing__(self, key):
        if self._closed:
            raise KeyError

        value = self[key] = type(self)()
        return value

    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError

        return self[key]

    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
            return

        self[key] = value

    # Define math operations
    def __iadd__(self, other):
        if type(self) != type(other):
            return type(other)() + other

        return self + other

    def __isub__(self, other):
        if type(self) != type(other):
            return type(other)() - other

        return self - other

    def __imul__(self, other):
        if type(self) != type(other):
            return type(other)() * other

        return self + other

    def __idiv__(self, other):
        if type(self) != type(other):
            return type(other)() // other

        return self + other

    def __itruediv__(self, other):
        if type(self) != type(other):
            return type(other)() / other

        return self + other
