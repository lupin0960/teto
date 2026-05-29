from typing import Any, Dict, List, Optional
from .base import BaseModel


class Record(BaseModel):
    """
    A single record from GET /records/:leaderboard or GET /records/reverse.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":
        return cls(data)

    @property
    def id(self) -> str:
        return self._raw.get("_id", "")

    @property
    def replayid(self) -> str:
        return self._raw.get("replayid", "")

    @property
    def stub(self) -> bool:
        return self._raw.get("stub", False)

    @property
    def gamemode(self) -> str:
        return self._raw.get("gamemode", "")

    @property
    def pb(self) -> bool:
        return self._raw.get("pb", False)

    @property
    def oncepb(self) -> bool:
        return self._raw.get("oncepb", False)

    @property
    def ts(self) -> Optional[str]:
        return self._raw.get("ts")

    @property
    def userid(self) -> Optional[str]:
        user = self._raw.get("user")
        if isinstance(user, dict):
            return user.get("_id")
        return self._raw.get("userid")

    @property
    def username(self) -> Optional[str]:
        user = self._raw.get("user")
        if isinstance(user, dict):
            return user.get("username")
        return None

    @property
    def results(self) -> Dict[str, Any]:
        return self._raw.get("results", {})

    @property
    def extras(self) -> Dict[str, Any]:
        return self._raw.get("extras", {})

    def __repr__(self) -> str:
        return f"<Record id={self.id!r} gamemode={self.gamemode!r}>"
