from collections import OrderedDict
import json
import glob

for fnj in glob.glob('**/*_japanese.txt.json', recursive=True):
    fne = fnj.replace('_japanese.txt.json', '_english.txt.json')
    with open(fnj, 'r', encoding='utf-8') as fj, open(fne, 'r', encoding='utf-8') as fe:
        jdata = json.load(fj, object_pairs_hook=OrderedDict)
        edata = json.load(fe)
        updated = False
        for key in list(jdata.keys()):
            if key not in edata:
                del jdata[key]
                updated = True
        if updated:
            print('Updating', fnj)
            with open(fnj, 'w', encoding='utf-8') as fj:
                json.dump(jdata, fj, ensure_ascii=False, indent=4)
