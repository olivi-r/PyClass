class LineNumber:
    __slots__ = ("start_pc", "line_number")

    def __init__(self, start_pc, line_number):
        self.start_pc = start_pc
        self.line_number = line_number

    def __repr__(self):
        return f"LineNumber(start_pc={self.start_pc}, line_number={self.line_number})"


class LocalVariable:
    __slots__ = ("start_pc", "line_number", "name_index", "descriptor_index", "index")

    def __init__(self, start_pc, line_number, name_index, descriptor_index, index):
        self.start_pc = start_pc
        self.line_number = line_number
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.index = index

    def __repr__(self):
        return f"LocalVariable(start_pc={self.start_pc}, line_number={self.line_number}, name_index={self.name_index}, descriptor_index={self.descriptor_index}, index={self.index})"


class LocalVariableType:
    __slots__ = ("start_pc", "line_number", "name_index", "signature_index", "index")

    def __init__(self, start_pc, line_number, name_index, signature_index, index):
        self.start_pc = start_pc
        self.line_number = line_number
        self.name_index = name_index
        self.signature_index = signature_index
        self.index = index

    def __repr__(self):
        return f"LocalVariableType(start_pc={self.start_pc}, line_number={self.line_number}, name_index={self.name_index}, signature_index={self.signature_index}, index={self.index})"


class InnerClass:
    __slots__ = (
        "inner_class_info",
        "outer_class_info",
        "inner_name",
        "inner_class_access_flags",
    )

    def __init__(
        self, inner_class_info, outer_class_info, inner_name, inner_class_access_flags
    ):
        self.inner_class_info = inner_class_info
        self.outer_class_info = outer_class_info
        self.inner_name = inner_name
        self.inner_class_access_flags = inner_class_access_flags

    def __repr__(self):
        return f"InnerClass(inner_class_info={self.inner_class_info}, outer_class_info={self.outer_class_info}, inner_name={self.inner_name}, inner_class_access_flags={self.inner_class_access_flags})"
