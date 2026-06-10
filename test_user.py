from teto import TetoClient

TEST_USER = "nplui"

client = TetoClient()


def section(title: str):
    print(f"\n{'='*40}")
    print(f"  {title}")
    print('='*40)


def test_get_user():
    section("get_user")
    user = client.get_user(TEST_USER)
    print(repr(user))
    print(f"  id          : {user.id}")
    print(f"  username    : {user.username}")
    print(f"  role        : {user.role}")
    print(f"  xp          : {user.xp}")
    print(f"  gamesplayed : {user.gamesplayed}")
    print(f"  gameswon    : {user.gameswon}")
    print(f"  gametime    : {user.gametime}")
    print(f"  country     : {user.country}")
    print(f"  supporter   : {user.supporter}")
    print(f"  verified    : {user.verified}")
    print(f"  bio         : {user.bio}")
    print(f"  friend_count: {user.friend_count}")


def test_get_user_summary_40l():
    section("get_user_summary_40l")
    s = client.get_user_summary_40l(TEST_USER)
    print(repr(s))
    print(f"  rank       : {s.rank}")
    print(f"  rank_local : {s.rank_local}")
    print(f"  record     : {s.record}")


def test_get_user_summary_blitz():
    section("get_user_summary_blitz")
    s = client.get_user_summary_blitz(TEST_USER)
    print(repr(s))
    print(f"  rank       : {s.rank}")
    print(f"  rank_local : {s.rank_local}")
    print(f"  record     : {s.record}")


def test_get_user_summary_zenith():
    section("get_user_summary_zenith")
    s = client.get_user_summary_zenith(TEST_USER)
    print(repr(s))
    print(f"  record : {s.record}")
    print(f"  best   : {s.best}")


def test_get_user_summary_zenithex():
    section("get_user_summary_zenithex")
    s = client.get_user_summary_zenithex(TEST_USER)
    print(repr(s))
    print(f"  record : {s.record}")
    print(f"  best   : {s.best}")


def test_get_user_summary_league():
    section("get_user_summary_league")
    s = client.get_user_summary_league(TEST_USER)
    print(repr(s))
    print(f"  tr              : {s.tr}")
    print(f"  glicko          : {s.glicko}")
    print(f"  rd              : {s.rd}")
    print(f"  rank            : {s.rank}")
    print(f"  bestrank        : {s.bestrank}")
    print(f"  apm             : {s.apm}")
    print(f"  pps             : {s.pps}")
    print(f"  vs              : {s.vs}")
    print(f"  standing        : {s.standing}")
    print(f"  standing_local  : {s.standing_local}")
    print(f"  gamesplayed     : {s.gamesplayed}")
    print(f"  gameswon        : {s.gameswon}")


def test_get_user_summary_zen():
    section("get_user_summary_zen")
    s = client.get_user_summary_zen(TEST_USER)
    print(repr(s))
    print(f"  level : {s.level}")
    print(f"  score : {s.score}")


def test_get_user_summary_achievements():
    section("get_user_summary_achievements")
    s = client.get_user_summary_achievements(TEST_USER)
    print(repr(s))
    print(f"  count : {len(s.achievements)}")
    if s.achievements:
        print(f"  first : {s.achievements[0]}")


def test_get_user_summaries():
    section("get_user_summaries (all)")
    s = client.get_user_summaries(TEST_USER)
    print(repr(s))
    print(f"  forty_lines : {repr(s.forty_lines)}")
    print(f"  blitz       : {repr(s.blitz)}")
    print(f"  zenith      : {repr(s.zenith)}")
    print(f"  zenithex    : {repr(s.zenithex)}")
    print(f"  league      : {repr(s.league)}")
    print(f"  zen         : {repr(s.zen)}")
    print(f"  achievements: {repr(s.achievements)}")


def test_get_user_records():
    section("get_user_records (40l/top)")
    records = client.get_user_records(TEST_USER, "40l", "top", limit=3)
    print(f"  count: {len(records)}")
    for r in records:
        print(f"  {repr(r)}")
        print(f"    userid   : {r.userid}")
        print(f"    gamemode : {r.gamemode}")
        print(f"    ts       : {r.ts}")
        print(f"    results  : {r.results}")


if __name__ == "__main__":
    test_get_user()
    test_get_user_summary_40l()
    test_get_user_summary_blitz()
    test_get_user_summary_zenith()
    test_get_user_summary_zenithex()
    test_get_user_summary_league()
    test_get_user_summary_zen()
    test_get_user_summary_achievements()
    test_get_user_summaries()
    test_get_user_records()

    client.close()
    print("\n[done]")
