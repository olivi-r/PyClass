import abc
import struct


class CONSTANT(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def _serialize(self):
        pass

    @classmethod
    @abc.abstractmethod
    def _parse(cls, fp):
        pass

    def serialize(self):
        return struct.pack(">B", self._tag) + self._serialize()

    @staticmethod
    def parse(fp):
        tag = fp.read(1)[0]
        for subclass in CONSTANT.__subclasses__():
            if subclass._tag == tag:
                return subclass._parse(fp)

        raise ValueError(f"Unknown tag: {tag}")


class CONSTANT_Class(CONSTANT):
    _tag = 7

    def __init__(self, name):
        self.name = name

    def _serialize(self):
        return struct.pack(">H", self.name)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">H", fp.read(2)))


class _CONSTANT_interface_0:
    def __init__(self, class_, name_and_type):
        self.class_ = class_
        self.name_and_type = name_and_type

    def _serialize(self):
        return struct.pack(">HH", self.class_, self.name_and_type)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">HH", fp.read(4)))


class CONSTANT_Fieldref(_CONSTANT_interface_0, CONSTANT):
    _tag = 9


class CONSTANT_Methodref(_CONSTANT_interface_0, CONSTANT):
    _tag = 10


class CONSTANT_InterfaceMethodref(_CONSTANT_interface_0, CONSTANT):
    _tag = 11


class CONSTANT_String(CONSTANT):
    _tag = 8

    def __init__(self, string):
        self.string = string

    def _serialize(self):
        return struct.pack(">H", self.string)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">H", fp.read(2)))


class CONSTANT_Integer(CONSTANT):
    _tag = 3

    def __init__(self, value):
        self.value = value

    def _serialize(self):
        return struct.pack(">I", self.value)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">I", fp.read(4)))


class CONSTANT_Float(CONSTANT):
    _tag = 4

    def __init__(self, bytes):
        self.bytes = bytes

    def _serialize(self):
        return struct.pack(">I", self.bytes)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">I", fp.read(4)))


class CONSTANT_Long(CONSTANT):
    _tag = 5

    def __init__(self, value):
        self.value = value

    def _serialize(self):
        return struct.pack(">Q", self.value)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">Q", fp.read(8)))


class CONSTANT_Double(CONSTANT):
    _tag = 6

    def __init__(self, high_bytes, low_bytes):
        self.high_bytes = high_bytes
        self.low_bytes = low_bytes

    def _serialize(self):
        return struct.pack(">II", self.bytes)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">II", fp.read(8)))


class CONSTANT_NameAndType(CONSTANT):
    _tag = 12

    def __init__(self, name, descriptor):
        self.name = name
        self.descriptor = descriptor

    def _serialize(self):
        return struct.pack(">HH", self.name, self.descriptor)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">HH", fp.read(4)))


class CONSTANT_Utf8(CONSTANT):
    _tag = 1

    def __init__(self, value):
        self.value = value

    def _serialize(self):
        value = self.value.encode("utf-8")
        return struct.pack(">H", len(value)) + value

    @classmethod
    def _parse(cls, fp):
        length = struct.unpack(">H", fp.read(2))[0]
        return cls(fp.read(length).decode("utf-8"))


class CONSTANT_MethodHandle(CONSTANT):
    _tag = 15

    def __init__(self, reference_kind, reference):
        self.reference_kind = reference_kind
        self.reference = reference

    def _serialize(self):
        return struct.pack(">BH", self.reference_kind, self.reference)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">BH", fp.read(3)))


class CONSTANT_MethodType(CONSTANT):
    _tag = 16

    def __init__(self, descriptor):
        self.descriptor = descriptor

    def _serialize(self):
        return struct.pack(">H", self.descriptor)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">H", fp.read(2)))


class CONSTANT_InvokeDynamic(CONSTANT):
    _tag = 18

    def __init__(self, bootstrap_method_attr, name_and_type):
        self.bootstrap_method_attr = bootstrap_method_attr
        self.name_and_type = name_and_type

    def _serialize(self):
        return struct.pack(">HH", self.bootstrap_method_attr, self.name_and_type)

    @classmethod
    def _parse(cls, fp):
        return cls(*struct.unpack(">HH", fp.read(4)))
