import struct

from .attributes import Attribute
from .cp_info import CONSTANT
from .field_info import Field
from .flags import ClassAccessFlags
from .method import Method


class ClassFile:
    def __init__(
        self,
        major_version,
        minor_version,
        constant_pool,
        access_flags,
        this_class,
        super_class,
        interfaces,
        fields,
        methods,
        attributes,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.constant_pool = constant_pool
        self.access_flags = access_flags
        self.this_class = this_class
        self.super_class = super_class
        self.interfaces = interfaces
        self.fields = fields
        self.methods = methods
        self.attributes = attributes

    @classmethod
    def parse(cls, fp):
        (
            magic,
            minor_version,
            major_version,
            constant_pool_count,
        ) = struct.unpack(">IHHH", fp.read(10))
        assert magic == 0xCAFEBABE

        constant_pool = []
        for _ in range(constant_pool_count - 1):
            constant_pool.append(CONSTANT.parse(fp))

        (
            access_flags,
            this_class,
            super_class,
            interfaces_count,
        ) = struct.unpack(">HHHH", fp.read(8))

        access_flags = ClassAccessFlags(access_flags)
        this_class = constant_pool[this_class - 1]
        super_class = constant_pool[super_class - 1]

        interfaces = []
        for _ in range(interfaces_count):
            interfaces.append(struct.unpack(">H", fp.read(2)))

        fields_count = struct.unpack(">H", fp.read(2))[0]
        fields = []
        for _ in range(fields_count):
            fields.append(Field.parse(fp, constant_pool))

        methods_count = struct.unpack(">H", fp.read(2))[0]
        methods = []
        for _ in range(methods_count):
            methods.append(Method.parse(fp, constant_pool))

        attributes_count = struct.unpack(">H", fp.read(2))[0]
        attributes = []
        for _ in range(attributes_count):
            attributes.append(Attribute.parse(fp, constant_pool))

        return cls(
            major_version,
            minor_version,
            constant_pool,
            access_flags,
            this_class,
            super_class,
            interfaces,
            fields,
            methods,
            attributes,
        )
