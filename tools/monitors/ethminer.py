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

import re
import time

from systemd import journal

import telegraf_output


def read_journal_line(live_journal):
    item = live_journal.get_previous()
    item_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return item_escape.sub('', item['MESSAGE'])


def get_line_item(live_journal, counter=0):
    while True:
        counter += 1
        item = read_journal_line(live_journal=live_journal)
        if 'speed' in item.lower():
            return item
        if counter >= 30:
            raise SystemExit('ERROR: ethminer is not reporting any new data')
        else:
            time.sleep(1)


j = journal.Reader()
j.log_level(journal.LOG_INFO)

j.add_match(_SYSTEMD_UNIT="ethminer.service")
j.seek_tail()

metric_data = dict()
gpu_info = metric_data['gpus'] = dict()
speed = metric_data['speed'] = dict()

item = get_line_item(live_journal=j)
metrics = item.split('  ')
for metric in metrics:
    if metric.lower().startswith('speed'):
        _, rate, rate_type = metric.split()
        speed['value'] = float(rate)
        speed['type'] = str(rate_type)
    elif metric.lower().startswith('gpu'):
        gpu, rate, temp, fan = metric.split()
        gpu_data = gpu_info[str(gpu.split('/')[-1])] = dict()
        gpu_data['rate'] = float(rate)
        gpu_data['temp'] = int(temp.lower().split('c')[0])
        gpu_data['fan'] = int(fan.split('%')[0])


timestamp = str(telegraf_output.current_time())
telegraf_output.write_telegraf(
    result=metric_data['speed'],
    metric_name='ethminer_speed_info',
    timestamp=timestamp
)
for k, v in metric_data['gpus'].items():
    telegraf_output.write_telegraf(
        result=v,
        metric_name='ethminer_rate_info',
        timestamp=timestamp,
        tag={'gpu': k}
    )
