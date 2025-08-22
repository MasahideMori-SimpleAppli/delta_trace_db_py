# coding: utf-8
from enum import Enum, auto

class EnumValueType(Enum):
    auto_ = auto()            # default
    datetime_ = auto()
    int_ = auto()
    floatStrict_ = auto()
    floatEpsilon12_ = auto()  # Tolerance 1e-12
    boolean_ = auto()
    string_ = auto()
