# services/game_analysis_service.py (ou similar)

from services.game_service import buscar_game_log, buscar_posicao_jogador
from services.analysis_service import analisar_desempenho
from services.display_service import exibir_resumo
from services.player_service import buscar_player_id


def analisar_jogadores_da_partida(jogadores, quantidade_jogos=5):
    dados_jogadores = []

    for jogador in jogadores:
        try:
            id_jogador = buscar_player_id(jogador)

            pos1 = buscar_posicao_jogador(id_jogador)
       
            game_log_df = buscar_game_log(id_jogador)
            desempenho = analisar_desempenho(game_log_df, quantidade_jogos)
            desempenho["POSITION"] = pos1
            desempenho["PLAYER"] = jogador

            if desempenho:
                dados_jogadores.append(desempenho)
        except Exception as e:
            print(f"Erro ao analisar {jogador}: {e}")

    return dados_jogadores


def exibir_analise_jogo(jogadores_time_a, jogadores_time_b, nome_time_a, nome_time_b):
    print(f"\n📋 Análise dos jogadores do {nome_time_a}:\n")
    dados_a = analisar_jogadores_da_partida(jogadores_time_a)
    for resumo in dados_a:
        exibir_resumo(resumo["PLAYER"], resumo, resumo["POSITION"])

    print(f"\n📋 Análise dos jogadores do {nome_time_b}:\n")
    dados_b = analisar_jogadores_da_partida(jogadores_time_b)
    for resumo in dados_b:
        exibir_resumo(resumo["PLAYER"], resumo, resumo["POSITION"])
