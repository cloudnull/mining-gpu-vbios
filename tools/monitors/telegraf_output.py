#!/usr/bin/env python

# Copyright (C) 2018  Kevin Carter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time


def current_time():
    """Return the current time in nanoseconds."""
    return int(time.time() * 1000000000)


def _telegraf_line_format(sets, quote=False):
    """Return a comma separated string."""
    store = list()
    for k, v in sets.items():
        k = k.replace(' ', '_')
        if not isinstance(v, (int, float, bool)) and quote:
            store.append('{}="{}"'.format(k, v))
        else:
            store.append('{}={}'.format(k, v))
    return ','.join(store).rstrip(',')


def write_telegraf(result, metric_name, timestamp, tag=None):
    """Output in telegraf format."""
    resultant = [metric_name]
    if tag:
        resultant.append(_telegraf_line_format(sets=tag))
    resultant = [
        ','.join(resultant).strip(','),
        _telegraf_line_format(sets=result, quote=True),
        timestamp
    ]
    print(' '.join(resultant))
