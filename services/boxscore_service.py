from utils.globals import pd
from utils.scraper import get_with_cloudscraper


def obter_boxscore_summary(game_id):
    url = "https://stats.nba.com/stats/boxscoresummaryv2"
    params = {"GameID": game_id}
    result = get_with_cloudscraper(url, params=params)

    if not result:
        print(f"⚠️ Nenhum resultado para o game_id {game_id}")
        return None

    try:
        for resultset in result["resultSets"]:
            if resultset["name"] == "LineScore":
                headers = resultset["headers"]
                rows = resultset["rowSet"]
                return pd.DataFrame(rows, columns=headers)
        return None
    except Exception as e:
        print(f"⚠️ Erro ao processar boxscore summary: {e}")
        return None



def obter_boxscore(game_id):
    """
    Retorna o boxscore completo do jogo (estatísticas dos dois times).
    """
    url = "https://stats.nba.com/stats/boxscoretraditionalv2"
    params = {
        "GameID": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10
    }

    result = get_with_cloudscraper(url, params=params)

    if not result:
        print(f"❌ Erro ao buscar boxscore para o jogo {game_id}.")
        return None

    try:
        headers = result["resultSets"][1]["headers"]  # index 1 = Team Stats
        rows = result["resultSets"][1]["rowSet"]
        df = pd.DataFrame(rows, columns=headers)
        return df
    except Exception as e:
        print(f"⚠️ Erro ao processar o boxscore: {e}")
        return None


def extrair_dados_boxscore(df_boxscore, team_id):
    """
    Dado o DataFrame do boxscore, retorna os pontos feitos, sofridos,
    pontos no 1º quarto e sofridos no 1º quarto para o time fornecido.
    """
    if df_boxscore is None or df_boxscore.empty:
        return None, None, None, None
    
    print(f"📊 Extraindo dados do boxscore para o time ID {team_id}...")
    print(f"📊 Dados do boxscore: {df_boxscore}")
    print(f"📊 Dados do boxscore: {df_boxscore.head()}")

    try:
        team_data = df_boxscore[df_boxscore['TEAM_ID'] == team_id]
        adversario_data = df_boxscore[df_boxscore['TEAM_ID'] != team_id]

        if team_data.empty or adversario_data.empty:
            return None, None, None, None

        pts_feitos = int(team_data.iloc[0]['PTS'])
        pts_sofridos = int(adversario_data.iloc[0]['PTS'])

        q1_feitos = int(team_data.iloc[0].get('PTS_QTR1', 0))
        q1_sofridos = int(adversario_data.iloc[0].get('PTS_QTR1', 0))

        return pts_feitos, pts_sofridos, q1_feitos, q1_sofridos
    except Exception as e:
        print(f"⚠️ Erro ao extrair dados do boxscore: {e}")
        return None, None, None, None


def extrair_pontos_quarto_e_sofridos(df, team_id):
    if df is None or df.empty:
        return None, None

    try:
        df = df.copy()
        df["TEAM_ID"] = df["TEAM_ID"].astype(int)

        team_data = df[df["TEAM_ID"] == team_id]
        adversario_data = df[df["TEAM_ID"] != team_id]

        if team_data.empty or adversario_data.empty:
            return None, None

        q1_feitos = int(team_data.iloc[0].get("PTS_QTR1", 0))
        q1_sofridos = int(adversario_data.iloc[0].get("PTS_QTR1", 0))

        return q1_feitos, q1_sofridos
    except Exception as e:
        print(f"⚠️ Erro ao extrair dados do 1º quarto: {e}")
        return None, None
