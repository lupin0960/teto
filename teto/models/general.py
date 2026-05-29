from typing import Any, Dict, List
from .base import BaseModel


class ServerStats(BaseModel):
    """
    GET /general/stats
    Some statistics about the service.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerStats":
        return cls(data)

    @property
    def usercount(self) -> int:
        return self._raw.get("usercount", 0)

    @property
    def usercount_delta(self) -> float:
        return self._raw.get("usercount_delta", 0.0)

    @property
    def anoncount(self) -> int:
        return self._raw.get("anoncount", 0)

    @property
    def totalaccounts(self) -> int:
        return self._raw.get("totalaccounts", 0)

    @property
    def rankedcount(self) -> int:
        return self._raw.get("rankedcount", 0)

    @property
    def replaycount(self) -> int:
        return self._raw.get("replaycount", 0)

    @property
    def gamesplayed(self) -> int:
        return self._raw.get("gamesplayed", 0)

    @property
    def gamesplayed_delta(self) -> float:
        return self._raw.get("gamesplayed_delta", 0.0)

    @property
    def gamesfinished(self) -> int:
        return self._raw.get("gamesfinished", 0)

    @property
    def gametime(self) -> float:
        return self._raw.get("gametime", 0.0)

    @property
    def inputs(self) -> int:
        return self._raw.get("inputs", 0)

    @property
    def piecesplaced(self) -> int:
        return self._raw.get("piecesplaced", 0)

    def __repr__(self) -> str:
        return f"<ServerStats usercount={self.usercount!r} gamesplayed={self.gamesplayed!r}>"


class ServerActivity(BaseModel):
    """
    GET /general/activity
    A graph of user activity over the last 2 days.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerActivity":
        return cls(data)

    @property
    def activity(self) -> List[int]:
        return self._raw.get("activity", [])

    def __repr__(self) -> str:
        return f"<ServerActivity datapoints={len(self.activity)}>"
