# coding: utf-8
from datetime import datetime
from typing import Any
import re
from delta_trace_db.query.nodes.enum_node_type import EnumNodeType
from delta_trace_db.query.nodes.enum_value_type import EnumValueType
from delta_trace_db.query.util_field import UtilField


class FieldEquals:
    def __init__(self, field: str, value: Any, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        try:
            match self.v_type:
                case EnumValueType.auto_:
                    return f_value == self.value
                case EnumValueType.datetime_:
                    return datetime.fromisoformat(str(f_value)) == self.value
                case EnumValueType.int_:
                    return int(str(f_value)) == int(self.value)
                case EnumValueType.floatStrict_:
                    return float(str(f_value)) == float(self.value)
                case EnumValueType.floatEpsilon12_:
                    return abs(float(str(f_value)) - float(self.value)) < 1e-12
                case EnumValueType.boolean_:
                    return str(f_value).lower() == str(self.value).lower()
                case EnumValueType.string_:
                    return str(f_value) == str(self.value)
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.equals_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldNotEquals:
    def __init__(self, field: str, value, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        try:
            if self.v_type == EnumValueType.auto_:
                return f_value != self.value
            if self.v_type == EnumValueType.datetime_:
                return datetime.fromisoformat(str(f_value)) != self.value
            if self.v_type == EnumValueType.int_:
                return int(str(f_value)) != int(self.value)
            if self.v_type == EnumValueType.floatStrict_:
                return float(str(f_value)) != float(self.value)
            if self.v_type == EnumValueType.floatEpsilon12_:
                return abs(float(str(f_value)) - float(self.value)) >= 1e-12
            if self.v_type == EnumValueType.boolean_:
                return str(f_value).lower() != str(self.value).lower()
            if self.v_type == EnumValueType.string_:
                return str(f_value) != str(self.value)
            return False
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.notEquals_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldGreaterThan:
    def __init__(self, field: str, value, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        if f_value is None or self.value is None:
            return False
        try:
            if self.v_type == EnumValueType.datetime_:
                return datetime.fromisoformat(str(f_value)) > self.value
            if self.v_type == EnumValueType.int_:
                return int(str(f_value)) > int(self.value)
            if self.v_type == EnumValueType.floatStrict_:
                return float(str(f_value)) > float(self.value)
            if self.v_type == EnumValueType.floatEpsilon12_:
                return float(str(f_value)) - float(self.value) > 1e-12
            if self.v_type == EnumValueType.string_:
                return str(f_value) > str(self.value)
            if self.v_type == EnumValueType.auto_:
                return f_value > self.value
            if self.v_type == EnumValueType.boolean_:
                return False
            return False
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.greaterThan_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldLessThan:
    def __init__(self, field: str, value, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        if f_value is None or self.value is None:
            return False
        try:
            if self.v_type == EnumValueType.datetime_:
                return datetime.fromisoformat(str(f_value)) < self.value
            if self.v_type == EnumValueType.int_:
                return int(str(f_value)) < int(self.value)
            if self.v_type == EnumValueType.floatStrict_:
                return float(str(f_value)) < float(self.value)
            if self.v_type == EnumValueType.floatEpsilon12_:
                return float(self.value) - float(str(f_value)) > 1e-12
            if self.v_type == EnumValueType.string_:
                return str(f_value) < str(self.value)
            if self.v_type == EnumValueType.auto_:
                return f_value < self.value
            if self.v_type == EnumValueType.boolean_:
                return False
            return False
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.lessThan_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldGreaterThanOrEqual:
    def __init__(self, field: str, value, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        if f_value is None or self.value is None:
            return False
        try:
            if self.v_type == EnumValueType.datetime_:
                return not datetime.fromisoformat(str(f_value)) < self.value
            if self.v_type == EnumValueType.int_:
                return int(str(f_value)) >= int(self.value)
            if self.v_type == EnumValueType.floatStrict_:
                return float(str(f_value)) >= float(self.value)
            if self.v_type == EnumValueType.floatEpsilon12_:
                return float(str(f_value)) - float(self.value) >= -1e-12
            if self.v_type == EnumValueType.string_:
                return str(f_value) >= str(self.value)
            if self.v_type == EnumValueType.auto_:
                return f_value >= self.value
            if self.v_type == EnumValueType.boolean_:
                return False
            return False
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.greaterThanOrEqual_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldLessThanOrEqual:
    def __init__(self, field: str, value, v_type: EnumValueType = EnumValueType.auto_):
        self.field = field
        self.value = value
        if isinstance(value, datetime):
            self.v_type = EnumValueType.datetime_
        else:
            self.v_type = v_type

    @classmethod
    def from_dict(cls, src: dict):
        t = EnumValueType[src['vType']]
        val = datetime.fromisoformat(src['value']) if t == EnumValueType.datetime_ else src['value']
        return cls(src['field'], val, v_type=t)

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        if f_value is None or self.value is None:
            return False
        try:
            if self.v_type == EnumValueType.datetime_:
                return not datetime.fromisoformat(str(f_value)) > self.value
            if self.v_type == EnumValueType.int_:
                return int(str(f_value)) <= int(self.value)
            if self.v_type == EnumValueType.floatStrict_:
                return float(str(f_value)) <= float(self.value)
            if self.v_type == EnumValueType.floatEpsilon12_:
                return float(self.value) - float(str(f_value)) >= -1e-12
            if self.v_type == EnumValueType.string_:
                return str(f_value) <= str(self.value)
            if self.v_type == EnumValueType.auto_:
                return f_value <= self.value
            if self.v_type == EnumValueType.boolean_:
                return False
            return False
        except Exception:
            return False

    def to_dict(self) -> dict:
        val = self.value.isoformat() if isinstance(self.value, datetime) else self.value
        return {
            'type': EnumNodeType.lessThanOrEqual_.name,
            'field': self.field,
            'value': val,
            'vType': self.v_type.name,
            'version': '2',
        }


class FieldMatchesRegex:
    def __init__(self, field: str, pattern: str):
        self.field = field
        self.pattern = pattern

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], src['pattern'])

    def evaluate(self, data: dict) -> bool:
        value = UtilField.get_nested_field_value(data, self.field)
        if value is None:
            return False
        return re.search(self.pattern, str(value)) is not None

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.regex_.name,
            'field': self.field,
            'pattern': self.pattern,
            'version': '1',
        }


class FieldContains:
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], src['value'])

    def evaluate(self, data: dict) -> bool:
        v = UtilField.get_nested_field_value(data, self.field)
        if isinstance(v, (list, tuple, set)):
            return self.value in v
        if isinstance(v, str) and isinstance(self.value, str):
            return self.value in v
        return False

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.contains_.name,
            'field': self.field,
            'value': self.value,
            'version': '1',
        }


class FieldIn:
    def __init__(self, field: str, values: list):
        self.field = field
        self.values = values

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], list(src['values']))

    def evaluate(self, data: dict) -> bool:
        return UtilField.get_nested_field_value(data, self.field) in self.values

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.in_.name,
            'field': self.field,
            'values': self.values,
            'version': '1',
        }


class FieldNotIn:
    def __init__(self, field: str, values):
        self.field = field
        self.values = list(values)

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], list(src['values']))

    def evaluate(self, data: dict) -> bool:
        return UtilField.get_nested_field_value(data, self.field) not in self.values

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.notIn_.name,
            'field': self.field,
            'values': self.values,
            'version': '1',
        }


class FieldStartsWith:
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], src['value'])

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        return str(f_value).startswith(self.value) if f_value is not None else False

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.startsWith_.name,
            'field': self.field,
            'value': self.value,
            'version': '1',
        }


class FieldEndsWith:
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

    @classmethod
    def from_dict(cls, src: dict):
        return cls(src['field'], src['value'])

    def evaluate(self, data: dict) -> bool:
        f_value = UtilField.get_nested_field_value(data, self.field)
        return str(f_value).endswith(self.value) if f_value is not None else False

    def to_dict(self) -> dict:
        return {
            'type': EnumNodeType.endsWith_.name,
            'field': self.field,
            'value': self.value,
            'version': '1',
        }
