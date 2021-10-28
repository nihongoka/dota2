from struct import unpack_from
from typing import List
from .closed_captions import ClosedCaptions, _MAGIC
from .crc import _crc_hash

def load(f:bytes, keys:List[str]=[]) -> ClosedCaptions:
    result = ClosedCaptions()
    (magic,) = unpack_from('<I', f)
    if magic != _MAGIC:
        raise Exception('This is not VCCD file')
    (version, num_block, block_size, dir_size, data_offset) = unpack_from('<IIIII', f, 4)
    if version != 2:
        raise Exception('Unsupported VCCD version')
    
    result.version = version
    result.raw_key = not bool(keys)
    result.block_size = block_size

    keys_dict = {}
    if keys:
        keys_dict = dict(map(lambda x:(_crc_hash(x), x), keys))

    kp = 24 # key pointer
    for _ in range(dir_size):
        (hash, text_hash, block_num, offset, length) = unpack_from('<IIIHH', f, kp)
        kp = kp + 16
        tp = data_offset + (block_num * block_size) + offset # text pointer
        text = f[tp:tp + length].decode('utf-16-le')
        text = text[:-1]
        key = str(hash)
        if keys_dict:
            if hash in keys_dict:
                key = keys_dict[hash]
            else:
                continue
        result.captions[key] = text
    return result
