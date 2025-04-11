from utils.globals import cloudscraper


def get_with_cloudscraper(url, params=None):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    })

    headers = {
        "Host": "stats.nba.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "x-nba-stats-token": "true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "x-nba-stats-origin": "stats",
        "Origin": "https://www.nba.com",
        "Referer": "https://www.nba.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = scraper.get(url, params=params, headers=headers, timeout=15)
        print(f"🔍 Status code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Erro ao acessar a URL: {url}")
            print("📄 Conteúdo da resposta:", response.text[:500])
            return None

        return response.json()

    except Exception as e:
        print(f"❌ Erro na requisição com cloudscraper: {e}")
        return None