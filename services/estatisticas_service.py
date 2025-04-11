from utils.globals import pd
from services.boxscore_service import obter_boxscore_summary, extrair_pontos_quarto_e_sofridos
from utils.formatters import interpretar_consistencia


def calcular_medianas_e_estatisticas(df, estatisticas=None):
    """
    Calcula média, mediana e desvio padrão para colunas numéricas selecionadas.
    Retorna um DataFrame organizado.
    """
    if estatisticas is None:
        estatisticas = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'FG_PCT', 'FG3M', 'MIN']

    resultados = []

    for coluna in estatisticas:
        if coluna in df.columns:
            resultados.append({
                'estatística': coluna,
                'média': round(df[coluna].mean(), 2),
                'mediana': round(df[coluna].median(), 2),
                'desvio_padrão': round(df[coluna].std(), 2),
                'consistência': interpretar_consistencia(df[coluna].std())
            })

    return pd.DataFrame(resultados)


def calcular_medias_boxscore_summary(game_log_df, team_id):
    lista_pts = []
    lista_pts_sofridos = []
    lista_q1 = []
    lista_q1_sofridos = []

    for _, jogo in game_log_df.iterrows():
        game_id = jogo["Game_ID"]
        df_summary = obter_boxscore_summary(game_id)

        if df_summary is not None:
            team_data = df_summary[df_summary["TEAM_ID"] == team_id]
            adversario_data = df_summary[df_summary["TEAM_ID"] != team_id]

            if not team_data.empty and not adversario_data.empty:
                try:                    
                    pts = int(team_data.iloc[0]["PTS"])
                    pts_sofridos = int(adversario_data.iloc[0]["PTS"])
                    q1, q1_sofrido = extrair_pontos_quarto_e_sofridos(df_summary, team_id)

                    lista_pts.append(pts)
                    lista_pts_sofridos.append(pts_sofridos)
                    lista_q1.append(q1)
                    lista_q1_sofridos.append(q1_sofrido)
                except Exception as e:
                    print(f"Erro ao extrair pontos: {e}")

    return (
        sum(lista_pts) / len(lista_pts) if lista_pts else None,
        sum(lista_pts_sofridos) / len(lista_pts_sofridos) if lista_pts_sofridos else None,
        sum(lista_q1) / len(lista_q1) if lista_q1 else None,
        sum(lista_q1_sofridos) / len(lista_q1_sofridos) if lista_q1_sofridos else None,
    )
