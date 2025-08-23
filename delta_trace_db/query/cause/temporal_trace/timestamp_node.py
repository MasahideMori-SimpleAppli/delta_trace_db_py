# coding: utf-8
from datetime import datetime
from typing import Dict, Any
from file_state_manager.cloneable_file import CloneableFile
from delta_trace_db.db.util_copy import UtilCopy


class TimestampNode(CloneableFile):
    """軌跡上の各チェックポイントを表すノード。"""

    class_name = "TimestampNode"
    version = "1"

    def __init__(self, timestamp: datetime, location: str, context: Dict[str, Any] = None):
        super().__init__()
        self.timestamp: datetime = timestamp
        self.location: str = location
        self.context: Dict[str, Any] = context if context is not None else {}

    @classmethod
    def from_dict(cls, src: Dict[str, Any]):
        return cls(
            timestamp=datetime.fromisoformat(src["timestamp"]),
            location=src["location"],
            context=src.get("context", {}),
        )

    def clone(self):
        return TimestampNode.from_dict(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "className": self.class_name,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "context": UtilCopy.jsonable_deep_copy(self.context),
        }
