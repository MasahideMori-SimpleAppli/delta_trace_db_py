from typing import List, Optional
from deltatracedb.query.cause.temporal_trace.timestamp_node import TimestampNode

class TemporalTrace:
    """イベントの「時間の軌跡」を記録するクラス。"""
    class_name = "TemporalTrace"
    version = "1"

    def __init__(self, nodes: Optional[List[TimestampNode]] = None):
        self.nodes: List[TimestampNode] = nodes if nodes is not None else []

    @property
    def initiated_at(self) -> Optional[str]:
        """最初のイベント発生時刻。"""
        return self.nodes[0].timestamp if self.nodes else None

    @property
    def finalized_at(self) -> Optional[str]:
        """最後のイベント記録時刻。"""
        return self.nodes[-1].timestamp if self.nodes else None

    @classmethod
    def from_dict(cls, src: dict):
        nodes_list = src.get("nodes", [])
        nodes = [TimestampNode.from_dict(n) for n in nodes_list]
        return cls(nodes=nodes)

    def clone(self):
        return TemporalTrace.from_dict(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "className": self.class_name,
            "version": self.version,
            "nodes": [node.to_dict() for node in self.nodes],
        }
