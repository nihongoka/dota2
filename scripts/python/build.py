#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import json
import vccd
import vdf
import vpk
import zipfile
from glob import glob
import shutil

default = (lambda data: {"lang": {"Language": "japanese", "Tokens": data}})
def simple(key):
    return lambda data: {key: data}

files = [
    ('abilities', default),
    ('broadcastfacts', default),
    ('chat', default),
    ('dota', default),
    ('gameui', default),
    #('hero_chat_wheel', simple('hero_chat_wheel')),
    #('hero_lore', default),
    ('leagues', simple('leagues')),
    ('richpresence', default),
]

if os.path.exists('pak01/'):
    shutil.rmtree('pak01/')
os.makedirs('pak01/resource/localization', exist_ok=True)
os.makedirs('pak01/resource/subtitles', exist_ok=True)

for file in files:
    with open('main/resource/localization/' + file[0] + '_japanese.txt.json', 'r', encoding='utf-8') as jf:
        data = file[1](json.load(jf))
        with open('pak01/resource/localization/' + file[0] + '_japanese.txt', 'w', encoding='utf-8') as of:
            vdf.dump(data, of, pretty=True)

"""
for file in glob('main/resource/subtitles/*_japanese.dat.json'):
    with open(file, 'r', encoding='utf-8') as jf:
        cc = vccd.ClosedCaptions()
        cc.captions = json.load(jf, object_pairs_hook=OrderedDict)
        with open('pak01/' + file[5:-5], 'wb') as of:
            of.write(cc.dump())
"""

vpk.new('./pak01').save('pak01_dir.vpk')

with zipfile.ZipFile('dota2jp.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zip:
    zip.write('pak01_dir.vpk', arcname='game/dota_japanese/pak01_dir.vpk')
