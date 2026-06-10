from typing import Any, Dict, List, Optional
from .base import BaseModel
from .record import Record, RecordResults
from .achievement import UserAchievement


class Badge(BaseModel):
    """
    A badge on a user's profile.
    Part of the user object returned by GET /users/:user
    """

    def __init__(
        self,
        id: str,
        label: str,
        ts: Optional[str] = None,
        group: Optional[str] = None,
        desc: Optional[str] = None,
        global_: Optional[bool] = None,
    ):
        self.id = id
        self.label = label
        self.ts = ts
        self.group = group
        self.desc = desc
        self.global_ = global_

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Badge":
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            ts=data.get("ts"),
            group=data.get("group"),
            desc=data.get("desc"),
            global_=data.get("global"),
        )

    def __repr__(self) -> str:
        return f"<Badge id={self.id!r} label={self.label!r}>"


class User(BaseModel):
    """
    GET /users/:user
    An object describing the user in detail.
    """

    def __init__(
        self,
        id: str,
        username: str,
        role: str,
        xp: float,
        gamesplayed: int,
        gameswon: int,
        gametime: float,
        ts: Optional[str] = None,
        country: Optional[str] = None,
        supporter: bool = False,
        verified: bool = False,
        league: Optional[Dict[str, Any]] = None,
        avatar_revision: Optional[int] = None,
        banner_revision: Optional[int] = None,
        bio: Optional[str] = None,
        connections: Optional[Dict[str, Any]] = None,
        friend_count: int = 0,
        badges: Optional[List[Badge]] = None,
    ):
        self.id = id
        self.username = username
        self.role = role
        self.xp = xp
        self.gamesplayed = gamesplayed
        self.gameswon = gameswon
        self.gametime = gametime
        self.ts = ts
        self.country = country
        self.supporter = supporter
        self.verified = verified
        self.league = league or {}
        self.avatar_revision = avatar_revision
        self.banner_revision = banner_revision
        self.bio = bio
        self.connections = connections or {}
        self.friend_count = friend_count
        self.badges = badges or []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        u = data.get("user", data)
        return cls(
            id=u.get("_id", ""),
            username=u.get("username", ""),
            role=u.get("role", ""),
            xp=u.get("xp", 0.0),
            gamesplayed=u.get("gamesplayed", 0),
            gameswon=u.get("gameswon", 0),
            gametime=u.get("gametime", 0.0),
            ts=u.get("ts"),
            country=u.get("country"),
            supporter=u.get("supporter", False),
            verified=u.get("verified", False),
            league=u.get("league", {}),
            avatar_revision=u.get("avatar_revision"),
            banner_revision=u.get("banner_revision"),
            bio=u.get("bio"),
            connections=u.get("connections", {}),
            friend_count=u.get("friend_count", 0),
            badges=[Badge.from_dict(b) for b in u.get("badges", [])],
        )

    def __repr__(self) -> str:
        return f"<User id={self.id!r} username={self.username!r} role={self.role!r}>"


class ZenithBest(BaseModel):
    """
    The best run entry inside UserSummaryZenith / UserSummaryZenithEx.
    Shape: { record: <Record>, rank: int }
    """

    def __init__(self, record: Optional[Record], rank: Optional[int]):
        self.record = record
        self.rank = rank

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ZenithBest":
        raw_record = data.get("record")
        return cls(
            record=Record.from_dict(raw_record) if raw_record else None,
            rank=data.get("rank"),
        )

    def __repr__(self) -> str:
        return f"<ZenithBest rank={self.rank!r}>"


class UserSummary40L(BaseModel):
    """
    GET /users/:user/summaries/40l
    A summary of the user's 40 LINES games.
    """

    def __init__(
        self,
        record: Optional[Record],
        rank: Optional[int],
        rank_local: Optional[int],
    ):
        self.record = record
        self.rank = rank
        self.rank_local = rank_local

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummary40L":
        raw_record = data.get("record")
        return cls(
            record=Record.from_dict(raw_record) if raw_record else None,
            rank=data.get("rank"),
            rank_local=data.get("rank_local"),
        )

    def __repr__(self) -> str:
        return f"<UserSummary40L rank={self.rank!r}>"


class UserSummaryBlitz(BaseModel):
    """
    GET /users/:user/summaries/blitz
    A summary of the user's BLITZ games.
    """

    def __init__(
        self,
        record: Optional[Record],
        rank: Optional[int],
        rank_local: Optional[int],
    ):
        self.record = record
        self.rank = rank
        self.rank_local = rank_local

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryBlitz":
        raw_record = data.get("record")
        return cls(
            record=Record.from_dict(raw_record) if raw_record else None,
            rank=data.get("rank"),
            rank_local=data.get("rank_local"),
        )

    def __repr__(self) -> str:
        return f"<UserSummaryBlitz rank={self.rank!r}>"


class UserSummaryZenith(BaseModel):
    """
    GET /users/:user/summaries/zenith
    A summary of the user's QUICK PLAY games.
    """

    def __init__(
        self,
        record: Optional[Record],
        best: ZenithBest,
    ):
        self.record = record
        self.best = best

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZenith":
        raw_record = data.get("record")
        return cls(
            record=Record.from_dict(raw_record) if raw_record else None,
            best=ZenithBest.from_dict(data.get("best", {})),
        )

    def __repr__(self) -> str:
        return "<UserSummaryZenith>"


class UserSummaryZenithEx(BaseModel):
    """
    GET /users/:user/summaries/zenithex
    A summary of the user's EXPERT QUICK PLAY games.
    """

    def __init__(
        self,
        record: Optional[Record],
        best: ZenithBest,
    ):
        self.record = record
        self.best = best

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZenithEx":
        raw_record = data.get("record")
        return cls(
            record=Record.from_dict(raw_record) if raw_record else None,
            best=ZenithBest.from_dict(data.get("best", {})),
        )

    def __repr__(self) -> str:
        return "<UserSummaryZenithEx>"


class UserSummaryLeague(BaseModel):
    """
    GET /users/:user/summaries/league
    A summary of the user's TETRA LEAGUE standing.
    """

    def __init__(
        self,
        gamesplayed: int,
        gameswon: int,
        tr: float,
        rank: str,
        bestrank: str,
        standing: int,
        standing_local: int,
        glicko: Optional[float] = None,
        rd: Optional[float] = None,
        apm: Optional[float] = None,
        pps: Optional[float] = None,
        vs: Optional[float] = None,
    ):
        self.gamesplayed = gamesplayed
        self.gameswon = gameswon
        self.tr = tr
        self.glicko = glicko
        self.rd = rd
        self.rank = rank
        self.bestrank = bestrank
        self.apm = apm
        self.pps = pps
        self.vs = vs
        self.standing = standing
        self.standing_local = standing_local

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryLeague":
        return cls(
            gamesplayed=data.get("gamesplayed", 0),
            gameswon=data.get("gameswon", 0),
            tr=data.get("tr", 0.0),
            glicko=data.get("glicko"),
            rd=data.get("rd"),
            rank=data.get("rank", "z"),
            bestrank=data.get("bestrank", "z"),
            apm=data.get("apm"),
            pps=data.get("pps"),
            vs=data.get("vs"),
            standing=data.get("standing", -1),
            standing_local=data.get("standing_local", -1),
        )

    def __repr__(self) -> str:
        return f"<UserSummaryLeague rank={self.rank!r} tr={self.tr!r}>"


class UserSummaryZen(BaseModel):
    """
    GET /users/:user/summaries/zen
    A summary of the user's ZEN progress.
    """

    def __init__(self, level: int, score: int):
        self.level = level
        self.score = score

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryZen":
        return cls(
            level=data.get("level", 0),
            score=data.get("score", 0),
        )

    def __repr__(self) -> str:
        return f"<UserSummaryZen level={self.level!r} score={self.score!r}>"


class UserSummaryAchievements(BaseModel):
    """
    GET /users/:user/summaries/achievements
    An object containing all the user's achievements.
    """

    def __init__(self, achievements: List[UserAchievement]):
        self.achievements = achievements

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryAchievements":
        raw_list = data if isinstance(data, list) else data.get("achievements", [])
        return cls(achievements=[UserAchievement.from_dict(a) for a in raw_list])

    def __repr__(self) -> str:
        return f"<UserSummaryAchievements count={len(self.achievements)}>"


class UserSummaryAll(BaseModel):
    """
    GET /users/:user/summaries
    All the user's summaries in one object.
    """

    def __init__(
        self,
        forty_lines: UserSummary40L,
        blitz: UserSummaryBlitz,
        zenith: UserSummaryZenith,
        zenithex: UserSummaryZenithEx,
        league: UserSummaryLeague,
        zen: UserSummaryZen,
        achievements: UserSummaryAchievements,
    ):
        self.forty_lines = forty_lines
        self.blitz = blitz
        self.zenith = zenith
        self.zenithex = zenithex
        self.league = league
        self.zen = zen
        self.achievements = achievements

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSummaryAll":
        return cls(
            forty_lines=UserSummary40L.from_dict(data.get("40l", {})),
            blitz=UserSummaryBlitz.from_dict(data.get("blitz", {})),
            zenith=UserSummaryZenith.from_dict(data.get("zenith", {})),
            zenithex=UserSummaryZenithEx.from_dict(data.get("zenithex", {})),
            league=UserSummaryLeague.from_dict(data.get("league", {})),
            zen=UserSummaryZen.from_dict(data.get("zen", {})),
            achievements=UserSummaryAchievements.from_dict(data.get("achievements", {})),
        )

    def __repr__(self) -> str:
        return "<UserSummaryAll>"


class UserRecord(BaseModel):
    """
    GET /users/:user/records/:gamemode/:leaderboard
    """

    def __init__(
        self,
        id: str,
        replayid: str,
        gamemode: str,
        userid: str,
        results: RecordResults,
        extras: Dict[str, Any],
        ts: Optional[str] = None,
    ):
        self.id = id
        self.replayid = replayid
        self.gamemode = gamemode
        self.userid = userid
        self.results = results
        self.extras = extras
        self.ts = ts

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserRecord":
        return cls(
            id=data.get("_id", ""),
            replayid=data.get("replayid", ""),
            gamemode=data.get("gamemode", ""),
            userid=data.get("userid", ""),
            results=RecordResults.from_dict(data.get("results", {})),
            extras=data.get("extras", {}),
            ts=data.get("ts"),
        )

    def __repr__(self) -> str:
        return f"<UserRecord id={self.id!r} gamemode={self.gamemode!r}>"
