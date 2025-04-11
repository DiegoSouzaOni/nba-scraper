from services.game_service import buscar_game_log_time
from services.estatisticas_service import calcular_medias_boxscore_summary
from utils.globals import pd


def buscar_ultimos_jogos(team_id, num_jogos=5):
    """
    Busca os últimos jogos de um time.
    """
    df = buscar_game_log_time(team_id, num_jogos)
    return df.head(num_jogos)


def arredondar(valor):
    try:
        return round(float(valor), 2)
    except (ValueError, TypeError):
        return "N/D"


def comparar_times(jogos_time1, jogos_time2):
    team_id1 = jogos_time1.iloc[0]["Team_ID"]
    team_id2 = jogos_time2.iloc[0]["Team_ID"]
    
    (
        media1_pts_feitos,
        media1_pts_sofridos,
        media1_q1_feitos,
        media1_q1_sofridos
    ) = calcular_medias_boxscore_summary(jogos_time1, team_id1)

    (
        media2_pts_feitos,
        media2_pts_sofridos,
        media2_q1_feitos,
        media2_q1_sofridos
    ) = calcular_medias_boxscore_summary(jogos_time2, team_id2)

    # Estrutura organizada para DataFrame
    data = {
        "Métrica": [
            "Pontos Feitos",
            "Pontos Sofridos",
            "1º Quarto Feitos",
            "1º Quarto Sofridos"
        ],
        "Visitante": [
            arredondar(media1_pts_feitos),
            arredondar(media1_pts_sofridos),
            arredondar(media1_q1_feitos),
            arredondar(media1_q1_sofridos),
        ],
        "Casa": [
            arredondar(media2_pts_feitos),
            arredondar(media2_pts_sofridos),
            arredondar(media2_q1_feitos),
            arredondar(media2_q1_sofridos),
        ],
    }

    return pd.DataFrame(data)