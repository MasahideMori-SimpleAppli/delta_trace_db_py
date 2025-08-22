# coding: utf-8
from typing import TypeVar, Generic, List, Dict, Callable, Any
from dummy_modules import QueryExecutionResult, EnumQueryType, UtilCopy

T = TypeVar('T')

class QueryResult(QueryExecutionResult, Generic[T]):
    class_name: str = "QueryResult"
    version: str = "4"

    def __init__(
        self,
        is_success: bool,
        type: EnumQueryType,
        result: List[Dict[str, Any]],
        db_length: int,
        update_count: int,
        hit_count: int,
        error_message: str | None = None,
    ):
        super().__init__(is_success=is_success)
        self.type: EnumQueryType = type
        self.result: List[Dict[str, Any]] = result
        self.db_length: int = db_length
        self.update_count: int = update_count
        self.hit_count: int = hit_count
        self.error_message: str | None = error_message

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "QueryResult[T]":
        return cls(
            is_success=src["isSuccess"],
            type=EnumQueryType[src["type"]],
            result=list(src["result"]),
            db_length=src["dbLength"],
            update_count=src["updateCount"],
            hit_count=src["hitCount"],
            error_message=src.get("errorMessage"),
        )

    def convert(self, from_dict: Callable[[Dict[str, Any]], T]) -> List[T]:
        return [from_dict(i) for i in self.result]

    def clone(self) -> "QueryResult[T]":
        return self.from_dict(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "isSuccess": self.is_success,
            "type": self.type.name,
            "result": UtilCopy.jsonable_deep_copy(self.result),
            "dbLength": self.db_length,
            "updateCount": self.update_count,
            "hitCount": self.hit_count,
            "errorMessage": self.error_message,
        }
