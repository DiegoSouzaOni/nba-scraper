from utils.globals import pd
from services.game_service import buscar_game_log


def analisar_jogo_em_casa_ou_fora(team_id, em_casa=True, num_jogos=5):
    """
    Filtra os últimos jogos em casa ou fora de um time.
    """
    df = buscar_game_log(team_id)

    if em_casa:
        df_filtrado = df[df['HOME'] == 1]
    else:
        df_filtrado = df[df['HOME'] == 0]

    return df_filtrado.head(num_jogos)


def analisar_confronto_direto(team1_id, team2_id, meses=2):
    """
    Retorna confrontos diretos entre os times nos últimos X meses.
    """
    df1 = buscar_game_log(team1_id)
    df2 = buscar_game_log(team2_id)

    df = pd.merge(df1, df2, on='GAME_ID')
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])

    data_limite = pd.Timestamp.today() - pd.DateOffset(months=meses)
    confrontos = df[df['GAME_DATE'] > data_limite]

    return confrontos
