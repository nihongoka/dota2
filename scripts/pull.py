#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import urllib.request
import vdf
import os.path
import pathlib
import json

base_url = 'https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/resource/localization/'

def default(data):
    return data['lang']['Tokens']

def simple(key):
    return lambda data: data[key]

files = [
    ('abilities', default),
    ('broadcastfacts', default),
    ('chat', default),
    ('dota', default),
    ('gameui', default),
    ('hero_chat_wheel', simple('hero_chat_wheel')),
    ('hero_lore', default),
#   huge
#   ('items', default),
    ('leagues', simple('leagues')),
    ('richpresence', default),
#   useless?
#   ('patchnotes/patchnotes', simple('patch')),
]

os.makedirs('localization/patchnotes', exist_ok=True)

# ダウンロード
for file in files:
    print(file[0])
    url = base_url + file[0] + '_english' + '.txt'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        data = vdf.loads(res.read().decode())
        tokens = file[1](data)
        with open('localization/' + file[0] + '_english' + '.json', 'w') as fw:
            json.dump(tokens, fw, indent=4)
