#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import vdf
import vpk
import zipfile
import shutil

format_default = (lambda data: {"lang": {"Language": "japanese", "Tokens": data}})


def format_simple(key):
    return lambda data: {key: data}


files = [
    ('abilities', format_default),
    ('broadcastfacts', format_default),
    ('chat', format_default),
    ('dota', format_default),
    ('gameui', format_default),
    # ('hero_chat_wheel', format_simple('hero_chat_wheel')),
    # ('hero_lore', format_default),
    ('leagues', format_simple('leagues')),
    ('richpresence', format_default),
    ('teamfandom', format_default)
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
    info = zipfile.ZipInfo()
    info.filename = 'game/dota_japanese/pak01_dir.vpk'
    with open('pak01_dir.vpk', 'rb') as pak01:
        zip.writestr(info, pak01.read())

    with open('addons.json', 'r') as addons:
        for addon in json.load(addons):
            name = addon['name'].replace('english', 'japanese')
            info = zipfile.ZipInfo()
            info.filename = 'game/dota_addons/' + name
            with open('addons/' + name + '.json', 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                if addon['is_simple']:
                    data = format_simple(addon['key_name'])(data)
                else:
                    data = format_default(data)
                zip.writestr(info, vdf.dumps(data, pretty=True))
