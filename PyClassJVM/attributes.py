import abc
import io
import struct

from .attribute_helpers import LineNumber, LocalVariable, LocalVariableType, InnerClass
from .flags import InnerClassAccessFlags


class Attribute(abc.ABC):
    def __init__(self, name, info):
        self.name = name
        self.info = info

    @classmethod
    @abc.abstractmethod
    def _parse(cls, name, fp, constant_pool):
        pass

    @classmethod
    def parse(cls, fp, constant_pool):
        name_index, attribute_length = struct.unpack(">HI", fp.read(6))
        name = constant_pool[name_index - 1]
        info = fp.read(attribute_length)

        for subclass in cls.__subclasses__():
            if subclass.__name__ == f"Attribute_{name.value}":
                return subclass._parse(name, io.BytesIO(info), constant_pool)

        return UnknownAttribute(name, info)


class UnknownAttribute(Attribute):
    @classmethod
    def _parse(cls, name, info):
        return cls(name, info)


class Attribute_ConstantValue(Attribute):
    def __init__(self, name, constant_value):
        self.name = name
        self.constant_value = constant_value

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        constant_value_index = struct.unpack(">H", fp.read(2))[0]
        constant_value = constant_pool[constant_value_index - 1]
        return cls(name, constant_value)


class Attribute_Code(Attribute):
    def __init__(self, name, max_stack, max_locals, code, exception_table, attributes):
        self.name = name
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.code = code
        self.exception_table = exception_table
        self.attributes = attributes

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        max_stack, max_locals, code_length = struct.unpack(">HHI", fp.read(8))
        code = fp.read(code_length)

        exception_table_length = struct.unpack(">H", fp.read(2))[0]

        exception_table = []
        for _ in range(exception_table_length):
            exception_table.append(struct.unpack(">HHHH", fp.read(8)))

        attributes_count = struct.unpack(">H", fp.read(2))[0]
        attributes = []

        for _ in range(attributes_count):
            attributes.append(Attribute.parse(fp, constant_pool))

        return cls(name, max_stack, max_locals, code, exception_table, attributes)


class Attribute_Exceptions(Attribute):
    def __init__(self, name, exception_index_table):
        self.name = name
        self.exception_index_table = exception_index_table

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        exception_index_table = []
        number_of_exceptions = struct.unpack(">H", fp.read(2))[0]
        for _ in range(number_of_exceptions):
            exception_index_table.append(struct.unpack(">H", fp.read(2))[0])

        return cls(name, exception_index_table)


class Attribute_InnerClasses(Attribute):
    def __init__(self, name, inner_classes):
        self.name = name
        self.inner_classes = inner_classes

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        inner_classes = []
        number_of_classes = struct.unpack(">H", fp.read(2))[0]
        for _ in range(number_of_classes):
            (
                inner_class_info_index,
                outer_class_info_index,
                inner_name_index,
                inner_class_access_flags,
            ) = struct.unpack(">HHHH", fp.read(8))
            inner_classes.append(
                InnerClass(
                    constant_pool[inner_class_info_index - 1],
                    constant_pool[outer_class_info_index - 1],
                    constant_pool[inner_name_index - 1],
                    InnerClassAccessFlags(inner_class_access_flags),
                )
            )

        return cls(name, inner_classes)


class Attribute_EnclosingMethod(Attribute):
    def __init__(self, name, class_, method):
        self.name = name
        self.class_ = class_
        self.method = method

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        class_index, method_index = struct.unpack(">HH", fp.read(4))
        return cls(
            name, constant_pool[class_index - 1], constant_pool[method_index - 1]
        )


class Attribute_Synthetic(Attribute):
    def __init__(self, name):
        self.name = name

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        return cls(name)


class Attribute_Signature(Attribute):
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        signature_index = struct.unpack(">H", fp.read(2))[0]
        signature = constant_pool[signature_index - 1]
        return cls(name, signature)


class Attribute_SourceFile(Attribute):
    def __init__(self, name, sourcefile):
        self.name = name
        self.sourcefile = sourcefile

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        sourcefile_index = struct.unpack(">H", fp.read(2))[0]
        sourcefile = constant_pool[sourcefile_index - 1]
        return cls(name, sourcefile)


class Attribute_SourceDebugExtension(Attribute):
    def __init__(self, name, debug_extension):
        self.name = name
        self.debug_extension = debug_extension

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        debug_extension = fp.read()
        return cls(name, debug_extension)


class Attribute_LineNumberTable(Attribute):
    def __init__(self, name, line_number_table):
        self.name = name
        self.line_number_table = line_number_table

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        line_number_table_length = struct.unpack(">H", fp.read(2))[0]

        line_number_table = []
        for _ in range(line_number_table_length):
            line_number_table.append(LineNumber(*struct.unpack(">HH", fp.read(4))))

        return cls(name, line_number_table)


class Attribute_LocalVariableTable(Attribute):
    def __init__(self, name, local_variable_table):
        self.name = name
        self.local_variable_table = local_variable_table

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        local_variable_table_length = struct.unpack(">H", fp.read(2))[0]

        local_variable_table = []
        for _ in range(local_variable_table_length):
            local_variable_table.append(
                LocalVariable(*struct.unpack(">HHHHH", fp.read(10)))
            )

        return cls(name, local_variable_table)


class Attribute_LocalVariableTypeTable(Attribute):
    def __init__(self, name, local_variable_type_table):
        self.name = name
        self.local_variable_type_table = local_variable_type_table

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        local_variable_type_table_length = struct.unpack(">H", fp.read(2))[0]

        local_variable_type_table = []
        for _ in range(local_variable_type_table_length):
            local_variable_type_table.append(
                LocalVariableType(*struct.unpack(">HHHHH", fp.read(10)))
            )
        return cls(name, local_variable_type_table)


class Attribute_Deprecated(Attribute):
    def __init__(self, name):
        self.name = name

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        return cls(name)


class Attribute_BootstrapMethods(Attribute):
    def __init__(self, name, bootstrap_methods):
        self.name = name
        self.bootstrap_methods = bootstrap_methods

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        num_bootstrap_methods = struct.unpack(">H", fp.read(2))[0]

        bootstrap_methods = []
        for _ in range(num_bootstrap_methods):
            (
                bootstrap_method_ref,
                num_bootstrap_arguments,
            ) = struct.unpack(">HH", fp.read(4))

            bootstrap_arguments = []
            for _ in range(num_bootstrap_arguments):
                bootstrap_arguments.append(
                    constant_pool[struct.unpack(">H", fp.read(2))[0] - 1]
                )

            bootstrap_methods.append(
                (constant_pool[bootstrap_method_ref - 1], bootstrap_arguments)
            )

        return cls(name, bootstrap_methods)


class Attribute_ModulePackages(Attribute):
    def __init__(self, name, package_index_table):
        self.name = name
        self.package_index_table = package_index_table

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        package_count = struct.unpack(">H", fp.read(2))[0]

        package_index_table = []
        for _ in range(package_count):
            package_index_table.append(
                constant_pool[struct.unpack(">H", fp.read(2))[0] - 1]
            )

        return cls(name, package_index_table)


class Attribute_ModuleMainClass(Attribute):
    def __init__(self, name, main_class):
        self.name = name
        self.main_class = main_class

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        main_class_index = struct.unpack(">H", fp.read(2))[0]
        return cls(name, constant_pool[main_class_index - 1])


class Attribute_NestHost(Attribute):
    def __init__(self, name, host_class):
        self.name = name
        self.host_class = host_class

    @classmethod
    def _parse(cls, name, fp, constant_pool):
        host_class_index = struct.unpack(">H", fp.read(2))[0]
        return cls(name, constant_pool[host_class_index - 1])
