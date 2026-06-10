from typing import Any, Dict, List, Optional
from .base import BaseModel


class RecordUser(BaseModel):
    """The user who set the record."""

    def __init__(
        self,
        id: str,
        username: str,
        country: Optional[str],
        supporter: bool,
        avatar_revision: Optional[int],
        banner_revision: Optional[int],
    ):
        self.id = id
        self.username = username
        self.country = country
        self.supporter = supporter
        self.avatar_revision = avatar_revision
        self.banner_revision = banner_revision

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordUser":
        return cls(
            id=data.get("id", data.get("_id", "")),
            username=data.get("username", ""),
            country=data.get("country"),
            supporter=data.get("supporter", False),
            avatar_revision=data.get("avatar_revision"),
            banner_revision=data.get("banner_revision"),
        )

    def __repr__(self) -> str:
        return f"<RecordUser id={self.id!r} username={self.username!r}>"


class RecordClears(BaseModel):
    """Clear type counts within a record's stats."""

    def __init__(
        self,
        singles: int,
        doubles: int,
        triples: int,
        quads: int,
        pentas: int,
        realtspins: int,
        minitspins: int,
        minitspinsingles: int,
        tspinsingles: int,
        minitspindoubles: int,
        tspindoubles: int,
        minitspintriples: int,
        tspintriples: int,
        minitspinquads: int,
        tspinquads: int,
        tspinpentas: int,
        allclear: int,
    ):
        self.singles = singles
        self.doubles = doubles
        self.triples = triples
        self.quads = quads
        self.pentas = pentas
        self.realtspins = realtspins
        self.minitspins = minitspins
        self.minitspinsingles = minitspinsingles
        self.tspinsingles = tspinsingles
        self.minitspindoubles = minitspindoubles
        self.tspindoubles = tspindoubles
        self.minitspintriples = minitspintriples
        self.tspintriples = tspintriples
        self.minitspinquads = minitspinquads
        self.tspinquads = tspinquads
        self.tspinpentas = tspinpentas
        self.allclear = allclear

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordClears":
        return cls(
            singles=data.get("singles", 0),
            doubles=data.get("doubles", 0),
            triples=data.get("triples", 0),
            quads=data.get("quads", 0),
            pentas=data.get("pentas", 0),
            realtspins=data.get("realtspins", 0),
            minitspins=data.get("minitspins", 0),
            minitspinsingles=data.get("minitspinsingles", 0),
            tspinsingles=data.get("tspinsingles", 0),
            minitspindoubles=data.get("minitspindoubles", 0),
            tspindoubles=data.get("tspindoubles", 0),
            minitspintriples=data.get("minitspintriples", 0),
            tspintriples=data.get("tspintriples", 0),
            minitspinquads=data.get("minitspinquads", 0),
            tspinquads=data.get("tspinquads", 0),
            tspinpentas=data.get("tspinpentas", 0),
            allclear=data.get("allclear", 0),
        )

    def __repr__(self) -> str:
        return f"<RecordClears quads={self.quads} allclear={self.allclear}>"


class RecordGarbage(BaseModel):
    """Garbage stats within a record."""

    def __init__(
        self,
        sent: int,
        sent_nomult: int,
        maxspike: int,
        maxspike_nomult: int,
        received: int,
        attack: int,
        cleared: int,
    ):
        self.sent = sent
        self.sent_nomult = sent_nomult
        self.maxspike = maxspike
        self.maxspike_nomult = maxspike_nomult
        self.received = received
        self.attack = attack
        self.cleared = cleared

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordGarbage":
        return cls(
            sent=data.get("sent", 0),
            sent_nomult=data.get("sent_nomult", 0),
            maxspike=data.get("maxspike", 0),
            maxspike_nomult=data.get("maxspike_nomult", 0),
            received=data.get("received", 0),
            attack=data.get("attack", 0),
            cleared=data.get("cleared", 0),
        )

    def __repr__(self) -> str:
        return f"<RecordGarbage sent={self.sent} received={self.received}>"


class RecordFinesse(BaseModel):
    """Finesse stats within a record."""

    def __init__(self, combo: int, faults: int, perfectpieces: int):
        self.combo = combo
        self.faults = faults
        self.perfectpieces = perfectpieces

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordFinesse":
        return cls(
            combo=data.get("combo", 0),
            faults=data.get("faults", 0),
            perfectpieces=data.get("perfectpieces", 0),
        )

    def __repr__(self) -> str:
        return f"<RecordFinesse faults={self.faults} perfectpieces={self.perfectpieces}>"


class RecordZenithStats(BaseModel):
    """Zenith-specific stats embedded in a record."""

    def __init__(
        self,
        altitude: float,
        rank: int,
        peakrank: int,
        avgrankpts: float,
        floor: int,
        targetingfactor: float,
        targetinggrace: float,
        totalbonus: float,
        revives: int,
        revives_total: int,
        revives_max_of_both: int,
        speedrun: bool,
        speedrun_seen: bool,
        splits: List[float],
    ):
        self.altitude = altitude
        self.rank = rank
        self.peakrank = peakrank
        self.avgrankpts = avgrankpts
        self.floor = floor
        self.targetingfactor = targetingfactor
        self.targetinggrace = targetinggrace
        self.totalbonus = totalbonus
        self.revives = revives
        self.revives_total = revives_total
        self.revives_max_of_both = revives_max_of_both
        self.speedrun = speedrun
        self.speedrun_seen = speedrun_seen
        self.splits = splits

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordZenithStats":
        return cls(
            altitude=data.get("altitude", 0.0),
            rank=data.get("rank", 0),
            peakrank=data.get("peakrank", 0),
            avgrankpts=data.get("avgrankpts", 0.0),
            floor=data.get("floor", 0),
            targetingfactor=data.get("targetingfactor", 0.0),
            targetinggrace=data.get("targetinggrace", 0.0),
            totalbonus=data.get("totalbonus", 0.0),
            revives=data.get("revives", 0),
            revives_total=data.get("revivesTotal", 0),
            revives_max_of_both=data.get("revivesMaxOfBoth", 0),
            speedrun=data.get("speedrun", False),
            speedrun_seen=data.get("speedrun_seen", False),
            splits=data.get("splits", []),
        )

    def __repr__(self) -> str:
        return f"<RecordZenithStats altitude={self.altitude} floor={self.floor}>"


class RecordStats(BaseModel):
    """Detailed per-game stats within a record."""

    def __init__(
        self,
        lines: int,
        level_lines: int,
        level_lines_needed: int,
        inputs: int,
        holds: int,
        score: int,
        zenlevel: int,
        zenprogress: int,
        level: int,
        combo: int,
        topcombo: int,
        combopower: float,
        btb: int,
        topbtb: int,
        btbpower: float,
        tspins: int,
        piecesplaced: int,
        clears: RecordClears,
        garbage: RecordGarbage,
        kills: int,
        finesse: RecordFinesse,
        zenith: RecordZenithStats,
        finaltime: float,
    ):
        self.lines = lines
        self.level_lines = level_lines
        self.level_lines_needed = level_lines_needed
        self.inputs = inputs
        self.holds = holds
        self.score = score
        self.zenlevel = zenlevel
        self.zenprogress = zenprogress
        self.level = level
        self.combo = combo
        self.topcombo = topcombo
        self.combopower = combopower
        self.btb = btb
        self.topbtb = topbtb
        self.btbpower = btbpower
        self.tspins = tspins
        self.piecesplaced = piecesplaced
        self.clears = clears
        self.garbage = garbage
        self.kills = kills
        self.finesse = finesse
        self.zenith = zenith
        self.finaltime = finaltime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordStats":
        return cls(
            lines=data.get("lines", 0),
            level_lines=data.get("level_lines", 0),
            level_lines_needed=data.get("level_lines_needed", 0),
            inputs=data.get("inputs", 0),
            holds=data.get("holds", 0),
            score=data.get("score", 0),
            zenlevel=data.get("zenlevel", 0),
            zenprogress=data.get("zenprogress", 0),
            level=data.get("level", 0),
            combo=data.get("combo", 0),
            topcombo=data.get("topcombo", 0),
            combopower=data.get("combopower", 0.0),
            btb=data.get("btb", 0),
            topbtb=data.get("topbtb", 0),
            btbpower=data.get("btbpower", 0.0),
            tspins=data.get("tspins", 0),
            piecesplaced=data.get("piecesplaced", 0),
            clears=RecordClears.from_dict(data.get("clears", {})),
            garbage=RecordGarbage.from_dict(data.get("garbage", {})),
            kills=data.get("kills", 0),
            finesse=RecordFinesse.from_dict(data.get("finesse", {})),
            zenith=RecordZenithStats.from_dict(data.get("zenith", {})),
            finaltime=data.get("finaltime", 0.0),
        )

    def __repr__(self) -> str:
        return f"<RecordStats finaltime={self.finaltime} piecesplaced={self.piecesplaced}>"


class RecordAggregateStats(BaseModel):
    """Aggregate stats (apm, pps, vsscore) within a record."""

    def __init__(self, apm: float, pps: float, vsscore: float):
        self.apm = apm
        self.pps = pps
        self.vsscore = vsscore

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordAggregateStats":
        return cls(
            apm=data.get("apm", 0.0),
            pps=data.get("pps", 0.0),
            vsscore=data.get("vsscore", 0.0),
        )

    def __repr__(self) -> str:
        return f"<RecordAggregateStats apm={self.apm} pps={self.pps} vsscore={self.vsscore}>"


class RecordResults(BaseModel):
    """The results block of a record."""

    def __init__(
        self,
        aggregatestats: RecordAggregateStats,
        stats: RecordStats,
        gameoverreason: str,
    ):
        self.aggregatestats = aggregatestats
        self.stats = stats
        self.gameoverreason = gameoverreason

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordResults":
        return cls(
            aggregatestats=RecordAggregateStats.from_dict(data.get("aggregatestats", {})),
            stats=RecordStats.from_dict(data.get("stats", {})),
            gameoverreason=data.get("gameoverreason", ""),
        )

    def __repr__(self) -> str:
        return f"<RecordResults gameoverreason={self.gameoverreason!r}>"


class RecordSortKey(BaseModel):
    """Sort key (p) of a record."""

    def __init__(self, pri: float, sec: float, ter: float):
        self.pri = pri
        self.sec = sec
        self.ter = ter

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordSortKey":
        return cls(
            pri=data.get("pri", 0.0),
            sec=data.get("sec", 0.0),
            ter=data.get("ter", 0.0),
        )

    def __repr__(self) -> str:
        return f"<RecordSortKey pri={self.pri}>"


class Record(BaseModel):
    """
    A single record from GET /records/:leaderboard or GET /records/reverse.
    """

    def __init__(
        self,
        id: str,
        replayid: str,
        stub: bool,
        gamemode: str,
        pb: bool,
        oncepb: bool,
        user: RecordUser,
        results: RecordResults,
        extras: Dict[str, Any],
        leaderboards: List[str],
        disputed: bool,
        p: RecordSortKey,
        ts: Optional[str] = None,
        revolution: Optional[str] = None,
        otherusers: Optional[List[RecordUser]] = None,
    ):
        self.id = id
        self.replayid = replayid
        self.stub = stub
        self.gamemode = gamemode
        self.pb = pb
        self.oncepb = oncepb
        self.ts = ts
        self.revolution = revolution
        self.user = user
        self.otherusers = otherusers or []
        self.leaderboards = leaderboards
        self.results = results
        self.extras = extras
        self.disputed = disputed
        self.p = p

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":
        user_data = data.get("user", {})
        return cls(
            id=data.get("_id", ""),
            replayid=data.get("replayid", ""),
            stub=data.get("stub", False),
            gamemode=data.get("gamemode", ""),
            pb=data.get("pb", False),
            oncepb=data.get("oncepb", False),
            ts=data.get("ts"),
            revolution=data.get("revolution"),
            user=RecordUser.from_dict(user_data) if user_data else RecordUser.from_dict({}),
            otherusers=[RecordUser.from_dict(u) for u in data.get("otherusers", [])],
            leaderboards=data.get("leaderboards", []),
            results=RecordResults.from_dict(data.get("results", {})),
            extras=data.get("extras", {}),
            disputed=data.get("disputed", False),
            p=RecordSortKey.from_dict(data.get("p", {})),
        )

    def __repr__(self) -> str:
        return f"<Record id={self.id!r} gamemode={self.gamemode!r}>"
