from typing import Any, Dict, List, Optional
from .base import BaseModel


class NewsItem(BaseModel):
    """
    A single news item from GET /news/ or GET /news/:stream.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewsItem":
        return cls(data)

    @property
    def id(self) -> str:
        return self._raw.get("_id", "")

    @property
    def stream(self) -> str:
        return self._raw.get("stream", "")

    @property
    def type(self) -> str:
        return self._raw.get("type", "")

    @property
    def data(self) -> Dict[str, Any]:
        return self._raw.get("data", {})

    @property
    def ts(self) -> Optional[str]:
        return self._raw.get("ts")

    def __repr__(self) -> str:
        return f"<NewsItem id={self.id!r} type={self.type!r} stream={self.stream!r}>"
