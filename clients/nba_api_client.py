from utils.globals import requests, BASE_URL
from utils.headers import default_headers


class NBAApiClient:
    """
    NBA API client to fetch data from the NBA API.
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = default_headers

    def get(self, endpoint_obj):
        url = self.base_url + endpoint_obj.endpoint
        try:
            print(f"[NBAApiClient] Requesting: {url}")
            if endpoint_obj.params:
                print(f"[NBAApiClient] With params: {endpoint_obj.params}")
            response = requests.get(url, params=endpoint_obj.params, headers=self.headers, timeout=10)
            response.raise_for_status()
            print("[NBAApiClient] Request successful.")
            
            return response.json()
        except Exception as e:
            print(f"[NBAApiClient] Request failed: {e}")
            return {}