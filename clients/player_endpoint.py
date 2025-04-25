from clients.nba_api_client import NBAApiClient
from endpoints.base_endpoint import BaseEndpoint
from utils.globals import SEASON_DEFAULT, SEASON_TYPE_DEFAULT, PER_MODE_DEFAULT, SEASON_TYPE_PLAYOFFS


class PlayerEndpoint:
    def __init__(self):
        self.client = NBAApiClient()

    def get_player_stats(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="playerdashboardbygeneralsplits",
            params={
                "PlayerID": player_id,
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT
            }
        )
        return self.client.get(endpoint_obj)

    def get_player_gamelog(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="playergamelog",
            params={
                "PlayerID": player_id,
                "Season": SEASON_DEFAULT,
                # "SeasonType": SEASON_TYPE_DEFAULT change to this option when season restarts
                "SeasonType": SEASON_TYPE_PLAYOFFS
            }
        )
        return self.client.get(endpoint_obj)

    def get_player_profile(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="commonplayerinfo",
            params={
                "PlayerID": player_id
            }
        )
        return self.client.get(endpoint_obj)
    
    def get_player_stats_career(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="playercareerstats",
            params={
                "PlayerID": player_id
            }
        )
        return self.client.get(endpoint_obj)
    
    def get_player_next_games(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="playernextngames",
            params={
                "PlayerID": player_id,
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT
            }
        )
        return self.client.get(endpoint_obj)
    
    def get_player_season_stats(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="playerprofilev2",
            params={
                "PlayerID": player_id,
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT
            }
        )
        return self.client.get(endpoint_obj)

    def get_all_players_season_stats(self):
        endpoint_obj = BaseEndpoint(
            endpoint="leaguedashplayerstats",
            params={
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT,
                "PerMode": PER_MODE_DEFAULT
            }
        )
        return self.client.get(endpoint_obj)
    
    def get_player_clutch_stats(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="leaguedashplayerclutch",
            params={
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT,
                "PerMode": "PerGame",
                "PlayerID": player_id,
                "MeasureType": "Base",
                "ClutchTime": "Last 5 Minutes",
                "AheadBehind": "Ahead or Behind",
                "PointDiff": 5
            }
        )

        return self.client.get(endpoint_obj)

    def get_player_shooting_stats(self, player_id):
        endpoint_obj = BaseEndpoint(
            endpoint="leaguedashplayerptshot",
            params={
                "Season": SEASON_DEFAULT,
                "SeasonType": SEASON_TYPE_DEFAULT,
                "PerMode": "PerGame",
                "PlayerID": player_id
            }
        )
        return self.client.get(endpoint_obj)
    
    def get_all_players(self):
        endpoint_obj = BaseEndpoint(
            endpoint="commonallplayers",
            params={
                "LeagueID": "00",
                "Season": SEASON_DEFAULT,
                "IsOnlyCurrentSeason": "1"
            }
        )
        return self.client.get(endpoint_obj)
