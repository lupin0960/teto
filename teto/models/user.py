from typing import Any, Dict, List, Optional
from .base import BaseModel


class User(BaseModel):
    """
    GET /users/:user
    An object describing the user in detail.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data
        self._user = data.get("user", data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(data)

    @property
    def id(self) -> str:
        return self._user.get("_id", "")

    @property
    def username(self) -> str:
        return self._user.get("username", "")

    @property
    def role(self) -> str:
        return self._user.get("role", "")

    @property
    def ts(self) -> Optional[str]:
        return self._user.get("ts")

    @property
    def xp(self) -> float:
        return self._user.get("xp", 0.0)

    @property
    def gamesplayed(self) -> int:
        return self._user.get("gamesplayed", 0)

    @property
    def gameswon(self) -> int:
        return self._user.get("gameswon", 0)

    @property
    def gametime(self) -> float:
        return self._user.get("gametime", 0.0)

    @property
    def country(self) -> Optional[str]:
        return self._user.get("country")

    @property
    def supporter(self) -> bool:
        return self._user.get("supporter", False)

    @property
    def verified(self) -> bool:
        return self._user.get("verified", False)

    @property
    def league(self) -> Dict[str, Any]:
        return self._user.get("league", {})

    @property
    def avatar_revision(self) -> Optional[int]:
        return self._user.get("avatar_revision")

    @property
    def banner_revision(self) -> Optional[int]:
        return self._user.get("banner_revision")

    @property
    def bio(self) -> Optional[str]:
        return self._user.get("bio")

    @property
    def connections(self) -> Dict[str, Any]:
        return self._user.get("connections", {})

    @property
    def friend_count(self) -> int:
        return self._user.get("friend_count", 0)

    def __repr__(self) -> str:
        return f"<User id={self.id!r} username={self.username!r} role={self.role!r}>"


class UserSummary40L(BaseModel):
    """
    GET /users/:user/summaries/40l
    A summary of the user's 40 LINES games.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummary40L":
        return cls(data)

    @property
    def record(self) -> Optional[Dict[str, Any]]:
        return self._raw.get("record")

    @property
    def rank(self) -> Optional[int]:
        return self._raw.get("rank")

    @property
    def rank_local(self) -> Optional[int]:
        return self._raw.get("rank_local")

    def __repr__(self) -> str:
        return f"<UserSummary40L rank={self.rank!r}>"


class UserSummaryBlitz(BaseModel):
    """
    GET /users/:user/summaries/blitz
    A summary of the user's BLITZ games.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryBlitz":
        return cls(data)

    @property
    def record(self) -> Optional[Dict[str, Any]]:
        return self._raw.get("record")

    @property
    def rank(self) -> Optional[int]:
        return self._raw.get("rank")

    @property
    def rank_local(self) -> Optional[int]:
        return self._raw.get("rank_local")

    def __repr__(self) -> str:
        return f"<UserSummaryBlitz rank={self.rank!r}>"


class UserSummaryZenith(BaseModel):
    """
    GET /users/:user/summaries/zenith
    A summary of the user's QUICK PLAY games.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZenith":
        return cls(data)

    @property
    def record(self) -> Optional[Dict[str, Any]]:
        return self._raw.get("record")

    @property
    def best(self) -> Dict[str, Any]:
        return self._raw.get("best", {})

    def __repr__(self) -> str:
        return "<UserSummaryZenith>"


class UserSummaryZenithEx(BaseModel):
    """
    GET /users/:user/summaries/zenithex
    A summary of the user's EXPERT QUICK PLAY games.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZenithEx":
        return cls(data)

    @property
    def record(self) -> Optional[Dict[str, Any]]:
        return self._raw.get("record")

    @property
    def best(self) -> Dict[str, Any]:
        return self._raw.get("best", {})

    def __repr__(self) -> str:
        return "<UserSummaryZenithEx>"


class UserSummaryLeague(BaseModel):
    """
    GET /users/:user/summaries/league
    A summary of the user's TETRA LEAGUE standing.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryLeague":
        return cls(data)

    @property
    def gamesplayed(self) -> int:
        return self._raw.get("gamesplayed", 0)

    @property
    def gameswon(self) -> int:
        return self._raw.get("gameswon", 0)

    @property
    def tr(self) -> float:
        return self._raw.get("tr", 0.0)

    @property
    def glicko(self) -> Optional[float]:
        return self._raw.get("glicko")

    @property
    def rd(self) -> Optional[float]:
        return self._raw.get("rd")

    @property
    def rank(self) -> str:
        return self._raw.get("rank", "z")

    @property
    def bestrank(self) -> str:
        return self._raw.get("bestrank", "z")

    @property
    def apm(self) -> Optional[float]:
        return self._raw.get("apm")

    @property
    def pps(self) -> Optional[float]:
        return self._raw.get("pps")

    @property
    def vs(self) -> Optional[float]:
        return self._raw.get("vs")

    @property
    def standing(self) -> int:
        return self._raw.get("standing", -1)

    @property
    def standing_local(self) -> int:
        return self._raw.get("standing_local", -1)

    def __repr__(self) -> str:
        return f"<UserSummaryLeague rank={self.rank!r} tr={self.tr!r}>"


class UserSummaryZen(BaseModel):
    """
    GET /users/:user/summaries/zen
    A summary of the user's ZEN progress.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZen":
        return cls(data)

    @property
    def level(self) -> int:
        return self._raw.get("level", 0)

    @property
    def score(self) -> int:
        return self._raw.get("score", 0)

    def __repr__(self) -> str:
        return f"<UserSummaryZen level={self.level!r} score={self.score!r}>"


class UserSummaryAchievements(BaseModel):
    """
    GET /users/:user/summaries/achievements
    An object containing all the user's achievements.
    """

    def __init__(self, data: Dict[str, Any]):
        self._achievements: List[Dict[str, Any]] = (
            data if isinstance(data, list) else data.get("achievements", [])
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryAchievements":
        return cls(data)

    @property
    def achievements(self) -> List[Dict[str, Any]]:
        return self._achievements

    def __repr__(self) -> str:
        return f"<UserSummaryAchievements count={len(self.achievements)}>"


class UserSummaryAll(BaseModel):
    """
    GET /users/:user/summaries
    All the user's summaries in one object.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data
        self.forty_lines = UserSummary40L.from_dict(data.get("40l", {}))
        self.blitz = UserSummaryBlitz.from_dict(data.get("blitz", {}))
        self.zenith = UserSummaryZenith.from_dict(data.get("zenith", {}))
        self.zenithex = UserSummaryZenithEx.from_dict(data.get("zenithex", {}))
        self.league = UserSummaryLeague.from_dict(data.get("league", {}))
        self.zen = UserSummaryZen.from_dict(data.get("zen", {}))
        self.achievements = UserSummaryAchievements.from_dict(
            data.get("achievements", {})
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryAll":
        return cls(data)

    def __repr__(self) -> str:
        return "<UserSummaryAll>"


class UserRecord(BaseModel):
    """
    GET /users/:user/records/:gamemode/:leaderboard
    A single record entry from a user's personal records.
    """

    def __init__(self, data: Dict[str, Any]):
        self._raw = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserRecord":
        return cls(data)

    @property
    def id(self) -> str:
        return self._raw.get("_id", "")

    @property
    def replayid(self) -> str:
        return self._raw.get("replayid", "")

    @property
    def ts(self) -> Optional[str]:
        return self._raw.get("ts")

    @property
    def userid(self) -> str:
        return self._raw.get("userid", "")

    @property
    def gamemode(self) -> str:
        return self._raw.get("gamemode", "")

    @property
    def results(self) -> Dict[str, Any]:
        return self._raw.get("results", {})

    @property
    def extras(self) -> Dict[str, Any]:
        return self._raw.get("extras", {})

    def __repr__(self) -> str:
        return f"<UserRecord id={self.id!r} gamemode={self.gamemode!r}>"
