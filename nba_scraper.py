

url = "https://stats.nba.com/stats/leagueLeaders"
params = {
    "LeagueID": "00",
    "PerMode": "PerGame",
    "Scope": "S",
    "Season": "2023-24",
    "SeasonType": "Regular Season",
    "StatCategory": "PTS"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Extrair os dados da resposta
headers = data['resultSet']['headers']
players = data['resultSet']['rowSet']

# Criar o DataFrame
df = pd.DataFrame(players, columns=headers)
# df.to_csv("dados_nba.csv", index=False)




jogador1 = "Shai Gilgeous-Alexander"
jogador2 = "Jayson Tatum"

id1 = buscar_player_id(jogador1)
id2 = buscar_player_id(jogador2)

print(f"ID encontrado: {id1}")

if id1:
    url = f"https://stats.nba.com/stats/playergamelog?PlayerID={id1}&Season=2024-25&SeasonType=Regular+Season"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nba.com/",
        "x-nba-stats-origin": "stats",
        "x-nba-stats-token": "true"
    }

    import requests
    response = requests.get(url, headers=headers)
    print(f"Status da resposta: {response.status_code}")
    print("Conteúdo (resumo):")
    print(response.text[:500])  # só um pedaço pra não lotar

    data = response.json()
    print("Chaves disponíveis na resposta:")
    print(data.keys())

if id1 and id2:
    df1 = buscar_game_log(id1)
    df2 = buscar_game_log(id2)

    resumo1 = analisar_desempenho(df1)
    resumo2 = analisar_desempenho(df2)

    score1 = calcular_score_confianca(
        resumo1["media_pontos"],
        resumo1["desvio_pontos"],
        resumo1["media_minutos"],
        resumo1["jogou_ontem"]
    )

    score2 = calcular_score_confianca(
        resumo2["media_pontos"],
        resumo2["desvio_pontos"],
        resumo2["media_minutos"],
        resumo2["jogou_ontem"]
    )

    exibir_resumo(jogador1, score1, resumo1)
    exibir_resumo(jogador2, score2, resumo2)

    # Atualiza os DataFrames com MIN já tratado
    df1["MIN"] = df1["MIN"].apply(minutos_jogados)
    df2["MIN"] = df2["MIN"].apply(minutos_jogados)

    # Exibe a comparação final
    comparativo = comparar_jogadores(df1, df2, nome1=jogador1, nome2=jogador2)
    print("\n🏀 Comparação entre jogadores:")
    print(comparativo.round(2))
    

jogador = "Jayson Tatum"
id_jogador = buscar_player_id(jogador)
if id_jogador:
    jogos = buscar_game_log(id_jogador)
    analise = analisar_desempenho(jogos)

    score = calcular_score_confianca(
        analise["media_pontos"],
        analise["desvio_pontos"],
        analise["media_minutos"],
        analise["jogou_ontem"]
    )

    exibir_resumo(jogador, score, analise)

    print("\nComparativo de Desempenho entre Jogadores:")
    print(tabulate(comparativo.round(2), headers="keys", tablefmt="pretty", floatfmt=".2f"))
