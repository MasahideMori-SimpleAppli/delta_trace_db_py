# coding: utf-8
from typing import Any, Callable, Dict, List, Set
from copy import deepcopy

from file_state_manager.cloneable_file import CloneableFile
from delta_trace_db.db.util_copy import UtilCopy

# --- ダミーインポート ---
from dummy_modules import Query, QueryResult, QueryNode


class Collection(CloneableFile):
    class_name = "Collection"
    version = "6"

    def __init__(self):
        super().__init__()
        self._data: List[Dict[str, Any]] = []
        self.listeners: Set[Callable[[], None]] = set()
        self._is_transaction_mode: bool = False
        self.run_notify_listeners_in_transaction: bool = False

    def change_transaction_mode(self, is_transaction_mode: bool):
        self._is_transaction_mode = is_transaction_mode
        self.run_notify_listeners_in_transaction = False

    @classmethod
    def from_dict(cls, src: Dict[str, Any]):
        instance = cls()
        instance._data = deepcopy(src.get("data", []))
        return instance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "data": deepcopy(self._data)
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
        self.listeners.add(cb)

    def remove_listener(self, cb: Callable[[], None]):
        self.listeners.discard(cb)

    def notify_listeners(self):
        if not self._is_transaction_mode:
            for cb in self.listeners:
                cb()
        else:
            self.run_notify_listeners_in_transaction = True

    def _evaluate(self, record: Dict[str, Any], node: QueryNode) -> bool:
        return node.evaluate(record)

    def add_all(self, q: Query) -> QueryResult:
        add_data = deepcopy(q.add_data)
        self._data.extend(add_data)
        self.notify_listeners()
        return QueryResult(True, q.type, [], len(self._data), len(add_data), 0)

    def update(self, q: Query, is_single_target: bool) -> QueryResult:
        if q.return_data:
            r = []
            for item in self._data:
                if self._evaluate(item, q.query_node):
                    item.update(deepcopy(q.override_data))
                    r.append(item)
                    if is_single_target:
                        break
            if r:
                self.notify_listeners()
            return QueryResult(True, q.type, deepcopy(r), len(self._data), len(r), len(r))
        else:
            count = 0
            for item in self._data:
                if self._evaluate(item, q.query_node):
                    item.update(deepcopy(q.override_data))
                    count += 1
                    if is_single_target:
                        break
            if count > 0:
                self.notify_listeners()
            return QueryResult(True, q.type, [], len(self._data), count, count)

    def delete(self, q: Query) -> QueryResult:
        if q.return_data:
            deleted_items = [item for item in self._data if self._evaluate(item, q.query_node)]
            self._data = [item for item in self._data if not self._evaluate(item, q.query_node)]
            if deleted_items:
                self.notify_listeners()
            return QueryResult(True, q.type, deepcopy(deleted_items), len(self._data), len(deleted_items),
                               len(deleted_items))
        else:
            count = sum(1 for item in self._data if self._evaluate(item, q.query_node))
            self._data = [item for item in self._data if not self._evaluate(item, q.query_node)]
            if count > 0:
                self.notify_listeners()
            return QueryResult(True, q.type, [], len(self._data), count, count)

    def delete_one(self, q: Query) -> QueryResult:
        deleted_items = []
        for i, item in enumerate(self._data):
            if self._evaluate(item, q.query_node):
                deleted_items.append(item)
                del self._data[i]
                break
        if deleted_items:
            self.notify_listeners()
        return QueryResult(True, q.type, deepcopy(deleted_items), len(self._data), len(deleted_items),
                           len(deleted_items))

    def search(self, q: Query) -> QueryResult:
        r = [item for item in self._data if self._evaluate(item, q.query_node)]
        hit_count = len(r)
        if q.sort_obj:
            r.sort(key=q.sort_obj.get_comparator())
        if q.offset:
            r = r[q.offset:]
        if q.limit:
            r = r[:q.limit]
        return QueryResult(True, q.type, deepcopy(r), len(self._data), 0, hit_count)

    def get_all(self, q: Query) -> QueryResult:
        r = deepcopy(self._data)
        if q.sort_obj:
            r.sort(key=q.sort_obj.get_comparator())
        return QueryResult(True, q.type, r, len(self._data), 0, len(r))

    def clear(self, q: Query) -> QueryResult:
        pre_len = len(self._data)
        self._data.clear()
        self.notify_listeners()
        return QueryResult(True, q.type, [], 0, pre_len, pre_len)

    def clear_add(self, q: Query) -> QueryResult:
        pre_len = len(self._data)
        self._data.clear()
        self._data.extend(deepcopy(q.add_data))
        self.notify_listeners()
        return QueryResult(True, q.type, [], len(self._data), pre_len, pre_len)

    def conform_to_template(self, q: Query) -> QueryResult:
        for item in self._data:
            keys_to_remove = [k for k in item.keys() if k not in q.template]
            for k in keys_to_remove:
                item.pop(k)
            for k, v in q.template.items():
                if k not in item:
                    item[k] = deepcopy(v)
        self.notify_listeners()
        return QueryResult(True, q.type, [], len(self._data), len(self._data), len(self._data))

    def rename_field(self, q: Query) -> QueryResult:
        r = []
        for item in self._data:
            if q.rename_before not in item:
                return QueryResult(False, q.type, [], len(self._data), 0, 0,
                                   f'The target key does not exist. key:{q.rename_before}')
            if q.rename_after in item:
                return QueryResult(False, q.type, [], len(self._data), 0, 0,
                                   f'An existing key was specified as the new key. key:{q.rename_after}')
        update_count = 0
        for item in self._data:
            item[q.rename_after] = item[q.rename_before]
            del item[q.rename_before]
            update_count += 1
            if q.return_data:
                r.append(item)
        self.notify_listeners()
        return QueryResult(True, q.type, deepcopy(r), len(self._data), update_count, update_count)

    def count(self, q: Query) -> QueryResult:
        return QueryResult(True, q.type, [], len(self._data), 0, len(self._data))
