#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import urllib.request
import vdf
import os.path
import pathlib
import json

base_url = 'https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/resource/localization/'
files = [
    'abilities',
    'broadcastfacts',
    'chat',
    'dota',
    'gameui',
#    'hero_chat_wheel', TODO: support later
    'hero_lore',
    'items',
#    'leagues', TODO: support later
    'richpresence',
#    'patchnotes/patchnotes', TODO: support later
]

os.makedirs('localization/patchnotes', exist_ok=True)

# ダウンロード
for file in files:
    print(file)
    url = base_url + file + '_english' + '.txt'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        tokens = vdf.loads(res.read().decode())['lang']['Tokens']
        with open('localization/' + file + '_english' + '.json', 'w') as fw:
            json.dump(tokens, fw, indent=4)
