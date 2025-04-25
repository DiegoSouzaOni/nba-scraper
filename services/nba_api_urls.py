class NBAApiURLs:
    BASE = "https://stats.nba.com/stats"

    @staticmethod
    def games_today():
        return f"{NBAApiURLs.BASE}/scoreboardV2?DayOffset=0"

    @staticmethod
    def game_stats(game_id: str):
        return f"{NBAApiURLs.BASE}/boxscoretraditionalv2?GameID={game_id}&StartPeriod=0&EndPeriod=14&RangeType=0"
