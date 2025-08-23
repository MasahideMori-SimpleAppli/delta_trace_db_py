# coding: utf-8
from file_state_manager.cloneable_file import CloneableFile
from delta_trace_db.db.util_copy import UtilCopy
from typing import List, Optional, Dict, Any
from delta_trace_db.query.cause.enum_actor_type import EnumActorType


class Actor(CloneableFile):
    class_name = "Actor"
    version = "1"

    def __init__(self, type_: EnumActorType, id_: str, roles: List[str], permissions: List[str],
                 context: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.type = type_
        self.id = id_
        self.roles = roles
        self.permissions = permissions
        self.context = context

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> 'Actor':
        type_ = EnumActorType[src["type"]]
        id_ = src["id"]
        roles = list(src["roles"])
        permissions = list(src["permissions"])
        context = src.get("context")
        return cls(type_, id_, roles, permissions, context)

    def clone(self) -> 'Actor':
        return Actor.from_dict(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "type": self.type.name,
            "id": self.id,
            "roles": list(self.roles),
            "permissions": list(self.permissions),
            "context": UtilCopy.jsonable_deep_copy(self.context),
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Actor):
            return False
        return (
                self.type == other.type
                and self.id == other.id
                and set(self.roles) == set(other.roles)
                and set(self.permissions) == set(other.permissions)
                and self.context == other.context
        )

    def __hash__(self) -> int:
        roles_hash = hash(tuple(sorted(self.roles)))
        permissions_hash = hash(tuple(sorted(self.permissions)))
        context_hash = hash(frozenset(self.context.items())) if self.context else 0
        return hash((self.type, self.id, roles_hash, permissions_hash, context_hash))
