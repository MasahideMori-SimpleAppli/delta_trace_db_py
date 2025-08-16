from typing import Any, Callable, Dict
from deltatracedb.query.sort.abstract_sort import AbstractSort
from deltatracedb.query.util_field import UtilField


class SingleSort(AbstractSort):
    """Single-key sorting for query results.

    (ja) クエリの戻り値について、単一キーでのソートを指定するためのクラスです。
    """

    class_name = "SingleSort"
    version = "2"

    def __init__(self, field: str, is_reversed: bool = False):
        self.field = field
        self.is_reversed = is_reversed

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "SingleSort":
        field = src["field"]
        is_reversed = src.get("reversed", False)
        return cls(field=field, is_reversed=is_reversed)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "field": self.field,
            "reversed": self.is_reversed,  # 外部的には"reversed"キーのまま
        }

    def get_comparator(self) -> Callable[[Dict[str, Any], Dict[str, Any]], int]:
        def comparator(a: Dict[str, Any], b: Dict[str, Any]) -> int:
            a_value = UtilField.get_nested_field_value(a, self.field)
            b_value = UtilField.get_nested_field_value(b, self.field)

            if a_value is None and b_value is None:
                return 0
            if a_value is None:
                return -1 if self.is_reversed else 1
            if b_value is None:
                return 1 if self.is_reversed else -1

            if isinstance(a_value, bool) and isinstance(b_value, bool):
                result = (a_value > b_value) - (a_value < b_value)
            elif isinstance(a_value, (int, float, str)) and isinstance(b_value, (int, float, str)):
                result = (a_value > b_value) - (a_value < b_value)
            else:
                raise TypeError(
                    f'Field "{self.field}" is not comparable: {a_value} ({type(a_value)}), {b_value} ({type(b_value)})'
                )

            return -result if self.is_reversed else result

        return comparator
