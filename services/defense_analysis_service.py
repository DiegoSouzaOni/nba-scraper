import json

from services.boxscore_service import obter_boxscore
from utils.globals import json, pd


def calcular_media_pontos_sofridos_por_posicao(jogos_df: pd.DataFrame) -> dict:
    print("Iniciando cálculo de média de pontos sofridos por posição...")

    if jogos_df.empty:
        print("DataFrame está vazio.")
        return {}

    if "opponent_stats" not in jogos_df.columns:
        print("Coluna 'opponent_stats' não encontrada no DataFrame.")
        return {}

    media_por_posicao = {}

    for index, row in jogos_df.iterrows():
        raw_stats = row.get("opponent_stats", {})
        print(f"\nLinha {index} - opponent_stats (raw): {raw_stats}")

        if isinstance(raw_stats, str):
            try:
                raw_stats = json.loads(raw_stats)
                print(f"Linha {index} - opponent_stats (json carregado): {raw_stats}")
            except Exception as e:
                print(f"Erro ao converter JSON em linha {index}: {e}")
                continue

        if not isinstance(raw_stats, dict):
            print(f"Linha {index} - opponent_stats não é um dicionário após conversão.")
            continue

        for posicao, pontos in raw_stats.items():
            print(f"  Posição: {posicao} | Pontos: {pontos}")
            try:
                pontos = float(pontos)
                media_por_posicao.setdefault(posicao, []).append(pontos)
            except ValueError:
                print(f"  Valor inválido para pontos: {pontos}")
                continue

    print("\nCálculo das médias:")
    for posicao, valores in media_por_posicao.items():
        media = round(sum(valores) / len(valores), 2) if valores else 0
        media_por_posicao[posicao] = media
        print(f"  {posicao}: média = {media} (valores: {valores})")

    print("\nCálculo finalizado.")
    return media_por_posicao


def gerar_opponent_stats_por_jogo(game_id: int, opponent_team_id: int) -> dict:
    """
    Gera um dicionário com os pontos por posição do time adversário (opponent_team_id)
    em um jogo específico (game_id).
    """
    opponent_stats = {}

    try:
        boxscore_df = obter_boxscore(game_id)
        if boxscore_df.empty:
            print(f"[AVISO] Boxscore vazio para o jogo {game_id}")
            return {}

        adversarios = boxscore_df[boxscore_df["TEAM_ID"] == opponent_team_id]

        if adversarios.empty:
            print(
                f"[AVISO] Nenhum jogador do time adversário encontrado para {opponent_team_id}"
            )
            return {}

        for _, jogador in adversarios.iterrows():
            posicao = jogador.get("START_POSITION", "").strip().upper()
            pontos = jogador.get("PTS", 0)

            if not posicao:
                continue

            try:
                pontos = float(pontos)
                opponent_stats.setdefault(posicao, []).append(pontos)
            except ValueError:
                continue

        for posicao, pontos_lista in opponent_stats.items():
            opponent_stats[posicao] = round(sum(pontos_lista), 2)

        print(f"[DEBUG] opponent_stats para jogo {game_id}: {opponent_stats}")
        return opponent_stats

    except Exception as e:
        print(f"[ERRO] Falha ao gerar opponent_stats para o jogo {game_id}: {e}")
        return {}
