# coding: utf-8
from typing import List, Dict, Optional

from .cause.cause import Cause
from .enum_query_type import EnumQueryType
from .query import Query
from file_state_manager.cloneable_file import CloneableFile
from delta_trace_db.query.nodes.query_node import QueryNode
from .sort.abstract_sort import AbstractSort


# CloneableFile, QueryNode, AbstractSort, Cause は外部クラスなので
# ここでは型アノテーションだけ残しています。
# 必要に応じてインポートしてください。

class QueryBuilder:
    def __init__(self,
                 target: str,
                 query_type: EnumQueryType,
                 add_data: Optional[List[CloneableFile]] = None,
                 override_data: Optional[Dict[str, any]] = None,
                 template: Optional[Dict[str, any]] = None,
                 query_node: Optional[QueryNode] = None,
                 sort_obj: Optional[AbstractSort] = None,
                 offset: Optional[int] = None,
                 start_after: Optional[Dict[str, any]] = None,
                 end_before: Optional[Dict[str, any]] = None,
                 rename_before: Optional[str] = None,
                 rename_after: Optional[str] = None,
                 limit: Optional[int] = None,
                 return_data: bool = False,
                 must_affect_at_least_one: bool = True,
                 cause: Optional[Cause] = None):
        self.target = target
        self.query_type = query_type
        self.add_data = add_data
        self.override_data = override_data
        self.template = template
        self.query_node = query_node
        self.sort_obj = sort_obj
        self.offset = offset
        self.start_after = start_after
        self.end_before = end_before
        self.rename_before = rename_before
        self.rename_after = rename_after
        self.limit = limit
        self.return_data = return_data
        self.must_affect_at_least_one = must_affect_at_least_one
        self.cause = cause

    # --------------------------
    # Factory methods (Dartの名前付きコンストラクタに対応)
    # --------------------------
    @classmethod
    def add(cls, target: str,
            add_data: List[CloneableFile],
            must_affect_at_least_one: bool = True,
            cause: Optional[Cause] = None):
        return cls(target, EnumQueryType.add,
                   add_data=add_data,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def update(cls, target: str,
               query_node: "QueryNode",
               override_data: Dict[str, any],
               return_data: bool,
               sort_obj: Optional["AbstractSort"] = None,
               must_affect_at_least_one: bool = True,
               cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.update,
                   query_node=query_node,
                   override_data=override_data,
                   return_data=return_data,
                   sort_obj=sort_obj,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def update_one(cls, target: str,
                   query_node: QueryNode,
                   override_data: Dict[str, any],
                   return_data: bool,
                   must_affect_at_least_one: bool = True,
                   cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.updateOne,
                   query_node=query_node,
                   override_data=override_data,
                   return_data=return_data,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def delete(cls, target: str,
               query_node: QueryNode,
               return_data: bool,
               sort_obj: Optional["AbstractSort"] = None,
               must_affect_at_least_one: bool = True,
               cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.delete,
                   query_node=query_node,
                   return_data=return_data,
                   sort_obj=sort_obj,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def delete_one(cls, target: str,
                   query_node: QueryNode,
                   return_data: bool,
                   must_affect_at_least_one: bool = True,
                   cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.deleteOne,
                   query_node=query_node,
                   return_data=return_data,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def search(cls, target: str,
               query_node: QueryNode,
               sort_obj: Optional["AbstractSort"] = None,
               offset: Optional[int] = None,
               start_after: Optional[Dict[str, any]] = None,
               end_before: Optional[Dict[str, any]] = None,
               limit: Optional[int] = None,
               cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.search,
                   query_node=query_node,
                   sort_obj=sort_obj,
                   offset=offset,
                   start_after=start_after,
                   end_before=end_before,
                   limit=limit,
                   cause=cause)

    @classmethod
    def get_all(cls, target: str,
                sort_obj: Optional["AbstractSort"] = None,
                cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.getAll,
                   sort_obj=sort_obj,
                   cause=cause)

    @classmethod
    def conform_to_template(cls, target: str,
                            template: CloneableFile,
                            must_affect_at_least_one: bool = True,
                            cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.conformToTemplate,
                   template=template,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def rename_field(cls, target: str,
                     rename_before: str,
                     rename_after: str,
                     return_data: bool,
                     must_affect_at_least_one: bool = True,
                     cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.renameField,
                   rename_before=rename_before,
                   rename_after=rename_after,
                   return_data=return_data,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def count(cls, target: str,
              cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.count,
                   cause=cause)

    @classmethod
    def clear(cls, target: str,
              must_affect_at_least_one: bool = True,
              cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.clear,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    @classmethod
    def clear_add_all(cls, target: str,
                      add_data: List[CloneableFile],
                      must_affect_at_least_one: bool = True,
                      cause: Optional["Cause"] = None):
        return cls(target, EnumQueryType.clearAdd,
                   add_data=add_data,
                   must_affect_at_least_one=must_affect_at_least_one,
                   cause=cause)

    # --------------------------
    # build() : Query インスタンスを返す
    # --------------------------
    def build(self) -> Query:
        m_data: Optional[List[Dict[str, any]]] = None
        if self.add_data is not None:
            m_data = [i.to_dict() for i in self.add_data]

        return Query(
            target=self.target,
            query_type=self.query_type,
            add_data=m_data,
            override_data=self.override_data,
            template=self.template.to_dict() if self.template else None,
            query_node=self.query_node,
            sort_obj=self.sort_obj,
            offset=self.offset,
            start_after=self.start_after,
            end_before=self.end_before,
            rename_before=self.rename_before,
            rename_after=self.rename_after,
            limit=self.limit,
            return_data=self.return_data,
            must_affect_at_least_one=self.must_affect_at_least_one,
            cause=self.cause
        )
