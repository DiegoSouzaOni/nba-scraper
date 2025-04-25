from clients.nba_api_client import NBAApiClient
from utils.globals import datetime
from endpoints.base_endpoint import BaseEndpoint


class GameEndpoint:
    def __init__(self):
        super().__init__()
        self.client = NBAApiClient()

    def get_today_games(self):
        today = datetime.now().strftime("%m/%d/%Y")

        endpoint_obj = BaseEndpoint(
            endpoint="scoreboardv2",
            params={
                "LeagueID": "00",
                "DayOffset": "0",
                "GameDate": today
            }
        )

        return self.client.get(endpoint_obj)

    def get_game_stats(self, game_id):
        endpoint_obj = BaseEndpoint(
            endpoint="boxscoretraditionalv2",
            params={
                "GameID": game_id,
                "StartPeriod": 0,
                "EndPeriod": 10,
                "StartRange": 0,
                "EndRange": 0,
                "RangeType": 0
            }
        )
        return self.client.get(endpoint_obj)

    def get_boxscore(self, game_id):
        endpoint_obj = BaseEndpoint(
            endpoint="boxscoresummaryv2",
            params={
                "GameID": game_id
            }
        )
        return self.client.get(endpoint_obj)
