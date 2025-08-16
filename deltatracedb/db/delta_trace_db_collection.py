from typing import Any, Callable, Dict, List, Optional, Set
from util_copy import UtilCopy
# Query, QueryNode, QueryResult は別途定義が必要

class CollectionBase:
    """DB内のクラス単位の内容に関する抽象クラス"""
    def clone(self):
        raise NotImplementedError


class Collection(CollectionBase):
    class_name = "Collection"
    version = "4"

    def __init__(self):
        self._data: List[Dict[str, Any]] = []
        self._listeners: Set[Callable[[], None]] = set()

    @classmethod
    def from_dict(cls, src: Dict[str, Any]):
        obj = cls()
        obj._data = list(src["data"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return {
            "class_name": self.class_name,
            "version": self.version,
            "data": UtilCopy.jsonable_deep_copy(self._data)
        }

    def clone(self):
        return Collection.from_dict(self.to_dict())

    @property
    def raw(self) -> List[Dict[str, Any]]:
        return self._data

    @property
    def length(self) -> int:
        return len(self._data)

    def add_listener(self, cb: Callable[[], None]):
        self._listeners.add(cb)

    def remove_listener(self, cb: Callable[[], None]):
        self._listeners.discard(cb)

    def _notify_listeners(self):
        for cb in self._listeners:
            cb()

    def add_all(self, q: Query) -> QueryResult:
        add_data = UtilCopy.jsonable_deep_copy(q.add_data)
        self._data.extend(add_data)
        self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=[],
            db_length=len(self._data),
            update_count=len(add_data),
            hit_count=0
        )

    def update(self, q: Query, is_single_target: bool) -> QueryResult:
        r: List[Dict[str, Any]] = []
        count = 0
        for i, record in enumerate(self._data):
            if self._evaluate(record, q.query_node):
                record.update(UtilCopy.jsonable_deep_copy(q.override_data))
                r.append(record)
                count += 1
                if is_single_target:
                    break
        if q.sort_obj:
            r.sort(key=q.sort_obj.get_comparator())
        if count > 0:
            self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=UtilCopy.jsonable_deep_copy(r),
            db_length=len(self._data),
            update_count=count,
            hit_count=count
        )

    def delete(self, q: Query) -> QueryResult:
        deleted_items: List[Dict[str, Any]] = []
        remaining_data = []
        for item in self._data:
            if self._evaluate(item, q.query_node):
                deleted_items.append(item)
            else:
                remaining_data.append(item)
        self._data = remaining_data
        if deleted_items:
            self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=UtilCopy.jsonable_deep_copy(deleted_items),
            db_length=len(self._data),
            update_count=len(deleted_items),
            hit_count=len(deleted_items)
        )

    def delete_one(self, q: Query) -> QueryResult:
        for i, item in enumerate(self._data):
            if self._evaluate(item, q.query_node):
                deleted_item = self._data.pop(i)
                self._notify_listeners()
                return QueryResult(
                    is_success=True,
                    result=UtilCopy.jsonable_deep_copy([deleted_item]),
                    db_length=len(self._data),
                    update_count=1,
                    hit_count=1
                )
        return QueryResult(
            is_success=True,
            result=[],
            db_length=len(self._data),
            update_count=0,
            hit_count=0
        )

    def search(self, q: Query) -> QueryResult:
        r = [item for item in self._data if self._evaluate(item, q.query_node)]
        hit_count = len(r)
        if q.sort_obj:
            r.sort(key=q.sort_obj.get_comparator())
        if q.offset:
            r = r[q.offset:]
        if q.limit:
            r = r[:q.limit]
        return QueryResult(
            is_success=True,
            result=UtilCopy.jsonable_deep_copy(r),
            db_length=len(self._data),
            update_count=0,
            hit_count=hit_count
        )

    def get_all(self, q: Query) -> QueryResult:
        r = list(self._data)
        if q.sort_obj:
            r.sort(key=q.sort_obj.get_comparator())
        return QueryResult(
            is_success=True,
            result=UtilCopy.jsonable_deep_copy(r),
            db_length=len(self._data),
            update_count=0,
            hit_count=len(r)
        )

    def conform_to_template(self, q: Query) -> QueryResult:
        for item in self._data:
            # 1. 削除処理
            keys_to_remove = [k for k in item if k not in q.template]
            for key in keys_to_remove:
                del item[key]
            # 2. 追加処理
            for key, val in q.template.items():
                if key not in item:
                    item[key] = UtilCopy.jsonable_deep_copy(val)
        self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=[],
            db_length=len(self._data),
            update_count=len(self._data),
            hit_count=len(self._data)
        )

    def rename_field(self, q: Query) -> QueryResult:
        r = []
        update_count = 0
        for item in self._data:
            if q.rename_before not in item:
                return QueryResult(
                    is_success=False,
                    result=[],
                    db_length=len(self._data),
                    update_count=0,
                    hit_count=0,
                    error_message=f'The target key does not exist. key:{q.rename_before}'
                )
            if q.rename_after in item:
                return QueryResult(
                    is_success=False,
                    result=[],
                    db_length=len(self._data),
                    update_count=0,
                    hit_count=0,
                    error_message=f'An existing key was specified as the new key. key:{q.rename_after}'
                )
        for item in self._data:
            item[q.rename_after] = item.pop(q.rename_before)
            update_count += 1
            if q.return_data:
                r.append(item)
        self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=UtilCopy.jsonable_deep_copy(r),
            db_length=len(self._data),
            update_count=update_count,
            hit_count=update_count
        )

    def count(self) -> QueryResult:
        return QueryResult(
            is_success=True,
            result=[],
            db_length=len(self._data),
            update_count=0,
            hit_count=len(self._data)
        )

    def clear(self) -> QueryResult:
        pre_len = len(self._data)
        self._data.clear()
        self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=[],
            db_length=0,
            update_count=pre_len,
            hit_count=pre_len
        )

    def clear_add(self, q: Query) -> QueryResult:
        pre_len = len(self._data)
        self._data.clear()
        self._data.extend(UtilCopy.jsonable_deep_copy(q.add_data))
        self._notify_listeners()
        return QueryResult(
            is_success=True,
            result=[],
            db_length=len(self._data),
            update_count=pre_len,
            hit_count=pre_len
        )

    def _evaluate(self, record: Dict[str, Any], node: QueryNode) -> bool:
        return node.evaluate(record)
