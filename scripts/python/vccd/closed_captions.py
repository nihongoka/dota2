from collections import OrderedDict
from io import BytesIO
from typing import List
from struct import pack

from .crc import _crc_hash


_MAGIC = 0x44434356  # VCCD


class ClosedCaptions():
    def __init__(self):
        self.version = 2
        self.raw_key = False
        self.block_size = 8192
        self.captions = OrderedDict[str, str]()

    def dump(self) -> bytes:
        buf = BytesIO()
        blocks: List[BytesIO] = [BytesIO()]
        block = blocks[0]
        block_num = 0
        block_size = 0  # current
        offset = 0

        buf.write(pack('<IIIIII', _MAGIC, self.version, 0, self.block_size, len(self.captions), 0))

        for key, text in self.captions.items():
            if key is not str or text is not str:
                raise Exception()
            text += '\0'
            text_data = text.encode('utf-16-le')
            length = len(text_data)
            if block_size + length > self.block_size:
                block = BytesIO()
                blocks.append(block)
                block_num += 1
                block_size = 0
                offset = 0
            block_size += block.write(text_data)

            buf.write(pack('<I', int(key, 16) if self.raw_key else _crc_hash(key)))
            buf.write(pack('<I', _crc_hash(text_data)))
            buf.write(pack('<IHH', block_num, offset, length))

            offset += length

        data_offset = buf.tell()

        for block in blocks:
            block.seek(0)
            size = buf.write(block.read())
            buf.write(b'\0' * (self.block_size - size))

        buf.seek(8)
        buf.write(pack('<I', len(blocks)))
        buf.seek(20)
        buf.write(pack('<I', data_offset))
        buf.seek(0)

        return buf.read()
