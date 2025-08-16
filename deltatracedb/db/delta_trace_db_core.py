from typing import Any, Callable, Dict, List, TypeVar

# 仮置きインポート（Collection, Query, TransactionQuery など）
from deltatracedb.db.delta_trace_db_collection import Collection, CollectionBase
from deltatracedb.query.query import Query, EnumQueryType, QueryResult, QueryExecutionResult
from deltatracedb.query.transaction_query import TransactionQuery, TransactionQueryResult


class DeltaTraceDatabase:
    className: str = "DeltaTraceDatabase"
    version: str = "4"

    def __init__(self) -> None:
        self._collections: Dict[str, CollectionBase] = {}

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "DeltaTraceDatabase":
        db = cls.__new__(cls)
        db._collections = cls._parse_collections(src)
        return db

    @staticmethod
    def _parse_collections(src: Dict[str, Any]) -> Dict[str, CollectionBase]:
        raw = src.get("collections")
        if not isinstance(raw, dict):
            raise ValueError("Invalid format: 'collections' should be a dict.")
        r: Dict[str, CollectionBase] = {}
        for key, value in raw.items():
            if not isinstance(value, dict):
                raise ValueError(f"Invalid format: value of collection '{key}' is not a dict.")
            r[key] = Collection.from_dict(value)
        return r

    def collection(self, name: str) -> Collection:
        if name in self._collections:
            return self._collections[name]  # type: ignore
        col = Collection()
        self._collections[name] = col
        return col

    def collection_to_dict(self, name: str) -> Dict[str, Any]:
        col = self._collections.get(name)
        if col is None:
            return {}
        return col.to_dict()

    def collection_from_dict(self, name: str, src: Dict[str, Any]) -> Collection:
        col = Collection.from_dict(src)
        self._collections[name] = col
        return col

    def clone(self) -> "DeltaTraceDatabase":
        return DeltaTraceDatabase.from_dict(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        m_collections: Dict[str, Dict[str, Any]] = {}
        for k, v in self._collections.items():
            m_collections[k] = v.to_dict()
        return {
            "className": self.className,
            "version": self.version,
            "collections": m_collections,
        }

    # --- Listener ---
    def add_listener(self, target: str, cb: Callable[[], None]) -> None:
        col = self.collection(target)
        col.add_listener(cb)

    def remove_listener(self, target: str, cb: Callable[[], None]) -> None:
        col = self.collection(target)
        col.remove_listener(cb)

    # --- Query execution ---
    def execute_query_object(self, query: Any) -> QueryExecutionResult:
        if isinstance(query, Query):
            return self.execute_query(query)
        elif isinstance(query, TransactionQuery):
            return self.execute_transaction_query(query)
        elif isinstance(query, dict):
            cls_name = query.get("className")
            if cls_name == "Query":
                return self.execute_query(Query.from_dict(query))
            elif cls_name == "TransactionQuery":
                return self.execute_transaction_query(TransactionQuery.from_dict(query))
            else:
                raise ValueError(f"Unsupported query class: {cls_name}")
        else:
            raise ValueError(f"Unsupported query type: {type(query)}")

    def execute_query(self, q: Query) -> QueryResult:
        col = self.collection(q.target)
        try:
            r: QueryResult
            t = q.type
            if t == EnumQueryType.add:
                r = col.add_all(q)
            elif t == EnumQueryType.update:
                r = col.update(q, is_single_target=False)
            elif t == EnumQueryType.updateOne:
                r = col.update(q, is_single_target=True)
            elif t == EnumQueryType.delete:
                r = col.delete(q)
            elif t == EnumQueryType.deleteOne:
                r = col.delete_one(q)
            elif t == EnumQueryType.search:
                r = col.search(q)
            elif t == EnumQueryType.getAll:
                r = col.get_all(q)
            elif t == EnumQueryType.conformToTemplate:
                r = col.conform_to_template(q)
            elif t == EnumQueryType.renameField:
                r = col.rename_field(q)
            elif t == EnumQueryType.count:
                r = col.count()
            elif t == EnumQueryType.clear:
                r = col.clear()
            elif t == EnumQueryType.clearAdd:
                r = col.clear_add(q)
            else:
                raise ValueError(f"Unsupported query type: {t}")

            if t in [
                EnumQueryType.add,
                EnumQueryType.update,
                EnumQueryType.updateOne,
                EnumQueryType.delete,
                EnumQueryType.deleteOne,
                EnumQueryType.conformToTemplate,
                EnumQueryType.renameField,
                EnumQueryType.clear,
                EnumQueryType.clearAdd,
            ]:
                if q.must_affect_at_least_one and r.update_count == 0:
                    return QueryResult(
                        is_success=False,
                        result=[],
                        db_length=len(col.raw),
                        update_count=0,
                        hit_count=r.hit_count,
                        error_message="No data matched the condition (must_affect_at_least_one=True)",
                    )
                else:
                    return r
            elif t in [EnumQueryType.search, EnumQueryType.getAll, EnumQueryType.count]:
                return r
        except ValueError as e:
            return QueryResult(
                is_success=False,
                result=[],
                db_length=len(col.raw),
                update_count=-1,
                hit_count=-1,
                error_message=str(e),
            )
        except Exception as e:
            print(f"{self.className}, execute_query: {e}")
            return QueryResult(
                is_success=False,
                result=[],
                db_length=len(col.raw),
                update_count=-1,
                hit_count=-1,
                error_message="Unexpected Error",
            )

    def execute_transaction_query(self, q: TransactionQuery) -> TransactionQueryResult:
        results: List[QueryResult] = []
        try:
            # バッファリング
            buff: Dict[str, Dict[str, Any]] = {}
            for query in q.queries:
                if query.target not in buff:
                    buff[query.target] = self.collection_to_dict(query.target)

            # 実行
            try:
                for query in q.queries:
                    results.append(self.execute_query(query))
            except Exception:
                for key, val in buff.items():
                    self.collection_from_dict(key, val)
                print(f"{self.className}, execute_transaction_query: Transaction failed")
                return TransactionQueryResult(is_success=False, results=[], error_message="Transaction failed")

            # 成功確認
            for r in results:
                if not r.is_success:
                    for key, val in buff.items():
                        self.collection_from_dict(key, val)
                    print(f"{self.className}, execute_transaction_query: Transaction failed")
                    return TransactionQueryResult(is_success=False, results=[], error_message="Transaction failed")

            return TransactionQueryResult(is_success=True, results=results)
        except Exception as e:
            print(f"{self.className}, execute_transaction_query: {e}")
            return TransactionQueryResult(is_success=False, results=[], error_message="Unexpected Error")
