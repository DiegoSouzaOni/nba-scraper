from utils.globals import unidecode, requests, json, os, pd, SEASON_DEFAULT
from utils.headers import default_headers
from clients.nba_api_client import NBAApiClient


def get_player_stats(player_id: str, season: str = "2024-25"):
    """
    Get statistics for a specific player.
    """
    endpoint = "playergamelog"
    params = {
        "PlayerID": player_id,
        "Season": season,
        "SeasonType": "Regular Season"
    }

    client = NBAApiClient(endpoint, params)
    data = client.get()

    if not data:
        print("[PlayerService] No data returned.")
        return {}

    return data.get("resultSets", [])


def extrair_ppg(df, jogador):
    linha = df[df["PLAYER"] == jogador]
    if not linha.empty:
        return float(linha["PTS"].values[0])
    return None


def extrair_rpg(df, jogador):
    linha = df[df["PLAYER"] == jogador]
    if not linha.empty:
        return float(linha["REB"].values[0])
    return None


def extrair_apg(df, jogador):
    linha = df[df["PLAYER"] == jogador]
    if not linha.empty:
        return float(linha["AST"].values[0])
    return None


def buscar_player_id(nome_jogador, debug=False, usar_cache=True):
    url = "https://stats.nba.com/stats/commonallplayers"
    params = {
        "LeagueID": "00",
        "Season": "2024-25",
        "IsOnlyCurrentSeason": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nba.com/"
    }

    cache_file = "jogadores_nba.json"

    try:
        if usar_cache and os.path.exists(cache_file):
            if debug: print("🔁 Carregando cache local de jogadores.")
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            if debug: print("🌐 Baixando dados da API da NBA...")
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Salva localmente o JSON se quiser cache
            if usar_cache:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        players = data["resultSets"][0]["rowSet"]
        headers = data["resultSets"][0]["headers"]
        idx_nome = headers.index("DISPLAY_FIRST_LAST")
        idx_id = headers.index("PERSON_ID")

        nome_normalizado = unidecode(nome_jogador.lower())

        for player in players:
            nome_atual = unidecode(player[idx_nome].lower())
            if nome_normalizado in nome_atual:
                if debug:
                    print(f"✅ Jogador encontrado: {player[idx_nome]} (ID: {player[idx_id]})")
                return player[idx_id]

        print(f"❌ Jogador '{nome_jogador}' não encontrado.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar a API da NBA: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao buscar ID do jogador: {e}")
        return None


def buscar_team_id_por_nome(team_name):
    """
    Busca o ID de um time a partir do nome completo ou parte dele.
    """
    url = "https://cdn.nba.com/static/json/staticData/teamList.json"
    response = requests.get(url)
    data = response.json()

    teams = data['league']['standard']

    for team in teams:
        full_name = f"{team['city']} {team['nickname']}"
        if team_name.lower() in full_name.lower():
            return team['teamId']

    return None


def buscar_jogadores_por_time(team_id):
    url = "https://stats.nba.com/stats/commonteamroster"
    params = {
        "TeamID": team_id,
        "Season": SEASON_DEFAULT
    }

    response = requests.get(url, headers=default_headers, params=params)
    response.raise_for_status()

    data = response.json()
    jogadores = pd.DataFrame(data["resultSets"][0]["rowSet"], columns=data["resultSets"][0]["headers"])
    
    nomes = jogadores["PLAYER"].tolist()
    return nomes