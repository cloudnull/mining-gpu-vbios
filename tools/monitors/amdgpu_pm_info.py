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

import os
import json

import telegraf_output


DRI_PATH = "/sys/kernel/debug/dri"

DRI_AMD_PM_INFO = list()

for path, _, files in os.walk(DRI_PATH):
    if 'amdgpu_pm_info' in files:
        DRI_AMD_PM_INFO.append([os.path.basename(path), os.path.join(path, 'amdgpu_pm_info')])

metric_data = dict()
for dri, dri_file in DRI_AMD_PM_INFO:
    item = metric_data[dri] = dict()

    with open(dri_file) as f:
        dri_file_open = f.read()

    flags, clocks_n_power, temp_n_load, opt1, opt2 = [i for i in dri_file_open.split('\n\n') if i]

    flag_items = item['flags'] = dict()
    for flag in flags.splitlines():
        k, v = flag.strip().split(':')
        v = v.strip()
        if v.isalpha:
            if v.lower() == 'on':
                v = True
            elif v.lower() == 'off':
                v = False

        flag_items[k.strip()] = v

    cp_items = item['clocks_n_power'] = dict()
    for cnp in clocks_n_power.splitlines():
        if ':' in cnp:
            continue

        for cp in cnp.split('\t'):
            if cp:
                cp_value, cp_type, cp_name = cp.strip().split(' ', 2)
                cp_name = cp_name.lstrip('(').rstrip(')')
                cp_func = cp_items[cp_name] = dict()
                cp_func['type'] = cp_type
                try:
                    cp_func['value'] = float(cp_value)
                except ValueError:
                    cp_func['value'] = cp_value

    tl_items = item['temp_n_load'] = dict()
    for tnp in temp_n_load.splitlines():
        tnp_name, value = tnp.split(':')
        tnp_value, tnp_type = value.strip().split()
        tnp_func = tl_items[tnp_name.strip()] = dict()
        tnp_func['type'] = tnp_type
        try:
            tnp_func['value'] = float(tnp_value)
        except ValueError:
            tnp_func['value'] = tnp_value

timestamp = str(telegraf_output.current_time())
for k, v in metric_data.items():
    for _k, _v in v.items():
        if _k == 'flags':
            telegraf_output.write_telegraf(
                result=_v,
                metric_name='amdgpu_pm_info_%s' % _k,
                timestamp=timestamp,
                tag={'gpu': k}
            )
        else:
            resultant = dict()
            for __k, __v in _v.items():
                name = '%s_%s' % (__k, __v['type'])
                resultant[name.lower()] = __v['value']

            telegraf_output.write_telegraf(
                result=resultant,
                metric_name=_k,
                timestamp=timestamp,
                tag={'gpu': k}
            )