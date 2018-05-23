#!/usr/bin/env python3

import sys,yaml
from string import Template


def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item):
      return item

inp = """\

rig:
    name: rig

coins:
    - zec:
        wallet: t1UzAvKXK6iiLZHPxzVTDZKuJ4juJbpVVcA
        pool:
          server: eu1-zcash.flypool.org
          port: 3333
          pwd: 2000
  
miners:
    - ewbf:
        path:  ".local/bin/ewbf-v0.3.4b"
        bin:    miner
        template: "--server $server --port $port --user $wallet --pass $pwd --eexit 1 --templimit 75 --fee 0" 

task:
    coin: zec
    miner: ewbf
"""

cfg = yaml.load(inp)
minerId = cfg['task']['miner']
coinId = cfg['task']['coin']

coin = find(lambda c: coinId in c, cfg['coins'])[coinId]

wallet = coin['wallet']
pool = coin['pool']
server = pool['server']
port = pool['port']
pwd = pool['pwd']

miner = find(lambda m: minerId in m, cfg['miners'])[minerId]
minerTemplate = miner['template']
args = Template(minerTemplate).substitute(
  server=server, port=port, wallet=wallet, pwd=pwd
)

"""
coin = cfg['coins'].f
wallet = coin['wallet']
pool = coin['pools'][0]
server = pool['server']
port = pool['port']
pwd = pool['pwd']

minerId = cfg['task']['miner']
miner = cfg['miners'][minerId]
minerFmt = str(miner['format'])
"""

print(args)