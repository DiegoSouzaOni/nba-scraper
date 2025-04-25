from playwright.sync_api import sync_playwright
import csv


def scrape_nba_stats():
    with sync_playwright() as p:
        # Lançando o navegador
        browser = p.chromium.launch(headless=True)  # headless=True para não abrir a janela
        page = browser.new_page()

        # Acessando a página de estatísticas
        url = "https://www.nba.com/stats/players/traditional?SeasonType=Playoffs"
        page.goto(url)

        # Alterando o tempo de espera para 60 segundos
        page.wait_for_selector("table", timeout=30000)


        # Extrai os dados da tabela
        rows = page.query_selector_all("table tbody tr")  # Obtém todas as linhas da tabela

        stats = []

        for row in rows:
            cols = row.query_selector_all("td")  # Obtém todas as células da linha
            stats_row = [col.inner_text() for col in cols]  # Pega o texto de cada célula
            stats.append(stats_row)

        # Fecha o navegador
        browser.close()

        # Salva os dados em um arquivo CSV
        with open("nba_playoffs_stats.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Player", "Team", "Games", "Minutes", "Points", "Rebounds", "Assists", "Steals", "Blocks", "Turnovers", "Personal Fouls", "Plus/Minus"])  # Cabeçalho da tabela
            writer.writerows(stats)

        print("[INFO] Dados extraídos e salvos com sucesso!")


scrape_nba_stats()
