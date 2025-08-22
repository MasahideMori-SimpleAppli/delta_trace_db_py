# coding: utf-8
from typing import Generic, TypeVar, List, Dict, Any, Optional
from dummy_modules import QueryExecutionResult, QueryResult, UtilCopy

T = TypeVar("T")

class TransactionQueryResult(QueryExecutionResult, Generic[T]):
    """
    (en) The result class for a transactional query.
    (ja) トランザクションクエリの結果クラスです。
    """
    className: str = "TransactionQueryResult"
    version: str = "2"

    def __init__(self, is_success: bool, results: List[QueryResult], error_message: Optional[str] = None):
        """
        :param is_success: A flag indicating whether the operation was successful.
        :param results: The QueryResults for each execution are stored in the same order as they were specified in the transaction query.
        :param error_message: A message that is added only if an error occurs.
        """
        super().__init__(is_success=is_success)
        self.results = results
        self.error_message = error_message

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "TransactionQueryResult[T]":
        qr = [QueryResult.from_dict(i) for i in src["results"]]
        return cls(
            is_success=src["isSuccess"],
            results=qr,
            error_message=src.get("errorMessage")
        )

    def to_dict(self) -> Dict[str, Any]:
        qr = [i.to_dict() for i in self.results]
        return {
            "className": self.className,
            "version": self.version,
            "isSuccess": self.is_success,
            "results": UtilCopy.jsonableDeepCopy(qr),
            "errorMessage": self.error_message,
        }

    def clone(self) -> "TransactionQueryResult[T]":
        return TransactionQueryResult.from_dict(self.to_dict())
