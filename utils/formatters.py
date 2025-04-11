def interpretar_score(score):
    if score >= 90:
        return "🔥 Extremamente confiável"
    elif score >= 80:
        return "✅ Confiável"
    elif score >= 70:
        return "⚠️ Médio risco"
    else:
        return "🚨 Pouco confiável"


def interpretar_consistencia(desvio_padrao):
    if desvio_padrao <= 2.0:
        return "Alta 🟢"
    elif desvio_padrao <= 4.0:
        return "Média 🟡"
    else:
        return "Baixa 🔴"


TEAM_ID_TO_NAME = {
    1610612737: "Atlanta Hawks",
    1610612738: "Boston Celtics",
    1610612751: "Brooklyn Nets",
    1610612766: "Charlotte Hornets",
    1610612741: "Chicago Bulls",
    1610612739: "Cleveland Cavaliers",
    1610612742: "Dallas Mavericks",
    1610612743: "Denver Nuggets",
    1610612765: "Detroit Pistons",
    1610612744: "Golden State Warriors",
    1610612745: "Houston Rockets",
    1610612754: "Indiana Pacers",
    1610612746: "Los Angeles Clippers",
    1610612747: "Los Angeles Lakers",
    1610612763: "Memphis Grizzlies",
    1610612748: "Miami Heat",
    1610612749: "Milwaukee Bucks",
    1610612750: "Minnesota Timberwolves",
    1610612740: "New Orleans Pelicans",
    1610612752: "New York Knicks",
    1610612760: "Oklahoma City Thunder",
    1610612753: "Orlando Magic",
    1610612755: "Philadelphia 76ers",
    1610612756: "Phoenix Suns",
    1610612757: "Portland Trail Blazers",
    1610612758: "Sacramento Kings",
    1610612759: "San Antonio Spurs",
    1610612761: "Toronto Raptors",
    1610612762: "Utah Jazz",
    1610612764: "Washington Wizards"
}


STAT_LABELS = {
    "PTS": "Pontos",
    "REB": "Rebotes",
    "AST": "Assistências",
    "STL": "Roubos de Bola",
    "BLK": "Tocos",
    "TO": "Turnovers",
    "FG_PCT": "Aproveitamento de Arremessos",
    "FG3M": "Cestas de 3 pontos",
    "MIN": "Minutos Jogados"
}


def get_team_name(team_id: int) -> str:
    return TEAM_ID_TO_NAME.get(team_id, f"ID {team_id}")


def get_team_id_by_name(team_name: str) -> int:
    for team_id, name in TEAM_ID_TO_NAME.items():
        if name == team_name:
            return team_id
    return None


def traduzir_estatisticas(estatisticas_dict):
    """
    Recebe um dicionário com siglas e retorna um novo com labels traduzidos.
    """
    from .formatters import STAT_LABELS

    if 'estatística' in estatisticas_dict.columns:
        estatisticas_dict['estatística'] = estatisticas_dict['estatística'].replace(STAT_LABELS)

    return estatisticas_dict