import json

from utils.globals import pd


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
