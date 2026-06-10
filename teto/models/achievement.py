from typing import Any, Dict, List, Optional
from .base import BaseModel


class UserAchievement(BaseModel):
    """
    A single achievement entry inside GET /users/:user/summaries/achievements.
    Each item is an achievement object merged with the user's progress fields.
    """

    def __init__(
        self,
        id: str,
        k: int,
        name: str,
        object: str,
        category: str,
        desc: str,
        n: str,
        v: Optional[float],
        a: Optional[float],
        t: Optional[str],
        pos: Optional[int],
        total: Optional[int],
        rank: Optional[int],
        progress: Optional[float],
        hidden: bool,
        nolb: bool,
        notifypb: bool,
        art: Optional[int],
        min: Optional[float],
        deci: Optional[int],
        rt: Optional[int],
        vt: Optional[int],
        tiebreak: Optional[int],
        o: Optional[int],
    ):
        self.id = id
        self.k = k
        self.name = name
        self.object = object
        self.category = category
        self.desc = desc
        self.n = n
        self.v = v
        self.a = a
        self.t = t
        self.pos = pos
        self.total = total
        self.rank = rank
        self.progress = progress
        self.hidden = hidden
        self.nolb = nolb
        self.notifypb = notifypb
        self.art = art
        self.min = min
        self.deci = deci
        self.rt = rt
        self.vt = vt
        self.tiebreak = tiebreak
        self.o = o

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserAchievement":
        return cls(
            id=data.get("_id", ""),
            k=data.get("k", 0),
            name=data.get("name", ""),
            object=data.get("object", ""),
            category=data.get("category", ""),
            desc=data.get("desc", ""),
            n=data.get("n", ""),
            v=data.get("v"),
            a=data.get("a"),
            t=data.get("t"),
            pos=data.get("pos"),
            total=data.get("total"),
            rank=data.get("rank"),
            progress=data.get("progress"),
            hidden=data.get("hidden", False),
            nolb=data.get("nolb", False),
            notifypb=data.get("notifypb", False),
            art=data.get("art"),
            min=data.get("min"),
            deci=data.get("deci"),
            rt=data.get("rt"),
            vt=data.get("vt"),
            tiebreak=data.get("tiebreak"),
            o=data.get("o"),
        )

    def __repr__(self) -> str:
        return f"<UserAchievement k={self.k!r} name={self.name!r} rank={self.rank!r}>"


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
