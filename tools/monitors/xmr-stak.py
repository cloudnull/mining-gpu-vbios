#!/usr/bin/env python

import httplib
import json

import telegraf_output

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 16000

conn = httplib.HTTPConnection(host=HTTP_HOST, port=HTTP_PORT)
try:
    conn.request('GET', '/api.json')
except httplib.BadStatusLine:
    raise SystemExit('Connection Failure')
else:
    resp = conn.getresponse()
    json_data = json.loads(resp.read())
finally:
    conn.close()

metric_data = dict()

miner = metric_data['miner'] = dict()
shares = miner[json_data['version'].split('/')[0]] = dict()
shares['uptime'] = float(json_data['connection']['uptime'])
shares['pool'] = json_data['connection']['pool']

result = json_data['hashrate']

try:
    shares['shares_good'] = float(json_data['results']['shares_good'])
except IndexError:
    shares['shares_good'] = float(0)

try:
    shares['shares_total'] = float(json_data['results']['shares_total'])
except IndexError:
    shares['shares_total'] = float(0)

try:
    shares['hashes_total'] = float(json_data['results']['hashes_total'])
except IndexError:
    shares['hashes_total'] = float(0)

sec10, sec60, min15 = json_data['hashrate']['total']

speed = metric_data['speed'] = dict()
speed['value'] = float(sec10 or 0)
speed['type'] = 'H/s'

thread_info = metric_data['threads'] = dict()
thread_hash_rate = json_data['hashrate']['threads']
count = 0
for ghr in thread_hash_rate:
    thread_data = thread_info['thread_%s' % count] = dict()
    thread_data['rate'] = float(ghr[0] or 0)
    count += 1

timestamp = str(telegraf_output.current_time())
telegraf_output.write_telegraf(
    result=metric_data['speed'],
    metric_name='xmrminer_speed_info',
    timestamp=timestamp
)
for k, v in metric_data['miner'].items():
    telegraf_output.write_telegraf(
        result=v,
        metric_name='xmrminer_%s' % k,
        timestamp=timestamp
    )
for k, v in metric_data['threads'].items():
    telegraf_output.write_telegraf(
        result=v,
        metric_name='xmrminer_rate_info',
        timestamp=timestamp,
        tag={'thread': k}
    )
