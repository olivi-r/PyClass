import struct


class Attribute:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    @classmethod
    def parse(cls, fp, constant_pool):
        name_index, attribute_length = struct.unpack(">HI", fp.read(6))
        name = constant_pool[name_index - 1]
        info = fp.read(attribute_length)
        return cls(name, info)
