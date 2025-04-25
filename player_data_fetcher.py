from clients.player_endpoint import PlayerEndpoint
from database.db_manager import DBManager

player_endpoint = PlayerEndpoint()
db = DBManager()


def get_all_players():
    response = player_endpoint.get_all_players()

    if not response:
        print("[WARNING] Não foi possível obter a lista de jogadores.")
        return []

    # print("[DEBUG] Resposta bruta de get_all_players():")
    # print(response)

    try:
        players_raw = response["resultSets"][0]["rowSet"]
        headers = response["resultSets"][0]["headers"]

        headers = [header.upper() for header in headers]
        players = [dict(zip(headers, row)) for row in players_raw]

        return players
    except (KeyError, IndexError) as e:
        print(f"[ERROR] Erro ao processar resposta dos jogadores: {e}")
        raise ValueError(f"[ERROR] Erro ao processar resposta dos jogadores: {e}")


def get_player_profile(player_id):
    response = player_endpoint.get_player_profile(player_id)

    if not response:
        print("[WARNING] Não foi possível obter os dados do jogadores.")
        return []

    # print("[DEBUG] Resposta bruta de get_player_profile():")
    # print(response)

    try:
        players_raw = response["resultSets"][0]["rowSet"]
        headers = response["resultSets"][0]["headers"]
        headers = [header.upper() for header in headers]

        normalized_headers = []
        for h in headers:
            h_up = h.upper()
            if h_up == "PERSON_ID":
                h_up = "PLAYER_ID"
            normalized_headers.append(h_up)

        player_profile = [dict(zip(normalized_headers, row)) for row in players_raw]

        return player_profile
    except (KeyError, IndexError) as e:
        print(f"[ERROR] Erro ao processar resposta dos jogadores: {e}")
        raise ValueError(f"[ERROR] Erro ao processar resposta dos jogadores: {e}")


def get_all_players_season_stats():
    response = player_endpoint.get_all_players_season_stats()

    if not response:
        print("[WARNING] Não foi possível obter os dados da season.")
        return []

    print("[DEBUG] Resposta bruta de get_all_players_season_stats():")
    print(response)

    try:
        players_raw = response["resultSets"][0]["rowSet"]
        headers = response["resultSets"][0]["headers"]
        headers = [header.upper() for header in headers]
        players_season_stats = [dict(zip(headers, row)) for row in players_raw]

        # normalized_headers = []
        # for h in headers:
        #     h_up = h.upper()
        #     if h_up == "PERSON_ID":
        #         h_up = "PLAYER_ID"
        #     normalized_headers.append(h_up)

        # player_profile = [dict(zip(normalized_headers, row)) for row in players_raw]

        return players_season_stats
    except (KeyError, IndexError) as e:
        print(f"[ERROR] Erro ao processar resposta dos season status: {e}")
        raise ValueError(f"[ERROR] Erro ao processar resposta de season status: {e}")


def fetch_and_store_player_data():
    players = get_all_players()
    if not players:
        print("[ERROR] Nenhum jogador encontrado.")
        return

    print(f"[INFO] Encontrados {len(players)} jogadores. Iniciando coleta...")

    for player in players:
        player_id = player.get("PERSON_ID")
        full_name = player.get("DISPLAY_FIRST_LAST")

        print(f"[INFO] Coletando dados de: {full_name} (ID: {player_id})")

        try:
            gamelog_response = player_endpoint.get_player_gamelog(player_id)
            print(f"[DEBUG] Resposta de gamelog para {full_name} (ID: {player_id}): {gamelog_response}")

            if gamelog_response:
                gamelog_data = gamelog_response["resultSets"][0]
                print(f"[DEBUG] Dados de gamelog para {full_name} (ID: {player_id}): {gamelog_data}")
                db.save_game_logs(gamelog_data["rowSet"], gamelog_data["headers"])

            profile_list = get_player_profile(player_id)
            print(f"[DEBUG] Resposta de perfil para {full_name} (ID: {player_id}): {profile_list}")            

            if not profile_list:
                print(f"❌ Erro no perfil para {full_name} (ID: {player_id}) — vazio")
                continue

            headers = list(profile_list[0].keys())
            db.save_player_profile(profile_list, headers)
            
            print(f"✅ Perfil salvo/atualizado: {profile_list[0]['DISPLAY_FIRST_LAST']}")

            # all_stats = get_all_players_season_stats()
            # stats = next((s for s in all_stats if s["PLAYER_ID"] == player["id"]), None)
            # if stats:
            #     db.save_season_stats(stats["rowSet"], stats["headers"])
            #     print(f"[INFO] Stats para {player['name']} encontrados.")
            # else:
            #     print(f"[WARNING] Stats não encontrados para {player['name']}.")

            # season_stats = get_all_players_season_stats(player_id)
            # print(f"[DEBUG] Resposta de season stats para {full_name} (ID: {player_id}): {season_stats}")
            # if season_stats and season_stats["resultSets"]:
            #     row = season_stats["resultSets"][0]["rowSet"][-1]  # temporada mais recente
            #     headers = season_stats["resultSets"][0]["headers"]
            #     db.save_season_stats(row, headers)
            #     print("✅ Stats da temporada salvos.")
            # else:
            #     print("❌ Erro nas stats da temporada")
        except Exception as e:
            print(f"[ERROR] Falha ao processar jogador {full_name} (ID: {player_id}): {e}")
            raise ValueError(f"Sem dados para o jogador {full_name} (ID: {player_id})")


if __name__ == "__main__":
    fetch_and_store_player_data()
