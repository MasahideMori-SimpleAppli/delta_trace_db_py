from abc import ABC, abstractmethod
from typing import Any, Dict
from deltatracedb.query.nodes.enum_node_type import EnumNodeType
from deltatracedb.query.nodes.logical_node import AndNode, OrNode, NotNode
from deltatracedb.query.nodes.comparison_node import FieldEquals, FieldNotEquals, FieldGreaterThan, FieldLessThan, \
    FieldGreaterThanOrEqual, FieldLessThanOrEqual, FieldMatchesRegex, FieldContains, FieldStartsWith, FieldEndsWith, \
    FieldIn, FieldNotIn


class QueryNode(ABC):
    """Base class for query nodes.

    (en) Returns True if the object matches the calculation.
    (ja) 計算と一致するオブジェクトだった場合はTrueを返します。
    """

    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> bool:
        """Evaluate the node against a data dictionary."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        pass

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "QueryNode":
        """Restore a QueryNode object from a dictionary."""
        node_type = EnumNodeType[src["type"]]

        if node_type == EnumNodeType.and_:
            return AndNode.from_dict(src)
        elif node_type == EnumNodeType.or_:
            return OrNode.from_dict(src)
        elif node_type == EnumNodeType.not_:
            return NotNode.from_dict(src)
        elif node_type == EnumNodeType.equals_:
            return FieldEquals.from_dict(src)
        elif node_type == EnumNodeType.notEquals_:
            return FieldNotEquals.from_dict(src)
        elif node_type == EnumNodeType.greaterThan_:
            return FieldGreaterThan.from_dict(src)
        elif node_type == EnumNodeType.lessThan_:
            return FieldLessThan.from_dict(src)
        elif node_type == EnumNodeType.greaterThanOrEqual_:
            return FieldGreaterThanOrEqual.from_dict(src)
        elif node_type == EnumNodeType.lessThanOrEqual_:
            return FieldLessThanOrEqual.from_dict(src)
        elif node_type == EnumNodeType.regex_:
            return FieldMatchesRegex.from_dict(src)
        elif node_type == EnumNodeType.contains_:
            return FieldContains.from_dict(src)
        elif node_type == EnumNodeType.in_:
            return FieldIn.from_dict(src)
        elif node_type == EnumNodeType.notIn_:
            return FieldNotIn.from_dict(src)
        elif node_type == EnumNodeType.startsWith_:
            return FieldStartsWith.from_dict(src)
        elif node_type == EnumNodeType.endsWith_:
            return FieldEndsWith.from_dict(src)
        else:
            raise ValueError(f"Unknown node type: {node_type}")
