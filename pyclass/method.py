import struct

from .attributes import Attribute
from .flags import MethodAccessFlags


class Method:
    def __init__(self, access_flags, name, descriptor, attributes):
        self.access_flags = access_flags
        self.name = name
        self.descriptor = descriptor
        self.attributes = attributes

    @staticmethod
    def parse(fp, constant_pool):
        (
            access_flags,
            name_index,
            descriptor_index,
            attributes_count,
        ) = struct.unpack(">HHHH", fp.read(8))

        access_flags = MethodAccessFlags(access_flags)

        attributes = []
        for _ in range(attributes_count):
            attributes.append(Attribute.parse(fp, constant_pool))

        name = constant_pool[name_index - 1]
        descriptor = constant_pool[descriptor_index - 1]
        return Method(access_flags, name, descriptor, attributes)
