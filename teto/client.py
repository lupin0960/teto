import uuid
from typing import List, Optional, Type

from .http_engines import HttpEngine, SyncEngine, AsyncEngine
from .models import (
    BaseModel,
    User,
    UserSummary40L,
    UserSummaryBlitz,
    UserSummaryZenith,
    UserSummaryZenithEx,
    UserSummaryLeague,
    UserSummaryZen,
    UserSummaryAchievements,
    UserSummaryAll,
    UserRecord,
    ServerStats,
    ServerActivity,
    Record,
    NewsItem,
    LabsScoreflow,
    LabsLeagueflow,
    LabsLeagueRanks,
    Achievement,
    AchievementEntry,
)


def _handle_response(model_cls: Type[BaseModel], raw_data: dict) -> BaseModel:
    return model_cls.from_dict(raw_data)


class TetoClient:
    BASE_URL = "https://ch.tetr.io/api"

    engine: HttpEngine

    def __init__(self, session_id: Optional[str] = None, async_mode: bool = False):
        self.session_id = session_id or str(uuid.uuid4())
        self.async_mode = async_mode

        if self.async_mode:
            self.engine = AsyncEngine(self.session_id)
        else:
            self.engine = SyncEngine(self.session_id)

    def get_request(self, url: str):
        api_url = f"{self.BASE_URL}/{url}"
        res = self.engine.request(api_url)
        return res

    def close(self):
        return self.engine.close()

    # -------------------------
    # General endpoints
    # -------------------------

    def get_server_stats(self) -> ServerStats:
        """GET /general/stats"""
        data = self.get_request("general/stats")
        return ServerStats.from_dict(data)

    def get_server_activity(self) -> ServerActivity:
        """GET /general/activity"""
        data = self.get_request("general/activity")
        return ServerActivity.from_dict(data)

    # -------------------------
    # User endpoints
    # -------------------------

    def get_user(self, user: str) -> User:
        """GET /users/:user — fetch a user's info by username or ID."""
        data = self.get_request(f"users/{user}")
        return User.from_dict(data)

    def get_user_summary_40l(self, user: str) -> UserSummary40L:
        """GET /users/:user/summaries/40l"""
        data = self.get_request(f"users/{user}/summaries/40l")
        return UserSummary40L.from_dict(data)

    def get_user_summary_blitz(self, user: str) -> UserSummaryBlitz:
        """GET /users/:user/summaries/blitz"""
        data = self.get_request(f"users/{user}/summaries/blitz")
        return UserSummaryBlitz.from_dict(data)

    def get_user_summary_zenith(self, user: str) -> UserSummaryZenith:
        """GET /users/:user/summaries/zenith"""
        data = self.get_request(f"users/{user}/summaries/zenith")
        return UserSummaryZenith.from_dict(data)

    def get_user_summary_zenithex(self, user: str) -> UserSummaryZenithEx:
        """GET /users/:user/summaries/zenithex"""
        data = self.get_request(f"users/{user}/summaries/zenithex")
        return UserSummaryZenithEx.from_dict(data)

    def get_user_summary_league(self, user: str) -> UserSummaryLeague:
        """GET /users/:user/summaries/league"""
        data = self.get_request(f"users/{user}/summaries/league")
        return UserSummaryLeague.from_dict(data)

    def get_user_summary_zen(self, user: str) -> UserSummaryZen:
        """GET /users/:user/summaries/zen"""
        data = self.get_request(f"users/{user}/summaries/zen")
        return UserSummaryZen.from_dict(data)

    def get_user_summary_achievements(self, user: str) -> UserSummaryAchievements:
        """GET /users/:user/summaries/achievements"""
        data = self.get_request(f"users/{user}/summaries/achievements")
        return UserSummaryAchievements.from_dict(data)

    def get_user_summaries(self, user: str) -> UserSummaryAll:
        """GET /users/:user/summaries — all summaries in one request."""
        data = self.get_request(f"users/{user}/summaries")
        return UserSummaryAll.from_dict(data)

    def search_users(self, query: str) -> List[User]:
        """GET /users/search/:query — search users by username."""
        data = self.get_request(f"users/search/{query}")
        users = data if isinstance(data, list) else data.get("users", [])
        return [User.from_dict(u) for u in users]

    def get_leaderboard(
        self,
        leaderboard: str,
        before: Optional[float] = None,
        after: Optional[float] = None,
        limit: Optional[int] = None,
        country: Optional[str] = None,
    ) -> List[User]:
        """
        GET /users/by/:leaderboard
        leaderboard: 'league', 'xp', 'ar', ...
        """
        params = []
        if before is not None:
            params.append(f"before={before}")
        if after is not None:
            params.append(f"after={after}")
        if limit is not None:
            params.append(f"limit={limit}")
        if country is not None:
            params.append(f"country={country}")
        url = f"users/by/{leaderboard}"
        if params:
            url += "?" + "&".join(params)
        data = self.get_request(url)
        entries = data if isinstance(data, list) else data.get("entries", [])
        return [User.from_dict(e) for e in entries]

    def get_historical_leaderboard(
        self,
        leaderboard: str,
        season: str,
        before: Optional[float] = None,
        after: Optional[float] = None,
        limit: Optional[int] = None,
        country: Optional[str] = None,
    ) -> List[User]:
        """
        GET /users/history/:leaderboard/:season
        leaderboard: 'league'
        season: e.g. '1'
        """
        params = []
        if before is not None:
            params.append(f"before={before}")
        if after is not None:
            params.append(f"after={after}")
        if limit is not None:
            params.append(f"limit={limit}")
        if country is not None:
            params.append(f"country={country}")
        url = f"users/history/{leaderboard}/{season}"
        if params:
            url += "?" + "&".join(params)
        data = self.get_request(url)
        entries = data if isinstance(data, list) else data.get("entries", [])
        return [User.from_dict(e) for e in entries]

    def get_user_records(
        self,
        user: str,
        gamemode: str,
        leaderboard: str,
        before: Optional[float] = None,
        after: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> List[UserRecord]:
        """
        GET /users/:user/records/:gamemode/:leaderboard
        gamemode: '40l', 'blitz', 'zenith', 'zenithex'
        leaderboard: 'top', 'recent', 'progression'
        """
        params = []
        if before is not None:
            params.append(f"before={before}")
        if after is not None:
            params.append(f"after={after}")
        if limit is not None:
            params.append(f"limit={limit}")
        url = f"users/{user}/records/{gamemode}/{leaderboard}"
        if params:
            url += "?" + "&".join(params)
        data = self.get_request(url)
        entries = data if isinstance(data, list) else data.get("entries", [])
        return [UserRecord.from_dict(r) for r in entries]

    # -------------------------
    # Records endpoints
    # -------------------------

    def get_records_leaderboard(
        self,
        leaderboard: str,
        before: Optional[float] = None,
        after: Optional[float] = None,
        limit: Optional[int] = None,
        country: Optional[str] = None,
    ) -> List[Record]:
        """
        GET /records/:leaderboard
        leaderboard: e.g. '40l_global', 'blitz_global', '40l_country_KR'
        """
        params = []
        if before is not None:
            params.append(f"before={before}")
        if after is not None:
            params.append(f"after={after}")
        if limit is not None:
            params.append(f"limit={limit}")
        if country is not None:
            params.append(f"country={country}")
        url = f"records/{leaderboard}"
        if params:
            url += "?" + "&".join(params)
        data = self.get_request(url)
        entries = data if isinstance(data, list) else data.get("entries", [])
        return [Record.from_dict(r) for r in entries]

    def search_record(
        self,
        gamemode: str,
        ts: str,
        user: Optional[str] = None,
    ) -> Optional[Record]:
        """
        GET /records/reverse
        gamemode: '40l', 'blitz', etc.
        ts: ISO 8601 timestamp
        user: optional user ID
        """
        params = [f"gamemode={gamemode}", f"ts={ts}"]
        if user is not None:
            params.append(f"user={user}")
        url = "records/reverse?" + "&".join(params)
        data = self.get_request(url)
        if data is None:
            return None
        return Record.from_dict(data)

    # -------------------------
    # News endpoints
    # -------------------------

    def get_all_news(self, limit: Optional[int] = None) -> List[NewsItem]:
        """
        GET /news/
        The latest news items in any stream.
        """
        url = "news/"
        if limit is not None:
            url += f"?limit={limit}"
        data = self.get_request(url)
        news = data if isinstance(data, list) else data.get("news", [])
        return [NewsItem.from_dict(n) for n in news]

    def get_news(self, stream: str, limit: Optional[int] = None) -> List[NewsItem]:
        """
        GET /news/:stream
        stream: 'global' or 'user_{user_id}'
        """
        url = f"news/{stream}"
        if limit is not None:
            url += f"?limit={limit}"
        data = self.get_request(url)
        news = data if isinstance(data, list) else data.get("news", [])
        return [NewsItem.from_dict(n) for n in news]

    # -------------------------
    # Labs endpoints
    # -------------------------

    def get_labs_scoreflow(self, user: str, gamemode: str) -> LabsScoreflow:
        """GET /labs/scoreflow/:user/:gamemode"""
        data = self.get_request(f"labs/scoreflow/{user}/{gamemode}")
        return LabsScoreflow.from_dict(data)

    def get_labs_leagueflow(self, user: str) -> LabsLeagueflow:
        """GET /labs/leagueflow/:user"""
        data = self.get_request(f"labs/leagueflow/{user}")
        return LabsLeagueflow.from_dict(data)

    def get_labs_league_ranks(self) -> LabsLeagueRanks:
        """GET /labs/league_ranks"""
        data = self.get_request("labs/league_ranks")
        return LabsLeagueRanks.from_dict(data)

    # -------------------------
    # Achievements endpoints
    # -------------------------

    def get_achievement(self, k: int) -> Achievement:
        """GET /achievements/:k"""
        data = self.get_request(f"achievements/{k}")
        return Achievement.from_dict(data)

    def get_achievement_entries(
        self,
        k: int,
        before: Optional[float] = None,
        after: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> List[AchievementEntry]:
        """GET /achievements/:k/entries"""
        params = []
        if before is not None:
            params.append(f"before={before}")
        if after is not None:
            params.append(f"after={after}")
        if limit is not None:
            params.append(f"limit={limit}")
        url = f"achievements/{k}/entries"
        if params:
            url += "?" + "&".join(params)
        data = self.get_request(url)
        entries = data if isinstance(data, list) else data.get("entries", [])
        return [AchievementEntry.from_dict(e) for e in entries]
