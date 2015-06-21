#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime


# A UTC class, same as the one in the Python Docs
class _UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


UTC = _UTC()


HOURS_PER_DAY = 24.0
MINUTES_PER_HOUR = 60.0
SECONDS_PER_MINUTE = 60.0
MUSECONDS_PER_SECOND = 1e6
MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_DAY
MUSECONDS_PER_DAY = MUSECONDS_PER_SECOND * SECONDS_PER_DAY


def _num2date(x, tz=None):
    # Same as matplotlib except if tz is None a naive datetime object
    # will be returned.
    """
    *x* is a float value which gives the number of days
    (fraction part represents hours, minutes, seconds) since
    0001-01-01 00:00:00 UTC *plus* *one*.
    The addition of one here is a historical artifact.  Also, note
    that the Gregorian calendar is assumed; this is not universal
    practice.  For details, see the module docstring.
    Return value is a :class:`datetime` instance in timezone *tz* (default to
    rcparams TZ value).
    If *x* is a sequence, a sequence of :class:`datetime` objects will
    be returned.
    """

    ix = int(x)
    dt = datetime.datetime.fromordinal(ix)
    remainder = float(x) - ix
    hour, remainder = divmod(HOURS_PER_DAY * remainder, 1)
    minute, remainder = divmod(MINUTES_PER_HOUR * remainder, 1)
    second, remainder = divmod(SECONDS_PER_MINUTE * remainder, 1)
    microsecond = int(MUSECONDS_PER_SECOND * remainder)
    if microsecond < 10:
        microsecond = 0  # compensate for rounding errors

    if tz is not None:
        dt = datetime.datetime(
            dt.year, dt.month, dt.day, int(hour), int(minute), int(second),
            microsecond, tzinfo=UTC).astimezone(tz)
    else:
        # If not tz has been passed return a non-timezoned dt
        dt = datetime.datetime(
            dt.year, dt.month, dt.day, int(hour), int(minute), int(second),
            microsecond)

    if microsecond > 999990:  # compensate for rounding errors
        dt += datetime.timedelta(microseconds=1e6 - microsecond)

    return dt


def _date2num(dt):
    """
    Convert :mod:`datetime` to the Gregorian date as UTC float days,
    preserving hours, minutes, seconds and microseconds.  Return value
    is a :func:`float`.
    """
    if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        delta = dt.tzinfo.utcoffset(dt)
        if delta is not None:
            dt -= delta

    base = float(dt.toordinal())
    if hasattr(dt, 'hour'):
        base += (dt.hour / HOURS_PER_DAY +
                 dt.minute / MINUTES_PER_DAY +
                 dt.second / SECONDS_PER_DAY +
                 dt.microsecond / MUSECONDS_PER_DAY
                 )
    return base
