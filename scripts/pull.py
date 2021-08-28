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

def remove_special_key(tokens):
    del tokens['DOTA_GiftedItems']
    del tokens['DOTA_GifterText_Random']
    del tokens['DOTA_GifterText_All']
    del tokens['DOTA_GifterText_SelfOpen']
    del tokens['DOTA_GifterText_Title']

files = [
    ('abilities', default, None),
    ('broadcastfacts', default, None),
    ('chat', default, None),
    ('dota', default, remove_special_key),
    ('gameui', default, None),
#    ('hero_chat_wheel', simple('hero_chat_wheel'), None),
#    ('hero_lore', default, None),
#   huge
#   ('items', default),
    ('leagues', simple('leagues'), None),
    ('richpresence', default, None),
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
        if file[2]:
            file[2](tokens)
        with open('main/resource/localization/' + file[0] + '_english' + '.txt.json', 'w', encoding="utf-8") as fw:
            json.dump(tokens, fw, indent=4, ensure_ascii=False)

