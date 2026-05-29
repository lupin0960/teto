from typing import Any, Dict, List
from .base import BaseModel


class LabsScoreflow(BaseModel):
    """
    GET /labs/scoreflow/:user/:gamemode
    A condensed graph of all of the user's records in the gamemode.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsScoreflow":
        return cls(data)

    @property
    def scoreflow(self) -> List[Any]:
        return self._raw.get("scoreflow", [])

    def __repr__(self) -> str:
        return f"<LabsScoreflow datapoints={len(self.scoreflow)}>"


class LabsLeagueflow(BaseModel):
    """
    GET /labs/leagueflow/:user
    A condensed graph of all of the user's matches in TETRA LEAGUE.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsLeagueflow":
        return cls(data)

    @property
    def leagueflow(self) -> List[Any]:
        return self._raw.get("leagueflow", [])

    def __repr__(self) -> str:
        return f"<LabsLeagueflow datapoints={len(self.leagueflow)}>"


class LabsLeagueRanks(BaseModel):
    """
    GET /labs/league_ranks
    A view over all TETRA LEAGUE ranks and their metadata.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabsLeagueRanks":
        return cls(data)

    @property
    def ranks(self) -> Dict[str, Any]:
        return self._raw

    def __repr__(self) -> str:
        return f"<LabsLeagueRanks ranks={list(self._raw.keys())!r}>"
