from typing import Dict
import vpk
import vdf
import json
import os
import vccd

DOTA2_CLIENT = os.getenv('DOTA2_CLIENT')
if not DOTA2_CLIENT:
    DOTA2_CLIENT = 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/'

class L10nRule:
    name = ''
    is_simple = False

    def __init__(self, name: str, is_simple: bool):
        self.name = name
        self.is_simple = is_simple
    
    def pull(self, data) -> Dict[str, str]:
        if self.is_simple:
            return data[self.name]
        else:
            return data['lang']['Tokens']

    def get_pak_path(self, lang: str) -> str:
        return f'resource/localization/{self.name}_{lang}.txt'

def remove_special_key(data: Dict[str, str]):
    keys = [
        'DOTA_GiftedItems',
        'DOTA_GifterText_Random',
        'DOTA_GifterText_All',
        'DOTA_GifterText_SelfOpen',
        'DOTA_GifterText_Title',
    ]
    for key in keys:
        if key in data:
            del data[key]

l10ns = [
    L10nRule('abilities', False),
    L10nRule('chat', False),
    L10nRule('dota', False),
    L10nRule('gameui', False),
    L10nRule('leagues', True),
    L10nRule('richpresence', False),
]

def detect_encoding(filename):
    with open(filename, 'rb') as f:
        if b'\xef\xbb\xbf' == f.read(3):
            return 'utf-8-sig'
        return 'utf-8'

def main():
    def main_version():
        head = 'ClientVersion='
        with open(DOTA2_CLIENT+'game/dota/steam.inf', 'r') as inf:
            while True:
                line = inf.readline().strip()
                if line:
                    if line.startswith(head):
                        with open('./version', 'w') as version:
                            version.write(line[len(head):])
                            return
                else:
                    raise Exception('Not found ClientVersion in steam.inf file.')
    main_version()

    os.makedirs('localization', exist_ok=True)

    with vpk.open(DOTA2_CLIENT+'game/dota/pak01_dir.vpk') as pak01:
        for rule in l10ns:
            with pak01.get_file(rule.get_pak_path('english')) as input:
                data = rule.pull(vdf.loads(input.read().decode('utf-8')))
                remove_special_key(data)
                out_name = f'main/resource/localization/{rule.name}_english.txt.json'
                with open(out_name, 'w', encoding='utf-8') as out:
                    json.dump(data, out, indent=4, ensure_ascii=False)
                    print(f'Wrote "{out_name}" done!!')

        with open('vo.txt', 'r') as vof:
            for vo in vof.readlines():
                vo = vo.strip()
                if len(vo) == 0:
                    continue
                with pak01.get_file(f'resource/subtitles/subtitles_{vo}_english.dat') as dat:
                    keys = []
                    for fn in pak01:
                        if not fn.startswith(f'sounds/vo/{vo}/'):
                            continue
                        fn = fn.removeprefix('sounds/vo/').removesuffix('.vsnd_c').replace('/', '_')
                        keys.append(fn)
                    data = vccd.load(dat.read(), keys=keys).captions
                    out_name = f'main/resource/subtitles/subtitles_{vo}_english.dat.json'
                    with open(out_name, 'w', encoding='utf-8') as out:
                        json.dump(data, out, indent=4, ensure_ascii=False)
                        print(f'Wrote "{out_name}" done!!')

    with open('addons.json', 'r') as addons:
        for addon in json.load(addons):
            filename = DOTA2_CLIENT + f'game/dota_addons/' + addon['name']
            with open(filename, encoding='utf-8') as input:
                data = vdf.loads(input.read())
                if addon['is_simple']:
                    data = data[addon['key_name']]
                else:
                    data = data['lang']['Tokens']
                os.makedirs(os.path.dirname('addons/' + addon['name']), exist_ok=True)
                out_name = 'addons/' + addon['name'] + '.json'
                with open(out_name, 'w', encoding='utf-8') as out:
                    json.dump(data, out, indent=4, ensure_ascii=False)
                    print(f'Wrote "{out_name}" done!!')

if __name__ == '__main__':
    main()