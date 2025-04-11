from services.game_service import buscar_ultimos_jogos_do_time


def calcular_media_pontos_sofridos_por_posicao(team_id, num_jogos=5):
    """
    Retorna a média de pontos sofridos por um time contra cada posição nos últimos jogos.
    """
    jogos = buscar_ultimos_jogos_do_time(team_id, num_jogos=num_jogos)
    if jogos.empty:
        return {}

    media_por_posicao = jogos.groupby('posicao_adversario')['pontos_sofridos'].mean().to_dict()
    return media_por_posicao