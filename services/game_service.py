from utils.formatters import get_team_name
from utils.globals import (
    SEASON_DEFAULT,
    SEASON_TYPE_DEFAULT,
    datetime,
    pd,
    requests,
    timedelta,
)
from utils.headers import default_headers
from utils.helpers import formatar_season_type_para_url, traduzir_posicao_para_ptbr
from utils.scraper import get_with_cloudscraper


def buscar_game_log(player_id, num_jogos=5):
    season_type_param = formatar_season_type_para_url(SEASON_TYPE_DEFAULT)
    url = f"https://stats.nba.com/stats/playergamelog?PlayerID={player_id}&Season={SEASON_DEFAULT}&SeasonType={season_type_param}"

    response = requests.get(url, headers=default_headers, timeout=10)
    data = response.json()
    result = data["resultSets"][0]
    headers = result["headers"]
    valores = result["rowSet"]
    df = pd.DataFrame(valores, columns=headers)
    df["GAME_DATE"] = pd.to_datetime(
        df["GAME_DATE"], format="mixed", dayfirst=False, errors="coerce"
    )
    df = (
        df.sort_values("GAME_DATE", ascending=False)
        .head(num_jogos)
        .reset_index(drop=True)
    )

    return df


def buscar_posicao_jogador(player_id):
    try:
        url = f"https://stats.nba.com/stats/commonplayerinfo?PlayerID={player_id}"

        response = requests.get(url, headers=default_headers, timeout=10)
        data = response.json()
        result = data["resultSets"][0]
        headers = result["headers"]
        row = result["rowSet"][0]
        player_info = dict(zip(headers, row))
        posicao_original = player_info.get("POSITION", "Desconhecida")

        return traduzir_posicao_para_ptbr(posicao_original)
    except Exception as e:
        print(f"❌ Erro ao buscar posição do jogador: {e}")
        return "Desconhecida"


def buscar_game_log_time(team_id, num_jogos):
    if not isinstance(team_id, int):
        print(f"❌ Erro: team_id inválido ({team_id}). Esperado um número inteiro.")
        return pd.DataFrame()

    url = "https://stats.nba.com/stats/teamgamelog"
    params = {
        "TeamID": team_id,
        "Season": SEASON_DEFAULT,
        "SeasonType": SEASON_TYPE_DEFAULT,
    }

    result = get_with_cloudscraper(url, params=params)

    if not result:
        print("❌ Nenhum dado retornado da NBA.")
        return pd.DataFrame()

    try:
        headers = result["resultSets"][0]["headers"]
        rows = result["resultSets"][0]["rowSet"]
        df = pd.DataFrame(rows, columns=headers)
        return df.head(num_jogos)
    except Exception as e:
        print(f"⚠️ Erro ao processar o JSON retornado: {e}")
        return pd.DataFrame()


def listar_jogos_hoje():
    hoje = datetime.now().strftime("%Y-%m-%d")
    # ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate={hoje}"

    try:
        response = requests.get(url, headers=default_headers, timeout=10)
        print(f"Status code: {response.status_code}")

        if response.status_code != 200:
            print("❌ Falha ao acessar API da NBA.")
            return []

        data = response.json()
        result_set = data["resultSets"][0]
        headers = result_set["headers"]
        jogos = result_set["rowSet"]

        idx_home = headers.index("HOME_TEAM_ID")
        idx_away = headers.index("VISITOR_TEAM_ID")

        jogos_disponiveis = []

        for jogo in jogos:
            home_id = jogo[idx_home]
            away_id = jogo[idx_away]

            home_name = get_team_name(home_id)
            away_name = get_team_name(away_id)

            jogos_disponiveis.append(
                {
                    "home_team_id": home_id,
                    "home_team_name": home_name,
                    "away_team_id": away_id,
                    "away_team_name": away_name,
                    "resumo": f"🛫 {away_name} vs 🏠 {home_name}",
                }
            )

        return jogos_disponiveis

    except Exception as e:
        print(f"⚠️ Erro ao buscar jogos de hoje: {e}")
        return []
