from services.analysis_service import (
    adicionar_opponent_stats_ao_dataframe,
    analisar_defesa_por_posicao,
    analisar_desempenho,
    analisar_jogador,
    comparar_jogadores,
    minutos_jogados,
    sugerir_aposta_com_base_no_score,
)
from services.defense_analysis_service import calcular_media_pontos_sofridos_por_posicao
from services.display_service import exibir_resumo
from services.game_analysis_service import exibir_analise_jogo
from services.game_service import (
    buscar_game_log,
    buscar_posicao_jogador,
    listar_jogos_hoje,
)
from services.player_service import buscar_jogadores_por_time, buscar_player_id
from services.time_service import buscar_ultimos_jogos, comparar_times
from utils.exporter import exportar_df_para_csv
from utils.formatters import get_team_id_by_name
from utils.globals import os, tabulate
from utils.logger import setup_logger

logger = setup_logger("nba_scraper")


def main():
    print("🏀 Bem-vindo ao NBA Scraper!")

    print("\nEscolha a análise:")
    print("1. Analisar jogadores")
    print("2. Analisar times")
    escolha = input("Digite sua opção (1 ou 2): ")

    if escolha == "1":
        jogador1 = input(f"Digite o nome do primeiro jogador: ").strip()
        jogador2 = input(f"Digite o nome do segundo jogador: ").strip()
        num_jogos = int(
            input("Quantos jogos recentes deseja analisar? (padrão = 5): ") or 5
        )

        output_dir = os.path.join("outputs", "comparativos", "jogadores")
        os.makedirs(output_dir, exist_ok=True)

        id1 = buscar_player_id(jogador1)
        id2 = buscar_player_id(jogador2)

        if id1 and id2:
            df1 = buscar_game_log(id1)
            df2 = buscar_game_log(id2)

            resumo1 = analisar_desempenho(df1, num_jogos)
            resumo2 = analisar_desempenho(df2, num_jogos)

            pos1 = buscar_posicao_jogador(id1)
            pos2 = buscar_posicao_jogador(id2)

            exibir_resumo(jogador1, resumo1, pos1)
            exibir_resumo(jogador2, resumo2, pos2)

            df1["MIN"] = df1["MIN"].apply(minutos_jogados)
            df2["MIN"] = df2["MIN"].apply(minutos_jogados)

            sugestao1 = sugerir_aposta_com_base_no_score(resumo1, pos1)
            sugestao2 = sugerir_aposta_com_base_no_score(resumo2, pos2)

            print(f"💡 Sugestão de aposta para {jogador1}: {sugestao1}")
            print(f"💡 Sugestão de aposta para {jogador2}: {sugestao2}")

            comparativo = comparar_jogadores(
                df1, df2, jogador1=jogador1, jogador2=jogador2, pos1=pos1, pos2=pos2
            )
            print("\n✅ Comparação finalizada com sucesso.")
            print(
                tabulate(
                    comparativo.round(2),
                    headers="keys",
                    tablefmt="pretty",
                    floatfmt=".2f",
                )
            )

            estatisticas_df1 = analisar_jogador(df1, nome_jogador=jogador1)
            estatisticas_df2 = analisar_jogador(df2, nome_jogador=jogador2)

            nome_arquivo1 = "estatisticas_" + jogador1.strip().replace(" ", "_").lower()
            nome_arquivo2 = "estatisticas_" + jogador2.strip().replace(" ", "_").lower()

            exportar_df_para_csv(estatisticas_df1, nome_arquivo1, output_dir)
            exportar_df_para_csv(estatisticas_df2, nome_arquivo2, output_dir)

            nome_arquivo = (
                f"{jogador1.replace(' ', '_')}_vs_{jogador2.replace(' ', '_')}.csv"
            )
            caminho_arquivo = os.path.join(output_dir, nome_arquivo)

            comparativo.index.name = "Nome do Jogador"
            comparativo.to_csv(caminho_arquivo, index=True, encoding="utf-8-sig")
            print(f"\n📁 Comparativo exportado com sucesso para: {caminho_arquivo}")
            logger.info(f"Exportado comparativo de jogadores para {caminho_arquivo}")

        else:
            print("❌ Um dos jogadores não foi encontrado.")
            logger.error(
                "Erro ao encontrar um dos jogadores: %s ou %s", jogador1, jogador2
            )

    elif escolha == "2":
        print("\n=== Jogos de hoje ===")
        jogos = listar_jogos_hoje()

        if not jogos:
            print("❌ Nenhum jogo encontrado para hoje.")
            logger.warning("Nenhum jogo encontrado para hoje.")
            return

        for idx, jogo in enumerate(jogos, 1):
            print(f"{idx}. {jogo['resumo']}")

        escolha = int(input("\nDigite o número do jogo que deseja analisar: "))
        if escolha < 1 or escolha > len(jogos):
            print("❌ Escolha inválida.")
            logger.warning("Escolha inválida no menu de jogos.")
            return

        # jogo_formatado = jogos[escolha - 1].replace("🏠 ", "").replace("🛫 ", "").strip()
        # time1, time2 = jogo_formatado.split(" vs ")
        time1 = jogos[escolha - 1]["away_team_name"]
        time2 = jogos[escolha - 1]["home_team_name"]
        num_jogos = int(
            input("Quantos jogos recentes deseja analisar? (padrão = 5): ") or 5
        )

        print(f"\nAnalisando os últimos {num_jogos} jogos de {time1} e {time2}...")
        logger.info(f"Analisando confronto: {time1} vs {time2}")

        team_id1 = get_team_id_by_name(time1)
        team_id2 = get_team_id_by_name(time2)

        jogos_time1 = buscar_ultimos_jogos(team_id1, num_jogos)
        jogos_time2 = buscar_ultimos_jogos(team_id2, num_jogos)

        print(f"\n📊 Análise do {time1}:")
        print(jogos_time1)
        print(f"\n📊 Análise do {time2}:")
        print(jogos_time2)

        comparativo_times = comparar_times(jogos_time1, jogos_time2)
        print("\n✅ Comparação entre os times finalizada com sucesso.")
        print(
            tabulate(
                comparativo_times.round(2),
                headers="keys",
                tablefmt="pretty",
                floatfmt=".2f",
            )
        )

        output_dir = os.path.join("outputs", "comparativos", "times")
        os.makedirs(output_dir, exist_ok=True)

        nome_arquivo = f"{time1.replace(' ', '_')}_vs_{time2.replace(' ', '_')}.csv"
        caminho_arquivo = os.path.join(output_dir, nome_arquivo)

        print("[ETAPA] Adicionando opponent_stats ao DataFrame de jogos...")
        jogos_df1 = adicionar_opponent_stats_ao_dataframe(jogos_time1)
        jogos_df2 = adicionar_opponent_stats_ao_dataframe(jogos_time2)

        print("[ETAPA] Calculando média de pontos sofridos por posição...")
        media_posicao_team1 = calcular_media_pontos_sofridos_por_posicao(jogos_df1)
        media_posicao_team2 = calcular_media_pontos_sofridos_por_posicao(jogos_df2)

        print("[RESULTADO FINAL] Média de pontos sofridos por posição:")
        print(media_posicao_team1)
        print(media_posicao_team2)

        media_pg_team1 = analisar_defesa_por_posicao(jogos_time1)
        media_pg_team2 = analisar_defesa_por_posicao(jogos_time2)
        print(f"Média de pontos sofridos contra PGs: {media_pg_team1}")
        print(f"Média de pontos sofridos contra PGs: {media_pg_team2}")

        comparativo_times.index.name = "Time"
        comparativo_times.to_csv(caminho_arquivo, index=True, encoding="utf-8-sig")
        print(
            f"\n📁 Comparativo entre os times exportado com sucesso para: {caminho_arquivo}"
        )
        logger.info(f"Exportado comparativo entre times para {caminho_arquivo}")

        jogadores_time1 = buscar_jogadores_por_time(team_id1)
        jogadores_time2 = buscar_jogadores_por_time(team_id2)
        print(f"\n🔍 Analisando os jogadores do confronto {time1} vs {time2}...\n")
        exibir_analise_jogo(jogadores_time1, jogadores_time2, time1, time2)

    else:
        print(
            "❌ Opção inválida. Por favor, escolha '1' para jogadores ou '2' para times."
        )
        logger.warning("Opção inválida selecionada no menu principal.")


if __name__ == "__main__":
    main()
