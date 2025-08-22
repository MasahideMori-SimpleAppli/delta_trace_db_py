# coding: utf-8
from typing import Dict, Any
from dummy_modules import CloneableFile, QueryResult, TransactionQueryResult

class QueryExecutionResult(CloneableFile):
    def __init__(self, is_success: bool):
        self.is_success: bool = is_success

    @staticmethod
    def from_dict(src: Dict[str, Any]) -> "QueryExecutionResult":
        class_name = src.get("className")
        if class_name == "QueryResult":
            return QueryResult.from_dict(src)
        elif class_name == "TransactionQueryResult":
            return TransactionQueryResult.from_dict(src)
        else:
            raise ValueError("QueryExecutionResult: The object cannot be converted.")
