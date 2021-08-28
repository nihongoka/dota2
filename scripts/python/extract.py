from typing import Dict
import vpk
import vdf
import json
import os

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

def main():
    def main_version():
        head = 'ClientVersion='
        with open('C:/dota2/game/dota/steam.inf', 'r') as inf:
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

    with vpk.open('C:/dota2/game/dota/pak01_dir.vpk') as pak01:
        for rule in l10ns:
            with pak01.get_file(rule.get_pak_path('english')) as input:
                data = rule.pull(vdf.loads(input.read().decode('utf-8')))
                remove_special_key(data)
                out_name = f'main/resource/localization/{rule.name}_english.txt.json'
                with open(out_name, 'w', encoding='utf-8') as out:
                    json.dump(data, out, indent=4, ensure_ascii=False)
                    print(f'Wrote "{out_name}" done!!')

if __name__ == '__main__':
    main()