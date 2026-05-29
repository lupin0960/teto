from typing import Any, Dict, List, Optional
from .base import BaseModel


class LabsScoreflow(BaseModel):
    """
    GET /labs/scoreflow/:user/:gamemode
    Response: { startTime: int, points: [[offset_ms, pb, score], ...] }
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsScoreflow":
        return cls(data)

    @property
    def start_time(self) -> Optional[int]:
        return self._raw.get("startTime")

    @property
    def points(self) -> List[Any]:
        """List of [offset_ms, is_pb, score] entries."""
        return self._raw.get("points", [])

    def __repr__(self) -> str:
        return f"<LabsScoreflow datapoints={len(self.points)}>"


class LabsLeagueflow(BaseModel):
    """
    GET /labs/leagueflow/:user
    Response shape mirrors scoreflow: { startTime: int, points: [...] }
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsLeagueflow":
        return cls(data)

    @property
    def start_time(self) -> Optional[int]:
        return self._raw.get("startTime")

    @property
    def points(self) -> List[Any]:
        """List of [offset_ms, ...] entries."""
        return self._raw.get("points", [])

    def __repr__(self) -> str:
        return f"<LabsLeagueflow datapoints={len(self.points)}>"


class LabsLeagueRanks(BaseModel):
    """
    GET /labs/league_ranks
    Response: { data: { <rank>: { ..stats.. } }, s: ..., t: ... }
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsLeagueRanks":
        return cls(data)

    @property
    def ranks(self) -> Dict[str, Any]:
        return self._raw.get("data", self._raw)

    def __repr__(self) -> str:
        return f"<LabsLeagueRanks ranks={list(self.ranks.keys())!r}>"
