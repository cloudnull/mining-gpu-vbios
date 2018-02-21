#!/usr/bin/env python

import socket
import json

import telegraf_output

TCP_IP = '127.0.0.1'
TCP_PORT = 3333
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
    s.send('{"id": 0,"jsonrpc": "2.0","method": "miner_getstat1"}')
except Exception:
    raise SystemExit('Socket Failed to connect')
else:
    data = s.recv(BUFFER_SIZE)
finally:
    s.close()

json_data = json.loads(data)
result = json_data['result']

metric_data = dict()

uptime = metric_data['uptime'] = dict()
uptime['value'] = float(result[1])
uptime['type'] = 'Minutes'

speed = metric_data['speed'] = dict()
speed['value'] = float(int(result[2].split(';')[0]) / 1024)
speed['type'] = 'MH/s'

valid_shares = metric_data['valid_shares'] = dict()
valid_shares['type'] = 'shares'
try:
    valid_shares['value'] = float(result[2].split(';')[1])
except IndexError:
    valid_shares['value'] = float(0)

rejected_shares = metric_data['rejected_shares'] = dict()
rejected_shares['type'] = 'shares'
try:
    rejected_shares['value'] = float(result[2].split(';')[2])
except IndexError:
    rejected_shares['value'] = float(0)

gpu_info = metric_data['gpus'] = dict()
gpu_hash_rate = result[3].split(';')
count = 0
for ghr in gpu_hash_rate:
    gpu_data = gpu_info['eth_gpu_%s' % count] = dict()
    gpu_data['rate'] = float(ghr) / 1024
    count += 1

fsts = result[6].split(';')
fan_speed_temp = [";".join(fsts[i:i+2]) for i in range(0, len(fsts), 2)]
count = 0
for fst in fan_speed_temp:
    gpu_data = gpu_info['eth_gpu_%s' % count]
    temp, fan = fst.split(';')
    gpu_data['temp'] = int(temp)
    gpu_data['fan'] = int(fan)
    count += 1

invalid_shares = metric_data['invalid_shares'] = dict()
invalid_shares['type'] = 'shares'
try:
    valid_shares['value'] = float(result[9].split(';')[0])
except IndexError:
    valid_shares['value'] = float(0)

invalid_shares = metric_data['eth_pool_switches'] = dict()
invalid_shares['type'] = 'pool_switches'
try:
    valid_shares['value'] = float(result[9].split(';')[1])
except IndexError:
    valid_shares['value'] = float(0)

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
