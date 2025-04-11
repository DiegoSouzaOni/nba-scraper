from utils.globals import requests, pd


def buscar_lideres_liga(stat="PTS", season="2024-25", season_type="Regular Season"):
    url = "https://stats.nba.com/stats/leagueLeaders"
    params = {
        "LeagueID": "00",
        "PerMode": "PerGame",
        "Scope": "S",
        "Season": season,
        "SeasonType": season_type,
        "StatCategory": stat
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nba.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    headers = data['resultSet']['headers']
    rows = data['resultSet']['rowSet']
    return pd.DataFrame(rows, columns=headers)