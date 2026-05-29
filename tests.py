from teto import TetoClient

username = "moonlightyx"

client = TetoClient()

# General
stats = client.get_server_stats()
print(stats)

activity = client.get_server_activity()
print(activity)

# Records leaderboard
records = client.get_records_leaderboard("40l_global", limit=3)
for r in records:
    print(r)

# News
news = client.get_news("global", limit=3)
for n in news:
    print(n)

# Labs
sf = client.get_labs_scoreflow(username, "40l")
print(sf)

lf = client.get_labs_leagueflow(username)
print(lf)

lr = client.get_labs_league_ranks()
print(lr)

# Achievements
ach = client.get_achievement(1)
print(ach)

entries = client.get_achievement_entries(1, limit=3)
for e in entries:
    print(e)

client.close()
