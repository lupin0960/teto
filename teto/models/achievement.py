from typing import Any, Dict, List, Optional
from .base import BaseModel


class Achievement(BaseModel):
    """
    GET /achievements/:k
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Achievement":
        return cls(data)

    @property
    def achievement(self) -> Dict[str, Any]:
        return self._raw.get("achievement", {})

    @property
    def cutoffs(self) -> Dict[str, Any]:
        return self._raw.get("cutoffs", {})

    @property
    def leaderboard(self) -> List[Dict[str, Any]]:
        return self._raw.get("leaderboard", [])

    def __repr__(self) -> str:
        k = self.achievement.get("k", "")
        name = self.achievement.get("name", "")
        return f"<Achievement k={k!r} name={name!r}>"


class AchievementEntry(BaseModel):
    """
    A single entry from GET /achievements/:k/entries.
    Response shape per entry:
      { _id: ..., k: ..., v: ..., additional: ..., t: ...,
        u: { _id: ..., username: ... } }
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AchievementEntry":
        return cls(data)

    @property
    def id(self) -> str:
        return self._raw.get("_id", "")

    @property
    def userid(self) -> str:
        u = self._raw.get("u")
        if isinstance(u, dict):
            return u.get("_id", "")
        return self._raw.get("userid", "")

    @property
    def username(self) -> Optional[str]:
        u = self._raw.get("u")
        if isinstance(u, dict):
            return u.get("username")
        return None

    @property
    def k(self) -> int:
        return self._raw.get("k", 0)

    @property
    def v(self) -> float:
        return self._raw.get("v", 0.0)

    @property
    def additional(self) -> Optional[float]:
        return self._raw.get("additional")

    @property
    def t(self) -> Optional[str]:
        return self._raw.get("t")

    def __repr__(self) -> str:
        return f"<AchievementEntry username={self.username!r} v={self.v!r}>"
