# coding: utf-8
from typing import Any, Dict, List, Set, Callable

# --- ダミーインポート ---
from dummy_modules import CloneableFile, Collection, Query, QueryResult, TransactionQuery, TransactionQueryResult, \
    EnumQueryType


class DeltaTraceDatabase(CloneableFile):
    class_name = "DeltaTraceDatabase"
    version = "6"

    def __init__(self):
        self._collections: Dict[str, Collection] = {}

    @classmethod
    def from_dict(cls, src: Dict[str, Any]):
        instance = cls()
        instance._collections = cls._parse_collections(src)
        return instance

    @staticmethod
    def _parse_collections(src: Dict[str, Any]) -> Dict[str, Collection]:
        raw = src.get("collections")
        if not isinstance(raw, dict):
            raise ValueError("Invalid format: 'collections' should be a dict")
        result: Dict[str, Collection] = {}
        for key, value in raw.items():
            if not isinstance(value, dict):
                raise ValueError(f"Invalid format: value of collection '{key}' is not a dict")
            result[key] = Collection.from_dict(value)
        return result

    def collection(self, name: str) -> Collection:
        if name in self._collections:
            return self._collections[name]
        col = Collection()
        self._collections[name] = col
        return col

    def collection_to_dict(self, name: str) -> Dict[str, Any]:
        return self._collections.get(name).to_dict() if name in self._collections else {}

    def collection_from_dict(self, name: str, src: Dict[str, Any]) -> Collection:
        col = Collection.from_dict(src)
        self._collections[name] = col
        return col

    def collection_from_dict_keep_listener(self, name: str, src: Dict[str, Any]) -> Collection:
        col = Collection.from_dict(src)
        listeners_buf: Set[Callable[[], None]] = self._collections.get(
            name).listeners if name in self._collections else set()
        self._collections[name] = col
        if listeners_buf:
            self._collections[name].listeners = listeners_buf
        return col

    def clone(self) -> "DeltaTraceDatabase":
        return DeltaTraceDatabase.from_dict(self.to_dict())

    @property
    def raw(self) -> Dict[str, Collection]:
        return self._collections

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "collections": {k: v.to_dict() for k, v in self._collections.items()},
        }

    def add_listener(self, target: str, cb: Callable[[], None]):
        self.collection(target).add_listener(cb)

    def remove_listener(self, target: str, cb: Callable[[], None]):
        self.collection(target).remove_listener(cb)

    def execute_query_object(self, query: Any) -> Any:
        if isinstance(query, Query):
            return self.execute_query(query)
        elif isinstance(query, TransactionQuery):
            return self.execute_transaction_query(query)
        elif isinstance(query, dict):
            if query.get("className") == "Query":
                return self.execute_query(Query.from_dict(query))
            elif query.get("className") == "TransactionQuery":
                return self.execute_transaction_query(TransactionQuery.from_dict(query))
            else:
                raise ValueError(f"Unsupported query class: {query.get('className')}")
        else:
            raise ValueError(f"Unsupported query type: {type(query)}")

    def execute_query(self, q: Query) -> QueryResult:
        col = self.collection(q.target)
        try:
            r: QueryResult = None
            if q.type == EnumQueryType.add:
                r = col.add_all(q)
            elif q.type == EnumQueryType.update:
                r = col.update(q, is_single_target=False)
            elif q.type == EnumQueryType.updateOne:
                r = col.update(q, is_single_target=True)
            elif q.type == EnumQueryType.delete:
                r = col.delete(q)
            elif q.type == EnumQueryType.deleteOne:
                r = col.delete_one(q)
            elif q.type == EnumQueryType.search:
                r = col.search(q)
            elif q.type == EnumQueryType.getAll:
                r = col.get_all(q)
            elif q.type == EnumQueryType.conformToTemplate:
                r = col.conform_to_template(q)
            elif q.type == EnumQueryType.renameField:
                r = col.rename_field(q)
            elif q.type == EnumQueryType.count:
                r = col.count(q)
            elif q.type == EnumQueryType.clear:
                r = col.clear(q)
            elif q.type == EnumQueryType.clearAdd:
                r = col.clear_add(q)

            if q.type in (
                    EnumQueryType.add,
                    EnumQueryType.update,
                    EnumQueryType.updateOne,
                    EnumQueryType.delete,
                    EnumQueryType.deleteOne,
                    EnumQueryType.conformToTemplate,
                    EnumQueryType.renameField,
                    EnumQueryType.clear,
                    EnumQueryType.clearAdd,
            ):
                if q.must_affect_at_least_one and r.update_count == 0:
                    return QueryResult(
                        is_success=False,
                        type=q.type,
                        result=[],
                        db_length=len(col.raw),
                        update_count=0,
                        hit_count=r.hit_count,
                        error_message="No data matched the condition (mustAffectAtLeastOne=True)"
                    )
            return r
        except Exception as e:
            print(f"{self.class_name},execute_query: {e}")
            return QueryResult(
                is_success=False,
                type=q.type,
                result=[],
                db_length=len(col.raw),
                update_count=-1,
                hit_count=-1,
                error_message=str(e)
            )

    def execute_transaction_query(self, q: TransactionQuery) -> TransactionQueryResult:
        results: List[QueryResult] = []
        try:
            buff: Dict[str, Dict[str, Any]] = {}
            for i in q.queries:
                if i.target not in buff:
                    buff[i.target] = self.collection_to_dict(i.target)
                    self.collection(i.target).change_transaction_mode(True)
            try:
                for i in q.queries:
                    results.append(self.execute_query(i))
            except Exception:
                for key, val in buff.items():
                    self.collection_from_dict_keep_listener(key, val)
                    self.collection(key).change_transaction_mode(False)
                print(f"{self.class_name},execute_transaction_query: Transaction failed")
                return TransactionQueryResult(is_success=False, results=[], error_message="Transaction failed")

            # rollback if any query failed
            if any(not r.is_success for r in results):
                for key, val in buff.items():
                    self.collection_from_dict_keep_listener(key, val)
                    self.collection(key).change_transaction_mode(False)
                print(f"{self.class_name},execute_transaction_query: Transaction failed")
                return TransactionQueryResult(is_success=False, results=[], error_message="Transaction failed")

            # commit: notify listeners
            for key in buff.keys():
                col = self.collection(key)
                need_callback = getattr(col, "run_notify_listeners_in_transaction", False)
                col.change_transaction_mode(False)
                if need_callback:
                    col.notify_listeners()
            return TransactionQueryResult(is_success=True, results=results)
        except Exception as e:
            print(f"{self.class_name},execute_transaction_query: {e}")
            return TransactionQueryResult(is_success=False, results=[], error_message="Unexpected Error")
