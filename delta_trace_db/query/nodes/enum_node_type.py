# coding: utf-8
from enum import Enum, auto

class EnumNodeType(Enum):
    # 論理演算ノード (構造的に条件を組み立てる)
    and_ = auto()
    or_ = auto()
    not_ = auto()

    # 比較/条件ノード (フィールド値に対して条件を設定)
    equals_ = auto()
    notEquals_ = auto()
    greaterThan_ = auto()
    lessThan_ = auto()
    greaterThanOrEqual_ = auto()
    lessThanOrEqual_ = auto()
    regex_ = auto()
    contains_ = auto()
    in_ = auto()
    notIn_ = auto()
    startsWith_ = auto()
    endsWith_ = auto()
