from services.defense_analysis_service import calcular_media_pontos_sofridos_por_posicao
from services.estatisticas_service import calcular_medianas_e_estatisticas
from utils.formatters import interpretar_score, traduzir_estatisticas
from utils.globals import pd


def calcular_score_confianca(media, desvio, minutos, jogou_ontem):
    peso_media = 0.4
    peso_desvio = 0.3
    peso_minutos = 0.2
    peso_descanso = 0.1

    score_desvio = max(0, 100 - desvio * 10)
    score_minutos = min(100, minutos / 36 * 100)
    score_descanso = 100 if not jogou_ontem else 60

    score_total = (
        peso_media * media
        + peso_desvio * score_desvio
        + peso_minutos * score_minutos
        + peso_descanso * score_descanso
    )

    return round(score_total, 2)


def analisar_jogador(game_log_df, nome_jogador=None):
    if game_log_df.empty:
        print("❌ Nenhum dado disponível para o jogador.")
        return

    if nome_jogador:
        print(f"\n📊 Análise estatística de {nome_jogador}\n")
    else:
        print("\n📊 Análise estatística do jogador\n")

    estatisticas_df = calcular_medianas_e_estatisticas(game_log_df)
    estatisticas_df = traduzir_estatisticas(estatisticas_df)

    print(estatisticas_df.to_string(index=True))

    return estatisticas_df


def minutos_jogados(valor):
    try:
        if isinstance(valor, str) and ":" in valor:
            return float(valor.split(":")[0]) + float(valor.split(":")[1]) / 60
        elif isinstance(valor, (int, float)):
            return float(valor)
        else:
            return 0.0
    except:
        return 0.0


def analisar_desempenho(game_log_df, quantidade_jogos=5, estatistica="PTS"):
    """Analisa o desempenho do jogador com base nos últimos N jogos."""

    jogos_recentes = game_log_df.head(quantidade_jogos).copy()
    jogos_recentes["MIN"] = jogos_recentes["MIN"].apply(minutos_jogados)

    jogos_jogados = jogos_recentes[jogos_recentes["MIN"] > 0]
    total_jogos_disputados = len(jogos_jogados)

    media_pontos = jogos_jogados[estatistica].mean()
    desvio_pontos = jogos_jogados[estatistica].std()
    media_minutos = jogos_jogados["MIN"].mean()
    media_rebotes = jogos_jogados["REB"].mean()
    media_assistencias = jogos_jogados["AST"].mean()

    jogou_ontem = False
    if len(jogos_jogados) > 1:
        data_ultimo_jogo = pd.to_datetime(jogos_jogados.iloc[0]["GAME_DATE"])
        data_anterior = pd.to_datetime(jogos_jogados.iloc[1]["GAME_DATE"])
        jogou_ontem = (data_ultimo_jogo - data_anterior).days == 1

    score = calcular_score_confianca(
        media_pontos, desvio_pontos, media_minutos, jogou_ontem
    )

    score_legenda = interpretar_score(score)

    return {
        "media_pontos": media_pontos,
        "desvio_pontos": desvio_pontos,
        "media_minutos": media_minutos,
        "media_rebotes": media_rebotes,
        "media_assistencias": media_assistencias,
        "jogos_analisados": quantidade_jogos,
        "jogos_disputados": total_jogos_disputados,
        "jogou_ontem": jogou_ontem,
        "score": round(score, 1),
        "score_legenda": score_legenda,
        "jogos_jogados": jogos_jogados[
            ["GAME_DATE", "MATCHUP", "PTS", "REB", "AST", "MIN"]
        ].to_dict(orient="records"),
    }


def calcular_estatisticas(df):
    return {
        "Pontos": df["PTS"].mean(),
        "Rebotes": df["REB"].mean(),
        "Assistências": df["AST"].mean(),
        "Minutos": df["MIN"].mean(),
        "FG%": df["FG_PCT"].mean() * 100,
        "3P%": df["FG3_PCT"].mean() * 100,
        "FT%": df["FT_PCT"].mean() * 100,
    }


def comparar_jogadores(
    df_jogador1,
    df_jogador2,
    jogador1="Jogador 1",
    jogador2="Jogador 2",
    pos1="None",
    pos2="None",
):
    """Compara estatísticas entre dois jogadores usando DataFrames."""

    stats1 = calcular_estatisticas(df_jogador1)
    stats2 = calcular_estatisticas(df_jogador2)

    return pd.DataFrame(
        [stats1, stats2], index=[f"{jogador1} ({pos1})", f"{jogador2} ({pos2})"]
    )


def sugerir_aposta_com_base_no_score(resumo, posicao):
    score = resumo["score"]
    media = resumo["media_pontos"]
    assistencias = resumo["media_assistencias"]
    rebotes = resumo["media_rebotes"]
    desvio = resumo["desvio_pontos"]

    if posicao in ["C", "PF"]:  # Pivô (Center) ou Ala-Pivô
        ajuste_risco = 0.1  # Jogadores mais focados em rebotes e pontos
    elif posicao in ["PG", "SG"]:  # Armador (Point Guard) ou Ala (Shooting Guard)
        ajuste_risco = (
            0.2  # Mais arriscado, pois sua produção pode ser mais imprevisível
        )
    else:
        ajuste_risco = 0.15  # Outras posições, risco moderado

    if score >= 90:
        tipo = "Mais de"
        risco = "🔒 Baixo" if ajuste_risco < 0.15 else "🟡 Médio"
    elif score >= 80:
        tipo = "Mais de"
        risco = "🟡 Médio" if ajuste_risco < 0.2 else "🟠 Médio-Alto"
    elif score >= 70:
        tipo = "Evitar ou Menos de"
        risco = "🟠 Médio-Alto" if ajuste_risco < 0.25 else "🔴 Alto"
    else:
        tipo = "Menos de"
        risco = "🔴 Alto"

    linha_pts = sugerir_linha_aposta(
        media, desvio, mercado="Pontos", tipo=tipo, risco=risco
    )
    linha_ast = sugerir_linha_aposta(
        assistencias, desvio, mercado="Assistências", tipo=tipo, risco=risco
    )
    linha_reb = sugerir_linha_aposta(
        rebotes, desvio, mercado="Rebotes", tipo=tipo, risco=risco
    )

    return {
        "Pontos": f"{linha_pts['tipo_aposta']} {linha_pts['linha_sugerida']} {linha_pts['mercado']} ({linha_pts['risco']})",
        "Rebotes": f"{linha_ast['tipo_aposta']} {linha_ast['linha_sugerida']} {linha_ast['mercado']} ({linha_ast['risco']})",
        "Assistencias": f"{linha_reb['tipo_aposta']} {linha_reb['linha_sugerida']} {linha_reb['mercado']} ({linha_reb['risco']})",
    }


def sugerir_linha_aposta(
    media, desvio, mercado="Pontos", tipo="Mais de", risco="🔒 Baixo"
):
    """
    Sugere uma linha de aposta segura com base na média e desvio padrão,
    considerando o tipo de mercado (ex: Pontos, Assistências, Rebotes).
    """
    linha_segura = round(media - desvio, 1)

    # Definir mínimo razoável por tipo de mercado
    limites_minimos = {"Pontos": 5, "Assistências": 2, "Rebotes": 3}

    # Valor mínimo seguro para o mercado atual
    minimo = limites_minimos.get(mercado, 3)

    if linha_segura < minimo:
        linha_segura = round(media * 0.8, 1)

    return {
        "tipo_aposta": tipo,
        "linha_sugerida": linha_segura,
        "mercado": mercado,
        "risco": risco,
    }


def analisar_defesa_por_posicao(jogos_df: pd.DataFrame) -> float:
    """
    Analyze how many points a team usually allows to a specific position.

    Args:
        team_name (str): Name of the team to analyze.
        position (str): Position to evaluate (e.g., 'PG', 'SG', 'SF', 'PF', 'C').
        season (str): NBA season (default is '2024-25').

    Returns:
        float: Average points allowed to the given position.
    """
    try:
        media = calcular_media_pontos_sofridos_por_posicao(jogos_df)
        return media
    except Exception as e:
        print(f"Error analyzing defense by position for {jogos_df}: {e}")
        return 0.0
