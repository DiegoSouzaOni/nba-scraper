def formatar_season_type_para_url(season_type: str) -> str:
    """
    Converte um tipo de temporada da NBA para o formato usado nas URLs da API.
    Exemplo: "Regular Season" -> "Regular+Season"
    """
    return season_type.replace(" ", "+")


def traduzir_posicao_para_ptbr(posicao_original: str) -> str:
    """
    Traduz a posição original de um jogador da NBA para português.
    """
    posicoes_ptbr = {
        "Guard": "Armador",
        "Forward": "Ala",
        "Center": "Pivô",
        "Guard-Forward": "Armador / Ala",
        "Forward-Guard": "Ala / Armador",
        "Forward-Center": "Ala / Pivô",
        "Center-Forward": "Pivô / Ala",
    }
    return posicoes_ptbr.get(posicao_original, posicao_original)