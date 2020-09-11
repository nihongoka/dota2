#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request

url = 'https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/steam.inf'

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as res:
    inf = res.read().decode().split('\n')[0]
    prefix = 'ClientVersion='
    if inf.startswith(prefix):
        version = int(inf[len(prefix):])
        with open('version', 'w') as f:
            f.write(str(version))
